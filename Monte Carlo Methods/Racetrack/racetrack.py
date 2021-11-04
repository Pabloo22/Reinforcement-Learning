import numpy as np
from random import choice
from levels import *


class Racetrack:
    """
    Racetrack class.
    The maze is represented by an array of strings which the respective meaning:
        - Empty: "_"
        - Wall: "/"
        - : "X"
    """
    grid: list[list[str]]
    initial_player_pos: tuple[int, int]
    size: tuple[int, int]
    finish_line: set[tuple[int, int]]

    def __init__(self, level: int):
        self.grid = Racetrack.load_grid(level)
        self.size = (len(self.grid), len(self.grid[0]))
        self.finish_line = self.load_finish_line()
        self.initial_pos = self.get_initial_pos()

    def get_initial_pos(self) -> tuple[int, int]:
        """
        Returns the initial position of the player.
        :return: initial position of the player [i, j]
        """
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if value == "S":
                    return i, j

    def load_finish_line(self) -> set[tuple[int, int]]:
        """
        Returns the finish line of the maze.
        :return: set of finish line positions
        """
        finish_line = set()
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if value == "#":
                    finish_line.add((i, j))

        return finish_line

    @staticmethod
    def create_grid(size: tuple[int, int]) -> list[list[str]]:
        """There are no guarantees that the maze can be solved.
        An easy way to visualize it is converting it into a numpy array"""
        return [[choice(["/", "_", "u", "_"]) for _ in range(size[1])] for _ in range(size[0])]

    @staticmethod
    def load_grid(level: int) -> list[list[str]]:
        """
        Loads the grid from the level.
        :param level: level of the maze (int)
        :return: grid of the maze
        """
        if level == 1:
            return LEVEL_1
        elif level == 2:
            return LEVEL_2
        elif level == 3:
            return LEVEL_3
        else:
            raise ValueError("level not found")

    def __str__(self):
        return str(np.array(self.grid))

    def __getitem__(self, item):
        return self.grid[item]
