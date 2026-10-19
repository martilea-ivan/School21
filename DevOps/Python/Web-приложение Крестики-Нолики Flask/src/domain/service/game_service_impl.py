from __future__ import annotations

import uuid

from domain.model.board import Board
from domain.model.game import Game
from domain.model.exceptions import (
    GameAlreadyOverError,
    GameNotFoundError,
    InvalidMoveError,
)
from domain.service.game_service import GameService
from domain.service.minimax import find_best_move
from datasource.repository.game_repository import GameRepository


class GameServiceImpl(GameService):
    def __init__(self, repository: GameRepository) -> None:
        self._repository = repository

    def create_game(self) -> uuid.UUID:
        game = Game.create()
        self._repository.save(game)
        return game.uuid

    def get_next_move(self, game_uuid: uuid.UUID, board: Board) -> Board:
        self.validate_board(game_uuid, board)

        if self.is_game_over(board):
            raise GameAlreadyOverError(
                f"Игра {game_uuid} уже завершена. Ходы больше не допускаются."
            )

        working = board.copy()
        move = find_best_move(working, player=-1)
        working.set_cell(move[0], move[1], -1)

        saved_game = self._repository.get(game_uuid)
        updated_game = Game(game_uuid=saved_game.uuid, board=working)
        self._repository.save(updated_game)

        return working

    def validate_board(self, game_uuid: uuid.UUID, board: Board) -> None:
        saved_game = self._repository.get(game_uuid)
        saved_board = saved_game.board
        saved_cells = saved_board.cells
        board_cells = board.cells

        forbidden = 0
        empty_to_x = 0
        empty_to_o = 0

        for r in range(3):
            for c in range(3):
                saved_val = saved_cells[r][c]
                current_val = board_cells[r][c]

                if saved_val != 0 and saved_val != current_val:
                    forbidden += 1
                elif saved_val == 0 and current_val == 1:
                    empty_to_x += 1
                elif saved_val == 0 and current_val == -1:
                    empty_to_o += 1

        if forbidden > 0:
            raise InvalidMoveError(
                "Недопустимый ход: предыдущий ход был изменён или удалён."
            )

        if empty_to_o > 0:
            raise InvalidMoveError(
                "Недопустимый ход: клиент не может ставить O (фигура компьютера)."
            )

        if empty_to_x > 1:
            raise InvalidMoveError(
                "Недопустимый ход: за один запрос можно сделать только один ход X."
            )

        x_count = sum(1 for row in board_cells for cell in row if cell == 1)
        o_count = sum(1 for row in board_cells for cell in row if cell == -1)

        if x_count < o_count or x_count - o_count > 1:
            raise InvalidMoveError(
                f"Нарушена очередность ходов: количество X ({x_count}) и O ({o_count}) "
                f"не соответствуют правильному порядку."
            )

    def is_game_over(self, board: Board) -> bool:
        return board.get_winner() is not None or board.is_full()
