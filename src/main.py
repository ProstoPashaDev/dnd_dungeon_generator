from src.genetic_algorithm import GeneticGenerator

print("Welcome to DND dungeon generator created by Pavel")
print("Please enter type of dungeon from the list below")
print("-"*10)
print("Cave \nCave with rooms \nDragon cave")
print("Human-built \nTomb \nSanctuary")
print("-"*10)

cave = "Cave"
dragon_cave = "Dragon cave"

generic_generator = GeneticGenerator(dragon_cave, "mid", 1)

#print(generic_generator.fitness_function_cave(cave))

res = generic_generator.start_evolution(10000)
#generic_generator.pretty_print(res)
generic_generator.pretty_print_squares(res)

