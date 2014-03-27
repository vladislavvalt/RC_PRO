__author__ = 'danylofitel'


from xmlrpclib import ServerProxy

from ai.reversi_engine import ReversiEngine

game_server = ServerProxy("http://ai-labs.org:8006")
game_id = game_server.start_game('den.ftl@gmail.com')

# 1 - player id, 2 - server's player id
player = 1
server = 2


def get_score(board_list):
    scores = [0, 0]
    for i in board_list:
        for j in i:
            if not j == 0:
                scores[j - 1] += 1
    return scores

ai = ReversiEngine(8)
difficulty = 2

step = 0
while True:
    print '==============================='
    board = game_server.get_board_state(game_id)
    print board

    ai.board = board
    ai.score = get_score(board)

    x, y = ai.get_best_move(player, difficulty)[0]

    state = game_server.move(x, y, game_id)

    step += 1

    board = game_server.get_board_state(game_id)
    print '_______________________________'
    print board
    print state
    score = get_score(board)
    if state[1] == 'game_over':
        if score[1] > score[2]:
            print "YOU'VE WON!!!", 'in ', step, 'steps'
        if score[1] == score[2]:
            print 'EQUAL SCORE', 'in ', step, 'steps'
        if score[1] < score[2]:
            print "YOU'VE LOST", 'in ', step, 'steps'

        print 'SCORE', board.score(1), board.score(2)
        break

print 'exiting'

