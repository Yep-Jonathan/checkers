# file for a generic player.  Should be subclassed into Human / AI player

# abstract class
class CheckersPlayer(object):

    def __init__(self, game, board, pieces):
        # pieces should be a list of (row, column) pairs that list all the pieces
        # controlled by this player.
        self.game = game
        self.board = board
        self.pieces = pieces

    def choose_move(self):
        raise NotImplementedError()

    def piece_captured(self, piece):
        if (piece in self.pieces):
            self.pieces.remove(piece)
