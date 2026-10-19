from __future__ import annotations

import copy
from typing import Tuple

from domain.model.board import Board
from datasource.model.board import BoardModel


def to_datasource(board: Board) -> BoardModel:
    return BoardModel(cells=copy.deepcopy(board.cells))


def to_domain(model: BoardModel) -> Board:
    return Board(cells=copy.deepcopy(model.cells))
