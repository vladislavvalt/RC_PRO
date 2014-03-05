__author__ = 'danylo'

BOARD_SIZE = 64


class GameModel:

    def create_board(self):
        board_position = [0 for i in range(BOARD_SIZE)]
        board_position[28] = 1
        board_position[27] = 1
        board_position[36] = 1
        board_position[35] = 1
        return board_position

    def __init__(self):
        self.winner = None
        self.is_game_over = False
        self.current_player = 1
        self.board_position = self.create_board()
        self.current_state = 0


    def is_game_over(self):
        return self.is_game_over

    ## return the winner of game
    def winner(self):
        return self.winner

    # who moves now
    def get_current_player(self):
        pass

    def get_available_moves(self):
        ##
        pass


    #TODO implement method move in derivative class


#board_position = [0 for i in range(64)]
#board_position[28] = 1
#board_position[27] = 1
#board_position[36] = 1
#board_position[35] = 1
#
#
#for i in range(8):
#    x = i * 8
#    print ''
#    for j in range(8):
#        print board_position[x + j],
