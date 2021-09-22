from windy_gridworld_game import WindyGridworldGame
from agent import SarsaAgent


def training():
    game = WindyGridworldGame(king_moves=True, stochastic_wind=True)
    agent = SarsaAgent(game)
    # game.play()
    agent.load_learning()
    old_avg_score = 12.588764000000106
    print("old score: ", old_avg_score)

    # with a small epsilon the agent doesn't explore enough and ends using with a suboptimal policy
    agent.train(n_episodes=100_000, epsilon=0.1, step_size=0.05)
    avg_score = agent.evaluate_agent(500_000)
    if avg_score < old_avg_score:
        agent.save_learning()
    else:
        print("no improvement")

    print("new_score: ", avg_score)


def player_vs_agent(victories=2):
    agent_wins = 0
    player_wins = 0

    game = WindyGridworldGame(king_moves=True, stochastic_wind=True)
    agent = SarsaAgent(game)
    agent.load_learning()

    while agent_wins < victories and player_wins < victories:
        player_score = game.play()
        agent_score = game.play(agent)
        if player_score < agent_score:
            player_wins += 1
            print("player wins!")
        elif player_score > agent_score:
            agent_wins += 1
            print("SarsaAgent wins!")
        else:
            print("draw")
        print(f"Player: {player_wins}, SarsaAgent: {agent_wins}")


def main():
    game = WindyGridworldGame(king_moves=True, stochastic_wind=True)
    agent = SarsaAgent(game)
    agent.load_learning()
    game.play(agent)


if __name__ == "__main__":
    main()
