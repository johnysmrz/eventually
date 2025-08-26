import logging

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from di import Container
from service.event import EventRepository, EventService
from service.programitem import ProgramItemRepository, ProgramItemService
from settings import Settings, get_settings

logger = logging.getLogger("container")
container = Container()

settings: Settings = get_settings()

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)

async_session: async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

event_repository = EventRepository(async_session)
container.add(EventRepository, event_repository)

event_service = EventService(event_repository)
container.add(EventService, event_service)

programitem_repository = ProgramItemRepository(async_session)
container.add(ProgramItemRepository, programitem_repository)

programitem_service = ProgramItemService(programitem_repository)
container.add(ProgramItemService, programitem_service)

container.spinup()

service = container.get
