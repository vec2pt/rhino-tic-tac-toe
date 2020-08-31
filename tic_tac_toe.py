import rhinoscriptsyntax as rs

import random

def get_possible_moves(board):
    possible_moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                possible_moves.append((i, j))
    return possible_moves


def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return "{} wins!".format(row[0])
    for i in range(3):
        column = [row[i] for row in board]
        if column[0] == column[1] == column[2] != '':
            return "{} wins!".format(column[0])
    if board[0][0] == board[1][1] == board[2][2] != '':
        return "{} wins!".format(board[0][0])
    if board[0][2] == board[1][1] == board[2][0] != '':
        return "{} wins!".format(board[0][2])
    if all(board[0]) and all(board[1]) and all(board[2]):
        return "Tie!"


def draw_board(point, size=10):
    grid = []
    for i in range(3):
        row =[]
        for j in range(3):
            x = point[0] + i * size
            y = point[1] + j * size
            r = rs.AddRectangle((x, y, 0), size, size)
            row.append(r)
        rs.HideObjects(row)
        grid.append(row)
    rectangles = [
    rs.AddRectangle((point[0], point[1] + size - size*.025, 0), size*3, size*.05),
    rs.AddRectangle((point[0], point[1] + 2*size - size*.025, 0), size*3, size*.05),
    rs.AddRectangle((point[0] + size - size*.025, point[1], 0), size*.05, size*3),
    rs.AddRectangle((point[0] + 2*size - size*.025, point[1], 0), size*.05, size*3)]
    rs.CurveBooleanUnion(rectangles)
    rs.DeleteObjects(rectangles)
    return grid


def draw_o(point, size=10):
    rs.AddCircle(point, size*(.7/2))
    rs.AddCircle(point, size*(.7/2 - .05))


def draw_x(point, size=10):
    x = point[0] - size*.025
    y = point[1] - (size*.75)/2
    r = rs.AddRectangle((x, y, 0), size*.05, size*.75)
    rectangles = [
    rs.RotateObject(r, point, 45, copy=True),
    rs.RotateObject(r, point, -45, copy=True)]
    rs.DeleteObject(r)
    rs.CurveBooleanUnion(rectangles)
    rs.DeleteObjects(rectangles)


def player_turn(board, grid, player_symbol):
    point = rs.GetPoint("{} turn".format(player_symbol))
    for i, j in get_possible_moves(board):
        if rs.PointInPlanarClosedCurve(point, grid[i][j]) == 1:
            point = rs.CurveAreaCentroid(grid[i][j])[0]
            if player_symbol == 'X':
                draw_x(point)
                board[i][j] = 'X'
            else:
                draw_o(point)
                board[i][j] = 'O'
            return True
    return False


def ai_turn(board, grid, ai_symbol, player_symbol):
    row, column = ai_brain(board, ai_symbol, player_symbol)
    board[row][column] = ai_symbol
    point = rs.CurveAreaCentroid(grid[row][column])[0]
    if ai_symbol == 'X':
        draw_x(point)
    else:
        draw_o(point)

def ai_brain(board, ai_symbol, player_symbol):
    for i, j in get_possible_moves(board):
        board_copy = [row[:] for row in board]
        board_copy[i][j] = ai_symbol
        if check_winner(board_copy) == "{} wins!".format(ai_symbol):
            return (i, j)
    for i, j in get_possible_moves(board):
        board_copy = [row[:] for row in board]
        board_copy[i][j] = player_symbol
        if check_winner(board_copy) == "{} wins!".format(player_symbol):
            return (i, j)
    return random.choice(get_possible_moves(board))

def tic_tac_toe():
    board = [['', '', ''], ['', '', ''], ['', '', '']]

    grid = draw_board(rs.GetPoint("Set board starter point"))

    if rs.ListBox(('O', 'X'), message='Choose your symbol', default='O') == 'O':
        player_symbol, ai_symbol = ('O', 'X')
    else:
        player_symbol, ai_symbol = ('X', 'O')

    if random.randint(0, 1):
        ai_turn(board, grid, ai_symbol, player_symbol)
    while not check_winner(board):
        if player_turn(board, grid, player_symbol):
            if not check_winner(board):
                ai_turn(board, grid, ai_symbol, player_symbol)
    else:
        rs.MessageBox(check_winner(board))
        for row in grid:
            for o in row:
                rs.ShowObject(o)
                rs.DeleteObject(o)


if __name__ == "__main__":
    tic_tac_toe()
