import math
import os
import random
from recipe import Recipe


def first_state(file):
    return Recipe(file)

def get_one_neighbour(state):
    neighbour = Recipe(file=state.file, ingredients=state.ingredients.copy())
    neighbour.toggle_ingredient(random.choice(list(neighbour.ingredients.keys())))
    return neighbour

def next_temperature(temperature, annealing_rate):
    return temperature * annealing_rate

def accept_probability(old_fitness, new_fitness, temperature):
    return math.exp(-(old_fitness - new_fitness) / temperature)

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

if __name__ == "__main__":
    simulated_annealing("data/d_difficile.txt", temperature_init=10, annealing_rate=0.99, nb_iter=1000, output_file="d_difficile_20_99.txt")