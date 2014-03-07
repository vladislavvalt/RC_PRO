import math
from controllers.common_board_controller import CommonBoardController, GAME_MODES
from model.checkers_model import MOVE_TYPES

__author__ = 'vladvalt'

FILLER_MAP = {0: None, 1: "checker_white", 2: "checker_black", 3: "checker_king_white", 4: "checker_king_black"}

AVAILABLE_MOVE_COLOR = "green"
CHECKERS_BACKGROUND_COLOR = "brown"

STATES = {"None" : 0, "checker_selected": 1}


class CheckersBoardController(CommonBoardController):

    def __init__(self, model):
        CommonBoardController.__init__(self, model=model)
        if self.game_mode == GAME_MODES["playerVSPlayer"]:
            self.state = STATES["None"]
            self.last_selected = None

    def fill_board(self):
        self.board.parent.title('Checkers')
        for i in range(self.model.board_size):
            for j in range(self.model.board_size):
                self.fill_cell(i, j, FILLER_MAP[self.model.board_position[i][j]])

    def simple_move(self, x, y, x_new, y_new):
        figure = self.model.board_position[x_new][y_new]
        self.fill_cell(x_new, y_new, FILLER_MAP[figure])
        self.clear_cell(x,y)

    def attack_move(self, x, y, x_new, y_new):
        figure = self.model.board_position[x_new][y_new]
        self.fill_cell(x_new, y_new, FILLER_MAP[figure])
        x_step = int(math.copysign(1, x_new - x))
        y_step = int(math.copysign(1, y_new - y))
        for i in range(int(math.fabs(x_new - x))):
            self.clear_cell(x + x_step * i, y + y_step * i)

    def on_cell_click(self, event, x, y):
        if self.game_mode == GAME_MODES["playerVSPlayer"]:
            if self.state == STATES["None"] and self.model.is_able_to_move(x, y):

                available_moves = self.model.get_available_moves(x, y)
                for a in available_moves:
                    self.change_cell_color(a[0], a[1], AVAILABLE_MOVE_COLOR)
                self.change_cell_color(x, y, AVAILABLE_MOVE_COLOR)
                self.last_selected = (x, y)
                self.state = STATES["checker_selected"]

            elif self.state == STATES["checker_selected"]:

                if not self.last_selected is None:
                    should_move_to_none_state = False
                    available_moves = self.model.get_available_moves(self.last_selected[0], self.last_selected[1])

                    if self.last_selected[0] == x and self.last_selected[1] == y and self.model.is_free_to_deselect():
                        should_move_to_none_state = True

                    elif (x, y) in self.model.get_available_moves(self.last_selected[0], self.last_selected[1]):
                        move_success = self.model.move(self.last_selected[0], self.last_selected[1], x, y)
                        if move_success:
                            if self.model.last_move_type == MOVE_TYPES["simple"]:
                                self.simple_move(self.last_selected[0], self.last_selected[1], x, y)
                                should_move_to_none_state = True
                            elif self.model.last_move_type == MOVE_TYPES["attack"]:
                                self.attack_move(self.last_selected[0], self.last_selected[1], x, y)
                                if self.model.should_continue_attack():
                                    for a in available_moves:
                                        self.change_cell_color(a[0], a[1], CHECKERS_BACKGROUND_COLOR)
                                    self.change_cell_color(self.last_selected[0], self.last_selected[1], CHECKERS_BACKGROUND_COLOR)
                                    self.change_cell_color(x, y, AVAILABLE_MOVE_COLOR)
                                    available_moves = self.model.get_available_moves(x, y)
                                    for a in available_moves:
                                        self.change_cell_color(a[0], a[1], AVAILABLE_MOVE_COLOR)
                                    self.last_selected = (x, y)
                                else:
                                    should_move_to_none_state = True

                    if should_move_to_none_state:
                        for a in available_moves:
                            self.change_cell_color(a[0], a[1], CHECKERS_BACKGROUND_COLOR)
                        self.change_cell_color(self.last_selected[0], self.last_selected[1], CHECKERS_BACKGROUND_COLOR)
                        self.state = STATES["None"]

        elif self.game_mode == GAME_MODES["playerVsPRO"]:
            pass