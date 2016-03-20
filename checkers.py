# has the game logic required to play a checkers game

import Tkinter as tk
import sys
from board import (CheckersBoard as CB,
                   Team as Team)


from human_player import HumanPlayer

class CheckersGame(object):
    def __init__(self, root, board):
        # have buttons to push each piece? Is that possible?
        self.root = root
        self.board = board

        self.human_vs_AI = tk.Button(self.root,
            text="Start 1-player Game",
            command=self.start_human_vs_ai_game)
        self.board.create_window(140, 155, anchor=tk.NW, window=self.human_vs_AI)

        self.human_vs_human = tk.Button(self.root,
            text="Start 2-player Game",
            command=self.start_human_vs_human_game)
        self.board.create_window(140, 190, anchor=tk.NW, window=self.human_vs_human)

        self.AI_vs_AI = tk.Button(self.root,
            text="Start AI vs AI Game",
            command=self.start_ai_vs_ai_game)
        self.board.create_window(140, 225, anchor=tk.NW, window=self.AI_vs_AI)

        self.human_vs_human.invoke()  # XXX

    def clear_buttons(self):
        if self.human_vs_AI:
            self.human_vs_AI.destroy()
        if self.human_vs_human:
            self.human_vs_human.destroy()
        if self.AI_vs_AI:
            self.AI_vs_AI.destroy()

    def start_human_vs_ai_game(self):
        self.clear_buttons()

    def start_human_vs_human_game(self):
        self.clear_buttons()

        self.team_black = HumanPlayer(self, self.board, Team.Black)
        self.team_red = HumanPlayer(self, self.board, Team.Red)

        self.turn = self.team_black

        self.team_black.choose_move()

    def start_ai_vs_ai_game(self):
        self.clear_buttons()

    def select_move(self, source_row, source_column, dest_row, dest_column):
        # execute the move.
        # if the move is a jump, check if that piece can jump again, and if so,
        # let the player to play again
        
        is_jump, _ = self.board.get_possible_moves(source_row, source_column)

        # assume move is valid
        self.board.move_piece(source_row, source_column, dest_row, dest_column)
        
        if (is_jump):
            self.board.remove_piece((source_row + dest_row) / 2, (source_column + dest_column) / 2)

            can_jump, _ = self.board.get_possible_moves(dest_row, dest_column)
            if (can_jump):
                self.turn.select_additional_jump(dest_row, dest_column)
            else:
                self.next_turn()
        else:
            self.next_turn()

    def next_turn(self):
        if (self.turn == self.team_black):
            self.turn = self.team_red
            self.team_red.choose_move()
        else:
            self.turn = self.team_black
            self.team_black.choose_move()

    def game_over(self):
        if (self.turn == self.team_black):
            print "RED WINS"
        else:
            print "BLACK WINS"

def close(event):
    sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    board = CB(root)
    root.bind('<Escape>', close)
    board.pack(side=tk.LEFT)

    CheckersGame(root, board)

    root.mainloop()
