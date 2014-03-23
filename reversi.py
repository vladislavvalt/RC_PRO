from Tkinter import Tk
from controllers.common_board_controller import GAME_MODES
from controllers.reversi_board_controller import ReversiBoardController
from model.reversi_model import ReversiGameModel
from ui.board_common import BoardCommonUI

__author__ = 'danfitel'

##The place to start reversi


def reversi():
    root = Tk()
    model = ReversiGameModel(1, 2)
    controller = ReversiBoardController(model=model, mode=GAME_MODES["playerVsPRO"])
    app = BoardCommonUI(master=root, controller=controller)
    controller.fill_board()
    root.mainloop()

reversi()