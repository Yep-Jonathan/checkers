# implementation of a human checkers player

from player import CheckersPlayer
import numpy as np


class RandomPlayer(CheckersPlayer):

    def choose_move(self):
        # choose a random play from the list of possible moves

        possible_moves = self.get_possible_moves()

        count = 0
        for _, dest_list in possible_moves.iteritems():
            count += len(dest_list)

        if count == 0:
            return  # game is over

        selected_move = np.random.randint(count)

        count = 0
        for (source_row, source_column), dest_list in possible_moves.iteritems():
            if (selected_move < (count + len(dest_list))):
                dest_row, dest_column = dest_list[count - selected_move]
                print "moved from (%s, %s) to (%s, %s)" % \
                    (source_row, source_column, dest_row, dest_column)
                self.game.select_move(source_row, source_column,
                    dest_row, dest_column)
                break
            else:
                count += len(dest_list)

    def select_additional_jump(self, source_row, source_column):
        _, moves = self.board.get_possible_moves(source_row, source_column)

        selected_move = np.random.randint(len(moves))
        dest_row, dest_column = moves[selected_move]

        self.game.select_move(source_row, source_column, dest_row, dest_column)
