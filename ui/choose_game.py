from Tkinter import *


__author__ = 'vladvalt'


class ChooseGameUI(Frame):

    def createWidgets(self):
        self.quit_button = Button(self)
        self.quit_button["text"] = "QUIT"
        self.quit_button["fg"]   = "red"
        self.quit_button["command"] =  self.quit

        self.quit_button.pack({"side": "left", "pady": 25})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Reversi"
        self.hi_there["command"] = self.choose_controller.reversi_select
        self.hi_there.pack({"side": "left", "pady": 25})

        self.checkers = Button(self)
        self.checkers["text"] = "Checkers"
        self.checkers["command"] = self.choose_controller.checkers_select
        self.checkers.pack({"side": "left", "pady": 25})

    def centerWindow(self):
        w = 300
        h = 100
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h) * 0.25
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def __init__(self,  master, choose_controller):
        Frame.__init__(self, master)
        self.parent = master
        self.choose_controller = choose_controller
        self.parent.title('Choose the game you like')
        self.parent.config({"bg": "grey"})
        self.config({"bg": "grey"})
        self.pack()
        self.createWidgets()
        self.centerWindow()