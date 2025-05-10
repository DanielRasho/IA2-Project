from enum import StrEnum
from typing import Tuple, List
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
    
    def get_scanned_tiles(self) -> int:
        return self.scanned_tiles

    def get_solution_path(self) -> List[int]:
        return self.solution_path
        
    def solve_tick(self) -> Tuple[MazeBoard, bool]:
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
        raise NotImplementedError("Subclasses should implement solve_tick()")