from uuid import UUID

from fastapi import APIRouter, Depends

from container import service
from service.event import CreateLocationEntity, EventService, LocationEntity

location_router = APIRouter()

event_service_dependency = Depends(service(EventService))


@location_router.get("")
async def get_event_locations(
    event_id: UUID,
    event_service: EventService = event_service_dependency,
) -> list[LocationEntity]:
    return await event_service.list_locations(event_id)


@location_router.post("")
async def create_event_location(
    event_id: UUID,
    location: CreateLocationEntity,
    event_service: EventService = event_service_dependency,
):
    return await event_service.create_location(event_id, location)
