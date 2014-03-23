import math
from threading import Thread
import time
from controllers.common_board_controller import CommonBoardController, GAME_MODES
from model.checkers_model import MOVE_TYPES

__author__ = 'vladvalt'

FILLER_MAP = {0: None, 1: "checker_white", 2: "checker_black", 3: "checker_king_white", 4: "checker_king_black"}

AVAILABLE_MOVE_COLOR = "green"
CHECKERS_BACKGROUND_COLOR = "brown"

STATES = {"None": 0, "checker_selected": 1}


class CheckersBoardController(CommonBoardController):

    def __init__(self, model, bot):
        CommonBoardController.__init__(self, model=model)
        self.game_mode = GAME_MODES["playerVsPRO"]
        self.state = STATES["None"]
        self.last_selected = None
        self.the_end = False
        self.bot = bot
        self.bot_move_delay = 1
        self.should_show_bot_play_on_board = True
        self.should_log_the_game = True
        self.should_log_the_game_on_board = True

    def fill_board(self):
        self.board.parent.title('Checkers')
        for i in range(self.model.board_size):
            for j in range(self.model.board_size):
                self.fill_cell(i, j, FILLER_MAP[self.model.board_position[i][j]])

    def simple_move(self, x, y, x_new, y_new):
        figure = self.model.board_position[x_new][y_new]
        self.fill_cell(x_new, y_new, FILLER_MAP[figure])
        self.clear_cell(x, y)

    def attack_move(self, x, y, x_new, y_new):
        figure = self.model.board_position[x_new][y_new]
        self.fill_cell(x_new, y_new, FILLER_MAP[figure])
        x_step = int(math.copysign(1, x_new - x))
        y_step = int(math.copysign(1, y_new - y))
        for i in range(int(math.fabs(x_new - x))):
            self.clear_cell(x + x_step * i, y + y_step * i)

    def perform_bot_move(self):
        class BotMovePerformer(Thread):

            def set_controller(self, controller):
                self.controller = controller

            def run(self):
                current_player = self.controller.model.current_player
                bot_move = self.controller.bot.move()
                time.sleep(self.controller.bot_move_delay)

                if not bot_move is None:
                    if self.controller.should_show_bot_play_on_board:
                        if self.controller.model.last_move_type == MOVE_TYPES["simple"]:
                            self.controller.simple_move(bot_move[0][0], bot_move[0][1], bot_move[1][0], bot_move[1][1])
                        elif self.controller.model.last_move_type == MOVE_TYPES["attack"]:
                            self.controller.attack_move(bot_move[0][0], bot_move[0][1], bot_move[1][0], bot_move[1][1])
                    if self.controller.should_log_the_game or self.controller.should_log_the_game_on_board:
                        txt_to_write = "Move of player " + str(current_player) \
                                       + ": from " + str(bot_move[0]) + " to " + str(bot_move[1])
                        if self.controller.should_log_the_game:
                            print txt_to_write
                        if self.controller.should_log_the_game_on_board:
                            self.controller.write_to_console(txt_to_write)

                    if self.controller.model.current_player == 2 and self.controller.model.should_continue_attack():
                        self.controller.perform_bot_move()

        bot_move_performer = BotMovePerformer()
        bot_move_performer.set_controller(self)
        bot_move_performer.start()
        if self.game_mode == GAME_MODES["PROvsPRO"]:
            bot_move_performer.join()

    def on_cell_click(self, event, x, y):
        if self.game_mode == GAME_MODES["playerVSPlayer"] or self.game_mode == GAME_MODES["playerVsPRO"]:
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
                    should_bot_move_after = True
                    available_moves = self.model.get_available_moves(self.last_selected[0], self.last_selected[1])

                    if self.last_selected[0] == x and self.last_selected[1] == y and self.model.is_free_to_deselect():
                        should_bot_move_after = False
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
                                    self.change_cell_color(self.last_selected[0], self.last_selected[1],
                                                           CHECKERS_BACKGROUND_COLOR)
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

                    if self.game_mode == GAME_MODES["playerVsPRO"] and should_move_to_none_state and should_bot_move_after:
                        self.perform_bot_move()

            if not self.the_end:
                if self.model.is_game_over:
                    if self.should_log_the_game:
                        print "Game over!"
                    if self.should_log_the_game_on_board:
                        self.write_to_console("Game over!")
                    if self.model.winner == 0:
                        if self.should_log_the_game:
                            print "Standoff..."
                        if self.should_log_the_game_on_board:
                            self.write_to_console("Standoff...")
                    else:
                        if self.should_log_the_game:
                            print "The winner is player " + str(self.model.winner)
                        if self.should_log_the_game_on_board:
                            self.write_to_console("The winner is player " + str(self.model.winner))
                    self.the_end = True

    def start_bot_play(self):

        class BotGamePerformer(Thread):

            def set_controller(self, controller):
                self.controller = controller

            def run(self):
                time.sleep(1)
                while not self.controller.the_end:
                    self.controller.perform_bot_move()
                    if self.controller.model.is_game_over:
                        if self.controller.should_log_the_game:
                            print "Game over!"
                        if self.controller.should_log_the_game_on_board:
                            self.controller.write_to_console("Game over!")
                        if self.controller.model.winner == 0:
                            if self.controller.should_log_the_game:
                                print "Standoff..."
                            if self.controller.should_log_the_game_on_board:
                                self.controller.write_to_console("Standoff...")
                        else:
                            if self.controller.should_log_the_game:
                                print "The winner is player " + str(self.controller.model.winner)
                            if self.controller.should_log_the_game_on_board:
                                self.controller.write_to_console("The winner is player " + str(self.controller.model.winner))
                        self.controller.the_end = True

        if self.game_mode == GAME_MODES["PROvsPRO"]:
            bot_game_perofmer = BotGamePerformer()
            bot_game_perofmer.set_controller(self)
            bot_game_perofmer.start()