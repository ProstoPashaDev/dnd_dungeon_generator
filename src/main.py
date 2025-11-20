from src.genetic_algorithm import GeneticGenerator

print("Welcome to DND dungeon generator created by Pavel")
print("Please enter type of dungeon from the list below")
print("-"*10)
print("Cave \nCave with rooms \nDragon cave")
print("Human-built \nTomb \nSanctuary")
print("-"*10)

generic_generator = GeneticGenerator("Cave", "Small", "No", 1, 20)
cave = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
#print(generic_generator.fitness_function_cave(cave))

res = generic_generator.start_evolution(1500)
#generic_generator.pretty_print(res)
generic_generator.pretty_print_squares(res)

