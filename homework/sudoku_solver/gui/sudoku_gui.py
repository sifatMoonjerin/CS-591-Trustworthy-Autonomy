import tkinter as tk

from pyparsing import col

from sudoku.solver import solve_sudoku


class SudokuGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")
        # self.root.geometry("500x550")

        self.cells = []

        self.create_grid()

        solve_button = tk.Button(
            self.root,
            text="Solve",
            command=self.solve
        )
        solve_button.grid(row=9, column=0, columnspan=9)

    def create_grid(self):

        for row in range(9):

            row_cells = []

            for col in range(9):

                cell = tk.Entry(
                    self.root,
                    width=2,
                    justify="center",
                    font=("Arial", 25)
                )

                cell.grid(
                    row=row,
                    column=col
                )

                row_cells.append(cell)

            self.cells.append(row_cells)

    def solve(self):

        givens = []

        for row in range(9):
            for col in range(9):

                value = self.cells[row][col].get()

                if value:
                    givens.append(
                        (row, col, int(value))
                    )

        solution = solve_sudoku(givens)

        if solution is None:
            print("No solution")
            return

        for row in range(9):
            for col in range(9):

                self.cells[row][col].delete(0, "end")

                self.cells[row][col].insert(
                    0,
                    str(solution[row][col])
                )

                self.cells[row][col].config(fg="blue")

        for row, col, value in givens:
            self.cells[row][col].config(fg="red")

    def run(self):
        self.root.mainloop()