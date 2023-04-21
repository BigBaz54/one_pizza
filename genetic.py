import os
import random
from get_score import get_score
from get_ingredients import get_ingredients
import matplotlib.pyplot as plt
from recipe import Recipe


def first_generation(file, size):
    return [Recipe(file=file) for _ in range(size)]

def crossover(parent1, parent2):
    child1 = Recipe(ingredients=parent2.ingredients.copy(), file=parent1.file)
    child2 = Recipe(ingredients=parent1.ingredients.copy(), file=parent2.file)
    c = 0
    ingr_nb = len(parent1.ingredients)
    for ingredient in parent1.ingredients:
        if c < ingr_nb/2:
            child1.ingredients[ingredient] = parent1.ingredients[ingredient]
            child2.ingredients[ingredient] = parent2.ingredients[ingredient]
        else:
            break
        c += 1
    return child1, child2

def mutation(recipe, rate):
    for ingredient in recipe.ingredients:
        if random.random() < rate:
            recipe.toggle_ingredient(ingredient)

def selection(recipes, size):
    # only the size best recipes are selected
    recipes.sort(key=lambda recipe: recipe.get_fitness(), reverse=True)
    return recipes[:size]

def tournament_selection(recipes, size):
    # the best recipe is always selected and we still have some randomness
    selected = []
    for i in range(size):
        if recipes[i].get_fitness() > recipes[-i-1].get_fitness():
            selected.append(recipes[i])
        else:
            selected.append(recipes[-i-1])
    return selected

def genetic_algorithm(file, pop_size, mutation_rate, nb_gen=None, objective=None, output_file=None, tournament=False):
    if output_file is None:
        output_file = file.split('/')[1]
    if nb_gen is None and objective is None:
        raise ValueError("Either nb_gen or objective must be specified")
    if pop_size % 2 != 0:
        raise ValueError("Population size must be even")
    gen = first_generation(file, pop_size)
    count = 0
    if not os.path.exists("solutions/genetic"):
        os.makedirs("solutions/genetic")
    while (nb_gen is None or count < nb_gen) and (objective is None or gen[0].get_fitness() < objective):
        with open(os.path.join("solutions", "genetic", output_file), "a") as f:
            f.write("Generation: " + str(count) + "\nBest score: " + str(gen[0].get_fitness()) + "\nBest recipe: " + str(gen[0].get_ingredients()) + "\n\n")
        gen = selection(gen, pop_size//2) if tournament == False else tournament_selection(gen, pop_size//2)
        for i in range(pop_size//4):
            child1, child2 = crossover(gen[i], gen[-i-1])
            mutation(child1, mutation_rate)
            mutation(child2, mutation_rate)
            gen.append(child1)
            gen.append(child2)
        count += 1
    return gen

def plot_results(file, title=None):
    scores = []
    with open(os.path.join("solutions", "genetic", file), "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("Best score"):
                scores.append(int(line.split(": ")[1]))
    plt.plot(scores)
    plt.xlabel("Generation")
    plt.ylabel("Score")
    if title is None:
        title = file.split('.')[0]
    plt.title(title)
    plt.show()



if __name__ == "__main__":
    recipes = genetic_algorithm("data/d_difficile.txt", 100, 0.001, objective=1800, nb_gen=300, output_file="d_difficile_001.txt")

    recipes2 = genetic_algorithm("data/d_difficile.txt", 100, 0.01, objective=1800, nb_gen=300, output_file="d_difficile_01.txt")

    recipes3 = genetic_algorithm("data/d_difficile.txt", 100, 0.05, objective=1800, nb_gen=300, output_file="d_difficile_05.txt")

    recipes4 = genetic_algorithm("data/d_difficile.txt", 100, 0.001, objective=1800, nb_gen=300, output_file="d_difficile_001_T.txt", tournament=True)