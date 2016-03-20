# implementation of a human checkers player

import Tkinter as tk
from player import CheckersPlayer
from functools import partial
from board import Team as Team


class HumanPlayer(CheckersPlayer):

    def __init__(self, game, board, team):
        super(HumanPlayer, self).__init__(game, board, team)

        self.button_color = "#444444"
        if self.team == Team.Black:
            self.button_color = "black"
            self.get_pieces = self.board.get_black_pieces
            print self.get_pieces()
        else:
            self.button_color = "red"
            self.get_pieces = self.board.get_red_pieces

        # use buttons to move pieces.  Ugly, but w/e
        self.buttons = []

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

        return possible_moves

    def clear_buttons(self):
        for button in self.buttons:
            button.destroy()
        del self.buttons[:]  # clear the list

    def choose_move(self):
        # create a button for each checkers piece that you can move
        # have the user choose one
        self.clear_buttons()

        possible_moves = self.get_possible_moves()

        # game ends if a player is unable to move
        if not possible_moves:
            self.game.game_over()

        for (row, column), dest_list in possible_moves.iteritems():
            self.buttons.append(
                tk.Button(self.game.root,
                    text="  ",
                    background=self.button_color,
                    command=partial(self.select_starting_piece, row, column)))

            # TODO: remove hard coded #s
            self.board.create_window(column * 50 + 18, row * 50 + 12, anchor=tk.NW, window=self.buttons[-1])

    def select_starting_piece(self, source_row, source_column):
        self.clear_buttons()

        _, moves = self.board.get_possible_moves(source_row, source_column)

        for (dest_row, dest_column) in moves:
            self.buttons.append(
                tk.Button(self.game.root,
                    text="  ",
                    background=self.button_color,
                    command=partial(self.select_move, source_row, source_column, dest_row, dest_column)))

            # TODO: remove hard coded #s
            self.board.create_window(dest_column * 50 + 18,
                dest_row * 50 + 12,
                anchor=tk.NW,
                window=self.buttons[-1])

        # reset button
        self.buttons.append(
            tk.Button(self.game.root,
                text="  ",
                background=self.button_color,
                command=partial(self.choose_move)))

        # TODO: remove hard coded #s
        self.board.create_window(source_column * 50 + 18,
            source_row * 50 + 12,
            anchor=tk.NW,
            window=self.buttons[-1])

    def select_additional_jump(self, source_row, source_column):
        self.clear_buttons()

        _, moves = self.board.get_possible_moves(source_row, source_column)

        for (dest_row, dest_column) in moves:
            self.buttons.append(
                tk.Button(self.game.root,
                    text="  ",
                    background=self.button_color,
                    command=partial(self.select_move, source_row, source_column, dest_row, dest_column)))

            # TODO: remove hard coded #s
            self.board.create_window(dest_column * 50 + 18,
                dest_row * 50 + 12,
                anchor=tk.NW,
                window=self.buttons[-1])

    def select_move(self, source_row, source_column, dest_row, dest_column):
        self.clear_buttons()
        self.game.select_move(source_row, source_column, dest_row, dest_column)
