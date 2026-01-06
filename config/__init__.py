"""Application configuration."""

from .settings import (
    APP_VERSION,
    APP_TITLE,
    APP_ICON,
    CACHE_TTL_PRICES,
    CACHE_TTL_MAPPING,
    CACHE_TTL_CHAINS,
    DEFAULT_CONFIG,
    URL_PARAMS,
    API_USER_AGENT,
    API_POLL_INTERVAL,
)

__all__ = [
    'APP_VERSION',
    'APP_TITLE',
    'APP_ICON',
    'CACHE_TTL_PRICES',
    'CACHE_TTL_MAPPING',
    'CACHE_TTL_CHAINS',
    'DEFAULT_CONFIG',
    'URL_PARAMS',
    'API_USER_AGENT',
    'API_POLL_INTERVAL',
]
