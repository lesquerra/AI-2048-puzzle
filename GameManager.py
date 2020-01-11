from Grid       import Grid
from ComputerAI import ComputerAI
from PlayerAI   import PlayerAI
from Displayer  import Displayer
from random     import randint
import time

# Initialize static parameters
defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

# Time limit before losing
timeLimit = 0.2
allowance = 0.05

class GameManager:
    """ Game Manager class
    
    Agrs:
        size: Puzzle grid side size
        ComputerAI: ComputerAI class object running the computer's moves
        PlayerAI: PlayerAI class object running the player's moves optimizing the implemented heuristics
        displayer: Displayer class object allowing the Game Manager to display the current state of the game 
        currTime: time.clock object indicating the current time at each move
    
    Methods:
        setComputerAI(): Set ComputerAI object
        setPlayerAI(): Set PlayerAI object
        setDisplayer(): Set Displayer object
        updateAlarm(): Check time consumed in the decision-making process doesn't exceed time limit
        start(): Start running the game
        isGameOver(): Check if the game is over, not allowing the player to perform any further moves
        getNewTileValue(): Get the value of the computer's new tile to be inserted
        insertRandomTile(): Insert the computer's new tile in a random available cell

    """
    def __init__(self, size = 4):
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles  = defaultInitialTiles
        self.computerAI = None
        self.playerAI   = None
        self.displayer  = None
        self.over       = False

    def setComputerAI(self, computerAI):
        """ Set ComputerAI object """
        self.computerAI = computerAI

    def setPlayerAI(self, playerAI):
        """ Set PlayerAI object """
        self.playerAI = playerAI

    def setDisplayer(self, displayer):
        """ Set Displayer object """
        self.displayer = displayer

    def updateAlarm(self, currTime):
        """ Check time consumed in the decision-making process doesn't exceed time limit 
        
        Args:
            currTime: time.clock object indicating the current time at each move
                
        """
        if currTime - self.prevTime > timeLimit + allowance:
            self.over = True
        else:
            while time.clock() - self.prevTime < timeLimit + allowance:
                pass

            self.prevTime = time.clock()

    def start(self):
        """ Start running the game """
        for i in range(self.initTiles):
            self.insertRandomTile()

        self.displayer.display(self.grid)

        # Player AI Goes First
        turn = PLAYER_TURN
        maxTile = 0

        self.prevTime = time.clock()

        while not self.isGameOver() and not self.over:
            # Copy to Ensure AI Cannot Change the Real Grid to Cheat
            gridCopy = self.grid.clone()

            move = None

            if turn == PLAYER_TURN:
                print("Player's Turn:", end="")
                move = self.playerAI.getMove(gridCopy)
                print(actionDic[move])

                # Validate Move
                if move != None and move >= 0 and move < 4:
                    if self.grid.canMove([move]):
                        self.grid.move(move)

                        # Update maxTile
                        maxTile = self.grid.getMaxTile()
                    else:
                        print("Invalid PlayerAI Move")
                        self.over = True
                else:
                    print("Invalid PlayerAI Move - 1")
                    self.over = True
            else:
                print("Computer's turn:")
                move = self.computerAI.getMove(gridCopy)

                # Validate Move
                if move and self.grid.canInsert(move):
                    self.grid.setCellValue(move, self.getNewTileValue())
                else:
                    print("Invalid Computer AI Move")
                    self.over = True

            if not self.over:
                self.displayer.display(self.grid)
            
            print(self.over)
            # Exceeding the Time Allotted for Any Turn Terminates the Game
            self.updateAlarm(time.clock())

            turn = 1 - turn
            print(self.over)
        print(maxTile)

    def isGameOver(self):
        """ Check if the game is over, not allowing the player to perform any further moves 
        
        Returns: Boolean whether the game is over or not
            
        """
        return not self.grid.canMove()

    def getNewTileValue(self):
        """ Get the value of the computer's new tile to be inserted 
        
        Returns: Value of the computer's new tile to be inserted 
        
        """
        if randint(0,99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1];

    def insertRandomTile(self):
        """ Insert the computer's new tile in a random available cell """
        tileValue = self.getNewTileValue()
        cells = self.grid.getAvailableCells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.setCellValue(cell, tileValue)

def main():
    # Initialize main classes
    gameManager = GameManager()
    playerAI  	= PlayerAI()
    computerAI  = ComputerAI()
    displayer 	= Displayer()

    # Initial Game Manager set-up
    gameManager.setDisplayer(displayer)
    gameManager.setPlayerAI(playerAI)
    gameManager.setComputerAI(computerAI)
    
    # Start running the game
    gameManager.start()

if __name__ == '__main__':
    main()
