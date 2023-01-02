from pydantic import BaseModel, UUID4, Field


class TeamBase(BaseModel):
    name: str | None = Field(max_length=64)


class Team(TeamBase):
    id: int
    owner_id: UUID4


class TeamDB(Team):
    id: int
    owner_id: UUID4


class TeamCreate(TeamBase):
    name: str = Field(max_length=64)


class TeamUpdate(TeamBase):
    name: str = Field(max_length=64)


class TeamResponse(BaseModel):
    team: Team
