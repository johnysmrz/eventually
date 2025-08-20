from collections.abc import Sequence
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession

from service.core import LocationModel

from .entity import CreateLocationEntity, EventEntity, LocationEntity, ProgramOverviewEntity

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
        """
        Retrieve an overview of program items for a given event.

        Args:
            event_id (UUID): The unique identifier of the event.
            session (AsyncSession, optional): An optional SQLAlchemy asynchronous session. If not provided, a new session will be created.

        Returns:
            list[ProgramOverviewEntity]: A list of program overview entities containing details about each program item associated with the event.

        Raises:
            Any exceptions raised by the repository or database layer.
        """
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


    async def list_locations(self, event_id: UUID, *, session: AsyncSession | None = None) -> list[LocationEntity]:
        """
        Asynchronously retrieves a list of locations associated with a given event.

        Args:
            event_id (UUID): The unique identifier of the event for which locations are to be listed.
            session (AsyncSession, optional): An optional SQLAlchemy asynchronous session. If not provided, a new session will be created.

        Returns:
            list[LocationEntity]: A list of LocationEntity objects representing the locations linked to the specified event.
        """
        async with self.repository.ensure_session(session) as session:
            result = []
            for row in await self.repository.get_locations(event_id, session=session):
                result.append(LocationEntity(
                    id_event=row.id_event,
                    name=row.name,
                    lat=row.lat,
                    lon=row.lon
                ))
            return result


    async def create_location(self, event_id: UUID, new_location: CreateLocationEntity, *, session: AsyncSession | None = None):
        """
        Asynchronously creates a new location associated with a given event.

        Args:
            event_id (UUID): The unique identifier of the event to which the location will be linked.
            new_location (CreateLocationEntity): An entity containing the details of the new location (name, latitude, longitude).
            session (AsyncSession, optional): An optional SQLAlchemy asynchronous session. If not provided, a new session will be created.

        Returns:
            None
        Raises:
            Any exceptions raised by the repository layer during creation or session management.
        """
        async with self.repository.ensure_session(session) as session:
            new_location_model = LocationModel(
                id_event=event_id,
                name=new_location.name,
                lat=new_location.lat,
                lon=new_location.lon
            )
            await self.repository.create(new_location_model, session=session)
