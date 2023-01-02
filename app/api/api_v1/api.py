from fastapi import APIRouter

from app.api.api_v1.routers import users, auth, teams

api_router = APIRouter()

api_router.include_router(auth.router, tags=['auth'], prefix='/auth')
api_router.include_router(users.router, tags=['users'], prefix='/users')
api_router.include_router(teams.router, tags=['teams'], prefix='/teams')
