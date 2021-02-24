
# By default player goes first, and then computer moves.
# Player is denoted X, computer is denoted by 0 and blank is denoted by _

import random

wining_positions = [[0, 1, 2],[3, 4, 5], [6, 7, 8], # All winning Combinations
                    [0, 3, 6], [1, 4, 7], [2, 5, 8],
                    [0, 4, 8], [2, 4, 6]]

def playerMove(game_position, available):
    move = int(input("Enter your Move :"))
    if move in available:
        game_position[move] = "X"
        available.remove(move)
    else:
        print("Enter a valid Move!!")
        playerMove(game_position, available)

def computerMove(game_position, available):
    move = random.choice(list(available))
    game_position[move] = "0"
    print("Computer puts circle at {}".format(move))
    available.remove(move)

def checkWinner(game_position, turn):
    for wining_position in wining_positions:
        if turn:
            if game_position[wining_position[0]] == "X" and game_position[wining_position[1]] == "X" and game_position[wining_position[2]] == "X":
                return "Player"
        else:
            if game_position[wining_position[0]] == "0" and game_position[wining_position[1]] == "0" and game_position[wining_position[2]] == "0":
                return "Computer"

def printGame(game_position):
    print()
    print(game_position[0:3])
    print(game_position[3:6])
    print(game_position[6:9])
    print(flush = True)

def startGame():

    game_position = ["_", "_", "_", "_", "_", "_", "_", "_", "_"] # Shows the current game state
    available = set([0, 1, 2, 3, 4, 5, 6, 7, 8]) # Shows available valid moves
    game_over = False # True if game is over or if we run out of moves
    turn = True # True For player, False for Computer
    winner = None


    while not game_over:
        if turn:
            playerMove(game_position, available)
            winner = checkWinner(game_position, turn)
            turn = False
        else:
            computerMove(game_position, available)
            winner = checkWinner(game_position, turn)
            turn = True

        printGame(game_position)

        if winner == "Player":
            print("{} Won!!".format(winner))
            break

        if len(available) == 0:
            print("Match Draw!!")
            break

        if winner == "Computer":
            print("{} Won!!".format(winner))
            break

if __name__ == "__main__":
    startGame()
