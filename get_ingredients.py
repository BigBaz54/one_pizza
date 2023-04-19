import pizza_parser

def get_ingredients(path):
    # get the ingredients from the pizza file
    clients = pizza_parser.parse(path)
    ingredients = set()
    for client in clients:
        for ingredient in client.liked:
            ingredients.add(ingredient)
        for ingredient in client.disliked:
            ingredients.add(ingredient)
    return list(ingredients)