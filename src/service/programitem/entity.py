from datetime import datetime, timedelta
from uuid import UUID

from pydantic import BaseModel


class ProgramItemEntity(BaseModel):
    id_program_item: UUID
    id_event: UUID
    id_location: UUID
    name: str
    description: str | None
    type: str
    attendee_limit: int | None
    attendee_limit_buffer: int | None
    required_time: int
    before_time_buffer: int
    after_time_buffer: int
    created_by: UUID | None
    created_at: datetime
    updated_by: UUID | None
    updated_at: datetime | None


class CreateProgramItemEntity(BaseModel):
    id_location: UUID
    name: str
    description: str | None
    type: str
    attendee_limit: int | None
    attendee_limit_buffer: int | None
    required_time: timedelta
    before_time_buffer: timedelta
    after_time_buffer: timedelta
