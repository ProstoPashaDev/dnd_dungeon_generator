import copy
from abc import ABC, abstractmethod

from src.services.arithmetic_service import count_dist, count_sum_around, count_space, iterations


class Dungeon(ABC):

    @abstractmethod
    def fitness_function(self, state):
        pass

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

    def decrease_points_border_space(self, i, j, n, m, decrease=5):
        return -decrease if i == 0 or j == 0 or i == n - 1 or j == m - 1 else 0

    def increase_points_space(self, increase=1):
        return increase

    def increase_notbig_space(self, i, j, n, m, state, space=2, increase=1, decrease=0):
        left, up, right, down = count_dist(i, j, state, n, m)
        dist = sorted([left, up, right, down], reverse=True)
        if dist[1] <= space and dist[2] <= space and dist[3] <= space:
            return increase
        return -decrease

    def increase_midwalls(self, n, m, state, increase=2.3):
        """
        Increase score for connected group of 1 around 1 in close radius and 0 in far radius
        :param n:
        :param m:
        :param state:
        :param increase:
        :return:
        """
        score = 0
        for i in range(n):
            for j in range(m):
                if state[i][j] == 1:
                    if 1 < i < n - 2 and 1 < j < m - 2:
                        if state[i - 1][j] + state[i + 1][j] + state[i][j - 1] + state[i][j + 1] >= 3:
                            if state[i - 2][j] + state[i + 2][j] + state[i][j - 2] + state[i][j + 2] <= 2:
                                score += increase
        return score

    def decrease_useless_border_space(self, state, entry, decrease=3):
        score = 0
        for i in range(len(entry)):
            if count_sum_around(entry[i][0], entry[i][1], state) == 3:
                score -= decrease
        return score

    def decrease_too_many_entries(self, entry, increase=10, entry_amount=3, decrease_per_entry=2):
        return increase if len(entry) <= entry_amount else -decrease_per_entry * (len(entry) - 2)

    def decrease_group_useless_border_space(self, state, entry, decrease=3):
        score = 0
        for i in range(len(entry)):
            count_space(entry[i][0], entry[i][1], copy.deepcopy(state))
            if iterations <= 5:
                score -= decrease
        return score

