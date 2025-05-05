from enum import IntEnum
from maze import MazeBoard

class GeneratorType(IntEnum):
    BACKTRACKING = 0
    PRIM = 1
	
class Generator:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width

    def generate(self):
        raise NotImplementedError("Subclasses should implement generate()")

    def generate_tick(self):
        raise NotImplementedError("Subclasses should implement generate_tick()")

class BacktrackingGenerator(Generator):
    def __init__(self, height: int, width: int):
        super().__init__(height, width)
        self.board = MazeBoard(height, width)

    def generate(self):
        # Do full maze generation
        return self.board

    def generate_tick(self):
        # Step-by-step logic
        return self.board
