from enum import IntEnum
from typing import Tuple
import random


class CellMark(IntEnum):
    EMPTY = 0
    WALL = 1
    PATH = 2  # For the solver to mark the path
    SCANNED = 3  # For the solver to mark scanned cells during search

    # States the solvers can use
    START = 4
    END = 5


class MazeBoard:
    """
    Representation of a maze. The maze is stored as a 1D array of CellMark.
    It provides utility methods to treat it as a 2D matrix.
    """

    def __init__(self, height: int, width: int, fill: CellMark = CellMark.EMPTY):
        self.height = height
        self.width = width
        self.cells = [fill] * (height * width)

    def get_cell(self, row: int, col: int) -> CellMark:
        if not self._valid_coords(row, col):
            raise IndexError("Coordinates out of bounds")
        return self.cells[self._index(row, col)]

    def set_cell(self, row: int, col: int, value: CellMark):
        if not self._valid_coords(row, col):
            raise IndexError(
                "Coordinates out of bounds", (self.width, self.height), (row, col)
            )
        self.cells[self._index(row, col)] = value

    def cell_as_coordinates(self, index: int) -> Tuple[int, int]:
        """Returns 2D coordinates given a cell index"""
        row = index // self.width
        col = index - row * self.width
        return (row, col)

    def set_start_and_end(self, start: tuple[int, int], end: tuple[int, int]):
        self.start = start
        self.set_cell(start[0], start[1], CellMark.START)

        self.end = end
        self.set_cell(end[0], end[1], CellMark.END)

    def set_distance(self, distance: int):
        self.distance = distance

    def _index(self, row: int, col: int) -> int:
        return row * self.width + col

    def _valid_coords(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def __str__(self):
        result = ""
        for r in range(self.height):
            for c in range(self.width):
                cell = self.get_cell(r, c)
                if cell == CellMark.EMPTY:
                    result += " "
                elif cell == CellMark.WALL:
                    result += "#"
                elif cell == CellMark.PATH:
                    result += "o"
                elif cell == CellMark.SCANNED:
                    result += "x"
                elif cell == CellMark.START:
                    result += "+"
                elif cell == CellMark.END:
                    result += "*"
            result += "\n"
        return result


def get_random_start_goal(maze: MazeBoard, min_distance: int):
    """
    Select 2 random EMPTY cells from a mazeboard with a list a minimum manhattan distance.
    The start and end of the MazeBoard are set in place!
    """

    empty_cells = [
        maze.cell_as_coordinates(i)
        for i, cell in enumerate(maze.cells)
        if cell == CellMark.EMPTY
    ]

    # Pick a random starting cell
    first_cell = random.choice(empty_cells)

    # Shuffle and find the first one that matches the distance
    random.shuffle(empty_cells)
    for cell in empty_cells:
        distance = abs(first_cell[0] - cell[0]) + abs(first_cell[1] - cell[1])
        if distance >= min_distance:
            print("Setting start and end", first_cell, cell)
            maze.set_start_and_end(first_cell, cell)
            maze.set_distance(distance)
            return

    raise ValueError("No valid second cell found with the required distance.")
