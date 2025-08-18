from collections.abc import Sequence
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession

from .entity import EventEntity, ProgramOverviewEntity

if TYPE_CHECKING:
    from .repository import EventRepository

class EventService:
    def __init__(self, repository: "EventRepository"):
        self.repository = repository

    async def list_events(self) -> Sequence[EventEntity]:
        """
        Asynchronously retrieves a sequence of active Event objects from the repository.

        Returns:
            Sequence[Event]: A sequence containing all active events.
        """
        async with self.repository.ensure_session() as session:
            return [EventEntity(
                id_event=event.id_event,
                name=event.name,
                description=event.description,
                start_date=event.start_date,
                end_date=event.end_date,
                status=str(event.status.value),
                created_by=event.created_by,
                created_at=event.created_at,
                updated_by=event.updated_by,
                updated_at=event.updated_at
            ) for event in await self.repository.list_active_events(session=session)]


    async def overview(self, event_id: UUID, *, session: AsyncSession | None = None) -> list[ProgramOverviewEntity]:
        async with self.repository.ensure_session(session) as session:
            result = []
            for row in await self.repository.overview(event_id, session=session):
                result.append(ProgramOverviewEntity(
                    id_program_item=row.id_program_item,
                    name=row.name,
                    type=row.type,
                    attendee_limit=row.attendee_limit,
                    attendee_limit_buffer=row.attendee_limit_buffer,
                    note=row.note,
                    status=row.status,
                    required_time=row.required_time,
                    before_time_buffer=row.before_time_buffer,
                    after_time_buffer=row.after_time_buffer,
                    start_time=row.start_time,
                    end_time=row.end_time,
                    attendee_count=row.attendee_count
                ))
            return result
