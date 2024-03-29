# CLI Tic Tac Toe with the Minimax Algorithm
# 20220123
# vec2pt
# https://github.com/vlmarch

PLAYER_O = 'O'
PLAYER_X = 'X'
MINIMAX_DEPTH = 10

import random

def print_board(board):
    for i in board:
        print('|'.join(i))
    print('')

def enter_move(board, whose_turn, player):
    if whose_turn == player:
        print("Player move:")
        while True:
            i = int(input("\tPlease enter row index:"))
            j = int(input("\tPlease enter column index:"))
            if (i, j) in get_possible_moves(board):
                break
    else:
        print("Computer move:")
        i, j = ai_turn(board, whose_turn)
    board[i][j] = whose_turn
    print_board(board)

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

def ai_turn(board, ai_player):
    best_score = -1000
    best_move = None
    for i, j in get_possible_moves(board):
        board[i][j] = ai_player
        score = minimax(board, ai_player)
        board[i][j] = '-'
        if score > best_score:
            best_score = score
            best_move = (i, j)
    return best_move

def minimax(board, player, depth=0, maximizing=False):
    if is_victory(board):
        if maximizing: return -10
        else: return 10
    elif is_tie(board): return 0

    if depth == MINIMAX_DEPTH:
        return 0

    if maximizing: best_score = -1000
    else: best_score = 1000
    for i, j in get_possible_moves(board):
        board[i][j] = next_player(player)
        score = minimax(board, next_player(player), depth+1, not maximizing)
        board[i][j] = '-'
        if maximizing: best_score = max(best_score, score)
        else: best_score = min(best_score, score)
    return best_score


def tic_tac_toe():
    board = [['-', '-', '-'],
             ['-', '-', '-'],
             ['-', '-', '-']]

    player = PLAYER_O
    ai_player = PLAYER_X


    if random.randint(0, 1):
        whose_turn = player
    else:
        whose_turn = ai_player

    print()
    print_board(board)
    while True:
        enter_move(board, whose_turn, player)
        if is_victory(board):
            print("{} wins!".format(whose_turn))
            return
        if is_tie(board):
            print("Tie!")
            return
        whose_turn = next_player(whose_turn)

if __name__ == "__main__":
    tic_tac_toe()
