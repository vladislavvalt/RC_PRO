from controllers.choose_game_controller import ChooseGameController
from ui.choose_game import ChooseGameUI
from Tkinter import *


__author__ = 'vladvalt'


def play():
    root = Tk()
    controller = ChooseGameController()
    app = ChooseGameUI(master=root, choose_controller=controller)
    root.mainloop()

play()
