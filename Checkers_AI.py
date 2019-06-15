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

    def canCapture(self, start):
        validMvFactor = self.getYFactor(start)
        enemyPieces = self.collectCheckers(0, 1)
        #piecesCanCap = []

        for y, x, c in self.collectCheckers(0, 0):
            for i in range(-1, 1, 2):
                if validMvFactor != 0:
                    y = y + validMvFactor
                    x = x + i
                    if (x < 8) and (y < 8):
                        if (x >= 0) and (y >= 0):
                            if (x,y,self.boardState[y][x]) in enemyPieces:
                                return True
                else:
                    for j in range(-1, 1, 2):
                        y = y + j
                        x = x + i                        
                        if (x < 8) and (y < 8):
                            if (x >= 0) and (y >= 0):
                                if (x,y,self.boardState[y][x]) in enemyPieces:
                                    return True
        return False
        


    def verifyTargetColor(self, start, finish, onlyCaptures = False):
        """This helper function takes in start and finish tuples formatted
        as (xCord, yCord) and the color as a string of a whitespace
        if onlyCaptures is True, then don't return True unless finish
        tile is occupied by enemy checker piece"""
        
        validMvFactor = 0
        y, x = start
        j, i = finish
        
        plyrTmClrs = []

        plyrColor = self.boardState[x][y]
        oppColor = self.boardState[i][j]
        
        if plyrColor in self.colorsPlyr: 
            plyrTmClrs = self.colorsPlyr
            enmyTmClrs = self.colorsAI
        else: 
            plyrTmClrs = self.colorsAI
            enmyTmClrs = self.colorsPlyr
        if (oppColor not in plyrTmClrs):
            if (onlyCaptures == True) and (oppColor in enmyTmClrs): return True
            elif(onlyCaptures == False): return True

        else: return False

     
    def validStrt(self, start):
        """Helper function to determine if any valid moves exist for the selected 
        checker piece. If a valid move exists then True, else False"""        

        validYDir = self.getYFactor(start)
        y, x = start
        #print(start)
        strtColor = self.boardState[y][x]
        validJumpToClrs = []
        queue = []
        if (strtColor == ' r') or (strtColor == ' R'): validJumpToClrs = [' -', ' b', ' B']
        else: validJumpToClrs = [' -', ' r', ' R']        
        
        if validYDir != 0:
            forwardLeft = (y + validYDir, x - 1)
            queue.append(forwardLeft)
        
            forwardRight = (y + validYDir, x + 1,)      
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
            if ((a < 8) and (a >= 0) and (b < 8) and (b >= 0)):
                for clr in range(3):
                    if self.boardState[a][b] == validJumpToClrs[clr]:
                 #       print("IS VALID!!\n", a, b)
                        return True
                #if self.verifyTargetColor(start, (a,b)) == True: return True
                #print("FAILED BIG TIME!!\n", a, b)
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
                if (mustAttack == True) or (self.canCapture((x, y)) == True):
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
                    

    def collectPosTargets(self, startChecker):
        x, y, plyrColor = startChecker
        queue = self.collectCheckers(0, 1)
        validTrgs = []
        allowedYChng = self.getYFactor((y,x))
        
        #if plyrColor == self.colorsAI[0]: allowedYChng = 1 
        #elif plyrColor == self.colorsPlyr[0]: allowedYChng = -1
        #else: allowedYChng = 2                
        if allowedYChng == 0:
            for i in range(-1, 1, 2):
                for j in range(-1, 1, 2):                    
                    queue.append(x + i, y + j)
        else:
            queue.append(y + allowedYChnge, x + 1)
            queue.append(y + allowedYChnge, x - 1)

        for trgt in queue:
            if (self.verifyTargetColor((y, x), trgt) == True):
                validTrgs.append(trgt)
        
        print("\n AVAILABLE TARGETS: ")
        for option in validTrgs:
            print(*option, sep=' ')



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
                
                #curPlyrPcs = self.collectCheckers(0, 0)
                #curOppPcs = self.collectCheckers(0, 1)
                validStartChoices = self.collectPosStart()
                if ' R' in plyrColors or ' B' in plyrColors:
                    print("It is now the", plyrColors[1], " team's turn!\n")
                
                    while gotStrt == False:                        
                        print("Please enter coordinates for the piece you want to move    ** 0,0 represents the TOP-LEFT corner **")
                        strtX, strtY = input("Format your input as follows - X Y:  ").split(' ')
                        strtX = int(strtX)
                        strtY = int(strtY)
                        
                       
                       # Prelim check of if input in domain of board coordinates                                           
                        if ((strtX < 8) and (strtY < 8)):
                            if self.boardState[strtX][strtY] in plyrColors:
                                gotStrt = True
                        if gotStrt == False:
                            print("\nPlease enter a valid checker piece of your color")                                
                    
                    color = self.boardState[strtX][strtY]

                    while (gotTrgt == False) or capPiece == False:
                        if capPiece == True:
                            print("Now please enter your next move for your piece")
                        else: 
                            print("Please enter coordinates for the tile you want to jump to    ** 0,0 represents the TOP-LEFT corner **")
                        trgtX, trgtY = input("Format your input as follows - X Y:  ").split(' ')
                        trgtX = int(trgtX)
                        #trgtY.replace(" ", "")
                        trgtY = int(trgtY)

                        # Prelim check of if input in domain of board coordinates                       
                        if ((trgtX < 8) and (trgtY < 8) and (trgtX >= 0) and (trgtY >= 0)):
                            if trgtPass == 0:
                                #print("Target Pass Count: ", trgtPass)
                                start = (strtX, strtY)
                            else: start = moveList[trgtPass - 1]
                            target = (trgtX, trgtY)
                            if (self.verifyTargetColor(start, target)) == True:
                                trgtColor = self.boardState[trgtX][trgtY]
                                moveList.append((trgtX, trgtY))
                                # If target is valid then check if any checkers are captured by player
                                if (trgtColor != ' -') and (trgtColor not in plyrColors):
                                    capPiece = True

                                gotTrgt = True
                                gotInput = True                                    
                                
                            
                
                """else:
                    print("The AI player will now take their turn\n")
                    startTimeAI = time.clock()                    
                    # moveList = CALL AI MOVE FINDER FUNCTION!!!
                    finishTimeAI = time.clock()
                    algRunTime = (finishTimeAI - startTimeAI)
                    print("AI algorith runtime: ", algRunTime)"""
                    

            self.turnCount += 1
            self.move(color, (strtX, strtY), moveList)

        
sampleArr = [[' -', ' R', ' -', ' -', ' -', ' B', ' -', ' B'], [' R', ' -', ' R', ' -', ' -', ' -', ' B', ' -'], [' -', ' R', ' -', ' -', ' -', ' B', ' -', ' B'], [' R', ' -', ' R', ' -', ' -', ' -', ' B', ' -'], [' -', ' R', ' -', ' -', ' -', ' B', ' -', ' B'], [' R', ' -', ' R', ' -', ' -', ' -', ' B', ' -'], [' -', ' R', ' -', ' -', ' -', ' B', ' -', ' B'], [' R', ' -', ' R', ' -', ' -', ' -', ' B', ' -']]
sampleArr = [[' -', ' B', ' -', ' -', ' -', ' B', ' -', ' B'], [' -', ' -', ' R', ' -', ' -', ' -', ' B', ' -'], [' -', ' -', ' -', ' -', ' -', ' B', ' -', ' B'], [' -', ' -', ' R', ' -', ' R', ' -', ' B', ' -'], [' -', ' -', ' -', ' -', ' -', ' -', ' -', ' -'], [' -', ' -', ' -', ' -', ' R', ' -', ' B', ' -'], [' -', ' -', ' -', ' -', ' -', ' B', ' -', ' B'], [' -', ' -', ' -', ' -', ' -', ' -', ' B', ' -']]

def movePieces(board, x, y): # Given the board, x, y, return an array of possible moves that the piece will end up. Returns 0 if it's no piece.
    moveList = []
    boardList = []
    if board[x][y] == ' -' or board[x][y] == ' r' or board[x][y] == ' R':
        return 0 # Piece does not exist in that space.
    # Identify if piece is crowned or not.
    crowned = False
    if board[x][y] == ' B':
        crowned = True
    # Produce attacking moves.
    attack_moveArr, attack_boardArr = eatEverything(board, x, y, crowned, [])
    #print("Mordekaiser")
    #print(attack_boardArr)
    myPiece = ' b'
    if crowned == True:
        myPiece = ' B'
    # Produce non-attacking moves (uncrowned).
    if isValidPosition(x-1,y-1):
        if board[x-1][y-1] == ' -':
            temp_board = copy.deepcopy(board)
            temp_board[x][y] = ' -'
            temp_board[x-1][y-1] = myPiece
            #print(board[x-1][y-1])
            boardList.append(temp_board)
            printBoardSimple(temp_board)
            moveList.append([x-1,y-1])
            print(boardList)
    if isValidPosition(x+1,y-1):
        if board[x+1][y-1] == ' -':
            temp_board = copy.deepcopy(board)
            print(temp_board)
            temp_board[x][y] = ' -'
            temp_board[x+1][y-1] = myPiece
            #print(board[x+1][y-1])
            boardList.append(temp_board)
            printBoardSimple(temp_board)
            moveList.append([x+1,y-1])
            #print("heya there")
            #print(boardList)
            
            print()
    # Produce non-attacking moves (crowned).
    if isValidPosition(x-1,y+1):
        if board[x-1][y+1] == ' -':
            temp_board = copy.deepcopy(board)
            temp_board[x][y] = ' -'
            temp_board[x-1][y+1] = ' B'
            boardList.append(temp_board)
            printBoardSimple(temp_board)
            moveList.append([x-1,y+1])
            #print("heya there")
            print(boardList)
    if isValidPosition(x+1,y+1):
        if board[x+1][y+1] == ' -':
            temp_board = copy.deepcopy(board)
            temp_board[x][y] = ' -'
            temp_board[x+1][y+1] = ' B'
            boardList.append(temp_board)
            printBoardSimple(temp_board)
            moveList.append([x+1,y+1])
            print(boardList)
    print("ughhh")
    #print(attack_moveArr)
    #print(attack_boardArr)
    #return moveList, boardList, attack_moveArr, attack_boardArr
    mergeArray(moveList, attack_moveArr)
    mergeArray(boardList, attack_boardArr)
    return moveList, boardList
            

def isValidPosition(x,y):
    return x >= 0 and y >= 0 and x < 8 and y < 8
    
def eatEverything(board, x, y, crowned, myMoves):
    canEat = False
    print(x,y)
    print("test")
    if isValidPosition(x-1,y-1): # Check for out of bounds.
        if board[x-1][y-1] == ' r' or board[x-1][y-1] == ' R': # Check if there's an enemy piece.
            if isValidPosition(x-2,y-2): # Check for out of bounds.
                if board[x-2][y-2] == ' -': # Check if it is empty space.
                    canEat = True
    if isValidPosition(x+1,y-1): # Check for out of bounds.
        if board[x+1][y-1] == ' r' or board[x+1][y-1] == ' R': # Check if there's an enemy piece.
            if isValidPosition(x+2,y-2): # Check for out of bounds.
                if board[x+2][y-2] == ' -': # Check if it is empty space.
                    canEat = True
    if crowned and isValidPosition(x-1,y+1): # Check for out of bounds.
        if board[x-1][y+1] == ' r' or board[x-1][y+1] == ' R': # Check if there's an enemy piece.
            if isValidPosition(x-2,y+2): # Check for out of bounds.
                if board[x-2][y+2] == ' -': # Check if it is empty space.
                    canEat = True
    if crowned and isValidPosition(x+1,y+1): # Check for out of bounds.
        #print(board[y][x])
        #printBoardSimple(board)
        if board[x+1][y+1] == ' r' or board[x+1][y+1] == ' R': # Check if there's an enemy piece.
            #print("test")
            if isValidPosition(x+2,y+2): # Check for out of bounds.
                if board[x+2][y+2] == ' -': # Check if it is empty space.
                    canEat = True
    if canEat == False: # Return the move list and board.
        print("Can't eat anymore")
        printBoardSimple(board)
        print()
        return [myMoves], [board]
    moveList = []
    myPiece = ' b'
    allMoveArr = []
    allBoardArr = []
    if crowned == True:
        myPiece = ' B'
    if isValidPosition(x-1,y-1): # Check for out of bounds.
        if board[x-1][y-1] == ' r' or board[x-1][y-1] == ' R': # Check if there's an enemy piece.
            if isValidPosition(x-2,y-2): # Check for out of bounds.
                if board[x-2][y-2] == ' -': # Check if it is empty space.
                    temp_board = copy.deepcopy(board)
                    temp_board[x][y] = ' -'
                    temp_board[x-1][y-1] = ' -'
                    temp_board[x-2][y-2] = myPiece
                    printBoardSimple(temp_board)
                    temp_myMoves = copy.deepcopy(myMoves)
                    temp_myMoves.append([x-2,y-2])
                    print("hello1")
                    moveArr, boardArr = eatEverything(temp_board, x-2, y-2, crowned, temp_myMoves)
                    mergeArray(allMoveArr, moveArr)
                    mergeArray(allBoardArr, boardArr)
    #print(x,y)
    if isValidPosition(x+1,y-1): # Check for out of bounds.
        if board[x+1][y-1] == ' r' or board[x+1][y-1] == ' R': # Check if there's an enemy piece.
            if isValidPosition(x+2,y-2): # Check for out of bounds.
                if board[x+2][y-2] == ' -': # Check if it is empty space.
                    temp_board = copy.deepcopy(board)
                    temp_board[x][y] = ' -'
                    temp_board[x+1][y-1] = ' -'
                    temp_board[x+2][y-2] = myPiece
                    printBoardSimple(temp_board)
                    temp_myMoves = copy.deepcopy(myMoves)
                    temp_myMoves.append([x+2,y-2])
                    print("hello2")
                    moveArr, boardArr = eatEverything(temp_board, x+2, y-2, crowned, temp_myMoves)
                    mergeArray(allMoveArr, moveArr)
                    mergeArray(allBoardArr, boardArr)
    if crowned and isValidPosition(x-1,y+1): # Check for out of bounds.
        if board[x-1][y+1] == ' r' or board[x-1][y+1] == ' R': # Check if there's an enemy piece.
            if isValidPosition(x-2,y+2): # Check for out of bounds.
                if board[x-2][y+2] == ' -': # Check if it is empty space.
                    #print(x,y)
                    temp_board = copy.deepcopy(board)
                    temp_board[x][y] = ' -'
                    temp_board[x-1][y+1] = ' -'
                    temp_board[x-2][y+2] = myPiece
                    printBoardSimple(temp_board)
                    temp_myMoves = copy.deepcopy(myMoves)
                    temp_myMoves.append([x-2,y+2])
                    print("hello3")
                    moveArr, boardArr = eatEverything(temp_board, x-2, y+2, crowned, temp_myMoves)
                    mergeArray(allMoveArr, moveArr)
                    mergeArray(allBoardArr, boardArr)
    if crowned and isValidPosition(x+1,y+1): # Check for out of bounds.
        if board[x+1][y+1] == ' r' or board[x+1][y+1] == ' R': # Check if there's an enemy piece.
            if isValidPosition(x+2,y+2): # Check for out of bounds.
                if board[x+2][y+2] == ' -': # Check if it is empty space.
                    temp_board = copy.deepcopy(board)
                    temp_board[x][y] = ' -'
                    temp_board[x+1][y+1] = ' -'
                    temp_board[x+2][y+2] = myPiece
                    printBoardSimple(temp_board)
                    temp_myMoves = copy.deepcopy(myMoves)
                    temp_myMoves.append([x+2,y+2])
                    print("hello4")
                    moveArr, boardArr = eatEverything(temp_board, x+2, y+2, crowned, temp_myMoves)
                    mergeArray(allMoveArr, moveArr)
                    mergeArray(allBoardArr, boardArr)
    print("These are my moves: ", end="")
    #print(allMoveArr)
    return allMoveArr, allBoardArr

def mergeArray(mainArr, subArr):
    for i in range(len(subArr)):
        mainArr.append(subArr[i])
    return mainArr

def printBoardSimple(board):
    for i in range(8):
        for j in range(8):
            print(board[j][i], end = "")
        print()


        

def main():
    newGame = Board()
    results = newGame.collectCheckers(0,0)
    newGame.playGame()
    time.sleep(10)
main()

moveList, boardList = movePieces(sampleArr, 0, 1)
#print(attack_boardArr)
#printBoardSimple(attack_boardArr[0])
#printBoardSimple(attack_boardArr[1])
#print()
for i in range(len(boardList)):
    printBoardSimple(boardList[i])
    print()
