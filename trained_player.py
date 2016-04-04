# implementation of a human checkers player

import Tkinter as tk
from random import randint
import sqlite3 as lite
from player import CheckersPlayer
from functools import partial
from board import TileSpecs
from board import Team
import time
import copy
import numpy as np

def get_moves_per_piece(board_config, row, column):

    if board_config[row][column] <= 0:
        return [],[]


    destinations = []
    jump_destinations = []
    # piece can move down
    if board_config[row][column] > 0:
        # move down and left
        if (column - 1) >= 0 and row < 7 and board_config[row+1][column-1] == 0:
            destinations.append((row+1,column-1 ))
        # move down and right
        if (column + 1) <= 7 and row < 7 and board_config[row+1][column+1] == 0:
            destinations.append((row+1, column+1))

    #piece can jump down
    if board_config[row][column] > 0:
        if (column) - 2 >= 0 and row < 6 and board_config[row+1][(column)-1] < 0 and board_config[row+2][(column)-2] == 0:
            jump_destinations.append((row+2,(column)-2 ))
        if (column) + 2 <= 7 and row < 6 and board_config[row+1][(column)+1] < 0 and board_config[row+2][(column)+2] == 0:
            jump_destinations.append((row+2,(column)+2 ))

    # king can move up
    if board_config[row][column] == 2:
        if (column) - 1 >= 0 and row > 0 and board_config[row-1][(column)-1] == 0:
            destinations.append((row-1,(column)-1 ))
        if (column) + 1 <= 7 and row > 0 and board_config[row-1][(column)+1] == 0:
            destinations.append((row-1,(column)+1 ))

    # king can jump up
    if board_config[row][column] == 2:
        if (column) - 2 >= 0 and row > 1 and board_config[row-1][(column)-1] < 0 and board_config[row-2][(column)-2] == 0:
            jump_destinations.append((row-2,(column)-2 ))
        if (column) + 2 <= 7 and row > 1 and board_config[row-1][(column)+1] < 0 and board_config[row-2][(column)+2] == 0:
            jump_destinations.append((row-2,(column)+2 ))

    if len(jump_destinations) > 0:
        destinations = []

    return jump_destinations, destinations

def get_moves(board_config):
    jump_moves = []
    moves = []
    for i in range(8):
        for j in range(8):
            mv_src = (i,j)
            mv_dst_jmp, mv_dst = get_moves_per_piece(board_config, i, j)
            if len(mv_dst) > 0:
                moves.append([mv_src, mv_dst])
            if len(mv_dst_jmp) > 0:
                jump_moves.append([mv_src, mv_dst_jmp])
    if len(jump_moves) > 0:
        moves = jump_moves
    return moves

def lookahead_config(original_config, team, lookahead=1):
    possible_moves = get_moves(original_config)
    # No more lookahead
    if not possible_moves:
        return None

    # Choose move from the database
    next_configs = []
    for move_row in range(0, len(possible_moves)):
        move_list = possible_moves[move_row][1]
        ai_move_src = possible_moves[move_row][0]
        for move_column in range (0,len(move_list)):
            ai_move_dest = move_list[move_column]

            copy_config = copy.deepcopy(original_config)
            next_config = [ai_move_src, ai_move_dest, return_new_config(copy_config, ai_move_src, ai_move_dest)]
            next_configs.append(next_config)

    if lookahead is 1:
        return next_configs
    next_team = Team.Red
    if team == Team.Red:
        next_team = Team.Black
    lookahead_configs = []
    for config in next_configs:
        invert = 1
        if lookahead % 2 == 0:
            invert = -1
        new_config = invert*lookahead_config(invert_config(config[2]), next_team, lookahead-1)
        lookahead_configs.append(new_config)
    return lookahead_configs

def invert_config(config):
    config1 = np.rot90(config, 2)  # rotate by 180
    config1 *= -1
    return config1

def return_new_config(original_config, mv_src, mv_dst):

    new_src = mv_src
    new_dst = mv_dst
    new_config = original_config

    new_config[new_dst[0]][new_dst[1]] = original_config[new_src[0]][new_src[1]]
    new_config[new_src[0]][new_src[1]] = 0

    # if there is a jump, remove the enemy's piece
    if abs(new_src[0] - new_dst[0]) > 1:
        jumped_point_x = (new_src[0] + new_dst[0]) / 2;
        jumped_point_y = (new_src[1] + new_dst[1]) / 2;
        new_config[jumped_point_x][jumped_point_y] = 0;
    return new_config


class TrainedPlayer(CheckersPlayer):

    def __init__(self, game, board, team):
        super(TrainedPlayer, self).__init__(game, board, team)
        self.board_configs = []
        self.ai = True

    def choose_move(self):
        possible_moves = self.get_possible_moves()
        self.board_configs.append(self.board.get_board_config(self.team))
        print "BOARD"
        print self.board.get_8_board_config(self.team)


        print lookahead_config(self.board.get_8_board_config(self.team), self.team, 2)
        print "DONE"
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
                next_config = [ai_move_src, ai_move_dest, return_new_config(self.board.get_board_config(self.team), ai_move_src, ai_move_dest)]
                next_configs.append(next_config)
        #
        # print "Possible configs"
        # for config in next_configs:
        #     print config[2]


        max_possibility = 0.0
        config_index = -1
        skippable_indeces = []
        conn = lite.connect("temp.db")
        c = conn.cursor()
        tableName = "trainingdata"
        for idx, config in enumerate(next_configs):
            query = "SELECT wins, total FROM " + tableName + " WHERE config = '" + str(config[2]) + "'"
            c.execute(query)
            data = c.fetchone()
            if data is not None:
                if data[0] is 0:
                    skippable_indeces.append(idx)
                else:
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
        else:
            #randomly choose a move
            print "MAKING RANDOM MOVE"
            move_row = randint(0, len(possible_moves)-1)
            move_list = possible_moves.items()[move_row][1]
            move_column = randint(0, len(move_list)-1)

            ai_move_src = possible_moves.items()[move_row][0]
            ai_move_dest = move_list[move_column]

        self.select_move(ai_move_src[0], ai_move_src[1], ai_move_dest[0], ai_move_dest[1])
        #self.board_configs.append(return_new_config(self.board.get_board_config(self.team) ,ai_move_src, ai_move_dest, self.team))

    def select_move(self, source_row, source_column, dest_row, dest_column):
        self.game.select_move(source_row, source_column, dest_row, dest_column)

    def select_additional_jump(self, source_row, source_column):
        _, moves = self.board.get_possible_moves(source_row, source_column)
        self.board_configs.append(self.board.get_board_config(self.team))

        random_move_number = randint(0,len(moves)-1)
        random_move = moves[random_move_number]

        self.select_move(source_row, source_column, random_move[0], random_move[1])
