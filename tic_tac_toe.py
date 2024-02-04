# Tic Tac Toe for Rhino with the Minimax Algorithm
# 20220124
# vec2pt
# https://github.com/vlmarch

import random
import rhinoscriptsyntax as rs

PLAYER_O = 'O'
PLAYER_X = 'X'
MINIMAX_DEPTH = 10
CELL_SIZE = 10

class TicTacToe:
    def __init__(self):
        self.board = [['-', '-', '-'],
                      ['-', '-', '-'],
                      ['-', '-', '-']]
        self.player_symbol = PLAYER_O
        self.ai_symbol = PLAYER_X
        self.whose_move = PLAYER_O
        self.board_location_point = (0,0,0)

    def get_possible_moves(self):
        """Generating a list of possible moves"""
        possible_moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    possible_moves.append((i,j))
        return possible_moves

    def is_victory(self):
        """Victory check"""
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '-':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '-':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '-':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '-':
            return True
        return False

    def is_tie(self):
        """Tie check"""
        return all([all([j !='-' for j in self.board[i]]) for i in range(3)])

    def next_player(self, previous_player):
        """Switches to the next player"""
        return PLAYER_O if previous_player == PLAYER_X else PLAYER_X

    def enter_move(self):
        """Apply the move"""
        self.get_possible_moves()
        if self.whose_move == self.player_symbol: i, j = self.player_move()
        else: i, j = self.ai_move()
        p1 , p2 = self.grid[i][j]
        point = ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2, 0)
        self.board[i][j] = self.whose_move
        self.draw_x(point) if self.whose_move == PLAYER_X else self.draw_o(point)
        self.whose_move = self.next_player(self.whose_move)

    def create_board(self, size=CELL_SIZE):
        """Drawing a game board"""
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
        """Drawing O"""
        rs.AddCircle(point, size*(.7/2))
        rs.AddCircle(point, size*(.7/2 - .05))

    def draw_x(self, point, size=CELL_SIZE):
        """Drawing X"""
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
        """Character selection for the player"""
        if rs.ListBox((PLAYER_O, PLAYER_X),
                      message='Choose your symbol',
                      default=PLAYER_O) == PLAYER_O:
            self.player_symbol, self.ai_symbol = (PLAYER_O, PLAYER_X)
        else:
            self.player_symbol, self.ai_symbol = (PLAYER_X, PLAYER_O)

    def player_move(self):
        """Player move"""
        while True:
            point = rs.GetPoint("{} turn".format(self.player_symbol))
            for i, j in self.get_possible_moves():
                p_x = point[0]
                p_y = point[1]
                g = self.grid[i][j]
                if g[0][0] <= p_x <= g[1][0] and \
                   g[0][1] <= p_y <= g[1][1]:
                    return (i, j)

    def ai_move(self):
        """Best move for AI"""
        best_score = -1000
        best_move = None
        for i, j in self.get_possible_moves():
            self.board[i][j] = self.ai_symbol
            score = self.minimax(self.ai_symbol)
            self.board[i][j] = '-'
            if score > best_score:
                best_score = score
                best_move = (i, j)
        return best_move

    def minimax(self, player, depth=0, maximizing=False):
        """Minimax Algorithm"""
        if self.is_victory():
            if maximizing: return -10
            else: return 10
        elif self.is_tie(): return 0
        if depth == MINIMAX_DEPTH:
            return 0
        if maximizing: best_score = -1000
        else: best_score = 1000
        for i, j in self.get_possible_moves():
            self.board[i][j] = self.next_player(player)
            score = self.minimax(self.next_player(player), depth+1, not maximizing)
            self.board[i][j] = '-'
            if maximizing: best_score = max(best_score, score)
            else: best_score = min(best_score, score)
        return best_score

    def start(self):
        """Starts the game"""
        self.create_board()
        self.get_player_symbol()

        # Who will start the game?
        if random.randint(0, 1):
            self.whose_move = self.ai_symbol

        while True:
            self.enter_move()
            if self.is_victory():
                message = "{} wins!".format(self.next_player(self.whose_move))
                rs.MessageBox(message, buttons=0, title="Tic Tac Toe")
                return
            if self.is_tie():
                rs.MessageBox("Tie!", buttons=0, title="Tic Tac Toe")
                return


if __name__ == "__main__":
    tic_tac_toe = TicTacToe()
    tic_tac_toe.start()
