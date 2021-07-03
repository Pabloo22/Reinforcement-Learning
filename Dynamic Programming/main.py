from game import Game
from agent import DPAgent


def compare_agents():

    # There are apparently no performance differences between the two ways of training
    game = Game(stuck_prob=0.5, level=4)
    agent1 = DPAgent(game)
    agent1.train(iteration=False)
    print(game.evaluate_agent(agent1.policy))

    agent2 = DPAgent(game)
    agent2.train(iteration=True)
    print(game.evaluate_agent(agent2.policy))


def main():
    game = Game(stuck_prob=0.5, level=4)
    agent1 = DPAgent(game)
    agent1.train(iteration=True)
    game.play(agent1.policy)


if __name__ == "__main__":
    main()
