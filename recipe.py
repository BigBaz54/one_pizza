from get_ingredients import get_ingredients
from get_score import get_score
import random


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
    
    def get_score(self, clients=None):
        # creating the client instances every time takes is not efficient, but it's the cleanest way to do it
        # with generations of 100 recipes, it takes approx 10% of the total time
        return get_score(self.file, self.get_ingredients(), clients=clients)

    def copy(self):
        return Recipe(self.file, self.ingredients.copy())
     
    def __eq__(self, other):
        return self.ingredients == other.ingredients
    
if __name__ == "__main__":
    recipe = Recipe("data/b_basique.txt")
    recipe2 = recipe.copy()
    print(recipe==recipe2)