from tkinter import Tk
import sys

root = Tk()
root.title("五子棋")
if sys.platform.lower().startswith("win"):
    root.state("zoomed")

root.mainloop()