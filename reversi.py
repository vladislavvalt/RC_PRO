from tkinter import Tk
from controllers.reversi_board_controller import ReversiBoardController
from controllers.reversi_board_controller import GAME_MODES
from model.reversi_model import ReversiGameModel
from ui.board_common import BoardCommonUI

__author__ = 'danylofitel'


def get_reversi_model():
    return ReversiGameModel(2)


def get_reversi_controller():
    return ReversiBoardController(get_reversi_model(), GAME_MODES["playerVSPro"], True)


def reversi():
    root = Tk()
    controller = get_reversi_controller()
    app = BoardCommonUI(root, controller)
    controller.fill_board()
    root.mainloop()


reversi()
