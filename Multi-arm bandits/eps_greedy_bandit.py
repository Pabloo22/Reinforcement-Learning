import numpy as np
from random import random, randint, choice
from typing import Callable

from bandit import Bandit
from environment import Environment


class EpsBandit(Bandit):
    """
    Epsilon-greedy bandit.
    """

    env: Environment
    estimations: np.ndarray
    epsilon: float
    step_size: Callable[[int], float]

    def __init__(self,
                 env: Environment = None,
                 k: int = 10,
                 default_est=0,
                 epsilon=0.1,
                 step_size: Callable[[int], float] = None):

        super().__init__(env, k, default_est)
        self.epsilon = epsilon
        self.step_size = (lambda n: 1/n) if step_size is None else step_size

    def choose_action(self) -> int:
        """
        Choose action by epsilon-greedy strategy.
        :return: action index
        """
        if random() > self.epsilon:
            mx = max(self.estimations)
            return choice([i for i in range(self.env.k) if self.estimations[i] == mx])
        else:
            return randint(0, self.env.k-1)

    def play(self, iters: int = 10_000):
        """
        Play the game for given number of iterations.
        :param iters: number of iterations
        :return: total reward, best action rate, reward rate
        """
        total_reward = 0
        n_best_action = 0
        self.env.reset()
        for n in range(1, iters+1):
            a = self.choose_action()
            if self.env.best_action == a:
                n_best_action += 1
            reward = self.env.select(a)
            total_reward += reward

            self.estimations[a] += self.step_size(n)*(reward - self.estimations[a])

        reward_goal = self.env.means[self.env.best_action] * iters

        total_reward = round(total_reward, 2)
        best_action_rate = round(n_best_action / iters, 4)
        reward_rate = round(total_reward / reward_goal, 4)

        return total_reward, best_action_rate, reward_rate

    def avg_results(self, reps: int = 100, iters: int = 10_000):
        """
        Average results of given number of repetitions.
        :param reps: number of repetitions
        :param iters: number of iterations per repetition
        :return: total reward, best action rate, reward rate
        """

        total_reward = 0
        total_best_action_rate = 0
        reward_goal = self.env.means[self.env.best_action] * iters

        for _ in range(reps):
            rw, ar, _ = self.play(iters)
            total_reward += rw
            total_best_action_rate += ar

        avg_reward = round(total_reward / reps, 2)
        avg_best_action_rate = round(total_best_action_rate / reps, 4)
        avg_reward_rate = round(avg_reward / reward_goal, 4)

        return avg_reward, avg_best_action_rate, avg_reward_rate
