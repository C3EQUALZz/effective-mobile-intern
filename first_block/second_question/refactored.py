from random import randint
from dataclasses import dataclass, field
from collections import deque
from typing import Final, Tuple, List
from itertools import product

INDEX_SHIFT: Final[Tuple[Tuple[int, int], ...]] = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))


@dataclass(slots=True)
class Cell:
    around_mines: int = 0
    mine: bool = False
    fl_open: bool = False

    def __str__(self) -> str:
        return "#" if not self.fl_open else self.around_mines if not self.mine else "*"


@dataclass(slots=True)
class GamePole:
    n: int
    m: int
    pole: List[List[Cell]] = field(init=False)

    def __post_init__(self) -> None:
        self.pole = [[Cell() for _ in range(self.m)] for _ in range(self.n)]

        count_of_mines: int = 0
        while count_of_mines < self.m:

            i, j = (randint(0, self.n - 1) for _ in range(2))

            if self.pole[i][j].mine:
                continue

            self.pole[i][j].mine = True
            count_of_mines += 1

        for x, y in product(range(self.n), range(self.n)):
            if not self.pole[x][y].mine:
                self.pole[x][y].around_mines = sum((self.pole[x + i][y + j].mine for i, j in INDEX_SHIFT if
                                                    0 <= x + i < self.n and 0 <= y + j < self.n))

    def __str__(self) -> str:
        result: deque[str] = deque()
        for row in self.pole:
            formatted_row: map = map(str, row)
            result.append(" ".join(formatted_row))
        return "\n".join(result)


pole_game = GamePole(10, 12)
print(pole_game)
