from random import randint
from itertools import product

INDEX_SHIFT = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))


class Cell:
    """
    Класс для представления клетки игрового поля;

    around_mines - число мин вокруг клетки (начальное значение 0);
    mine - наличие/отсутствие мины в текущей клетке (True/False);
    fl_open - открыта/закрыта клетка - булево значение (True/False). Изначально все клетки закрыты (False).
    """
    def __init__(self, around_mines: int = 0, mine: bool = False) -> None:
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False

    def __str__(self) -> str:
        return "#" if not self.fl_open else self.around_mines if not self.mine else "*"


class GamePole:
    """
    Класс для управления игровым полем, размером N x N клеток.
    """
    def __init__(self, n: int, m: int) -> None:
        self.__n = n
        self.__m = m
        self.pole = [[Cell() for _ in range(self.__n)] for _ in range(self.__n)]
        self.init()

    def init(self) -> None:
        """
        Метод для инициализации поля с новой расстановкой M мин (случайным образом по игровому полю,
        разумеется каждая мина должна находиться в отдельной клетке).
        """
        m = 0
        while m < self.__m:
            i, j = (randint(0, self.__n - 1) for _ in range(2))
            if self.pole[i][j].mine:
                continue
            self.pole[i][j].mine = True
            m += 1

        for x, y in product(range(self.__n), range(self.__n)):
            if not self.pole[x][y].mine:
                count_of_mines: int = sum(
                    (
                        self.pole[x + i][y + j].mine
                        for i, j in INDEX_SHIFT
                        if 0 <= x + i < self.__n and 0 <= y + j < self.__n
                    )
                )
                self.pole[x][y].around_mines = count_of_mines

    def show(self) -> None:
        """
        Метод для отображения поля в консоли в виде таблицы чисел открытых клеток (если клетка не открыта, то
        отображается символ #; мина отображается символом *; между клетками при отображении ставить пробел).
        """
        for row in self.pole:
            print(*map(str, row))


pole_game = GamePole(10, 12)
