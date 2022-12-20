import logging
from os import path

import uvicorn
from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.db import database

log_file_path = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(api_router, prefix='/api')


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
