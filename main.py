from gui.app import RubiksCubeApp
import tkinter as tk
if __name__ == "__main__":
    root = tk.Tk() # tkinterのキャンバスを作成
    root.title("Rubiks-Cube-Solver")
    rubiks_cube = RubiksCubeApp(root)
    root.mainloop()