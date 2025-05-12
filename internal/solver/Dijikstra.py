from typing import List, Tuple, Dict
import heapq
from ..maze.maze import MazeBoard, CellMark
from .solver import Solver

class Dijikstra(Solver):
    def __init__(self, board: MazeBoard, start: Tuple[int, int], goal: Tuple[int, int]):
        super().__init__(board, start, goal)
        self.board = board
        self.start = start
        self.goal = goal
        
        self.distances = {} 
        self.previous = {}  
        self.priority_queue = []
        self.visited = set() 
        
        self.distances[start] = 0
        heapq.heappush(self.priority_queue, (0, start))
        
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
            
            if (0 <= new_row < self.board.height and 
                0 <= new_col < self.board.width and 
                self.board.get_cell(new_row, new_col) != CellMark.WALL):
                neighbors.append((new_row, new_col))
                
        return neighbors

    def solve_tick(self) -> bool:
        """Perform one step of Dijkstra's algorithm."""
        if self.reconstructed_path:
            return False
            
        if self.found_goal:
            self._reconstruct_path()
            self.reconstructed_path = True
            return False
            
        if not self.priority_queue:
            print("No path found to the goal!")
            return False
            
        current_distance, current_position = heapq.heappop(self.priority_queue)
        
        if current_position in self.visited:
            return True
            
        self.visited.add(current_position)
        self.scanned_tiles += 1
        
        row, col = current_position
        if current_position != self.start and current_position != self.goal:
            self.board.set_cell(row, col, CellMark.SCANNED)
        
        if current_position == self.goal:
            self.found_goal = True
            return True
            
        for neighbor in self.get_neighbors(current_position):
            distance = current_distance + 1
            
            if neighbor not in self.distances or distance < self.distances[neighbor]:
                self.distances[neighbor] = distance
                self.previous[neighbor] = current_position
                heapq.heappush(self.priority_queue, (distance, neighbor))
                
        return True
        
    def _reconstruct_path(self):
        """Reconstruct the path from start to goal using the previous dictionary."""
        current = self.goal
        path = []
        
        while current != self.start:
            path.append(current)
            current = self.previous[current]
            
        path.append(self.start)
        path.reverse() 
        
        self.solution_path = path
        
        for position in path:
            row, col = position
            if position != self.start and position != self.goal:
                self.board.set_cell(row, col, CellMark.PATH)
                
        print(f"Camino encontrado! Longitud: {len(path)}")
        print(f"Nodos visitados: {self.scanned_tiles}")

