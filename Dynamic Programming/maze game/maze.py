from copy import deepcopy
import numpy as np
from random import choice

from levels import *


class Maze:
    """
    The maze is represented by an array of strings which the respective meaning:
        - Empty: "_"
        - Mud: "u"
        - Wall: "/"
        - Exit: "X"
    """
    grid: list[list[str]]
    player_pos: tuple[int, int]
    size: tuple[int, int]
    exit: tuple[int, int]

    def __init__(self, size: tuple[int, int] = (18, 18), random=True, level: int = 2):
        self.grid = Maze.load_grid(level) if not random else Maze.create_grid(size)
        self.size = (len(self.grid), len(self.grid[0]))
        self.player_pos = (0, 0)
        self.exit = (self.size[0] - 1, self.size[1] - 1)

    def reset(self):
        """
        Resets the maze to its initial state
        """
        self.player_pos = (0, 0)

    @staticmethod
    def create_grid(size: tuple[int, int]) -> list[list[str]]:
        """There are no guarantees that the maze can be solved.
        An easy way to visualize it is converting it into a numpy array"""
        return [[choice(["/", "_", "u", "_"]) for _ in range(size[1])] for _ in range(size[0])]

    @staticmethod
    def load_grid(level: int) -> list[list[str]]:
        """
        Loads a grid from a file
        :param level: The level of the grid
        :return: The grid
        """
        if level == 1:
            return LEVEL_1
        elif level == 2:
            return LEVEL_2
        elif level == 3:
            return LEVEL_3
        elif level == 4:
            return LEVEL_4
        else:
            raise ValueError("level not found")

    def __str__(self):
        grid_with_player = deepcopy(self.grid)
        r, c = self.player_pos
        grid_with_player[r][c] = "P" if grid_with_player[r][c] != "u" else "p"

        return str(np.array(grid_with_player))

    def __getitem__(self, item):
        return self.grid[item]
