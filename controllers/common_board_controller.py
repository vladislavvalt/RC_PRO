__author__ = 'vladvalt'


class CommonBoardController:

    def __init__(self):
        self.EMPTY = 1000500
        self.board = None

    def set_board(self, board):
        self.board = board

    def clear_cell(self, x, y):
        pass

    def fill_cell(self, x, y, filler):
        if filler == self.EMPTY:
            self.clear_cell(x, y)
            return
        pass

    def modify_cell(self, filler):
        self.clear_cell()
        self.fill_cell()

    def change_cell_color(self, x, y, color):
        self.board.cells[x][y].config(bg=color)