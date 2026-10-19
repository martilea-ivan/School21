from __future__ import annotations

import logging
from typing import Any

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError

from domain.model.exceptions import (
    DomainError,
    GameNotFoundError,
    InvalidBoardError,
    InvalidMoveError,
)

_logger = logging.getLogger(__name__)

_ERROR_CODE_MAP: dict[type[Exception], str] = {
    GameNotFoundError: "game_not_found",
    InvalidBoardError: "invalid_board",
    InvalidMoveError: "invalid_move",
    DomainError: "domain_error",
}

_HTTP_CODE_MAP: dict[type[Exception], int] = {
    GameNotFoundError: 404,
    InvalidBoardError: 400,
    InvalidMoveError: 400,
    DomainError: 400,
}


def _build_error_response(error: Exception) -> tuple[dict[str, Any], int]:
    error_type = type(error)
    error_code = _ERROR_CODE_MAP.get(error_type, "internal_error")
    http_code = _HTTP_CODE_MAP.get(error_type, 500)

    return {
        "error": error_code,
        "message": str(error),
    }, http_code


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError) -> tuple:
        raw_errors = error.errors()
        serializable_errors = []
        for err in raw_errors:
            serializable_err: dict[str, Any] = {}
            for key, value in err.items():
                if isinstance(value, Exception):
                    serializable_err[key] = str(value)
                elif isinstance(value, dict):
                    serializable_err[key] = {
                        k2: str(v2) if isinstance(v2, Exception) else v2
                        for k2, v2 in value.items()
                    }
                else:
                    serializable_err[key] = value
            serializable_errors.append(serializable_err)
        return jsonify({
            "error": "validation_error",
            "message": serializable_errors,
        }), 400

    @app.errorhandler(GameNotFoundError)
    def handle_game_not_found(error: GameNotFoundError) -> tuple:
        return _build_error_response(error)

    @app.errorhandler(InvalidBoardError)
    def handle_invalid_board(error: InvalidBoardError) -> tuple:
        return _build_error_response(error)

    @app.errorhandler(InvalidMoveError)
    def handle_invalid_move(error: InvalidMoveError) -> tuple:
        return _build_error_response(error)

    @app.errorhandler(DomainError)
    def handle_domain_error(error: DomainError) -> tuple:
        return _build_error_response(error)

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException) -> tuple:
        return jsonify({
            "error": error.name.lower().replace(" ", "_"),
            "message": error.description,
        }), error.code

    @app.errorhandler(Exception)
    def handle_generic_error(error: Exception) -> tuple:
        _logger.exception("Произошло необработанное исключение")
        return jsonify({
            "error": "internal_error",
            "message": "Внутренняя ошибка сервера",
        }), 500
