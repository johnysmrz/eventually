import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from opentelemetry import metrics, trace
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel

logger = logging.getLogger("rzbportal.repository")
tracer = trace.get_tracer("rzbportal.repository.tracer")
meter = metrics.get_meter("rzbportal.repository.meter")


class BaseRepository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        """
        Initializes the repository with a sessionmaker.

        Args:
            sessionmaker (async_sessionmaker[AsyncSession]): The sessionmaker to be used for creating database sessions.
        """
        self._sessionmaker = sessionmaker

    @asynccontextmanager
    async def ensure_session(self, session: AsyncSession | None = None) -> AsyncGenerator[AsyncSession, Any]:
        """
        Ensures that an asynchronous session is available for database operations.

        If a session is provided, it yields the provided session. Otherwise, it creates a new session
        using the sessionmaker, begins a transaction, and yields the new session. The session is committed
        if no exceptions occur, otherwise it is rolled back.

        Args:
            session (AsyncSession | None): An optional existing session to use.

        Yields:
            AsyncGenerator[AsyncSession, Any]: An asynchronous generator yielding the session.

        Raises:
            Exception: If an error occurs during the session, it is rolled back and the exception is raised.

        Example:
        async def example_usage(repo: BaseRepository):
            async with repo.ensure_session() as session:
                # Perform database operations using the session
                result = await session.execute("SELECT 1")
                print(result.scalar())
        """
        if session is not None:
            yield session
        else:
            async with self._sessionmaker(expire_on_commit=True) as session, session.begin():
                with tracer.start_as_current_span("database_session"):
                    try:
                        yield session
                        if session.in_transaction():
                            logger.debug("Transaction already commited")
                            await session.commit()
                    except Exception:
                        await session.rollback()
                        raise

    async def create(self, model: SQLModel, session: AsyncSession | None = None):
        """
        Asynchronously adds a new model instance to the database session.

        Args:
            model (SQLModel): The model instance to be added to the session.
            session (AsyncSession | None, optional): An existing asynchronous database session. 
                If None, a new session is created and managed internally.
        """
        async with self.ensure_session(session) as session:
            session.add(model)
            return model
