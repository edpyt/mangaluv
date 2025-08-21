"""Healthcheck route."""

from dataclasses import dataclass

from fastapi import APIRouter

router = APIRouter()


@dataclass(frozen=True)
class ServiceHealth:
    """Service healthcheck response."""

    status: int
    msg: str


@dataclass(frozen=True)
class ServicesHealthCheckResponse:
    """Services healthcheck response."""

    auth: ServiceHealth
    manga: ServiceHealth


@router.get("/healthcheck", response_model=ServicesHealthCheckResponse)
def healthcheck() -> dict[str, dict[str, int | str]]:
    """Return current server status."""
    return {
        "auth": {"status": 200, "msg": "TODO"},
        "manga": {"status": 200, "msg": "TODO"},
    }
