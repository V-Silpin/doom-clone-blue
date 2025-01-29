class Graph:
    def __init__(self, value):
        self.value = value
        self.neighbor = []
    def push(self, node):
        self.neighbor.append(node)