# Tic Tac Toe for Rhino v2
# 20220123
# Vladyslav M
# https://github.com/vlmarch


# import rhinoscriptsyntax as rs
import random
import copy

CELL_SIZE = 10
PLAYER_O = 'O'
PLAYER_X = 'X'
MODE = False # True - for Rhino mode; False - for cmd mode;

def display_board(board):
    for i in board:
        print('|'.join(i))
    print('')

def enter_move(board, whose_turn, player):
    if whose_turn == player:
        i = input()
        j = input()
        board[i][j] = player
    else:
        print(ai_turn(board, whose_turn))


def get_possible_moves(board):
    possible_moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                possible_moves.append((i,j))
    return possible_moves

def is_victory(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '-':
            return True
        if board[0][i] == board[1][i] == board[2][i] != '-':
            return True
    if board[0][0] == board[1][1] == board[2][2] != '-':
        return True
    if board[0][2] == board[1][1] == board[2][0] != '-':
        return True
    return False

def is_tie(board):
    return all([all([j !='-' for j in board[i]]) for i in range(3)])

def next_player(previous_player):
    return PLAYER_O if previous_player == PLAYER_X else PLAYER_X


def draw_move(board):
    pass
    # The function draws the computer's move and updates the board.

def ai_turn(board, ai_player):
    # temp_board = copy.deepcopy(board)
    return minimax(board, ai_player)

def minimax(board, ai_player, maximizing=True, level=0):
    best_score = float('-inf')
    for i, j in get_possible_moves(board):
        temp_board = copy.deepcopy(board)
        temp_board[i][j] = ai_player
        # display_board(temp_board)
        if is_victory(temp_board):
            if maximizing:
                store = 1 - level
            else:
                store = -1 - level
        elif is_tie(temp_board):
            store = 0
        else:
            if maximizing:
                store = min(minimax(temp_board, next_player(ai_player), not(maximizing), level=level+1))
            else:
                store = max(minimax(temp_board, next_player(ai_player), not(maximizing), level=level+1))
        if store > best_score:
            best_move = (i, j)
    return best_move

# def ai_turn(board, ai_player):
#     best_score = float('-inf')
#     for i, j in get_possible_moves(board):
#         temp_board = copy.deepcopy(board)
#         temp_board[i][j] = ai_player
#         score = minimax(temp_board, ai_player)
#         if score > best_score:
#             best_score = score
#             best_move = (i, j)
#     return best_move

# def minimax(board, ai_player, maximizing=True):
#     if is_victory(board):
#         if maximizing: return 1
#         else: return -1
#     elif is_tie(board): return 0
#     else:
#         if maximizing:
#             x = min(minimax(board, next_player(ai_player), not(maximizing)))
#         else:
#             x = max(minimax(board, next_player(ai_player), maximizing))
#         return x 


def game():
    board = [['-', '-', '-'], 
             ['-', '-', '-'], 
             ['-', '-', '-']]

    player = PLAYER_O
    ai_player = PLAYER_X
    whose_turn = player

    while True:
        display_board(board)
        # board = enter_move(board, player)
        enter_move(board, whose_turn, player)
        if is_victory(board):
            print("{} wins!".format(whose_turn))
            return
        if is_tie(board):
            print("Tie!")
            return
        whose_turn = next_player(whose_turn)         

# game()

board = [['O', '-', '-'], 
         ['-', '-', 'O'], 
         ['O', 'X', 'X']]

ai_player = PLAYER_X
print(ai_turn(board, ai_player))
