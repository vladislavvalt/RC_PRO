import os
from PIL import Image, ImageTk
__author__ = 'vladvalt'

FILLERS = {"checker_white": "Apple.png",
           "checker_black": "Vista.png",
           "checker_king_white": "king_Apple.png",
           "checker_king_black": "king_natural_Apple.png",
           "reversi_white": "WBSmiley.png",
           "reversi_black": "BWSmiley.png",
           "reversi_available_move_white": "Star.png",
           "reversi_available_move_black": "Star.png"}

IMAGE_LOCATION = os.path.join(os.path.dirname(__file__), '../ui/pictures/')

GAME_MODES = {"playerVSPlayer": 1, "playerVSPRO": 2, "proVSPro": 3, "proVSEnemy": 4}


class CommonBoardController:

    def __init__(self, model):
        self.board = None
        self.model = model
        self.img_size = 32
        self.game_mode = GAME_MODES["playerVSPlayer"]

    #just derive it
    def fill_board(self):
        #TODO clear all this stuff later
        image = Image.open(IMAGE_LOCATION + "Apple.png")
        photo = ImageTk.PhotoImage(image)
        for i in range(self.board.numberOfRows):
            self.board.cells[i][i].create_image(self.img_size, self.img_size, image=photo)
            #python bug force us to keep reference
            self.board.cells[i][i].image=photo
            self.write_to_console("Cell number " + str(i) + " added")

    def write_to_console(self, txt):
        self.board.console.insert("1.0", txt + '\n')

    def set_board(self, board):
        self.board = board

    def clear_cell(self, x, y):
        self.board.cells[x][y].delete("all")

    def fill_cell(self, x, y, filler):
        if filler in FILLERS:
            image = Image.open(IMAGE_LOCATION + FILLERS[filler])
            photo = ImageTk.PhotoImage(image)
            self.board.cells[x][y].create_image(self.img_size, self.img_size, image=photo)
            #python bug force us to keep reference
            self.board.cells[x][y].image=photo

    def modify_cell(self, x, y, filler):
        #self.clear_cell(x, y)
        self.fill_cell(x, y, filler)

    def change_cell_color(self, x, y, color):
        self.board.cells[x][y].config(bg=color)

    def on_cell_click(self, event, x, y):
        print "click ON CELL"
        print "x = ", x
        print "y = ", y

    #show possible moves on the board
    def show_available_moves(self):
        moves = self.model.get_available_moves()