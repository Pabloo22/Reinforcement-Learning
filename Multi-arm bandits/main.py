from bandit import Bandit
from environment import Environment
from eps_greedy_bandit import EpsBandit


def main():
    e = Environment(10, seed=10, non_stationary=True)
    iters = 1000
    reps = 1000

    b1 = EpsBandit(e, epsilon=0.1, default_est=1, step_size=lambda n: 0.1)
    b2 = EpsBandit(e, epsilon=0.1, default_est=1, step_size=lambda n: 0.9)

    print(Bandit.compare_bandits(b1, b2, iters=iters, reps=reps, non_stationary=True))


if __name__ == "__main__":
    main()
