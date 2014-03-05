from controllers.common_board_controller import CommonBoardController, GAME_MODES

__author__ = 'vladvalt'

FILLER_MAP = {0: None, 1: "checker_white", 2: "checker_black", 3: "checker_king_white", 4: "checker_king_black"}

AVAILABLE_MOVE_COLOR = "green"


class CheckersBoardController(CommonBoardController):

    def __init__(self, model):
        CommonBoardController.__init__(self, model=model)

    def fill_board(self):
        for i in range(self.model.board_size):
            for j in range(self.model.board_size):
                self.fill_cell(i, j, FILLER_MAP[self.model.board_position[i][j]])

    def on_cell_click(self, event, x, y):
        if self.game_mode == GAME_MODES["playerVSPlayer"]:
            #TODO update it
            available_moves = self.model.get_available_moves(x, y)
            for a in available_moves:
                self.change_cell_color(a[0], a[1], AVAILABLE_MOVE_COLOR)
        elif self.game_mode == GAME_MODES["playerVsPRO"]:
            pass