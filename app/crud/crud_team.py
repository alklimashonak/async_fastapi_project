from pydantic import UUID4

from app import db
from app.db import database
from app.schemas.team import TeamCreate, TeamDB, TeamUpdate


async def create(
        team_in: TeamCreate,
        owner_id: UUID4
) -> TeamDB | None:
    query = db.teams.insert() \
        .values(
            name=team_in.name,
            owner_id=owner_id,
        ) \
        .returning(db.teams.c.id, db.teams.c.name, db.teams.c.owner_id)
    team_row = await database.fetch_one(query=query)

    for pick in team_in.picks:
        await add_driver(team_id=team_row.id, driver_id=pick)

    return TeamDB(**team_row._mapping) if team_row else None


async def get_team_by_id(team_id: int) -> TeamDB | None:
    query = db.teams.select() \
        .where(db.teams.c.id == team_id)

    team_row = await database.fetch_one(query=query)
    return TeamDB(**team_row._mapping) if team_row else None


async def update(team_id: int, team_in: TeamUpdate) -> TeamDB | None:
    query = db.teams.update() \
        .where(db.teams.c.id == team_id) \
        .values(name=team_in.name) \
        .returning(db.teams.c.id, db.teams.c.name, db.teams.c.owner_id)

    team_row = await database.fetch_one(query=query)
    return TeamDB(**team_row._mapping) if team_row else None


async def get_user_teams(user_id: UUID4) -> list[TeamDB]:
    query = db.teams.select() \
        .where(db.teams.c.owner_id == user_id)

    team_rows = await database.fetch_all(query=query)
    return [TeamDB(**team_row._mapping) for team_row in team_rows]


async def add_driver(team_id: int, driver_id: int) -> None:
    query = db.drivers_teams.insert() \
        .values(
            team_id=team_id,
            driver_id=driver_id,
        ) \
        .returning(db.drivers_teams.c.driver_id)
    await database.execute(query=query)
