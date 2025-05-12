import tkinter as tk
from tkinter import Scrollbar, RIGHT, Y
from threading import Lock
from internal.maze.maze import MazeBoard, CellMark, get_random_start_goal
from internal.maze.generators import Generator, PrimsGenerator, BorubskaGenerator
from internal.solver.A_Star import A_Star
from internal.solver.BFS import BFS
from internal.solver.DFS import DFS
from internal.solver.Dijikstra import Dijikstra
from internal.solver.solver_utils import SolverType, SolverFromType
from random import randint


WORKERS_COUNT = 0

DONE_COUNT_LOCK = Lock()
DONE_COUNT = 0


class UiStats:
    def __init__(
        self,
        sType: SolverType,
        distance: int,
        expanded: int,
        isDone: bool,
        current_exp_count: int,
    ):
        self.type = sType
        self.distance = distance
        self.expanded = expanded
        self.isDone = isDone
        self.currentExpCount = current_exp_count


class MazeUI:
    CELL_SIZE = 10
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
        self.sType = solverType

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
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
                elif cell == CellMark.END:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="red")

        self.root.update()

    def get_stats(self) -> UiStats:
        current_board = self.mazes[self.current_experiment]
        if self.solver == None:
            return UiStats(self.sType, 0, 0, False, 0)
        else:
            return UiStats(
                self.sType,
                current_board.distance,
                self.solver.get_scanned_tiles(),
                self.finished,
                self.current_experiment + 1,
            )
        pass

    def animate(self):
        global DONE_COUNT
        DONE_COUNT_LOCK.acquire()
        # Done animating this current experiment
        experimentDone = DONE_COUNT == WORKERS_COUNT and self.finished
        doneButOthersAreNot = DONE_COUNT != WORKERS_COUNT and self.finished
        if experimentDone:
            self.current_experiment += 1
            reachedEndOfExperiments = (
                self.current_experiment < 0
                and self.current_experiment >= len(self.mazes)
            )
            if reachedEndOfExperiments:
                return

            current_board = self.mazes[self.current_experiment]
            [srow, scol] = current_board.start
            [erow, ecol] = current_board.end
            self.solver = SolverFromType(
                self.sType,
                current_board,
                current_board.cords_as_cell(current_board.start),
                current_board.cords_as_cell(current_board.end),
            )
            self.finished = False
            DONE_COUNT -= 1
            DONE_COUNT_LOCK.release()
            self.draw_maze()  # Redraw the maze after a tick
            self.root.after(self.DELAY, self.animate)
        elif doneButOthersAreNot:
            DONE_COUNT_LOCK.release()
            self.root.after(self.DELAY, self.animate)
        else:  # Normal tick
            self.finished = self.solver.solve_tick()

            if self.finished:
                DONE_COUNT += 1
            DONE_COUNT_LOCK.release()

            self.draw_maze()
            self.root.after(self.DELAY, self.animate)  # Continue animation


class TableUI:
    DELAY = 1

    def __init__(
        self,
        root: tk.Tk,
        mazeUis: list[MazeUI],
        solvers: list[SolverType],
        x_offset: int,
        y_offset: int,
    ):
        self.root = root

        self.avg_table_header = tk.Label(
            root, text="ALG\tAVG PLACE", font=("Helvetica", 20)
        )
        y = y_offset
        self.avg_table_header.place(x=x_offset, y=y)
        position_avg = [0 for _ in solvers]
        self.avg_table = {k: v for (k, v) in zip(solvers, position_avg)}
        entries = [
            tk.Label(root, text="INITIAL TEXT", font=("Helvetica", 20)) for _ in solvers
        ]
        for i in range(len(entries)):
            ent = entries[i]
            x = x_offset
            y += 40
            ent.place(x=x, y=y)
        self.avg_table_entries = {k: v for (k, v) in zip(solvers, entries)}

        self.exp_table_header = tk.Label(
            root, text="ALG\tDIST\tEXPAN\tPLACE\t#EXP", font=("Helvetica", 20)
        )
        y += 120
        self.exp_table_header.place(x=x_offset, y=y)
        values = [[0, 0, 0, 0] for _ in solvers]
        self.exp_table = {k: v for (k, v) in zip(solvers, values)}
        entries = [
            tk.Label(root, text="INITIAL TEXT", font=("Helvetica", 20)) for _ in solvers
        ]
        for i in range(len(entries)):
            ent = entries[i]
            x = x_offset
            y += 40
            ent.place(x=x, y=y)
        self.exp_table_entries = {k: v for (k, v) in zip(solvers, entries)}

        self.mazeUis = mazeUis
        self.animate()

    def update_tables(self):
        for header in self.exp_table:
            row = self.exp_table[header]
            entry = self.exp_table_entries[header]
            entry.config(text=f"{header}\t{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")

        for header in self.avg_table:
            row = self.avg_table[header]
            entry = self.avg_table_entries[header]
            entry.config(text=f"{header}\t{row}")

    def animate(self):
        order = []
        expCount = {}
        for ui in self.mazeUis:
            stats = ui.get_stats()
            if stats.isDone:
                order.append(stats.type)
            self.exp_table[stats.type] = [
                stats.distance,
                stats.expanded,
                -1,
                stats.currentExpCount,
            ]
            expCount[stats.type] = stats.currentExpCount

        for i in range(len(order)):
            ordType = order[i]
            self.exp_table[ordType][2] = i + 1
            self.avg_table[ordType] += (i + 1 - self.avg_table[ordType]) / expCount[
                ordType
            ]

        self.update_tables()
        self.root.after(self.DELAY, self.animate)  # Continue animation


def generate_random_board(generator: Generator) -> MazeBoard:
    board = generator.generate()
    get_random_start_goal(board, 3)
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
    v = Scrollbar(root)
    v.pack(side=RIGHT, fill=Y)

    maze_width = ((generator.width * 2) + 1) * MazeUI.CELL_SIZE
    maze_height = ((generator.height * 2) + 1) * MazeUI.CELL_SIZE

    # Set the window size dynamically to fit both canvases vertically
    window_width = maze_width + 20
    window_height = maze_height + 100
    root.geometry(f"{window_width}x{window_height}")

    # Create two independent UI instances, one besides the other
    solvers = [SolverType.BFS, SolverType.DFS, SolverType.DIJIKSTRA, SolverType.A_STAR]
    WORKERS_COUNT = len(solvers)
    DONE_COUNT = WORKERS_COUNT
    mazeUis = []
    for i in range(WORKERS_COUNT):
        solver = solvers[i]
        x_offset = 10
        if i % 2 != 0:
            x_offset += maze_width + 10
        y_offset = 10
        if i > 1:
            y_offset += maze_height + 50

        ui = MazeUI(
            root,
            mazes,
            solver,
            maze_width,
            maze_height,
            x_offset,
            y_offset,
            label=solver,
        )
        mazeUis.append(ui)

    x_offset = (maze_width + 10 + 10) * 2 + 50
    y_offset = 10
    tableUi = TableUI(root, mazeUis, solvers, x_offset, y_offset)

    root.mainloop()
