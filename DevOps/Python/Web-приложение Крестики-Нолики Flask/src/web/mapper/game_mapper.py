from __future__ import annotations

import copy
import uuid

from domain.model.board import Board
from domain.model.game import Game
from web.model.board import BoardSchema
from web.model.game import GameRequest, GameResponse


def to_domain(request: GameRequest, game_uuid: uuid.UUID) -> Game:
    board = Board(cells=copy.deepcopy(request.board.cells))
    return Game(game_uuid=game_uuid, board=board)


def to_web(game: Game) -> GameResponse:
    board_schema = BoardSchema(cells=copy.deepcopy(game.board.cells))
    winner = game.board.get_winner()
    return GameResponse(uuid=game.uuid, board=board_schema, winner=winner)
