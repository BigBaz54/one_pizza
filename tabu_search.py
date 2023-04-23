import math
import os

from matplotlib import pyplot as plt
from recipe import Recipe
import pizza_parser

class TabuList():
    def __init__(self, size):
        self.size = size
        self.list = []

    def add(self, item):
        if len(self.list) >= self.size:
            self.list.pop(0)
        self.list.append(item)

    def contains(self, item):
        return item in self.list
    
    def __str__(self):
        return str(self.list)
    
def first_state(file):
    return Recipe(file)

def get_neighbours(state):
    neighbours = []
    for ingredient in state.ingredients:
        neighbour = state.copy()
        neighbour.toggle_ingredient(ingredient)
        neighbours.append(neighbour)
    return neighbours

def tabu_search(file, tabu_size, objective=None, max_iterations=None, output_file=None, first_state=None):
    if objective is None and max_iterations is None:
        raise ValueError("Either max_iterations or objective must be specified")
    if output_file is None:
        output_file = file.split('/')[1]
    clients = pizza_parser.parse(file)
    if first_state is None:
        state = first_state(file)
    else:
        state = first_state
    tabu_list = TabuList(tabu_size)
    count = 0
    if not os.path.exists("solutions/tabu_search"):
        os.makedirs("solutions/tabu_search")
    best_state = state
    best_score = state.get_score(clients=clients)
    while (max_iterations is None or count < max_iterations) and (objective is None or best_score < objective):
        neighbours = get_neighbours(state)
        neighbours = [neighbour for neighbour in neighbours if not tabu_list.contains(neighbour)]
        if len(neighbours) == 0:
            raise Exception("No neighbours found")
        if len(neighbours) > 0:
            neighbours.sort(key=lambda x: x.get_score(clients=clients), reverse=True)
            state = neighbours[0]
            tabu_list.add(state)
            if state.get_score(clients=clients) > best_score:
                best_state = state
                best_score = state.get_score(clients=clients)
        if count % 10 == 0:
            with open(os.path.join("solutions", "tabu_search", output_file), "a") as f:
                f.write("Iteration: " + str(count) + "\nBest score: " + str(best_score) + "\nBest recipe: " + str(best_state.get_ingredients()) + "\n\n")
        count += 1
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
        with open(os.path.join("solutions", "tabu_search", files[i]), "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("Best score"):
                    scores.append(int(line.split(": ")[1]))
        axs[i%len_side, i//len_side].plot(range(0, len(scores)*10, 10), scores)
        axs[i%len_side, i//len_side].set_title(titles[i])
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    for ts in [1, 5, 10, 20, 50, 100, 200, 500, 1000]:
        tabu_search("data/d_difficile.txt", tabu_size=ts, objective=1800, max_iterations=1000, output_file=f"d_difficile_{ts}.txt")
