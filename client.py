class Client():
    def __init__(self, liked, disliked):
        self.liked = liked
        self.disliked = disliked
    
    def get_liked(self):
        return self.liked
    
    def get_disliked(self):
        return self.disliked
    
    def does_like_pizza(self, ingredients):
        for l_ing in self.liked:
            if l_ing not in ingredients:
                return False
        for d_ing in self.disliked:
            if d_ing in ingredients:
                return False
        return True
    
if __name__ == '__main__':
    client = Client(['a', 'b', 'c'], ['f', 'e'])
    print(client.does_like_pizza(['a', 'b']))
    print(client.does_like_pizza(['a', 'b', 'c']))
    print(client.does_like_pizza(['a', 'b', 'c', 'd']))
    print(client.does_like_pizza(['a', 'b', 'c', 'd', 'e']))
    print(client.does_like_pizza(['a', 'b', 'c', 'e']))
    print(client.does_like_pizza(['a', 'b', 'c', 'f']))
        