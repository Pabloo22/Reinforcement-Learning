from abc import abstractmethod
import numpy as np

from environment import Environment


class Bandit:
    """
    Abstract class for a bandit.
    """

    env: Environment
    k: int
    estimations: np.ndarray

    def __init__(self, env: Environment = None, k: int = 10, default_est: int = 1):
        self.env = env
        self.k = k
        self.estimations = np.full(self.env.k, default_est, dtype=float)

    @abstractmethod
    def choose_action(self):
        pass

    @abstractmethod
    def play(self, iters: int):
        pass

    @staticmethod
    def compare_bandits(bandit1: 'Bandit', bandit2: 'Bandit', iters=1000, reps=1000, seed=None, non_stationary=False):
        """
        :return: [avg_best_action_rate1, avg_reward_rate1], [avg_best_action_rate2, avg_reward_rate2]
        """
        env1 = bandit1.env
        env2 = bandit2.env

        total_reward1 = 0
        total_best_action_rate1 = 0
        total_reward2 = 0
        total_best_action_rate2 = 0

        for _ in range(reps):
            new_env = Environment(env1.k, seed=seed, non_stationary=non_stationary)
            bandit1.env = new_env
            bandit2.env = new_env

            reward1, best_action_rate1, _ = bandit1.play(iters)
            total_reward1 += reward1
            total_best_action_rate1 += best_action_rate1

            reward2, best_action_rate2, _ = bandit2.play(iters)
            total_reward2 += reward2
            total_best_action_rate2 += best_action_rate2

        bandit1.env = env1
        bandit2.env = env2

        avg_best_action_rate1 = round(total_best_action_rate1 / reps, 4)
        avg_best_action_rate2 = round(total_best_action_rate2 / reps, 4)
        avg_reward1 = round(total_reward1 / reps, 4)
        avg_reward2 = round(total_reward2 / reps, 4)

        stats1 = [avg_best_action_rate1, avg_reward1]
        stats2 = [avg_best_action_rate2, avg_reward2]

        return stats1, stats2
