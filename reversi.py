from Tkinter import Tk
from controllers.common_board_controller import GAME_MODES
from controllers.reversi_board_controller import ReversiBoardController
from model.reversi_model import ReversiGameModel
from ui.board_common import BoardCommonUI

__author__ = 'danylofitel'


def get_reversi_model():
    return ReversiGameModel(1, 2)


def get_reversi_controller():
    return ReversiBoardController(model=get_reversi_model(), mode=GAME_MODES["playerVSPRO"])


def reversi():
    root = Tk()
    controller = get_reversi_controller()
    app = BoardCommonUI(master=root, controller=controller)
    controller.fill_board()
    root.mainloop()

reversi()