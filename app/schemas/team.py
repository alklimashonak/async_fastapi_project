from pydantic import BaseModel, UUID4, Field

from app.schemas.driver import DriverForTeamResponse


class TeamBase(BaseModel):
    name: str | None = Field(max_length=64)


class TeamForUserResponse(TeamBase):
    id: int


class TeamForResponse(TeamForUserResponse):
    owner_id: UUID4
    drivers: list[DriverForTeamResponse]


class TeamDB(TeamForUserResponse):
    owner_id: UUID4


class TeamResponse(BaseModel):
    team: TeamForResponse


class TeamCreate(TeamBase):
    name: str = Field(max_length=64)
    picks: set[int] = Field(min_items=5, max_items=5)


class TeamUpdate(TeamBase):
    pass
