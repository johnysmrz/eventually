import pytest

from service.event import EventRepository
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from service.core import EventModel, EventStatus
from datetime import date as date_type
from rich.console import Console

c = Console()

@pytest.fixture
async def event_repository(engine: AsyncEngine) -> EventRepository:
    sessionmaker = async_sessionmaker(bind=engine)
    return EventRepository(sessionmaker)
        
@pytest.fixture
async def session(engine: AsyncEngine):
    sessionmaker = async_sessionmaker(bind=engine)
    async with sessionmaker() as session:
        yield session

@pytest.mark.asyncio
async def test_list_active_events(event_repository: EventRepository, session: AsyncSession):
    session.add_all([
        EventModel(
            name="Test Event 1",
            description="Description for Test Event 1",
            start_date=date_type(2025, 1, 1),
            end_date=date_type(2025, 1, 2),
            status=EventStatus.DRAFT
        ),
        EventModel(
            name="Test Event 2",
            description="Description for Test Event 2",
            start_date=date_type(2025, 1, 3),
            end_date=date_type(2025, 1, 4),
            status=EventStatus.PUBLISHED
        ),
        EventModel(
            name="Test Event 3",
            description="Description for Test Event 3",
            start_date=date_type(2025, 1, 5),
            end_date=date_type(2025, 1, 6),
            status=EventStatus.ARCHIVED
        ),
    ])
    await session.commit()

    events = await event_repository.list_active_events(session=session)
    assert len(events) == 2
    assert all(event.status in (EventStatus.DRAFT, EventStatus.PUBLISHED) for event in events)
