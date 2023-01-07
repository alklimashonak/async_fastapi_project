import logging

from faker import Faker

from app.crud import crud_driver
from app.schemas.driver import DriverCreate, DriverDB

logger = logging.getLogger(__name__)

fake = Faker()


async def create_test_driver(
        first_name: str | None = None,
        last_name: str | None = None,
        short_name: str | None = None,
) -> DriverDB:
    if not first_name:
        first_name = fake.unique.first_name()
    if not last_name:
        last_name = fake.unique.last_name()
    if not short_name:
        short_name = first_name[0:2].upper() + last_name[0:3].upper()

    driver_data = DriverCreate(
        first_name=first_name,
        last_name=last_name,
        short_name=short_name,
    )

    return await crud_driver.create(driver_in=driver_data)
