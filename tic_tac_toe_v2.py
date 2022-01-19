# Tic Tac Toe for Rhino v2
# 20220118
# Vladyslav M
# https://github.com/vlmarch


import rhinoscriptsyntax as rs
import random

CELL_SIZE = 10
PLAYER_O = 'O'
PLAYER_X = 'X'


class TicTacToe:
    def __init__(self):
        self.board_location_point = (0,0,0)
        self.board = [['', '', ''], ['', '', ''], ['', '', '']]
        self.player_symbol = PLAYER_O
        self.ai_symbol = PLAYER_X
        self.whose_turn = PLAYER_O

    def get_possible_moves(self):
        self.possible_moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.possible_moves.append((i, j))

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return "{} wins!".format(row[0])
        for i in range(3):
            column = [row[i] for row in self.board]
            if column[0] == column[1] == column[2] != '':
                return "{} wins!".format(column[0])
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return "{} wins!".format(self.board[0][0])
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return "{} wins!".format(self.board[0][2])
        if all(self.board[0]) and all(self.board[1]) and all(self.board[2]):
            return "Tie!"

    def make_turn(self):
        self.get_possible_moves()
        if self.whose_turn == self.player_symbol: i, j = self.player_turn()
        else: i, j = self.ai_turn()
        line = rs.AddLine(self.grid[i][j][0], self.grid[i][j][1])
        point = rs.CurveMidPoint(line)
        rs.DeleteObject(line)
        self.board[i][j] = self.whose_turn
        self.draw_x(point) if self.whose_turn == PLAYER_X else self.draw_o(point)
        self.whose_turn = PLAYER_X if self.whose_turn == PLAYER_O else PLAYER_O

    def create_board(self, size=CELL_SIZE):
        board_location_point = rs.GetPoint("Set board starter point")
        if board_location_point:
            self.board_location_point = board_location_point
        point = self.board_location_point
        self.grid = []
        for i in range(3):
            row =[]
            for j in range(3):
                x1 = point[0] + i * size
                y1 = point[1] + j * size
                x2 = point[0] + (i+1) * size
                y2 = point[1] + (j+1) * size
                row.append([(x1,y1), (x2, y2)])
            self.grid.append(row)

        rectangles = [
            rs.AddRectangle((point[0], point[1] + size - size*.025, 0), size*3, size*.05),
            rs.AddRectangle((point[0], point[1] + 2*size - size*.025, 0), size*3, size*.05),
            rs.AddRectangle((point[0] + size - size*.025, point[1], 0), size*.05, size*3),
            rs.AddRectangle((point[0] + 2*size - size*.025, point[1], 0), size*.05, size*3)]
        rs.CurveBooleanUnion(rectangles)
        rs.DeleteObjects(rectangles)

    def draw_o(self, point, size=CELL_SIZE):
        rs.AddCircle(point, size*(.7/2))
        rs.AddCircle(point, size*(.7/2 - .05))

    def draw_x(self, point, size=CELL_SIZE):
        x = point[0] - size*.025
        y = point[1] - (size*.75)/2
        r = rs.AddRectangle((x, y, 0), size*.05, size*.75)
        rectangles = [
            rs.RotateObject(r, point, 45, copy=True),
            rs.RotateObject(r, point, -45, copy=True)]
        rs.DeleteObject(r)
        rs.CurveBooleanUnion(rectangles)
        rs.DeleteObjects(rectangles)


    def get_player_symbol(self):
        if rs.ListBox((PLAYER_O, PLAYER_X), message='Choose your symbol', default=PLAYER_O) == PLAYER_O:
            self.player_symbol, self.ai_symbol = (PLAYER_O, PLAYER_X)
        else:
            self.player_symbol, self.ai_symbol = (PLAYER_X, PLAYER_O)

    def test_point(self, point, li):
        p_x = point[0]
        p_y = point[1]
        if li[0][0] <= p_x <= li[1][0] and li[0][1] <= p_y <= li[1][1]:
            return True

    def player_turn(self):
        while True:
            point = rs.GetPoint("{} turn".format(self.player_symbol))
            for i, j in self.possible_moves:
                if self.test_point(point, self.grid[i][j]):
                    return (i, j)


    def ai_turn(self):
        for i, j in self.possible_moves:
            self.minimax(i, j, 2)
        i, j = random.choice(self.possible_moves)
        return (i, j)

    def minimax(self, i, j, depth): #def minimax(self, i, j, depth, maximizingPlayer):
        if depth == 0:
            return 0
        if self.whose_turn == self.ai_symbol:
            pass
        pass

    def start(self):
        self.create_board()
        self.get_player_symbol()

        if random.randint(0, 1):
            self.whose_turn = self.ai_symbol

        while True:
            self.make_turn()
            mes = self.check_winner()
            if mes:
                print(mes)
                return




# Start the game
tic_tac_toe = TicTacToe()
tic_tac_toe.start()