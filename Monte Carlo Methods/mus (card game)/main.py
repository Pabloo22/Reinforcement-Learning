from game import MusGame
from player import Human
from ai import Agent


def main():
    p1 = Human()
    p2 = Agent()

    game = MusGame(10, p1, p2)
    game.play()


if __name__ == "__main__":
    main()
