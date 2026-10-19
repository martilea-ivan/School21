from __future__ import annotations

from typing import Annotated, Any, List

from pydantic import BaseModel, Field, model_validator


def _validate_board_cells(value: Any) -> List[List[int]]:
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError("Поле должно содержать ровно 3 строки")
    for row_idx, row in enumerate(value):
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError(f"В строке {row_idx} должно быть ровно 3 столбца")
        for col_idx, cell in enumerate(row):
            if cell not in (0, 1, -1):
                raise ValueError(
                    f"Клетка ({row_idx}, {col_idx}) содержит недопустимое значение {cell}. "
                    f"Ожидалось 0, 1 или -1."
                )
    return value


class BoardSchema(BaseModel):
    cells: Annotated[
        List[List[int]],
        Field(..., description="Матрица поля 3×3"),
    ]

    @model_validator(mode="before")
    @classmethod
    def validate_board(cls, data: Any) -> Any:
        if isinstance(data, dict) and "cells" in data:
            data["cells"] = _validate_board_cells(data["cells"])
        elif isinstance(data, dict):
            data["cells"] = _validate_board_cells(data.get("cells", []))
        else:
            data = _validate_board_cells(data)
        return data
