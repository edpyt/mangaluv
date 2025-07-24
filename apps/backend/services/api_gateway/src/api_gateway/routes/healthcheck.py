"""Healthcheck route."""

from dataclasses import dataclass

from fastapi import APIRouter

router = APIRouter()


@dataclass(frozen=True)
class HealthCheckResponse:
    """Response schema for healthcheck route."""

    message: str


@router.get("/healthcheck")
def healthcheck() -> HealthCheckResponse:
    """Return current server status."""
    return HealthCheckResponse(message="OK")
