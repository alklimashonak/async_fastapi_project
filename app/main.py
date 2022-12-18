import logging

import uvicorn
from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.db import database

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(api_router, prefix='/api')


@app.on_event("startup")
async def startup() -> None:
    logger.info("Connect to database")
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    logger.info("Disconnect to database")
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
