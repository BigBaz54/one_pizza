from client import Client

def parse(path):
    clients = []
    with open(path, 'r') as f:
        lines = f.readlines()
        clients_nb = int(lines[0])
        lines = lines[1:]
        for i in range(clients_nb):
            liked = lines[2*i].strip().split(' ')[1:]
            disliked = lines[2*i+1].strip().split(' ')[1:]
            clients.append(Client(liked, disliked))
    return clients


if __name__ == '__main__':
    print(len(parse('data/a_exemple.txt')))
    for e in parse('data/a_exemple.txt'):
        print(e)
    print(len(parse('data/b_basique.txt')))
    for e in parse('data/b_basique.txt'):
        print(e)
        