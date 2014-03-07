import math
from model import GameModel, BOARD_SIZE

__author__ = 'vladvalt'

MOVE_TYPES = {"simple": 1, "attack": 2}


class CheckersGameModel(GameModel):

    def __init__(self):
        self.board_size= 8
        self.last_move_type = MOVE_TYPES["simple"]
        self.last_move = None
        GameModel.__init__(self)

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
                if move_type == MOVE_TYPES["simple"]:
                    self.perform_simple_move(x, y, x_new, y_new)
                    self.last_move = (x_new, y_new)
                    self.last_move_type = MOVE_TYPES["simple"]
                    return True
                elif move_type == MOVE_TYPES["attack"]:
                    self.perform_attack_move(x, y, x_new, y_new)
                    self.last_move = (x_new, y_new)
                    self.last_move_type = MOVE_TYPES["attack"]
                    return True
        return False

    def perform_simple_move(self, x, y, x_new, y_new):
        self.board_position[x_new][y_new] = self.board_position[x][y]
        self.board_position[x][y] = 0
        self.current_player = 3 - self.current_player

    def perform_attack_move(self, x, y, x_new, y_new):
        self.board_position[x_new][y_new] = self.board_position[x][y]
        x_step = int(math.copysign(1, x_new - x))
        y_step = int(math.copysign(1, y_new - y))
        for i in range(int(math.fabs(x_new - x))):
            self.board_position[x + x_step * i][y + y_step * i] = 0
        if self.get_move_type(x_new, y_new) == MOVE_TYPES["simple"]:
            self.current_player = 3 - self.current_player
        #TODO hold selection on attack checker

    def is_able_to_move(self, x, y):
        if self.is_figure_of_current_player(x, y):
            #TODO optimise later
            if self.should_attack_on_this_move():
                if self.get_move_type(x, y) == MOVE_TYPES["attack"]:
                    #self.last_move_type = MOVE_TYPES["attack"]
                    return True
            elif len(self.get_available_moves(x, y)) > 0:
                #self.last_move_type = MOVE_TYPES["simple"]
                return True
        return False

    def get_move_type(self, x, y):
        if self.is_figure_king(x, y):
            #TODO
            pass
        else:
            curr_f = self.board_position[x][y]
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
        #todo think about king but now is ok for simple
        if self.board_position[x][y] == 0:
            return None
        if self.board_position[x_new][y_new] == 0 and math.fabs(x - x_new) > 1:
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
        #TODO rewrite according to the attack
        #TODO rewrite according to the kings
        available_moves = []
        move_type = self.get_move_type(x, y)
        if move_type == MOVE_TYPES["simple"]:
            if self.is_figure_king(x, y):
                pass
            else:
                if y > 0 and self.board_position[x + self.get_move_direction()][y - 1] == 0:
                    available_moves.append((x + self.get_move_direction(), y - 1))
                if y < self.board_size - 1 and self.board_position[x + self.get_move_direction()][y + 1] == 0:
                    available_moves.append((x + self.get_move_direction(), y + 1))
        elif move_type == MOVE_TYPES["attack"]:
            if self.is_figure_king(x, y):
                pass
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

    def is_free_to_diselect(self):
        return not (self.last_move_type == MOVE_TYPES["attack"] and self.should_continue_atack())

    def should_continue_atack(self):
        return self.get_move_type(self.last_move[0], self.last_move[1]) == MOVE_TYPES["attack"]