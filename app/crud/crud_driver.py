from app import db
from app.db import database
from app.schemas.driver import DriverCreate, DriverDB, DriverUpdate


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
