from pydantic import BaseModel, Field


class DriverBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    short_name: str | None = None


class DriverForTeamResponse(DriverBase):
    id: int


class DriverResponse(DriverForTeamResponse):
    pass


class DriverDB(DriverForTeamResponse):
    pass


class DriverCreate(DriverBase):
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    short_name: str = Field(max_length=3)


class DriverUpdate(DriverBase):
    pass
