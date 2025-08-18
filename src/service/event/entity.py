from datetime import date, datetime, timedelta
from uuid import UUID

from pydantic import BaseModel


class EventEntity(BaseModel):
    id_event: UUID | None = None
    name: str
    description: str | None = None
    start_date: date
    end_date: date
    status: str | None = None
    created_by: UUID | None = None
    created_at: datetime | None = None
    updated_by: UUID | None = None
    updated_at: datetime | None = None

class ProgramOverviewEntity(BaseModel):
    id_program_item: UUID
    name: str
    type: str | None = None
    attendee_limit: int | None = None
    attendee_limit_buffer: int | None = None
    note: str | None = None
    status: str | None = None
    required_time: timedelta | None = None
    before_time_buffer: timedelta | None = None
    after_time_buffer: timedelta | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    attendee_count: int | None = None
