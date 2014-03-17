from model import GameModel
from reversi import ReversiGame

__author__ = 'danylo'


class ReversiGameModel(GameModel):
    def __init__(self):
        GameModel.__init__(self)
        self.game = ReversiGame(8)
        self.current_player = 0

    def is_over(self):
        return self.game.is_over()

    def get_winner(self):
        return self.game.get_winner()

    def get_current_player(self):
        return self.current_player

    def get_available_moves(self):
        return self.game.get_valid_moves(self.get_current_player())

    def get_cell_index(self, number):
        return [number / self.game.size, number % self.game.size]

    def get_cell(self, index):
        return self.game.board[index / self.game.size][index % self.game.size]

    def move_human(self, x, y):
        self.game.move(self.current_player, x, y)

    def move_computer(self, difficulty):
        # Search depth for ai
        search_depth = difficulty + 1

        if difficulty < 2:
            pass
        elif difficulty == 2:
            pass
        else:
            # Search depth can be increased by the end of the game
            if self.game.cells_count - (self.game.score[0] + self.game.score[1]) < 2 * difficulty:
                search_depth = self.game.cells_count - (self.game.score[0] + self.game.score[1])

        self.game.move_ai(self.current_player, search_depth)
