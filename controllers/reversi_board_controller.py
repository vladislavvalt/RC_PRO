from controllers.common_board_controller import GAME_MODES
from controllers.common_board_controller import CommonBoardController

__author__ = 'vladvalt'

FILLER_MAP = {0: None, 1: "reversi_black", 2: "reversi_white", 3: "reversi_available_move"}

AVAILABLE_MOVE_COLOR = "green"
BACKGROUND_COLOR = "brown"


class ReversiBoardController(CommonBoardController):
    def __init__(self, model, mode):
        CommonBoardController.__init__(self, model=model)
        self.game_mode = mode
        if mode == GAME_MODES["playerVsPRO"]:
            self.computer = self.model.get_current_opponent()
            self.difficulty = 3
            self.the_end = False

    def fill_board(self):
        self.board.parent.title('Reversi')

        for i in range(self.model.board_size):
            for j in range(self.model.board_size):
                value = self.model.get_cell(i, j)
                if value == 0:
                    self.clear_cell(i, j)
                else:
                    self.fill_cell(i, j, FILLER_MAP[value])

        if not self.model.is_over():
            available_moves = self.model.get_available_moves()
            for a in available_moves:
                self.fill_cell(a[0], a[1], FILLER_MAP[3])

    def on_cell_click(self, event, x, y):
        if self.game_mode == GAME_MODES["playerVSPlayer"]:
            self.move_human(x, y)
        elif self.game_mode == GAME_MODES["playerVsPRO"]:
            if self.model.get_current_player() == self.computer:
                self.move_computer(self.difficulty)
            else:
                self.move_human(x, y)

        if not self.the_end:
            if self.model.is_over():
                self.write_to_console("Game over!")
                if self.model.get_winner() == 0:
                    self.write_to_console("Draw...")
                else:
                    self.write_to_console("The winner is player " + str(self.model.get_winner()))
                self.the_end = True

    def move_human(self, x, y):
        if not self.model.is_over():
            available_moves = self.model.get_available_moves()
            if (x, y) in available_moves:
                self.model.move_human(x, y)
                self.fill_board()
            elif available_moves == [self.model.engine.pass_move]:
                self.move_human(available_moves[0][0], available_moves[0][1])
                self.write_to_console("Pass")

    def move_computer(self, difficulty):
        self.model.move_computer(difficulty)
        self.fill_board()