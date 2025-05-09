from enum import IntEnum

class CellMark(IntEnum):
    EMPTY = 0
    WALL = 1
    PATH = 2
    SCANNED = 3
    
class MazeBoard:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.cells = [CellMark.EMPTY] * (height * width)

    def _index(self, row: int, col: int) -> int:
        return row * self.width + col

    def get_cell(self, row: int, col: int) -> CellMark:
        if not self._valid_coords(row, col):
            raise IndexError("Coordinates out of bounds")
        return self.cells[self._index(row, col)]

    def set_cell(self, row: int, col: int, value: CellMark):
        if not self._valid_coords(row, col):
            raise IndexError("Coordinates out of bounds")
        self.cells[self._index(row, col)] = value

    def _valid_coords(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def __str__(self):
        result = ""
        for r in range(self.height):
            for c in range(self.width):
                cell = self.get_cell(r, c)
                if cell == CellMark.EMPTY:
                    result += "."
                elif cell == CellMark.WALL:
                    result += "#"
                elif cell == CellMark.PATH:
                    result += "o"
            result += "\n"
        return result
    