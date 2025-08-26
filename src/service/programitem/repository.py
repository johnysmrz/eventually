from collections.abc import Sequence
from uuid import UUID

from rich.console import Console
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from service.core import BaseRepository, ProgramItemModel

c = Console()


class ProgramItemRepository(BaseRepository):
    async def list_program_items(self, *, event_id: UUID, session: AsyncSession | None = None) -> Sequence[ProgramItemModel]:
        """
        Asynchronously retrieves a list of program items associated with a specific event.

        Args:
            event_id (UUID): The unique identifier of the event for which to list program items.
            session (AsyncSession, optional): An optional SQLAlchemy asynchronous session. If not provided, a new session will be created.

        Returns:
            Sequence[ProgramItemModel]: A sequence of ProgramItemModel instances corresponding to the given event_id.
        """
        async with self.ensure_session(session) as session:
            result = await session.execute(
                select(ProgramItemModel).where(
                    ProgramItemModel.id_event == event_id
                )
            )
            return result.scalars().all()
