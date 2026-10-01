class Sudoku:
    def __init__(self, size=9):
        self.size = size
        self.grid = [
            [0 for _ in range(size)]
            for _ in range(size)
        ]

    def set_value(self, row, col, value):
        self.grid[row][col] = value

    def get_value(self, row, col):
        return self.grid[row][col]