import abc


class Player(abc.ABC):

    position: tuple[int, int]  # [row, col]
    acceleration: tuple[int, int]  # [y axis, x axis]  0 <= x,y < 5, velocity != [0, 0]

    def __init__(self, pos: tuple[int, int]):
        self.position = pos
        self.acceleration = (1, 0)
        self.max_speed = 4

    def update_accelaration(self, action: tuple[int, int]):
        y_0, x_0 = self.acceleration
        a_y, a_x = action
        self.acceleration = (y_0 + a_y, x_0 + a_x)

    @abc.abstractmethod
    def get_action(self) -> (tuple[int, int]):
        pass

    def is_valid_acceleration(self, y, x):
        return 0 <= x <= self.max_speed and 0 <= y <= self.max_speed and (x != 0 or y != 0)


class Human(Player):

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def get_action(self) -> (tuple[int, int]):

        y = -2
        while y < -1 or y > 1:
            y = int(input("Enter the change in vertical velocity (-1, 0 or 1): "))
        x = -2
        while x < -1 or x > 1:
            x = int(input("Enter the change in horizontal velocity (-1, 0 or 1): "))

        return y, x
