from random import randint
from dataclasses import dataclass, field
from collections import deque
from typing import Final, Tuple, List
from itertools import product

INDEX_SHIFT: Final[Tuple[Tuple[int, int], ...]] = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))


@dataclass(slots=True)
class Cell:
    count_of_around_mines: int = 0
    is_mine: bool = False
    is_open: bool = False

    def __str__(self) -> str:
        return "#" if not self.is_open else self.count_of_around_mines if not self.is_mine else "*"


@dataclass(slots=True)
class GamePole:
    count_of_rows: int
    count_of_columns: int
    field: List[List[Cell]] = field(init=False)

    def __post_init__(self) -> None:
        self.field = [[Cell() for _ in range(self.count_of_columns)] for _ in range(self.count_of_rows)]

        count_of_mines: int = 0
        while count_of_mines < self.count_of_columns:

            i, j = (randint(0, self.count_of_rows - 1) for _ in range(2))

            if self.field[i][j].is_mine:
                continue

            self.field[i][j].is_mine = True
            count_of_mines += 1

        for x, y in product(range(self.count_of_rows), range(self.count_of_rows)):
            if not self.field[x][y].is_mine:
                count_of_mines: int = sum(
                    (
                        self.field[x + i][y + j].is_mine
                        for i, j in INDEX_SHIFT
                        if 0 <= x + i < self.count_of_rows and 0 <= y + j < self.count_of_rows
                    )
                )
                self.field[x][y].count_of_around_mines = count_of_mines

    def __str__(self) -> str:
        result: deque[str] = deque()
        for row in self.field:
            formatted_row: map = map(str, row)
            result.append(" ".join(formatted_row))
        return "\n".join(result)


pole_game = GamePole(10, 12)
print(pole_game)
