import os
import random
from get_score import get_score
from get_ingredients import get_ingredients

class Recipe():
    def __init__(self, file, ingredients=None):
        self.file = file
        if not ingredients:
            all_ingredients = get_ingredients(file)
            self.ingredients = {ingredient: random.randint(0,1) for ingredient in all_ingredients}
        else:
            self.ingredients = ingredients
    
    def __str__(self):
        return str(self.ingredients)
    
    def toggle_ingredient(self, ingredient):
        self.ingredients[ingredient] = 1 - self.ingredients[ingredient]

    def get_ingredients(self):
        return [ingredient for ingredient in self.ingredients if self.ingredients[ingredient] == 1]
    
    def get_fitness(self):
        return get_score(self.file, self.get_ingredients())

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
    recipes.sort(key=lambda recipe: recipe.get_fitness(), reverse=True)
    return recipes[:size]

def genetic_algorithm(file, pop_size, mutation_rate, nb_gen=None, objective=None):
    if nb_gen is None and objective is None:
        raise ValueError("Either nb_gen or objective must be specified")
    if pop_size % 2 != 0:
        raise ValueError("Population size must be even")
    gen = first_generation(file, pop_size)
    count = 0
    while (nb_gen is None or count < nb_gen) and (objective is None or gen[0].get_fitness() < objective):
        with open(os.path.join("solutions", "genetic", file.split('/')[1]), "a") as f:
            f.write("Generation: " + str(count) + "\nBest score: " + str(gen[0].get_fitness()) + "\nBest recipe: " + str(gen[0].get_ingredients()) + "\n\n")
        gen = selection(gen, pop_size//2)
        for i in range(pop_size//4):
            child1, child2 = crossover(gen[i], gen[-i])
            mutation(child1, mutation_rate)
            mutation(child2, mutation_rate)
            gen.append(child1)
            gen.append(child2)
        count += 1
    return gen


if __name__ == "__main__":
    recipes = genetic_algorithm("data/d_difficile.txt", 100, 0.01, objective=1800)
    recipes.sort(key=lambda recipe: recipe.get_fitness(), reverse=True)
    print(recipes[0].get_ingredients())