from Tkinter import Tk
from ui.checkers_board import CheckersBoardUI

__author__ = 'vladvalt'

##The place to start checkers


def checkers():
    root = Tk()
    print('lol')
    app = CheckersBoardUI(master=root, controller=None)
    root.mainloop()

checkers()