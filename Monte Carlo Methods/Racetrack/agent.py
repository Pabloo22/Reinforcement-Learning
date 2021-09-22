from copy import deepcopy
from itertools import product
import numpy as np
from random import choice, random

from player import Player


class MCAgent(Player):
    # inherited attributes:
    position: tuple[int, int]
    acceleration: tuple[int, int]  # [y axis, x axis]  0 <= x,y < 5, velocity != [0, 0]

    game: ''  # Game object
    state_action_value_array: np.ndarray  # of floats
    policy: np.ndarray  # of sets of tuples of integers. Indexation: [a_y, a_x, y, x]
    possible_actions: np.ndarray
    counter_array: np.ndarray

    def __init__(self, pos: tuple[int, int], game):
        super().__init__(pos)
        self.game = game

        # All values set to zero at the start
        y, x = game.racetrack.size
        self.state_action_value_array = np.zeros(shape=(9, self.max_speed + 1, self.max_speed + 1, y, x), dtype=float)
        self.counter_array = np.zeros(shape=(9, self.max_speed + 1, self.max_speed + 1, y, x), dtype=float)

        # we start with the random policy
        policy_array = [[[[set(product((-1, 0, 1), repeat=2)) for _ in range(x)] for _ in range(y)]
                         for _ in range(self.max_speed + 1)]
                        for _ in range(self.max_speed + 1)]  # we can not create it with np.full because the array is
        # created with the same set in every position, so a change in one set will affect to all the sets
        self.policy = np.array(policy_array)
        self.possible_actions = deepcopy(self.policy)

    def filter_not_valid_actions(self):

        for a_y, m1 in enumerate(self.policy):
            for a_x, m2 in enumerate(m1):  # shape m1: (5, y, x)
                for y, m3 in enumerate(m2):  # shape m2: (y, x)
                    for x, actions in enumerate(m3):  # shape m3: (x)
                        for action in deepcopy(actions):
                            if not (a_y == 0 and a_x == 0):
                                if not self.game.is_valid_action(action, (a_y, a_x)):
                                    self.policy[a_y][a_x][y][x].remove(action)
                                    self.possible_actions[a_y][a_x][y][x].remove(action)

    def evaluate_agent(self, n_episodes=100):
        avg_reward = 0
        for k in range(1, n_episodes + 1):
            reward, _ = self.game.play(True)
            self.game.reset()
            avg_reward += 1 / k * (reward - avg_reward)

        return avg_reward

    def train(self, n_episodes=100_000,
              rand_start: bool = True,
              epsilon: float = 1.,
              discounter: float = 1.,
              decrease_epsilon: float = 0.,
              n_policy_iters: int = 10,
              min_epsilon: float = 0.02):

        self.filter_not_valid_actions()
        ACTION_NUMBER = {(-1, -1): 0, (-1, 0): 1, (-1, 1): 2,
                         (0, -1): 3, (0, 0): 4, (0, 1): 5,
                         (1, -1): 6, (1, 0): 7, (1, 1): 8}

        for i in range(1, n_episodes + 1):
            reward, state_action = self.game.play(True, epsilon)
            for k, (state, action) in enumerate(reversed(state_action)):
                y, x, a_y, a_x = state
                # calculate the new average
                self.counter_array[ACTION_NUMBER[action], a_y, a_x, y, x] += 1
                n = self.counter_array[ACTION_NUMBER[action], a_y, a_x, y, x]
                self.state_action_value_array[ACTION_NUMBER[action], a_y, a_x, y, x] += \
                    1 / n * (reward * discounter ** k - self.state_action_value_array[
                        ACTION_NUMBER[action], a_y, a_x, y, x])

            self.game.reset()

            if rand_start:
                y = choice(range(self.game.racetrack.size[0]))
                x = choice(range(self.game.racetrack.size[1]))

                possible_accelerations: list[tuple] = list(product((0, 1, 2, 3, 4), (0, 1, 2, 3, 4)))
                possible_accelerations.remove((0, 0))
                acceleration = choice(possible_accelerations)
                if self.game.racetrack[y][x] == "_":
                    self.position = (y, x)
                    self.acceleration = acceleration

            if i % (n_episodes // n_policy_iters) == 0:
                epsilon = max(epsilon - decrease_epsilon, min_epsilon)
                for state, _ in state_action:
                    y, x, a_y, a_x = state
                    best_actions = set()
                    best_reward = float("-inf")
                    for action in self.possible_actions[a_y, a_x, y, x]:
                        expected_reward = self.state_action_value_array[ACTION_NUMBER[action], a_y, a_x, y, x]
                        if expected_reward > best_reward:
                            best_actions = {action}
                            best_reward = expected_reward
                        elif expected_reward == best_reward:
                            best_actions.add(action)
                    self.policy[a_y, a_x, y, x] = best_actions

        for a_y, m1 in enumerate(self.policy):
            for a_x, m2 in enumerate(m1):  # shape m1: (5, y, x)
                for y, m3 in enumerate(m2):  # shape m2: (y, x)
                    for x, actions in enumerate(m3):  # shape m3: (x)
                        best_actions = set()
                        best_reward = float("-inf")
                        for action in actions:
                            expected_reward = self.state_action_value_array[ACTION_NUMBER[action], a_y, a_x, y, x]
                            if expected_reward > best_reward:
                                best_actions = {action}
                                best_reward = expected_reward
                            elif expected_reward == best_reward:
                                best_actions.add(action)
                        self.policy[a_y, a_x, y, x] = best_actions

        self.game.reset()

    def get_action(self, epsilon: float = None) -> (tuple[int, int]):
        a_y, a_x = self.acceleration
        y, x = self.position

        return choice(list(self.policy[a_y][a_x][y][x])) if epsilon is None or random() > epsilon else \
            choice(list(self.possible_actions[a_y][a_x][y][x]))

    def save_learning(self):
        np.save("policy.txt", self.policy)
        np.save("state_action_value.txt", self.state_action_value_array)
        np.save("counter.txt", self.counter_array)
