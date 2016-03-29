# file for a generic player.  Should be subclassed into Human / AI player
from board import Team as Team


# abstract class
class CheckersPlayer(object):

    def __init__(self, game, board, team):
        # pieces should be a list of (row, column) pairs that list all the pieces
        # controlled by this player.
        self.game = game
        self.board = board
        self.team = team
        self.board_configs = []

        if self.team == Team.Black:
            self.get_pieces = self.board.get_black_pieces
        else:
            self.get_pieces = self.board.get_red_pieces

    def choose_move(self):
        raise NotImplementedError()

    def select_additional_jump(self, source_row, source_column):
        raise NotImplementedError()

    def piece_captured(self, piece):
        if (piece in self.pieces):
            self.pieces.remove(piece)

    def get_possible_moves(self):
        possible_moves = {}
        must_jump = False

        for row, column in self.get_pieces():

            is_jump, moves = self.board.get_possible_moves(row, column)
            if not moves:
                continue

            if (must_jump and is_jump):
                possible_moves[row, column] = moves
            elif (not must_jump and is_jump):
                possible_moves.clear()
                possible_moves[row, column] = moves
                must_jump = is_jump
            elif (not must_jump and not is_jump):
                possible_moves[row, column] = moves

        # game ends if a player is unable to move
        if not possible_moves:
            self.game.game_over()

        return possible_moves
