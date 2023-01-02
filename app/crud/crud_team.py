from pydantic import UUID4

from app import db
from app.db import database
from app.schemas.team import TeamCreate, TeamDB


async def create(payload: TeamCreate, owner_id: UUID4):
    query = db.teams.insert() \
        .values(
            name=payload.name,
            owner_id=owner_id,
        ) \
        .returning(db.teams.c.id, db.teams.c.name, db.teams.c.owner_id)

    user_row = await database.fetch_one(query=query)
    return TeamDB(**user_row._mapping) if user_row else None
