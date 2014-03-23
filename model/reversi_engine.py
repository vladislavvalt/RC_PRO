__author__ = "danylo"

from random import randrange


# Integer constants representing infinity
int_max = 1000000000
int_min = -int_max


# Reversi game engine
class ReversiEngine(object):
    # States of a cell and player titles
    empty = 0
    first = 1
    second = 2

    # List of possible directions from the cell
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    # A special index for specifying pass
    pass_move = (-1, -1)

    # Construct a game board
    def __init__(self, board_size):
        # Size of the square board
        self.size = board_size
        self.cells_count = self.size ** 2

        # A list of board columns
        self.board = []

        # Fill the board with empty cells
        for col in range(self.size):
            self.board.append([self.empty for i in range(self.size)])

        # Fill the four squares in the middle
        self.board[self.size / 2 - 1][self.size / 2 - 1] = self.first
        self.board[self.size / 2][self.size / 2] = self.first
        self.board[self.size / 2 - 1][self.size / 2] = self.second
        self.board[self.size / 2][self.size / 2 - 1] = self.second

        # Initialize score for both players
        self.score = [2, 2]

        # Bonus points for each corner cell
        self.corner_cell_bonus = self.size

        # Bonus points for each stable cell
        self.stability_bonus = self.size

        # Points for victory
        self.victory_score = int_max

        # A stack of moves
        self.moves_stack = []

    # Represent a game board as a string
    def __repr__(self):
        vertical = "|"
        horizontal_numbers = "   0 1 2 3 4 5 6 7 "

        j = 0
        rep = horizontal_numbers + "\n"
        for x in range(self.size):
            rep += str(j)
            rep += vertical

            for y in range(self.size):
                rep += " " + str(self.board[x][y])
            rep += vertical + "\n"
            j += 1

        return rep

    # Get other player
    def get_opponent(self, player):
        if player == self.first:
            return self.second
        elif player == self.second:
            return self.first
        else:
            raise Exception("Invalid player")

    # Check if the game is over
    def is_over(self):
        # The game is over if all cells are filled
        if self.score[0] + self.score[1] == self.cells_count:
            return True
        # The game is over when none of the players can move
        else:
            return self.get_valid_moves(self.first) == [self.pass_move] and self.get_valid_moves(self.second) == [
                self.pass_move]

    # Get the winner
    def get_winner(self):
        if not self.is_over():
            raise Exception("The game is still in progress")
        else:
            # The first player has won
            if self.score[0] > self.score[1]:
                return self.first
            # The second player has won
            elif self.score[0] < self.score[1]:
                return self.second
            # Both players scored equally, this means draw
            else:
                return None

    # Perform a move
    def move(self, player, x, y):
        # Return an empty list if move is a pass
        if x == self.pass_move[0] and y == self.pass_move[1]:
            return []

        # Make sure the move is valid
        if not self.move_is_valid(player, x, y):
            raise Exception("Invalid move [" + str(x) + ", " + str(y) + "]")

        # Other player
        opponent = self.get_opponent(player)

        # Prepare a list of flipped cells
        flipped_cells = []

        # Mark the cell
        self.board[x][y] = player
        self.score[player - 1] += 1

        # Flip cells in all directions
        for dx, dy in self.directions:
            for cell in self.flip_cells_in_direction(player, x, y, dx, dy):
                flipped_cells.append(cell)
                self.score[player - 1] += 1
                self.score[opponent - 1] -= 1

        # Push the move into the moves stack
        self.moves_stack.append([player, (x, y), flipped_cells])

        # Return the list of opponent's cells that have been flipped
        return flipped_cells

    # Return the board to the state before the move
    def undo_move(self, player, x, y, flipped_cells):
        # The move needs to be undone only if it was not a pass
        if not (x == self.pass_move[0] and y == self.pass_move[1]):
            # Other player
            opponent = self.get_opponent(player)

            # Clear current cell
            self.board[x][y] = self.empty
            self.score[player - 1] -= 1

            # Flip back all cells flipped by the move
            for cell in flipped_cells:
                self.board[cell[0]][cell[1]] = opponent
                self.score[player - 1] -= 1
                self.score[opponent - 1] += 1

    def undo_last_move(self):
        # Check if there are moves in the stack
        if len(self.moves_stack) == 0:
            raise Exception("Moves stack is empty")

        # Get the last move
        last_move = self.moves_stack.pop(len(self.moves_stack) - 1)

        # Undo the last move
        self.undo_move(last_move[0], last_move[1][0], last_move[1][1], last_move[2])

    # Perform a move by current player using built-in AI
    def move_ai(self, player, search_depth):
        # Find the best move for the player
        move = self.get_best_move(player, search_depth)

        # Perform a move
        return self.move(player, move[0][0], move[0][1])

    # Get the player's score
    def get_score(self, player):
        return self.score[player - 1]

    # Get the difference between the player's score and opponent's score
    def get_score_difference(self, player):
        # Return difference between the corresponding scores
        return self.score[player - 1] - self.score[self.get_opponent(player) - 1]

    # Get heuristic score of corner cells
    def get_corner_cells_score_difference(self, player):
        opponent = self.get_opponent(player)

        # Difference between the number of the player's and opponent's corner cells
        corners_count = 0

        # Check all corner cells
        for c in self.get_corners():
            if self.board[c[0]][c[1]] == player:
                corners_count += 1
            elif self.board[c[0]][c[1]] == opponent:
                corners_count -= 1

        # Each corner cell costs additional bonus points
        return self.corner_cell_bonus * corners_count

    # Get heuristic score of stable edges on current board
    def get_stable_cells_score_difference(self, player):
        # All stable cells provide additional bonus score
        return self.stability_bonus * (
            len(self.get_stable_cells(player)) - len(self.get_stable_cells(self.get_opponent(player))))

    # Get heuristic score for the victory of one of the players
    def get_victory_score_difference(self, player):
        # Value of victory in terms of score
        # It must significantly exceed the maximal score actually possible\
        # to prevent situations where loss scores more than victory

        # Return the value only if the game is over
        if self.is_over():
            winner = self.get_winner()

            # The sign of victory score depends on the winner
            if winner == player:
                return self.victory_score
            elif winner == self.get_opponent(player):
                return -self.victory_score
            else:
                return 0
        # Return zero if the game is in progress
        else:
            return 0

    # Get heuristic value of current position
    def get_board_heuristics(self, player):
        # The score is determined by current score, the number of stable cells and state of the game
        return self.get_score_difference(player) + self.get_corner_cells_score_difference(
            player) + self.get_stable_cells_score_difference(player) + self.get_victory_score_difference(player)

    # Check if the cell is on the board
    def is_on_board(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    # Check if the cell is in at the edge of the board
    def is_on_edge(self, x, y):
        min_coord = 0
        max_coord = self.size - 1
        return (x == min_coord or x == max_coord) or (y == min_coord or y == max_coord)

    # Check if the cell is in one of the four corners
    def is_on_corner(self, x, y):
        min_coord = 0
        max_coord = self.size - 1
        return (x == min_coord or x == max_coord) and (y == min_coord or y == max_coord)

    # Get the list of four corner cells
    def get_corners(self):
        max_index = self.size - 1
        return [(0, 0), (0, max_index), (max_index, 0), (max_index, max_index)]

    # Get stable cells in the direction from corner
    def get_stable_cells_on_edges_in_direction_from_corner(self, player, x, y, dx, dy):
        # The cell has to be a corner
        if not self.is_on_corner(x, y):
            raise Exception("The cell is not on corner")

        # The list of stable cells found in direction (dx, dy) from corner cell (x, y)
        stable = []

        # Neighbour of current cell in selected direction
        nx = x + dx
        ny = y + dy

        # Move in direction until another corner or another player's cell is reached
        while self.is_on_board(nx, ny) and self.board[nx][ny] == player and not self.is_on_corner(nx, ny):
            # Save the stable cell
            stable.append((nx, ny))

            # Progress in the same direction
            nx += dx
            ny += dy

        return stable

    # Get stable cells on filled edge between corners
    def get_stable_cells_on_filled_edge(self, player, x, y, dx, dy):
        # The cell has to be a corner
        if not self.is_on_corner(x, y):
            raise Exception("The cell is not on corner")

        # Player cells on current edge
        player_cells = []

        # Index of current cell in selected direction
        nx = x
        ny = y

        # Move in direction until another corner or another player's cell is reached
        while self.is_on_board(nx, ny):
            # Save the stable cell if it belongs to the player
            if self.board[nx][ny] == player:
                player_cells.append((nx, ny))
            # If an empty cell has been found, there's no guarantees of stability
            elif self.board[nx][ny] == self.empty:
                return []

            # Progress in the same direction
            nx += dx
            ny += dy

        # If the whole edge is filled, return cells occupied by the player
        return player_cells

    # Get  a list of stable cells, i.e. the cells that can't be flipped in the future
    def get_stable_cells(self, player):
        # A list of stable cells
        stable_cells = []

        # Directions from corners to stable neighbour cells
        corner_directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

        # Corners are the first candidates
        for corner in self.get_corners():
            if self.board[corner[0]][corner[1]] == player:
                # The corner is already stable
                stable_cells.append(corner)

                # Move along the edges from current corner and find other stable cells
                for direction in corner_directions:
                    for stable in self.get_stable_cells_on_edges_in_direction_from_corner(
                            player,
                            corner[0],
                            corner[1],
                            direction[0],
                            direction[1]):
                        if stable not in stable_cells:
                            stable_cells.append(stable)

        # Move along the filled edges and add search for remaining stable cells
        for direction in corner_directions:
            for stable in self.get_stable_cells_on_filled_edge(
                    player,
                    corner[0],
                    corner[1],
                    direction[0],
                    direction[1]):
                if stable not in stable_cells:
                    stable_cells.append(stable)

        return stable_cells

    # Get all free cells
    def get_free_cells(self):
        free_cells = []
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == self.empty:
                    free_cells.append((x, y))
        return free_cells

    # Get a list of valid moves for current player
    def get_valid_moves(self, player):
        # Create a list of possible moves
        valid_moves = []

        # Loop through empty cells
        for cell in self.get_free_cells():
            # Check if the move is valid
            if self.move_is_valid(player, cell[0], cell[1]):
                valid_moves.append(cell)

        # Add pass if there are no free cells
        if len(valid_moves) == 0:
            valid_moves.append(self.pass_move)

        return valid_moves

    # Check if the possible move is valid
    def move_is_valid(self, player, x, y):
        # The cell has to be on board
        if not self.is_on_board(x, y):
            return False
        # The cell has to be empty
        elif not self.board[x][y] == self.empty:
            return False
        else:
            # Check all possible directions from current cell
            for dx, dy in self.directions:
                if self.move_captures_direction(player, x, y, dx, dy):
                    return True
            # No valid directions exist
            return False

    # Check if the move affects the direction
    def move_captures_direction(self, player, x, y, dx, dy):
        # Current player's opponent
        opponent = self.get_opponent(player)

        # Neighbour in current direction
        nx = x + dx
        ny = y + dy

        # The neighbour cell has to be on the board
        if not self.is_on_board(nx, ny):
            return False
        # The neighbour cell has to belong to the opponent
        elif not self.board[nx][ny] == opponent:
            return False

        # Skip the rest of cells belonging to the opponent
        while self.is_on_board(nx, ny) and self.board[nx][ny] == opponent:
            nx += dx
            ny += dy

        # If current cell belongs to the player, it is a valid move
        if self.is_on_board(nx, ny):
            if self.board[nx][ny] == player:
                return True

        # Otherwise the direction is not valid
        return False

    # Flip cells in specified direction
    def flip_cells_in_direction(self, player, x, y, dx, dy):
        # Flip all cells and return the list containing them if the direction is valid
        if self.move_captures_direction(player, x, y, dx, dy):
            # Current player's opponent
            opponent = self.get_opponent(player)

            # Neighbour in current direction, belongs to the opponent
            nx = x + dx
            ny = y + dy

            # List of cells that are possibly flipped by the move
            flipped_cells = []

            # Iterate through all cells in current direction belonging to the opponent
            while self.is_on_board(nx, ny) and self.board[nx][ny] == opponent:
                self.board[nx][ny] = player
                flipped_cells.append((nx, ny))
                nx += dx
                ny += dy

            # Return the list of flipped cells
            return flipped_cells
        # Otherwise return an empty list since no cells have been flipped
        else:
            return []

    # Get the list of possible moves for the player associated with their values
    def get_move_evaluations(self, player, search_depth, max_value):
        # The best result so far, initial value is the smallest possible
        max_so_far = int_min

        # Move-value pairs
        evaluations = []

        # The list of valid moves for current player
        valid_moves = self.get_valid_moves(player)

        for move in valid_moves:
            value = self.get_move_value(player, move[0], move[1], search_depth - 1, -max_so_far)

            # Alpha-Beta Pruning
            # The current result is over the maximum value.
            # This means that the opponent has at least one
            # move that will result in a better outcome by avoiding
            # this branch completely. Therefore, there is no
            # point in searching it further, so stop searching
            # and yield the evaluation.
            if value > max_value:
                evaluations.append((move, value))
                continue

            # Current move is worse than ones already found, skip it
            if value < max_so_far:
                continue

            max_so_far = max(value, max_so_far)
            evaluations.append((move, value))

        if len(valid_moves) == 0:
            evaluations.append((self.pass_move, self.get_move_value(player, self.pass_move[0], self.pass_move[1],
                                                                    search_depth - 1, -max_so_far)))

        return evaluations

    # Get heuristic value associated with the move
    def get_move_value(self, player, x, y, search_depth, max_value):
        # Make a move and save flipped cells
        cells_flipped_by_move = self.move(player, x, y)

        # Check whether the search is over
        if search_depth == 0 or self.is_over():
            result = self.get_board_heuristics(player)
            self.undo_move(player, x, y, cells_flipped_by_move)
            return result

        # Return the opposite of the opponent's best move value
        opponent = self.get_opponent(player)

        # Recursively call back to GetMoveEvaluations
        move_evaluations = self.get_move_evaluations(opponent, search_depth, max_value)

        max_found = int_min

        # Find the best available move and use it to evaluate the next depth level
        for move_value_pair in move_evaluations:
            if move_value_pair[1] > max_found:
                max_found = move_value_pair[1]

        # Undo the move
        self.undo_move(player, x, y, cells_flipped_by_move)

        return -max_found

    # Get the best possible move for the player according to game heuristics
    def get_best_move(self, player, search_depth):
        # Get all possible moves along with their values for the player
        moves = self.get_move_evaluations(player, search_depth, int_max)

        # If there are no possible moves, the player has to pass
        if len(moves) == 0:
            return (self.pass_move,
                    self.get_move_value(player, self.pass_move[0], self.pass_move[1], search_depth, int_max))
        # Only one move is possible, there's no need to search
        elif len(moves) == 1:
            return moves[0]
        # Return the move with highest value for the player
        else:
            # The list of moves that are best
            best_moves = []

            # Value of the best moves
            best_value = int_min

            # Find the best moves among remaining candidates
            for move in moves:
                # Current move candidate is better than the previous one
                if move[1] > best_value:
                    # Update best move and best move value
                    best_moves = [move[0]]
                    best_value = move[1]
                # Value of the current move is equal to the value of the best one yet
                elif move[1] == best_value:
                    # Add current move to the list of the best moves
                    best_moves.append(move[0])

            # Randomly return any of the best moves
            rand_best_move = randrange(len(best_moves))
            return best_moves[rand_best_move], best_value


"""
game = ReversiEngine(8)

cur_player = game.first

while not game.is_over():
    game.move_ai(cur_player, 4)
    cur_player = game.get_opponent(cur_player)
    print game

print "The score is " + str(game.get_score_difference(game.first))
if game.get_winner() == game.first:
    print "The first player won!"
elif game.get_winner() == game.second:
    print "The second player has won!"
else:
    print "Draw!"
"""