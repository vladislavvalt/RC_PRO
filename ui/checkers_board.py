from ui.board_common import BoardCommonUI

__author__ = 'vladvalt'


class CheckersBoardUI(BoardCommonUI):

    def __init__(self, master, controller):
        BoardCommonUI.__init__(self, master=master, controller=None)