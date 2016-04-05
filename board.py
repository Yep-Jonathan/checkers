# A Representation of a checkers board, drawn using Tkinter

import numpy as np
import Tkinter as tk
import sys

class Direction:
    Upward = 1
    Both = 0
    Downward = -1


class Piece:
    BlackKing = 2
    Black = 1
    NoPiece = 0
    Red = -1
    RedKing = -2


class TileSpecs:
    CellWidth = 50
    CellHeight = 50
    PieceSpacing = 10
    BoardColor = "#444444"


class Team:
    Black = "black"
    Red = "red"
    NoPiece = "no_piece"
    Invalid = "invalid"


class CheckersBoard(tk.Canvas):

    class InvalidTileError(Exception):
        pass

    class Tile():
        # defines a tile square that tells where pieces can move to
        def __init__(self, canvas, row, column):
            if (0 <= row <= 7 and 0 <= column <= 7 and (row + column) % 2 != 0):
                self.row = row
                self.column = column
            else:
                raise InvalidTileError("%s, %s not valid" % (row, column))

            self.canvas = canvas

            # initialization of the checkers board
            if (row in [0, 1, 2]):
                self.piece = Piece.Black
                self.draw_piece = self.create_piece(row, column, "black")
            elif (row in [5, 6, 7]):
                self.piece = Piece.Red
                self.draw_piece = self.create_piece(row, column, "red")
            else:
                self.piece = Piece.NoPiece
                self.draw_piece = None

        def get_piece_coordinates(self, row, column):
            # coordinates for drawing a piece
            x1 = column * TileSpecs.CellWidth
            y1 = row * TileSpecs.CellHeight
            x2 = x1 + TileSpecs.CellWidth
            y2 = y1 + TileSpecs.CellHeight
            return (x1+TileSpecs.PieceSpacing, y1+TileSpecs.PieceSpacing,
                    x2-TileSpecs.PieceSpacing, y2-TileSpecs.PieceSpacing)

        def get_king_piece_coordinates(self, row, column):
            # coordinates for drawing a king piece
            x1 = column * TileSpecs.CellWidth + 10
            y1 = row * TileSpecs.CellHeight + 15

            x2 = x1
            y2 = y1 + 20

            x3 = x2 + 30
            y3 = y2

            x4 = x3
            y4 = y3 - 20

            x5 = x4 - 10
            y5 = y4 + 5

            x6 = x5 - 5
            y6 = y5 - 10

            x7 = x6 - 5
            y7 = y6 + 10

            return (x1, y1, x2, y2, x3, y3,
                x4, y4, x5, y5, x6, y6, x7, y7)

        def create_piece(self, row, column, color="#444444"):
            return self.canvas.create_oval(*self.get_piece_coordinates(row, column),
                                           fill=color,
                                           outline=TileSpecs.BoardColor,
                                           tags="piece")


        def create_king_piece(self, row, column, color="#444444"):
            return self.canvas.create_polygon(*self.get_king_piece_coordinates(row, column),
                fill=color,
                outline=TileSpecs.BoardColor,
                tags="piece")


        def update_piece(self, new_piece_type):
            if (new_piece_type != self.piece):
                if self.draw_piece:
                    self.canvas.delete(self.draw_piece)  # remove the original piece

                if (new_piece_type == Piece.Black or new_piece_type == Piece.Red):
                    color = "black" if new_piece_type == Piece.Black else "red"
                    self.draw_piece = self.create_piece(self.row, self.column, color)
                elif (new_piece_type == Piece.BlackKing or new_piece_type == Piece.RedKing):
                    color = "black" if new_piece_type == Piece.BlackKing else "red"
                    self.draw_piece = self.create_king_piece(self.row, self.column, color)
                else:
                    self.draw_piece = None  # draw no piece

            self.piece = new_piece_type

        def get_upward_moves(self):
            return self.get_moves(Direction.Upward)

        def get_downward_moves(self):
            return self.get_moves(Direction.Downward)

        def get_king_moves(self):
            return self.get_moves(Direction.Both)

        def draw(self):
            pass


    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=400, height=400, borderwidth=0, highlightthickness=0)
        self.rows = 8
        self.columns = 8
        TileSpecs.BoardColor = '#444444'

        self.tiles = {}
        for column in range(8):
            for row in range(8):
                x1 = column * TileSpecs.CellWidth
                y1 = row * TileSpecs.CellHeight
                x2 = x1 + TileSpecs.CellWidth
                y2 = y1 + TileSpecs.CellHeight
                if ((column + row) % 2 == 0):
                    self.create_rectangle(x1, y1, x2, y2, fill="red", tags="emptySpaces")
                else:
                    self.create_rectangle(x1, y1, x2, y2,
                        fill=TileSpecs.BoardColor, tags="board")
                    self.tiles[row, column] = self.Tile(self, row, column)

    # inefficient, but okay for now
    def get_black_pieces(self):
        # returns a list of all of black's pieces
        black_pieces = []
        for row in range(8):
            for column in range(8):
                if self.check_tile(row, column) == Team.Black:
                    black_pieces.append((row, column))
        return black_pieces

    def get_red_pieces(self):
        # returns a list of all of red's pieces
        red_pieces = []
        for row in range(8):
            for column in range(8):
                if self.check_tile(row, column) == Team.Red:
                    red_pieces.append((row, column))
        return red_pieces

    def get_board_config(self, team):
        # return a 8 x 4 array of the pieces
        # the array will always have the team you specify heading downwards

        # first, construct the array as is, black is (+), red is (-)
        config = np.zeros((8,4), dtype=np.int)
        for row in range(8):
            for column in range(8):
                if ((row, column) in self.tiles):
                    piece = self.tiles[row, column].piece
                    config[row, column / 2] = piece  # enum defined as ints

        if (team == Team.Red):
            # rotate and invert the array
            config = np.rot90(config, 2)  # rotate by 180
            config *= -1

        return config

    def get_8_board_config(self, team):
    # return a 8 x 8 array of the pieces
    # the array will always have the team you specify heading downwards

    # first, construct the array as is, black is (+), red is (-)
        config = np.zeros((8,8), dtype=np.int)
        for row in range(8):
            for column in range(8):
                if ((row, column) in self.tiles):
                    piece = self.tiles[row, column].piece
                    config[row, column] = piece  # enum defined as ints

        if (team == Team.Red):
            # rotate and invert the array
            config = np.rot90(config, 2)  # rotate by 180
            config *= -1

        return config


    def check_tile(self, row, column):
        # returns the team of the tile (red, black, or no_piece)
        if ((row, column) not in self.tiles):
            return Team.Invalid

        tile = self.tiles[row, column]
        if (tile.piece > 0):
            return Team.Black
        elif (tile.piece < 0):
            return Team.Red
        else:
            return Team.NoPiece

    def opposing_teams(self, team1, team2):
        if ((team1 == Team.Red and team2 == Team.Black)
                or (team1 == Team.Black and team2 == Team.Red)):
            return True
        else:
            return False

    def get_possible_moves(self, row, column):
        # returns the possible moves for a piece on the tile (row, column)
        moves = []
        jump_moves = []

        tile = self.tiles[row, column]
        this_team = self.check_tile(row, column)
        direction = None
        if (tile.piece == 2 or tile.piece == -2):
            direction = Direction.Both
        elif (tile.piece == 1):
            direction = Direction.Downward
        elif (tile.piece == -1):
            direction = Direction.Upward

        # check each diagonal direction for moves / jumps
        # x - - - x
        # - x - x -
        # - - o - -
        # - x - x -
        # x - - - x

        if ((direction == Direction.Upward or direction == Direction.Both)):
            team_up_left = self.check_tile(row - 1, column - 1)
            if (team_up_left == Team.NoPiece):
                moves.append((row - 1, column - 1))
            elif (self.opposing_teams(this_team, team_up_left)):
                # check if a jump is possible
                team_up_left_jump = self.check_tile(row - 2, column - 2)
                if (team_up_left_jump == Team.NoPiece):
                    jump_moves.append((row - 2, column - 2))

            team_up_right = self.check_tile(row - 1, column + 1)
            if (team_up_right == Team.NoPiece):
                moves.append((row - 1, column + 1))
            elif (self.opposing_teams(this_team, team_up_right)):
                # check if a jump is possible
                team_up_right_jump = self.check_tile(row - 2, column + 2)
                if (team_up_right_jump == Team.NoPiece):
                    jump_moves.append((row - 2, column + 2))

        if ((direction == Direction.Downward or direction == Direction.Both)):
            team_down_left = self.check_tile(row + 1, column - 1)
            if (team_down_left == Team.NoPiece):
                moves.append((row + 1, column - 1))
            elif (self.opposing_teams(this_team, team_down_left)):
                # check if a jump is possible
                team_down_left_jump = self.check_tile(row + 2, column - 2)
                if (team_down_left_jump == Team.NoPiece):
                    jump_moves.append((row + 2, column - 2))

            team_down_right = self.check_tile(row + 1, column + 1)
            if (team_down_right == Team.NoPiece):
                moves.append((row + 1, column + 1))
            elif (self.opposing_teams(this_team, team_down_right)):
                # check if a jump is possible
                team_down_right_jump = self.check_tile(row + 2, column + 2)
                if (team_down_right_jump == Team.NoPiece):
                    jump_moves.append((row + 2, column + 2))

        # capturing moves must be taken before regular moves
        if jump_moves:
            return (True, jump_moves)
        else:
            return (False, moves)

    def move_piece(self, source_row, source_column, dest_row, dest_column):
        dest_tile = self.tiles[dest_row, dest_column]
        if self.tiles[dest_row, dest_column].piece != Piece.NoPiece:
            return False # cannot move to an already occupied space

        source_tile = self.tiles[source_row, source_column]

        # KING ME
        if (source_tile.piece == Piece.Red and dest_row == 0):
            dest_tile.update_piece(Piece.RedKing)
        elif (source_tile.piece == Piece.Black and dest_row == 7):
            dest_tile.update_piece(Piece.BlackKing)
        else:
            dest_tile.update_piece(source_tile.piece)

        source_tile.update_piece(Piece.NoPiece)

        return True

    def remove_piece(self, row, column):
        # remove a piece because it GOT JUMPED
        self.tiles[row, column].update_piece(Piece.NoPiece)
