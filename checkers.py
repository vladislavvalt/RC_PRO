from Tkinter import Tk
import time
import sys
from ai.checkers_bot import CheckersBot
from controllers.checkers_board_controller import CheckersBoardController
from controllers.common_board_controller import GAME_MODES
from model.checkers_model import CheckersGameModel
from ui.board_common import BoardCommonUI

__author__ = 'vladvalt'

##The place to start checkers


def checkers(game_bot):
    #Reserve it for demo usage
    #total = len(sys.argv)
    #cmd_args = str(sys.argv)
    #print ("The total numbers of args passed to the script: %d " % total)
    #print ("Args list: %s " % cmd_args)

    root = Tk()
    model = CheckersGameModel()
    game_bot.model = model
    controller = CheckersBoardController(model=model, bot=game_bot)
    controller.game_mode = GAME_MODES["playerVSPro"]
    controller.bot_move_delay = 0.3
    controller.should_show_bot_play_on_board = True
    controller.should_log_the_game = True
    app = BoardCommonUI(master=root, controller=controller)
    controller.fill_board()
    if controller.game_mode == GAME_MODES["proVSPro"]:
        controller.start_bot_play()

    root.mainloop()


def improve_skill(bot, number_of_games):
    for i in range(number_of_games):
        print("IMPROVE ITERATION NUMBER " + str(i))
        model = CheckersGameModel()
        bot.model = model
        controller = CheckersBoardController(model=model, bot=bot)
        controller.bot_move_delay = 0
        controller.game_mode = GAME_MODES["proVSPro"]
        controller.should_show_bot_play_on_board = False
        controller.should_log_the_game_on_board = False
        controller.should_log_the_game = True
        controller.start_bot_play()
        while not controller.the_end:
            time.sleep(0.001)
        print()
        print()

bot = CheckersBot(None)
#improve_skill(bot, 2)
checkers(bot)