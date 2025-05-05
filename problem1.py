import tkinter as tk
from enum import IntEnum
import time
from internal.maze.maze import MazeBoard

class CellMark(IntEnum):
    EMPTY = 0
    WALL = 1
    PATH = 2

class MazeBoard:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.cells = [CellMark.EMPTY] * (height * width)

    def _index(self, row: int, col: int) -> int:
        return row * self.width + col

    def get_cell(self, row: int, col: int) -> CellMark:
        return self.cells[self._index(row, col)]

    def set_cell(self, row: int, col: int, value: CellMark):
        self.cells[self._index(row, col)] = value

class FakeStepGenerator:
    """
    Dummy step generator that adds a WALL on each call, left to right, top to bottom.
    """
    def __init__(self, board: MazeBoard):
        self.board = board
        self.next_row = 0
        self.next_col = 0

    def generate_tick(self) -> MazeBoard:
        if self.next_row < self.board.height:
            self.board.set_cell(self.next_row, self.next_col, CellMark.WALL)
            self.next_col += 1
            if self.next_col >= self.board.width:
                self.next_col = 0
                self.next_row += 1
        return self.board

class MazeUI:
    CELL_SIZE = 30
    DELAY = 200  # milliseconds

    def __init__(self, root, maze: MazeBoard, generator):
        self.root = root
        self.maze = maze
        self.generator = generator

        self.canvas = tk.Canvas(root, width=maze.width * self.CELL_SIZE,
                                      height=maze.height * self.CELL_SIZE)
        self.canvas.pack()
        self.rects = [[None for _ in range(maze.width)] for _ in range(maze.height)]
        self.draw_maze()
        self.animate()

    def draw_maze(self):
        for r in range(self.maze.height):
            for c in range(self.maze.width):
                x0 = c * self.CELL_SIZE
                y0 = r * self.CELL_SIZE
                x1 = x0 + self.CELL_SIZE
                y1 = y0 + self.CELL_SIZE

                cell = self.maze.get_cell(r, c)
                color = {
                    CellMark.EMPTY: "white",
                    CellMark.WALL: "black",
                    CellMark.PATH: "green"
                }[cell]

                if self.rects[r][c] is None:
                    self.rects[r][c] = self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill=color, outline="gray"
                    )
                else:
                    self.canvas.itemconfig(self.rects[r][c], fill=color)

    def animate(self):
        self.generator.generate_tick()
        self.draw_maze()
        self.root.after(self.DELAY, self.animate)

# ---------- MAIN ----------
if __name__ == "__main__":
    maze = MazeBoard(10, 10)
    generator = FakeStepGenerator(maze)

    root = tk.Tk()
    root.title("Maze Generator Animation")
    app = MazeUI(root, maze, generator)
    root.mainloop()