import numpy as np
from random import random
from random import choice
from time import sleep

from maze import Maze




class Game:
    """
    The objective of the game is to escape of a maze.
    The game has the following elements:
        - The player
        - Walls
        - Mud: there is a chance of stuck and not be able to continue

    Every state is represented by an array of strings which the respective meaning:
        - Empty: "_"
        - Mud: "u"
        - Wall: "/"
        - Exit: "X"
        - Player: "P"
        - Player in mud: "p"
    """

    maze: Maze
    steps: int
    stuck_prob: float
    level: int

    def __init__(self,
                 stuck_prob: float = 0.5,
                 level: int = 0,
                 random_grid: bool = False,
                 grid_size: tuple[int, int] = None):
        self.maze = Maze(grid_size, random_grid, level)
        self.steps = 0
        self.stuck_prob = stuck_prob
        self.level = level

    def get_new_pos(self, direction: int, current_pos: tuple[int, int] = None, mud=True) -> tuple[int, int]:

        r, c = self.maze.player_pos if current_pos is None else current_pos

        if direction == 2:
            new_pos = (r - 1, c)
        elif direction == 4:
            new_pos = (r, c + 1)
        elif direction == 3:
            new_pos = (r + 1, c)
        elif direction == 1:
            new_pos = (r, c - 1)
        else:
            raise ValueError("direction must be: 1=left, 2=up, 3=down or 4=right")

        if self.is_valid_pos(new_pos):
            r, c = self.maze.player_pos
            if self.maze[r][c] == "u" and mud:
                stuck = random() < self.stuck_prob
                new_pos = new_pos if not stuck else self.maze.player_pos
        else:
            new_pos = self.maze.player_pos

        return new_pos

    def move(self, direction: int):
        """
        :param direction:  1=left, 2=up, 3=down, 4=right
        :return: None
        """
        if self.is_finished():
            raise ValueError("The game is over")
        self.maze.player_pos = self.get_new_pos(direction)
        self.steps += 1

    def is_valid_pos(self, pos: tuple[int, int]) -> bool:
        r, c = pos
        return (0 <= r < self.maze.size[0]) and (0 <= c < self.maze.size[1]) and self.maze[r][c] != "/"

    def is_finished(self):
        return self.maze.exit == self.maze.player_pos

    def play(self, policy=None):

        while not self.is_finished():
            print(self)
            if policy is None:
                self.move(Game.ask_move())
            else:
                self.move(self.automatic_move(policy))
                sleep(0.5)

        print(f"You have achieved the goal in {self.steps} steps")

        if self.stuck_prob == 0.5 and self.level:
            with open("high_scores.txt", "r") as f:
                high_scores = list(f.read().split(" "))

            high_score = int(high_scores[self.level-1])

            if self.steps < high_score:
                print("Congratulations! You have beaten the high-score")
                print("old high score: " + str(high_score))
                high_score = str(self.steps)
                high_scores[self.level-1] = high_score
                with open("high_scores.txt", "w") as f:
                    txt = " ".join(high_scores)
                    f.write(txt)
            print("current high score: " + str(high_score))

    def reset(self):
        self.maze.reset()
        self.steps = 0

    def evaluate_agent(self, policy, iters=10_000) -> float:
        puntuations = []

        for _ in range(iters):
            while not self.is_finished():
                self.move(self.automatic_move(policy))
            puntuations.append(self.steps)
            self.reset()

        return float(np.mean(puntuations))

    @staticmethod
    def ask_move() -> int:
        move = int(input("select movement: 1=left, 2=up, 3=down or 4=right -> "))
        return move

    def automatic_move(self, policy):
        r, c = self.maze.player_pos
        return choice(list(policy[r][c]))

    def __str__(self):
        return str(self.maze)
