# Write your code here
import numpy as np

letter_dict = dict()
letter_dict["I"] = [[4, 14, 24, 34], [3, 4, 5, 6]]
letter_dict["J"] = [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]
letter_dict["L"] = [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]
letter_dict["O"] = [[4, 14, 15, 5]]
letter_dict["S"] = [[5, 4, 14, 13], [4, 14, 15, 25]]
letter_dict["T"] = [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]
letter_dict["Z"] = [[4, 5, 15, 16], [5, 15, 14, 24]]

class Piece:
    def __init__(self, letter):
        self.letter = letter
        self.values = letter_dict[letter]
        self.num_values = len(self.values)
        self.rotation = 0
        self.atleft = False
        self.atright = False
        self.atbottom = False

    def adjust_letter(self, base, ncols):
        self.values = [[((x // base) * ncols) + ((x % base) % ncols) for x in pos] for pos in self.values]

    def rotate(self):
        if not self.atbottom:
            self.rotation += 1
            self.rotation = self.rotation % self.num_values

    def get_value(self):
        return self.values[self.rotation]

    def down(self, grid):
        if not self.atbottom:
            self.values = [[(((x + grid.cols) // grid.cols) * grid.cols) + ((x % grid.cols) % grid.cols) for x in pos]
                                for pos in self.values]
            # Check if at bottom
            if any((x // grid.cols) + 1 == grid.rows for x in self.get_value()):
                self.atbottom = True
                self.atright = True
                self.atleft = True

    def right(self, grid):
        if not self.atright:
            self.values = [[((x // grid.cols) * grid.cols) + (((x + 1) % grid.cols) % grid.cols) for x in pos] for pos in self.values]
            # Check if at right
            self.atright = any((x % grid.cols) + 1 == grid.cols for x in self.get_value())
            self.atleft = False

    def left(self, grid):
        if not self.atleft:
            self.values = [[((x // grid.cols) * grid.cols) + (((x - 1 + grid.cols) % grid.cols) % grid.cols) for x in pos] for pos in self.values]
            # Check if at left
            self.atleft = any(x % grid.cols == 0 for x in self.get_value())
            self.atright = False


class Grid:
    def __init__(self, nrows, ncols):
        self.rows = nrows
        self.cols = ncols
        self.values = np.array([["-"] * ncols] * nrows)

    def add_letter(self, letter):
        for point in letter.get_value():
            self.values[(point // self.cols) % self.rows, point % self.cols] = "0"

    def print(self):
        print("\n".join(" ".join(x) for x in self.values), end="\n\n")

class Tetris:
    def __init__(self, grid, piece):
        self.rows = grid.rows
        self.cols = grid.cols
        self.grid = grid
        self.piece = piece

    def start(self):
        self.grid.print()
        self.grid.add_letter(self.piece)
        self.grid.print()

        while True:
            command = input()

            if command == "rotate":
                self.piece.rotate()
            if command == "right":
                self.piece.right(self.grid)
            if command == "left":
                self.piece.left(self.grid)
            if command == "down":
                pass
            if command == "exit":
                break

            self.piece.down(self.grid)
            self.grid = Grid(self.rows, self.cols)
            self.grid.add_letter(self.piece)
            self.grid.print()


def start_game():
    letter = input()
    if letter in letter_dict:
        piece = Piece(letter)
    else:
        piece = Piece("O")

    dimensions = input()
    ncols, nrows = (int(x) for x in dimensions.split())

    piece.adjust_letter(10, ncols)

    grid = Grid(nrows, ncols)

    myTetris = Tetris(grid, piece)
    myTetris.start()


start_game()




