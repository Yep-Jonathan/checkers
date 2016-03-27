# implementation of a human checkers player

import Tkinter as tk
from random import randint
from player import CheckersPlayer
from functools import partial
from board import TileSpecs
import time

class AIPlayer(CheckersPlayer):

    def __init__(self, game, board, team):
        super(AIPlayer, self).__init__(game, board, team)
        self.board_configs = []

    def choose_move(self):
        self.board_configs.append(self.board.get_board_config(self.team))

        possible_moves = self.get_possible_moves()

        # game ends if a player is unable to move
        if not possible_moves:
            self.game.game_over()
            return

        #randomly choose a move
        move_row = randint(0, len(possible_moves)-1)
        move_list = possible_moves.items()[move_row][1]
        move_column = randint(0, len(move_list)-1)

        ai_move_src = possible_moves.items()[move_row][0]
        ai_move_dest = move_list[move_column]

        self.select_move(ai_move_src[0], ai_move_src[1], ai_move_dest[0], ai_move_dest[1])

    def select_move(self, source_row, source_column, dest_row, dest_column):
        self.game.select_move(source_row, source_column, dest_row, dest_column)

    def select_additional_jump(self, source_row, source_column):
        _, moves = self.board.get_possible_moves(source_row, source_column)

        random_move_number = randint(0,len(moves)-1)
        random_move = moves[random_move_number]

        self.select_move(source_row, source_column, random_move[0], random_move[1])
