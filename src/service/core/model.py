import enum
from datetime import date as date_type
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint
from sqlmodel import DateTime, Field, SQLModel, text

SQLModel.metadata.naming_convention = {
    "ix": "index_%(column_0_label)s",
    "uq": "unique_%(table_name)s_%(column_0_name)s",
    "fk": "foreign_key_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "primary_key_%(table_name)s"
}

def default_datetime_tz() -> datetime:
    """Returns the current datetime in UTC timezone."""
    return datetime.now()


class EventStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class SessionStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"
    ENDED = "ended"


class ProgramType(enum.Enum):
    UNSPECIFIED = "unspecified"
    WORKSHOP = "workshop"
    LECTURE = "lecture"


class LifecycleMixin(SQLModel):
    created_by: UUID | None = Field(
        foreign_key="t_user.id_user",
        nullable=True,
        default=None
    )
    created_at: datetime = Field(
        default_factory=default_datetime_tz,
        sa_type=DateTime,
        sa_column_kwargs={"server_default": text("NOW()")}
    )
    updated_by: UUID | None = Field(
        foreign_key="t_user.id_user",
        nullable=True,
        default=None
    )
    updated_at: datetime | None = Field(
        default=None,
        nullable=True,
        sa_type=DateTime,
        sa_column_kwargs={"onupdate": default_datetime_tz}
    )

class UserModel(LifecycleMixin, table=True):
    __tablename__ = "t_user" # pyright: ignore[reportAssignmentType]
    id_user: UUID | None = Field(
        default=None,
        primary_key=True
    )
    email: str = Field(
        max_length=255,
        nullable=False
    )
    full_name: str | None = Field(
        default=None,
        max_length=255
    )

class EventModel(LifecycleMixin, table=True):
    __tablename__ = "t_event" # pyright: ignore[reportAssignmentType]
    id_event: UUID | None = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=255, nullable=False)
    description: str | None = Field(default=None, max_length=1024)
    start_date: date_type = Field()
    end_date: date_type = Field()
    status: EventStatus = Field(default=EventStatus.DRAFT)

    __table_args__ = (
        CheckConstraint("start_date <= end_date", name="check_event_start_before_end"),
    )


class ProgramItemModel(LifecycleMixin, table=True):
    __tablename__ = "t_program_item" # pyright: ignore[reportAssignmentType]
    id_program_item: UUID | None = Field(default=None, primary_key=True)
    id_event: UUID | None = Field(foreign_key="t_event.id_event", nullable=False)
    name: str = Field(max_length=255, nullable=False)
    description: str | None = Field(default=None, max_length=1024)
    type: ProgramType = Field(default=ProgramType.UNSPECIFIED)


class ProgramSessionModel(LifecycleMixin, table=True):
    __tablename__ = "t_program_session"  # pyright: ignore[reportAssignmentType]
    id_program_session: UUID | None = Field(default=None, primary_key=True)
    id_program_item: UUID | None = Field(foreign_key="t_program_item.id_program_item", nullable=False)
    start_time: datetime = Field(default_factory=default_datetime_tz, sa_type=DateTime)
    end_time: datetime | None = Field(default=None, sa_type=DateTime)
    note: str | None = Field(default=None, max_length=1024)
    status: SessionStatus = Field(default=SessionStatus.DRAFT)


from sqlalchemy.ext.asyncio.engine import AsyncEngine  # noqa: E402


async def create_db(engine: AsyncEngine):
    """
    Asynchronously creates the database schema by dropping existing tables and recreating them.

    Args:
        engine (AsyncEngine): The asynchronous SQLAlchemy engine to use for database operations.
    This function drops the tables 't_event', 't_program_item', and 't_program_session' if they exist,
    and then creates all tables defined in the SQLModel metadata.
    """
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS t_user CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS t_event CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS t_program_item CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS t_program_session CASCADE;"))
        await conn.run_sync(SQLModel.metadata.create_all)
