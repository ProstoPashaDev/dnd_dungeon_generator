import copy

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

    def increase_mid_corridor(self, i, j, state, increase=3.0, decrease=0):
        left, up, right, down = count_dist(i, j, state, self.n, self.m)
        if (5 <= left + right <= 7) or (5 <= up + down <= 8):
            return increase if left + right < 6 else increase - 1
        else:
            return -decrease

    def increase_big_space(self, i, j, state, increase=3, decrease=0):
        left, up, right, down = count_dist(i, j, state, self.n, self.m)
        if 10 < left + right + up + down < 16 and left > 1 and right > 1 and up > 1 and down > 1:
            return increase
        else:
            return -decrease

    def check_1_connect_1(self, n, m, state, increase=1.0):
        score = 0
        for i in range(n):
            for j in range(m):
                if state[i][j] == 1:
                    left, up, right, down = count_dist(i, j, state, self.n, self.m)
                    if left == 0 or right == 0 or up == 0 or down == 0:
                        score += increase
        return score

    def check_dragon_size(self, i, j, n, m, state, dragon_size=3, increase_per_cell=3, decrease=0):
        res = 0
        half_size = dragon_size // 2
        if i - half_size < 0 or i + half_size > n - 1 or j - half_size < 0 or j + half_size > m - 1:
            return -decrease

        left, up, right, down = count_dist(i, j, state, self.n, self.m)
        if left + right > 4 or up + down > 4:
            return -decrease

        for k in range(dragon_size):
            res += self.sum_with_star(state[i - half_size + k][j - half_size:j + half_size + 1:])
        if res == 0:
            return increase_per_cell * dragon_size ** 2
        else:
            return -decrease

    def sum_with_star(self, lis):
        s = 0
        for i in range(len(lis)):
            s += (lis[i] if lis[i] != "*" else 0)
        return s

    def fitness_function(self, state):
        entry = self.find_entry(state)
        for i in range(len(entry)):
            state_copy = copy.deepcopy(state)
            self.infection_cave(entry[i][0], entry[i][1], state_copy)
            break

        #self.score += self.increase_midwalls(self.n, self.m, state)
        self.score += self.check_1_connect_1(self.n, self.m, state, increase=0.5)

        score = self.score
        self.score = 0
        return score

    def infection_cave(self, i, j, state):

        self.score += self.increase_points_space()
        self.score += self.decrease_points_border_space(i, j, self.n, self.m)
        #self.score += self.increase_big_space(i, j, state)
        self.score += self.increase_mid_corridor(i, j, state, increase=2, decrease=0)
        self.score += self.check_dragon_size(i, j, self.n, self.m, state)
        #self.score += self.increase_notbig_space(i, j, self.n, self.m, state, space=3, decrease=1)

        state[i][j] = "*"

        if i - 1 >= 0 and state[i - 1][j] == 0:
            self.infection_cave(i - 1, j, state)

        if i + 1 < self.n and state[i + 1][j] == 0:
            self.infection_cave(i + 1, j, state)

        if j - 1 >= 0 and state[i][j - 1] == 0:
            self.infection_cave(i, j - 1, state)

        if j + 1 < self.m and state[i][j + 1] == 0:
            self.infection_cave(i, j + 1, state)
