from enum import StrEnum
from typing import Tuple
from ..maze.maze import MazeBoard
from .solver import Solver

class Dijikstra(Solver):
    def __init__(self, board: MazeBoard, start : int, goal: int):
        self.board = board
        self.start = start
        self.goal = goal
        # YOU ARE RESPONSABLE FOR UPDATING THIS VARIABLES:
        self.solution_path = []
        self.scanned_tiles = 0
        
    # Return True if the maze has not be solved
    # False either
    def solve_tick(self) -> bool:
        # modify the maze internally
        # Do path finding and whatever
        
        # Yield a conclusion
        print("Finished to solve (Actually i didn't do anyting)")
        return False