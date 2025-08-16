import asyncclick as click

from container import engine
from service.core.model import create_db
from settings import get_settings
from utils import provision_events, provision_users

settings = get_settings()

@click.group()
async def console():
    ...

@console.group()
async def db():
    ...

@db.command("create")
async def db_create():
    await create_db(engine)

@db.command("provision")
async def db_provision():
    await provision_users()
    await provision_events()

@db.command("recreate")
async def db_recreate():
    await create_db(engine)
    await provision_users()
    await provision_events()

if __name__ == "__main__":
    console()
