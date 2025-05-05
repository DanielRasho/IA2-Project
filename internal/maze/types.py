# // package maze

# // // Represents the state of a cell in the board.
# // // A board cell can either be:
# // // * Empty.
# // // * Marked by X.
# // // * Marked by O.
# // type CellMark = int

# // const (
# // 	EMPTY CellMark = iota
# // 	WALL
# // 	PATH
# // )

# // // 3x3 board represented by a 1D array.
# // // Indices on the array:
# // // |0|1|2|
# // // |3|4|5|
# // // |6|7|8|
# // type MazeBoard struct {
# // 	Height int
# // 	Width  int
# // 	Cells  []CellMark
# // }

# // func (m *MazeBoard) String() {

# // }

# // func (m *MazeBoard) GetCell() CellMark {
# // 	return 0
# // }

# // func (m *MazeBoard) SetCell(row, column int) error {
# // 	return nil
# // }

# // func NewMazeGenerator(height, width int, generator GeneratorType) Generator {
# // 	return nil
# // }
