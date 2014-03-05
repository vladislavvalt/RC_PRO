from controllers.common_board_controller import CommonBoardController

__author__ = 'vladvalt'


class CheckersBoardController(CommonBoardController):

    def __init__(self, model):
        CommonBoardController.__init__(self, model=model)