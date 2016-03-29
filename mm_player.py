"""Implementation of an AI checkers player that uses the Minimax algorithm.
"""

import numpy as np
from player import CheckersPlayer


def expand_board_config(board):
    exp = np.zeros((8, 8), dtype=int)
    for i, row in enumerate(board):
        for j, elem in enumerate(row):
            if i % 2 == 0:
                exp[i][2 * j + 1] = elem
            else:
                exp[i][2 * j] = elem
    return exp


class MMPlayer(CheckersPlayer):

    def __init__(self, game, board, team):
        super(MMPlayer, self).__init__(game, board, team)
        self.board_configs = []
        self.ai = True

    def evaluate(self, board):
        return sum([sum(x) for x in board])

    def check_move(self, board, src_x, src_y, dst_x, dst_y):
        return src_x, src_y, dst_x, dst_y, self.evaluate(board)

    def choose_move(self):
        board_config = self.board.get_board_config(self.team)
        self.board_configs.append(board_config)
        board_config = expand_board_config(board_config)

        possible_moves = self.get_possible_moves()

        # game ends if a player is unable to move
        if not possible_moves:
            self.game.game_over()
            return

        scores = []
        for src, dst_list in possible_moves.iteritems():
            for dst in dst_list:
                scores.append(self.check_move(board_config, src[0], src[1], dst[0], dst[1]))

        # randomly choose a move
        move_row = np.random.randint(len(possible_moves))
        move_list = possible_moves.items()[move_row][1]
        move_column = np.random.randint(len(move_list))

        ai_move_src = possible_moves.items()[move_row][0]
        ai_move_dest = move_list[move_column]

        self.select_move(ai_move_src[0], ai_move_src[1], ai_move_dest[0], ai_move_dest[1])

    def select_move(self, source_row, source_column, dest_row, dest_column):
        self.game.select_move(source_row, source_column, dest_row, dest_column)

    def select_additional_jump(self, source_row, source_column):
        _, moves = self.board.get_possible_moves(source_row, source_column)

        self.board_configs.append(self.board.get_board_config(self.team))

        random_move_number = np.random.randint(len(moves))
        random_move = moves[random_move_number]

        self.select_move(source_row, source_column, random_move[0], random_move[1])
