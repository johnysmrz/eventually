from functools import lru_cache
from typing import Callable

import psycopg2
import pytest
import redis as rds

from settings import Settings, get_settings


@lru_cache
def postgresql() -> Callable:
    settings: Settings = get_settings()
    try:
        c = psycopg2.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
        )
        c.close()
    except psycopg2.OperationalError as e:
        return pytest.mark.skipif(True, reason=f"No postgresql: {e}")
    return pytest.mark.skipif(False, reason="")


@lru_cache
def redis() -> Callable:
    try:
        c = rds.Redis(host='localhost')
        c.get('ping')
    except Exception as e:
        return pytest.mark.skipif(True, reason=f"No redis: {e}")
    return pytest.mark.skipif(False, reason="")