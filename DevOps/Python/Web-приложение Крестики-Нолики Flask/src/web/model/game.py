from __future__ import annotations

import uuid
from typing import Annotated, Optional

from pydantic import BaseModel, Field

from web.model.board import BoardSchema


class GameRequest(BaseModel):
    board: Annotated[
        BoardSchema,
        Field(..., description="Текущее состояние поля с ходом человека"),
    ]


class GameResponse(BaseModel):
    uuid: Annotated[
        uuid.UUID,
        Field(..., description="Уникальный идентификатор игры"),
    ]
    board: Annotated[
        BoardSchema,
        Field(..., description="Обновлённое состояние поля"),
    ]
    winner: Annotated[
        Optional[int],
        Field(default=None, description="ID победителя: 1 (X) или -1 (O). None при ничьей или в процессе игры."),
    ]


class GameErrorResponse(BaseModel):
    error: Annotated[
        str,
        Field(..., description="Код ошибки"),
    ]
    message: Annotated[
        str,
        Field(..., description="Описание ошибки"),
    ]
