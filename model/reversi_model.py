from model import GameModel
from reversi_engine import ReversiEngine

__author__ = 'danylo'


class ReversiGameModel():
    def __init__(self, first_player, difficulty):
        self.board_size = 8
        self.difficulty = difficulty
        self.engine = ReversiEngine(self.board_size)
        self.current_player = first_player

    def get_difficulty(self):
        return self.difficulty

    def set_difficulty(self, diff):
        if diff < 0:
            raise Exception("Negative difficulty level")
        self.difficulty = diff

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

    def move_computer(self):
        # Search depth for ai
        search_depth = self.difficulty + 1

        # The number of empty cells
        remaining_cells = self.engine.cells_count - (self.engine.score[0] + self.engine.score[1])

        # Tweaks for hard levels
        if self.difficulty >= 2:
            # Number of free cells that require specific logic
            threshold = self.board_size - 1
            if self.difficulty > 4:
                threshold += self.board_size
            elif self.difficulty == 4 or self.difficulty == 3:
                threshold += self.difficulty

            # Search depth can be increased by the end of the game
            if remaining_cells <= threshold:
                search_depth = remaining_cells

        self.engine.move_ai(self.current_player, search_depth)
        self.current_player = self.engine.get_opponent(self.current_player)

    def move_enemy(self):
        pass