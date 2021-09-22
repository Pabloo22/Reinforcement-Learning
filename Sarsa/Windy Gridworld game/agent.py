import numpy as np
from random import choice, random
from tqdm import trange
from typing import Union

from windy_gridworld_game import WindyGridworldGame


class SarsaAgent:

    __game: WindyGridworldGame
    __state_action_value_array: Union[list[list[float]], np.ndarray]

    def __init__(self, game):
        self.__game = game

        # The matrix is converted to a single array
        # One reason for this choice is that the spatial aspect of the problem is secondary and there is no need for
        # the agent to know about the exact dimensions of the environment.
        w, h = self.game.grid.width, self.game.grid.height
        n_actions = 8 if self.game.king_moves else 4
        # The initial value could be any. Nevertheless, it is better to use an optimistic one to encourage exploration.
        # Moreover, setting the initial value to zero avoid the need to set manually terminal
        # state-action pairs to zero.
        self.__state_action_value_array = [[0. for _ in range(n_actions)] for _ in range(w * h)]

    @property
    def game(self):
        return self.__game

    @property
    def state_action_value_array(self):
        return self.__state_action_value_array

    def get_state(self, r, c) -> int:
        w = self.game.grid.width
        return r * w + c

    def train(self, n_episodes=100_000, step_size: float = 0.1, epsilon: float = 0.1, discounter: float = 1.):
        """
        We use Sarsa(0), an on-policy TD control algorithm. We consider transitions
        from state–action pair to state–action pair, and learn the value of state–action pairs.

        :param n_episodes: the number of episodes we want to simulate
        :param step_size: the alpha parameter in
        :param epsilon: we follow a epsilon greedy policy in order to maintain exploration
        :param discounter: the gamma parameter
        """
        q = self.__state_action_value_array
        for _ in trange(n_episodes):
            state = self.get_state(*self.game.grid.player_pos)
            action = self.get_action(epsilon)
            while not self.game.is_finished():
                reward = self.game.move(action)
                new_state = self.get_state(*self.game.grid.player_pos)
                new_action = self.get_action(epsilon)
                q[state][action-1] += step_size*(reward + discounter*q[new_state][new_action-1] - q[state][action-1])
                state = new_state
                action = new_action
            self.game.reset()

    def evaluate_agent(self, n_episodes=100):
        """
        :return: the avg reward after n episodes (100 by default)
        """
        avg_reward = 0
        for k in trange(1, n_episodes + 1):
            reward = self.game.play(agent=self, evaluating_agent=True)
            self.game.reset()
            avg_reward += 1 / k * (reward - avg_reward)
        return avg_reward

    def get_action(self, epsilon: float = 0.) -> int:
        r, c = self.game.grid.player_pos  # The current step
        s = self.get_state(r, c)
        q = self.__state_action_value_array

        n_actions = 8 if self.game.king_moves else 4
        set_of_actions = range(1, n_actions+1)
        mx = max(q[s])
        best_actions = [a for a in set_of_actions if q[s][a-1] == mx]
        return choice(best_actions) if random() > epsilon else choice(set_of_actions)

    def save_learning(self, safe_rewrite=True):

        if self.game.king_moves and self.game.grid.stochastic_wind and safe_rewrite:
            with open("learning/q_king_stochastic.npy", "wb") as f:
                # noinspection PyTypeChecker
                np.save(f, np.array(self.__state_action_value_array))
            print("learning saved!")
        else:
            print("save learning allowed only to games with stochastic wind and king moves")

    def load_learning(self):

        with open("learning/q_king_stochastic.npy", "rb") as f:
            # noinspection PyTypeChecker
            self.__state_action_value_array = np.load(f)
