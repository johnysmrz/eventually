from fastapi import APIRouter, Depends

from container import service
from service.core import ListResponse
from service.event import EventEntity, EventService

event_router = APIRouter()

event_service_dependency = Depends(service(EventService))

@event_router.get("")
async def list_events(
    event_service: EventService = event_service_dependency,
) -> ListResponse[EventEntity]:
    events = await event_service.list_events()
    return ListResponse(
        data=events,
        limit=999,
        offset=0,
        total=len(events)
    )
