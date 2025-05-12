from enum import StrEnum
from typing import Tuple
from ..maze.maze import MazeBoard
from .solver import Solver


class A_Star(Solver):

    def __init__(self, board: MazeBoard, start: int, goal: int):
        super().__init__(board, start, goal)

    def solve_tick(self) -> bool:
        # modify the maze internally
        # Do path finding and whatever

        # Yield a conclusion
        print("Finished to solve (Actually i didn't do anyting)")
        return False
