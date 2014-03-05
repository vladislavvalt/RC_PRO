from Tkinter import Tk
from controllers.checkers_board_controller import CheckersBoardController
from model.checkers_model import CheckersGameModel
from ui.board_common import BoardCommonUI

__author__ = 'vladvalt'

##The place to start checkers


def checkers():
    root = Tk()
    model = CheckersGameModel()
    controller = CheckersBoardController(model=model)
    app = BoardCommonUI(master=root, controller=controller)
    controller.fill_board()
    root.mainloop()

checkers()