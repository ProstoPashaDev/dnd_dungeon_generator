import copy
from src.services.arithmetic_service import count_dist, count_sum_around, count_space, iterations
from src.dungeons.Dungeon import Dungeon


class Cave(Dungeon):

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.score = 0

    def find_entry(self, state):
        entry = []
        for i in range(self.n):
            if state[i][0] == 0:
                entry.append((i, 0))
            if state[i][-1] == 0:
                entry.append((i, self.m - 1))

        for j in range(self.m):
            if state[0][j] == 0:
                entry.append((0, j))
            if state[-1][j] == 0:
                entry.append((self.n - 1, j))

        return entry

    def decrease_points_border_space(self, i, j):
        if i == 0 or j == 0 or i == self.n - 1 or j == self.m - 1:
            self.score -= 5

    def increase_points_space(self):
        self.score += 1

    def increase_notbig_space(self, i, j, state):
        left, up, right, down = count_dist(i, j, state, self.n, self.m)
        dist = sorted([left, up, right, down], reverse=True)
        if dist[1] <= 2 and dist[2] <= 2 and dist[3] <= 2:
            self.score += 1

    def increase_midwalls(self, state):
        score = 0
        for i in range(self.n):
            for j in range(self.m):
                if state[i][j] == 1:
                    if 1 < i < self.n - 2 and 1 < j < self.m - 2:
                        if state[i - 1][j] + state[i + 1][j] + state[i][j - 1] + state[i][j + 1] >= 3:
                            if state[i - 2][j] + state[i + 2][j] + state[i][j - 2] + state[i][j + 2] <= 2:
                                score += 2.3
        return score

    def decrease_useless_border_space(self, state, entry):
        score = 0
        for i in range(len(entry)):
            if count_sum_around(entry[i][0], entry[i][1], state) == 3:
                score -= 3
        return score

    def decrease_too_many_entries(self, entry):
        return 10 if len(entry) <= 3 else -2 * (len(entry) - 2)

    def decrease_group_useless_border_space(self, state, entry):
        score = 0
        for i in range(len(entry)):
            count_space(entry[i][0], entry[i][1], copy.deepcopy(state))
            if iterations <= 5:
                score -= 3
        return score

    def infection_cave(self, i, j, state):

        self.decrease_points_border_space(i, j)
        self.increase_points_space()

        self.increase_notbig_space(i, j, state)

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
        score += self.increase_midwalls(state)
        score += self.decrease_too_many_entries(entry)
        #score += self.decrease_useless_border_space(state, entry)
        score += self.decrease_group_useless_border_space(state, entry)

        return score
