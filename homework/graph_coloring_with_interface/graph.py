class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = []
        self.positions = {}

    def add_vertex(self, vertex, x, y):
        self.vertices.add(vertex)
        self.positions[vertex] = (x, y)

    def add_edge(self, vertex1, vertex2):
        self.edges.append((vertex1, vertex2))

    def clear(self):
        self.vertices.clear()
        self.edges.clear()
        self.positions.clear()