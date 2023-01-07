import logging

from app import db
from app.db import database
from app.schemas.driver import DriverCreate, DriverDB, DriverUpdate

logger = logging.getLogger(__name__)


async def create(
        driver_in: DriverCreate,
) -> DriverDB | None:
    query = db.drivers.insert() \
        .values(
            first_name=driver_in.first_name,
            last_name=driver_in.last_name,
            short_name=driver_in.short_name,
        ) \
        .returning(db.drivers.c.id, db.drivers.c.first_name, db.drivers.c.last_name, db.drivers.c.short_name)

    driver_row = await database.fetch_one(query=query)
    return DriverDB(**driver_row._mapping) if driver_row else None


async def get_driver_by_id(driver_id: int) -> DriverDB | None:
    query = db.drivers.select() \
        .where(db.drivers.c.id == driver_id)

    driver_row = await database.fetch_one(query=query)
    return DriverDB(**driver_row._mapping) if driver_row else None


async def get_drivers() -> list[DriverDB]:
    query = db.drivers.select()
    rows = await database.fetch_all(query=query)
    return [DriverDB(**row._mapping) for row in rows]


async def get_drivers_by_ids(drivers_ids: list[int]) -> list[DriverDB]:
    query = db.drivers.select() \
        .filter(db.drivers.c.id.in_(drivers_ids))

    drivers = await database.fetch_all(query=query)

    return [DriverDB(**driver._mapping) for driver in drivers]


async def get_team_drivers(team_id: int) -> list[DriverDB]:
    query = db.drivers_teams.select() \
        .where(db.drivers_teams.c.team_id == team_id)

    relations = await database.fetch_all(query=query)

    drivers_ids = [relation.driver_id for relation in relations]

    return await get_drivers_by_ids(drivers_ids=drivers_ids)


async def update(driver_id: int, driver_in: DriverUpdate) -> DriverDB | None:
    query = db.drivers.update() \
        .where(db.drivers.c.id == driver_id) \
        .values(
            first_name=driver_in.first_name,
            last_name=driver_in.last_name,
            short_name=driver_in.short_name,
        ) \
        .returning(db.drivers.c.id, db.drivers.c.first_name, db.drivers.c.last_name, db.drivers.c.short_name)

    driver_row = await database.fetch_one(query=query)
    return DriverDB(**driver_row._mapping) if driver_row else None
