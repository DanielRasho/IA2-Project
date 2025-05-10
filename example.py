import tkinter as tk
from internal.maze.maze import MazeBoard, CellMark, get_random_start_goal
from internal.maze.generators import Generator, get_generator, GeneratorType
from internal.solver.Dijikstra import Dijikstra

# ---------- MAIN ----------
# Boilerplate code

if __name__ == "__main__":
    generator = get_generator(GeneratorType.PRIM, 10, 10)
    # Let the generator build a maze internally
    generator.generate()
    # Retrieve maze board
    maze = generator.to_maze()
    # Select random start and goal
    start, goal = get_random_start_goal(maze, 3)
    
    solver = Dijikstra(maze, start, goal)
    
    # Solve the maze
    while solver.solve_tick() :
        print(solver.board)
        
    print("Maze solved!")
    print(solver.board)
    print(f"tiles scanned {solver.scanned_tiles}")
    print(f"solution path tiles {solver.scanned_tiles}")
