import pygame, sys
import random
from pygame.locals import *


white = (219, 217, 217)
blue = (157, 214, 250)
green = (33, 173, 103)
red = (247, 69, 69)
yellow = (252, 187, 66)
black = (0, 0, 0)
gray = (145, 145, 145)

pygame.init()
clock = pygame.time.Clock()

length = 200
breadth = 200
margin = 5
rows, cols = 3, 3
fontsize = 112
size = width, height = ((length + margin)* cols + margin ) , ((breadth + margin)* rows + margin)

window = pygame.display.set_mode(size)
font = pygame.font.Font('freesansbold.ttf', fontsize)
pygame.display.set_caption("Tic Tac Toe")

def drawGrid(rows, cols, board):

    for i in range(rows):
        for j in range(cols):
            #available.append([i,j])
            rect = Rect((margin + length) * j + margin, (margin + breadth) * i + margin, length, breadth)
            ranges[str(i) + str(j)] = (((margin + length) * j + margin,(margin + breadth) * i + margin ), ((margin + length) * j + margin + length , (margin + breadth) * i + margin + breadth))
            pygame.draw.rect(window, white, rect)

    pygame.display.update()

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def updateWindow(i, j, symbol):

    if symbol == "X":
        text = font.render(symbol, True, red)
    else:
        text = font.render(symbol, True, green)

    textRect = text.get_rect()
    rect = Rect((margin + length) * j + margin, (margin + breadth) * i + margin, length, breadth)
    textRect.center = rect.center
    window.blit(text, textRect)

    pygame.display.update()

def clearDisplay(rows, cols, board):
    drawGrid(rows, cols, board)



def displayWinner(winner):
    clearDisplay(rows, cols, board)
    if winner == 1:
        message = "Computer Won!"

    if winner == -1:
        message = "Player Won!"

    if winner == 0:
        message = "Match Draw"

    message = message.split()


    message0 = message[0]
    message1 = message[1]


    message0 = font.render(message[0], True, yellow)
    message1 = font.render(message[1], True, yellow)


    rect0 = message0.get_rect()
    rect1 = message1.get_rect()

    rect0.center = width//2, height//2 - 100
    rect1.center = width//2, height//2 + 20

    window.blit(message0, rect0)
    window.blit(message1, rect1)

    pygame.display.update()




def getMove(ranges, move):
    x, y = move
    for key, value in ranges.items():

        if x >= value[0][0] and y >= value[0][1] and x <= value[1][0] and y <= value[1][1]:
            return int(key[0]), int(key[1])

def playerTurn(board):
    while True:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            #checks if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if the mouse is clicked on the available make move
                move = mouse
                #print(move)
                [i, j] = getMove(ranges, move)

                #print([i, j] in available)
                if board[i][j] == '':
                    board[i][j] = player
                    updateWindow(i, j, player)
                    return True

def bestMove(board):

    bestScore = float("-inf")
    move = None

    for i in range(3):
        for j in range(3):

            if board[i][j] == '':
                board[i][j] = computer
                score = miniMax(board, 0, False)
                board[i][j] = ''
                if score > bestScore:
                    bestScore = score
                    move = [i, j]

    return move


def miniMax(board, depth, isMaximizing):

    result = checkWinner(board)

    if result != None:
        return result

    if isMaximizing:
        bestScore = float("-inf")

        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = computer
                    score = miniMax(board, depth + 1, False)
                    board[i][j] = ''
                    bestScore = max(score, bestScore)

        return bestScore

    else:
        bestScore = float("inf")


        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = player
                    score = miniMax(board, depth + 1, True)
                    board[i][j] = ''
                    bestScore = min(score, bestScore)

        return bestScore

def computerTurn(board):
    """i, j = random.randint(0,2), random.randint(0, 2)
    while board[i][j] != '':
        i, j = random.randint(0,2), random.randint(0, 2)"""

    i, j = bestMove(board)

    board[i][j] = computer
    pygame.time.delay(500)
    updateWindow(i, j, computer)

def checkWinner(board):

    for row in range(3) :
        if (board[row][0] == board[row][1] and board[row][1] == board[row][2]) :
            if (board[row][0] == player) :
                return -1
            elif (board[row][0] == computer) :
                return 1

    # Checking for Columns for X or O victory.
    for col in range(3) :

        if (board[0][col] == board[1][col] and board[1][col] == board[2][col]) :

            if (board[0][col] == player) :
                return -1
            elif (board[0][col] == computer) :
                return 1

    # Checking for Diagonals for X or O victory.
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2]) :

        if (board[0][0] == player) :
            return -1
        elif (board[0][0] == computer) :
            return 1

    if (board[0][2] == board[1][1] and board[1][1] == board[2][0]) :

        if (board[0][2] == player) :
            return -1
        elif (board[0][2] == computer) :
            return 1

    # Else if none of them have won then return 0
    if not isMovesLeft(board):
        return 0

    return None

def isMovesLeft(board) :

    for i in range(3) :
        for j in range(3) :
            if (board[i][j] == '') :
                return True
    return False


board = [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
]

ranges = {}

player = "X"
computer = "O"

game_over = False

turn = True

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    drawGrid(rows, cols, board)

    while True:

        if turn:
            playerTurn(board)
            turn = False

        else:
            computerTurn(board)
            turn  = True

        winner = checkWinner(board)

        if winner == -1:
            print("Player Won!")
            break

        if winner == 1:
            print("Computer Won!")
            break

        if winner == 0:
            print("Match Draw!")
            break

    pygame.time.delay(800)
    displayWinner(winner)
    wait()
