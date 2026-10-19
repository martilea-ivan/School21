from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from datasource.model.board import BoardModel


@dataclass
class GameModel:
    uuid: uuid.UUID
    board: BoardModel

    def __post_init__(self) -> None:
        if not isinstance(self.uuid, uuid.UUID):
            raise TypeError("GameModel.uuid должен быть экземпляром UUID")

    @staticmethod
    def create(game_uuid: Optional[uuid.UUID] = None,
               cells: Optional[list[list[int]]] = None) -> GameModel:
        if game_uuid is None:
            game_uuid = uuid.uuid4()
        if cells is None:
            cells = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        return GameModel(uuid=game_uuid, board=BoardModel(cells=cells))
