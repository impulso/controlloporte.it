"""Tests for query_address"""

import pytest

from api.app.helpers.query import (
    JsonAPIException,
    _check_port_status,
    check_ddns,
    check_ports,
    query_address,
    resolve_hostname,
)

from .conftest import (
    CLOSED_PORTS,
    INVALID_HOST,
    OPEN_PORTS,
    PORTS,
    SOCKET_OPEN,
    VALID_PUBLIC_IPV4,
    mock_connect,
)


@pytest.mark.parametrize(
    "host,ports,expected",
    [
        (
            VALID_PUBLIC_IPV4,
            [CLOSED_PORTS[0]],
            [{"port": CLOSED_PORTS[0], "status": False}],
        ),
        (
            VALID_PUBLIC_IPV4,
            OPEN_PORTS,
            [{"port": port, "status": True} for port in OPEN_PORTS],
        ),
        (
            VALID_PUBLIC_IPV4,
            CLOSED_PORTS,
            [{"port": port, "status": False} for port in CLOSED_PORTS],
        ),
        (VALID_PUBLIC_IPV4, [], []),
    ],
)
def test_query_address_various(host, ports, expected):
    """Test query_address for various valid scenarios."""
    result = query_address(host, ports)
    assert result == [
        {
            **item,
            "latency_ms": result[index]["latency_ms"] if item["status"] else None,
        }
        for index, item in enumerate(expected)
    ]
    for item in result:
        if item["status"]:
            assert item["latency_ms"] is not None
        else:
            assert item["latency_ms"] is None


def test_query_address_multiple_ports_mixed_status():
    """Test when some ports are open and some are closed."""
    result = query_address(VALID_PUBLIC_IPV4, PORTS)
    expected = [
        {
            "port": port,
            "status": mock_connect((VALID_PUBLIC_IPV4, port)) == SOCKET_OPEN,
            "latency_ms": result[index]["latency_ms"]
            if mock_connect((VALID_PUBLIC_IPV4, port)) == SOCKET_OPEN
            else None,
        }
        for index, port in enumerate(PORTS)
    ]
    assert result == expected
    for item in result:
        if item["status"]:
            assert item["latency_ms"] is not None
        else:
            assert item["latency_ms"] is None


def test_query_address_resolves_hostname_before_port_checks(mocker):
    """Test hostname DNS resolution happens before TCP latency measurements."""
    mock_gethostbyname = mocker.patch(
        "socket.gethostbyname", return_value=VALID_PUBLIC_IPV4
    )
    result = query_address("example.com", OPEN_PORTS)

    mock_gethostbyname.assert_called_once_with("example.com")
    assert result == [
        {"port": port, "status": True, "latency_ms": result[index]["latency_ms"]}
        for index, port in enumerate(OPEN_PORTS)
    ]


def test_check_ddns_matching_requester_ip(mocker):
    """Test DDNS check returns a match when hostname resolves to requester IP."""
    mocker.patch("socket.gethostbyname", return_value=VALID_PUBLIC_IPV4)

    result = check_ddns("home.example.com", VALID_PUBLIC_IPV4)

    assert result == {
        "host": "home.example.com",
        "requester_ip": VALID_PUBLIC_IPV4,
        "resolved_ip": VALID_PUBLIC_IPV4,
        "match": True,
    }


def test_check_ddns_different_requester_ip(mocker):
    """Test DDNS check returns no match when hostname resolves elsewhere."""
    mocker.patch("socket.gethostbyname", return_value=VALID_PUBLIC_IPV4)

    result = check_ddns("home.example.com", "1.2.3.4")

    assert result == {
        "host": "home.example.com",
        "requester_ip": "1.2.3.4",
        "resolved_ip": VALID_PUBLIC_IPV4,
        "match": False,
    }


def test_check_ddns_rejects_plain_ip_hostname():
    """Test DDNS check requires a hostname instead of a direct IP address."""
    with pytest.raises(JsonAPIException, match="Inserisci un nome host DNS dinamico"):
        check_ddns(VALID_PUBLIC_IPV4, VALID_PUBLIC_IPV4)


def test_resolve_hostname_rejects_private_resolved_ip(mocker):
    """Test hostnames resolving to private IPs are rejected."""
    mocker.patch("socket.gethostbyname", return_value="192.168.1.10")
    with pytest.raises(ValueError, match="L'indirizzo IP inserito non è Pubblico"):
        resolve_hostname("internal.example.com")


def test_query_address_invalid_hostname(mocker):
    """Test query_address raises JsonAPIException for an invalid hostname (mocked DNS failure)."""
    mocker.patch(
        "socket.gethostbyname",
        side_effect=OSError("Hostname does not appear to resolve"),
    )
    with pytest.raises(JsonAPIException, match=".*Il nome host inserito non risulta raggiungibile"):
        query_address(INVALID_HOST, [OPEN_PORTS[0]])


def test_query_address_empty_host():
    """Test query_address raises JsonAPIException for empty host."""
    with pytest.raises(JsonAPIException, match="Inserisci un nome host"):
        query_address("", [80])


def test_query_address_none_host():
    """Test query_address raises JsonAPIException for None as host."""
    with pytest.raises(JsonAPIException):
        query_address(None, [80])


def test_query_address_invalid_port_type():
    """Test query_address raises TypeError for non-integer port."""
    with pytest.raises(Exception):
        query_address(VALID_PUBLIC_IPV4, ["notaport"])


def test_query_address_ipv6():
    """Test query_address raises JsonAPIException for IPv6 address."""
    with pytest.raises(JsonAPIException, match="IPv6 non è attualmente supportato"):
        query_address("2001:4860:4860::8888", [80])


def test_query_address_duplicate_ports():
    """Test query_address handles duplicate ports gracefully."""
    ports = [80, 80, 443]
    result = query_address(VALID_PUBLIC_IPV4, ports)
    assert len([item for item in result if item["port"] == 80 and item["status"]]) == 2
    assert any(item["port"] == 443 and item["status"] for item in result)
    assert all(item["latency_ms"] is not None for item in result)


def test_check_ports_all_open():
    """Test when all ports are open."""
    result = check_ports(VALID_PUBLIC_IPV4, OPEN_PORTS)
    expected = [
        {"port": port, "status": True, "latency_ms": result[index]["latency_ms"]}
        for index, port in enumerate(OPEN_PORTS)
    ]
    assert result == expected


def test_check_ports_all_closed():
    """Test when all ports are closed."""
    result = check_ports(VALID_PUBLIC_IPV4, CLOSED_PORTS)
    expected = [
        {"port": port, "status": False, "latency_ms": None} for port in CLOSED_PORTS
    ]
    assert result == expected


def test_check_ports_mixed():
    """Test when some ports are open and some are closed."""
    result = check_ports(VALID_PUBLIC_IPV4, PORTS)
    expected = [
        {
            "port": port,
            "status": mock_connect((VALID_PUBLIC_IPV4, port)) == SOCKET_OPEN,
            "latency_ms": result[index]["latency_ms"]
            if mock_connect((VALID_PUBLIC_IPV4, port)) == SOCKET_OPEN
            else None,
        }
        for index, port in enumerate(PORTS)
    ]
    assert result == expected


def test_check_port_status_open():
    """Test _check_port_status with an open port."""
    result = _check_port_status(VALID_PUBLIC_IPV4, OPEN_PORTS[0])
    expected = {
        "port": OPEN_PORTS[0],
        "status": True,
        "latency_ms": result["latency_ms"],
    }
    assert result == expected
    assert result["latency_ms"] is not None


def test_check_port_status_closed():
    """Test _check_port_status with a closed port."""
    result = _check_port_status(VALID_PUBLIC_IPV4, CLOSED_PORTS[0])
    expected = {"port": CLOSED_PORTS[0], "status": False, "latency_ms": None}
    assert result == expected
