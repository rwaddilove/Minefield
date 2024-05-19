# Minefield

import os
import random

board = []  # board - 9 is bomb, <9 is cell's bomb count
dug = []  # where users have dug - 0/1


def new_board(size, bomb_count):

    # make an empty board
    b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]    # a row in board[]
    d = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']   # a row in dug[]
    for row in range(size):
        board.append(b[:size])  # board with bombs and bomb counts, 0-9 (9 is bomb)
        dug.append(d[:size])  # where users have dug - 0/1

    # add bombs in random places. Not bothered if same cell selected twice
    for _ in range(bomb_count):
        board[random.randint(0, size - 1)][random.randint(0, size - 1)] = 9     # bomb!

    # pre-calculate neighbouring bombs for each cell
    for row in range(size):
        for col in range(size):
            if board[row][col] < 9:     # if no bomb here, count neighbours with bombs
                board[row][col] = nearby_bombs(row, col)


def nearby_bombs(row, col) -> int:
    size = len(board)
    bombs = 0
    for r in range(max(row - 1, 0), min(row + 2, size)):
        for c in range(max(col - 1, 0), min(col + 2, size)):
            if board[r][c] == 9:
                bombs += 1
    return bombs


def show_dug():
    """Show only cells where we've dug in board"""
    size = len(board)  # dug[] and board[] have same dimensions
    print("   ", end="")
    for i in range(size):
        print(f" {i} ", end="")         # modify to format within space to allow double digits
    print("\n  ", "---" * size)

    for row in range(0, size):
        print(f"{row} |", end="")
        for col in range(0, size):
            if dug[row][col] == '': print(f" . ", end="")
            if dug[row][col] == 'D': print(f" {board[row][col]} ", end="")
            if dug[row][col] == 'F': print(f" X ", end="")
        print()


def show_board():
    """show the board with bombs and bomb counts"""
    size = len(board)
    print("   ", end="")
    for i in range(size):
        print(f" {i} ", end="")         # modify to format within space to allow double digits
    print("\n  ", "---" * size)

    for row in range(0, size):
        print(f"{row} |", end="")
        for col in range(0, size):
            if board[row][col] == 9:
                print(f" * ", end="")
            else:
                print(f" {board[row][col]} ", end="")
        print()


def get_move() -> str:
    """Returns 'Bomb! or 'OK'"""
    # quit?
    inp = 'z'
    while len(inp) != 1 or inp not in 'QDF':
        inp = input("(Q)uit, (D)ig, (F)lag: ").upper()
    if inp[0] == 'Q':
        return 'Q'

    # input coordinates of cell and then set in dug[]
    row = col = -1
    while row < 0 or row > len(dug)-1 or col < 0 or col > len(dug)-1:
        cell = input("Enter row,col (eg. 2,5): ").split(',')
        if len(cell) == 2:
            if cell[0].isdigit(): row = int(cell[0])
            if cell[1].isdigit(): col = int(cell[1])
    dug[row][col] = inp       # (D)ig or (F)lag

    if board[row][col] == 0 and inp == 'D':
        show_clear_cells(row,col)       # fill blank cells

    # check if it's a bomb!
    if board[row][col] == 9 and inp == 'D':
        return 'Bomb!'  # lost game!
    else:
        return 'OK'   # carry on playing


def show_clear_cells(row,col):
    """If nothing here (0), fill connected cells with 0"""
    for r in range(max(0,row-1),min(row+2,len(board))):
        for c in range(max(0,col-1), min(col+2,len(board))):
            dug[r][c] = 'D'
            # if board[r][c] == 0 and r != row and c != col:
            #     show_clear_cells(r, c)


def check_minefield():
    size = len(board)
    bombs = 0
    incorrect = 0
    correct = 0
    for row in range(size):
        for col in range(size):
            if board[row][col] == 9:
                bombs = bombs + 1
                if dug[row][col] == 'F':
                    correct = correct + 1
            if dug[row][col] == 'F' and board[row][col] != 9:
                incorrect = incorrect + 1
    print(f"There are {bombs} bombs. You flagged {correct} correctly.")
    if correct == bombs:
        print("Congratulations! You have done it!")
        return 'Done!'
    if incorrect > 0:
        print(f"There are {incorrect} flags.")
    return 'OK'


# ================== MAIN ===============
os.system('cls') if os.name == 'nt' else os.system('clear')

new_board(10, 10)
print("\n-------------------")
print(" M I N E F I E L D")
print("-------------------")
print()

play = 'OK'
while play == 'OK':
    show_dug()  # the user view
    play = get_move()   # returns 'OK' or 'Bomb!'
    if play == 'Bomb!':
        print("Oh no! You stepped on a bomb!\n")
        show_board()
    if play == 'OK':
        play = check_minefield()  # returns 'Done!' if completed
