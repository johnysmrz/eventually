from collections.abc import Sequence
from datetime import datetime, timedelta
from typing import NamedTuple
from uuid import UUID

from rich.console import Console
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select, text

from service.core import BaseRepository, EventModel, EventStatus

c = Console()

class OverviewResult(NamedTuple):
    id_program_item: UUID
    name: str
    type: str
    attendee_limit: int | None
    attendee_limit_buffer: int | None
    note: str | None
    status: str
    required_time: timedelta | None
    before_time_buffer: timedelta | None
    after_time_buffer: timedelta | None
    start_time: datetime | None
    end_time: datetime | None
    attendee_count: int

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

    async def overview(self, event_id: UUID, *, session: AsyncSession | None = None) -> Sequence[OverviewResult]:
        """
        Retrieves an overview of program sessions for a given event.

        Args:
            event_id (UUID): The unique identifier of the event.
            session (AsyncSession, optional): An optional SQLAlchemy asynchronous session. If not provided, a new session is created.

        Returns:
            Sequence[tuple]: A sequence of tuples, each containing the following fields for each program session:
                - id_program_item: The unique identifier of the program item.
                - name: The name of the program item.
                - type: The type of the program item.
                - attendee_limit: The attendee limit for the session (overridden if specified).
                - attendee_limit_buffer: The buffer for attendee limit.
                - note: Any note associated with the session.
                - status: The status of the session.
                - required_time: The required time for the session.
                - before_time_buffer: Buffer time before the session.
                - after_time_buffer: Buffer time after the session.
                - start_time: The start time of the session.
                - end_time: The end time of the session.
                - attendee_count: The number of attendees registered for the session.
        """
        async with self.ensure_session(session) as session:
            result = await session.execute(text(
                """
                    SELECT
                        pi.id_program_item,
                        pi.name,
                        pi.type,
                        COALESCE(ps.attendee_limit_override, pi.attendee_limit) AS attendee_limit,
                        pi.attendee_limit_buffer,
                        ps.note,
                        ps.status,
                        pi.required_time,
                        pi.before_time_buffer,
                        pi.after_time_buffer,
                        ps.start_time,
                        ps.end_time,
                        (SELECT COUNT(*) FROM t_attendee_program_session aps WHERE aps.id_program_session = ps.id_program_session) AS attendee_count
                    FROM
                        t_program_session ps
                    LEFT JOIN
                        t_program_item pi USING (id_program_item)
                    WHERE
                        pi.id_event = :event_id
                    ORDER BY ps.start_time ASC
                """
            ), {"event_id": event_id})
            return [OverviewResult(*row) for row in result.fetchall()]
