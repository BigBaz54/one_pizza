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