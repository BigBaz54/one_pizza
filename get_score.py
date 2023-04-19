import pizza_parser

def get_score(path, solution):
    # get the score of a solution
    clients = pizza_parser.parse(path)
    score = 0
    for client in clients:
        if client.does_like_pizza(solution):
            score += 1
    return score