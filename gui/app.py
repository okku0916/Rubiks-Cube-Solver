from cube.state import CubeState
import cube.constants as const
from visualization.plot_3d import plot_3d
from recognition.recognition import CubeRecognition
from solver.brute_force import start_brute_force
from solver.two_phase_algorithm import TPASolver
import threading
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog

class RubiksCubeApp:
    def __init__(self, root):
        self.state = CubeState() # キューブの状態
        self.root = root
        self.canvas = tk.Canvas(self.root, width=600, height=750)

        self.scramble_label = tk.Label(self.root, text="                                  ", fg="black", bg="white",
                               font=("Arial", 14, "bold"))
        self.scramble_label.place(x=25, y=700)
        self.progress_win = None

        self.cancel_flag = False
        self.rotate_label = None
        self.solve_label = None

        U = tk.Button(self.root, text="U", width=4, height=2, command=lambda: self.handle_rotate("U", 1, True))
        U.place(x=25, y=450)
        R = tk.Button(self.root, text="R", width=4, height=2, command=lambda: self.handle_rotate("R", 1, True))
        R.place(x=100, y=450)
        L = tk.Button(self.root, text="L", width=4, height=2, command=lambda: self.handle_rotate("L", 1, True))
        L.place(x=175, y=450)
        F = tk.Button(self.root, text="F", width=4, height=2, command=lambda: self.handle_rotate("F", 1, True))
        F.place(x=250, y=450)
        B = tk.Button(self.root, text="B", width=4, height=2, command=lambda: self.handle_rotate("B", 1, True))
        B.place(x=325, y=450)
        D = tk.Button(self.root, text="D", width=4, height=2, command=lambda: self.handle_rotate("D", 1, True))
        D.place(x=400, y=450)
        U3 = tk.Button(self.root, text="U'", width=4, height=2, command=lambda: self.handle_rotate("U'", 1, True))
        U3.place(x=25, y=500)
        R3 = tk.Button(self.root, text="R'", width=4, height=2, command=lambda: self.handle_rotate("R'", 1, True))
        R3.place(x=100, y=500)
        L3 = tk.Button(self.root, text="L'", width=4, height=2, command=lambda:self.handle_rotate("L'", 1, True))
        L3.place(x=175, y=500)
        F3 = tk.Button(self.root, text="F'", width=4, height=2, command=lambda: self.handle_rotate("F'", 1, True))
        F3.place(x=250, y=500)
        B3 = tk.Button(self.root, text="B'", width=4, height=2, command=lambda: self.handle_rotate("B'", 1, True))
        B3.place(x=325, y=500)
        D3 = tk.Button(self.root, text="D'", width=4, height=2, command=lambda: self.handle_rotate("D'", 1, True))
        D3.place(x=400, y=500)

        plot3d = tk.Button(self.root, text="3D", width=8, height=5, command=lambda: plot_3d(self.state.rubiks))
        plot3d.place(x=450, y=20)

        scramble_botton = tk.Button(self.root, text="Generate Scramble", width=12, height=2, command=lambda: self.handle_scramble())
        scramble_botton.place(x=25, y=600)

        recognition_button = tk.Button(self.root, text="Recognize", width=5, height=2, command=lambda: self.handle_recognition())
        recognition_button.place(x=25, y=650)

        solve_brute_force_botton = tk.Button(root, text="Brute Force", width=7, height=2, command=lambda: self.handle_solve_brute_force())
        solve_brute_force_botton.place(x=335, y=600)

        solve_tpa_botton = tk.Button(root, text="TPA(Greedy)", width=12, height=2, command=lambda: self.handle_solve_tpa(True))
        solve_tpa_botton.place(x=440, y=600)

        solve_tpa_set_limit_botton = tk.Button(root, text="TPA with limit", width=12, height=2, command=lambda: self.handle_solve_tpa(False))
        solve_tpa_set_limit_botton.place(x=440, y=650)

        self.canvas.pack()
        self.draw()

    def draw(self):
        self.canvas.delete("all") # 描画をクリア

        self.state.rubiks = self.edge_corner_to_arrays(self.state.cp, self.state.co, self.state.ep, self.state.eo) # 配列を変換
        
        # 描画
        sp_x = 150 # U面の左上の座標 startpoint
        sp_y = 100
        side = 30 # １ブロックの一辺の長さ
        space = 10 # 描画する際の面同士の隙間

        face = 0
        for i in self.state.rubiks:  # i:面を取り出す
            face += 1
            row = 0
            for j in i:  # j:行を取り出す
                row += 1
                column = 0
                for color in j:  # k:色を取り出す
                    column += 1
                    if face == 1 or face == 3:
                        self.canvas.create_rectangle(sp_x + side * (column - 1), sp_y + (side*3+space)/2 * (face - 1) + side * (row - 1),
                                                sp_x + side * column, sp_y + (side*3+space)/2 * (face - 1) + side * row, fill=color)
                    if face == 6:
                        self.canvas.create_rectangle(sp_x + side * (column - 1), (sp_y+side*6+space*2) + side * (row - 1), sp_x + side * column,
                                                (sp_y+side*6+space*2) + side * row, fill=color)
                    if face == 2 or face == 4:
                        self.canvas.create_rectangle((sp_x - side * 3 - space) + (side * 6 + space * 2)/2 * (face - 2) + side * (column - 1), (sp_y + side * 3 + space) + side * (row - 1),
                                                (sp_x - side * 3 - space) + (side * 6 + space * 2)/2 * (face - 2) + side * column, (sp_y + side * 3 + space) + side * row, fill=color)
                    if face == 5:
                        self.canvas.create_rectangle((sp_x + side * 6 + space * 2) + side * (column - 1), (sp_y + side * 3 + space) + side * (row - 1), (sp_x + side * 6 + space * 2) + side * column,
                                                (sp_y + side * 3 + space) + side * row, fill=color)

        self.canvas.create_rectangle(sp_x, sp_y, sp_x + side * 3, sp_y + side * 3, width=3)
        self.canvas.create_rectangle(sp_x - side * 3 - space, sp_y + side * 3 + space, sp_x - space, sp_y + side * 6 + space, width=3)
        self.canvas.create_rectangle(sp_x, sp_y + side * 3 + space, sp_x + side * 3, sp_y + side * 6 + space, width=3)
        self.canvas.create_rectangle(sp_x + side * 3 + space, sp_y + side * 3 + space, sp_x + side * 6 + space, sp_y + side * 6 + space, width=3)
        self.canvas.create_rectangle(sp_x + side * 6 + space * 2, sp_y + side * 3 + space, sp_x + side * 9 + space * 2, sp_y + side * 6 + space, width=3)
        self.canvas.create_rectangle(sp_x, sp_y + side * 6 + space * 2, sp_x + side * 3, sp_y + side * 9 + space * 2, width=3)

        self.rotate_label = self.canvas.create_text(50, 430, text="回転", font=("Arial", 18))
        self.scramble_and_recognize_label = self.canvas.create_text(145, 580, text="スクランブル 画像認識", font=("Arial", 18))
        self.solve_label = self.canvas.create_text(385, 580, text="解法選択", font=("Arial", 18))

    # 回転
    def handle_rotate(self, how, num_rotate, do_draw):
        self.state.rotate(how, num_rotate)
        if do_draw:
            self.draw()

    def handle_scramble(self):
        scramble_label = self.state.scramble()
        self.scramble_label["text"] = f"{scramble_label}"
        self.draw()

    def handle_recognition(self):
        recognition = CubeRecognition()
        arrays = recognition.recognize() # カメラを起動
        cp, co, ep, eo = self.arrays_to_edge_corner(arrays) # 配列を変換
        # 認識が全て完了されている時にセットする
        if cp is None:
            pass
        else:
            self.state.update_state(cp, co, ep, eo)
            self.draw()

    # キューブの3次元配列をcp,co,ep,eo配列に変換する
    def arrays_to_edge_corner(self, arrays):
        if arrays is None:
            print("認識した色のデータが不完全です。")
            return None, None, None, None
        cp, co, ep, eo = [0] * 8, [0] * 8, [0] * 12, [0] * 12

        # コーナーの配置
        for i in range(8):  # コーナー8個をループ
            corner_colors = [arrays[a][b][c] for (a, b, c) in const.CORNER_FACE_POSITIONS[i]]  # 実際の各コーナーの色を取得
            for j in range(8):  # どのコーナーかを判定
                target_colors = [const.FACE_NAMES[k] for k in const.CORNER_FACES[j]]  # 完成状態のコーナーの色を取得

                for orientation in range(3):  # 向きを変えて判定
                    rotated_corner_colors = [corner_colors[(k - orientation) % 3] for k in range(3)]
                    if rotated_corner_colors == target_colors:
                        cp[i] = j
                        co[i] = orientation
                        break
                else:  # 二重ループを抜ける
                    continue
                break

        # エッジの配置
        for i in range(12):  # エッジ12個をループ
            edge_colors = [arrays[a][b][c] for (a, b, c) in const.EDGE_FACE_POSITIONS[i]]  # 各エッジの色を取得

            for j in range(12):  # どのエッジかを判定
                target_colors = [const.FACE_NAMES[k] for k in const.EDGE_FACES[j]]  # 完成状態のエッジの色を取得

                if edge_colors == target_colors:
                    ep[i] = j
                    eo[i] = 0
                    break
                elif edge_colors[::-1] == target_colors:  # エッジが逆の場合
                    ep[i] = j
                    eo[i] = 1
                    break

        # 認識のエラーを検知
        visited_cp = [False] * 8
        for i in cp:
            visited_cp[i] = True
        if not all(visited_cp):
            print("認識エラー")
            return None, None, None, None

        visited_ep = [False] * 12
        for i in ep:
            visited_ep[i] = True
        if not all(visited_ep):
            print("認識エラー")
            return None, None, None, None

        return cp, co, ep, eo

    # cp,co,ep,eo配列をキューブの3次元配列に変換する
    def edge_corner_to_arrays(self, cp, co, ep, eo):

        # 6面 x 3x3 の空の配列
        arrays = [[[None for _ in range(3)] for _ in range(3)] for _ in range(6)]

        # コーナー配置
        for i in range(8):
            permutation = cp[i]
            orientation = co[i]
            faces = const.CORNER_FACES[permutation] # コーナーの面(3つのリスト)
            changed = [faces[(j + orientation) % 3] for j in range(3)] # 面の順番を変える
            for j in range(3): # 3つの面を貼るためにループ
                face, row, column = const.CORNER_FACE_POSITIONS[i][j]
                arrays[face][row][column] = const.FACE_COLORS[changed[j]]

        # エッジ配置
        for i in range(12):
            permutation = ep[i]
            orientation = eo[i]
            faces = const.EDGE_FACES[permutation]
            if orientation == 0:
                changed = faces
            else:
                changed = faces[::-1] # 配置を逆にする
            for j in range(2):
                face, row, column = const.EDGE_FACE_POSITIONS[i][j]
                arrays[face][row][column] = const.FACE_COLORS[changed[j]]

        # センター配置
        for i in range(6):
            arrays[i][1][1] = const.FACE_COLORS[i]

        return arrays

    def handle_solve_brute_force(self):
        self.cancel_flag = False
        self.show_progress_window()

        # 探索完了時に呼ばれるコールバック関数を定義
        def on_finish(result_steps, status, elapsed_time):
            self.root.after(0, self.close_progress_window)
            if status == "success":
                print(*result_steps)  # アンパックして表示
                print(f"elapsed_time: {elapsed_time:.3f} seconds")
                print(f"{len(result_steps)} 手かかりました")
                self.root.after(0, self.update_gui_after_solve, result_steps, elapsed_time)
            elif status == "cancelled":
                print("キャンセルされました。")
        # Solverには状態とコールバック関数を渡す
        thread = threading.Thread(
            target=lambda: start_brute_force(self.state, on_finish, is_cancelled=lambda: self.cancel_flag)
        )
        thread.start()

    def handle_solve_tpa(self, is_greedy):
        time_limit = 1
        if is_greedy == True: # 貪欲
            is_greedy = True
        else: # 時間制限を指定できるTPA
            time_limit_str = simpledialog.askstring("Set Time Limit", "時間制限を秒で入力してください(例: 60)")
            if time_limit_str is None:
                return  
            try:
                time_limit = int(time_limit_str)
                if time_limit <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("エラー", "正しい正の整数を入力してください。")
                return

        self.cancel_flag = False
        self.show_progress_window()

        # 探索完了時に呼ばれるコールバック関数を定義
        def on_finish(result_steps, status, elapsed_time):
            self.root.after(0, self.close_progress_window)
            if status == "success":
                print("----------------------------")
                print (*result_steps)
                print(f"合計探索時間: {elapsed_time:.3f} seconds")
                print(f"合計手数: {len(result_steps)} 手")
                print("----------------------------")
                self.root.after(0, self.update_gui_after_solve, result_steps, elapsed_time)
            elif status == "cancelled":
                print("キャンセルされました。")
            elif status == "failed":
                self.root.after(0, lambda: messagebox.showwarning("エラー", f"{time_limit}秒では解が見つかりませんでした。"))
                print(f"{time_limit}秒では解が見つかりませんでした。")
        # TPASolverを作成してスレッドを起動
        solver = TPASolver(self.state, on_finish, lambda: self.cancel_flag, is_greedy, time_limit)
        thread = threading.Thread(target=solver.start_tpa)
        thread.start()

    def update_gui_after_solve(self, steps, elapsed_time):
        # この関数は確実にメインスレッドで実行されるため、安全にTkinterを操作できる
        display_steps = " ".join(steps) # 手順を文字列に変換
        messagebox.showinfo("解法", f"{display_steps}\n合計{len(steps)} 手\n{elapsed_time:.3f} seconds")
        
        # キューブの状態を手順通りに回して再描画
        for step in steps:
            self.state.rotate(step, 1)
        self.draw()

    def show_progress_window(self):
        if self.progress_win is not None:
            return
        self.root.update_idletasks()  # 最新のサイズ情報を強制更新
        # メイン画面の上に新しいウィンドウを作成
        self.progress_win = tk.Toplevel(self.root)
        self.progress_win.title("探索中")

        # 真ん中に配置するための座標を計算
        width = 200
        height = 100
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        self.progress_win.geometry(f"{width}x{height}+{x}+{y}")
        
        tk.Label(self.progress_win, text="最適解を探索しています...").pack(pady=10)
        
        # このウィンドウ以外の操作をすべてブロックする
        self.progress_win.grab_set()

        cancel_btn = tk.Button(self.progress_win, text="キャンセル", command=self.cancel_search)
        cancel_btn.pack()

    def close_progress_window(self):
        if self.progress_win is not None:
            self.progress_win.grab_release() # ブロック解除
            self.progress_win.destroy()      # ウィンドウを破棄
            self.progress_win = None
        
    def cancel_search(self):
        self.cancel_flag = True
