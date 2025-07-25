"""Database connection logic."""

import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

logger = logging.getLogger(__name__)


async def check_db_health(db: AsyncSession) -> bool:
    """Return is db available."""
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.exception(e)
        return False
