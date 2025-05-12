from enum import StrEnum
from typing import Tuple, List, Set, Dict, Deque
from collections import deque
from ..maze.maze import MazeBoard, CellMark
from .solver import Solver


class BFS(Solver):

    def __init__(self, board: MazeBoard, start: Tuple[int, int], goal: Tuple[int, int]):
        super().__init__(board, start, goal)
        self.board = board
        self.start = start
        self.goal = goal

        self.queue = deque([start])
        self.visited = {start}
        self.parent = {start: None}

        self.scanned_tiles = 0
        self.solution_path = []
        self.found_goal = False
        self.reconstructed_path = False

    def get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring cells (up, down, left, right)."""
        row, col = position
        neighbors = []

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = row + dr, col + dc

            if (
                0 <= new_row < self.board.height
                and 0 <= new_col < self.board.width
                and self.board.get_cell(new_row, new_col) != CellMark.WALL
            ):
                neighbors.append((new_row, new_col))

        return neighbors

    def solve_tick(self) -> bool:
        """Perform one step of BFS algorithm."""
        if self.reconstructed_path:
            return False

        if self.found_goal:
            self._reconstruct_path()
            self.reconstructed_path = True
            return False

        if not self.queue:
            print("No path found to the goal!")
            return False

        current = self.queue.popleft()

        if current == self.goal:
            self.found_goal = True
            return True

        for neighbor in self.get_neighbors(current):
            if neighbor not in self.visited:
                self.visited.add(neighbor)
                self.scanned_tiles += 1

                self.queue.append(neighbor)

                self.parent[neighbor] = current

                row, col = neighbor
                if neighbor != self.start and neighbor != self.goal:
                    self.board.set_cell(row, col, CellMark.SCANNED)

        return True

    def _reconstruct_path(self):
        """Reconstruct the path from start to goal using the parent dictionary."""
        current = self.goal
        path = []

        while current != self.start:
            path.append(current)
            current = self.parent[current]

        path.append(self.start)
        path.reverse()

        self.solution_path = path

        # Mark the path on the board
        for position in path:
            row, col = position
            if position != self.start and position != self.goal:
                self.board.set_cell(row, col, CellMark.PATH)

        print(f"Camino encontrad! Longitud: {len(path)}")
        print(f"Nodos escaneados: {self.scanned_tiles}")
