# implementation of a human checkers player

import Tkinter as tk
from random import randint
import sqlite3 as lite
from player import CheckersPlayer
from functools import partial
from board import TileSpecs
from board import Team
import time

def return_new_config(original_config, mv_src, mv_dst, team, recursion=False):

    if (team == Team.Red):
        new_src = (7-mv_src[0], 7-mv_src[1])
        new_dst = (7-mv_dst[0], 7-mv_dst[1])
    if (team == Team.Black):
        new_src = mv_src
        new_dst = mv_dst
    new_config = original_config

    new_config[new_dst[0]][new_dst[1]/2] = original_config[new_src[0]][new_src[1]/2]
    new_config[new_src[0]][new_src[1]/2] = 0

    # if there is a jump, remove the enemy's piece
    if abs(new_src[0] - new_dst[0]) > 1:
        jumped_point_x = (new_src[0] + new_dst[0]) / 2;
        jumped_point_y = (new_src[1] + new_dst[1]) / 2;
        new_config[jumped_point_x][jumped_point_y/2] = 0;

    return new_config


class TrainedPlayer(CheckersPlayer):

    def __init__(self, game, board, team):
        super(TrainedPlayer, self).__init__(game, board, team)
        self.board_configs = []
        self.ai = True

    def choose_move(self):
        possible_moves = self.get_possible_moves()
        self.board_configs.append(self.board.get_board_config(self.team))

        # game ends if a player is unable to move
        if not possible_moves:
            self.game.game_over()
            return

        # Choose move from the database
        next_configs = []
        for move_row in range(0, len(possible_moves)):
            move_list = possible_moves.items()[move_row][1]
            ai_move_src = possible_moves.items()[move_row][0]
            for move_column in range (0,len(move_list)):
                ai_move_dest = move_list[move_column]
                next_config = [ai_move_src, ai_move_dest, return_new_config(self.board.get_board_config(self.team), ai_move_src, ai_move_dest, self.team, True)]
                next_configs.append(next_config)
        #
        # print "Possible configs"
        # for config in next_configs:
        #     print config[2]


        max_possibility = 0.0
        config_index = -1
        for idx, config in enumerate(next_configs):
            conn = lite.connect("temp.db")
            c = conn.cursor()
            tableName = "trainingdata"
            query = "SELECT wins, total FROM " + tableName + " WHERE config = '" + str(config[2]) + "'"
            c.execute(query)
            data = c.fetchone()
            if data is not None:
                new_possibility = float(data[0]) / float(data[1])
                if new_possibility > max_possibility:
                    max_possibility = new_possibility
                    config_index = idx

        conn.close()

        ai_move_src
        ai_move_dest
        if config_index >=0:
            print "MAKING DB MOVE"
            ai_move_src = next_configs[config_index][0]
            ai_move_dest = next_configs[config_index][1]
            self.select_move(ai_move_src[0], ai_move_src[1], ai_move_dest[0], ai_move_dest[1])
        else:
            #randomly choose a move
            print "MAKING RANDOM MOVE"

            move_row = randint(0, len(possible_moves)-1)
            move_list = possible_moves.items()[move_row][1]
            move_column = randint(0, len(move_list)-1)

            ai_move_src = possible_moves.items()[move_row][0]
            ai_move_dest = move_list[move_column]

            self.select_move(ai_move_src[0], ai_move_src[1], ai_move_dest[0], ai_move_dest[1])
        self.board_configs.append(return_new_config(self.board.get_board_config(self.team) ,ai_move_src, ai_move_dest, self.team))

    def select_move(self, source_row, source_column, dest_row, dest_column):
        self.game.select_move(source_row, source_column, dest_row, dest_column)

    def select_additional_jump(self, source_row, source_column):
        _, moves = self.board.get_possible_moves(source_row, source_column)
        self.board_configs.append(self.board.get_board_config(self.team))

        random_move_number = randint(0,len(moves)-1)
        random_move = moves[random_move_number]

        self.select_move(source_row, source_column, random_move[0], random_move[1])
