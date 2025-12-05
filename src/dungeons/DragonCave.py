from src.dungeons.Dungeon import Dungeon
from src.services.arithmetic_service import count_dist


class DragonCave(Dungeon):

    def __init__(self, n, m, size):
        self.sizes = {"small": (8, 18),
                      "mid": (10, 30),
                      "big": (15, 45)}

        if not (n == 10 and m == 30):
            self.n = n
            self.m = m
        else:
            self.n = self.sizes[size][0]
            self.m = self.sizes[size][1]
        self.score = 0

    def fitness_function(self, state):
        pass

    def increase_big_corridor(self, i, j, state):
        left, up, right, down = count_dist(i, j, state, self.n, self.m)
        if left + right == 5 or up + down == 5:
            self.score += 2

    def increase_points_space(self):
        self.score += 1


    def infection_cave(self, i, j, state):

        self.increase_points_space()
        self.increase_big_corridor(i, j, state)

        state[i][j] = "*"

        if i - 1 >= 0 and state[i - 1][j] == 0:
            self.infection_cave(i - 1, j, state)

        if i + 1 < self.n and state[i + 1][j] == 0:
            self.infection_cave(i + 1, j, state)

        if j - 1 >= 0 and state[i][j - 1] == 0:
            self.infection_cave(i, j - 1, state)

        if j + 1 < self.m and state[i][j + 1] == 0:
            self.infection_cave(i, j + 1, state)

