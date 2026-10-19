from __future__ import annotations

from typing import Optional, Tuple

from domain.model.board import Board
from domain.model.exceptions import InvalidBoardError

HUMAN = 1
COMPUTER = -1


def find_best_move(board: Board, player: int) -> Tuple[int, int]:
    empty_cells = board.get_empty_cells()
    if not empty_cells:
        raise InvalidBoardError("Нет свободных клеток для хода.")

    opponent = -player
    best_score = float("-inf")
    best_move: Optional[Tuple[int, int]] = None

    for row, col in empty_cells:
        new_board = board.copy()
        new_board.set_cell(row, col, player)
        score = _minimax(new_board, opponent, depth=0, is_maximizing=False)
        if score > best_score:
            best_score = score
            best_move = (row, col)

    if best_move is None:
        raise InvalidBoardError("Не удалось определить лучший ход.")

    return best_move


def _minimax(board: Board, player: int, depth: int, is_maximizing: bool) -> float:
    winner = board.get_winner()
    if winner == COMPUTER:
        return 10 - depth
    if winner == HUMAN:
        return -10 + depth
    if board.is_full():
        return 0

    empty_cells = board.get_empty_cells()
    opponent = -player

    if is_maximizing:
        best_score = float("-inf")
        for row, col in empty_cells:
            new_board = board.copy()
            new_board.set_cell(row, col, player)
            score = _minimax(new_board, opponent, depth + 1, is_maximizing=False)
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for row, col in empty_cells:
            new_board = board.copy()
            new_board.set_cell(row, col, player)
            score = _minimax(new_board, opponent, depth + 1, is_maximizing=True)
            best_score = min(best_score, score)
        return best_score
