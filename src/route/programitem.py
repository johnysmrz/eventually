from uuid import UUID

from fastapi import APIRouter, Depends

from container import service
from service.programitem import CreateProgramItemEntity, ProgramItemEntity, ProgramItemService

programitem_router = APIRouter()

event_service_dependency = Depends(service(ProgramItemService))


@programitem_router.get("")
async def list_program_items(
    event_id: UUID,
    event_service: ProgramItemService = event_service_dependency,
) -> list[ProgramItemEntity]:
    return await event_service.list_program_items(event_id)


@programitem_router.post("")
async def create_program_item(
    event_id: UUID,
    program_item: CreateProgramItemEntity,
    event_service: ProgramItemService = event_service_dependency,
):
    return await event_service.create_program_item(event_id, program_item)
