from datetime import date, datetime
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
