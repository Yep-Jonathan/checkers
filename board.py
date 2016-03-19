# A Representation of a checkers board, drawn using Tkinter

import Tkinter as tk
# import random

class CheckersBoard(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=400, height=400, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = 8
        self.columns = 8
        self.cellwidth = 50
        self.cellheight = 50
        self.piece_spacing = 10

        self.rect = {}
        self.oval = {}
        for column in range(8):
            for row in range(8):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                if ((column + row) % 2 == 0):
                    self.canvas.create_rectangle(x1,y1,x2,y2, fill="red", tags="emptySpaces")
                else:
                    self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="#444444", tags="board")
                    if (row in [0, 1, 2]):
                        self.oval[row,column] = self.create_black_piece(row, column)
                    elif (row in [5, 6, 7]):
                        self.oval[row,column] = self.create_red_piece(row, column)



        #self.redraw(1000)

    def create_piece(self, row, column, is_black=False, is_king=False):
        x1 = column*self.cellwidth
        y1 = row * self.cellheight
        x2 = x1 + self.cellwidth
        y2 = y1 + self.cellheight

        return self.canvas.create_oval(x1+self.piece_spacing, y1+self.piece_spacing,
                                       x2-self.piece_spacing, y2-self.piece_spacing,
                                       fill="black" if is_black else "red",
                                       outline="#444444",
                                       tags="pieces")

    def create_black_piece(self, row, column, is_king=False):
        # Creates an black oval at the specified row,column
        return self.create_piece(row, column, True, is_king)

    def create_red_piece(self, row, column, is_king=False):
        # Creates an red piece at the row,column
        return self.create_piece(row, column, False, is_king)

    # def redraw(self, delay):
    #     self.canvas.itemconfig("rect", fill="#444444")
    #     self.canvas.itemconfig("pieces", fill="#444444")
    #     for i in range(10):
    #         row = random.randint(0,7)
    #         col = random.randint(0,7)
    #         if ((col+row) % 2 == 1):
    #             item_id = self.oval[row,col]
    #             self.canvas.itemconfig(item_id, fill="red")
    #     self.after(delay, lambda: self.redraw(delay))

if __name__ == "__main__":
    app = CheckersBoard()
    app.mainloop()