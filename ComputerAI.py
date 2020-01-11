from random import randint
from BaseAI import BaseAI

class ComputerAI(BaseAI):
    """ Computer AI class
    
    Args:
        grid: Grid class object with the current state of the puzzle
    
    Methods:
        getMove(): Get the Computer AI's next move. Inherited from Base AI

    """
    def getMove(self, grid):
        """ Get the Computer AI's next move
        
        Args:
            grid: Grid class object with the current state of the puzzle
            
        Returns: Randomly selected computer's next move
        
        """
        cells = grid.getAvailableCells()

        return cells[randint(0, len(cells) - 1)] if cells else None
