from solve3by3 import RubiksCube
import tkinter as tk
if __name__ == "__main__":
    root = tk.Tk() # tkinterのキャンバスを作成
    rubiks_cube = RubiksCube(root)
    root.mainloop()