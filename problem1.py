import tkinter as tk
from internal.maze.maze import MazeBoard, CellMark, get_random_start_goal
from internal.maze.generators import Generator, PrimsGenerator

class MazeUI:
    CELL_SIZE = 8
    DELAY = 1  # milliseconds

    def __init__(self, root : tk.Tk , generator : Generator):
        self.root = root
        self.generator = generator

        canvas_with = ((generator.width * 2) + 1) * self.CELL_SIZE
        canvas_height = ((generator.height * 2) + 1) * self.CELL_SIZE
        self.canvas = tk.Canvas(root, width=canvas_with,
                                      height=canvas_height)
        self.canvas.pack()
        self.rects = [[None for _ in range(generator.width)] for _ in range(generator.height)]
        self.draw_maze()
        self.animate()

    def draw_maze(self):
        maze_board : MazeBoard = self.generator.to_maze()
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
        if self.generator.generate_tick():  # Generate step-by-step
            self.draw_maze()  # Redraw the maze after a tick
            self.root.after(self.DELAY, self.animate)  # Continue animation
        else:
            print("Maze generation finished.")

# ---------- MAIN ----------
if __name__ == "__main__":
    generator = PrimsGenerator(5, 5)
    generator.generate()
    board = generator.to_maze()
    start, goal = get_random_start_goal(board, 3)
    
    board.set_cell(start[0], start[1], CellMark.SCANNED)
    board.set_cell(goal[0], goal[1], CellMark.SCANNED)

    print(board)

    # Initialize Tkinter root window
    root = tk.Tk()
    root.title("Maze Generator Animation")
    app = MazeUI(root, generator)
    root.mainloop()