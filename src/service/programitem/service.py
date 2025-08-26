from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession

from service.core import ProgramItemModel, ProgramType

from .entity import CreateProgramItemEntity, ProgramItemEntity

if TYPE_CHECKING:
    from .repository import ProgramItemRepository

class ProgramItemService:
    def __init__(self, repository: "ProgramItemRepository"):
        self.repository = repository

    async def list_program_items(self, event_id: UUID, session: AsyncSession | None = None) -> list[ProgramItemEntity]:
        async with self.repository.ensure_session(session) as session:
            program_items = await self.repository.list_program_items(event_id=event_id, session=session)
            return [ProgramItemEntity(
                id_program_item=item.id_program_item,
                id_event=item.id_event,
                id_location=item.id_location,
                name=item.name,
                description=item.description,
                type=item.type.value,
                attendee_limit=item.attendee_limit,
                attendee_limit_buffer=item.attendee_limit_buffer,
                required_time=int(item.required_time.total_seconds() // 60),
                before_time_buffer=int(item.before_time_buffer.total_seconds() // 60),
                after_time_buffer=int(item.after_time_buffer.total_seconds() // 60),
                created_by=item.created_by,
                created_at=item.created_at,
                updated_by=item.updated_by,
                updated_at=item.updated_at,
            ) for item in program_items]


    async def create_program_item(self, event_id: UUID, program_item: CreateProgramItemEntity, session: AsyncSession | None = None):
        async with self.repository.ensure_session(session) as session:
            new_program_item_model = ProgramItemModel(
                id_event=event_id,
                id_location=program_item.id_location,
                name=program_item.name,
                description=program_item.description,
                type=ProgramType(program_item.type),
                attendee_limit=program_item.attendee_limit,
                attendee_limit_buffer=program_item.attendee_limit_buffer,
                required_time=program_item.required_time,
                before_time_buffer=program_item.before_time_buffer,
                after_time_buffer=program_item.after_time_buffer,
            )

            await self.repository.create(new_program_item_model, session=session)
