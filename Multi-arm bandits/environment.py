import numpy as np


class Environment:

    k: int
    means: np.ndarray
    best_action: int
    non_stationary: bool
    initial_means: np.ndarray

    def __init__(self, n_actions: int, seed=None, non_stationary: bool = False):
        if seed is not None:
            np.random.seed(seed)
        self.k = n_actions
        self.means = np.random.normal(1, size=n_actions)
        self.best_action = int(self.means.argmax())
        self.non_stationary = non_stationary
        self.initial_means = self.means.copy()

    def select(self, action: int) -> float:
        """ returns the reward """
        mean = self.means[action]
        if self.non_stationary:
            self.means[action] -= 0.04
            self.means = np.array(list(map(lambda x: x + 0.02, self.means)))
            self.best_action = int(self.means.argmax())

        return np.random.normal(mean)

    def reset(self):
        self.means = self.initial_means.copy()


if __name__ == "__main__":
    a = np.array([1, 1, 0])
    print(a.argmax())

