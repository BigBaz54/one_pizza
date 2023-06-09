import math
import os
import random
from recipe import Recipe
import matplotlib.pyplot as plt
import pizza_parser


def first_state(file):
    return Recipe(file)

def get_one_neighbour(state):
    neighbour = state.copy()
    neighbour.toggle_ingredient(random.choice(list(neighbour.ingredients.keys())))
    return neighbour

def next_temperature(temperature, annealing_rate):
    return temperature * annealing_rate

def accept_probability(old_fitness, new_fitness, temperature):
    try :
        return math.exp((new_fitness - old_fitness) / temperature)
    except ZeroDivisionError:
        return 0

def simulated_annealing(file, temperature_init, annealing_rate=0.99, max_iterations=None, objective=None, output_file=None, init_state=None):
    if output_file is None:
        output_file = file.split('/')[1]
    if objective is None and max_iterations is None:
        raise ValueError("Either max_iterations or objective must be specified")
    clients = pizza_parser.parse(file)
    if init_state is None:
        state = first_state(file)
    else:
        state = init_state
    best_state = state
    best_fitness = state.get_score(clients)
    temperature = temperature_init
    count = 0
    if not os.path.exists("solutions/simulated_annealing"):
        os.makedirs("solutions/simulated_annealing")
    while (max_iterations is None or count < max_iterations) and (objective is None or best_fitness < objective):
        neighbour = get_one_neighbour(state)
        if neighbour.get_score(clients) > state.get_score(clients):
            state = neighbour
            if state.get_score(clients) > best_fitness:
                best_state = state
                best_fitness = state.get_score(clients)
        else:
            if random.random() < accept_probability(state.get_score(clients), neighbour.get_score(clients), temperature):
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
    # for temp in [100, 50, 20, 10, 5, 2, 1]:
    #     for rate in [0.99, 0.95, 0.9, 0.8]:
    #         simulated_annealing("data/d_difficile.txt", temperature_init=temp, annealing_rate=rate, max_iterations=1000, output_file=f"d_difficile_{temp}_{str(rate).split('.')[1]}.txt")
    
    # plot results were rate = 0.99
    plot_results(["d_difficile_100_0.99.txt", "d_difficile_50_0.99.txt", "d_difficile_20_0.99.txt", "d_difficile_10_0.99.txt", "d_difficile_5_0.99.txt", "d_difficile_2_0.99.txt", "d_difficile_1_0.99.txt"], ["initial temperature = 100", "initial temperature = 50", "initial temperature = 20", "initial temperature = 10", "initial temperature = 5", "initial temperature = 2", "initial temperature = 1"])