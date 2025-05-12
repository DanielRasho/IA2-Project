import tkinter as tk
from internal.maze.maze import MazeBoard, CellMark, get_random_start_goal
from internal.maze.generators import Generator, PrimsGenerator, BorubskaGenerator
from internal.solver.A_Star import A_Star
from internal.solver.BFS import BFS
from internal.solver.DFS import DFS
from internal.solver.Dijikstra import Dijikstra
from internal.solver.solver_utils import SolverType, SolverFromType
from random import randint


workersCount = 0
doneCount = 0


class MazeUI:
    CELL_SIZE = 5
    DELAY = 1  # milliseconds

    def __init__(
        self,
        root: tk.Tk,
        mazes: list[MazeBoard],
        solverType: SolverType,
        canvas_width: int,
        canvas_height: int,
        x_offset: int,
        y_offset: int,
        label: str,
    ):
        """
        Initialize the Maze UI.
        - root: Tkinter root window.
        - generator: The maze generation algorithm.
        - x_offset, y_offset: Offsets for positioning the canvas.
        - label: Text to display under the maze.
        """
        self.root = root
        self.mazes = mazes

        self.current_experiment = -1
        self.solver = None
        self.finished = True

        # Create canvas with an offset
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.canvas.place(x=x_offset, y=y_offset)

        # Create a label under the canvas
        self.label = tk.Label(root, text=label, font=("Helvetica", 10))
        self.label.place(
            x=x_offset + canvas_width // 2 - 20, y=y_offset + canvas_height + 5
        )

        self.draw_maze()
        self.animate()

    def draw_maze(self):
        """Draws the maze on the canvas."""
        if self.current_experiment < 0 and self.current_experiment >= len(self.mazes):
            return

        maze_board: MazeBoard = self.mazes[self.current_experiment]
        self.canvas.delete("all")

        for row in range(maze_board.height):
            for col in range(maze_board.width):
                x0, y0 = col * self.CELL_SIZE, row * self.CELL_SIZE
                x1, y1 = x0 + self.CELL_SIZE, y0 + self.CELL_SIZE

                cell = maze_board.get_cell(row, col)

                if cell == CellMark.WALL:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                elif cell == CellMark.EMPTY:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                elif cell == CellMark.SCANNED:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="skyblue")
                elif cell == CellMark.PATH:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="brown")
                elif cell == CellMark.START:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="lightgreen")
                elif cell == CellMark.END:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="pink")

        self.root.update()

    def animate(self):
        # Done animating this current experiment
        experimentDone = doneCount == workersCount and self.finished
        doneButOthersAreNot = doneCount != workersCount and self.finished
        if experimentDone:
            self.current_experiment += 1
            reachedEndOfExperiments = (
                self.current_experiment < 0
                and self.current_experiment >= len(self.mazes)
            )
            if reachedEndOfExperiments:
                return

            current_board = self.mazes[self.current_experiment]
            self.solver = SolverFromType(
                self.sType, current_board, current_board.start, current_board.end
            )

            self.finished = False
            self.draw_maze()  # Redraw the maze after a tick
            self.root.after(self.DELAY, self.animate)
        elif doneButOthersAreNot:
            self.root.after(self.DELAY, self.animate)
        else:  # Normal tick
            self.solver
            self.draw_maze()
            self.root.after(self.DELAY, self.animate)  # Continue animation


def generate_random_board(generator: Generator) -> MazeBoard:
    board = generator.generate()
    get_random_start_goal(board, 10)
    return board


# ---------- MAIN ----------
if __name__ == "__main__":
    print(" ==== MAZE GENERATION ===== ")
    width = int(input("Width: "))
    height = int(input("Height: "))

    # Generators
    genInput = input("Borubska/Prims (b/p): ")
    generator = PrimsGenerator(width, height)
    if genInput == "b":
        generator = BorubskaGenerator(width, height)

    experimentCount = int(input("Experiment count: "))
    mazes = [generate_random_board(generator) for _ in range(experimentCount)]

    # Initialize Tkinter root window
    root = tk.Tk()
    root.title("Maze solvers comparison")

    maze_width = width * MazeUI.CELL_SIZE
    maze_hegith = height * MazeUI.CELL_SIZE

    # Set the window size dynamically to fit both canvases vertically
    window_width = maze_width + 20
    window_height = maze_hegith + 100
    root.geometry(f"{window_width}x{window_height}")

    # Create two independent UI instances, one besides the other
    solvers = [SolverType.BFS, SolverType.DFS, SolverType.DIJIKSTRA, SolverType.A_STAR]
    workersCount = len(solvers)
    doneCount = workersCount
    for i in range(workersCount):
        solver = solvers[i]
        x_offset = 10
        if i % 2 != 0:
            x_offset += maze_width + 10
        y_offset = 10
        if i % 2 != 0:
            y_offset += maze_hegith + 10

        MazeUI(
            root,
            mazes,
            solver,
            maze_width,
            maze_hegith,
            x_offset,
            y_offset,
            label=solver,
        )

    root.mainloop()
