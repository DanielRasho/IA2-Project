from .BFS import BFS
from .DFS import DFS
from .Dijikstra import Dijikstra
from .A_Star import A_Star
from enum import StrEnum
from ..maze.maze import MazeBoard


class SolverType(StrEnum):
    BFS = "BFS"
    DFS = "DFS"
    DIJIKSTRA = "Dijikstra"
    A_STAR = "A*"


def SolverFromType(sType: SolverType, board: MazeBoard, start: int, goal: int):
    if sType == SolverType.BFS:
        return BFS(board, start, goal)
    elif sType == SolverType.DFS:
        return DFS(board, start, goal)
    elif sType == SolverType.DIJIKSTRA:
        return Dijikstra(board, start, goal)
    elif sType == SolverType.A_STAR:
        return A_Star(board, start, goal)
