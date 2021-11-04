from random import choice
from time import sleep

from grid import Grid


class WindyGridworldGame:
    """
    Check rules.md to understand the game rules
    """

    __grid: Grid
    __steps: int
    __king_moves: bool

    def __init__(self,
                 size: tuple[int, int] = (7, 10),
                 initial_player_pos: tuple[int, int] = (3, 0),
                 wind: tuple = (0, 0, 0, 1, 1, 1, 2, 2, 1, 0),
                 goal_pos: tuple[int, int] = (3, 7),
                 stochastic_wind: bool = False,
                 king_moves: bool = False):

        self.__grid = Grid(size, initial_player_pos, wind, goal_pos, stochastic_wind)
        self.__steps = 0
        self.__king_moves = king_moves

    @property
    def grid(self):
        return self.__grid

    @property
    def steps(self):
        return self.__steps

    @property
    def king_moves(self):
        return self.__king_moves

    def get_new_pos(self, action: int) -> tuple[int, int]:
        """
        :param action: 1=left, 2=up, 3=down, 4=right, (5=up-right, 6=down-right, 7=up-left, 8=down-left)
        :return: new position
        """

        r, c = self.grid.player_pos

        w = self.grid.wind[c]
        if not self.grid.stochastic_wind:
            r -= w
        else:
            r -= max(choice([w - 1, w, w + 1]), 0)

        match action:
            case 1: c -= 1  # left
            case 2: r -= 1  # up
            case 3: r += 1  # down
            case 4: c += 1  # right
            case _:
                if self.__king_moves:
                    match action:
                        case 5:  # up-right
                            r -= 1
                            c += 1
                        case 6:  # down-right
                            r += 1
                            c += 1
                        case 7:  # up-left
                            r -= 1
                            c -= 1
                        case 8:  # down-left
                            r += 1
                            c -= 1
                        case _:
                            raise ValueError("direction must be: 1=left, 2=up, 3=down, 4=right, "
                                             "5=up-right, 6=down-right, 7=up-left, 8=down-left")
                else:
                    raise ValueError("direction must be: 1=left, 2=up, 3=down or 4=right")

        if action == 2:  # up
            r -= 1
        elif action == 4:  # right
            c += 1
        elif action == 3:  # down
            r += 1
        elif action == 1:  # left
            c -= 1
        elif self.__king_moves:
            if action == 5:  # up-right
                r -= 1
                c += 1
            elif action == 6:  # down-right
                r += 1
                c += 1
            elif action == 7:  # up-left
                r -= 1
                c -= 1
            elif action == 8:  # down-left
                r += 1
                c -= 1
            else:
                raise ValueError("direction must be: 1=left, 2=up, 3=down, 4=right, "
                                 "5=up-right, 6=down-right, 7=up-left, 8=down-left")
        else:
            raise ValueError("direction must be: 1=left, 2=up, 3=down or 4=right")

        if c < 0:
            c = 0
        elif c >= self.grid.width:
            c = self.grid.width - 1

        if r < 0:
            r = 0
        elif r >= self.grid.height:
            r = self.grid.height - 1

        return r, c

    def move(self, action: int) -> int:
        """
        :param action: 1=left, 2=up, 3=down, 4=right, (5=up-right, 6=down-right, 7=up-left, 8=down-left)
        :return: -1, the reward
        """
        if self.is_finished():
            raise ValueError("The game is over")
        self.grid.player_pos = self.get_new_pos(action)
        self.__steps += 1

        return -1

    def is_finished(self) -> bool:
        return self.grid.goal_pos == self.grid.player_pos

    def play(self, agent=None, evaluating_agent=False) -> int:

        while not self.is_finished():
            if not evaluating_agent:
                print(self)
            if agent is None:
                self.move(self.ask_move())
            else:
                self.move(agent.get_action())
                if not evaluating_agent:
                    sleep(0.5)
        if not evaluating_agent:
            print(f"You have achieved the goal in {self.steps} steps")

        score = self.steps
        self.reset()
        return score

    def reset(self):
        self.grid.reset()
        self.__steps = 0

    def ask_move(self) -> int:

        move = int(input("select movement: 1=left, 2=up, 3=down or 4=right -> ")) if not self.__king_moves else \
               int(input("select movement: 1=left, 2=up, 3=down, 4=right, "
                         "5=up-right, 6=down-right, 7=up-left, 8=down-left -> "))

        return move

    def __str__(self):
        return str(self.grid)
