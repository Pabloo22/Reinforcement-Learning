from game import Game


def main():
    game = Game(2, True)
    game.player.train(500_000,
                      rand_start=False,
                      epsilon=1,
                      decrease_epsilon=0.0025,
                      discounter=1,
                      n_policy_iters=250,
                      min_epsilon=0.001)  # level 3 needs at less 1_000_00 episodes
    print(game.player.evaluate_agent(100))


if __name__ == "__main__":
    main()
