from collections.abc import Sequence
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

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
                    id_location=row.id_location,
                    id_event=row.id_event,
                    name=row.name,
                    lat=row.lat,
                    lon=row.lon,
                    color=row.color,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                    created_by=row.created_by,
                    updated_by=row.updated_by
                ))
            return result


    async def create_location(self, event_id: UUID, new_location: CreateLocationEntity, *, session: AsyncSession | None = None) -> UUID:
        """
        Asynchronously creates a new location for a given event.

        Args:
            event_id (UUID): The unique identifier of the event to which the location will be added.
            new_location (CreateLocationEntity): The data required to create the new location.
            session (AsyncSession, optional): An optional SQLAlchemy asynchronous session. If not provided, a new session will be created.

        Returns:
            UUID: The unique identifier of the newly created location.
        """
        new_location_id = uuid4()
        async with self.repository.ensure_session(session) as session:
            new_location_model = LocationModel(
                id_event=event_id,
                id_location=new_location_id,
                name=new_location.name,
                lat=new_location.lat,
                lon=new_location.lon,
                color=new_location.color
            )
            await self.repository.create(new_location_model, session=session)
        return new_location_id

    async def get_location_by_id(self, location_id: UUID, *, session: AsyncSession | None = None) -> LocationEntity | None:
        """
        Asynchronously retrieves a location by its unique identifier.

        Args:
            location_id (UUID): The unique identifier of the location to retrieve.
            session (AsyncSession, optional): An optional SQLAlchemy asynchronous session. If not provided, a new session will be created.

        Returns:
            LocationEntity | None: The location entity if found, or None if not found.
        """
        async with self.repository.ensure_session(session) as session:
            row = await self.repository.get_location_by_id(location_id, session=session)
            if row:
                return LocationEntity(
                    id_event=row.id_event,
                    id_location=row.id_location,
                    name=row.name,
                    lat=row.lat,
                    lon=row.lon,
                    color=row.color,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                    created_by=row.created_by,
                    updated_by=row.updated_by
                )
            return None

    async def delete_location(self, location_id: UUID, *, session: AsyncSession | None = None) -> None:
        """
        Asynchronously deletes a location identified by the given UUID.

        Args:
            location_id (UUID): The unique identifier of the location to delete.
            session (AsyncSession, optional): An optional SQLAlchemy asynchronous session. If not provided, a new session will be created.

        Returns:
            None
        Raises:
            Any exceptions raised by the repository's delete_location method.
        """
        async with self.repository.ensure_session(session) as session:
            await self.repository.delete_location(location_id, session=session)
