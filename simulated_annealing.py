import math
import os
import random
from recipe import Recipe
import matplotlib.pyplot as plt


def first_state(file):
    return Recipe(file)

def get_one_neighbour(state):
    neighbour = Recipe(file=state.file, ingredients=state.ingredients.copy())
    neighbour.toggle_ingredient(random.choice(list(neighbour.ingredients.keys())))
    return neighbour

def next_temperature(temperature, annealing_rate):
    return temperature * annealing_rate

def accept_probability(old_fitness, new_fitness, temperature):
    try :
        return math.exp((new_fitness - old_fitness) / temperature)
    except ZeroDivisionError:
        return 0

def simulated_annealing(file, temperature_init, annealing_rate=0.99, nb_iter=None, objective=None, output_file=None):
    if output_file is None:
        output_file = file.split('/')[1]
    if objective is None and nb_iter is None:
        raise ValueError("Either nb_iter or objective must be specified")
    state = first_state(file)
    best_state = state
    best_fitness = state.get_score()
    temperature = temperature_init
    count = 0
    if not os.path.exists("solutions/simulated_annealing"):
        os.makedirs("solutions/simulated_annealing")
    while (nb_iter is None or count < nb_iter) and (objective is None or best_fitness < objective):
        neighbour = get_one_neighbour(state)
        if neighbour.get_score() > state.get_score():
            state = neighbour
            if state.get_score() > best_fitness:
                best_state = state
                best_fitness = state.get_score()
        else:
            if random.random() < accept_probability(state.get_score(), neighbour.get_score(), temperature):
                state = neighbour
        if count % 10 == 0:
            with open(os.path.join("solutions", "simulated_annealing", output_file), "a") as f:
                f.write("Iteration: " + str(count) + "\nBest score: " + str(best_fitness) + "\nBest recipe: " + str(best_state.get_ingredients()) + "\n\n")
        count += 1
        temperature = next_temperature(temperature, annealing_rate)
    return best_state


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
        with open(os.path.join("solutions", "simulated_annealing", files[i]), "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("Best score"):
                    scores.append(int(line.split(": ")[1]))
        axs[i%len_side, i//len_side].plot(range(0, len(scores)*10, 10), scores)
        axs[i%len_side, i//len_side].set_title(titles[i])
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    for temp in [100, 50, 20, 10, 5, 2, 1]:
        for rate in [0.99, 0.95, 0.9, 0.8, 0.5, 0.1]:
            simulated_annealing("data/d_difficile.txt", temperature_init=temp, annealing_rate=rate, nb_iter=1000, output_file=f"d_difficile_{temp}_{str(rate).split('.')[1]}.txt")
    plot_results(["d_difficile_100_0.99.txt", "d_difficile_100_0.95.txt", "d_difficile_100_0.9.txt", "d_difficile_100_0.8.txt", "d_difficile_100_0.5.txt"])