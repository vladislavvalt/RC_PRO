from Tkinter import *
from controllers.common_board_controller import CommonBoardController

__author__ = 'vladvalt'


class BoardCommonUI(Frame):

    def initUI(self):

        self.right_menu = Frame(self)
        self.right_menu.config({"bg": "brown"})
        self.right_menu.pack(fill=BOTH, expand=TRUE, side=RIGHT, anchor=W)
        self.right_menu.update()

        self.bottom_console = Frame(self)
        self.bottom_console.config(bg="green")
        self.bottom_console.pack(fill=BOTH, expand=TRUE, side=BOTTOM)

        self.console = Text(self.bottom_console, height=5)
        self.console.pack(padx=2, pady=2)

        self.grid = Frame(self)
        self.grid.pack(fill=BOTH, expand=TRUE, side=LEFT, ipadx=100, ipady=150, padx=25, pady=25)

        for i in range(self.numberOfRows):
            for j in range(self.numberOfRows):
                color = "pink"
                if (i + j) % 2:
                    color = "brown"
                else:
                    color = "yellow"
                self.cells[i][j] = Canvas(self.grid, bg=color, height=30, width=10, borderwidth=0, highlightthickness=0)
                self.cells[i][j].grid(row=i, column=j, sticky=N+S+E+W)
                self.cells[i][j].bind("<Button-1>", lambda event, x=i, y=j: self.controller.on_cell_click(event, x, y))

        for x in range(self.numberOfRows):
            Grid.columnconfigure(self.grid, x, weight=1)
        for y in range(self.numberOfRows):
            Grid.rowconfigure(self.grid, y, weight=1)

    def centerWindow(self):
        w = 640
        h = 640
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) * 0.25
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.parent = master
        self.controller = controller
        controller.set_board(self)
        self.parent.title('Board common')
        #self.parent.config({"bg": "grey"})
        self.numberOfRows = 8
        self.cells = [[None for col in range(self.numberOfRows)] for row in range(self.numberOfRows)]
        self.config({"bg": "chocolate"})
        self.pack(fill=BOTH, expand=True)

        self.grid = None
        self.right_menu = None
        self.bottom_console = None
        self.console = None

        self.centerWindow()
        self.initUI()

###TODO remove it when necessary
#root = Tk()
#
#controller = CommonBoardController(model=None)
#app = BoardCommonUI(master=root, controller=controller)
#controller.fill_board()
#controller.clear_cell(1, 1)
#controller.fill_cell(2, 4, "checker_white")
#controller.fill_cell(2, 5, "checker_black")
#controller.modify_cell(0, 0, "checker_king_white")
#controller.modify_cell(7, 7, "checker_king_black")
#controller.change_cell_color(3, 3, "green")
#root.mainloop()
