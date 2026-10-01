from z3 import Bool, And, Or, Not, Implies

def create_variables(n):
    sudoku = {}

    for i in range(n):
        for j in range(n):
            for k in range(1, n + 1):
                sudoku[(i, j, k)] = Bool(f"sudoku_{i}_{j}_{k}")

    return sudoku


def add_constraints(s, sudoku, n):
    for row in range(n):
        for col in range(n):
            s.add(
                Or(
                    sudoku[(row, col, k)] for k in range(1, n + 1)
                )
            )

            for k in range(1, n + 1):
                s.add(
                    Implies(
                        sudoku[(row, col, k)],
                        Not(Or(
                            sudoku[(r, col, k)] for r in range(n) if r != row
                        ))
                    )
                )

                s.add(
                    Implies(
                        sudoku[(row, col, k)],
                        Not(Or(
                            sudoku[(row, c, k)] for c in range(n) if c != col
                        ))
                    )
                )

                box_size = 3

                box_row = (row // box_size) * box_size
                box_col = (col // box_size) * box_size

                s.add(
                    Implies(
                        sudoku[(row, col, k)],
                        Not(Or(
                            sudoku[(r, c, k)] 
                            for r in range(box_row, box_row + 3) 
                            for c in range(box_col, box_col + 3) 
                            if not(r == row and c == col)
                        ))
                    )
                )


