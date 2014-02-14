from Tkinter import Tk
from ui.reversi_board import ReversiBoardUI

__author__ = 'denfitel'

##The place to start reversi

def reversi():
    root = Tk()
    print 'REVERSI'
    app = ReversiBoardUI(master=root, controller=None)
    root.mainloop()

reversi()