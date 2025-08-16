from datetime import date
from uuid import UUID

from pydantic import BaseModel

    # __tablename__ = "t_event" # pyright: ignore[reportAssignmentType]
    # id_event: UUID | None = Field(default_factory=uuid4, primary_key=True)
    # name: str = Field(max_length=255, nullable=False)
    # description: str | None = Field(default=None, max_length=1024)
    # start_date: date_type = Field()
    # end_date: date_type = Field()
    # status: EventStatus = Field(default=EventStatus.DRAFT)

class EventEntity(BaseModel):
    id_event: UUID | None = None
    name: str
    description: str | None = None
    start_date: date
    end_date: date
    status: str | None = None
