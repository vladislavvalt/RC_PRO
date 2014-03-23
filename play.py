from ui.choose_game import ChooseGameUI
from Tkinter import *


__author__ = 'vladvalt'


def play():
    root = Tk()
    app = ChooseGameUI(master=root)
    root.mainloop()

play()
