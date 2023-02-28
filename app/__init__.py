from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.configuration.server import Server
from app.configuration.settings import settings
from app.internal.models import __models__
app_: FastAPI


def create_app(_=None) -> FastAPI:
    global app_
    app = FastAPI()
    app_ = Server(app).get_class()

    return Server(app).get_class()


app_ = create_app()


@app_.on_event("startup")
async def startup_event():
    client = AsyncIOMotorClient(settings.db_url)
    print(client, settings.db_url, settings.db_name)
    await init_beanie(
        database=client[settings.db_name], document_models=__models__
    )
