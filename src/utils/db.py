from datetime import date as date_type
from uuid import UUID

from container import async_session
from service.core import EventModel, ProgramItemModel, UserModel


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
            ProgramItemModel(
                id_program_item=UUID("81f20f69-6f3f-4e55-af11-d173ff41ee4b"),
                id_event=UUID("98992867-827f-4c7b-b603-a435b1234706"),
                name="Knitting steel wires",
                description="A program item about knitting steel wires."
            )
        )
        session.add(
            ProgramItemModel(
                id_program_item=UUID("a8899df5-4296-49ba-ba72-9a001cee3df5"),
                id_event=UUID("98992867-827f-4c7b-b603-a435b1234706"),
                name="Snow fighting in the summer",
                description="A program item about snow fighting in the summer."
            )
        )

        await session.commit()

