"""Implementation of an AI checkers player that uses the Minimax algorithm.
"""

import numpy as np

from board import Team
from player import CheckersPlayer
from trained_player import lookahead_config, invert_config

SCALING = np.array([
    [4, 4, 4, 4],
    [4, 3, 3, 3],
    [3, 2, 2, 4],
    [4, 2, 1, 3],
    [3, 1, 2, 4],
    [4, 2, 2, 3],
    [3, 3, 3, 4],
    [4, 4, 4, 4]
])


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

    def opponent(self):
        if self.team == Team.Black:
            return Team.Red
        elif self.team == Team.Red:
            return Team.Black

    def evaluate(self, board):
        scaled = np.multiply(expand_board_config(SCALING), board)
        piece_diff = sum([sum(x) for x in scaled])
        return -piece_diff

    def check_move(self, board, src_x, src_y, dst_x, dst_y):
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

        lookahead1 = lookahead_config(self.board.get_8_board_config(self.team), self.team)
        scores = []

        # calculate scores of each possible board position
        if lookahead1:
            for src1, dst1, new_board1 in lookahead1:
                min_score = self.evaluate(new_board1)
                lookahead2 = lookahead_config(invert_config(new_board1), self.opponent())
                if lookahead2:
                    scores2 = []
                    for src2, dst2, new_board2 in lookahead2:
                        scores2.append(self.check_move(new_board2, src2[0], src2[1], dst2[0], dst2[1]))
                    min_score = min(map(lambda x: x[4], scores2))
                scores.append((src1[0], src1[1], dst1[0], dst1[1], min_score))
        else:
            for src, dst_list in possible_moves.iteritems():
                for dst in dst_list:
                    scores.append(self.check_move(board_config, src[0], src[1], dst[0], dst[1]))

        # sort scores and use the last one
        best = sorted(scores, key=lambda x: x[4])[-1]
        print("best move: {}".format(best))

        self.select_move(best[0], best[1], best[2], best[3])

    def select_move(self, source_row, source_column, dest_row, dest_column):
        self.game.select_move(source_row, source_column, dest_row, dest_column)

    def select_additional_jump(self, source_row, source_column):
        _, moves = self.board.get_possible_moves(source_row, source_column)

        board_config = self.board.get_board_config(self.team)
        self.board_configs.append(board_config)

        lookahead = lookahead_config(self.board.get_8_board_config(self.team), self.team)
        scores = []

        if lookahead:
            for src, dst, new_board in lookahead:
                scores.append(self.check_move(new_board, src[0], src[1], dst[0], dst[1]))
        else:
            for move in moves:
                scores.append(self.check_move(board_config, source_row, source_column, move[0], move[1]))

        # sort scores and use the last one
        best = sorted(scores, key=lambda x: x[4])[-1]
        print("best addl move: {}".format(best))

        self.select_move(best[0], best[1], best[2], best[3])
