from ai.reversi_engine import ReversiEngine

__author__ = 'danylofitel'


class ReversiGameModel():
    def __init__(self, difficulty):
        self.board_size = 8
        self.difficulty = difficulty
        self.engine = ReversiEngine(self.board_size)
        self.first_player = self.engine.first
        self.current_player = self.first_player

    def is_over(self):
        return self.engine.is_over()

    def get_winner(self):
        return self.engine.get_winner()

    def switch_current_player(self):
        self.current_player = self.engine.get_opponent(self.current_player)

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
        self.switch_current_player()

    def move_computer(self):
        move = self.engine.move_ai(self.current_player, self.difficulty)
        self.switch_current_player()
        return move