from asyncio import sleep
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from container import service
from service.event import CreateLocationEntity, EventService, LocationEntity

location_router = APIRouter()

event_service_dependency = Depends(service(EventService))


class AutoFormField(BaseModel):
    id: str
    label: str
    type: str
    required: bool
    pattern: str | None = None
    step: str | None = None
    min: str | None = None
    max: str | None = None
    placeholder: str | None = None
    options: list[dict[str, str]] | None = None
    group: str | None = None

class AutoFormConfig(BaseModel):
    fields: list[AutoFormField]
    groups: list[str] | None = None

@location_router.get("")
async def get_event_locations(
    id_event: UUID,
    event_service: EventService = event_service_dependency,
) -> list[LocationEntity]:
    return await event_service.list_locations(id_event)


@location_router.post("")
async def create_event_location(
    id_event: UUID,
    location: CreateLocationEntity,
    event_service: EventService = event_service_dependency,
):
    new_location_id = await event_service.create_location(id_event, location)
    return await event_service.get_location_by_id(new_location_id)

@location_router.delete("/{location_id}")
async def delete_event_location(
    location_id: UUID,
    event_service: EventService = event_service_dependency,
):
    await event_service.delete_location(location_id)

@location_router.get("/$autoform")
async def get_event_location_options() -> AutoFormConfig:
    return AutoFormConfig(
        fields=[
            AutoFormField(
                id="name",
                label="Název lokace",
                type="text",
                required=True,
                pattern="^[a-zA-Z0-9 ]+$",
                placeholder="Název lokace",
            ),
            AutoFormField(
                id="lat",
                label="Zeměpisná šířka",
                type="number",
                required=False,
                step="0.000001",
                min="-90",
                max="90",
                placeholder="50.058956",
            ),
            AutoFormField(
                id="lon",
                label="Zeměpisná délka",
                type="number",
                required=False,
                step="0.000001",
                placeholder="14.010947"
            ),
            AutoFormField(
                id="color",
                label="Barva",
                type="color",
                required=True,
            ),
        ],
        groups=["General", "Details"]
    )
