import pizza_parser


def generate_all_subsets(ingredients):
    # generate all subsets of the list of ingredients (all ingredients must be distinct)
    if len(ingredients) == 1:
        return [ingredients, []]
    else:
        subsets = generate_all_subsets(ingredients[1:])
        new_subsets = []
        for subset in subsets:
            new_subsets.append(subset + [ingredients[0]])
            new_subsets.append(subset)
        return new_subsets

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

def get_all_solutions(path):
    # get all possible combinations of ingredients
    ingredients = get_ingredients(path)
    solutions = generate_all_subsets(ingredients)
    return solutions

def get_score(path, solution):
    # get the score of a solution
    clients = pizza_parser.parse(path)
    score = 0
    for client in clients:
        if client.does_like_pizza(solution):
            score += 1
    return score

def get_best_solution(path):
    # get the best solution
    solutions = get_all_solutions(path)
    best_score = 0
    best_solution = []
    for solution in solutions:
        score = get_score(path, solution)
        if score > best_score:
            best_score = score
            best_solution = solution
    return best_solution, best_score

if __name__ == '__main__':
    print(get_ingredients('data/a_exemple.txt'))
    print(len(get_all_solutions('data/a_exemple.txt')))
    print("Best solution: ", get_best_solution('data/a_exemple.txt')[0], "score", get_best_solution('data/a_exemple.txt')[1])
    print("Best solution: ", get_best_solution('data/b_basique.txt')[0], "score", get_best_solution('data/b_basique.txt')[1])
    print("Best solution: ", get_best_solution('data/c_grossier.txt')[0], "score", get_best_solution('data/c_grossier.txt')[1])