import rhinoscriptsyntax as rs

import random


class TicTacToe:

    def __init__(self):
        self.board = []
        self.ui_grid = []
        self.cell_size = 10

    def create_board(self):
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    def create_ui_grid(self, point):
        self.ui_grid = [[(None, None), (None, None), (None, None)],
                        [(None, None), (None, None), (None, None)],
                        [(point, None), (None, None), (None, None)]]

    def draw_board(self, point):
        self.ui_grid = [point,(point[0]+self.cell_size, point[1]+self.cell_size)]
        rectangles = [
            rs.AddRectangle((point[0], point[1] + self.cell_size - self.cell_size*.025, 0),
                            self.cell_size*3,
                            self.cell_size*.05),
            rs.AddRectangle((point[0], point[1] + 2*self.cell_size - self.cell_size*.025, 0),
                            self.cell_size*3,
                            self.cell_size*.05),
            rs.AddRectangle((point[0] + self.cell_size - self.cell_size*.025, point[1], 0),
                            self.cell_size*.05,
                            self.cell_size*3),
            rs.AddRectangle((point[0] + 2*self.cell_size - self.cell_size*.025, point[1], 0),
                            self.cell_size*.05,
                            self.cell_size*3)]
        rs.CurveBooleanUnion(rectangles)
        rs.DeleteObjects(rectangles)

    def draw_o(self, point):
        rs.AddCircle(point, self.cell_size*(.7/2))
        rs.AddCircle(point, self.cell_size*(.7/2 - .05))

    def draw_x(self, point):
        x = point[0] - self.cell_size*.025
        y = point[1] - (self.cell_size*.75)/2
        r = rs.AddRectangle((x, y, 0), self.cell_size*.05, self.cell_size*.75)
        rectangles = [
            rs.RotateObject(r, point, 45, copy=True),
            rs.RotateObject(r, point, -45, copy=True)]
        rs.DeleteObject(r)
        rs.CurveBooleanUnion(rectangles)
        rs.DeleteObjects(rectangles)

    def get_random_first_player(self):
        return random.randint(0, 1)

    def fix_spot(self, row, col, player):
        self.board[row][col] = player

    def start(self):
        self.draw_board(rs.GetPoint("Set board starter point"))



# starting the game
tic_tac_toe = TicTacToe()
tic_tac_toe.start()