import math
import os
import random
import matplotlib.pyplot as plt
from recipe import Recipe
import pizza_parser


def first_generation(file, size):
    return [Recipe(file=file) for _ in range(size)]

def crossover(parent1, parent2):
    child1 = parent1.copy()
    child2 = parent2.copy()
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

def selection(recipes, size, clients=None):
    # only the size best recipes are selected
    recipes.sort(key=lambda recipe: recipe.get_score(clients), reverse=True)
    return recipes[:size]

def tournament_selection(recipes, size, clients=None):
    # the best recipe is always selected and we still have some randomness
    selected = []
    for i in range(size):
        if recipes[i].get_score(clients) > recipes[-i-1].get_score(clients):
            selected.append(recipes[i])
        else:
            selected.append(recipes[-i-1])
    return selected

def genetic_algorithm(file, pop_size, mutation_rate, nb_gen=None, objective=None, output_file=None, tournament=False, shuffle_before_crossover=False):
    if output_file is None:
        output_file = file.split('/')[1]
    if nb_gen is None and objective is None:
        raise ValueError("Either nb_gen or objective must be specified")
    if pop_size % 2 != 0:
        raise ValueError("Population size must be even")
    clients = pizza_parser.parse(file)
    gen = first_generation(file, pop_size)
    count = 0
    if not os.path.exists("solutions/genetic"):
        os.makedirs("solutions/genetic")
    while (nb_gen is None or count < nb_gen) and (objective is None or gen[0].get_score(clients) < objective):
        with open(os.path.join("solutions", "genetic", output_file), "a") as f:
            f.write("Generation: " + str(count) + "\nBest score: " + str(gen[0].get_score(clients)) + "\nBest recipe: " + str(gen[0].get_ingredients()) + "\n\n")
        gen = selection(gen, pop_size//2, clients) if tournament == False else tournament_selection(gen, pop_size//2, clients)
        if shuffle_before_crossover:
            # we keep the best recipe in first position to avoid having to compute all the scores again to get the best recipe
            gen = [gen[0]] + random.sample(gen[1:], len(gen)-1)
        for i in range(pop_size//4):
            child1, child2 = crossover(gen[i], gen[-i-1])
            mutation(child1, mutation_rate)
            mutation(child2, mutation_rate)
            gen.append(child1)
            gen.append(child2)
        count += 1
    return gen

def plot_results(files, titles=None):
    if titles is None:
        titles = files
    elif len(titles) != len(files):
        raise ValueError("Titles must have the same length as files")
    n = len(files)
    len_side = math.ceil(math.sqrt(n))
    fig, axs = plt.subplots(len_side, len_side)
    for i in range(n):
        scores = []
        with open(os.path.join("solutions", "genetic", files[i]), "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("Best score"):
                    scores.append(int(line.split(": ")[1]))
        axs[i%len_side, i//len_side].plot(range(0, len(scores)*10, 10), scores)
        axs[i%len_side, i//len_side].set_title(titles[i])
    fig.tight_layout()
    plt.show()



if __name__ == "__main__":
    # recipes = genetic_algorithm("data/d_difficile.txt", 100, 0.001, objective=1800, nb_gen=1000, output_file="d_difficile_001_2.txt", tournament=True)

    plot_results(["d_difficile_001_2.txt", "d_difficile_001_T_2.txt"], ["Mutation rate = 0.001", "Mutation rate = 0.001, tournament selection"])
