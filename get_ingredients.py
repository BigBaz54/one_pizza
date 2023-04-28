import pizza_parser

def get_ingredients(path):
    # get the ingredients from the problem file
    clients = pizza_parser.parse(path)
    ingredients = set()
    for client in clients:
        for ingredient in client.liked:
            ingredients.add(ingredient)
        for ingredient in client.disliked:
            ingredients.add(ingredient)
    return list(ingredients)

def get_ingredients_sorted_best_to_worst(path):
    # ingredients are sorted by their score, which is explained in get_ingredient_score
    ingredients = get_ingredients(path)
    ingredients.sort(key=lambda x: get_ingredient_score(x, path), reverse=True)
    return ingredients

def get_ingredient_score(ingredient, path):
    # the score is increased by 1/n for every client that has the ingredient in their liked list of n ingredients
    # the score is decreased by 1 for every client that has the ingredient in their disliked list
    clients = pizza_parser.parse(path)
    score = 0
    for client in clients:
        if ingredient in client.liked:
            score += 1/len(client.liked)
        if ingredient in client.disliked:
            score -= 1
    return score

if __name__ == "__main__":
    print(get_ingredients_sorted_best_to_worst("data/d_difficile.txt"))