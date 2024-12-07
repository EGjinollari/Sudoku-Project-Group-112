import pygame
from cell import Cell
from sudoku_generator import SudokuGenerator

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen

        # Determine the number of cells to remove based on difficulty
        difficulties = {"easy": 30, "medium": 40, "hard": 50}
        self.removed_cells = difficulties[difficulty]

        # Generate the board
        sudoku = SudokuGenerator(9, self.removed_cells)
        sudoku.fill_values()
        # Assigns self.solution to a copy of sudoku.get_board() because sudoku.get_board() is passed by reference
        self.solution = [[val for val in row] for row in sudoku.get_board()]
        sudoku.remove_cells()
        self.board = sudoku.get_board()


        # Create Cell objects
        self.cells = []
        for row in range(9):
            row_cells = []
            for col in range(9):
                row_cells += [Cell(self.board[row][col], row, col, screen)]

            self.cells += [row_cells]
        
        self.selected = None

    def draw(self):
        # Draw grid lines
        gap = self.width // 9
        thickness = 7
        for i in range(3, 9 + 1, 3):
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * gap), (self.width, i * gap), thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thickness)

        # Draw each cell
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected:
            prev_row, prev_col = self.selected
            self.cells[prev_row][prev_col].selected = False
        self.selected = (row, col)
        self.cells[row][col].selected = True

    def click(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            gap = self.width // 9
            row = y // gap
            col = x // gap
            return row, col

        return None

    def clear(self):
        if self.selected:
            row, col = self.selected
            cell = self.cells[row][col]
            if self.board[row][col] == 0:  # Only clear modifiable cells
                cell.set_cell_value(0)
                cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected:
            row, col = self.selected
            cell = self.cells[row][col]
            if cell.value == 0:  # Only sketch in modifiable cells
                cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected:
            row, col = self.selected
            cell = self.cells[row][col]
            if self.board[row][col] == 0:  # Only place in modifiable cells
                cell.set_cell_value(value)
                cell.set_sketched_value(0)

    def reset_to_original(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:  # Reset only modifiable cells
                    self.cells[row][col].set_cell_value(0)
                    self.cells[row][col].set_sketched_value(0)

    '''
        Determines if a board has had all values filled
    '''

    def is_full(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    print("Cell not full:", row, col)
                    return False
        
        return True

    def update_board(self):
        for row in range(9):
            for col in range(9):
                value = self.cells[row][col].value
                self.board[row][col] = value

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return row, col

        return None

    def check_board(self):
        # Verify the board matches the solution
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value != self.solution[row][col]:
                    return False
        return True
