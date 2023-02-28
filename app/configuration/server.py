import motor
from beanie import init_beanie
from fastapi import FastAPI
from app.configuration.routes import __routes__
from app.configuration.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient
from app.internal.models import __models__




class Server:
    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_routes(app)

    def get_class(self) -> FastAPI:
        return self.__app

    @staticmethod
    async def __register_events(app):
        ...

    @staticmethod
    def __register_routes(app):
        __routes__.register_routes(app)
