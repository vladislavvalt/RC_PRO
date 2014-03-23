import random

__author__ = 'vladvalt'


class CheckersBot:

    def __init__(self, model):
        self.model = model
        self.player = 2
        self.move_delay = 0
        self.depth = 1

    def move(self):
        return self.perform_random_move()

    def perform_random_move(self):
        available_moves = self.find_available_moves(self.model)
        if not available_moves is None and len(available_moves) > 0:
            start_pos = random.choice(available_moves)
            move = (start_pos[0], random.choice(start_pos[1]))
            self.model.move(move[0][0], move[0][1], move[1][0], move[1][1])
            return move
        return None

    def perform_model_based_move(self):
        pass

    def perform_heuristic_move(self):
        pass

    # forms tuple, first element of tuple is starting position of figure
    # the second element is array of available moves from position
    def find_available_moves(self, model):
        available_moves = []
        for i in range(self.model.board_size):
            for j in range(self.model.board_size):
                if self.model.is_figure_of_current_player(i, j):
                    if self.model.is_able_to_move(i, j):
                        moves = model.get_available_moves(i, j)
                        if not moves is None and len(moves) > 0:
                            available_moves.append(((i, j), model.get_available_moves(i, j)))
        #print available_moves
        return available_moves