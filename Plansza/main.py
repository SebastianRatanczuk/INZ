from tkinter import *

import matplotlib

matplotlib.use("TkAgg")


class Widget(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        self.winfo_toplevel().title("Szaszki")
        self.winfo_toplevel().geometry("1200x900")
        self.make_chess_board()

    def make_chess_board(self):
        board_size = 600
        checker_size = board_size / 8
        self.ImagePanel = Canvas(self.parent, height=board_size, width=board_size)
        self.ImagePanel.pack(pady=20)

        color = 0

        for y in range(8):
            for x in range(8):
                x1 = x * checker_size
                y1 = y * checker_size
                x2 = x1 + checker_size
                y2 = y1 + checker_size
                if color:
                    self.ImagePanel.create_rectangle((x1, y1, x2, y2), fill="#d8debd", outline="")
                else:
                    self.ImagePanel.create_rectangle((x1, y1, x2, y2), fill="#727567", outline="")

                color = not color
            color = not color


if __name__ == '__main__':
    root = Tk()
    root.iconphoto(False, PhotoImage(file='sources/chess-3413420_640_cr.png'))
    chessBoard = Widget(root)
    root.mainloop()
