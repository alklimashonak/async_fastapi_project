from pydantic import BaseModel, UUID4, Field


class TeamBase(BaseModel):
    name: str | None


class TeamDB(TeamBase):
    id: int
    name: str = Field(max_length=64)
    owner_id: UUID4


class TeamCreate(TeamBase):
    name: str = Field(max_length=64)


class TeamUpdate(TeamBase):
    name: str = Field(max_length=64)


class TeamResponse(BaseModel):
    team: TeamBase
