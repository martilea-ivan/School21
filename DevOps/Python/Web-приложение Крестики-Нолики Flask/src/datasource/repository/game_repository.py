from __future__ import annotations

import uuid

from domain.model.game import Game
from domain.model.exceptions import GameNotFoundError
from datasource.model.game import GameModel
from datasource.mapper.game_mapper import to_datasource, to_domain
from datasource.repository.in_memory_storage import InMemoryStorage


class GameRepository:
    def __init__(self, storage: InMemoryStorage) -> None:
        self._storage = storage

    def save(self, game: Game) -> None:
        model = to_datasource(game)
        self._storage.save(model)

    def get(self, game_uuid: uuid.UUID) -> Game:
        model = self._storage.get(game_uuid)
        if model is None:
            raise GameNotFoundError(f"Игра с UUID {game_uuid} не найдена.")
        return to_domain(model)
