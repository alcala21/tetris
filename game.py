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

    def right(self, grid):
        if not self.atright:
            self.values = [[((x // grid.cols) * grid.cols) + (((x + 1) % grid.cols) % grid.cols) for x in pos] for pos in self.values]
            if not self.atbottom:
                self.atleft = False

    def left(self, grid):
        if not self.atleft:
            self.values = [[((x // grid.cols) * grid.cols) + (((x - 1 + grid.cols) % grid.cols) % grid.cols) for x in pos] for pos in self.values]
            if not self.atbottom:
                self.atright = False

    def check_edges(self, grid):
        # Check if at bottom
        if not self.atbottom and any((x // grid.cols) + 1 >= grid.bottom[x % grid.cols] for x in self.get_value()):
            self.atbottom = True
            self.atright = True
            self.atleft = True

        # Check if at right
        if not self.atright and any((x % grid.cols) + 1 == grid.cols for x in self.get_value()):
            self.atright = True
            self.atleft = False

        # Check if at left
        if not self.atleft and any(x % grid.cols == 0 for x in self.get_value()):
            self.atleft = True
            self.atright = False


class Grid:
    def __init__(self, values):
        self.values = values
        self.rows = len(values)
        self.cols = len(values[0])
        self.bottom = np.sum(values == "-", axis=0)
        self.set_bottom()

    def add_letter(self, letter):
        for point in letter.get_value():
            self.values[(point // self.cols) % self.rows, point % self.cols] = "0"

    def print(self):
        print("\n".join(" ".join(x) for x in self.values), end="\n\n")

    def set_bottom(self):
        self.bottom = np.sum(self.values == "-", axis=0)

    def check_lines(self):
        available = np.where(np.sum(self.values == '0', axis=1) < self.cols)[0]

    def remove_lines(self):
        available = np.where(np.sum(self.values == '0', axis=1) < self.cols)[0]
        nfull = self.rows - len(available)
        self.values[nfull:, :] = self.values[available, :]
        self.values[:nfull, :] = np.full((nfull, self.cols), "-")


class Tetris:
    def __init__(self, grid):
        self.rows = grid.rows
        self.cols = grid.cols
        self.grid = grid
        self.piece = None

    def choose_piece(self):
        letter = input()
        if letter in letter_dict:
            self.piece = Piece(letter)
        else:
            self.piece = Piece("O")
        self.piece.adjust_letter(10, self.cols)

    def start(self):
        temp_grid = Grid(self.grid.values.copy())
        temp_grid.print()

        while True:
            command = input()
            if command == "exit":
                break
            elif command == "piece":
                if not self.piece:
                    self.choose_piece()
            elif command == "break":
                self.grid.remove_lines()

            if self.piece:
                if command == "rotate":
                    self.piece.rotate()
                    self.piece.down(self.grid)
                elif command == "right":
                    self.piece.right(self.grid)
                    self.piece.down(self.grid)
                elif command == "left":
                    self.piece.left(self.grid)
                    self.piece.down(self.grid)
                elif command == "down":
                    self.piece.down(self.grid)

                self.piece.check_edges(self.grid)
                temp_grid = Grid(self.grid.values.copy())
                temp_grid.add_letter(self.piece)
                temp_grid.print()

                if self.piece.atbottom:
                    self.grid = Grid(temp_grid.values.copy())
                    self.piece = None
            else:
                self.grid.set_bottom()
                self.grid.print()
                if self.is_game_over():
                    print("Game Over!")
                    break

    def is_game_over(self):
        return any(self.grid.bottom == 0)


ncols, nrows = (int(x) for x in input().split())
grid = Grid(np.full((nrows, ncols), "-"))
Tetris(grid).start()
