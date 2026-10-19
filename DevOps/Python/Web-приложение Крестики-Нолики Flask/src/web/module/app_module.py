from __future__ import annotations

from flask import Flask

from domain.service.game_service import GameService
from web.route.error_handler import register_error_handlers
from web.route.game_route import create_game_blueprint


def create_app(service: GameService) -> Flask:
    app = Flask(__name__)

    game_bp = create_game_blueprint(service)
    app.register_blueprint(game_bp)

    register_error_handlers(app)

    return app
