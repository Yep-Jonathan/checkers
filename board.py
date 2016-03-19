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


class CheckersBoard(tk.Tk):

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
                self.draw_piece = self.create_piece(row, column)

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
                self.canvas.delete(self.draw_piece)  # remove the original piece

                if (new_piece_type == Piece.black or new_piece_type == Piece.red):
                    color = "black" if new_piece_type == Piece.black else "red"
                    self.draw_piece = self.create_piece(self.row, self.column, color)
                elif (new_piece_type == Piece.black_king or new_piece_type == Piece.red_king):
                    color = "black" if new_piece_type == Piece.black else "red"
                    self.draw_piece = self.create_king_piece(self.row, self.column, color)
                else:
                    self.draw_piece = self.create_piece(self.row, self.column)  # draw no piece

            self.piece = new_piece_type


        def get_moves(self, direction):
            moves = []
            row = self.row
            column = self.column
            if ((direction == Direction.upward or direction == Direction.both) and self.row != 0):
                if (row % 2 == 0):
                    moves.append((row - 1, column))
                    if (column != 3):
                        moves.append((row - 1, column + 1))
                else:
                    moves.append((row - 1, column))
                    if (self.column != 0):
                        moves.append((row - 1, column - 1))
            if ((direction == Direction.downward or direction == Direction.both) and self.row != 7):
                if (row % 2 == 0):
                    moves.append((row + 1, column))
                    if (column != 3):
                        moves.append((row + 1, column + 1))
                else:
                    moves.append((row + 1, column))
                    if (column != 0):
                        moves.append((row + 1, column - 1))
            
            return moves

        def get_upward_moves(self):
            return self.get_moves(Direction.upward)

        def get_downward_moves(self):
            return self.get_moves(Direction.downward)

        def get_king_moves(self):
            return self.get_moves(Direction.both)

        def draw(self):
            pass



    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=400, height=400, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = 8
        self.columns = 8
        self.cellwidth = 50
        self.cellheight = 50
        self.board_color = '#444444'
        
        self.tiles = {}
        for column in range(8):
            for row in range(8):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                if ((column + row) % 2 == 0):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", tags="emptySpaces")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                        fill=self.board_color, tags="board")
                    self.tiles[row, column] = self.Tile(self.canvas, row, column)

        self.move_piece(2, 1, 3, 2)
        #self.tiles[0, 1].update_piece(Piece.red)
        
        #self.redraw(5000)

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

    def draw(self):
        # go through the each tile and draw what is necessary
        for tile in self.tiles:
            pass


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
    app = CheckersBoard()
    app.bind('<Escape>', close)
    app.mainloop()