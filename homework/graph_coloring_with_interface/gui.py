import tkinter as tk
from tkinter import messagebox

from graph import Graph
from solver import solve_graph


class GraphGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("4-Color Graph")
        self.root.geometry("600x400")

        # Graph data
        self.graph = Graph()

        # GUI settings
        self.vertex_radius = 20
        self.min_vertex_distance = 30
        self.next_vertex_id = 0
        self.selected_vertex = None
        self.vertex_items = {}

        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=600,
            height=350,
            bg="white"
        )
        self.canvas.pack()

        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.solve_button = tk.Button(
            self.button_frame,
            text="Color Graph",
            command=self.solve
        )

        self.solve_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(
            self.button_frame,
            text="Clear",
            command=self.clear_graph
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Mouse interaction
        self.canvas.bind("<Button-1>", self.canvas_click)

    def canvas_click(self, event):
        vertex = self.get_vertex_at(event.x, event.y)

        if vertex is None:
            self.create_vertex(event.x, event.y)
        else:
            self.select_vertex(vertex)

    def create_vertex(self, x, y):
        if self.is_position_occupied(x, y):
            return

        vertex = chr(ord("a") + self.next_vertex_id)

        self.next_vertex_id += 1

        self.graph.add_vertex(vertex, x, y)

        self.draw_vertex(vertex)

    def draw_vertex(self, vertex):
        x, y = self.graph.positions[vertex]
        r = self.vertex_radius

        circle = self.canvas.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill="lightgray",
            outline="black",
            width=2
        )

        self.canvas.create_text(
            x,
            y,
            text=vertex
        )

        self.vertex_items[vertex] = circle

    def get_vertex_at(self, x, y):
        for vertex, (vx, vy) in self.graph.positions.items():

            distance_squared = (x - vx) ** 2 + (y - vy) ** 2

            if distance_squared <= self.vertex_radius ** 2:
                return vertex

        return None

    def select_vertex(self, vertex):

        if self.selected_vertex is None:

            self.selected_vertex = vertex

            self.highlight_vertex(vertex)

        else:

            if vertex != self.selected_vertex:
                self.create_edge(
                    self.selected_vertex,
                    vertex
                )

            self.unhighlight_vertex(self.selected_vertex)

            self.selected_vertex = None

    def highlight_vertex(self, vertex):
        self.canvas.itemconfigure(
            self.vertex_items[vertex],
            outline="blue",
            width=3
        )

    def unhighlight_vertex(self, vertex):
        self.canvas.itemconfigure(
            self.vertex_items[vertex],
            outline="black",
            width=2
        )

    def create_edge(self, vertex1, vertex2):

        if (vertex1, vertex2) in self.graph.edges:
            return

        if (vertex2, vertex1) in self.graph.edges:
            return

        self.graph.add_edge(vertex1, vertex2)

        x1, y1 = self.graph.positions[vertex1]
        x2, y2 = self.graph.positions[vertex2]

        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="black",
            width=2
        )

        # Move the edge behind the vertices
        self.canvas.tag_lower(self.canvas.find_all()[-1])

    def is_position_occupied(self, x, y):
        for vx, vy in self.graph.positions.values():
            distance_squared = (x - vx) ** 2 + (y - vy) ** 2

            if distance_squared < self.min_vertex_distance ** 2:
                return True

        return False

    def color_vertex(self, vertex, color):
        color_map = {
            "r": "red",
            "g": "green",
            "b": "blue",
            "y": "yellow"
        }

        self.canvas.itemconfigure(
            self.vertex_items[vertex],
            fill=color_map[color]
        )

    def reset_vertex_colors(self):
        for vertex in self.graph.vertices:
            self.canvas.itemconfigure(
                self.vertex_items[vertex],
                fill="lightgray"
            )

    def solve(self):
        self.reset_vertex_colors()
        coloring = solve_graph(self.graph)

        if coloring is None:
            print("Graph is not 4-colorable.")

            messagebox.showinfo(
                "4-Coloring",
                "The graph is not four colorable."
            )

            return

        print("Graph is 4-colorable.")
        print(coloring)

        for vertex, color in coloring.items():
            self.color_vertex(vertex, color)

        # messagebox.showinfo(
        #     "4-Coloring",
        #     "The graph is four colorable!"
        # )

    def clear_graph(self):
        self.canvas.delete("all")

        self.graph.clear()

        self.next_vertex_id = 0
        self.selected_vertex = None

    def run(self):
        self.root.mainloop()