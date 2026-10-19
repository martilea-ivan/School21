from __future__ import annotations

from flask import Flask

from datasource.repository.in_memory_storage import InMemoryStorage
from datasource.repository.game_repository import GameRepository
from domain.service.game_service import GameService
from domain.service.game_service_impl import GameServiceImpl
from web.module.app_module import create_app


class Container:
    def __init__(self) -> None:
        self._storage: InMemoryStorage = InMemoryStorage()
        self._repository: GameRepository = GameRepository(self._storage)
        self._service: GameService = GameServiceImpl(self._repository)

    @property
    def storage(self) -> InMemoryStorage:
        return self._storage

    @property
    def repository(self) -> GameRepository:
        return self._repository

    @property
    def service(self) -> GameService:
        return self._service

    def build_app(self) -> Flask:
        return create_app(self._service)
