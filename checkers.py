# has the game logic required to play a checkers game

import Tkinter as tk
import sys
from board import CheckersBoard as CB



def close(event):
    sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = CB(root)
    root.bind('<Escape>', close)
    app.pack(side=LEFT)

    app.move_piece(2, 1, 3, 2)

    app.mainloop()


