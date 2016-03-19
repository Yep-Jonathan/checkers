# has the game logic required to play a checkers game

import Tkinter as tk
import sys
from board import (CheckersBoard as CB,
                   Team as Team)


import human_player

class CheckersGame(object):
    def __init__(self, root, board):
        # have buttons to push each piece? Is that possible?
        self.root = root
        self.board = board

        self.turn = Team.Black

        self.human_vs_AI = tk.Button(self.root,
            text="Start 1-player Game",
            command=self.start_human_vs_ai_game)
        self.board.create_window(150, 155, anchor=tk.NW, window=self.human_vs_AI)

        self.human_vs_human = tk.Button(self.root,
            text="Start 2-player Game",
            command=self.start_human_vs_human_game)
        self.board.create_window(150, 190, anchor=tk.NW, window=self.human_vs_human)

        self.AI_vs_AI = tk.Button(self.root,
            text="Start AI vs AI Game",
            command=self.start_ai_vs_ai_game)
        self.board.create_window(150, 225, anchor=tk.NW, window=self.AI_vs_AI)

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

        # TODO: list of black pieces and red pieces

        self.team_black = human_player(self, self.board, black_pieces)
        self.team_red = human_player(self, self.board, red_pieces)

        self.team_black.choose_move()

    def start_ai_vs_ai_game(self):
        self.clear_buttons()

    def next_turn():
        if (self.turn == Team.Black):
            self.turn = Team.Red
            self.team_red.choose_move()
        else:
            self.turn = Team.Black
            self.team_black.choose_move()

def close(event):
    sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    board = CB(root)
    root.bind('<Escape>', close)
    board.pack(side=tk.LEFT)

    CheckersGame(root, board)

    root.mainloop()
