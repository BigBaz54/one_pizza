from recipe import Recipe
from get_ingredients import get_ingredients
import pizza_parser


def greedy(file):
    clients = pizza_parser.parse(file)
    recipe = Recipe(file)
    all_ingredients = get_ingredients(file)
    for ingredient in recipe.get_ingredients():
        recipe.toggle_ingredient(ingredient)
    best_ingredient_score = 1
    while best_ingredient_score > 0:
        not_used_ingredients = [ingredient for ingredient in all_ingredients if ingredient not in recipe.get_ingredients()]
        ingredients_scores = []
        for ingredient in not_used_ingredients:
            base_score = recipe.get_score(clients)
            recipe.toggle_ingredient(ingredient)
            ingredient_score = recipe.get_score(clients) - base_score
            ingredients_scores.append((ingredient, ingredient_score))
            recipe.toggle_ingredient(ingredient)
        best_ingredient = max(ingredients_scores, key=lambda x: x[1])
        print(best_ingredient)
        best_ingredient_score = best_ingredient[1]
        if best_ingredient_score > 0:
            recipe.toggle_ingredient(best_ingredient[0])
    return recipe

if __name__ == '__main__':
    r = greedy('data/d_difficile.txt')
    # takes hours
    # print("Best score:", r.get_score())


