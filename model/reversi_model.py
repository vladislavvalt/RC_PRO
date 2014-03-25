from reversi_engine import ReversiEngine

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
        self.current_player = self.engine.get_opponent(self.current_player)

    def get_search_depth(self, difficulty):
        # Search depth directly depends on the difficulty level
        search_depth = self.difficulty + 1

        total_cells = self.engine.cells_count
        filled_cells = self.engine.get_score(1) + self.engine.get_score(2)
        empty_cells = total_cells - filled_cells

        # Tweaks for hard levels
        if self.difficulty >= 2:
            # Search depth can be increased when most of the cells are filled
            if empty_cells < filled_cells:
                # Every 10% of filled cells after 50% increase the search depth by 1
                search_depth += int(10 * (filled_cells / float(total_cells) - 0.5))

            # It is possible to search to the end at some point
            if search_depth < empty_cells:
                threshold = self.board_size
                if self.difficulty > 4:
                    threshold += self.difficulty
                elif self.difficulty == 4 or self.difficulty == 3 or self.difficulty == 2:
                    threshold += self.difficulty / 2

                # Search depth can be increased by the end of the game
                if empty_cells <= threshold:
                    search_depth = empty_cells + 1

        return search_depth

    def move_computer(self):
        self.engine.move_ai(self.current_player, self.get_search_depth(self.difficulty))
        self.current_player = self.engine.get_opponent(self.current_player)
