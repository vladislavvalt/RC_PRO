from model import GameModel, BOARD_SIZE

__author__ = 'vladvalt'


class CheckersGameModel(GameModel):

    def __init__(self):
        self.board_size= 8
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

        for i in range(8):
            for j in range(8):
                print self.board_position[i][j],
            print ''

    def get_available_moves(self):
        return [(1,1),(1,5),(1,6)]

    def get_available_moves(self, x, y):
        return [(1,1),(1,5),(1,6)]