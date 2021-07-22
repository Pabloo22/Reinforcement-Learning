from game import Game


def main():
    game = Game(3, True)
    game.player.train(1_000_000)  # level 3 needs at less 1_000_00 episodes
    game.play()


if __name__ == "__main__":
    main()
