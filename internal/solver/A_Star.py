from enum import StrEnum
from typing import Tuple
from ..maze.maze import MazeBoard, CellMark
from .solver import Solver

import heapq


class A_Star(Solver):
    def __init__(self, board: MazeBoard, start: int, goal: int):
        super().__init__(board, start, goal)

        self.start = start
        self.goal = goal

        # Convert 1D indices to 2D coordinates
        self.start_coords = self.board.cell_as_coordinates(start)
        self.goal_coords = self.board.cell_as_coordinates(goal)

        # Priority queue for A* - stores (f_score, count, coords)
        # Count is used to break ties for cells with equal f_scores
        self.open_set = []
        self.open_set_counter = 0  # Used to break ties in priority queue

        # Track which nodes are in the open set for faster lookup
        self.in_open_set = set()

        # Track visited (closed set) cells
        self.visited = set()

        # Track g_score (actual cost from start) and f_score (g_score + heuristic)
        self.g_score = {}  # Stores actual cost from start
        self.f_score = {}  # Stores g_score + heuristic

        # Initialize start node
        self.g_score[self.start] = 0
        self.f_score[self.start] = self._heuristic(self.start_coords)

        # Add start node to open set
        heapq.heappush(
            self.open_set,
            (self.f_score[self.start], self.open_set_counter, self.start_coords),
        )
        self.open_set_counter += 1
        self.in_open_set.add(self.start)

        # For path reconstruction
        self.came_from = {}

        # Flag to indicate if we've reached the goal
        self.goal_reached = False

    def _heuristic(self, coords):
        """Manhattan distance heuristic"""
        return abs(coords[0] - self.goal_coords[0]) + abs(
            coords[1] - self.goal_coords[1]
        )

    def solve_tick(self) -> bool:
        # If we've already reached the goal and reconstructed the path, we're done
        if self.goal_reached:
            return True

        # If the open set is empty and we haven't reached the goal, no solution exists
        if not self.open_set:
            print("No solution exists")
            return True  # Done, but no solution

        # Get the node with the lowest f_score from the priority queue
        _, _, current_coords = heapq.heappop(self.open_set)
        current_index = self.board.cords_as_cell(current_coords)

        # Remove from the open set tracking
        self.in_open_set.remove(current_index)

        # If we've reached the goal
        if current_coords == self.goal_coords:
            self.goal_reached = True
            self._reconstruct_path()
            return True

        # Add to visited set
        self.visited.add(current_index)
        self.scanned_tiles += 1

        # Mark current cell as scanned (if it's not the start or end)
        current_row, current_col = current_coords
        if self.board.get_cell(current_row, current_col) not in [
            CellMark.START,
            CellMark.END,
        ]:
            self.board.set_cell(current_row, current_col, CellMark.SCANNED)

        # Explore neighbors
        neighbors = self._get_valid_neighbors(current_coords)

        for neighbor_coords in neighbors:
            neighbor_index = self.board.cords_as_cell(neighbor_coords)

            # Skip if already in closed set
            if neighbor_index in self.visited:
                continue

            # Calculate tentative g_score (cost from start to this neighbor through current)
            # In a simple grid like this, all moves cost 1
            tentative_g_score = self.g_score[current_index] + 1

            if (
                neighbor_index not in self.g_score
                or tentative_g_score < self.g_score[neighbor_index]
            ):
                # This path to neighbor is better than any previous one
                self.came_from[neighbor_index] = current_index
                self.g_score[neighbor_index] = tentative_g_score
                self.f_score[neighbor_index] = tentative_g_score + self._heuristic(
                    neighbor_coords
                )

                if neighbor_index not in self.in_open_set:
                    # Add to open set
                    heapq.heappush(
                        self.open_set,
                        (
                            self.f_score[neighbor_index],
                            self.open_set_counter,
                            neighbor_coords,
                        ),
                    )
                    self.open_set_counter += 1
                    self.in_open_set.add(neighbor_index)

        return False  # Not done yet

    def _get_valid_neighbors(self, position):
        """Get all valid neighbors of the current position."""
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
                neighbors.append((new_row, new_col))

        return neighbors

    def _reconstruct_path(self):
        """Reconstruct the path from start to goal."""
        current = self.board.cords_as_cell(self.goal_coords)
        start_index = self.start

        while current != start_index:
            current_coords = self.board.cell_as_coordinates(current)
            row, col = current_coords

            # Mark the cell as part of the path (except start and end)
            if self.board.get_cell(row, col) not in [CellMark.START, CellMark.END]:
                self.board.set_cell(row, col, CellMark.PATH)

            current = self.came_from[current]
