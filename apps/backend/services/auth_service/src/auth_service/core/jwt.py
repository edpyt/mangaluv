"""JWT logic."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import TypedDict
from uuid import UUID, uuid4

from jose import jwt


@dataclass(frozen=True)
class TokenPair:
    """JWT token pair."""

    access: "JwtToken"
    refresh: "JwtToken"


@dataclass(frozen=True, kw_only=True)
class JwtToken:
    """Main jwt token class."""

    token: str
    payload: "_JwtPayload"
    expire: datetime


class _JwtPayload(TypedDict):
    sub: str
    jti: str
    iat: datetime
    exp: str | None


def create_token_pair(
    user_id: UUID,
    *,
    access_expire_minutes: int,
    refresh_expire_minutes: int,
    secret_key: str,
    algorithm: str,
) -> TokenPair:
    """Return token pair from provided user data."""
    payload: _JwtPayload = {
        "sub": str(user_id),
        "jti": str(uuid4()),
        "iat": datetime.now(UTC),
        "exp": None,
    }
    return TokenPair(
        access=_create_access_token(
            payload.copy(),
            access_expire_minutes,
            secret_key,
            algorithm,
        ),
        refresh=_create_refresh_token(
            payload.copy(),
            refresh_expire_minutes,
            secret_key,
            algorithm,
        ),
    )


def _create_access_token(
    payload: _JwtPayload,
    /,
    access_expire_minutes: int,
    secret_key: str,
    algorithm: str,
) -> JwtToken:
    expire = datetime.now(UTC) + timedelta(minutes=access_expire_minutes)
    payload["exp"] = expire
    return JwtToken(
        token=jwt.encode(
            payload,  # pyright: ignore[reportArgumentType]
            secret_key,
            algorithm=algorithm,
        ),
        expire=expire,
        payload=payload,
    )


def _create_refresh_token(
    payload: _JwtPayload,
    /,
    refresh_expire_minutes: int,
    secret_key: str,
    algorithm: str,
) -> JwtToken:
    expire = datetime.now(UTC) + timedelta(minutes=refresh_expire_minutes)
    payload["exp"] = expire
    return JwtToken(
        token=jwt.encode(
            payload,  # pyright: ignore[reportArgumentType]
            secret_key,
            algorithm,
        ),
        expire=expire,
        payload=payload,
    )
