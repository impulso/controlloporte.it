"""
The API routes for v2
"""

from typing import Annotated

from litestar import MediaType, Request, get, post
from litestar.params import Body
from litestar.status_codes import HTTP_200_OK

from app.helpers.exceptions import JsonAPIException
from app.helpers.nat_scan import format_quick_nat_scan_report, run_quick_nat_scan
from app.helpers.query import check_ddns, get_requester, query_address
from app.schemas.api import (
    APIResponseSchema,
    APISchema,
    DDNSCheckSchema,
    DDNSResponseSchema,
    HostAnnotation,
    NATScanRequestSchema,
    NATScanResponseSchema,
    PortAnnotation,
    PortCheckStrAnnotation,
    RequesterAnnotation,
)


@get("/api/me", media_type=MediaType.TEXT, sync_to_thread=False)
def my_ip(request: Request) -> RequesterAnnotation:
    """
    Returns the requester IP.

    Auto-detects the public IP address associated with the incoming request.
    """
    return get_requester(request)


@get("/api/{host:str}/{port:int}", media_type=MediaType.TEXT, sync_to_thread=False)
def get_port_check(
    request: Request, host: HostAnnotation, port: PortAnnotation
) -> PortCheckStrAnnotation:
    """
    Legacy plain text `GET` endpoint to check one TCP port.

    Use `me` as the host to auto-detect the requester IP address based
    on the incoming request.

    This endpoint returns `True` or `False` as `text/plain`.
    For JSON responses with latency, use `/api/check/{host}/{port}`.
    """
    host = get_requester(request) if host == "me" else host
    return str(query_address(host, [port])[0].get("status"))


@get(
    "/api/check/{host:str}/{port:int}",
    media_type=MediaType.JSON,
    status_code=HTTP_200_OK,
    sync_to_thread=False,
)
def get_port_check_json(
    request: Request, host: HostAnnotation, port: PortAnnotation
) -> APIResponseSchema:
    """
    JSON `GET` endpoint to check one TCP port.

    Use `me` as the host to auto-detect the requester IP address based
    on the incoming request.

    DNS resolution is performed before the TCP check. The response uses the same
    structure as `POST /api/query`. Open ports include `latency_ms`, the TCP
    connection latency in milliseconds. Closed or unreachable ports return
    `latency_ms: null`.
    """
    resolved_host = get_requester(request) if host == "me" else host
    return post_helper(resolved_host, [port])


@post(
    "/api/query",
    media_type=MediaType.JSON,
    status_code=HTTP_200_OK,
    sync_to_thread=False,
)
def query_post(
    request: Request,
    data: Annotated[
        APISchema,
        Body(
            title="Query a resolvable hostname, public IPv4 address, or requester IP",
            description=(
                "Query a resolvable hostname, public IPv4 address, or use `me` "
                "to check the requester public IP address."
            ),
        ),
    ],
) -> APIResponseSchema:
    """
    A `POST` endpoint to query the status of multiple ports on a given hostname
    or IP address.

    This endpoint accepts a JSON payload containing either a public IPv4 address
    or a resolvable hostname, along with an array of TCP port numbers to be checked.
    Use `me` as the host to auto-detect the requester IP address based
    on the incoming request. In that case, the response `host` field contains
    the resolved requester public IP address. The `ports` values must be integers,
    not strings.
    DNS resolution is performed once before the TCP checks, so `latency_ms` does not
    include DNS lookup time. For each port in the array, the endpoint performs a TCP
    connectivity check with a timeout of 1 second per port. Open ports include the
    TCP connection latency in milliseconds. Closed or unreachable ports return
    `latency_ms: null`.
    """
    host = get_requester(request) if data.host == "me" else data.host
    return post_helper(host, data.ports)


@post(
    "/api/controlloDDNS",
    media_type=MediaType.JSON,
    status_code=HTTP_200_OK,
    sync_to_thread=False,
)
def controllo_ddns_post(
    request: Request,
    data: Annotated[
        DDNSCheckSchema,
        Body(
            title="Check a dynamic DNS hostname against the requester IP",
            description=(
                "Resolve a hostname and compare it with the public IP address "
                "detected for the incoming request."
            ),
        ),
    ],
) -> DDNSResponseSchema:
    """
    Compare a DNS hostname with the requester public IP address.

    The endpoint resolves the supplied hostname to an IPv4 address and compares it
    with the public IP detected from the request headers. It is useful to verify
    whether a dynamic DNS hostname currently points to the same public IP used by
    the visitor.
    """
    try:
        requester_ip = get_requester(request)
    except ValueError as ex:
        raise JsonAPIException(key="requester_ip", message=str(ex)) from ex

    ddns_check = check_ddns(data.host, requester_ip)
    return DDNSResponseSchema(error=False, msg=None, **ddns_check)


@post(
    "/api/nat/quick-scan",
    media_type=MediaType.JSON,
    status_code=HTTP_200_OK,
    sync_to_thread=True,
)
def quick_nat_scan_post(
    request: Request,
    data: Annotated[
        NATScanRequestSchema,
        Body(
            title="Run a quick NAT scan against the requester public IP",
            description=(
                "Runs a controlled nmap top-ports scan against the requester "
                "public IPv4 address. The target IP is always detected from "
                "the request and cannot be supplied by the client."
            ),
        ),
    ],
) -> NATScanResponseSchema:
    """
    Run a quick NAT scan against the requester public IPv4 address.

    The client must provide explicit consent. The endpoint never accepts a target IP
    from the request body; it scans only the public IP detected from proxy headers.
    """
    if data.consent is not True:
        raise JsonAPIException(
            key="consent",
            message="Devi autorizzare la scansione rapida del tuo IP pubblico.",
        )

    try:
        requester_ip = get_requester(request)
    except ValueError as ex:
        raise JsonAPIException(key="requester_ip", message=str(ex)) from ex

    scan = run_quick_nat_scan(requester_ip)
    report = format_quick_nat_scan_report(scan)
    summary = report.rsplit("\n\n", maxsplit=1)[-1]

    return NATScanResponseSchema(
        error=False,
        msg=None,
        summary=summary,
        report=report,
        **scan.model_dump(),
    )


def post_helper(host: str, ports: list[int]) -> APIResponseSchema:
    """A helper method for returning the `APIResponse`. Also used by the deprecated v1 API"""
    return APIResponseSchema(
        msg=None,
        error=False,
        host=host,
        check=query_address(host, ports),
    )
