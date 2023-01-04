from pydantic import BaseModel, UUID4, Field


class TeamBase(BaseModel):
    name: str | None = Field(max_length=64)


class TeamForUserResponse(TeamBase):
    id: int


class TeamForResponse(TeamForUserResponse):
    owner_id: UUID4


class TeamDB(TeamForResponse):
    pass


class TeamResponse(BaseModel):
    team: TeamForResponse


class TeamCreate(TeamBase):
    name: str = Field(max_length=64)


class TeamUpdate(TeamBase):
    name: str = Field(max_length=64)
