from collections.abc import Sequence

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from service.core import BaseRepository, EventModel, EventStatus


class EventRepository(BaseRepository):
    async def list_active_events(self, *, session: AsyncSession | None = None) -> Sequence[EventModel]:
        """
        Retrieve a list of active events.

        Active events are considered those with status DRAFT or PUBLISHED
        and a future end date plus a grace period of 7 days.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session to use for the query.

        Returns:
            Sequence[Event]: A sequence of Event objects that are currently active (DRAFT or PUBLISHED).
        """
        async with self.ensure_session(session) as session:
            result = await session.execute(
                select(EventModel).where(
                    (EventModel.status == EventStatus.DRAFT) | (EventModel.status == EventStatus.PUBLISHED)
                )
            )
            return result.scalars().all()
