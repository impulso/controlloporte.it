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
