"""Unified rate limiting for kinemotion backend.

Provides a single rate limiting interface that works in both production
and test environments. Uses slowapi for production and a no-op fallback
for testing or when fastapi-limiter is unavailable.
"""

import os
from typing import Any

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from ..logging_config import get_logger
from .rate_limiter import NoOpLimiter

logger = get_logger(__name__)


# Rate limiter instance - set during initialization
_rate_limiter: Limiter | NoOpLimiter | None = None


def get_rate_limiter() -> Limiter | NoOpLimiter:
    """Get the rate limiter instance.

    Returns:
        Limiter instance for production, NoOpLimiter for testing

    Raises:
        RuntimeError: If rate limiter has not been initialized
    """
    if _rate_limiter is None:
        raise RuntimeError("Rate limiter not initialized. Call setup_rate_limiter() first.")
    return _rate_limiter


def setup_rate_limiter(app: Any) -> Limiter | NoOpLimiter:
    """Set up rate limiting for the FastAPI application.

    Args:
        app: FastAPI application instance

    Returns:
        Configured rate limiter instance (Limiter or NoOpLimiter)
    """
    global _rate_limiter

    # Check if we should use no-op limiter (for testing)
    if os.getenv("TESTING", "").lower() == "true":
        logger.info("using_noop_rate_limiter", reason="testing_mode")
        _rate_limiter = NoOpLimiter()
        return _rate_limiter

    # Use slowapi for production
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200/hour"],
        storage_uri=os.getenv("REDIS_URL", ""),
        storage_options={"connect_timeout": 5},
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    _rate_limiter = limiter
    logger.info("rate_limiter_initialized", type="slowapi")
    return _rate_limiter
