import tkinter as tk
import heapq
from enum import StrEnum
from internal.maze.maze import MazeBoard, CellMark, get_random_start_goal
from internal.maze.generators import get_generator, GeneratorType
from internal.solver.solver import Solver
from internal.solver.solver_utils import SolverType, SolverFromType


class MazeUI:
    CELL_SIZE = 5
    DELAY = 1

    def __init__(
        self,
        root: tk.Tk,
        maze_board: MazeBoard,
        solver_type: SolverType,
        x_offset: int,
        y_offset: int,
        label: str,
    ):
        """
        Initialize the Maze Solver UI.
        - root: Tkinter root window.
        - maze_board: The maze to solve.
        - solver_type: The algorithm to use for solving.
        - x_offset, y_offset: Offsets for positioning the canvas.
        - label: Text to display under the maze.
        """
        self.root = root
        self.board = maze_board

        canvas_width = self.board.width * self.CELL_SIZE
        canvas_height = self.board.height * self.CELL_SIZE

        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.canvas.place(x=x_offset, y=y_offset)

        self.label = tk.Label(root, text=label, font=("Helvetica", 10))
        self.label.place(
            x=x_offset + canvas_width // 2 - 20, y=y_offset + canvas_height + 5
        )

        self.stats_frame = tk.Frame(root)
        self.stats_frame.place(x=x_offset, y=y_offset + canvas_height + 25)

        self.path_length_label = tk.Label(self.stats_frame, text="Path Length: 0")
        self.path_length_label.pack(side=tk.LEFT, padx=5)

        self.nodes_explored_label = tk.Label(self.stats_frame, text="Nodes Explored: 0")
        self.nodes_explored_label.pack(side=tk.LEFT, padx=5)

        start_row, start_col = 1, 1

        goal_row, goal_col = self.board.height - 2, self.board.width - 2

        if self.board.get_cell(start_row, start_col) == CellMark.WALL:
            for r in range(1, self.board.height - 1):
                for c in range(1, self.board.width - 1):
                    if self.board.get_cell(r, c) == CellMark.EMPTY:
                        start_row, start_col = r, c
                        break
                if self.board.get_cell(start_row, start_col) == CellMark.EMPTY:
                    break

        if self.board.get_cell(goal_row, goal_col) == CellMark.WALL:
            for r in range(self.board.height - 2, 0, -1):
                for c in range(self.board.width - 2, 0, -1):
                    if self.board.get_cell(r, c) == CellMark.EMPTY:
                        goal_row, goal_col = r, c
                        break
                if self.board.get_cell(goal_row, goal_col) == CellMark.EMPTY:
                    break

        start_index = start_row * self.board.width + start_col
        goal_index = goal_row * self.board.width + goal_col

        self.board.set_cell(start_row, start_col, CellMark.START)
        self.board.set_cell(goal_row, goal_col, CellMark.END)

        print(f"Start position: ({start_row}, {start_col}), index: {start_index}")
        print(f"Goal position: ({goal_row}, {goal_col}), index: {goal_index}")

        self.solver = SolverFromType(solver_type, self.board, start_index, goal_index)

        self.draw_maze()

        self.animate()

    def draw_maze(self):
        """Draws the current state of the maze on the canvas."""
        self.canvas.delete("all")

        for row in range(self.board.height):
            for col in range(self.board.width):
                x0, y0 = col * self.CELL_SIZE, row * self.CELL_SIZE
                x1, y1 = x0 + self.CELL_SIZE, y0 + self.CELL_SIZE

                cell = self.board.get_cell(row, col)

                if cell == CellMark.WALL:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                elif cell == CellMark.EMPTY:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                elif cell == CellMark.PATH:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="green")
                elif cell == CellMark.SCANNED:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="light blue")
                elif cell == CellMark.START:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
                elif cell == CellMark.END:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="red")

        path_length = len(self.solver.get_solution_path())
        nodes_explored = self.solver.get_scanned_tiles()

        self.path_length_label.config(text=f"Longitud: {path_length}")
        self.nodes_explored_label.config(text=f"Nodod explorados: {nodes_explored}")

        self.root.update()

    def animate(self):
        """Runs the maze solving step by step."""
        if not self.solver.solve_tick():
            self.draw_maze()
            self.root.after(self.DELAY, self.animate)
        else:
            self.draw_maze()
            print(f"{self.label.cget('text')} Laberinto terinado.")
            print(f"Longitud: {len(self.solver.get_solution_path())}")
            print(f"Nodos explorados: {self.solver.get_scanned_tiles()}")


# ---------- MAIN ----------
if __name__ == "__main__":
    print(" ==== RESOLVIENDO LABERINTO ===== ")

    width, height = 60, 80

    generator = get_generator(GeneratorType.PRIM, height, width)
    generator.generate()
    maze = generator.to_maze()

    root = tk.Tk()
    root.title("Maze Solver Animation")

    window_width = maze.width * MazeUI.CELL_SIZE + 40
    window_height = maze.height * MazeUI.CELL_SIZE + 150
    root.geometry(f"{window_width}x{window_height}")

    solvers = [
        (SolverType.BFS, "BFS"),
        (SolverType.DFS, "DFS"),
        (SolverType.DIJIKSTRA, "Dijkstra"),
        (SolverType.A_STAR, "A*"),
    ]

    solver_type, solver_label = solvers[2]

    app = MazeUI(root, maze, solver_type, x_offset=20, y_offset=20, label=solver_label)

    root.mainloop()
