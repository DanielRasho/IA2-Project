from enum import StrEnum
from typing import Tuple
from ..maze.maze import MazeBoard, CellMark
from .solver import Solver


class DFS(Solver):

    def __init__(self, board: MazeBoard, start: int, goal: int):
        super().__init__(board, start, goal)
        # Initialize stack for DFS
        self.stack = []

        # Convert 1D indices to 2D coordinates
        start_coords = self.board.cell_as_coordinates(start)
        goal_coords = self.board.cell_as_coordinates(goal)

        # Add start position to the stack
        self.stack.append(start_coords)

        # Track visited cells to avoid cycles
        self.visited = set()
        self.visited.add(start)

        # For path reconstruction
        self.came_from = {}

        # Flag to indicate if we've reached the goal
        self.goal_reached = False

        # Flag to indicate if we're in backtracking mode
        self.backtracking = False

        # Store the goal for easy reference
        self.goal_coords = goal_coords

    def solve_tick(self) -> bool:
        # If we've already reached the goal and reconstructed the path, we're done
        if self.goal_reached:
            return True

        # If the stack is empty and we haven't reached the goal, no solution exists
        if not self.stack:
            return True  # Done, but no solution

        # Get the current position from the top of the stack
        current = self.stack[-1]
        current_row, current_col = current

        # If we've reached the goal
        if current == self.goal_coords:
            # We've found the goal! Now reconstruct the path
            self.goal_reached = True
            self._reconstruct_path()
            return True

        # Mark current cell as scanned (if it's not the start or end)
        if self.board.get_cell(current_row, current_col) not in [
            CellMark.START,
            CellMark.END,
        ]:
            self.board.set_cell(current_row, current_col, CellMark.SCANNED)

        # Get unvisited neighbors
        neighbors = self._get_unvisited_neighbors(current)

        if neighbors:
            # Choose the first unvisited neighbor
            next_cell = neighbors[0]
            next_row, next_col = next_cell
            next_index = self.board.cords_as_cell(next_cell)

            # Mark it as visited and add to stack
            self.visited.add(next_index)
            self.stack.append(next_cell)

            # Record where we came from (for path reconstruction)
            self.came_from[next_index] = self.board.cords_as_cell(current)

            return False  # Not done yet
        else:
            # No unvisited neighbors, backtrack
            self.stack.pop()
            return False  # Not done yet

    def _get_unvisited_neighbors(self, position):
        """Get all valid unvisited neighbors of the current position."""
        row, col = position
        neighbors = []

        # Define the four possible directions (up, right, down, left)
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Check if the new position is valid
            if not self.board._valid_coords(new_row, new_col):
                continue

            # Get the cell mark at the new position
            cell = self.board.get_cell(new_row, new_col)

            # Check if the new position is a valid move
            if cell in [CellMark.EMPTY, CellMark.END]:
                # Convert to index and check if already visited
                index = self.board.cords_as_cell((new_row, new_col))
                if index not in self.visited:
                    neighbors.append((new_row, new_col))

        return neighbors

    def _reconstruct_path(self):
        """Reconstruct the path from start to goal."""
        current = self.board.cords_as_cell(self.goal_coords)
        start_index = self.board.cords_as_cell(
            self.board.cell_as_coordinates(self.start)
        )

        while current != start_index:
            current_coords = self.board.cell_as_coordinates(current)
            row, col = current_coords

            # Mark the cell as part of the path (except start and end)
            if self.board.get_cell(row, col) not in [CellMark.START, CellMark.END]:
                self.board.set_cell(row, col, CellMark.PATH)

            current = self.came_from[current]
