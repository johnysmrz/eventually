import uuid
from collections.abc import AsyncGenerator
from typing import Any
import asyncio

import asyncpg
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

# from app import app
from settings import Settings

connection_semaphore = asyncio.Semaphore(1)


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()  # type: ignore


@pytest.fixture(autouse=True)
async def engine(settings: Settings) -> AsyncGenerator[AsyncEngine, Any]:
    """
    Creates and manages a database engine for testing purposes.

    This function creates a temporary test database, initializes an engine
    using the database URL, and yields the engine for use in test cases.
    After the test cases are executed, the function cleans up by dropping
    the test database and closing the connection.

    Returns:
        AsyncGenerator[Any, Any]: An asynchronous generator that yields the
        database engine.

    Raises:
        Any: Any exceptions that occur during the creation or disposal of
        the database engine.

    Example:
        async def test_my_function(engine):
            # Use the engine to perform database operations
            async with engine.connect() as conn:
                # Perform database operations

        async with engine() as engine:
            await test_my_function(engine)
    """
    # Generate a unique test database name
    TEST_DB_NAME = f"{settings.POSTGRES_DB}_test_{uuid.uuid4()}"

    async with connection_semaphore:
        pool = await asyncpg.create_pool(user=settings.POSTGRES_USER, password=settings.POSTGRES_PASSWORD, host=settings.POSTGRES_HOST, command_timeout=10)
        conn = await pool.acquire()
        await conn.execute(f'CREATE DATABASE "{TEST_DB_NAME}" OWNER "{settings.POSTGRES_USER}"')

        DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{TEST_DB_NAME}"

        # NullPool is used to avoid connection pooling so that the database can be dropped after the tests
        engine = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)
        async with engine.begin() as c:
            await c.run_sync(SQLModel.metadata.create_all)

        yield engine

        await engine.dispose()

        await conn.execute(f'DROP DATABASE "{TEST_DB_NAME}"')
        await conn.close()
        await pool.close()
