from __future__ import annotations

import copy
from typing import Tuple

from domain.model.game import Game
from datasource.model.game import GameModel
from datasource.mapper import board_mapper


def to_datasource(game: Game) -> GameModel:
    return GameModel(uuid=game.uuid, board=board_mapper.to_datasource(game.board))


def to_domain(model: GameModel) -> Game:
    return Game(game_uuid=model.uuid, board=board_mapper.to_domain(model.board))
