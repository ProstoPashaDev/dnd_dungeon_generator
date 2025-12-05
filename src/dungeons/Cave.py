import copy
from src.services.arithmetic_service import count_dist, count_sum_around, count_space, iterations
from src.dungeons.Dungeon import Dungeon


class Cave(Dungeon):

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

    def infection_cave(self, i, j, state):

        self.score += self.decrease_points_border_space(i, j, self.n, self.m, decrease=5)
        self.score += self.increase_points_space(increase=1)
        self.score += self.increase_notbig_space(i, j, self.n, self.m, state, increase=1)

        state[i][j] = "*"

        if i - 1 >= 0 and state[i - 1][j] == 0:
            self.infection_cave(i - 1, j, state)

        if i + 1 < self.n and state[i + 1][j] == 0:
            self.infection_cave(i + 1, j, state)

        if j - 1 >= 0 and state[i][j - 1] == 0:
            self.infection_cave(i, j - 1, state)

        if j + 1 < self.m and state[i][j + 1] == 0:
            self.infection_cave(i, j + 1, state)

    def fitness_function(self, state):
        entry = self.find_entry(state)
        for i in range(len(entry)):
            state_copy = copy.deepcopy(state)
            self.infection_cave(entry[i][0], entry[i][1], state_copy)
            break

        score = self.score
        self.score = 0
        score += self.increase_midwalls(self.n, self.m, state)
        score += self.decrease_too_many_entries(entry)
        #score += self.decrease_useless_border_space(state, entry)
        score += self.decrease_group_useless_border_space(state, entry)

        return score
