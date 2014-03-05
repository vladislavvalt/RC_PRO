from Tkconstants import NW, N
from Tkinter import Label, PhotoImage, Canvas
from PIL import Image, ImageTk
import numpy as np
__author__ = 'vladvalt'


class CommonBoardController:

    def __init__(self):
        self.empty = 1000500
        self.board = None
        self.model = None
        self.img_size = 32

    #just derive it
    def fill_board(self):
        #TODO clear all this stuff later
        image = Image.open("pictures/Apple.png")
        photo = ImageTk.PhotoImage(image)
        for i in range(self.board.numberOfRows):
            self.board.cells[i][i].create_image(self.img_size, self.img_size, image=photo)
            #python bug force us to keep reference
            self.board.cells[0][0].image=photo

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

    def on_cell_click(self):
        pass

    #show possible moves on the board
    def show_available_moves(self):
        moves = self.model.get_available_moves()