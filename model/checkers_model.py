import math
from model import GameModel, BOARD_SIZE

__author__ = 'vladvalt'

MOVE_TYPES = {"simple": 1, "attack": 2}

DELTA = [
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1)
]

MAX_NUMBER_OF_SIMPLE_MOVES_IN_SERIES = 30


class CheckersGameModel(GameModel):

    def __init__(self):
        self.board_size= 8
        self.last_move_type = MOVE_TYPES["simple"]
        self.last_move = None
        self.number_of_simple_moves_in_series = 0
        GameModel.__init__(self)

    def number_of_checkers_left(self, player):
        number = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board_position[i][j] == player or self.board_position[i][j] == player + 2:
                    number += 1
        return number

    def create_board(self):
        self.board_position = [[0 for j in range(self.board_size)] for i in range(self.board_size)]

        k = 1
        for i in range(self.board_size):
            for j in range(self.board_size):
                if i * self.board_size + j == k:
                    if k % 8 == -1 or k % 8 == 7:
                        k += 1
                    elif k % 8 == -2 or k % 8 == 6:
                        k += 3
                    else:
                        k += 2
                    if i * self.board_size + j < 3 * BOARD_SIZE / 8:
                        self.board_position[i][j] = 2
                    if i * self.board_size + j >= 5 * BOARD_SIZE / 8:
                        self.board_position[i][j] = 1

        #for i in range(8):
        #    for j in range(8):
        #        print self.board_position[i][j],
        #    print ''

    def move(self, x, y, x_new, y_new):
        if (x_new, y_new) in self.get_available_moves(x, y):
            move_type = self.get_move_type(x, y)
            if move_type == self.get_move_type_concrete(x, y, x_new, y_new):
                is_ok = False
                if move_type == MOVE_TYPES["simple"]:
                    self.perform_simple_move(x, y, x_new, y_new)
                    is_ok = True

                elif move_type == MOVE_TYPES["attack"]:
                    self.perform_attack_move(x, y, x_new, y_new)
                    is_ok = True

                if is_ok:
                    self.last_move = (x_new, y_new)
                    self.last_move_type = move_type
                    self.check_for_game_end()
                    return True
        return False

    def check_for_game_end(self):
        if self.number_of_simple_moves_in_series >= MAX_NUMBER_OF_SIMPLE_MOVES_IN_SERIES:
                        self.is_game_over = True
                        self.winner = 0
        if self.number_of_checkers_left(1) == 0:
            self.is_game_over = True
            self.winner = 2
        elif self.number_of_checkers_left(2) == 0:
            self.is_game_over = True
            self.winner = 1
        elif not self.is_able_to_move_any():
            self.is_game_over = True
            self.winner = 3 - self.current_player

    def promote_checker(self, x, y):
        if not self.is_figure_king(x, y):
            if (x == 0 and self.board_position[x][y] == 1) or (x == self.board_size - 1 and self.board_position[x][y] == 2):
                self.board_position[x][y] += 2

    def perform_simple_move(self, x, y, x_new, y_new):
        self.board_position[x_new][y_new] = self.board_position[x][y]
        self.board_position[x][y] = 0
        self.promote_checker(x_new, y_new)
        self.current_player = 3 - self.current_player
        self.number_of_simple_moves_in_series += 1

    def perform_attack_move(self, x, y, x_new, y_new):
        self.board_position[x_new][y_new] = self.board_position[x][y]
        x_step = int(math.copysign(1, x_new - x))
        y_step = int(math.copysign(1, y_new - y))
        for i in range(int(math.fabs(x_new - x))):
            self.board_position[x + x_step * i][y + y_step * i] = 0
        self.promote_checker(x_new, y_new)
        if self.get_move_type(x_new, y_new) == MOVE_TYPES["simple"]:
            self.current_player = 3 - self.current_player
        self.number_of_simple_moves_in_series = 0

    def is_able_to_move_any(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board_position[i][j] != 0:
                    if self.is_able_to_move(i, j):
                        return True
        return False

    def is_able_to_move(self, x, y):
        if not self.is_game_over and self.is_figure_of_current_player(x, y):
            if self.should_attack_on_this_move():
                if self.get_move_type(x, y) == MOVE_TYPES["attack"]:
                    return True
            elif len(self.get_available_moves(x, y)) > 0:
                return True
        return False

    def get_move_type(self, x, y):
        curr_f = self.board_position[x][y]
        if self.is_figure_king(x, y):
            n = max(self.board_size - x + 1, x + 1)
            for d in DELTA:
                for i in range(1, n):
                    if x + i * d[0] < self.board_size - 1 and y + i * d[1] < self.board_size - 1:
                        if x + i * d[0] > 0 and y + i * d[1] > 0:
                            if self.board_position[x + i * d[0]][y + i * d[1]] != 0:
                                if self.is_figures_of_the_same_type(x, y, x + i * d[0], y + i * d[1]):
                                    break
                                else:
                                    if self.board_position[x + (i + 1) * d[0]][y + (i + 1) * d[1]] == 0:
                                        return MOVE_TYPES["attack"]
                                    else:
                                        break
        else:
            if x > 1 and y > 1 and self.board_position[x-1][y-1] != 0:
                if (self.board_position[x-1][y-1] - curr_f) % 2 != 0 and self.board_position[x-2][y-2] == 0:
                    return MOVE_TYPES["attack"]
            if x < self.board_size - 2 and y < self.board_size - 2 and self.board_position[x+1][y+1] != 0:
                if (self.board_position[x+1][y+1] - curr_f) % 2 != 0 and self.board_position[x+2][y+2] == 0:
                    return MOVE_TYPES["attack"]
            if x > 1 and y < self.board_size - 2 and self.board_position[x-1][y+1] != 0:
                if (self.board_position[x-1][y+1] - curr_f) % 2 != 0 and self.board_position[x-2][y+2] == 0:
                    return MOVE_TYPES["attack"]
            if x < self.board_size - 2 and y > 1 and self.board_position[x+1][y-1] != 0:
                if (self.board_position[x+1][y-1] - curr_f) % 2 != 0 and self.board_position[x+2][y-2] == 0:
                    return MOVE_TYPES["attack"]

        return MOVE_TYPES["simple"]

    def get_move_type_concrete(self, x, y, x_new, y_new):
        if self.board_position[x][y] == 0:
            return None
        x_step = int(math.copysign(1, x_new - x))
        y_step = int(math.copysign(1, y_new - y))
        for i in range(1, int(math.fabs(x_new - x))):
            if self.board_position[x + x_step * i][y + y_step * i] != 0:
                return MOVE_TYPES["attack"]
        return MOVE_TYPES["simple"]

    def get_move_direction(self):
        if self.current_player == 1:
            return -1
        else:
            return 1

    def is_figure_of_current_player(self, x, y):
        return self.board_position[x][y] == self.current_player or self.board_position[x][y] == self.current_player + 2

    def should_attack_on_this_move(self):
        should_attack = False
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.is_figure_of_current_player(i, j):
                    if self.get_move_type(i, j) == MOVE_TYPES["attack"]:
                        should_attack = True
                        break
        return should_attack

    def is_figure_king(self, x, y):
        return self.board_position[x][y] == 3 or self.board_position[x][y] == 4

    def get_available_moves(self, x, y):
        available_moves = []
        move_type = self.get_move_type(x, y)
        if move_type == MOVE_TYPES["simple"]:
            if self.is_figure_king(x, y):
                n = max(self.board_size - x + 1, x + 1)
                for d in DELTA:
                    for i in range(1, n):
                        if x + i * d[0] < self.board_size and y + i * d[1] < self.board_size:
                            if x + i * d[0] >= 0 and y + i * d[1] >= 0:
                                if self.board_position[x + i * d[0]][y + i * d[1]] != 0:
                                    break
                                available_moves.append((x + i * d[0], y + i * d[1]))
            else:
                if y > 0 and self.board_position[x + self.get_move_direction()][y - 1] == 0:
                    available_moves.append((x + self.get_move_direction(), y - 1))
                if y < self.board_size - 1 and self.board_position[x + self.get_move_direction()][y + 1] == 0:
                    available_moves.append((x + self.get_move_direction(), y + 1))
        elif move_type == MOVE_TYPES["attack"]:
            if self.is_figure_king(x, y):
                n = max(self.board_size - x + 1, x + 1)
                for d in DELTA:
                    for i in range(1, n):
                        if x + i * d[0] < self.board_size - 1 and y + i * d[1] < self.board_size - 1:
                            if x + i * d[0] > 0 and y + i * d[1] > 0:
                                if self.board_position[x + i * d[0]][y + i * d[1]] != 0:
                                    if self.is_figures_of_the_same_type(x, y, x + i * d[0], y + i * d[1]):
                                        break
                                    else:
                                        if self.board_position[x + (i + 1) * d[0]][y + (i + 1) * d[1]] == 0:
                                            for j in range(i+1, n):
                                                if x + j * d[0] < self.board_size and y + j * d[1] < self.board_size:
                                                    if x + j * d[0] >= 0 and y + j * d[1] >= 0:
                                                        if self.board_position[x + j * d[0]][y + j * d[1]] == 0:
                                                            available_moves.append((x + j * d[0], y + j * d[1]))
                                                        else:
                                                            break
                                            break
                                        else:
                                            break
            else:
                curr_f = self.board_position[x][y]
                if x > 1 and y > 1 and self.board_position[x-1][y-1] != 0:
                    if (self.board_position[x-1][y-1] - curr_f) % 2 != 0 and self.board_position[x-2][y-2] == 0:
                        available_moves.append((x-2, y-2))
                if x < self.board_size - 2 and y < self.board_size - 2 and self.board_position[x+1][y+1] != 0:
                    if (self.board_position[x+1][y+1] - curr_f) % 2 != 0 and self.board_position[x+2][y+2] == 0:
                        available_moves.append((x+2, y+2))
                if x > 1 and y < self.board_size - 2 and self.board_position[x-1][y+1] != 0:
                    if (self.board_position[x-1][y+1] - curr_f) % 2 != 0 and self.board_position[x-2][y+2] == 0:
                        available_moves.append((x-2, y+2))
                if x < self.board_size - 2 and y > 1 and self.board_position[x+1][y-1] != 0:
                    if (self.board_position[x+1][y-1] - curr_f) % 2 != 0 and self.board_position[x+2][y-2] == 0:
                        available_moves.append((x+2, y-2))
        return available_moves

    def is_figures_of_the_same_type(self, x, y, a, b):
        if self.board_position[x][y] != 0 and self.board_position[a][b] != 0:
            if (self.board_position[a][b] - self.board_position[x][y]) % 2 == 0:
                return True
        return False

    def number_of_checkers_left(self, player_num):
        number = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board_position[i][j] == player_num or self.board_position[i][j] == player_num + 2:
                    number += 1
        return number

    def is_free_to_deselect(self):
        return not (self.last_move_type == MOVE_TYPES["attack"] and self.should_continue_attack())

    def should_continue_attack(self):
        return self.get_move_type(self.last_move[0], self.last_move[1]) == MOVE_TYPES["attack"]