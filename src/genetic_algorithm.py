import copy
import random
from src.dungeons.Cave import Cave
from src.dungeons.DragonCave import DragonCave


class GeneticGenerator:

    def __init__(self, cave_type, size, floors=1, n=10, m=30, maps=3, mutations=0):
        dungeons = {"Cave": Cave(n, m, size),
                    "Dragon cave": DragonCave(n, m, size)}
        self.size = size
        self.floors = floors
        self.maps = maps
        self.dungeon = dungeons[cave_type]
        if not (n == 10 and m == 30):
            self.n = n
            self.m = m
        else:
            self.n = self.dungeon.sizes[size][0]
            self.m = self.dungeon.sizes[size][1]
        self.mutations = mutations if mutations != 0 else self.n * self.m // 50

    def generate_parents(self):
        parents = []
        for k in range(self.maps):
            chromosome = []
            for i in range(self.n):
                a = []
                for j in range(self.m):
                    a.append(random.randint(0, 1))
                chromosome.append(a)
            parents.append(chromosome)
        return parents

    def apply_mutations(self, state, amount):
        state_copy = copy.deepcopy(state)
        for i in range(amount):
            i = random.randint(0, self.n - 1)
            j = random.randint(0, self.m - 1)
            state_copy[i][j] = 0 if state[i][j] == 1 else 1
        return state_copy

    def start_evolution(self, tries=10000):
        parents = self.generate_parents()
        chromosomes = []
        for i in range(len(parents)):
            chromosomes.append((parents[i], self.dungeon.fitness_function(parents[i])))

        for k in range(tries // 10):
            for i in range(len(parents)):
                for j in range(10):
                    child = self.apply_mutations(chromosomes[i][0], self.mutations)
                    result = self.dungeon.fitness_function(child)
                    if result > chromosomes[i][1]:
                        chromosomes[i] = (child, result)
        return chromosomes

    def pretty_print(self, res):
        for i in range(len(res)):
            print("-" * self.m)
            for j in range(len(res[i][0])):
                print(res[i][0][j])
            print("-" * self.m)

    def pretty_print_squares(self, res):
        for i in range(len(res)):
            print("-" * self.m)
            for j in range(len(res[i][0])):
                for k in range(len(res[i][0][j])):
                    print("⬜️" if res[i][0][j][k] == 0 else "⬛️", end="")
                print()
            print("-" * self.m)
