from ..maze.maze import MazeBoard
from ..solver.solver import Solver

class Game:
    def __init__(self, board: MazeBoard, solver: Solver):
        self.board = board
        self.solver = solver
        self.isFinished = False
        
    def tick(self):
        if self.isFinished == True:
            return self.board

        _, isFinished = self.solver.solve_tick(self.board)
        self.isFinished = isFinished
        return self.board