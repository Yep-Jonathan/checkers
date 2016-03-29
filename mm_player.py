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
        # TODO: update board based on suggested dst
        return src_x, src_y, dst_x, dst_y, self.evaluate(board)

    def choose_move(self):
        board_config = self.board.get_board_config(self.team)
        self.board_configs.append(board_config)
        # generate 8x8 board for evaluation
        board_config = expand_board_config(board_config)

        possible_moves = self.get_possible_moves()

        # game ends if a player is unable to move
        if not possible_moves:
            self.game.game_over()
            return

        # calculate scores of each possible board position
        scores = []
        for src, dst_list in possible_moves.iteritems():
            for dst in dst_list:
                scores.append(self.check_move(board_config, src[0], src[1], dst[0], dst[1]))

        # sort scores and use the last one
        best = sorted(scores, key=lambda x: x[4])[-1]
        # print("best move: {}".format(best))

        self.select_move(best[0], best[1], best[2], best[3])

    def select_move(self, source_row, source_column, dest_row, dest_column):
        self.game.select_move(source_row, source_column, dest_row, dest_column)

    def select_additional_jump(self, source_row, source_column):
        _, moves = self.board.get_possible_moves(source_row, source_column)

        board_config = self.board.get_board_config(self.team)
        self.board_configs.append(board_config)

        scores = []
        for move in moves:
            scores.append(self.check_move(board_config, source_row, source_column, move[0], move[1]))

        # sort scores and use the last one
        best = sorted(scores, key=lambda x: x[4])[-1]
        # print("best addl move: {}".format(best))

        self.select_move(best[0], best[1], best[2], best[3])
