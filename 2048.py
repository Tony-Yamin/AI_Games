# Name: Tony Yamin
# UNI: ty2492

import random
import time
import math
from BaseAI import BaseAI

class IntelligentAgent(BaseAI):
    def __init__(self):
        self.time_limit = 0.2 
        self.start_time = None
        self.depth_limit = 3 

    def getMove(self, grid):
        self.start_time = time.time()
        return self.expectiminimax(grid, "human", float("-inf"), float("inf"), self.depth_limit)[0]
    
    def heuristic(self, grid):
        score = (2 * self.similarity(grid) + 
                4 * self.merges(grid) +
                2 * self.largest_corner_tile_value(grid) + 
                3 * self.ordering(grid) + 
                6 * len(grid.getAvailableCells()) +
                1 * grid.getMaxTile())

        return score
    
    # Check difference in values across adjacent tiles
    def similarity(self, grid):
        n = grid.size
        score = 0

        for row in range(n):
            for col in range(n):
                current_tile = grid.map[row][col]
                if current_tile > 0:
                    if col - 1 >= 0:
                        left_tile = grid.map[row][col - 1]
                        if left_tile > 0:
                            score -= abs(math.log(current_tile, 2) - math.log(left_tile, 2))
                    
                    if row - 1 >= 0:
                        up_tile = grid.map[row - 1][col]
                        if up_tile > 0:
                            score -= abs(math.log(current_tile, 2) - math.log(up_tile, 2))

        return score
    
    # Check increasing/decreasing values of tiles in rows and columns
    def ordering(self, grid):
        n = grid.size
        scores = [0, 0, 0, 0]

        # Right and Left
        for row in range(n):
            for col in range(n):
                if col + 1 < n:
                    current_tile = grid.map[row][col]
                    if current_tile > 0:
                        next_tile = grid.map[row][col + 1]
                        if next_tile > 0:
                            scores[0] += math.log(next_tile, 2) - math.log(current_tile, 2)
                        else:
                            scores[0] += - math.log(current_tile, 2)
                
                if col - 1 >= 0:
                    current_tile = grid.map[row][col]
                    if current_tile > 0:
                        next_tile = grid.map[row][col - 1]
                        if next_tile > 0:
                            scores[1] += math.log(next_tile, 2) - math.log(current_tile, 2)
                        else:
                            scores[1] += - math.log(current_tile, 2)
        
        # Up and Down
        for row in range(n):
            for col in range(n):
                if row + 1 < n:
                    current_tile = grid.map[row][col]
                    if current_tile > 0:
                        next_tile = grid.map[row + 1][col]
                        if next_tile > 0:
                            scores[2] += math.log(next_tile, 2) - math.log(current_tile, 2)
                        else:
                            scores[2] += - math.log(current_tile, 2)
                
                if row - 1 >= 0:
                    current_tile = grid.map[row][col]
                    if current_tile > 0:
                        next_tile = grid.map[row -1 ][col]
                        if next_tile > 0:
                            scores[3] += math.log(next_tile, 2) - math.log(current_tile, 2)
                        else:
                            scores[3] += - math.log(current_tile, 2)

        return max(scores[0], scores[1], scores[2], scores[3])
                    
    # Check possible merges between tiles
    def merges(self, grid):
        n = grid.size
        score = 0

        # Check rows
        for row in range(n):
            row_tiles = []
            for col in range(n):
                if grid.map[row][col] > 0:
                    row_tiles.append(grid.map[row][col])
            
            col = 0
            while col < len(row_tiles) - 1:
                if row_tiles[col] == row_tiles[col + 1]:
                    score += 1
                    col += 1
                col += 1
        
        # Check columns
        for col in range(n):
            col_tiles = []
            for row in range(n):
                if grid.map[row][col] > 0:
                    col_tiles.append(grid.map[row][col])
            
            row = 0
            while row < len(col_tiles) - 1:
                if col_tiles[row] == col_tiles[row + 1]:
                    score += 1
                    row += 1
                row += 1
        
        return score
    
    # Find max value of corner tile
    def largest_corner_tile_value(self, grid):
        n = grid.size
        max_tile = grid.getMaxTile()

        if max_tile == grid.map[0][0] or max_tile == grid.map[0][n-1] or max_tile == grid.map[n-1][0] or max_tile == grid.map[n-1][n-1]:
            return math.log(max_tile, 2)
        
        return 0


    def expectiminimax(self, grid, player, alpha, beta, depth):
        # Terminal State
        if time.time() - self.start_time > self.time_limit or depth == 0 or not grid.canMove():
            return -1, self.heuristic(grid)
            
        # Human Player
        if player == "human":
            max_utility = float("-inf")
            for move, new_grid in grid.getAvailableMoves():
                utility = self.expectiminimax(new_grid, "AI", alpha, beta, depth - 1)[1]

                if utility > max_utility:
                    max_child = move
                    max_utility = utility
                
                if max_utility > alpha:
                    alpha = max_utility
                
                if max_utility >= beta:
                    break
            
            return max_child, max_utility
        
        # AI
        elif player == "AI":
            expected_utility = 0
            min_utility = float("inf")
            for cell in grid.getAvailableCells():
                for tile, probability in [(2, 0.9), (4, 0.1)]:
                    new_grid = grid.clone()
                    new_grid.setCellValue(cell, tile)

                    utility = self.expectiminimax(new_grid, "human", alpha, beta, depth - 1)[1]
                    expected_utility += (probability * utility) 

                    if expected_utility < min_utility:
                        min_utility = expected_utility
                    
                    if min_utility < beta:
                        beta = min_utility
                    
                    if min_utility <= alpha:
                        break
            
            return -1, min_utility




