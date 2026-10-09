from z3 import Bool, And, Or, Not, Solver, is_true, sat

def solve_graph(graph, colors = None):
    if colors is None:
        colors = ['r', 'g', 'b', 'y']  # Default colors

    s = Solver()

    # Define boolean variables for each vertex and color

    vertex_color_variables = {}
    vertices = graph.vertices
    edges = graph.edges

    for v in vertices:
        for c in colors:
            vertex_color_variables[(v, c)] = Bool(f"V_{v}_{c}")

    # s.add(vertex_color_variables[('a', 'r')])  # Fix the color of the first vertex to 'r'
    # s.add(vertex_color_variables[('a', 'g')])  # Fix the color of the first vertex to 'g'

    for v in vertices:
        s.add(
            Or(
                *(vertex_color_variables[(v, c)] for c in colors)
            )
        ) # Each vertex has at least one color


        s.add(
            And(
                *(
                    Or(
                        Not(vertex_color_variables[(v, c1)]), 
                        Not(vertex_color_variables[(v, c2)])
                    ) 
                    for i, c1 in enumerate(colors) 
                    for j, c2 in enumerate(colors) 
                    if i < j
                )
            )
        ) # Each vertex has only one color


    for u, v in edges:
        s.add(
            And(
                *(
                    Or(
                        Not(vertex_color_variables[(u, c)]), 
                        Not(vertex_color_variables[(v, c)])
                    ) for c in colors
                )
            )
        ) # connected nodes do not have the same color


    if s.check() == sat:
        model = s.model()
        print("Solution found:")
        print(s.model())
        return {
            v: c for v in graph.vertices 
            for c in colors 
            if is_true(model.evaluate(vertex_color_variables[(v, c)]))
        }
    else:
        return None