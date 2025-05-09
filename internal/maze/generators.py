from enum import IntEnum
from typing import Tuple
from maze import MazeBoard

class GeneratorType(IntEnum):
    BACKTRACKING = 0
    PRIM = 1
	
class Generator:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width

    def generate(self) -> MazeBoard :
        raise NotImplementedError("Subclasses should implement generate()")

    def generate_tick(self) -> MazeBoard:
        raise NotImplementedError("Subclasses should implement generate_tick()")

class BacktrackingGenerator(Generator):
    def __init__(self, height: int, width: int):
        super().__init__(height, width)
        self.board = MazeBoard(height, width)

    def generate(self) -> MazeBoard:
        # Do full maze generation
        return self.board

    def generate_tick(self) -> Tuple[MazeBoard, bool]:
        # Step-by-step logic
        return self.board, False

class BacktrackingGenerator(Generator):
    def __init__(self, height: int, width: int):
        super().__init__(height, width)
        self.board = MazeBoard(height, width)

    def generate(self) -> MazeBoard:
        # Do full maze generation
        return self.board

    def generate_tick(self) -> Tuple[MazeBoard, bool]:
        # Step-by-step logic
        return self.board, False
