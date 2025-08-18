import pytest

from service.event import EventRepository
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from service.core import EventModel, EventStatus, ProgramItemModel, ProgramSessionModel, AttendeeModel, AttendeeProgramSessionModel
from datetime import date as date_type, datetime, timedelta
from rich.console import Console
from uuid import UUID
from service.event.repository import OverviewResult

c = Console()

@pytest.fixture
async def event_repository(engine: AsyncEngine) -> EventRepository:
    sessionmaker = async_sessionmaker(bind=engine)
    return EventRepository(sessionmaker)
        
@pytest.fixture
async def clean_session(engine: AsyncEngine):
    sessionmaker = async_sessionmaker(bind=engine, autoflush=True)
    async with sessionmaker() as session:
        yield session

@pytest.fixture
async def session(engine: AsyncEngine):
    sessionmaker = async_sessionmaker(bind=engine, autoflush=True)
    async with sessionmaker() as session:
        session.add(
            EventModel(
                id_event=UUID("98992867-827f-4c7b-b603-a435b1234706"),
                name="Example Event",
                description="This is an example event.",
                start_date=date_type(2025, 7, 31),
                end_date=date_type(2025, 8, 2)
            )
        )
        session.add(
            EventModel(
                id_event=UUID("6cc53c48-44ed-4973-905e-a46c60218d92"),
                name="Example Event 2",
                description="This is an example event.",
                start_date=date_type(2025, 9, 10),
                end_date=date_type(2025, 9, 12)
            )
        )
        session.add(
            ProgramItemModel(
                id_program_item=UUID("81f20f69-6f3f-4e55-af11-d173ff41ee4b"),
                id_event=UUID("98992867-827f-4c7b-b603-a435b1234706"),
                name="Knitting steel wires",
                description="A program item about knitting steel wires.",
                required_time=timedelta(hours=2),
                attendee_limit=5
            )
        )
        session.add(
            ProgramItemModel(
                id_program_item=UUID("a8899df5-4296-49ba-ba72-9a001cee3df5"),
                id_event=UUID("98992867-827f-4c7b-b603-a435b1234706"),
                name="Snow fighting in the summer",
                description="A program item about snow fighting in the summer.",
                required_time=timedelta(hours=1, minutes=30),
            )
        )
        session.add(
            ProgramSessionModel(
                id_program_session=UUID("5fcbfce7-c178-4123-b31c-c8e835c81fe9"),
                id_program_item=UUID("81f20f69-6f3f-4e55-af11-d173ff41ee4b"),
                start_time=datetime(2025, 7, 31, 10, 0, 0),
                end_time=datetime(2025, 7, 31, 12, 0, 0),
                note="Test Session Note",
                attendee_limit_override=3
            )
        )
        session.add(
            ProgramSessionModel(
                id_program_session=UUID("7f0c21f7-1040-430e-ac29-74aefd625642"),
                id_program_item=UUID("81f20f69-6f3f-4e55-af11-d173ff41ee4b"),
                start_time=datetime(2025, 7, 31, 14, 30, 0),
                end_time=datetime(2025, 7, 31, 16, 0, 0),
            )
        )
        session.add(
            ProgramSessionModel(
                id_program_session=UUID("2fee4d72-36a9-4ec9-8592-606c3a809992"),
                id_program_item=UUID("81f20f69-6f3f-4e55-af11-d173ff41ee4b"),
                start_time=datetime(2025, 7, 31, 17, 0, 0),
                end_time=datetime(2025, 7, 31, 18, 0, 0),
            )
        )
        session.add(
            ProgramSessionModel(
                id_program_session=UUID("c7672346-1ee2-4234-b096-4b44c00f3311"),
                id_program_item=UUID("81f20f69-6f3f-4e55-af11-d173ff41ee4b"),
                start_time=datetime(2025, 7, 31, 17, 0, 0),
                end_time=datetime(2025, 7, 31, 18, 0, 0),
                note="Test Session Note 2",
            )
        )
        session.add(
            ProgramSessionModel(
                id_program_session=UUID("42dffc7c-a94a-4c94-8445-a8d6f896b8d9"),
                id_program_item=UUID("a8899df5-4296-49ba-ba72-9a001cee3df5"),
                start_time=datetime(2025, 7, 31, 17, 0, 0),
                end_time=datetime(2025, 7, 31, 18, 0, 0),
                attendee_limit_override=2
            )
        )
        await session.commit()
        session.add(
            AttendeeModel(
                id_attendee=UUID("feb4dc59-cc5f-47c7-a101-a6eaa7011935"),
                id_event=UUID("98992867-827f-4c7b-b603-a435b1234706"),
                email="attendee@example.com",
                full_name="Attendee One"
            )
        )
        session.add(
            AttendeeModel(
                id_attendee=UUID("c693e1ca-9342-42d9-9c16-00415a1950e4"),
                id_event=UUID("98992867-827f-4c7b-b603-a435b1234706"),
                email="attendee2@example.com",
                full_name="Attendee Two"
            )
        )
        await session.commit()
        session.add(
            AttendeeProgramSessionModel(
                id_attendee=UUID("feb4dc59-cc5f-47c7-a101-a6eaa7011935"),
                id_program_session=UUID("5fcbfce7-c178-4123-b31c-c8e835c81fe9")
            )
        )
        session.add(
            AttendeeProgramSessionModel(
                id_attendee=UUID("c693e1ca-9342-42d9-9c16-00415a1950e4"),
                id_program_session=UUID("7f0c21f7-1040-430e-ac29-74aefd625642")
            )
        )
        await session.commit()
        yield session

@pytest.mark.asyncio
async def test_list_active_events(event_repository: EventRepository, clean_session: AsyncSession):
    clean_session.add_all([
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
    await clean_session.commit()

    events = await event_repository.list_active_events(session=clean_session)
    assert len(events) == 2
    assert all(event.status in (EventStatus.DRAFT, EventStatus.PUBLISHED) for event in events)


@pytest.mark.asyncio
async def test_event_overview(event_repository: EventRepository, session: AsyncSession):
    overviews = await event_repository.overview(session=session, event_id=UUID("98992867-827f-4c7b-b603-a435b1234706"))
    assert len(overviews) == 5
    assert all(isinstance(overview, OverviewResult) for overview in overviews)
    assert overviews[0].id_program_item == UUID("81f20f69-6f3f-4e55-af11-d173ff41ee4b")
    assert overviews[0].name == "Knitting steel wires"
    assert overviews[0].type == "UNSPECIFIED"
    assert overviews[0].attendee_limit == 3
    assert overviews[0].attendee_limit_buffer is None
    assert overviews[0].note == "Test Session Note"
    assert overviews[0].status == "DRAFT"
    assert overviews[0].required_time == timedelta(hours=2)
    assert overviews[0].before_time_buffer == timedelta(minutes=10)
    assert overviews[0].after_time_buffer == timedelta(minutes=10)
    assert overviews[0].start_time == datetime(2025, 7, 31, 10, 0, 0)
    assert overviews[0].end_time == datetime(2025, 7, 31, 12, 0, 0)
    assert overviews[0].attendee_count == 1