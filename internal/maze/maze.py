from enum import IntEnum
from typing import Tuple
import random

class CellMark(IntEnum):
    EMPTY = 0
    WALL = 1
    PATH = 2  # For the solver to mark the path
    SCANNED = 3  # For the solver to mark scanned cells during search
    
class MazeBoard:
    '''
        Representation of a maze. The maze is stored as a 1D array of CellMark.
        It provides utility methods to treat it as a 2D matrix.
    '''
    def __init__(self, height: int, width: int, fill : CellMark = CellMark.EMPTY):
        self.height = height
        self.width = width
        self.cells = [fill] * (height * width)

    def get_cell(self, row: int, col: int) -> CellMark:
        if not self._valid_coords(row, col):
            raise IndexError("Coordinates out of bounds")
        return self.cells[self._index(row, col)]

    def set_cell(self, row: int, col: int, value: CellMark):
        if not self._valid_coords(row, col):
            raise IndexError("Coordinates out of bounds")
        self.cells[self._index(row, col)] = value

    def cell_as_coordinates(self, index:int) -> Tuple[int, int]:
        '''Returns 2D coordinates given a cell index'''
        return ( index % self.width ,index // self.width)

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
            result += "\n"
        return result

def get_random_start_goal(maze: MazeBoard, min_distance: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    '''
        Select 2 random EMPTY cells from a mazeboard with a list a minimum manhattan distance.
    '''
    
    empty_cells = [ maze.cell_as_coordinates(i)
                   for i, cell in enumerate(maze.cells) if cell == CellMark.EMPTY]
    
    # Pick a random starting cell
    first_cell = random.choice(empty_cells)
    
    # Shuffle and find the first one that matches the distance
    random.shuffle(empty_cells)
    for cell in empty_cells:
        if abs(first_cell[0] - cell[0]) + abs(first_cell[1] - cell[1]) >= min_distance:
            return first_cell, cell
    
    raise ValueError("No valid second cell found with the required distance.")