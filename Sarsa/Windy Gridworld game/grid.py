import numpy as np
from copy import deepcopy


class Grid:
    """
    The maze is represented by an array of strings which the respective meaning:
        - Empty: "_"
        - Player: "S"
        - Goal: "G"
    """
    __height: int
    width: int
    player_pos: tuple[int, int]
    player_initial_pos: tuple[int, int]
    wind: tuple
    goal_pos: tuple[int, int]
    stochastic_wind: bool
    grid: list[list[str]]

    def __init__(self,
                 size: tuple[int, int] = (7, 10),
                 initial_player_pos: tuple[int, int] = (3, 0),
                 wind: tuple = (0, 0, 0, 1, 1, 1, 2, 2, 1, 0),
                 goal_pos: tuple[int, int] = (3, 7),
                 stochastic_wind: bool = False):

        self.__height, self.__width = size
        self.player_pos = initial_player_pos
        self.player_initial_pos = initial_player_pos
        self.wind = wind
        self.goal_pos = goal_pos
        self.stochastic_wind = stochastic_wind
        self.__grid = [["_"]*size[1] for _ in range(size[0])]

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def grid(self):
        return self.__grid

    def reset(self):
        self.player_pos = self.player_initial_pos

    def __str__(self):

        grid_with_elements = deepcopy(self.grid)
        grid_with_elements.append(list(map(str, self.wind)))
        r, c = self.player_pos
        grid_with_elements[r][c] = "S"
        r_2, c_2 = self.goal_pos
        grid_with_elements[r_2][c_2] = "G"

        return str(np.array(grid_with_elements))

    def __getitem__(self, item):
        return self.grid[item]
