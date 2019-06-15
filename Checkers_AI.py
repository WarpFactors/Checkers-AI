import sys
import time
class Board:
    """This class is designed to encapsulate key functionality for our Checkers AI project including
    functions to initialize the board as well as, to carry out moves, coordinate turns, and print the current
    state of the game board"""



    #AI RETURNS: [(strtXPos, strtYPos), [(mv1X, mv1Y), ...]]
    #boardState = [x][y] = Color


    # Each killed enemy = 5pt
    # vulnerable = -1
    # basic jump = 2
    # kill kill jump vulnerable = 6 ->

    



    def __init__(self):
        """Places all the checker pieces in the appropriate starting positions"""        
        
        self.running = True
        self.boardState = []        
        self.colorsAI = [' b', ' B']
        self.colorsPlyr = [' r', ' R']        
        self.turnCount = 1
        self.initBoardState()
    


    def initBoardState(self):
        """Simple helper function that creates the formatted 2D array used to
        maintain the state of each tile on the checkerboard and for printing to the
        terminal"""
        for y in range(8):
            newRow = []
            for x in range(8):                
                if (x < 3) and (((y % 2 == 0) and (x == 1)) or ((y % 2 == 1) and (x % 2 == 0))):
                    newRow.append(self.colorsPlyr[0])
                elif (x >= 5) and (((y % 2 == 0) and (x % 2 == 1)) or ((y % 2 == 1) and (x % 2 == 0))):
                    newRow.append(self.colorsAI[0])
                else:
                    newRow.append(' -')
            self.boardState.append(newRow)
        self.print_board()



    def validCoords(self, start):
        """Helper function that returns True if the x and y values are both
        between 0 and 8"""
        x, y = start
        if (x >= 0) and (x < 8) and (y >= 0) and (y < 8):
            return True
        return False



    def verifyTargetColor(self, start, finish, onlyCaptures = False):
        """This helper function takes in start and finish tuples formatted
        as (xCord, yCord) and the color as a string of a whitespace
        if onlyCaptures is True, then don't return True unless finish
        tile is occupied by enemy checker piece"""
        if ((self.validCoords(start) == False) or (self.validCoords(finish) == False)): return False        
        else: trgtColor = self.boardState[finish[0]][finish[1]]

        if ((onlyCaptures == True) and (trgtColor != ' -') and (trgtColor not in self.colorsPlyr)): return True
        elif ((onlyCaptures == False) and (trgtColor not in self.colorsPlyr)): return True
        else: return False
    
    
    def adjTileEnemies(self, start):
        """Designed for specific use by human players. If the entered tuple
        of x, y coordinates has a neighboring tile occupied by an enemy piece
        this function returns True, otherwise, False is returned."""

        x, y = start
        currColor = self.boardState[x][y]
        if (currColor == ' R'):
            if (self.validCoords((x-1,y-1)) == True):
                if self.boardState[x-1][y-1] in self.colorsAI: 
                    if (self.validCoords((x-2, y-2)) == True): return True
            elif (self.validCoords((x+1,y-1)) == True):
                if self.boardState[x+1][y-1] in self.colorsAI:
                    if (self.validCoords((x+2, y-2)) == True): return True

        elif (self.validCoords((x-1,y+1)) == True):
            if self.boardState[x-1][y+1] in self.colorsAI:
                if (self.validCoords((x-2, y+2)) == True): return True

        elif (self.validCoords((x+1,y+1)) == True):
            if self.boardState[x+1][y+1] in self.colorsAI:
                if (self.validCoords((x+2, y+2)) == True): return True

        else: return False



    def getYFactor(self, checkerPiece):
        """Takes (xCord, yCord) as checkerPiece and retrieves what change
        in y position is possible for the piece.
        if 0 is returned, then the piece is a king and can move up or down"""
        
        curClr = self.boardState[checkerPiece[0]][checkerPiece[1]]
        if curClr == self.colorsPlyr[0]: return -1
        elif curClr == self.colorsAI[0]: return 1
        else: return 0



    def collectCheckers(self, onlyKings = 0, turnMod = 0):
        """Helper function to collect and append all checkers and their coordinates
        to a list of pieces owned by the player currently taking their turn and returns
        checkers in the reduced self.boardState format: [(xCord, yCord, color), ...]
        The optional argument onlyKings, will be used to slice the array of team colors
        to exclude normal checkers when its equal to 0. The optional argument turnMod, 
        when equal to 1, returns only the opponents pieces"""
        
        playerPcs = []        
        if (self.turnCount + turnMod) % 2 == 0:
            validClrs = self.colorsAI[(0 + onlyKings):]
        else:
            validClrs = self.colorsPlyr[(0 + onlyKings):]
            
        for y, x, c in self.reduceDimsArr():
            if c in validClrs:
                playerPcs.append((y, x, c))
                
        return playerPcs


    def validStrt(self, start):
        """Helper function to determine if any valid moves exist for the selected 
        checker piece. If a valid move exists then True, else False"""        

        validYDir = self.getYFactor(start)
        y, x = start
        #print(start)
        strtColor = self.boardState[y][x]
        crowned = False
        if strtColor == ' R':
            crowned = True

        queue = []
        if crowned == False:
            forwardLeft = (y - 1, x + 1)
            queue.append(forwardLeft)
        
            forwardRight = (y + 1, x + 1)      
            queue.append(forwardRight)            

        else:
            forwardLeft = (y - 1, x + 1)
            queue.append(forwardLeft)
        
            forwardRight = (y + 1, x + 1)      
            queue.append(forwardRight)                                 
            
            backwardLeft = (y - 1, x - 1)
            queue.append(forwardLeft)
        
            backwardRight = (y + 1, x - 1)            
            queue.append(forwardRight)
        
        for (a, b) in queue:
            if ((self.validCoords((a,b)) == True) and (self.boardState[a][b] not in self.colorsPlyr)):
                return True
        return False

   
    
    def collectPosStart(self):
        startPosLocs = self.collectCheckers(0, 0)
        enemyColors = []
        checkersCanCap = []
        checkersValid = []
        mustAttack = False

        for x,y,c in startPosLocs:
            #print("In collect pass: ", x, y, c)
            if self.validStrt((x, y)) == True:
                if (mustAttack == True) or (self.adjTileEnemies((x, y)) == True):
                    print(self.adjTileEnemies((x,y)))
                    checkersCanCap.append((x,y,c))
                    checkersValid.append((x,y,c))
                    mustAttack = True
                    
                else:                    
                    checkersValid.append((x,y,c))
        
        #print(self.collectCheckers(0,0))
        if mustAttack == False:
            print("\n\nAVAILABLE CHECKERS: ")
            for checker in checkersValid:            
                print(*checker, sep=' ')            
            return checkersValid

        else:
            print("\n\nAVAILABLE CHECKERS: ")
            for checker in checkersCanCap:
                print(*checker, sep=' ')
            return checkersCanCap
                    


    def collectPosTargets(self, startChecker, onlyCaptures = False):
        x, y, plyrColor = startChecker
        crowned = False
        if plyrColor == ' R': crowned = True

        validTrgs = []
        queue = []        
        
        if crowned == False:
            forwardLeft = (x - 1, y + 1)
            if (self.validCoords(forwardLeft) == True):
                queue.append(forwardLeft)
        
            forwardRight = (x + 1, y + 1)      
            if (self.validCoords(forwardRight) == True):
                queue.append(forwardRight)            

        else:
            forwardLeft = (x - 1, y + 1)
            if (self.validCoords(forwardLeft) == True):
                queue.append(forwardLeft)
        
            forwardRight = (x + 1, y + 1)      
            if (self.validCoords(forwardRight) == True):
                queue.append(forwardRight)                                 
            
            backwardLeft = (x - 1, y - 1)
            if (self.validCoords(backwardLeft) == True):
                queue.append(backwardLeft)
        
            backwardRight = (x + 1, y - 1)            
            if (self.validCoords(backwardRight) == True):
                queue.append(backwardRight)        
        print(queue)
    
        for trgt in queue:
            if (self.verifyTargetColor((x, y), (trgt[0], trgt[1]), onlyCaptures) == True):                
                validTrgs.append((trgt[0], trgt[1]))
        
        print("\nAVAILABLE TARGETS: ")
        for option in validTrgs:
            print(*option, sep=' ')
        return validTrgs



    def reduceDimsArr(self):
        """Helper function that takes the 2D array used to represent the state of the
        board and converts it into a list of 3n Tuples (xCord, yCord, Color)"""

        newArray = []
        for x in range(len(self.boardState)):
            for y in range(len(self.boardState[x])):
                newArray.append((x,y,self.boardState[x][y]))
        return newArray



    def gameWon(self):
        """A simple helper function that counts the number of spaces occupied by each team
        and if one team has no pieces occupying the board, then the True is returned,
        otherwise False is returned"""

        blueCount = 0
        for y in range(8):
            for x in range(8):
                if (self.boardState[y][x] == ' b') or (self.boardState[y][x] == ' B'): blueCount = blueCount + 1

        if blueCount == 0:
            print("The red team has won in ", self.turnCount, " turns\n\n")            
            self.running = False
            return True
        
        redCount = 0
        for y in range(8):
            for x in range(8):
                if (self.boardState[y][x] == ' r') or (self.boardState[y][x] == ' R'): redCount = redCount + 1
        if redCount == 0:
            print("The AI player has won in ", self.turnCount, " turns\n\n")
            print("Clearly robots are better, duhhhh!\n\n")
            self.running = False
            return True

        else: return False



    def print_board(self):
        """A simple function designed to print out the current state of the board
        This function also indexes each tile along the top and left sides to aid
        in finding proper coordinates"""

        time.sleep(1)
        output = []
        output.append('    0 1 2 3 4 5 6 7')
        output.append('  ___________________')        
        for y in range(8):
            newRow = []
            for x in range(8):                
                if x == 0:
                    newRow.append(y)
                    newRow.append(' |')
                    newRow.append(self.boardState[x][y])                
                elif (x % 8 == 7):
                    newRow.append(self.boardState[x][y])
                    newRow.append(' |')                              
                else: newRow.append(self.boardState[x][y])                                                            
            if y == 7: 
                newRow.append('\n  ___________________\n')
            output.append(newRow)
                
        for row in output:
            print(*row, sep='')



    def move(self, plyrColor, pieceToMove, newLocation):
        """A Simple recursive function that takes a tuple for the current position
        of the piece that is to be moved, and a list of tuples, newLocation that
        holds the the x,y coordinates and the current color on the tile for each
        individual jump in the case that enemy pieces are captured. plyrColor is a simple
        string that uses a leading whitespace followed by R or r, for the red team, 
        and B or b, for the blue team and - for an empty tile.
        black team, and - for an empty tile"""

        cappedChker = False
        if len(newLocation) == 0: return
        
        #Capture useful info from tile tuple of (x, y, color) info
        nextMove = newLocation[0]
        (x, y) = (pieceToMove[0], pieceToMove[1])
        (i, j) = (nextMove[0], nextMove[1])
        
        if self.boardState[x][y] in self.colorsAI: plyClrs = self.colorsAI
        else: plyClrs = self.colorsPlyr
        self.boardState[x][y] = ' -'
                
        if (self.boardState[i][j] not in plyClrs) and (self.boardState[i][j] != ' -'):
            # This occurs if jumping a piece and sets the game to skip representing
            # the intermediate jump onto the opponent checker piece

            print("Capture detected in move()\n\n")
            cappedChkr = True
            deltaX = i-x
            deltaY = j-y
            self.boardState[i][j] = ' -'
            #print("Resulting change in x, y: ", deltaX, ", ", deltaY)
            i = x + 2*deltaX
            j = y + 2*deltaY            

        if (plyrColor == ' r') and (j == 7):
            plyrColor = ' R'

        elif (plyrColor == ' b') and (j == 0):
            plyrColor = ' B'
        
        self.boardState[i][j] = plyrColor
        self.print_board()
        
        if self.gameWon() == True: return        
        elif cappedChker == True: self.move(plyrColor, newLocation[1], newLocation[2:])
        elif len(newLocation) > 1: self.move(plyrColor, newLocation[0], newLocation[1:])
        else: return



    def playGame(self):
        while self.running == True:
            if self.turnCount % 2 == 0: plyrColors = [' b', ' B']
            else: plyrColors = [' r', ' R']
            
            gotInput = False
            gotStrt = False
            gotTrgt = False
            capPiece = False
            trgtPass = 0
            moveList = []
            color = ''

            while gotInput == False:
                
                if ' R' in plyrColors or ' B' in plyrColors:
                    print("It is now the", plyrColors[1], " team's turn!\n")         
                    validStartChoices = self.collectPosStart()
                
                    while gotStrt == False:
                        print("Please enter coordinates for the piece you want to move    ** 0,0 represents the TOP-LEFT corner **")
                        strtX, strtY = input("Format your input as follows - X Y:  ").split(' ')
                        strtX = int(strtX)
                        strtY = int(strtY)
                        strtColor = self.boardState[strtX][strtY]
                        print(strtColor)
                        #Prelim check of if input in domain of board coordinates
                        if (self.validCoords((strtX, strtY))):
                            print(validStartChoices)
                            if (strtX, strtY, strtColor) in validStartChoices:
                                gotStrt = True
                        if gotStrt == False:
                            print("\nPlease enter a valid checker piece of your color")
                                                        
                    start = (strtX, strtY)     
                    color = self.boardState[strtX][strtY]
                    startFull = (start[0], start[1], self.boardState[start[0]][start[1]])
                            
                    
                    while (gotTrgt == False):
                        validTargetChoices = self.collectPosTargets(startFull)
                        print("Please select a valid tile from above to jump to")
                        trgtX, trgtY = input("Format your input as follows - X Y:  ").split(' ')
                        trgtX = int(trgtX)
                        trgtY = int(trgtY)

                        if self.validCoords((trgtX, trgtY)):
                            target = (trgtX, trgtY)                            
                            if target in validTargetChoices:
                                trgtColor = self.boardState[trgtX][trgtY]                            
                                moveList.append(target)
                                gotTrgt == True
                                trgtPass += 1
                                
                    while(self.adjTileEnemies(moveList[trgtPass - 1]) == True):
                        nxtMove = (moveList[trgtPass-1][0], moveList[trgtPass-1][1])
                        nxtColor = self.boardState[nxtMove[0]][nxtMove[1]]
                        nxtMoveFull = (nxtMove[0], nxtMove[1], nxtColor)
                        validTargetChoices = self.collectPosTargets(nxtMoveFull, True)
                        print("ZZZZ\n")
                        print("Please select a valid tile from above to jump to    ** 0,0 represents the TOP-LEFT corner **")
                        trgtX = int(trgtX)
                        trgtY = int(trgtY)
                        target = (trgtX, trgtY)
                        if target in validTargetChoices:
                            moveList.append(target)
                            print(moveList)
                            trgtPass += 1

                        gotInput == True
            self.turnCount += 1
            self.move(color, (strtX, strtY), moveList)

        


        

def main():
    newGame = Board()
    results = newGame.collectCheckers(0,0)
    newGame.playGame()
    time.sleep(10)
main()