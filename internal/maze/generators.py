from enum import IntEnum
from typing import Tuple, List
from .maze import MazeBoard, CellMark
import random

class GeneratorType(IntEnum):
    BORUBSKA = 0
    PRIM = 1

class Generator:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width

    '''Generate a fully flesh-out maze'''
    def generate(self) -> MazeBoard :
        raise NotImplementedError("Subclasses should implement generate()")

    '''Represents one tick of the generation step'''
    def generate_tick(self) -> bool:
        raise NotImplementedError("Subclasses should implement generate_tick()")

    '''Returns a Mazeboard representation of the internal maze generator'''
    def to_maze() -> MazeBoard:
        raise NotImplementedError("Subclasses should implement generate_tick()")

class BorubskaGenerator(Generator):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
    VISITED = 4

    def __init__(self, height: int, width: int):
        super().__init__(height, width)
        self.rng = random.Random()
        self.grid = [[0b1111 for _ in range(width)] for _ in range(height)]
        self.components = {}  # To keep track of connected components
        self.edges = []       # List of edges between components
        self.phase_completed = False
        
        # Initialize components and edges, each cell is its own component
        for y in range(height):
            for x in range(width):
                idx = y * width + x

                # Insert each node as a component
                self.components[idx] = idx

                # Build all possible edges with their weights.
                if y > 0:  # NORTH
                    self.edges.append((idx, idx - self.width))
                if y < self.height - 1:  # SOUTH
                    self.edges.append((idx, idx + self.width))
                if x > 0:  # WEST
                    self.edges.append((idx, idx - 1))
                if x < self.width - 1:  # EAST
                    self.edges.append((idx, idx + 1))
        # Shuffle the edges to introduce randomness
        self.rng.shuffle(self.edges)

        
    def _find(self, component):
        """Find the root of the component."""
        if self.components[component] != component:
            self.components[component] = self._find(self.components[component])
        return self.components[component]

    def _union(self, u, v):
        """Union two components."""
        root_u = self._find(u)
        root_v = self._find(v)
        if root_u != root_v:
            self.components[root_v] = root_u

    def generate(self) -> MazeBoard:
        """Generate the full maze using Borůvka's algorithm."""
        while not self.phase_completed:
            self.generate_tick()
        return self.to_maze()

    def generate_tick(self) -> bool:
        """One step in the Borůvka's algorithm, processing a single edge."""
        if not self.edges or self.phase_completed:
            return False

        # Pop one edge from the list
        u, v = self.edges.pop()

        root_u = self._find(u)
        root_v = self._find(v)

        if root_u != root_v:
            self._union(u, v)

            # Remove the walls in the maze representation
            uy, ux = divmod(u, self.width)
            vy, vx = divmod(v, self.width)

            if uy == vy and ux + 1 == vx:
                self.grid[uy][ux] &= ~(1 << self.EAST)
                self.grid[vy][vx] &= ~(1 << self.WEST)
            elif uy == vy and ux - 1 == vx:
                self.grid[uy][ux] &= ~(1 << self.WEST)
                self.grid[vy][vx] &= ~(1 << self.EAST)
            elif ux == vx and uy + 1 == vy:
                self.grid[uy][ux] &= ~(1 << self.SOUTH)
                self.grid[vy][vx] &= ~(1 << self.NORTH)
            elif ux == vx and uy - 1 == vy:
                self.grid[uy][ux] &= ~(1 << self.NORTH)
                self.grid[vy][vx] &= ~(1 << self.SOUTH)

        # If there are no more edges to process, mark as completed
        if not self.edges:
            self.phase_completed = True

        return True

    def to_maze(self) -> MazeBoard:
        """Convert the internal bitmask representation to a MazeBoard."""
        maze_board = MazeBoard(self.height * 2 + 1, self.width * 2 + 1, CellMark.WALL)
        for i in range(self.height):
            for j in range(self.width):
                r, c = i * 2 + 1, j * 2 + 1
                maze_board.set_cell(r, c, CellMark.EMPTY)

                if not (self.grid[i][j] & (1 << self.NORTH)):
                    maze_board.set_cell(r - 1, c, CellMark.EMPTY)
                if not (self.grid[i][j] & (1 << self.SOUTH)):
                    maze_board.set_cell(r + 1, c, CellMark.EMPTY)
                if not (self.grid[i][j] & (1 << self.WEST)):
                    maze_board.set_cell(r, c - 1, CellMark.EMPTY)
                if not (self.grid[i][j] & (1 << self.EAST)):
                    maze_board.set_cell(r, c + 1, CellMark.EMPTY)

        return maze_board

class PrimsGenerator(Generator):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
    VISITED = 4

    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.rng = random.Random()
        # Initialize all cells with all walls (0b1111) and not visited (0b00000)
        self.grid = [[0b1111 for _ in range(width)] for _ in range(height)]
        self.frontier = []
        
        
        # Start at a random cell
        start = (self.rng.randint(0, self.height - 1), self.rng.randint(0, self.width - 1))
        self._mark_visited(*start)
        self._add_frontier(*start)


    def _mark_visited(self, i, j):
        self.grid[i][j] |= (1 << self.VISITED)

    def _is_visited(self, i, j):
        return bool(self.grid[i][j] & (1 << self.VISITED))

    def _remove_wall(self, i1, j1, i2, j2, direction):
        # Remove wall between cells based on direction
        if direction == 'N':
            self.grid[i1][j1] &= ~(1 << self.NORTH)
            self.grid[i2][j2] &= ~(1 << self.SOUTH)
        elif direction == 'S':
            self.grid[i1][j1] &= ~(1 << self.SOUTH)
            self.grid[i2][j2] &= ~(1 << self.NORTH)
        elif direction == 'E':
            self.grid[i1][j1] &= ~(1 << self.EAST)
            self.grid[i2][j2] &= ~(1 << self.WEST)
        elif direction == 'W':
            self.grid[i1][j1] &= ~(1 << self.WEST)
            self.grid[i2][j2] &= ~(1 << self.EAST)

    def _add_frontier(self, i, j):
        for (di, dj, direction, opposite) in [
            (-1, 0, 'N', 'S'), (1, 0, 'S', 'N'), (0, -1, 'W', 'E'), (0, 1, 'E', 'W')
        ]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.height and 0 <= nj < self.width and not self._is_visited(ni, nj):
                self.frontier.append((i, j, ni, nj, direction, opposite))

    def generate(self) -> MazeBoard:

        # Run the generator step by step
        while self.frontier:
            self.generate_tick()

        return self.to_maze()

    def generate_tick(self) -> bool:
        if not self.frontier:
            return False

        # Pick a random frontier cell
        i, j, ni, nj, direction, opposite = self.frontier.pop(self.rng.randint(0, len(self.frontier) - 1))

        # If the neighboring cell hasn't been visited
        if not self._is_visited(ni, nj):
            # Remove walls between current cell and chosen neighboring cell
            self._remove_wall(i, j, ni, nj, direction)
            self._mark_visited(ni, nj)
            # Add new frontiers from the newly visited cell
            self._add_frontier(ni, nj)
        return True

    def to_maze(self):
        maze_board = MazeBoard(self.height * 2 + 1, self.width * 2 + 1, CellMark.WALL)

        for i in range(self.height):
            for j in range(self.width):
                r, c = i * 2 + 1, j * 2 + 1
                maze_board.set_cell(r, c, CellMark.EMPTY)

                if not (self.grid[i][j] & (1 << self.NORTH)):
                    maze_board.set_cell(r - 1, c, CellMark.EMPTY)
                if not (self.grid[i][j] & (1 << self.SOUTH)):
                    maze_board.set_cell(r + 1, c, CellMark.EMPTY)
                if not (self.grid[i][j] & (1 << self.WEST)):
                    maze_board.set_cell(r, c - 1, CellMark.EMPTY)
                if not (self.grid[i][j] & (1 << self.EAST)):
                    maze_board.set_cell(r, c + 1, CellMark.EMPTY)

        return maze_board

def get_generator(type: GeneratorType, height, width) -> Generator:
    if type == GeneratorType.BORUBSKA:
        return BorubskaGenerator(height, width)
    elif type == GeneratorType.PRIM:
        return PrimsGenerator(height, width)