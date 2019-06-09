import sys
import time

class Board:
    """This class is designed to encapsulate key functionality for our Checkers AI project including
    functions to initialize the board as well, to carry out moves, coordinate turns, and print the current
    state of the game board"""

    def __init__(self):
        """Places all the checker pieces in the appropriate starting positions"""

        self.boardState = []        
        for y in range(8):
            newRow = []
            for x in range(8):                
                if (x < 3) and (((y % 2 == 0) and (x == 1)) or ((y % 2 == 1) and (x % 2 == 0))):
                    newRow.append(' R')
                elif (x >= 5) and (((y % 2 == 0) and (x % 2 == 1)) or ((y % 2 == 1) and (x % 2 == 0))):
                    newRow.append(' B')
                else:
                    newRow.append(' -')
            self.boardState.append(newRow)
    
    
    def print_board(self):
        """A simple function designed to print out the current state of the board"""

        time.sleep(1)
        output = []
        output.append('___________________')        
        for y in range(8):
            newRow = []
            for x in range(8):                
                if x == 0:
                    newRow.append('|')
                    newRow.append(self.boardState[x][y])                
                elif (x % 8 == 7):
                    newRow.append(self.boardState[x][y])
                    newRow.append(' |')                              
                else: newRow.append(self.boardState[x][y])                                                            
            if y == 7:
                newRow.append('\n___________________')
            output.append(newRow)
                
        for row in output:
            print(*row, sep='')
                
    def move (self, plyrColor, pieceToMove, newLocation):
        """A Simple recursive function that takes a tuple for the current position
        of the piece that is to be moved, and a list of tuples, newLocation that
        holds the the x,y coordinates and the current color on the tile for each
        individual jump in the case that enemy pieces are captured. plyrColor is a simple
        string that uses a leading whitespace followed by R, for the red team, B, for the 
        black team, and - for an empty tile"""

        #print ("It's the", plyrColor, " team's turn to make a move!\n")

        capturePiece = False
        if len(newLocation) == 0: return []

        else:            
            print("____________________________________________________")
            print ("It's the", plyrColor, " team's turn to make a move!\n")
            nextMove = newLocation[0]
        
        (i,j) = (nextMove[0], nextMove[1])
        for y in range(8):
            for x in range(8):            
                if (x == i) and (y == j):
                    color = self.boardState[x][y]
                    if (color != ' -') and (color != plyrColor):
                        capturePiece = True
                        self.boardState[x][y] = plyrColor
                        (l, m) = (pieceToMove[0], pieceToMove[1])
                        self.boardState[l][m] = ' -'
                    
                    elif (color == ' -'):
                        self.boardState[x][y] = plyrColor
                        (l, m) = (pieceToMove[0], pieceToMove[1])
                        self.boardState[l][m] = ' -'        
        self.print_board()
        if capturePiece == True: print ("The", plyrColor, " team just captured a", color, " player piece!\n")
                        
        if self.gameWon() == True:
            return []
        else:
            self.move(plyrColor, (nextMove[0], nextMove[1], plyrColor), newLocation[1:])

    def gameWon(self):
        """A simple helper function that counts the number of spaces occupied by each team
        and if one team has no pieces occupying the board, then the True is returned,
        otherwise False is returned"""

        if self.countBlack() == 0:
            print("The red team is victorious!!\n\n")
            return True
        
        elif self.countRed() == 0:
            print("The black team is victorious!!\n\n")
            return True

        else: return False
    
    def countRed(self):
        """Helper function for gameWon and for UI elements"""
        redCount = 0
        for y in range(8):
            for x in range(8):
                if self.boardState[x][y] == ' R': redCount = redCount + 1
        return redCount
    
    def countBlack(self):
        """Helper function for gameWon and for UI elements"""
        blackCount = 0
        for y in range(8):
            for x in range(8):
                if self.boardState[x][y] == ' B': blackCount = blackCount + 1
        return blackCount

"""class AI_PLAYER():
    def __init__(self,):"""

def main():
   newGame = Board()
   newGame.print_board()
   
   newGame.move(' R', (1, 2,' R'), [(2, 3,' -')])
   # Simple test move 1
   time.sleep(2)

   newGame.move(' B', (6, 5,' R'), [(5, 4,' -')])
   # Simple test move 1

   time.sleep(2)   

   newGame.move(' R', (2, 3,' R'), [(3, 4,' -')])
   # Simple test move 1
   time.sleep(2)

   newGame.move(' B', (2, 5,' R'), [(3, 4,' -'), (4, 3,' -')])
   # Capture move test 1

   time.sleep(100)

main()