import math
import os
import random

from matplotlib import pyplot as plt
from recipe import Recipe
import pizza_parser
from get_ingredients import get_ingredients, get_ingredients_with_score

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

def get_neighbourhood(state, size, ingredients_scores):
    # creating lists of potential ingredients to toggle and their score
    active_ingredients = []
    active_ingredients_scores = []
    inactive_ingredients = []
    inactive_ingredients_scores = []

    # the higher the score, the more likely an inactive ingredient will be added
    # the lower the score, the more likely an active ingredient will be removed
    for ingredient in state.ingredients.keys():
        score = ingredients_scores[ingredient]
        if state.ingredients[ingredient] == 1:
            active_ingredients.append(ingredient)
            if score <= 0:
                score = -score + 1
            else:
                score = 1/score
            active_ingredients_scores.append(score)
        else:
            inactive_ingredients.append(ingredient)
            if score >= 0:
                score = score + 1
            else:
                score = -1/score
            inactive_ingredients_scores.append(score)

    # selecting randomly the number of ingredients to be added and removed
    add_nb = random.randint(1, min(size, len(inactive_ingredients)))
    remove_nb = size - add_nb

    # selecting the ingredients to add and remove randomly but weighted by their score
    to_be_added = set()
    to_be_removed = set()
    while len(to_be_added) < add_nb:
        to_be_added.add(random.choices(inactive_ingredients, weights=inactive_ingredients_scores, k=1)[0])
    while len(to_be_removed) < remove_nb:
        to_be_removed.add(random.choices(active_ingredients, weights=active_ingredients_scores, k=1)[0])

    # generating neighbourhood
    neighbours = []
    for ingredient_to_remove in list(to_be_removed):
        neighbour = state.copy()
        neighbour.ingredients[ingredient_to_remove] = 0
        neighbours.append(neighbour)
    for ingredient_to_add in list(to_be_added):
        neighbour = state.copy()
        neighbour.ingredients[ingredient_to_add] = 1
        neighbours.append(neighbour)
    return neighbours

def tabu_search(file, tabu_size, objective=None, max_iterations=None, neighbourhood_size=None, output_file=None, init_state=None):
    if neighbourhood_size is None:
        neighbourhood_size = len(get_ingredients(file))
    if objective is None and max_iterations is None:
        raise ValueError("Either max_iterations or objective must be specified")
    if output_file is None:
        output_file = file.split('/')[1]
    clients = pizza_parser.parse(file)
    if init_state is None:
        state = first_state(file)
    else:
        state = init_state
    tabu_list = TabuList(tabu_size)
    count = 0
    if not os.path.exists("solutions/tabu_search"):
        os.makedirs("solutions/tabu_search")
    ingredients_with_scores = get_ingredients_with_score(file)
    ingredients_scores = {ingredient: score for ingredient, score in ingredients_with_scores}
    best_state = state
    best_score = state.get_score(clients=clients)
    while (max_iterations is None or count < max_iterations) and (objective is None or best_score < objective):
        neighbours = get_neighbourhood(state, neighbourhood_size, ingredients_scores)
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
    # for ts in [1, 10, 50, 200, 500]:
    #     for ns in [5, 20, 50]:
    #         tabu_search("data/d_difficile.txt", tabu_size=ts, objective=1800, max_iterations=500, neighbourhood_size=ns, output_file=f"d_difficile_{ts}_{ns}.txt")

    plot_results([f"d_difficile_{ts}_{ns}.txt" for ts in [1, 10, 50, 200, 500] for ns in [5, 20, 50]], titles=[f"tabu_size={ts}, neighbourhood_size={ns}" for ts in [1, 10, 50, 200, 500] for ns in [5, 20, 50]])
