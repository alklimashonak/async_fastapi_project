import pytest
from httpx import AsyncClient

from app.crud import crud_driver
from app.schemas.driver import DriverCreate, DriverUpdate, DriverDB
from tests.utils.driver import create_test_driver
from tests.utils.team import create_test_team
from tests.utils.user import create_test_user

pytestmark = pytest.mark.anyio


class TestCreateDriver:
    async def test_create_driver_works(
            self,
            async_client: AsyncClient,
    ) -> None:
        driver_in = DriverCreate(
            first_name='Max',
            last_name='Verstappen',
            short_name='VER',
        )

        driver = await crud_driver.create(driver_in=driver_in)

        assert driver
        assert driver.id
        assert driver.first_name == driver_in.first_name
        assert driver.last_name == driver_in.last_name


class TestGetDrivers:
    async def test_get_drivers_works(self) -> None:
        drivers = await crud_driver.get_drivers()

        assert len(drivers) == 1

    async def test_get_drivers_by_ids_works(self) -> None:
        driver = await create_test_driver()
        drivers = await crud_driver.get_drivers_by_ids([driver.id, 2000, 2001, 2002, 2003])

        assert len(drivers) == 1
        assert driver in drivers


class TestGetDriverByID:
    async def test_get_driver_by_existing_id_returns_driver(self) -> None:
        driver_in = DriverCreate(
            first_name='Lewis',
            last_name='Hamilton',
            short_name='HAM',
        )
        test_driver = await crud_driver.create(driver_in=driver_in)

        driver = await crud_driver.get_driver_by_id(driver_id=test_driver.id)

        assert driver
        assert driver.id == test_driver.id
        assert driver.last_name == test_driver.last_name

    async def test_get_driver_by_non_existing_id_returns_none(self) -> None:
        driver = await crud_driver.get_driver_by_id(driver_id=21312)

        assert not driver


class TestGetTeamDrivers:
    async def test_get_team_drivers_works(self) -> None:
        user = await create_test_user()
        team = await create_test_team(owner_id=user.id)

        drivers = await crud_driver.get_team_drivers(team_id=team.id)
        driver1 = drivers[0]

        assert len(drivers) == 5
        assert isinstance(driver1, DriverDB)


class TestUpdateDriver:
    async def test_update_driver_works(self) -> None:
        driver_to_update = await create_test_driver()

        updated_driver_in = DriverUpdate(
            first_name='George',
            last_name='Russel',
            short_name='RUS',
        )

        driver = await crud_driver.update(driver_id=driver_to_update.id, driver_in=updated_driver_in)

        assert driver
        assert driver.id == driver_to_update.id
        assert driver.last_name == updated_driver_in.last_name
