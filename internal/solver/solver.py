from ..maze.maze import MazeBoard


class Solver:
    def __init__(self, board: MazeBoard, start: int, goal: int):
        self.board = board
        # YOU ARE RESPONSABLE FOR UPDATING THIS VARIABLES:
        self.solution_path = []
        self.scanned_tiles = 0

    def get_scanned_tiles(self) -> int:
        return self.scanned_tiles

    def get_solution_path(self) -> list[int]:
        return self.solution_path

    def solve_tick(self) -> bool:
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
