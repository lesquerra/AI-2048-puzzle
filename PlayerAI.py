from random import choices, sample, randint

from BaseAI import BaseAI

import numpy as np

import time
 
class PlayerAI(BaseAI):
    """ Grid class
    
    Args:
        grid: Grid class object with the current state of the puzzle
        alpha: Alpha parameter. Largest value for max across seen children
        beta: Beta parameter. Lowest value for min across seen children
        layer: Tree layer depth
        prevTime: time.clock object indicating the time when the previous move was decided 
        current_tile: Value of the tile to be evaluated
    
    Methods:
        maximize(): Find the move that maximizes the expected tile value
        minimize(): Find the move that minimizes the expected tile value
        evaluateState(): Heuristic function to assign approximate values to nodes in the tree
        isTerminal(): Check if it's the last node in a tree either because the game is over or the maximum search depth has been reached
        isTimeOver(): Check if the maximum decision time has passed
        getMove(): Get the Player AI's next move. Inherited from Base AI
        
    """    
    def __init__(self):
        self.timeLimit = 0.2
        self.defaultProbability = 0.9
        
    def maximize(self, grid, alpha, beta, layer, prevTime):
        """ Find the move that maximizes the expected tile value
        
        Args:
            grid: Grid class object with the current state of the puzzle
            alpha: Alpha parameter. Largest value for max across seen children
            beta: Beta parameter. Lowest value for min across seen children
            layer: Tree layer depth
            prevTime: time.clock object indicating the time when the previous move was decided
                
        Returns: Returns the move expected to maximize the tile value and the value of this tile
        
        """
        max_move, max_tile = None, alpha
            
        if self.isTerminal(grid, layer):
            return max_move, self.evaluateState(grid, max_tile)
     
        moves = grid.getAvailableMoves()
         
        for m in moves:
            
            if self.isTimeOver(prevTime):
                break
            
            new_grid = grid.clone()
            new_grid.move(m)
            _, minmax = self.minimize(new_grid, alpha, beta, layer + 1, prevTime)
                
            if minmax > max_tile:
                max_move, max_tile = m, minmax
            
            if max_tile >= beta:
                break
            
            if max_tile > alpha:
                alpha = max_tile
            
        return max_move, max_tile
    
    def minimize(self, grid, alpha, beta, layer, prevTime):
        """ Find the move that minimizes the expected tile value
        
        Args:
            grid: Grid class object with the current state of the puzzle
            alpha: Alpha parameter. Largest value for max across seen children
            beta: Beta parameter. Lowest value for min across seen children
            layer: Tree layer depth
            prevTime: time.clock object indicating the time when the previous move was decided
                
        Returns: Returns the move expected to minimize the tile value and the value of this tile
        
        """
        min_move, min_tile = None, beta
    
        if self.isTerminal(grid, layer):
            return min_move, self.evaluateState(grid, min_tile)
        
        avail_cells = grid.getAvailableCells()
        rand_cells = sample(avail_cells, k = min(len(avail_cells), 5))
            
        for x, y in rand_cells:
            
            if self.isTimeOver(prevTime):
                break
            
            new_grid = grid.clone()
            new_grid.map[x][y] = choices([2, 4], [self.defaultProbability, 1 - self.defaultProbability])[0]
            _, maxmin = self.maximize(new_grid, alpha, beta, layer + 1, prevTime)
                
            if maxmin < min_tile:
                min_tile = maxmin
                
            if min_tile <= alpha:
                break
            
            if min_tile < beta:
                beta = min_tile
        
        return min_move, min_tile
    
    def evaluateState(self, grid, current_tile):
        """ Heuristic function to assign approximate values to nodes in the tree
        
        Args:
            grid: Grid class object with the current state of the puzzle
            current_tile: Value of the tile to be evaluated
                
        Returns: Returns the expected value of the tree
        
        """
        return 0.2 * np.log2(grid.getMaxTile() - current_tile + 0.0001) + 0.8 * len(grid.getAvailableCells())
    
    def isTerminal(self, grid, layer):
        """ Check if it's the last node in a tree either because the game is over or the maximum search depth has been reached
        
        Args:
            grid: Grid class object with the current state of the puzzle
            layer: Tree layer depth
                
        Returns: Boolean whether the the current grid state is terminal (terminal = True; non-terminal = False)
        
        """
        return not grid.canMove() or layer == self.max_layer
    
    def isTimeOver(self, prevTime):
        """ Check if the maximum decision time has passed
        
        Args:
            prevTime: time.clock object indicating the time when the previous move was decided 
                
        Returns: Boolean whether the the maximum decision time is over (time over = True; still time available = False)
        
        """
        return time.clock() - prevTime >= self.timeLimit

    def getMove(self, grid):
        """ Get the Player AI's next move. Inherited from Base AI
        
        Args:
            grid: Grid class object with the current state of the puzzle
                
        Returns: Returns the optimal player's next move
        
        """
        prevTime = time.clock()
        self.moves = grid.getAvailableMoves()
        self.max_layer = np.round(np.exp(18/(len(grid.getAvailableCells()) + 3) + 1))
        if self.max_layer % 2 == 1:
            self.max_layer -= 1
            
        alpha, beta = 2, 4096
        layer = 1
    
        if self.moves:    
            prevTime = time.clock()
            max_move, max_tile = self.maximize(grid, alpha, beta, layer, prevTime)
            print(time.clock() - prevTime)
            
            if max_move is None:
                max_move = self.moves[randint(0, len(self.moves) - 1)]
        
        return max_move if self.moves else None
