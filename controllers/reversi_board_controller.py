from controllers.common_board_controller import GAME_MODES
from controllers.common_board_controller import CommonBoardController

__author__ = 'danylofitel'

FILLER_MAP = {0: None,
              1: "reversi_black",
              2: "reversi_white",
              3: "reversi_available_move_black",
              4: "reversi_available_move_white"}


class ReversiBoardController(CommonBoardController):
    def __init__(self, model, mode, player_moves_first):
        CommonBoardController.__init__(self, model=model)
        self.game_mode = mode
        self.game_finished = False
        if mode == GAME_MODES["playerVSPro"]:
            if player_moves_first:
                self.computer = self.model.get_current_opponent()
            else:
                self.computer = self.model.get_current_player()
                self.model.move_computer()

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
                if not a == self.model.engine.pass_move:
                    filler = self.model.get_current_player() + 2
                    self.fill_cell(a[0], a[1], FILLER_MAP[filler])

    def on_cell_click(self, event, x, y):
        if self.game_finished:
            return

        if self.game_mode == GAME_MODES["playerVSPlayer"]:
            self.move_human(x, y)
        elif self.game_mode == GAME_MODES["playerVSPro"]:
            if self.model.get_current_player() == self.computer:
                self.move_computer()
            else:
                self.move_human(x, y)

        if not self.game_finished:
            if self.model.is_over():
                self.write_to_console("Game over!!!")
                if self.model.get_winner() == 0:
                    self.write_to_console("Draw...")
                else:
                    winner = self.model.get_winner()
                    loser = self.model.engine.get_opponent(winner)
                    score_winner = self.model.engine.get_score(winner)
                    score_loser = self.model.engine.get_score(loser)
                    score = str(score_winner) + ":" + str(score_loser)

                    if self.game_mode == GAME_MODES["playerVSPlayer"]:
                        self.write_to_console("Player " + str(winner) + " has won with score " + score)
                    elif self.game_mode == GAME_MODES["playerVSPro"]:
                        if self.model.get_winner() == self.computer:
                            self.write_to_console("Computer has won with score " + score)
                            self.write_to_console("I'm the best here!!! Keep trying, looser!")
                        else:
                            self.write_to_console("Player has won with score " + score)
                            self.write_to_console("Okay, okay, this time you win!")
                self.game_finished = True

    def move_human(self, x, y):
        if not self.model.is_over():
            available_moves = self.model.get_available_moves()
            if (x, y) in available_moves:
                move = "(" + str(x) + ", " + str(y) + ")"
                self.model.move_human(x, y)
                if self.game_mode == GAME_MODES["playerVSPlayer"]:
                    self.write_to_console("Player " + str(self.model.get_current_player()) + " moves to " + move)
                elif self.game_mode == GAME_MODES["playerVSPro"]:
                    self.write_to_console("Player moves to " + move)
            elif available_moves == [self.model.engine.pass_move]:
                self.model.move_human(available_moves[0][0], available_moves[0][1])
                if self.game_mode == GAME_MODES["playerVSPlayer"]:
                    self.write_to_console("Player " + str(self.model.get_current_player()) + " passes")
                elif self.game_mode == GAME_MODES["playerVSPro"]:
                    self.write_to_console("Player passes")
            self.fill_board()

    def move_computer(self):
        if not self.model.is_over():
            if self.model.get_available_moves() == [self.model.engine.pass_move]:
                self.write_to_console("Computer passes")
            move = self.model.move_computer()
            self.write_to_console("Computer moves to " + str(move[0]))
            self.fill_board()