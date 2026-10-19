from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from domain.model.board import Board
from domain.model.exceptions import DomainError


class GameService(ABC):
    @abstractmethod
    def create_game(self) -> uuid.UUID:
        pass

    @abstractmethod
    def get_next_move(self, game_uuid: uuid.UUID, board: Board) -> Board:
        pass

    @abstractmethod
    def validate_board(self, game_uuid: uuid.UUID, board: Board) -> None:
        pass

    @abstractmethod
    def is_game_over(self, board: Board) -> bool:
        pass
