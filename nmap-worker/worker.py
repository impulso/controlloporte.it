"""Small internal HTTP worker for controlled nmap quick scans."""

from __future__ import annotations

import json
import os
import subprocess
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from ipaddress import ip_address
from xml.etree import ElementTree

ALLOWED_SCAN_TYPE = "top_ports"
ALLOWED_NUM_PORTS = 50
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8080"))


class ScanHandler(BaseHTTPRequestHandler):
    """Handle internal scan requests from the API container."""

    server_version = "controlloporte-nmap-worker/1.0"

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            self._send_json(200, {"ok": True})
            return
        self._send_json(404, {"error": True, "message": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/scan":
            self._send_json(404, {"error": True, "message": "Not found"})
            return

        try:
            payload = self._read_json()
            result = run_scan(payload)
        except ValueError as ex:
            self._send_json(400, {"error": True, "message": str(ex)})
            return
        except TimeoutError:
            self._send_json(
                504,
                {
                    "error": True,
                    "message": "La scansione ha superato il tempo massimo.",
                },
            )
            return
        except Exception:
            self._send_json(
                500,
                {
                    "error": True,
                    "message": "La scansione non è riuscita. Riprova tra poco.",
                },
            )
            return

        self._send_json(200, result)

    def log_message(self, fmt: str, *args: object) -> None:
        return

    def _read_json(self) -> dict:
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0 or content_length > 2048:
            raise ValueError("Richiesta non valida")
        try:
            return json.loads(self.rfile.read(content_length).decode("utf-8"))
        except json.JSONDecodeError as ex:
            raise ValueError("JSON non valido") from ex

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_scan(payload: dict) -> dict:
    ip = validate_payload(payload)
    started = time.perf_counter()
    command = [
        "nmap",
        "-Pn",
        "-sT",
        "--top-ports",
        str(ALLOWED_NUM_PORTS),
        "--host-timeout",
        "30s",
        "--max-retries",
        "1",
        "--reason",
        "-oX",
        "-",
        ip,
    ]

    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=40,
        )
    except subprocess.TimeoutExpired as ex:
        raise TimeoutError from ex

    if completed.returncode not in (0, 1):
        raise ValueError("La scansione non è riuscita. Riprova tra poco.")

    duration_ms = round((time.perf_counter() - started) * 1000)
    return parse_nmap_xml(completed.stdout, ip, duration_ms)


def validate_payload(payload: dict) -> str:
    scan_type = payload.get("scan_type")
    num_ports = payload.get("num_ports")
    ip = payload.get("ip")

    if scan_type != ALLOWED_SCAN_TYPE or num_ports != ALLOWED_NUM_PORTS:
        raise ValueError("Profilo di scansione non consentito")
    if not isinstance(ip, str):
        raise ValueError("IP non valido")

    try:
        parsed_ip = ip_address(ip)
    except ValueError as ex:
        raise ValueError("IP non valido") from ex

    if parsed_ip.version != 4:
        raise ValueError("IPv6 non è attualmente supportato")
    if parsed_ip.is_private or parsed_ip.is_loopback or parsed_ip.is_link_local:
        raise ValueError("L'indirizzo IP rilevato non è pubblico")

    return ip


def parse_nmap_xml(xml_output: str, ip: str, duration_ms: int) -> dict:
    try:
        root = ElementTree.fromstring(xml_output)
    except ElementTree.ParseError as ex:
        raise ValueError("Output scansione non valido") from ex

    open_ports = []
    scanned_ports = 0
    not_shown = {"count": ALLOWED_NUM_PORTS, "state": "filtered", "reason": "no-response"}
    ports_node = root.find("./host/ports")

    if ports_node is not None:
        extraports = ports_node.find("extraports")
        if extraports is not None:
            count = int(extraports.attrib.get("count", "0"))
            state = extraports.attrib.get("state", "filtered")
            reason_node = extraports.find("extrareasons")
            reason = "no-response"
            if reason_node is not None:
                reason = reason_node.attrib.get("reason", reason)
            not_shown = {"count": count, "state": state, "reason": reason}

        for port_node in ports_node.findall("port"):
            scanned_ports += 1
            state_node = port_node.find("state")
            state = (
                state_node.attrib.get("state", "unknown")
                if state_node is not None
                else "unknown"
            )
            if state != "open":
                continue

            service_node = port_node.find("service")
            open_ports.append(
                {
                    "port": int(port_node.attrib["portid"]),
                    "protocol": port_node.attrib.get("protocol", "tcp"),
                    "state": state,
                    "service": (
                        service_node.attrib.get("name", "unknown")
                        if service_node is not None
                        else "unknown"
                    ),
                    "reason": (
                        state_node.attrib.get("reason")
                        if state_node is not None
                        else None
                    ),
                }
            )

    scanned_ports = max(ALLOWED_NUM_PORTS, scanned_ports + not_shown["count"])

    return {
        "ip": ip,
        "scan_type": ALLOWED_SCAN_TYPE,
        "num_ports": ALLOWED_NUM_PORTS,
        "scanned_ports": scanned_ports,
        "open_ports": open_ports,
        "not_shown": not_shown,
        "duration_ms": duration_ms,
    }


if __name__ == "__main__":
    ThreadingHTTPServer((HOST, PORT), ScanHandler).serve_forever()
