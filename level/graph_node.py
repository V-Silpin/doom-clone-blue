class Graph:
    def __init__(self, x, y):
        self.value = (x, y)
        self.neighbor = []
    def push(self, x, y):
        self.neighbor.append((x, y))