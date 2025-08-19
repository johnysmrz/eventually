from uuid import UUID

from fastapi import APIRouter, Depends

from container import service
from service.core import ListResponse
from service.event import EventEntity, EventService, ProgramOverviewEntity

program_router = APIRouter()

event_service_dependency = Depends(service(EventService))


@program_router.get("/{event_id}/program/overview")
async def get_program_overview(
    event_id: UUID,
    event_service: EventService = event_service_dependency,
) -> list[ProgramOverviewEntity]:
    return await event_service.overview(event_id)
