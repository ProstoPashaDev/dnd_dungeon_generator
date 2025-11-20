import copy
import random


class GeneticGenerator:

    def __init__(self, cave_type, size, traps, floors=1, n=10):
        self.type = cave_type
        self.size = size
        self.traps = traps
        self.floors = floors
        self.n = n
        self.score = 0

    def generate_parents(self):
        parents = []
        for k in range(3):
            chromosome = []
            for i in range(self.n):
                a = []
                for j in range(self.n):
                    a.append(random.randint(0, 1))
                chromosome.append(a)
            parents.append(chromosome)
        return parents

    def apply_mutations(self, state, amount):
        state_copy = copy.deepcopy(state)
        for i in range(amount):
            i = random.randint(0, self.n - 1)
            j = random.randint(0, self.n - 1)
            state_copy[i][j] = 0 if state[i][j] == 1 else 1
        return state_copy

    def count_dist(self, i, j, state):
        up, left, right, down = 0, 0, 0, 0
        # up
        s = 0
        for i1 in range(0, i):
            if state[i1][j] == 1:
                s = i1
        up = max(i - s - 1, 0)

        # down
        s = self.n - 1
        for i1 in range(i + 1, self.n):
            if state[i1][j] == 1:
                s = i1
                break
        down = max(s - i - 1, 0)

        # left
        s = -1
        for j1 in range(j):
            if state[i][j1] == 1:
                s = j1
        left = max(j - s - 1, 0)

        # right
        s = self.n - 1
        for j1 in range(j + 1, self.n):
            if state[i][j1] == 1:
                s = j1
                break
        right = max(s - j - 1, 0)

        return left, up, right, down

    def infection_cave(self, i, j, state):
        if i == 0 or j == 0 or i == self.n - 1 or j == self.n - 1:
            self.score -= 4
        else:
            self.score += 1

        left, up, right, down = self.count_dist(i, j, state)
        dist = sorted([left, up, right, down], reverse=True)
        if dist[1] <= 2 and dist[2] <= 2 and dist[3] <= 2:
            self.score += 1

        state[i][j] = "*"

        if i - 1 >= 0 and state[i - 1][j] == 0:
            self.infection_cave(i - 1, j, state)

        if i + 1 < self.n and state[i + 1][j] == 0:
            self.infection_cave(i + 1, j, state)

        if j - 1 >= 0 and state[i][j - 1] == 0:
            self.infection_cave(i, j - 1, state)

        if j + 1 < self.n and state[i][j + 1] == 0:
            self.infection_cave(i, j + 1, state)

    def fitness_function_cave(self, state):
        entry = []
        for i in range(self.n):
            if state[0][i] == 0:
                entry.append((0, i))
            if state[-1][i] == 0:
                entry.append((self.n - 1, i))
            if state[i][0] == 0:
                entry.append((i, 0))
            if state[i][-1] == 0:
                entry.append((i, self.n - 1))

        for i in range(len(entry)):
            state_copy = copy.deepcopy(state)
            self.infection_cave(entry[i][0], entry[i][1], state_copy)
            break

        score = self.score
        self.score = 0

        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] == 1:
                    if 1 < i < self.n - 2 and 1 < j < self.n - 2:
                        if state[i - 1][j] + state[i + 1][j] + state[i][j - 1] + state[i][j + 1] >= 3:
                            if state[i - 2][j] + state[i + 2][j] + state[i][j - 2] + state[i][j + 2] <= 2:
                                score += 2

        return score

    def start_evolution(self, tries=100):
        parents = self.generate_parents()
        chromosomes = []
        for i in range(len(parents)):
            chromosomes.append((parents[i], self.fitness_function_cave(parents[i])))

        for k in range(tries):
            for i in range(len(parents)):
                for j in range(10):
                    child = self.apply_mutations(chromosomes[i][0], 6)
                    result = self.fitness_function_cave(child)
                    if result > chromosomes[i][1]:
                        chromosomes[i] = (child, result)
        return chromosomes

    def pretty_print(self, res):
        for i in range(len(res)):
            print("-" * 15)
            for j in range(len(res[i][0])):
                print(res[i][0][j])
            print("-" * 15)

    def pretty_print_squares(self, res):
        for i in range(len(res)):
            print("-" * 15)
            for j in range(len(res[i][0])):
                for k in range(len(res[i][0][j])):
                    print("⬜️" if res[i][0][j][k] == 0 else "⬛️", end = "")
                print()
            print("-" * 15)
