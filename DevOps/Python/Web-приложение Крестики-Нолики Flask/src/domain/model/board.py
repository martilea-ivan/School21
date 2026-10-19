from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from domain.model.exceptions import InvalidBoardError

VALID_VALUES = (0, 1, -1)
BOARD_SIZE = 3


class Board:
    cells: List[List[int]]

    def __init__(self, cells: Optional[Sequence[Sequence[int]]] = None) -> None:
        if cells is None:
            self.cells = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        else:
            self.cells = [list(row) for row in cells]
        self._validate()

    def _validate(self) -> None:
        if len(self.cells) != BOARD_SIZE:
            raise InvalidBoardError(
                f"Поле должно содержать ровно {BOARD_SIZE} строк, получено {len(self.cells)}"
            )
        for row_idx, row in enumerate(self.cells):
            if len(row) != BOARD_SIZE:
                raise InvalidBoardError(
                    f"В строке {row_idx} должно быть ровно {BOARD_SIZE} столбцов, "
                    f"получено {len(row)}"
                )
            for col_idx, value in enumerate(row):
                if value not in VALID_VALUES:
                    raise InvalidBoardError(
                        f"Клетка ({row_idx}, {col_idx}) содержит недопустимое значение {value}. "
                        f"Ожидалось 0, 1 или -1."
                    )

    def is_full(self) -> bool:
        return all(cell != 0 for row in self.cells for cell in row)

    def is_empty(self) -> bool:
        return all(cell == 0 for row in self.cells for cell in row)

    def get_winner(self) -> Optional[int]:
        lines = self._get_lines()
        for line in lines:
            if len(set(line)) == 1 and line[0] != 0:
                return line[0]
        return None

    def _get_lines(self) -> List[List[int]]:
        lines: List[List[int]] = []
        for i in range(BOARD_SIZE):
            lines.append([self.cells[i][j] for j in range(BOARD_SIZE)])
            lines.append([self.cells[j][i] for j in range(BOARD_SIZE)])
        lines.append([self.cells[i][i] for i in range(BOARD_SIZE)])
        lines.append([self.cells[i][BOARD_SIZE - 1 - i] for i in range(BOARD_SIZE)])
        return lines

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        empty: List[Tuple[int, int]] = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.cells[r][c] == 0:
                    empty.append((r, c))
        return empty

    def copy(self) -> Board:
        new_cells = [list(row) for row in self.cells]
        return Board(cells=new_cells)

    def set_cell(self, row: int, col: int, value: int) -> None:
        if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
            raise InvalidBoardError(
                f"Координаты ({row}, {col}) выходят за пределы поля {BOARD_SIZE}x{BOARD_SIZE}."
            )
        if value not in VALID_VALUES:
            raise InvalidBoardError(
                f"Недопустимое значение клетки {value}. Ожидалось 0, 1 или -1."
            )
        self.cells[row][col] = value
