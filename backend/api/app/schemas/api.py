"""
The API schemas
"""

from typing import Annotated

from annotated_types import Ge, Le, MaxLen, MinLen
from litestar.openapi.spec import Example
from litestar.params import Parameter
from pydantic import BaseModel, Field

HostAnnotation = Annotated[
    str,
    Parameter(
        description=(
            "Resolvable hostname, public IPv4 address, or `me` to use the "
            "requester public IP address."
        ),
        examples=[
            Example(value="example.com"),
            Example(value="1.1.1.1"),
            Example(value="me"),
        ],
        min_length=1,
        max_length=253,
    ),
    MinLen(1),
    MaxLen(253),
]

PortAnnotation = Annotated[
    int,
    Parameter(
        description="The port number to query",
        examples=[Example(value=443)],
        ge=1,
        le=65535,
    ),
    Ge(1),
    Le(65535),
]

PortCheckStrAnnotation = Annotated[
    str,
    Parameter(
        description="Whether the port was connectable",
        examples=[Example(value="True")],
    ),
]

PortCheckAnnotation = Annotated[
    bool,
    Parameter(
        description="Whether the port was connectable",
        examples=[Example(value=True)],
    ),
]

RequesterAnnotation = Annotated[
    str,
    Parameter(
        description="The IP address of the requester",
        examples=[Example(value="1.1.1.1")],
    ),
]


class APISchema(BaseModel):
    """Schema for the `query_post` endpoint"""

    host: HostAnnotation = Field(
        description=(
            "Resolvable hostname, public IPv4 address, or `me` to check the "
            "requester public IP address."
        ),
        examples=["example.com", "me"],
    )
    ports: list[PortAnnotation] = Field(
        description="TCP port numbers to check. Values must be integers from 1 to 65535.",
        examples=[[80, 443]],
    )


class DDNSCheckSchema(BaseModel):
    """Schema for the `controllo_ddns_post` endpoint"""

    host: HostAnnotation = Field(
        description="Resolvable hostname to compare with the requester public IP.",
        examples=["casa.example.com"],
    )


class NATScanRequestSchema(BaseModel):
    """Schema for requesting a quick NAT scan."""

    consent: bool = Field(
        description=(
            "Explicit user confirmation that they want to scan their detected "
            "public IP address and are authorized to do so."
        ),
        examples=[True],
    )


class APICheckSchema(BaseModel):
    """Schema for the individual results of a check"""

    port: PortAnnotation
    status: PortCheckAnnotation = Field(
        description="Whether the TCP port is open from the public Internet",
        examples=[True],
    )
    latency_ms: int | None = Field(
        default=None,
        description=(
            "TCP connection latency in milliseconds when the port is open. "
            "Null when the port is closed or unreachable."
        ),
        examples=[23],
    )


class NATScanOpenPortSchema(BaseModel):
    """One open TCP port found by the quick NAT scan."""

    port: int = Field(description="TCP port number", examples=[443])
    protocol: str = Field(description="Protocol scanned", examples=["tcp"])
    state: str = Field(description="Nmap state", examples=["open"])
    service: str = Field(description="Detected or known service name", examples=["https"])
    reason: str | None = Field(default=None, description="Nmap reason", examples=["syn-ack"])


class NATScanNotShownSchema(BaseModel):
    """Nmap-style summary of ports not shown in the report."""

    count: int = Field(description="Number of non-open ports not shown", examples=[48])
    state: str = Field(description="Dominant state for non-open ports", examples=["filtered"])
    reason: str = Field(description="Dominant reason for non-open ports", examples=["no-response"])


class NATScanWorkerResponseSchema(BaseModel):
    """Structured response returned by the internal nmap worker."""

    ip: str = Field(description="Requester public IPv4 address", examples=["91.99.156.172"])
    scan_type: str = Field(description="Scan profile", examples=["top_ports"])
    num_ports: int = Field(description="Number of top ports scanned", examples=[50])
    scanned_ports: int = Field(description="Number of TCP ports scanned", examples=[50])
    open_ports: list[NATScanOpenPortSchema]
    not_shown: NATScanNotShownSchema
    duration_ms: int = Field(description="Scan duration in milliseconds", examples=[12340])


class NATScanResponseSchema(NATScanWorkerResponseSchema):
    """Public quick NAT scan response."""

    error: bool = Field(description="Whether an error occurred", examples=[False])
    msg: str | None
    summary: str = Field(
        description="Short human-readable interpretation of the result",
        examples=["Sono state trovate 2 porte raggiungibili dall'esterno."],
    )
    report: str = Field(description="Italian nmap-like report text")


class APIResponseSchema(BaseModel):
    """The schema used for the API response"""

    error: bool = Field(
        description="Whether an error occurred during the check", examples=[False]
    )
    msg: str | None
    check: list[APICheckSchema]
    host: str = Field(
        description=(
            "Host that was checked. When the request uses `me`, this is the "
            "resolved requester public IP address."
        ),
        examples=["example.com", "1.1.1.1"],
    )


class DDNSResponseSchema(BaseModel):
    """The schema used for the DDNS check response"""

    error: bool = Field(
        description="Whether an error occurred during the check", examples=[False]
    )
    msg: str | None
    host: str = Field(
        description="Hostname that was resolved", examples=["casa.example.com"]
    )
    requester_ip: str = Field(
        description="Public IP address detected for the requester",
        examples=["1.2.3.4"],
    )
    resolved_ip: str = Field(
        description="IPv4 address resolved from the hostname",
        examples=["1.2.3.4"],
    )
    match: bool = Field(
        description="Whether the requester public IP matches the hostname resolution",
        examples=[True],
    )


class APIErrorResponseSchema(BaseModel):
    """The error schema used for the API error response"""

    error: bool = Field(description="Whether an error occurred", examples=[True])
    detail: str = Field(description="The error message")
    extra: list[dict] = Field(
        description="The parameter and error this exception relates to"
    )
