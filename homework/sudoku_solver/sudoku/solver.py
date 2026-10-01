from z3 import Solver, sat, is_true

from .constraints import create_variables, add_constraints


def solve_sudoku(givens, n=9):

    s = Solver()

    sudoku = create_variables(n)

    add_constraints(s, sudoku, n)

    # Add user-provided values
    for row, col, value in givens:
        s.add(sudoku[(row, col, value)])

    if s.check() != sat:
        return None

    model = s.model()

    solution = [
        [0 for _ in range(n)]
        for _ in range(n)
    ]

    for i in range(n):
        for j in range(n):
            for k in range(1, n + 1):

                if is_true(model.evaluate(sudoku[(i, j, k)])):
                    solution[i][j] = k

    return solution