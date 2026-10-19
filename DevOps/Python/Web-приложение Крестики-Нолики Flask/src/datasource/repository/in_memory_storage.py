from __future__ import annotations

import threading
from typing import Dict, Optional

import uuid

from datasource.model.game import GameModel


class InMemoryStorage:
    def __init__(self) -> None:
        self._data: Dict[uuid.UUID, GameModel] = {}
        self._lock = threading.Lock()

    def save(self, game: GameModel) -> None:
        with self._lock:
            self._data[game.uuid] = game

    def get(self, uuid_value: uuid.UUID) -> Optional[GameModel]:
        with self._lock:
            return self._data.get(uuid_value)

    def exists(self, uuid_value: uuid.UUID) -> bool:
        with self._lock:
            return uuid_value in self._data

    def delete(self, uuid_value: uuid.UUID) -> None:
        with self._lock:
            self._data.pop(uuid_value, None)

    def clear(self) -> None:
        with self._lock:
            self._data.clear()
