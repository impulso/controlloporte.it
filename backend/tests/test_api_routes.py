"""Tests for API routes"""
from litestar.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST

from app.schemas.api import NATScanNotShownSchema, NATScanWorkerResponseSchema

from .conftest import HEADER_REAL_IP, INVALID_HOST, VALID_DOMAIN


def test_route_health_check(client):
    """Test health check route returns status 200 and 'true' response text."""
    response = client.get("/healthz")
    assert response.status_code == HTTP_200_OK
    assert response.text == "true"


def test_my_ip_endpoint(client, mocker):
    """Test my_ip endpoint returns correct requester IP."""
    mock_get_requester = mocker.patch(
        "app.routes.v2.get_requester", return_value=HEADER_REAL_IP
    )
    response = client.get("/api/me")
    assert response.status_code == HTTP_200_OK
    assert response.text == HEADER_REAL_IP
    mock_get_requester.assert_called_once()


def test_get_port_check_endpoint_with_hostname(client, mocker):
    """Test port check endpoint with hostname returns expected status."""
    mock_get_requester = mocker.patch(
        "app.routes.v2.get_requester", return_value=HEADER_REAL_IP
    )
    mock_query_address = mocker.patch(
        "app.routes.v2.query_address",
        return_value=[{"port": 443, "status": True, "latency_ms": 23}],
    )
    response = client.get(f"/api/{VALID_DOMAIN}/443")

    assert response.status_code == HTTP_200_OK
    assert response.text == "True"
    mock_get_requester.assert_not_called()
    mock_query_address.assert_called_once_with("example.com", [443])


def test_get_port_check_endpoint_with_me(client, mocker):
    """Test port check endpoint with 'me' parameter uses get_requester."""
    mock_get_requester = mocker.patch(
        "app.routes.v2.get_requester", return_value=HEADER_REAL_IP
    )
    mock_query_address = mocker.patch(
        "app.routes.v2.query_address",
        return_value=[{"port": 443, "status": True, "latency_ms": 23}],
    )

    # Send the request with the 'me' parameter to trigger get_requester
    response = client.get("/api/me/443")

    # Assertions to ensure function calls and response correctness
    assert response.status_code == HTTP_200_OK
    assert response.text == "True"
    mock_get_requester.assert_called_once()  # Confirm get_requester was called once
    mock_query_address.assert_called_once_with(HEADER_REAL_IP, [443])


def test_get_port_check_json_endpoint_with_hostname(client, mocker):
    """Test JSON port check endpoint with hostname returns structured response."""
    mock_get_requester = mocker.patch(
        "app.routes.v2.get_requester", return_value=HEADER_REAL_IP
    )
    mock_query_address = mocker.patch(
        "app.routes.v2.query_address",
        return_value=[{"port": 443, "status": True, "latency_ms": 23}],
    )

    response = client.get(f"/api/check/{VALID_DOMAIN}/443")

    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "error": False,
        "msg": None,
        "host": "example.com",
        "check": [{"port": 443, "status": True, "latency_ms": 23}],
    }
    mock_get_requester.assert_not_called()
    mock_query_address.assert_called_once_with("example.com", [443])


def test_get_port_check_json_endpoint_with_me(client, mocker):
    """Test JSON port check endpoint with 'me' parameter uses get_requester."""
    mock_get_requester = mocker.patch(
        "app.routes.v2.get_requester", return_value=HEADER_REAL_IP
    )
    mock_query_address = mocker.patch(
        "app.routes.v2.query_address",
        return_value=[{"port": 443, "status": True, "latency_ms": 23}],
    )

    response = client.get("/api/check/me/443")

    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "error": False,
        "msg": None,
        "host": HEADER_REAL_IP,
        "check": [{"port": 443, "status": True, "latency_ms": 23}],
    }
    mock_get_requester.assert_called_once()
    mock_query_address.assert_called_once_with(HEADER_REAL_IP, [443])


def test_query_post_endpoint_v1(client, mocker):
    """Test v1 query endpoint with valid data returns correct status."""
    mock_query_address = mocker.patch(
        "app.routes.v2.query_address",
        return_value=[
            {"port": 80, "status": True, "latency_ms": 12},
            {"port": 443, "status": False, "latency_ms": None},
        ],
    )

    request_data = {"host": VALID_DOMAIN, "ports": [80, 443]}
    response = client.post("/api/v1/query", json=request_data)
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "error": False,
        "msg": None,
        "host": "example.com",
        "check": [
            {"port": 80, "status": True, "latency_ms": 12},
            {"port": 443, "status": False, "latency_ms": None},
        ],
    }
    mock_query_address.assert_called_once_with(VALID_DOMAIN, [80, 443])


def test_query_post_endpoint_invalid_port_v1(client):
    """Test v1 query endpoint raises error with invalid port number."""
    request_data = {"host": VALID_DOMAIN, "ports": [80, 70000]}  # Invalid port range

    path = "/api/v1/query"
    response = client.post(path, json=request_data)
    assert response.status_code == HTTP_400_BAD_REQUEST
    ret = response.json()
    assert ret["detail"] == f"errore di validazione: richiesta non valida per POST {path}"
    assert ret["error"] is True
    assert ret["extra"][0]["message"] == "La porta deve essere un numero da 1 a 65535"


def test_query_post_endpoint_invalid_hostname_v1(client, mocker):
    """Test v1 query endpoint raises error with invalid hostname."""
    mocker.patch(
        "socket.gethostbyname",
        side_effect=OSError("Hostname does not appear to resolve"),
    )
    request_data = {"host": INVALID_HOST, "ports": [80]}  # Invalid host
    path = "/api/v1/query"
    response = client.post(path, json=request_data)
    assert response.status_code == HTTP_400_BAD_REQUEST
    ret = response.json()
    assert ret["detail"] == f"errore di validazione: richiesta non valida per POST {path}"
    assert ret["error"] is True
    assert ret["extra"][0]["key"] == "host"
    assert ret["extra"][0]["message"] == "Il nome host inserito non risulta raggiungibile"


def test_query_post_endpoint_v2(client, mocker):
    """Test v2 query endpoint with valid data returns correct status."""
    mock_query_address = mocker.patch(
        "app.routes.v2.query_address",
        return_value=[
            {"port": 80, "status": True, "latency_ms": 12},
            {"port": 443, "status": False, "latency_ms": None},
        ],
    )

    request_data = {"host": VALID_DOMAIN, "ports": [80, 443]}
    response = client.post("/api/query", json=request_data)
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "error": False,
        "msg": None,
        "host": "example.com",
        "check": [
            {"port": 80, "status": True, "latency_ms": 12},
            {"port": 443, "status": False, "latency_ms": None},
        ],
    }
    mock_query_address.assert_called_once_with(VALID_DOMAIN, [80, 443])


def test_query_post_endpoint_v2_with_me(client, mocker):
    """Test v2 query endpoint with 'me' host uses requester IP."""
    mock_get_requester = mocker.patch(
        "app.routes.v2.get_requester", return_value=HEADER_REAL_IP
    )
    mock_query_address = mocker.patch(
        "app.routes.v2.query_address",
        return_value=[{"port": 443, "status": True, "latency_ms": 23}],
    )

    request_data = {"host": "me", "ports": [443]}
    response = client.post("/api/query", json=request_data)

    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "error": False,
        "msg": None,
        "host": HEADER_REAL_IP,
        "check": [{"port": 443, "status": True, "latency_ms": 23}],
    }
    mock_get_requester.assert_called_once()
    mock_query_address.assert_called_once_with(HEADER_REAL_IP, [443])


def test_controllo_ddns_endpoint_matching_ip(client, mocker):
    """Test DDNS endpoint compares the requester IP with hostname resolution."""
    mock_get_requester = mocker.patch(
        "app.routes.v2.get_requester", return_value=HEADER_REAL_IP
    )
    mock_check_ddns = mocker.patch(
        "app.routes.v2.check_ddns",
        return_value={
            "host": "home.example.com",
            "requester_ip": HEADER_REAL_IP,
            "resolved_ip": HEADER_REAL_IP,
            "match": True,
        },
    )

    response = client.post("/api/controlloDDNS", json={"host": "home.example.com"})

    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "error": False,
        "msg": None,
        "host": "home.example.com",
        "requester_ip": HEADER_REAL_IP,
        "resolved_ip": HEADER_REAL_IP,
        "match": True,
    }
    mock_get_requester.assert_called_once()
    mock_check_ddns.assert_called_once_with("home.example.com", HEADER_REAL_IP)


def test_controllo_ddns_endpoint_missing_requester_ip(client, mocker):
    """Test DDNS endpoint returns JSON validation error when requester IP is missing."""
    mocker.patch(
        "app.routes.v2.get_requester",
        side_effect=ValueError("Impossibile rilevare l'indirizzo IP del richiedente"),
    )

    response = client.post("/api/controlloDDNS", json={"host": "home.example.com"})

    assert response.status_code == HTTP_400_BAD_REQUEST
    ret = response.json()
    assert ret["detail"] == (
        "errore di validazione: richiesta non valida per POST /api/controlloDDNS"
    )
    assert ret["error"] is True
    assert ret["extra"][0]["key"] == "requester_ip"
    assert (
        ret["extra"][0]["message"]
        == "Impossibile rilevare l'indirizzo IP del richiedente"
    )


def test_quick_nat_scan_endpoint_success(client, mocker):
    """Test quick NAT scan uses requester IP and returns the formatted report."""
    mock_get_requester = mocker.patch(
        "app.routes.v2.get_requester", return_value=HEADER_REAL_IP
    )
    mock_run_scan = mocker.patch(
        "app.routes.v2.run_quick_nat_scan",
        return_value=NATScanWorkerResponseSchema(
            ip=HEADER_REAL_IP,
            scan_type="top_ports",
            num_ports=50,
            scanned_ports=50,
            open_ports=[],
            not_shown=NATScanNotShownSchema(
                count=50,
                state="filtered",
                reason="no-response",
            ),
            duration_ms=1234,
        ),
    )

    response = client.post("/api/nat/quick-scan", json={"consent": True})

    assert response.status_code == HTTP_200_OK
    ret = response.json()
    assert ret["error"] is False
    assert ret["ip"] == HEADER_REAL_IP
    assert ret["scan_type"] == "top_ports"
    assert ret["num_ports"] == 50
    assert ret["summary"] == "Nessuna porta aperta è stata trovata tra le 50 più comuni."
    assert "Report scansione NAT veloce" in ret["report"]
    mock_get_requester.assert_called_once()
    mock_run_scan.assert_called_once_with(HEADER_REAL_IP)


def test_quick_nat_scan_endpoint_requires_consent(client):
    """Test quick NAT scan requires explicit user consent."""
    response = client.post("/api/nat/quick-scan", json={"consent": False})

    assert response.status_code == HTTP_400_BAD_REQUEST
    ret = response.json()
    assert ret["error"] is True
    assert ret["extra"][0]["key"] == "consent"
    assert (
        ret["extra"][0]["message"]
        == "Devi autorizzare la scansione rapida del tuo IP pubblico."
    )


def test_query_post_endpoint_invalid_port_v2(client):
    """Test v2 query endpoint raises error with invalid port number."""
    request_data = {"host": VALID_DOMAIN, "ports": [80, 70000]}  # Invalid port range

    path = "/api/query"
    response = client.post(path, json=request_data)
    assert response.status_code == HTTP_400_BAD_REQUEST
    ret = response.json()
    assert ret["detail"] == f"errore di validazione: richiesta non valida per POST {path}"
    assert ret["error"] is True
    assert ret["extra"][0]["message"] == "La porta deve essere un numero da 1 a 65535"


def test_query_post_endpoint_invalid_hostname_v2(client, mocker):
    """Test v2 query endpoint raises error with invalid hostname."""
    mocker.patch(
        "socket.gethostbyname",
        side_effect=OSError("Hostname does not appear to resolve"),
    )
    request_data = {"host": INVALID_HOST, "ports": [80]}  # Invalid host
    path = "/api/query"
    response = client.post(path, json=request_data)
    assert response.status_code == HTTP_400_BAD_REQUEST
    ret = response.json()
    assert ret["detail"] == f"errore di validazione: richiesta non valida per POST {path}"
    assert ret["error"] is True
    assert ret["extra"][0]["key"] == "host"
    assert ret["extra"][0]["message"] == "Il nome host inserito non risulta raggiungibile"
