import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for i in range(self.rows):
            grid.append([])
            for _ in range(self.cols):
                if randomize:
                    grid[i].append(random.randint(0, 1))
                else:
                    grid[i].append(0)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        x, y = cell

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):

                if i == x and y == j:
                    continue
                elif (-1 < i < len(self.curr_generation) and
                      -1 < j < len(self.curr_generation[0])):
                    neighbours.append(int(self.curr_generation[i][j]))

        return neighbours

    def get_next_generation(self) -> Grid:
        grid = []
        for i in range(self.rows):
            grid.append([])
            for _ in range(self.cols):
                grid[i].append(0)

        for i, row in enumerate(self.curr_generation):
            for j, el in enumerate(row):
                alive_neighbours = sum(self.get_neighbours((i, j)))

                if alive_neighbours in (2, 3) and int(self.curr_generation[i][j]) == 1:
                    grid[i][j] = 1
                elif alive_neighbours == 3 and int(self.curr_generation[i][j]) == 0:
                    grid[i][j] = 1
                else:
                    grid[i][j] = 0

        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []

        with open(filename, 'r') as f:
            next_line = f.readline()
            i = 0
            while len(next_line) > 0 and next_line != '\n':
                grid.append([])
                for el in next_line:
                    if el == '\n':
                        continue
                    grid[i].append(el)
                i += 1
                next_line = f.readline()

        rows = len(grid)
        cols = len(grid[0])

        state = GameOfLife((rows, cols))
        state.curr_generation = grid

        return state

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'w') as f:
            for row in self.curr_generation:
                line = ''
                for el in row:
                    line += str(el)
                f.write(line + '\n')
