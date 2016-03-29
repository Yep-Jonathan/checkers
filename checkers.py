# has the game logic required to play a checkers game

import Tkinter as tk
import sqlite3 as lite
import sys
from board import (CheckersBoard as CB,
                   Team as Team)

from human_player import HumanPlayer
from random_player import RandomPlayer
from ai_player import AIPlayer
from mm_player import MMPlayer
from trained_player import TrainedPlayer


class CheckersGame(object):
    def __init__(self, root, board, training=False, ui=True):
        self.root = root
        self.board = board
        self.training = training
        self.ui = ui
        if(training is False and ui is True):
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

        # self.human_vs_human.invoke()  # XXX

    def clear_buttons(self):
        if self.human_vs_AI:
            self.human_vs_AI.destroy()
        if self.human_vs_human:
            self.human_vs_human.destroy()
        if self.AI_vs_AI:
            self.AI_vs_AI.destroy()

    def start_human_vs_ai_game(self):
        self.clear_buttons()

        self.team_black = HumanPlayer(self, self.board, Team.Black)
        self.team_red = MMPlayer(self, self.board, Team.Red)

        self.start_game()

    def start_human_vs_human_game(self):
        self.clear_buttons()

        self.team_black = HumanPlayer(self, self.board, Team.Black)
        self.team_red = HumanPlayer(self, self.board, Team.Red)

        self.start_game()

    def start_ai_vs_ai_game(self):
        self.clear_buttons()
        self.team_black = MMPlayer(self, self.board, Team.Black)
        self.team_red = MMPlayer(self, self.board, Team.Red)

        self.start_game()

    def start_ai_vs_ai_no_ui_game(self):
        self.team_black = MMPlayer(self, self.board, Team.Black)
        self.team_red = MMPlayer(self, self.board, Team.Red)

        self.start_game()

    def start_ai_training_game(self):
        self.team_black = AIPlayer(self, self.board, Team.Black)
        self.team_red = AIPlayer(self, self.board, Team.Red)

        self.start_game()

    def start_game(self):
        self.turn = self.team_black

        self.team_black.choose_move()

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
        # if self.training is False and self.ui is True:
        #     if (self.turn == self.team_black):
        #         print "RED WINS"
        #     else:
        #         print "BLACK WINS"
        #     exit()
        self.losing_configs = []
        self.winning_configs = []
        if (self.turn == self.team_black):
            self.losing_configs = self.team_black.board_configs
            self.winning_configs = self.team_red.board_configs
            print "RED WINS"
        else:
            self.losing_configs = self.team_red.board_configs
            self.winning_configs = self.team_black.board_configs
            print "BLACK WINS"
        # self.log_results()
        exit()

    def log_results(self):
        print "Logging results"
        conn = lite.connect("temp.db")
        c = conn.cursor()

        # Create table if not exists
        tableName = "trainingdata"
        tableCreationQuery = "CREATE TABLE IF NOT EXISTS " + tableName + " (config text PRIMARY KEY, wins integer, total integer)"
        c.execute(tableCreationQuery)

        for config in self.losing_configs:
            updateQuery = "UPDATE " + tableName + " SET total = total + 1 WHERE config = '" + str(config) + "'"
            c.execute(updateQuery)
            if c.rowcount is 0:
                insertionQuery = "INSERT INTO " + tableName + " VALUES ('" + str(config) + "', 0 , 1)"
                c.execute(insertionQuery)
        conn.commit()

        for config in self.winning_configs:
            updateQuery = "UPDATE " + tableName + " SET total = total + 1, wins = wins + 1 WHERE config = '" + str(config) + "'"
            c.execute(updateQuery)
            if c.rowcount is 0:
                insertionQuery = "INSERT INTO " + tableName + " VALUES ('" + str(config) + "', 1 , 1)"
                c.execute(insertionQuery)
        conn.commit()

        conn.close()



def close(event):
    sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    board = CB(root)
    root.bind('<Escape>', close)
    board.pack(side=tk.LEFT)

    if (len(sys.argv) > 1 and sys.argv[1] == 'training'):
        cg = CheckersGame(root, board, True)
        cg.start_ai_training_game();
    if (len(sys.argv) > 1 and sys.argv[1] == 'ai_vs_ai'):
        cg = CheckersGame(root, board, False, False)
        cg.start_ai_vs_ai_no_ui_game();
    else:
        cg = CheckersGame(root, board)

    root.mainloop()
