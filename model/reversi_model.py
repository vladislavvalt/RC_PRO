from model import GameModel
from reversi_engine import ReversiEngine

__author__ = 'danylo'


class ReversiGameModel():
    def __init__(self, first_player):
        self.board_size = 8
        self.engine = ReversiEngine(self.board_size)
        self.current_player = first_player

    def is_over(self):
        return self.engine.is_over()

    def get_winner(self):
        return self.engine.get_winner()

    def get_current_player(self):
        return self.current_player

    def get_current_opponent(self):
        return self.engine.get_opponent(self.current_player)

    def get_available_moves(self):
        return self.engine.get_valid_moves(self.current_player)

    def get_cell(self, x, y):
        return self.engine.board[x][y]

    def move_human(self, x, y):
        self.engine.move(self.current_player, x, y)
        self.current_player = self.engine.get_opponent(self.current_player)

    def move_computer(self, difficulty):
        # Search depth for ai
        search_depth = difficulty + 1

        # The number of empty cells
        remaining_cells = self.engine.cells_count - (self.engine.score[0] + self.engine.score[1])

        if difficulty >= 2:
            # Search depth can be increased by the end of the game
            if remaining_cells < self.board_size + difficulty:
                search_depth = remaining_cells
            # Or it can be decreased at the beginning for performance reasons
            elif remaining_cells > self.engine.cells_count / 2 and search_depth > 1:
                search_depth -= 1

        self.engine.move_ai(self.current_player, search_depth)
        self.current_player = self.engine.get_opponent(self.current_player)

    def move_enemy(self):
        pass