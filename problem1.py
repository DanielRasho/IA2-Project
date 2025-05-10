import tkinter as tk
from internal.maze.maze import MazeBoard, CellMark, get_random_start_goal
from internal.maze.generators import Generator, PrimsGenerator, BorubskaGenerator

class MazeUI:
    CELL_SIZE = 5
    DELAY = 1  # milliseconds

    def __init__(self, root: tk.Tk, generator: Generator, x_offset: int, y_offset: int, label: str):
        """
        Initialize the Maze UI.
        - root: Tkinter root window.
        - generator: The maze generation algorithm.
        - x_offset, y_offset: Offsets for positioning the canvas.
        - label: Text to display under the maze.
        """
        self.root = root
        self.generator = generator

        canvas_width = ((generator.width * 2) + 1) * self.CELL_SIZE
        canvas_height = ((generator.height * 2) + 1) * self.CELL_SIZE
        
        # Create canvas with an offset
        self.canvas = tk.Canvas(root, width=canvas_width,
                                      height=canvas_height)
        self.canvas.place(x=x_offset, y=y_offset)

        # Create a label under the canvas
        self.label = tk.Label(root, text=label, font=("Helvetica", 10))
        self.label.place(x=x_offset + canvas_width // 2 - 20, y=y_offset + canvas_height + 5)

        self.draw_maze()
        self.animate()

    def draw_maze(self):
        """Draws the maze on the canvas."""
        maze_board: MazeBoard = self.generator.to_maze()
        self.canvas.delete("all")

        for row in range(maze_board.height):
            for col in range(maze_board.width):
                x0, y0 = col * self.CELL_SIZE, row * self.CELL_SIZE
                x1, y1 = x0 + self.CELL_SIZE, y0 + self.CELL_SIZE

                if maze_board.get_cell(row, col) == CellMark.WALL:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                elif maze_board.get_cell(row, col) == CellMark.EMPTY:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")

        self.root.update()

    def animate(self):
        """Runs the maze generation step by step."""
        if self.generator.generate_tick():  # Generate step-by-step
            self.draw_maze()  # Redraw the maze after a tick
            self.root.after(self.DELAY, self.animate)  # Continue animation
        else:
            print(f"{self.label.cget('text')} Maze generation finished.")


# ---------- MAIN ----------
if __name__ == "__main__":
    print(" ==== MAZE GENERATION ===== ")
    width = int(input("Width: "))
    height = int(input("Height: "))

    # Generators
    BorubsGen = BorubskaGenerator(width, height)
    PrimsGen = PrimsGenerator(width, height)

    # Initialize Tkinter root window
    root = tk.Tk()
    root.title("Maze Generator Animation")

    # Set the window size dynamically to fit both canvases vertically
    window_width = ((width * 2) + 1) * MazeUI.CELL_SIZE + 20
    window_height = ((height * 2) + 1) * 2 * MazeUI.CELL_SIZE + 100
    root.geometry(f"{window_width}x{window_height}")

    # Create two independent UI instances, one below the other
    app1 = MazeUI(root, BorubsGen, x_offset=10, y_offset=10, label="Borůvka")
    app2 = MazeUI(root, PrimsGen, x_offset=10, y_offset=((height * 2) + 1) * MazeUI.CELL_SIZE + 50, label="Prim")

    root.mainloop()