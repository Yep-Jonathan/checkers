# implementation of a human checkers player

import Tkinter as tk
from player import CheckersPlayer
from functools import partial
from board import TileSpecs

class HumanPlayer(CheckersPlayer):

    def __init__(self, game, board, team):
        super(HumanPlayer, self).__init__(game, board, team)

        # use buttons to move pieces.  Ugly, but w/e
        self.buttons = []
        self.board_configs = []

    def clear_buttons(self):
        for button in self.buttons:
            button.destroy()
        del self.buttons[:]  # clear the list

    def get_button_coordinates(self, row, column):
        x1 = column * TileSpecs.CellWidth + 18
        y1 = row * TileSpecs.CellHeight + 12
        return (x1, y1)

    def create_button(self, row, column, func_callback):
        self.buttons.append(
            tk.Button(self.game.root,
                text="  ",
                background=self.team,
                command=func_callback))

        self.board.create_window(*self.get_button_coordinates(row, column),
            anchor=tk.NW,
            window=self.buttons[-1])

    def choose_move(self):
        # create a button for each checkers piece that you can move
        # have the user choose one
        self.clear_buttons()

        possible_moves = self.get_possible_moves()

        # game ends if a player is unable to move
        if not possible_moves:
            self.game.game_over()
            return

        for (row, column), dest_list in possible_moves.iteritems():
            self.create_button(row, column, partial(self.select_starting_piece, row, column))

    def select_starting_piece(self, source_row, source_column):
        self.clear_buttons()

        _, moves = self.board.get_possible_moves(source_row, source_column)

        for (dest_row, dest_column) in moves:
            self.create_button(dest_row, dest_column,
                partial(self.select_move, source_row, source_column, dest_row, dest_column))

        # reset button
        self.create_button(source_row, source_column,self.choose_move)

    def select_additional_jump(self, source_row, source_column):
        self.clear_buttons()

        _, moves = self.board.get_possible_moves(source_row, source_column)

        for (dest_row, dest_column) in moves:
            self.create_button(dest_row, dest_column,
                partial(self.select_move, source_row, source_column, dest_row, dest_column))

    def select_move(self, source_row, source_column, dest_row, dest_column):
        self.clear_buttons()
        self.game.select_move(source_row, source_column, dest_row, dest_column)
