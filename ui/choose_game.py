from Tkinter import *

from ui.board_common import BoardCommonUI
from checkers import get_checkers_controller
from reversi import get_reversi_controller


__author__ = 'vladvalt'


class ChooseGameUI(Frame):
    def play_reversi(self):
        self.play(get_reversi_controller())

    def play_checkers(self):
        self.play(get_checkers_controller())

    def play(self, controller):
        self.quit()
        root = Tk()
        app = BoardCommonUI(master=root, controller=controller)
        controller.fill_board()
        root.mainloop()

    def createWidgets(self):
        self.quit_button = Button(self)
        self.quit_button["text"] = "QUIT"
        self.quit_button["fg"] = "red"
        self.quit_button["command"] = self.quit

        self.quit_button.pack({"side": "left", "pady": 25})

        self.reversi = Button(self)
        self.reversi["text"] = "Reversi"
        self.reversi["command"] = self.play_reversi
        self.reversi.pack({"side": "left", "pady": 25})

        self.checkers = Button(self)
        self.checkers["text"] = "Checkers"
        self.checkers["command"] = self.play_checkers
        self.checkers.pack({"side": "left", "pady": 25})

    def centerWindow(self):
        w = 300
        h = 100
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) * 0.25
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        self.parent.title('Choose the game you like')
        self.parent.config({"bg": "grey"})
        self.config({"bg": "grey"})
        self.pack()
        self.createWidgets()
        self.centerWindow()