import logging
import logging.config
from contextlib import asynccontextmanager
from pathlib import Path

import yaml
from fastapi import FastAPI

from route import ExceptionHandlingMiddleware
from route.event import event_router
from route.location import location_router
from route.program import program_router

root_logger = logging.getLogger()

logger = logging.getLogger("app")


src_path = Path(__file__).resolve()
logging_config_path = f"{src_path.parent.parent}/logging.yaml"

with Path(logging_config_path).open() as f:
    logger.debug(f"Loading logging configuration from {logging_config_path}")
    cfg = yaml.safe_load(f)
    logging.config.dictConfig(cfg)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)
app.include_router(event_router, prefix="/public/event", tags=["event"])
app.include_router(program_router, prefix="/public/event", tags=["program"])
app.include_router(location_router, prefix="/public/event/{id_event}", tags=["location"])

exception_map = [
    # ExceptionConfiguration(
    #     exception=BalanceNotFoundException,
    #     status_code=404,
    #     app_code="KREDSYS_BALANCE_NOT_FOUND",
    # )
]

app.add_middleware(ExceptionHandlingMiddleware, exception_map=exception_map)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
