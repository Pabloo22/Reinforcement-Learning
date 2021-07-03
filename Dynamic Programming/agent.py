from game import Game
import numpy as np
from copy import deepcopy
from random import choice


class DPAgent:
    """
    Planning by dynamic programming
    """

    game: Game
    state_value_array: np.ndarray  # of floats
    policy: np.ndarray   # of integers

    def __init__(self, game: Game):
        self.game = game

        # All values set to zero at the start
        self.state_value_array = np.zeros(shape=game.maze.size, dtype=float)
        # we start with the random policy
        self.policy = np.array([[{1, 2, 3, 4} for _ in range(game.maze.size[1])] for _ in range(game.maze.size[0])])
        self.reward = -1
        self.gamma = 1

    def train(self, iteration: bool = True, theta: float = 1.):
        if iteration:
            self.__policy_iteration()
        else:
            self.__policy_evaluation()

    def __policy_evaluation(self, theta: float = 1.):
        delta = float("inf")

        while theta <= delta:
            new_state_value_array = deepcopy(self.state_value_array)
            delta = 0
            for i in range(self.game.maze.size[0]):
                for j in range(self.game.maze.size[1]):
                    if self.game.maze[i][j] not in {"/", "X"}:
                        v = self.state_value_array[i][j]
                        new_state_value_array[i][j] = self.__compute_new_value(i, j)
                        delta = max(delta, abs(v - new_state_value_array[i][j]))
            self.state_value_array = new_state_value_array
        self.__policy_improvement(theta)

    def __policy_iteration(self):

        new_state_value_array = deepcopy(self.state_value_array)
        delta = 0
        for i in range(self.game.maze.size[0]):
            for j in range(self.game.maze.size[1]):
                if self.game.maze[i][j] not in {"/", "X"}:
                    v = self.state_value_array[i][j]
                    new_state_value_array[i][j] = self.__compute_new_value(i, j)
                    delta = max(delta, abs(v - new_state_value_array[i][j]))
        self.state_value_array = new_state_value_array
        self.__policy_improvement(iteration=True)

    def __compute_new_value(self, i: int, j: int) -> float:
        actions = self.policy[i][j]
        sm = 0
        for a in actions:
            r, c = self.game.get_new_pos(a, (i, j), mud=False)
            sm += 1/len(actions) * (self.reward + self.gamma*self.state_value_array[r][c])
        if self.game.maze[i][j] == "u":
            sm *= (1 - self.game.stuck_prob)
            sm += self.game.stuck_prob*(self.reward + self.gamma*self.state_value_array[i][j])
        return sm

    def __policy_improvement(self, theta: float = 0.1, iteration=False):
        policy_stable = True
        for i in range(self.game.maze.size[0]):
            for j in range(self.game.maze.size[1]):
                if self.game.maze[i][j] != "/":
                    old_actions = self.policy[i][j]
                    best_actions = {1}
                    mx = float("-inf")
                    for a in range(1, 5):
                        r, c = self.game.get_new_pos(a, (i, j), mud=False)
                        value = self.reward + self.gamma*self.state_value_array[r][c]
                        if self.game.maze[i][j] == "u":
                            value *= (1 - self.game.stuck_prob)
                            value += self.game.stuck_prob * (self.reward + self.gamma*self.state_value_array[i][j])
                        if value > mx:
                            best_actions = {a}
                            mx = value
                        elif value == mx:
                            best_actions.add(a)
                    self.policy[i][j] = best_actions
                    if old_actions != best_actions:
                        policy_stable = False
                else:
                    self.policy[i][j] = set()

        if not policy_stable:
            if iteration:
                self.__policy_iteration()
            else:
                self.__policy_evaluation(theta)

    def move(self, player_pos: tuple[int, int]):
        r, c = player_pos
        return choice(list(self.policy[r][c]))


if __name__ == "__main__":
    agent = DPAgent(Game())
    agent.train1()
    print(agent.state_value_array)
