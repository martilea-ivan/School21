from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence


@dataclass
class BoardModel:
    cells: List[List[int]]

    def __post_init__(self) -> None:
        if not isinstance(self.cells, list):
            raise TypeError("BoardModel.cells должен быть списком списков")
        for row in self.cells:
            if not isinstance(row, list):
                raise TypeError("BoardModel.cells должен быть списком списков ц��лых чисел")
