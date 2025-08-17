from collections.abc import Sequence
from typing import TYPE_CHECKING

from .entity import EventEntity

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
