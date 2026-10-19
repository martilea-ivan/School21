from __future__ import annotations

import uuid

from flask import Blueprint, jsonify, request

from domain.model.game import Game
from domain.model.exceptions import GameAlreadyOverError
from domain.service.game_service import GameService
from web.mapper.game_mapper import to_domain, to_web
from web.model.game import GameRequest


def create_game_blueprint(service: GameService) -> Blueprint:
    bp = Blueprint("game", __name__)

    @bp.route("/game", methods=["POST"])
    def create_game() -> tuple:
        game_uuid = service.create_game()
        return jsonify({"uuid": str(game_uuid)}), 201

    @bp.route("/game/<uuid:game_uuid>", methods=["POST"])
    def make_move(game_uuid: uuid.UUID) -> tuple:
        raw_data = request.get_json(silent=True)
        if raw_data is None:
            return jsonify(
                {"error": "invalid_request", "message": "Неверный формат JSON"}
            ), 400

        game_request = GameRequest.model_validate(raw_data)
        game = to_domain(game_request, game_uuid)

        try:
            updated_board = service.get_next_move(game.uuid, game.board)
            response = to_web(Game(game_uuid=game.uuid, board=updated_board))
            return jsonify(response.model_dump(mode="json")), 200
        except GameAlreadyOverError:
            saved_game = service._repository.get(game_uuid)
            response = to_web(saved_game)
            return jsonify(response.model_dump(mode="json")), 200

    return bp
