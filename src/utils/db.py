from datetime import date as date_type, timedelta
from uuid import UUID

from container import async_session
from datetime import datetime
from service.core import EventModel, ProgramItemModel, UserModel, ProgramSessionModel, AttendeeModel, AttendeeProgramSessionModel, LocationModel


async def provision_users():
    async with async_session() as session:
        user = UserModel(
            id_user=UUID("f2015c51-7808-41c5-8b77-47b0ceecca13"),
            email="user@example.com",
            full_name="Example User"
        )
        session.add(user)
        await session.commit()

async def provision_events():
    async with async_session() as session:
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
            LocationModel(
                id_location=UUID("6bb4dee0-c0c9-407d-b3e3-b752942103d2"),
                id_event=UUID("98992867-827f-4c7b-b603-a435b1234706"),
                name="Agora",
                lat=52.5200,
                lon=13.4050
            )
        )
        session.add(
            LocationModel(
                id_location=UUID("77006683-90a8-46af-a3ea-9ad7af6f5d85"),
                id_event=UUID("98992867-827f-4c7b-b603-a435b1234706"),
                name="Spad",
                lat=52.5200,
                lon=13.4050
            )
        )
        session.add(
            LocationModel(
                id_location=UUID("7c8ed9fd-c3ab-4eba-9710-601c38a21eea"),
                id_event=UUID("98992867-827f-4c7b-b603-a435b1234706"),
                name="Dira",
                lat=52.5200,
                lon=13.4050
            )
        )
        session.add(
            LocationModel(
                id_location=UUID("89bceaee-1906-4a77-add9-6ac105f91f24"),
                id_event=UUID("6cc53c48-44ed-4973-905e-a46c60218d92"),
                name="Brana pekel",
                lat=52.5200,
                lon=13.4050
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
