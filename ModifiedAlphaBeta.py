import math
import copy

myPlayerNumber = 0;

def modifiedAlphaBetaSearch(depth, state, player):
    global myPlayerNumber
    myPlayerNumber = player

    _, action = maxValue(depth, state, -math.inf, math.inf)

    return action


def maxValue(depth, state, alpha, beta):
    #print("Enter maxValue func")
    #print("Depth: ", depth)

    action = None
    utility = -math.inf

    if depth == 0 or len(getValidFutureMoves(state, myPlayerNumber)) == 0:
        utility = getUtility(state)
        return utility, action

    # if len(getValidFutureMoves(state, myPlayerNumber)) == 0:
    #     print("Valid moves is Empty!!!")

    for a in getValidFutureMoves(state, myPlayerNumber):

        actionUtilityofMinimizer, _ = minValue(depth-1, getResults(state, a, myPlayerNumber), alpha, beta)

        if actionUtilityofMinimizer > utility:
            #print(actionUtilityofMinimizer, " is greater than ", utility)
            utility = actionUtilityofMinimizer
            action = a

        if utility >= beta:
            #print("Prune")
            return utility, action

        alpha = max(alpha, utility)
        #print("Alpha after comparison: ", alpha)


    return utility, action


def minValue(depth, state, alpha, beta):
    #print("Enter minValue func")
    #print("Depth: ", depth)
    action = None
    utility = math.inf
    playerNum = 1 if myPlayerNumber == 2 else 1

    if depth == 0 or len(getValidFutureMoves(state, playerNum)) == 0:
        utility = getUtility(state)
        return utility, action

    for a in getValidFutureMoves(state, playerNum):

        actionUtilityofMaximizer, _ = maxValue(depth-1, getResults(state, a, playerNum), alpha, beta)

        if actionUtilityofMaximizer < utility:
            #print(actionUtilityofMaximizer, " is less than ", utility)
            utility = actionUtilityofMaximizer
            action = a

        if utility <= beta:
            #print("Prune")
            return utility, action

        beta = min(beta, utility)
        #print("Beta after comparison: ", alpha)

    return utility, action

def getResults(state, action, player):

    futureState = copy.deepcopy(state)

    # futureState = state

    futureState[action[0]][action[1]] = player

    flipThePieces(futureState, action, player, 1, 1)
    flipThePieces(futureState, action, player, 0, 1)
    flipThePieces(futureState, action, player, -1, 1)
    flipThePieces(futureState, action, player, 1, 0)
    flipThePieces(futureState, action, player, -1, 0)
    flipThePieces(futureState, action, player, -1, -1)
    flipThePieces(futureState, action, player, 0, -1)
    flipThePieces(futureState, action, player, 1, -1)

    #print("\n")
    #print("Player: ", player)
    #print("Action: ", action)

    return futureState

def flipThePieces(futureState, move, player, moveRow, moveColumn):
    row = move[0]
    column = move[1]
    continuous = True
    possibleFlip = []
    while(True):
        row += moveRow
        column += moveColumn
        if (row > 7 or row < 0 or column > 7 or column <0):
            break
        elif (futureState[row][column] == 0):
            break
        elif (futureState[row][column] == player and continuous):
            break
        elif (futureState[row][column] != player):
            continuous = False
            possibleFlip.append([row, column])
        elif (futureState[row][column] == player and not continuous): #flip
            for coord in possibleFlip:
                futureState[coord[0]][coord[1]] = player
            break


def getValidFutureMoves(futureState, me):
    validMoves = []
    for i in range(8):
        for j in range(8):
            if (futureState[i][j] == 0):
                if (couldBe(futureState, i, j, me)):
                    validMoves.append([i, j])
    return validMoves

def getUtility(state):
    score = 0;
    for i in range(8):
        for j in range(8):
            if (state[i][j] == myPlayerNumber):
                score += 1
    score += scoreUnflippablePieces(state, myPlayerNumber)
    return score

def couldBe(futureState, row, col, me):
    for incx in range(-1, 2):
        for incy in range(-1, 2):
            if ((incx == 0) and (incy == 0)):
                continue

            if (checkDirection(futureState, row, col, incx, incy, me)):
                return True

    return False

def checkDirection(futureState, row, col, incx, incy, me):
    sequence = []
    for i in range(1, 8):
        r = row + incy * i
        c = col + incx * i

        if ((r < 0) or (r > 7) or (c < 0) or (c > 7)):
            break

        sequence.append(futureState[r][c])

    count = 0

    for i in range(len(sequence)):
        if (me == 1):
            if (sequence[i] == 2):
                count = count + 1
            else:
                if ((sequence[i] == 1) and (count > 0)):
                    return True
                break
        else:
            if (sequence[i] == 1):
                count = count + 1
            else:
                if ((sequence[i] == 2) and (count > 0)):
                    return True
                break

    return False

def scoreUnflippablePieces(state, player):
    count = 0
    for i in range(8):
        for j in range(8):
            if (state[i][j] == player):
                directions = 0
                if (not isFlippableHorizontal(state, i, j, player)): directions += 1
                if (not isFlippableVertical(state, i, j, player)): directions += 1
                if (not isFlippableLeftDiagonal(state, i, j, player)): directions += 1
                if (not isFlippableRightDiagonal(state, i, j, player)): directions += 1
                if (directions == 2): count += 1
                if (directions == 3): count += 3
                if (directions == 4): count += 6
    return count


def isFlippableHorizontal(state, row, column, player):
    r = row
    left = player
    right = player
    while(True):
        r -= 1
        if (r < 0): break
        if (state[r][column] != player):
            left = state[r][column]
            break
    r = row
    while(True):
        r +=1
        if (r > 7): break
        if (state[r][column] != player):
            right = state[r][column]
            break
    if (left == player or right == player): return False
    if (left != 0 and right != 0): return True
    return True

def isFlippableVertical(state, row, column, player):
    c = column
    top = False
    bottom = False
    while(True):
        c -= 1
        if (c < 0): break
        if(state[row][c] != player):
            top = state[row][c]
            break
    c = column
    while(True):
        c +=1
        if (c > 7): break
        if (state[row][c] != player):
            bottom = state[row][c]
            break
    if (top == player or bottom == player): return False
    if (top != 0 and bottom != 0): return True
    return True

def isFlippableLeftDiagonal(state, row, column, player):
    r = row
    c = column
    left = False
    right = False
    while(True):
        r -= 1
        c -= 1
        if (r < 0 or c < 0): break
        if (state[r][c] != player):
            left = state[r][c]
            break
    r = row
    c = column
    while(True):
        r += 1
        c += 1
        if (r > 7 or c > 7): break
        if (state[r][c] != player):
            right = state[r][c]
            break
    if (left == player or right == player): return False
    if (left != 0 and right != 0): return True
    return True

def isFlippableRightDiagonal(state, row, column, player):
    r = row
    c = column
    left = False
    right = False
    while(True):
        r -= 1
        c += 1
        if (r < 0 or c > 7): break
        if (state[r][c] != player):
            left = state[r][c]
            break
    r = row
    c = column
    while(True):
        r += 1
        c -= 1
        if (r > 7 or c < 0): break
        if (state[r][c] != player):
            right = state[r][c]
            break
    if (left == player or right == player): return False
    if (left != 0 and right != 0): return True
    return True

