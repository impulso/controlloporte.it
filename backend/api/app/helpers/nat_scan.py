"""
Helpers for the quick NAT scan endpoint.
"""

import json
import os
import time
from ipaddress import ip_address
from urllib.error import HTTPError, URLError
from urllib.request import Request as UrlRequest
from urllib.request import urlopen

from app.helpers.exceptions import JsonAPIException
from app.helpers.query import is_address_valid
from app.schemas.api import NATScanWorkerResponseSchema

NAT_SCAN_NUM_PORTS = 50
NAT_SCAN_TYPE = "top_ports"
NAT_SCAN_RATE_LIMIT_SECONDS = int(os.environ.get("NAT_SCAN_RATE_LIMIT_SECONDS", "300"))
NMAP_WORKER_URL = os.environ.get("NMAP_WORKER_URL", "http://nmap-worker:8080/scan")

_last_scan_by_ip: dict[str, float] = {}


def run_quick_nat_scan(requester_ip: str) -> NATScanWorkerResponseSchema:
    """Run the quick NAT scan against the requester public IPv4 address."""
    try:
        parsed_ip = ip_address(requester_ip)
        if parsed_ip.version != 4:
            raise ValueError("IPv6 non è attualmente supportato")
        is_address_valid(requester_ip)
    except Exception as ex:
        raise JsonAPIException(key="requester_ip", message=str(ex)) from ex

    _enforce_rate_limit(requester_ip)

    payload = {
        "ip": requester_ip,
        "scan_type": NAT_SCAN_TYPE,
        "num_ports": NAT_SCAN_NUM_PORTS,
    }
    request = UrlRequest(
        NMAP_WORKER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=45) as response:  # nosec B310 - internal worker URL
            response_payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as ex:
        message = _read_worker_error(ex)
        raise JsonAPIException(key="scan", message=message) from ex
    except (TimeoutError, URLError, json.JSONDecodeError) as ex:
        raise JsonAPIException(
            key="scan",
            message="La scansione non è disponibile in questo momento. Riprova tra poco.",
        ) from ex

    return NATScanWorkerResponseSchema(**response_payload)


def format_quick_nat_scan_report(scan: NATScanWorkerResponseSchema) -> str:
    """Format the scan result as an Italian nmap-like report."""
    lines = [
        f"Report scansione NAT veloce per il tuo IP pubblico ({scan.ip})",
        "",
        (
            f"Non mostrate: {scan.not_shown.count} porte TCP "
            f"{_translate_state(scan.not_shown.state)} "
            f"({_translate_reason(scan.not_shown.reason)})"
        ),
        "",
        "PORTA    STATO   SERVIZIO",
    ]

    for port in scan.open_ports:
        lines.append(
            f"{port.port}/{port.protocol:<3}   {_translate_state(port.state):<6}  "
            f"{port.service}"
        )

    lines.extend(
        [
            "",
            _summary_for_open_ports(len(scan.open_ports), scan.num_ports),
            "",
            "Vuoi verificare una porta specifica?",
            "Usa il test porta dedicato: https://controlloporte.it/me/",
            "",
            "Una porta che ti aspetti aperta risulta chiusa?",
            (
                "Consulta la checklist: "
                "https://controlloporte.it/perche-una-porta-risulta-chiusa/"
            ),
        ]
    )

    return "\n".join(lines)


def _enforce_rate_limit(ip: str) -> None:
    now = time.monotonic()
    last_scan = _last_scan_by_ip.get(ip)
    if last_scan is not None:
        wait_seconds = int(NAT_SCAN_RATE_LIMIT_SECONDS - (now - last_scan))
        if wait_seconds > 0:
            raise JsonAPIException(
                key="rate_limit",
                message=(
                    "Hai già avviato una scansione di recente. "
                    f"Riprova tra {wait_seconds} secondi."
                ),
            )
    _last_scan_by_ip[ip] = now


def _read_worker_error(error: HTTPError) -> str:
    try:
        payload = json.loads(error.read().decode("utf-8"))
        message = payload.get("message")
        if isinstance(message, str) and message:
            return message
    except Exception:
        pass
    return "La scansione non è riuscita. Riprova tra poco."


def _translate_state(state: str) -> str:
    return {
        "open": "aperta",
        "closed": "chiuse",
        "filtered": "filtrate",
        "closed|filtered": "chiuse/filtrate",
        "open|filtered": "aperte/filtrate",
    }.get(state, state)


def _translate_reason(reason: str) -> str:
    return {
        "no-response": "nessuna risposta",
        "conn-refused": "connessione rifiutata",
        "syn-ack": "risposta TCP",
    }.get(reason, reason)


def _summary_for_open_ports(open_count: int, scanned_ports: int) -> str:
    if open_count == 0:
        return f"Nessuna porta aperta è stata trovata tra le {scanned_ports} più comuni."
    if open_count == 1:
        return (
            "È stata trovata 1 porta raggiungibile dall'esterno. "
            "Questo indica che almeno un servizio risulta visibile da Internet."
        )
    return (
        f"Sono state trovate {open_count} porte raggiungibili dall'esterno. "
        "Questo indica che almeno alcuni servizi risultano visibili da Internet."
    )
