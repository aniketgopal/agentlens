from __future__ import annotations

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.core.config import settings


class MongoRepository:
    def __init__(self, database: Database | None = None) -> None:
        self._database = database

    @property
    def database(self) -> Database:
        if self._database is None:
            client = MongoClient(settings.mongodb_uri)
            self._database = client[settings.mongodb_database]
        return self._database

    def collection(self, name: str) -> Collection:
        return self.database[name]
