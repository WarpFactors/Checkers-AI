import sys
import time
import pygame

class Board:
    """This class is designed to encapsulate key functionality for our Checkers AI project including
    functions to initialize the board as well, to carry out moves, coordinate turns, and print the current
    state of the game board"""

    def __init__(self):
        """Places all the checker pieces in the appropriate starting positions"""
        
        pygame.init()
        self.running = True
        self.gameDisplay = PyGameBoard()
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
            self.gameDisplay.updateGame(self.reduceDimsArr())
        time.sleep(4)

    def reduceDimsArr(self):
        newArray = []
        for x in range(len(self.boardState)):
            for y in range(len(self.boardState[x])):
                newArray.append((x,y,self.boardState[x][y]))
        return newArray

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
                
    def move(self, plyrColor, pieceToMove, newLocation):
        """A Simple recursive function that takes a tuple for the current position
        of the piece that is to be moved, and a list of tuples, newLocation that
        holds the the x,y coordinates and the current color on the tile for each
        individual jump in the case that enemy pieces are captured. plyrColor is a simple
        string that uses a leading whitespace followed by R, for the red team, B, for the 
        black team, and - for an empty tile"""

        #print ("It's the", plyrColor, " team's turn to make a move!\n")

        capturePiece = False
        if len(newLocation) == 0: return []

        # Capture useful info from tile tuple of (x, y, color) info
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

        self.gameDisplay.updateGame(self.reduceDimsArr())

        #self.print_board()        
        #if capturePiece == True: print ("The", plyrColor, " team just captured a", color, " player piece!\n")
                                
        if self.gameWon() == True:
            pygame.quit()
            return []
        
        else:
            self.move(plyrColor, (nextMove[0], nextMove[1], plyrColor), newLocation[1:])

    def gameWon(self):
        """A simple helper function that counts the number of spaces occupied by each team
        and if one team has no pieces occupying the board, then the True is returned,
        otherwise False is returned"""

        if self.countBlue() == 0:
            print("The red team is victorious!!\n\n")
            return True
        
        elif self.countRed() == 0:
            print("The blue team is victorious!!\n\n")
            return True

        else: return False
    
    def countRed(self):
        """Helper function for gameWon and for UI elements"""
        redCount = 0
        for y in range(8):
            for x in range(8):
                if self.boardState[x][y] == ' R': redCount = redCount + 1
        return redCount
    
    def countBlue(self):
        """Helper function for gameWon and for UI elements"""
        blueCount = 0
        for y in range(8):
            for x in range(8):
                if self.boardState[x][y] == ' B': blueCount = blueCount + 1
        return blueCount

    """def findTargetSq(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = pygame.mouse.get_pos()
                trgX = int((mouseX + 2) / PyGameBoard.size)
                trgY = int((mouseY + 2) / PyGameBoard.size)"""
                

class PyGameBoard:

    def __init__(self):
        # Define color values
        self.white, self.black, self.red, self.blue = (255,255,255), (0,0,0), (255,0,0), (0,0,255)
        
        
        #self.font = pygame.font.Font('freesansbold.ttf', 24)

        # Square side length & number of tiles per row on the board
        self.size = 60
        self.boardLength = 8

        # Define PyGame window dimensions
        self.windowDims = (self.size * (self.boardLength + 4))
        self.boardDims = (self.size * (self.boardLength + 2))

        self.mainDisplay = pygame.display.set_mode((self.windowDims, self.windowDims))
        self.gameDisplay = pygame.display.set_mode((self.boardDims, self.boardDims))
        #self.gameDisplay.scroll = (int(self.windowDims / 2), int(self.windowDims / 2))
        
        self.drawCheckerBoard()
        


    def reduceDimsArr(self):
        newArray = []
        for x in range(len(self.boardState)):
            for y in range(len(self.boardState[x])):
                newArray.append((x,y,self.boardState[x][y]))
        return newArray

    def drawCheckerBoard(self, STR = 'test'):
        self.gameDisplay.fill(self.white)
        self.mainDisplay.fill(self.white)

        currentTile = 0
        for i in range(1, self.boardLength + 1):
            for z in range(1, self.boardLength + 1):
                # Use loop val to determine color of square
                if currentTile % 2 == 0:
                    pygame.draw.rect(self.gameDisplay, self.white,[self.size*z,self.size*i,self.size,self.size])
                else:
                    pygame.draw.rect(self.gameDisplay, self.black, [self.size*z, self.size*i, self.size, self.size])
                currentTile +=1
            #since theres an even number of squares go back one value
            currentTile-=1
            
        #Add a nice border
        pygame.draw.rect(self.gameDisplay, self.black, [self.size, self.size, self.boardLength*self.size, self.boardLength*self.size], 1)        
        

        """ text = self.font.render(STR, True, self.black, self.white)
        textBox = text.get_rect()
        textBox.center = (int(self.boardDims / 2), int(self.windowDims - (2*self.size)))
        
        self.mainDisplay.blit(text, textBox)"""
        self.mainDisplay.blit(self.gameDisplay,(int(self.windowDims - (2*self.size)), int(self.windowDims - (2*self.size))))        

        
        pygame.display.update()

    def updateGame(self, pieceLocations):
        """ This function places the players pieces onto the checkerboard 
        using an array of tuples taken from the Board class."""

        self.drawCheckerBoard()

        # Use c to determine color of checker piece to draw
        for (x, y, c) in pieceLocations:
            if c != ' -':
                if c == ' R': color = self.red
                else: color = self.blue
                pygame.draw.circle(self.gameDisplay, color, (int(((self.size * (x + 2)) - (self.size / 2))), int(((self.size * (y + 2)) - (self.size / 2)))), int((self.size*0.5)), 8)
        
        pygame.display.update()

def main():
    
    newGame = Board()
           
    newGame.move(' R', (1, 2,' R'), [(2, 3,' -')])
    time.sleep(2)
    newGame.move(' B', (6, 5,' R'), [(5, 4,' -')])       
    time.sleep(2)   
    newGame.move(' R', (2, 3,' R'), [(3, 4,' -')])    
    time.sleep(2)
    newGame.move(' B', (2, 5,' R'), [(3, 4,' -'), (4, 3,' -')])
    time.sleep(10)

    pygame.quit()
main()