from copy import deepcopy

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)

class Grid:
    """ Grid class
    
    Args:
        size: Puzzle grid side size
        pos: Selected cell's grid position
        value: Value for the computer's new tile to be inserted
        dir: Selected move direction
        down: Boolean. Player's move is down (yes, down = 1; no, up = 0)
        right: Boolean. Player's move is to the right (yes, right = 1; no, left = 0)
        cells: Vector containing occupied cell values in the current puzzle state
        dirs: Vector defining possible moves in the current puzzle state
    
    Methods:
        clone(): Make a deepcopy of the grid in the current puzzle state
        insertTile(): Insert a tile in an empty cell
        setCellValue(): Set the new value for the selected cell
        getAvailableCells(): Get a list of all empty cells
        getMaxTile(): Return the tile with maximum value
        canInsert(): Check if it is possible to insert a tile in the specified position
        move(): Move the grid
        moveUD(): Move the grid UP or DOWN
        moveLR(): Move the grid LEFT or RIGHT
        merge(): Merge the tiles when applying specified move
        canMove(): Check if the grid has available moves in the current puzzle state
        getAvailableMoves(): Get the available moves in the current puzzle state
        crossBound(): Check that the specified position is within the grid (size) limits
        getCellValue(): Get the current value of the tile in the specified position
        
    """
    def __init__(self, size = 4):
        self.size = size
        self.map = [[0] * self.size for i in range(self.size)]

    def clone(self):
        """ Make a deepcopy of the grid in the current puzzle state 
        
        Returns: Copy of th current grid class object 
        
        """
        gridCopy = Grid()
        gridCopy.map = deepcopy(self.map)
        gridCopy.size = self.size

        return gridCopy

    def insertTile(self, pos, value):
        """ Insert a tile in an empty cell 
        
        Args:
            pos: Selected random position for the computer's new tile to be inserted
            value: Value for the computer's new tile to be inserted
            
        """
        self.setCellValue(pos, value)

    def setCellValue(self, pos, value):
        """ Set the new value for the selected cell 
        
        Args:
            pos: Selected random position for the computer's new tile to be inserted
            value: Value for the computer's new tile to be inserted
            
        """
        self.map[pos[0]][pos[1]] = value

    def getAvailableCells(self):
        """ Get a list of all empty cells 
        
        Returns: List of all empty cells
        
        """
        cells = []

        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y] == 0:
                    cells.append((x,y))

        return cells

    def getMaxTile(self):
        """ Return the tile with maximum value 
        
        Returns: Value of the highest tile in the current puzzle state
        
        """
        maxTile = 0

        for x in range(self.size):
            for y in range(self.size):
                maxTile = max(maxTile, self.map[x][y])

        return maxTile

    def canInsert(self, pos):
        """ Check if it is possible to insert a tile in the specified position 
        
        Args:
            pos: Selected random position for the computer's new tile to be inserted
            
        Returns: Boolean whether specified position is available (available = True; unavailable = False)
            
        """
        return self.getCellValue(pos) == 0

    def move(self, dir):
        """ Move the grid 
        
        Args:
            dir: Selected move direction
            
        Returns: Updated grid after moving it in the specified direction
            
        """
        dir = int(dir)

        if dir == UP:
            return self.moveUD(False)
        if dir == DOWN:
            return self.moveUD(True)
        if dir == LEFT:
            return self.moveLR(False)
        if dir == RIGHT:
            return self.moveLR(True)

    def moveUD(self, down):
        """ Move the grid UP or DOWN 
        
        Args:
            down: Boolean. Player's move is down (yes, down = 1; no, up = 0)
            
        Returns: Boolean whether the grid has been successfully moved or not
         
        """
        r = range(self.size -1, -1, -1) if down else range(self.size)

        moved = False

        for j in range(self.size):
            cells = []

            for i in r:
                cell = self.map[i][j]

                if cell != 0:
                    cells.append(cell)

            self.merge(cells)

            for i in r:
                value = cells.pop(0) if cells else 0

                if self.map[i][j] != value:
                    moved = True

                self.map[i][j] = value

        return moved

    def moveLR(self, right):
        """ Move the grid LEFT or RIGHT 
        
        Args:
            right: Boolean. Player's move is to the right (yes, right = 1; no, left = 0)
            
        Returns: Boolean whether the grid has been successfully moved or not
         
        """
        r = range(self.size - 1, -1, -1) if right else range(self.size)

        moved = False

        for i in range(self.size):
            cells = []

            for j in r:
                cell = self.map[i][j]

                if cell != 0:
                    cells.append(cell)

            self.merge(cells)

            for j in r:
                value = cells.pop(0) if cells else 0

                if self.map[i][j] != value:
                    moved = True

                self.map[i][j] = value

        return moved

    def merge(self, cells):
        """ Merge the tiles when applying specified move 
        
        Args:
            cells: Vector containing occupied cell values in the current puzzle state
         
        """
        if len(cells) <= 1:
            return cells

        i = 0

        while i < len(cells) - 1:
            if cells[i] == cells[i+1]:
                cells[i] *= 2

                del cells[i+1]

            i += 1

    def canMove(self, dirs = vecIndex):
        """ Check if the grid has available moves in the current puzzle state 
        
        Args:
            dirs: Vector defining possible moves in the current puzzle state
        
        Returns: Boolean whether there are available moves in the current puzzle state
                
        """
        # Init Moves to be Checked
        checkingMoves = set(dirs)

        for x in range(self.size):
            for y in range(self.size):

                # If Current Cell is Filled
                if self.map[x][y]:

                    # Look Ajacent Cell Value
                    for i in checkingMoves:
                        move = directionVectors[i]

                        adjCellValue = self.getCellValue((x + move[0], y + move[1]))

                        # If Value is the Same or Adjacent Cell is Empty
                        if adjCellValue == self.map[x][y] or adjCellValue == 0:
                            return True

                # Else if Current Cell is Empty
                elif self.map[x][y] == 0:
                    return True

        return False

    def getAvailableMoves(self, dirs = vecIndex):
        """ Get the available moves in the current puzzle state 
        
        Args:
            dirs: Vector defining possible moves in the current puzzle state

        Returns: List of available moves in the current puzzle state
        
        """
        availableMoves = []

        for x in dirs:
            gridCopy = self.clone()

            if gridCopy.move(x):
                availableMoves.append(x)

        return availableMoves

    def crossBound(self, pos):
        """ Check that the specified position is within the grid (size) limits 
        
        Args:
            pos: Selected cell's grid position

        Returns: Boolean whether specified position is within the grid (size) limits
         
        """
        return pos[0] < 0 or pos[0] >= self.size or pos[1] < 0 or pos[1] >= self.size

    def getCellValue(self, pos):
        """ Get the current value of the tile in the specified position 
        
        Args:
            pos: Selected cell's grid position
        
        Returns: Value of the tile in the specified position 
         
        """
        if not self.crossBound(pos):
            return self.map[pos[0]][pos[1]]
        else:
            return None

if __name__ == '__main__':
    g = Grid()
    g.map[0][0] = 2
    g.map[1][0] = 2
    g.map[3][0] = 4

    while True:
        for i in g.map:
            print(i)

        print(g.getAvailableMoves())

        v = input()

        g.move(v)
