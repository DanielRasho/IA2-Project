from enum import StrEnum
from typing import Tuple
from ..maze.maze import MazeBoard

class SolverType(StrEnum):
    BFS = "BFS"
    DFS = "DFS"
    DIJIKSTRA = "Dijikstra"
    A_STAR = "A*"

class Solver:
    def __init__(self, board: MazeBoard, start : int, goal: int):
        self.board = board
        # YOU ARE RESPONSABLE FOR UPDATING THIS VARIABLES:
        self.solution_path = []
        self.scanned_tiles = 0
        
    """
    Performs a single step (tick) of the solving algorithm.

    During each tick, the solver attempts to move one step closer to the 
    solution. It returns the current state of the new board and a boolean 
    indicating if the goal has been reached.

    solution_path and scanned_tiles must be updated.

    Returns:
        Tuple[MazeBoard, bool]: A tuple containing:
            - MazeBoard: The current state of the maze after the tick.
            - bool: True if the goal is reached, otherwise False.
    """
    def solve_tick(self) -> Tuple[MazeBoard, bool]:
        raise NotImplementedError("Subclasses should implement solve_tick()")