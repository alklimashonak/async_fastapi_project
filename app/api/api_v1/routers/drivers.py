from fastapi import APIRouter, Depends
from starlette import status

from app.api.dependencies import get_current_superuser
from app.crud import crud_driver
from app.schemas.driver import DriverResponse, DriverCreate
from app.schemas.user import UserDB

router = APIRouter()


@router.get('/', response_model=list[DriverResponse])
async def get_drivers() -> list[DriverResponse]:
    drivers = await crud_driver.get_drivers()
    return [DriverResponse(**driver.dict()) for driver in drivers]


@router.post('/', response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
async def create_driver(
        driver_in: DriverCreate,
        current_user: UserDB = Depends(get_current_superuser), # noqa
):
    return await crud_driver.create(driver_in=driver_in)
