# A Representation of a checkers board, drawn using Tkinter

import Tkinter as tk
import sys
# import random

class Direction:
    upward = 1
    both = 0
    downward = -1


class Piece:
    black_king = 2
    black = 1
    no_piece = 0
    red = -1
    red_king = -2


class Team:
    black = "black"
    red = "red"
    no_piece = "no_piece"
    invalid = "invalid"


class CheckersBoard(tk.Canvas):

    class InvalidTileError(Exception):
        pass

    class Tile():
        cellwidth = 50
        cellheight = 50
        piece_spacing = 10

        board_color = "#444444"

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
                self.piece = Piece.black
                self.draw_piece = self.create_piece(row, column, "black")
            elif (row in [5, 6, 7]):
                self.piece = Piece.red
                self.draw_piece = self.create_piece(row, column, "red")
            else:
                self.piece = Piece.no_piece
                self.draw_piece = None

        def get_piece_coordinates(self, row, column):
            x1 = column*self.cellwidth
            y1 = row * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            return (x1+self.piece_spacing, y1+self.piece_spacing,
                    x2-self.piece_spacing, y2-self.piece_spacing)


        def create_piece(self, row, column, color="#444444"):
            return self.canvas.create_oval(*self.get_piece_coordinates(row, column),
                                           fill=color,
                                           outline=self.board_color,
                                           tags="piece")


        def create_king_piece(self, row, column, color="#444444"):
            # draw a king piece (polygon?)
            pass


        def update_piece(self, new_piece_type):
            if (new_piece_type != self.piece):
                if self.draw_piece:
                    self.canvas.delete(self.draw_piece)  # remove the original piece

                if (new_piece_type == Piece.black or new_piece_type == Piece.red):
                    color = "black" if new_piece_type == Piece.black else "red"
                    self.draw_piece = self.create_piece(self.row, self.column, color)
                elif (new_piece_type == Piece.black_king or new_piece_type == Piece.red_king):
                    color = "black" if new_piece_type == Piece.black else "red"
                    self.draw_piece = self.create_king_piece(self.row, self.column, color)
                else:
                    self.draw_piece = None  # draw no piece

            self.piece = new_piece_type

        def get_upward_moves(self):
            return self.get_moves(Direction.upward)

        def get_downward_moves(self):
            return self.get_moves(Direction.downward)

        def get_king_moves(self):
            return self.get_moves(Direction.both)

        def draw(self):
            pass



    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=400, height=400, borderwidth=0, highlightthickness=0)
        self.rows = 8
        self.columns = 8
        self.board_color = '#444444'
        
        self.tiles = {}
        for column in range(8):
            for row in range(8):
                x1 = column * self.Tile.cellwidth
                y1 = row * self.Tile.cellheight
                x2 = x1 + self.Tile.cellwidth
                y2 = y1 + self.Tile.cellheight
                if ((column + row) % 2 == 0):
                    self.create_rectangle(x1, y1, x2, y2, fill="red", tags="emptySpaces")
                else:
                    self.create_rectangle(x1, y1, x2, y2,
                        fill=self.board_color, tags="board")
                    self.tiles[row, column] = self.Tile(self, row, column)

        # self.move_piece(5, 0, 4, 1)
        # self.move_piece(4, 1, 3, 0)
        # possible_moves = {}
        # must_jump = False

        # for column in range(8):
        #     for row in range(8):
        #         if (self.check_tile(row, column) == Team.black):
        #             is_jump, moves = self.get_moves(row, column)
        #             if not moves:
        #                 continue

        #             if (must_jump and is_jump):
        #                 possible_moves[row, column] = moves
        #             elif (not must_jump and is_jump):
        #                 print "clear"
        #                 possible_moves.clear()
        #                 possible_moves[row, column] = moves
        #                 must_jump = is_jump
        #             elif (not must_jump and not is_jump):
        #                 possible_moves[row, column] = moves

        # print possible_moves

    def check_tile(self, row, column):
        # returns the team of the tile (red, black, or no_piece)
        if ((row, column) not in self.tiles):
            return Team.invalid
        
        tile = self.tiles[row, column]
        if (tile.piece > 0):
            return Team.black
        elif (tile.piece < 0):
            return Team.red
        else:
            return Team.no_piece

    def opposing_teams(self, team1, team2):
        if ((team1 == Team.red and team2 == Team.black)
                or (team1 == Team.black and team2 == Team.red)):
            return True
        else:
            return False

    def get_moves(self, row, column):
        # returns the possible moves for a piece on the tile (row, column) 
        moves = []
        jump_moves = []

        tile = self.tiles[row, column]
        this_team = self.check_tile(row, column)
        direction = None
        if (tile.piece == 2 or tile.piece == -2):
            direction = Direction.both
        elif (tile.piece == 1):
            direction = Direction.downward
        elif (tile.piece == -1):
            direction = Direction.upward

        # check each diagonal direction for moves / jumps
        # x - - - x
        # - x - x -
        # - - o - -
        # - x - x -
        # x - - - x

        if ((direction == Direction.upward or direction == Direction.both)):
            team_up_left = self.check_tile(row - 1, column - 1)
            if (team_up_left == Team.no_piece):
                moves.append((row - 1, column - 1))
            elif (self.opposing_teams(this_team, team_up_left)):
                # check if a jump is possible
                team_up_left_jump = self.check_tile(row - 2, column - 2)
                if (team_up_left_jump == Team.no_piece):
                    jump_moves.append((row - 2, column - 2))

            team_up_right = self.check_tile(row - 1, column + 1)
            if (team_up_right == Team.no_piece):
                moves.append((row - 1, column + 1))
            elif (self.opposing_teams(this_team, team_up_right)):
                # check if a jump is possible
                team_up_right_jump = self.check_tile(row - 2, column + 2)
                if (team_up_right_jump == Team.no_piece):
                    jump_moves.append((row - 2, column + 2))

        if ((direction == Direction.downward or direction == Direction.both)):
            team_down_left = self.check_tile(row + 1, column - 1)
            if (team_down_left == Team.no_piece):
                moves.append((row + 1, column - 1))
            elif (self.opposing_teams(this_team, team_down_left)):
                # check if a jump is possible
                team_down_left_jump = self.check_tile(row + 2, column - 2)
                if (team_down_left_jump == Team.no_piece):
                    jump_moves.append((row + 2, column - 2))

            team_down_right = self.check_tile(row + 1, column + 1)
            if (team_down_right == Team.no_piece):
                moves.append((row + 1, column + 1))
            elif (self.opposing_teams(this_team, team_down_right)):
                # check if a jump is possible
                team_down_right_jump = self.check_tile(row + 2, column + 2)
                if (team_down_right_jump == Team.no_piece):
                    jump_moves.append((row + 2, column + 2))

        # capturing moves must be taken before regular moves
        if jump_moves:
            return (True, jump_moves)
        else:
            return (False, moves)


    def move_piece(self, source_row, source_column, dest_row, dest_column):
        dest_tile = self.tiles[dest_row, dest_column]
        if self.tiles[dest_row, dest_column].piece != Piece.no_piece:
            return False # cannot move to an already occupied space

        source_tile = self.tiles[source_row, source_column]

        dest_tile.update_piece(source_tile.piece)
        source_tile.update_piece(Piece.no_piece)

        # update the dictionary
        #self[dest_row, dest_column] = piece
        #del self.pieces[init_row, init_column]
        return True

    # def redraw(self, delay):
    #     self.canvas.itemconfig("rect", fill="#444444")
    #     self.canvas.itemconfig("pieces", fill="#444444")
    #     for i in range(10):
    #         row = random.randint(0,7)
    #         col = random.randint(0,7)
    #         if ((col+row) % 2 == 1):
    #             item_id = self.oval[row,col]
    #             self.canvas.itemconfig(item_id, fill="red")
    #     self.after(delay, lambda: self.redraw(delay))

def close(event):
    sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = CheckersBoard(root)
    app.pack()
    root.bind('<Escape>', close)
    app.mainloop()