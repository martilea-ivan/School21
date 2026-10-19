from __future__ import annotations

import uuid
from typing import Optional

from domain.model.board import Board


class Game:
    uuid: uuid.UUID
    board: Board

    def __init__(self, board: Optional[Board] = None, game_uuid: Optional[uuid.UUID] = None) -> None:
        if game_uuid is None:
            self.uuid = uuid.uuid4()
        else:
            self.uuid = game_uuid
        if board is None:
            self.board = Board()
        else:
            self.board = board

    @staticmethod
    def create() -> Game:
        return Game(board=Board())
