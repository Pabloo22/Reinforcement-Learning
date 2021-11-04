from time import sleep
from copy import deepcopy
import numpy as np
from typing import Union

from racetrack import Racetrack
from player import Human
from agent import MCAgent


class Game:
    """
    The game has the following elements:
        - The player
        - Walls
        - Mud: 50% chance of stucking and not be able to continue

    Every state is represented by an array of strings which the respective meaning:
        - Road: "_"
        - Wall: "%"
        - finish line: "#"
        - Player: "X"
        - Start: "S"
    """

    racetrack: Racetrack
    steps: int
    level: int
    player: Union[Human, MCAgent]

    def __init__(self, level=0, ai: bool = False):
        self.racetrack = Racetrack(level)
        self.steps = 0
        self.level = level
        pos = self.racetrack.get_initial_pos()
        self.player = Human(pos) if not ai else MCAgent(self.racetrack.get_initial_pos(), self)
        self.accident = False

    def get_new_pos(self) -> tuple[int, int]:
        y_0, x_0 = self.player.position
        y, x = self.player.acceleration

        return x_0 + x, y_0 - y

    def is_valid_pos(self, pos: tuple[int, int]) -> bool:
        """
        Check if the position is valid
        :param pos: the position to check
        :return: True if the position is valid, False otherwise
        """
        r, c = pos
        return (0 <= r < self.racetrack.size[0]) and (0 <= c < self.racetrack.size[1]) and self.racetrack[r][c] != "%"

    def is_finished(self) -> bool:
        """
        The game is finished when the player reaches the finish line
        """
        return self.player.position in self.racetrack.finish_line

    def move(self):
        """
        The player moves according to the acceleration
        :return: the new position
        """
        y_0, x_0 = self.player.position
        y, x = self.player.acceleration
        self.racetrack.player_pos = self.player.position
        return y_0 - y, x_0 + x

    def is_valid_action(self, action: tuple[int, int], accelaration: tuple[int, int] = None):
        """
        Check if the action is valid
        :param action: the action to check
        :param accelaration: the current acceleration
        :return: True if the action is valid, False otherwise
        """
        y_0, x_0 = self.player.acceleration if accelaration is None else accelaration
        a_y, a_x = action
        return self.player.is_valid_acceleration(y_0 + a_y, x_0 + a_x)

    def play(self, ai_training=False, epsilon: float = None) -> Union[int, tuple[list[int], list[tuple]]]:
        """
        Reward: -1 per time step, -100 if it crashes
        :param ai_training: wheter if it is a game use it to train or not
        :param epsilon: needed for training, the epsilon for the epsilon-greedy policy used for mantain exploration
        :return: The reward if not training
        """
        reward = 0

        state_action = []
        while not self.is_finished() and not self.accident:
            if not ai_training:
                print(self)
                print(f"current acceleration: {self.player.acceleration}")
            action = self.player.get_action(epsilon)
            while not self.is_valid_action(action):
                if not ai_training:
                    print("velocity can not be more than 5 in any direction neither motionless")
                    print(f"current acceleration: {self.player.acceleration}")
                action = self.player.get_action(epsilon)

            state = (self.player.position[0], self.player.position[1],
                     self.player.acceleration[0], self.player.acceleration[1])

            state_action.append((state, action))
            self.player.update_accelaration(action)
            new_pos = self.move()

            if self.is_valid_pos(new_pos):
                self.player.position = new_pos
                reward -= 1

            else:
                if not ai_training:
                    print("You had an accident!")
                self.accident = True
                reward = -100

            if isinstance(self.player, MCAgent) and not ai_training:
                sleep(0.5)

            self.steps += 1

        if not self.accident and not ai_training:
            print(f"You have achieved the goal in {self.steps} steps")

        if not ai_training:
            with open("high_scores.txt", "r") as f:
                highscores = list(f.read().split(" "))

            high_score = int(highscores[self.level-1])

            if self.steps < high_score and not self.accident:
                print("Congratulations! You have beaten the highscore")
                print("old high score: " + str(high_score))
                high_score = str(self.steps)
                highscores[self.level-1] = high_score
                with open("high_scores.txt", "w") as f:
                    txt = " ".join(highscores)
                    f.write(txt)
            print("current high score: " + str(high_score))

        return reward if not ai_training else (reward, state_action)

    def reset(self):
        """
        Reset the game
        """
        self.player.position = self.racetrack.initial_pos
        self.player.acceleration = (1, 0)
        self.steps = 0
        self.accident = False

    def __str__(self):
        grid = deepcopy(self.racetrack.grid)
        i, j = self.player.position
        grid[i][j] = "X"
        return str(np.array(grid))
