# Write your code here
import numpy as np


class Tetris:
    def __init__(self, rows=20, cols=10):
        self.letter_dict = {}
        self.rows = rows
        self.cols = cols
        self.grid = self.make_grid(rows, cols)
        self.make_letter_dict()
        self.letter = None
        self.rotation = None
        self.letter_vals = None
        self.base = 10

    def make_letter_dict(self):
        self.letter_dict["I"] = [[4, 14, 24, 34], [3, 4, 5, 6]]
        self.letter_dict["J"] = [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]
        self.letter_dict["L"] = [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]
        self.letter_dict["O"] = [[4, 14, 15, 5]]
        self.letter_dict["S"] = [[5, 4, 14, 13], [4, 14, 15, 25]]
        self.letter_dict["T"] = [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]
        self.letter_dict["Z"] = [[4, 5, 15, 16], [5, 15, 14, 24]]

    def start(self, letter):
        if letter in self.letter_dict:
            self.letter = letter
            self.rotation = 0
            self.adjust_letter()
            self.base = self.cols
            self.display_grid()
            self.display_letter()

            while True:
                command = input()
                if command == "rotate":
                    self.down()
                    self.rotate()
                if command == "right":
                    self.down()
                    self.right()
                if command == "left":
                    self.down()
                    self.left()
                if command == "down":
                    self.down()
                if command == "exit":
                    break
                self.display_letter()


    def make_grid(self, rows, cols):
        return np.array([["-"] * cols] * rows)

    def display(self, grid):
        print("\n".join(" ".join(x) for x in grid), end="\n\n")

    def display_grid(self):
        self.display(self.grid)

    def display_letter(self):
        self.display(self.add_letter(self.grid.copy(), self.letter_vals[self.rotation]))

    def add_letter(self, grid, arr):
        for point in arr:
            grid[(point // self.cols) % self.rows, point % self.cols] = "0"
        return grid

    def adjust_letter(self):
        self.letter_vals = [[((x // self.base) * self.cols) + ((x % self.base) % self.cols) for x in pos]
                            for pos in self.letter_dict[self.letter]]

    def rotate(self):
        self.rotation += 1
        self.rotation = self.rotation % len(self.letter_vals)

    def right(self):
        self.letter_vals = [[((x // self.base) * self.cols) + (((x + 1) % self.base) % self.cols) for x in pos]
                            for pos in self.letter_vals]

    def left(self):
        self.letter_vals = [[((x // self.base) * self.cols) + (((x - 1 + self.base) % self.base) % self.cols) for x in pos]
                            for pos in self.letter_vals]

    def down(self):
        self.letter_vals = [[(((x + self.base) // self.base) * self.cols) + ((x % self.base) % self.cols) for x in pos]
                            for pos in self.letter_vals]


def start_game():
    letter = input()
    dimensions = input()
    ncols, nrows = (int(x) for x in dimensions.split())
    myTetris = Tetris(nrows, ncols)
    myTetris.start(letter)

start_game()




