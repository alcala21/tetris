# Write your code here
import numpy as np


class Tetris:
    def __init__(self):
        self.letters = {}
        self.grid = self.make_grid()
        self.get_letters()

    def get_letters(self):
        self.letters["I"] = [[1, 5, 9, 13], [4, 5, 6, 7], [1, 5, 9, 13], [4, 5, 6, 7]]
        self.letters["J"] = [[2, 6, 9, 10], [4, 5, 6, 10], [1, 2, 5, 9], [0, 4, 5, 6]]
        self.letters["L"] = [[1, 5, 9, 10], [6, 8, 9, 10], [5, 6, 10, 14], [4, 5, 6, 8]]
        self.letters["O"] = [[5, 6, 9, 10], [5, 6, 9, 10], [5, 6, 9, 10], [5, 6, 9, 10]]
        self.letters["S"] = [[6, 5, 9, 8], [5, 9, 10, 14], [6, 5, 9, 8], [5, 9, 10, 14]]
        self.letters["T"] = [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]]
        self.letters["Z"] = [[4, 5, 9, 10], [2, 5, 6, 9], [4, 5, 9, 10], [2, 5, 6, 9]]

    def start(self):
        letter = input()
        if letter in self.letters:
            self.display(self.grid)

            letter_array = self.letters[letter]
            self.display(self.add_letter(self.grid.copy(), letter_array[0]))

            for i in range(1, 5):
                letter_points = letter_array[i % 4]
                self.display(self.add_letter(self.grid.copy(), letter_points))

    def make_grid(self):
        return np.array([["-"]*4] * 4)

    def display(self, grid):
        print("\n".join(" ".join(x) for x in grid), end="\n\n")

    def add_letter(self, grid, arr):
        for point in arr:
            grid[point // 4, point % 4] = "0"
        return grid


Tetris().start()

