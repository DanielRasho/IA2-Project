import tkinter as tk
import sys
import time

from tkinter import Scrollbar, RIGHT, Y
from threading import Lock
from internal.maze.maze import MazeBoard, CellMark, get_random_start_goal
from internal.maze.generators import Generator, PrimsGenerator, BorubskaGenerator
from internal.solver.solver import Solver
from internal.solver.A_Star import A_Star
from internal.solver.BFS import BFS
from internal.solver.DFS import DFS
from internal.solver.Dijikstra import Dijikstra
from internal.solver.solver_utils import SolverType, SolverFromType
from random import randint


sys.setrecursionlimit(15000)


class WholeUI:
    CELL_SIZE = 10
    PAUSE_SECS = 2
    DELAY = 5  # milliseconds

    def __init__(
        self,
        root: tk.Tk,
        mazes: list[MazeBoard],
        solvers: list[SolverType],
        canvas_width: int,
        canvas_height: int,
        x_offset: int,
        y_offset: int,
    ):
        """
        Initialize the Maze UI.
        - root: Tkinter root window.
        - generator: The maze generation algorithm.
        - x_offset, y_offset: Offsets for positioning the canvas.
        """
        self.root = root
        self.mazes = mazes

        self.current_experiment = 0
        self.solversType = solvers
        self.doneSolversType = []

        self.boards_per_player = {}
        for sType in solvers:
            self.boards_per_player[sType] = [MazeBoard.copy_from(m) for m in mazes]
            # self.board_per_solver[sType] = [m for m in mazes]

        self.solvers = {
            st: SolverFromType(
                st,
                self.boards_per_player[st][0],
                self.boards_per_player[st][0].cords_as_cell(
                    self.boards_per_player[st][0].start
                ),
                self.boards_per_player[st][0].cords_as_cell(
                    self.boards_per_player[st][0].end
                ),
            )
            for st in solvers
        }

        self.solvers_canvas = {}
        for i in range(len(solvers)):
            x_offset = 10
            if i % 2 != 0:
                x_offset += maze_width + 10
            y_offset = 10
            if i > 1:
                y_offset += maze_height + 50
            cv = tk.Canvas(root, width=canvas_width, height=canvas_height)
            cv.place(x=x_offset, y=y_offset)
            self.solvers_canvas[solvers[i]] = cv

            label = tk.Label(root, text=solvers[i], font=("Helvetica", 10))
            label.place(
                x=x_offset + canvas_width // 2 - 20, y=y_offset + canvas_height + 5
            )

        x = canvas_width * 2 + 50

        # AVG table
        self.avg_table_header = tk.Label(
            root, text="ALG\tAVG PLACE", font=("Helvetica", 20)
        )
        y = y_offset
        self.avg_table_header.place(x=x, y=y)
        position_avg = [0 for _ in solvers]
        self.avg_table = {k: v for (k, v) in zip(solvers, position_avg)}
        entries = [
            tk.Label(root, text="INITIAL TEXT", font=("Helvetica", 20)) for _ in solvers
        ]
        for i in range(len(entries)):
            ent = entries[i]
            x = x
            y += 40
            ent.place(x=x, y=y)
        self.avg_table_entries = {k: v for (k, v) in zip(solvers, entries)}

        # EXP table
        self.exp_table_header = tk.Label(
            root, text="ALG\tDIST\tEXPAN\tPLACE\t#EXP", font=("Helvetica", 20)
        )
        y += 120
        self.exp_table_header.place(x=x, y=y)
        values = [[0, 0, 0, 0] for _ in solvers]
        self.exp_table = {k: v for (k, v) in zip(solvers, values)}
        entries = [
            tk.Label(root, text="INITIAL TEXT", font=("Helvetica", 20)) for _ in solvers
        ]
        for i in range(len(entries)):
            ent = entries[i]
            x = x
            y += 40
            ent.place(x=x, y=y)
        self.exp_table_entries = {k: v for (k, v) in zip(solvers, entries)}

        self.draw_ui()
        self.animate()

    def draw_ui(self):
        currentIdx = self.current_experiment
        if self.reached_end_experiments():
            currentIdx = len(self.mazes) - 1

        for sType in self.solvers:
            maze_board: MazeBoard = self.boards_per_player[sType][currentIdx]
            canvas: tk.Canvas = self.solvers_canvas[sType]
            canvas.delete("all")

            for row in range(maze_board.height):
                for col in range(maze_board.width):
                    x0, y0 = col * self.CELL_SIZE, row * self.CELL_SIZE
                    x1, y1 = x0 + self.CELL_SIZE, y0 + self.CELL_SIZE

                    cell = maze_board.get_cell(row, col)

                    if cell == CellMark.WALL:
                        canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                    elif cell == CellMark.EMPTY:
                        canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                    elif cell == CellMark.SCANNED:
                        canvas.create_rectangle(x0, y0, x1, y1, fill="skyblue")
                    elif cell == CellMark.PATH:
                        canvas.create_rectangle(x0, y0, x1, y1, fill="brown")
                    elif cell == CellMark.START:
                        canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
                    elif cell == CellMark.END:
                        canvas.create_rectangle(x0, y0, x1, y1, fill="red")

        for header in self.exp_table:
            row = self.exp_table[header]
            entry = self.exp_table_entries[header]
            entry.config(text=f"{header}\t{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")

        for header in self.avg_table:
            row = self.avg_table[header]
            entry = self.avg_table_entries[header]
            entry.config(text=f"{header}\t{row}")

        self.root.update()

    def reached_end_experiments(self) -> bool:
        return self.current_experiment < 0 and self.current_experiment >= len(
            self.mazes
        )

    def animate(self):
        # Done animating this current experiment
        allDoneExperiment = len(self.doneSolversType) == len(self.solvers.keys())
        if allDoneExperiment:
            if self.reached_end_experiments():
                return

        if allDoneExperiment:
            print("ALL COMPLETED!")
            time.sleep(self.PAUSE_SECS)
            self.doneSolversType = []
            self.current_experiment += 1
            if self.reached_end_experiments():
                return
            else:
                print("Changing board and solvers!")
                for sType in self.solvers:
                    next_board = self.boards_per_player[sType][self.current_experiment]
                    self.solvers[sType] = SolverFromType(
                        sType,
                        next_board,
                        next_board.cords_as_cell(next_board.start),
                        next_board.cords_as_cell(next_board.end),
                    )

        for sType in self.solvers:
            solver: Solver = self.solvers[sType]
            solverBoard: MazeBoard = self.boards_per_player[sType][
                self.current_experiment % len(self.solversType)
            ]

            doneButOthersAreNot = (
                len(self.doneSolversType) != len(self.solversType)
                and sType in self.doneSolversType
            )

            if doneButOthersAreNot:
                print(
                    sType,
                    "Done! But others haven't completed!",
                    self.doneSolversType,
                    self.solversType,
                )
            else:  # Normal tick
                solved_laberinth = solver.solve_tick()

                self.exp_table[sType] = [
                    solverBoard.distance,
                    solver.get_scanned_tiles(),
                    -1,
                    self.current_experiment + 1,
                ]

                if solved_laberinth and sType not in self.doneSolversType:
                    self.doneSolversType.append(sType)
                    finishPosition = len(self.doneSolversType)
                    self.exp_table[sType][2] = finishPosition
                    self.avg_table[sType] += (
                        finishPosition - self.avg_table[sType]
                    ) / (self.current_experiment + 1)

        self.draw_ui()  # Redraw the maze after a tick
        self.root.after(self.DELAY, self.animate)


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

    maze_width = ((generator.width * 2) + 1) * WholeUI.CELL_SIZE
    maze_height = ((generator.height * 2) + 1) * WholeUI.CELL_SIZE

    # Set the window size dynamically to fit both canvases vertically
    window_width = maze_width + 20
    window_height = maze_height + 100
    root.geometry(f"{window_width}x{window_height}")

    # Create two independent UI instances, one besides the other
    solvers = [SolverType.BFS, SolverType.DFS, SolverType.DIJIKSTRA, SolverType.A_STAR]
    # solvers = [SolverType.DFS, SolverType.A_STAR]
    WholeUI(root, mazes, solvers, maze_width, maze_height, 10, 10)

    v = Scrollbar(root)
    v.pack(side=RIGHT, fill=Y)

    root.mainloop()
