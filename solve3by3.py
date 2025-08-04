from tkinter import *
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
from plot_3d import *
from recognition import CubeRecognition
import random
import sys
import copy
import threading
from math import factorial, comb
import time
import timeout_decorator

# 3×3 コーナー、エッジの位置と向きだけで表現する版

class RubiksCube:
    def __init__(self):
        self.rubiks = [[[None for _ in range(3)] for _ in range(3)] for _ in range(6)]
        self.cp = [0, 1, 2, 3, 4, 5, 6, 7] # コーナーの位置
        self.co = [0, 0, 0, 0, 0, 0, 0, 0] # コーナーの向き (0=正しい向き, 1=反時計回り, 2=時計回り)
        self.ep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] # エッジの位置
        self.eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # エッジの向き (0=正しい向き, 1=逆向き)

        root = Tk() # tkinterのキャンバスを作成
        canvas = Canvas(root, width=600, height=750)

        self.scramble_label = Label(root, text="                                  ", fg="black", bg="white",
                               font=("Arial", 18, "bold"))
        self.scramble_label.place(x=25, y=700)
        self.root = root
        self.canvas = canvas

        self.max_steps = 24 # 最大許容手数、探索を続ける最大の手数
        self.arrays_copy = []
        self.solutions = [] # 解法を保存するリスト
        self.min_steps = 10000 # 最善手の手数
        self.is_greedy = False # 貪欲法を使うかどうか


        U = Button(self.root, text="U", width=4, height=2, command=lambda: self.rotate("U", 1, True, [self.cp, self.co, self.ep, self.eo]))
        U.place(x=25, y=450)
        R = Button(self.root, text="R", width=4, height=2, command=lambda: self.rotate("R", 1, True, [self.cp, self.co, self.ep, self.eo]))
        R.place(x=100, y=450)
        L = Button(self.root, text="L", width=4, height=2, command=lambda: self.rotate("L", 1, True, [self.cp, self.co, self.ep, self.eo]))
        L.place(x=175, y=450)
        F = Button(self.root, text="F", width=4, height=2, command=lambda: self.rotate("F", 1, True, [self.cp, self.co, self.ep, self.eo]))
        F.place(x=250, y=450)
        B = Button(self.root, text="B", width=4, height=2, command=lambda: self.rotate("B", 1, True, [self.cp, self.co, self.ep, self.eo]))
        B.place(x=325, y=450)
        D = Button(self.root, text="D", width=4, height=2, command=lambda: self.rotate("D", 1, True, [self.cp, self.co, self.ep, self.eo]))
        D.place(x=400, y=450)
        U3 = Button(self.root, text="U'", width=4, height=2, command=lambda: self.rotate("U'", 1, True, [self.cp, self.co, self.ep, self.eo]))
        U3.place(x=25, y=500)
        R3 = Button(self.root, text="R'", width=4, height=2, command=lambda: self.rotate("R'", 1, True, [self.cp, self.co, self.ep, self.eo]))
        R3.place(x=100, y=500)
        L3 = Button(self.root, text="L'", width=4, height=2, command=lambda:self.rotate("L'", 1, True, [self.cp, self.co, self.ep, self.eo]))
        L3.place(x=175, y=500)
        F3 = Button(self.root, text="F'", width=4, height=2, command=lambda: self.rotate("F'", 1, True, [self.cp, self.co, self.ep, self.eo]))
        F3.place(x=250, y=500)
        B3 = Button(self.root, text="B'", width=4, height=2, command=lambda: self.rotate("B'", 1, True, [self.cp, self.co, self.ep, self.eo]))
        B3.place(x=325, y=500)
        D3 = Button(self.root, text="D'", width=4, height=2, command=lambda: self.rotate("D'", 1, True, [self.cp, self.co, self.ep, self.eo]))
        D3.place(x=400, y=500)

        plot3d = Button(self.root, text="3D", width=8, height=5, command=lambda: plot_3d(self.rubiks))
        plot3d.place(x=450, y=20)

        scramble_botton = Button(self.root, text="Generate Scramble", width=12, height=2, command=lambda: self.scramble())
        scramble_botton.place(x=25, y=600)

        recognition_button = Button(self.root, text="Recognize", width=5, height=2, command=lambda: self.start_recognition())
        recognition_button.place(x=175, y=600)

        solve_random_botton = Button(root, text="Random", width=4, height=2, command=lambda: self.solve("random"))
        solve_random_botton.place(x=260, y=600)

        solve_brute_force_botton = Button(root, text="Brute Force", width=7, height=2, command=lambda: self.solve("brute_force"))
        solve_brute_force_botton.place(x=335, y=600)

        solve_tpa_botton = Button(root, text="TPA(Greedy)", width=12, height=2, command=lambda: self.solve("tpa"))
        solve_tpa_botton.place(x=440, y=600)

        solve_tpa_set_limit_botton = Button(root, text="TPA with limit", width=12, height=2, command=lambda: self.solve("tpa_set_limit"))
        solve_tpa_set_limit_botton.place(x=440, y=650)
        self.draw()

    def draw(self):
        self.canvas.delete("all") # 描画をクリア
        self.canvas.pack()

        self.rubiks = self.edge_corner_to_arrays(self.cp, self.co, self.ep, self.eo) # 配列を変換
        
        # 描画
        sp_x = 150 # U面の左上の座標 startpoint
        sp_y = 100
        side = 30 # １ブロックの一辺の長さ
        space = 10 # 描画する際の面同士の隙間

        face = 0
        for i in self.rubiks:  # i:面を取り出す
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

        self.canvas.mainloop()


    # 回転
    def rotate(self, how, num_rotate, do_draw, arrays):
        cp, co, ep, eo = arrays
        num = 1 # 一回の操作での回転数

        # 'と2を変換
        if "'" in how:
            how = how[0]
            num = 3
        elif "2" in how:
            how = how[0]
            num = 2

        # 回転を定義
        rotate = []
        if how == "U":
            # Uは向きは変わらない
            rotate = [[3, 0, 1, 2, 4, 5, 6, 7], [0] * 8, [3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11], [0] * 12]
        elif how == "R":
            # Rは向きが変わる
            rotate = [[4, 1, 2, 0, 7, 5, 6, 3], [1, 0, 0, 2, 2, 0, 0, 1], [8, 1, 2, 3, 11, 5, 6, 7, 4, 9, 10, 0], [0] * 12]
        elif how == "L":
            rotate = [[0, 2, 6, 3, 4, 1, 5, 7], [0, 2, 1, 0, 0, 1, 2, 0], [0, 1, 10, 3, 4, 5, 9, 7, 8 ,2 ,6, 11], [0] * 12]
        elif how == "F":
            rotate = [[1, 5, 2, 3, 0, 4, 6, 7], [2, 1, 0, 0, 1, 2, 0, 0], [0, 9, 2, 3, 4, 8, 6, 7, 1, 5, 10, 11], [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]]
        elif how == "B":
            rotate = [[0, 1, 3, 7, 4, 5, 2, 6], [0, 0, 2, 1, 0, 0, 1, 2], [0, 1, 2, 11, 4, 5, 6, 10, 8, 9, 3, 7], [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]]
        elif how == "D":
            # Dは向きは変わらない
            rotate = [[0, 1, 2, 3, 5, 6, 7, 4], [0] * 8, [0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11], [0] * 12]

        for n in range(num_rotate): # num_rotate回転する
            for i in range(num): # U'は3回回すので、3回ループ、U2は2回ループ
                # スライスで更新することで再代入にならないため、arraysを更新できる
                # 再代入だと配列の参照が変わってしまうため、更新できない
                cp[:] = [cp[j] for j in rotate[0]] # 位置は置き換え
                co[:] = [(co[j] + rotate[1][k]) % 3 for k, j in enumerate(rotate[0])] # 向きは操作で捻れる
                ep[:] = [ep[j] for j in rotate[2]]
                eo[:] = [(eo[j] + rotate[3][k]) % 2 for k, j in enumerate(rotate[2])]

        if do_draw:
            self.draw()

    def scramble(self):
        # 配色を初期化
        self.cp = [0, 1, 2, 3, 4, 5, 6, 7] # コーナーの位置
        self.co = [0, 0, 0, 0, 0, 0, 0, 0] # コーナーの向き (0=正しい向き, 1=反時計回り, 2=時計回り)
        self.ep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] # エッジの位置
        self.eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # エッジの向き (0=正しい向き, 1=逆向き)

        n = random.randint(18,22)
        scramble = []
        for _ in range(n):
            while True:
                new = random.choice(["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"])
                if self.is_valid(scramble, new):
                    self.rotate(new, 1, False, [self.cp, self.co, self.ep, self.eo])
                    scramble.append(new)
                    break
        sc = ""
        for i in scramble:
            sc += f"{i} "
        self.scramble_label["text"] = f"{sc}"
        self.draw()

    def is_valid(self, steps, step):
        if steps != []:
            prev_step = steps[-1]
        else: # １手目は絶対有効
            return True

        # 直前の手と同じ面を回す場合は無効
        if step == prev_step[0] or step == prev_step[0] + "'" or step == prev_step[0] + "2":
            return False

        # 逆面を回す場合は辞書式なら有効
        if INVERSE[prev_step[0]] == step[0]:
            if prev_step[0] < step[0]:
                return False
        return True

    def is_complete(self, arrays):
        # for i in self.rubiks:
        #     for j in i:
        #         for k in j:
        #             if k != i[0][0]: # 面(i)のすべての色が同じでない場合
        #                 print("完成していません")
        #                 return False
        # print("完成しています")
        # return True

        cp, co, ep, eo = arrays
        if cp == [0, 1, 2, 3, 4, 5, 6, 7] and co == [0] * 8 and \
                ep == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] and eo == [0] * 12:
            print("完成しています")
            return True
        else:
            # print("完成していません")
            return False

    def start_recognition(self):
        recognition = CubeRecognition()
        arrays = recognition.recognize() # カメラを起動
        cp, co, ep, eo = self.arrays_to_edge_corner(arrays) # 配列を変換
        # 認識が全て完了されている時にセットする
        if cp is None:
            pass
        else:
            self.cp, self.co, self.ep, self.eo = cp, co, ep, eo
            self.draw()

    # キューブの3次元配列をcp,co,ep,eo配列に変換する
    def arrays_to_edge_corner(self, arrays):
        if arrays is None:
            print("認識した色のデータが不完全です。")
            return None, None, None, None
        cp, co, ep, eo = [0] * 8, [0] * 8, [0] * 12, [0] * 12

        # コーナーの配置
        for i in range(8):  # コーナー8個をループ
            corner_colors = [arrays[a][b][c] for (a, b, c) in CORNER_FACE_POSITIONS[i]]  # 実際の各コーナーの色を取得
            for j in range(8):  # どのコーナーかを判定
                target_colors = [FACE_NAMES[k] for k in CORNER_FACES[j]]  # 完成状態のコーナーの色を取得

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
            edge_colors = [arrays[a][b][c] for (a, b, c) in EDGE_FACE_POSITIONS[i]]  # 各エッジの色を取得

            for j in range(12):  # どのエッジかを判定
                target_colors = [FACE_NAMES[k] for k in EDGE_FACES[j]]  # 完成状態のエッジの色を取得

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
            faces = CORNER_FACES[permutation] # コーナーの面(3つのリスト)
            changed = [faces[(j + orientation) % 3] for j in range(3)] # 面の順番を変える
            for j in range(3): # 3つの面を貼るためにループ
                face, row, column = CORNER_FACE_POSITIONS[i][j]
                arrays[face][row][column] = FACE_COLORS[changed[j]]

        # エッジ配置
        for i in range(12):
            permutation = ep[i]
            orientation = eo[i]
            faces = EDGE_FACES[permutation]
            if orientation == 0:
                changed = faces
            else:
                changed = faces[::-1] # 配置を逆にする
            for j in range(2):
                face, row, column = EDGE_FACE_POSITIONS[i][j]
                arrays[face][row][column] = FACE_COLORS[changed[j]]

        # センター配置
        for i in range(6):
            arrays[i][1][1] = FACE_COLORS[i]

        return arrays

    # ---------- 状態のindex化-----------

    # cp,epのインデックス化
    # 辞書式で何番目かを求めることでインデックス化
    # 求める辞書式よりも前の個数を数え上げる
    def permutation_to_index(self, perm):
        array = copy.deepcopy(perm)  # 元の配列を変更しないようにコピー
        index = 0
        while len(array) > 1:
            a = len([l for l in array if l < array[0]]) # 配列の先頭より小さい数の個数
            index += a * factorial(len(array) - 1)
            array = array[1:] # 計算済みを除外
        return index

    # インデックスからcp,ep
    # n個の辞書式での順列を求める
    def index_to_permutation(self, index, n):
        array = list(range(n))
        permutation = []
        for i in range(n - 1, -1, -1): # n-1から0までループ
            f = factorial(i)
            j = index // f  # indexをfで割った商
            index %= f  # indexをfで割った余り
            permutation.append(array[j])  # 商の位置の要素を追加
            del array[j]  # 商の位置の要素を削除
        return permutation


    # co,eoのインデックス化
    # 向きは0,1,2の３種類なので3進数で表現
    # 上の桁からループして、毎回3を掛けて桁をずらす
    def orientation_to_index(self, ori, is_edge):
        index = 0
        for i in ori[:-1]: # 最後は他が決まれば一意に決まるから除外
            if is_edge: # エッジの向きは0,1の２種類なので2進数で表現
                index *= 2
            else: # コーナーの向きは0,1,2の３種類なので3進数で表現
                index *= 3
            index += i
        return index

    # インデックスからco,eo
    def index_to_orientation(self, index, is_edge):
        if is_edge:
            base = 2
            n = 11
        else:
            base = 3
            n = 7
        orientation = [0] * (n + 1)  # 向きの配列を初期化
        sum = 0
        for i in range(n - 1, -1, -1):  # n-1から0までループ
            orientation[i] = index % base
            index //= base  # indexをbaseで割った商
            sum += orientation[i]  # 向きの合計を計算
        if is_edge:
            orientation[-1] = (2 - sum % 2) % 2  # エッジの向きは最後の１つで決まる
        else:
            orientation[-1] = (3 - sum % 3) % 3 # コーナーの向きは最後の１つで決まる
        return orientation


    # UDスライス(中間層)のインデックス化
    # FR, FL, BL, BRの4つがある位置をTrue、それ以外をFalseとする要素数12のリストを引数に持たせ、それをインデックス化
    def udslice_comb_to_index(self, boolean_udslice):
        index = 0
        k = 3
        n = 11 # 位置
        # 後ろからFalseのとこで順列を計算し、Trueのとこでkを減らす
        while k >= 0:
            if boolean_udslice[n]:
                k -= 1
            else:
                index += comb(n, k)
            n -= 1
        return index # 正しい位置なら0を返す

    # インデックス化されたUDスライスのエッジの位置を変換
    def index_to_udslice_comb(self, index):
        boolean_udslice = [False] * 12
        k = 3
        n = 11
        # 後ろから順にインデックスを引いていく
        while k >= 0:
            if index >= comb(n, k):
                index -= comb(n, k)
            else:
                boolean_udslice[n] = True
                k -= 1
            n -= 1
        return boolean_udslice

    # -----------------------------------

    def solve(self, method):
        self.arrays_copy = []
        self.start_time = time.perf_counter()

        if method == "random":
            self.solve_random()
        elif method == "brute_force":
            thread = threading.Thread(target=self.start_brute_force())  # 探索は別スレッドで実行することでreturnされるように
            thread.start()
        elif method == "tpa":
            self.is_greedy = True # 貪欲法を使う
            thread = threading.Thread(target=self.tpa_start())
            thread.start()
        elif method == "tpa_set_limit": # 時間制限を指定できるTPA
            self.is_greedy = False
            time_limit = int(simpledialog.askstring("Set Time Limit", "時間制限を秒で入力してください(例: 60)"))
            self.start_time = time.perf_counter()
            self.tpa_start(time_limit)


    def solve_random(self):
        steps = []
        while True:
            while True:
                new = random.choice(["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"])
                if self.is_valid(steps, new):
                    break
            self.rotate(new, 1, False, [self.cp, self.co, self.ep, self.eo])
            steps.append(new)
            if self.is_complete([self.cp, self.co, self.ep, self.eo]):
                print(steps)
                elapsed_time = time.perf_counter() - self.start_time
                print(f"elapsed_time: {elapsed_time:.3f} seconds")
                print(f"{len(steps)} 手かかりました")
                self.draw()
                break

    def start_brute_force(self):
        for depth in range(1, 21):
            self.arrays_copy = copy.deepcopy([self.cp, self.co, self.ep, self.eo])
            if self.brute_force_search(depth, [], self.arrays_copy): # 揃ったら抜け出す
                break
            print(f"{depth} 手目探索終了")
            elapsed_time = time.perf_counter() - self.start_time
            print(f"elapsed_time: {elapsed_time:.3f} seconds")

    def brute_force_search(self, depth, steps, arrays):
        if self.is_complete(arrays):
            self.cp, self.co, self.ep, self.eo = arrays # 同期
            elapsed_time = time.perf_counter() - self.start_time
            print(*steps)  # アンパックして表示
            print(f"elapsed_time: {elapsed_time:.3f} seconds")
            print(f"{len(steps)} 手かかりました")
            display_steps = " ".join(steps)  # 手順を文字列に変換
            messagebox.showinfo("解法", f"{display_steps}\n合計{len(steps)} 手\n{elapsed_time:.3f} seconds")
            self.root.after(0, self.draw) # メインスレッドで描画を更新
            return True

        if depth == 0:
            return False

        for step in ["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]:
            if not self.is_valid(steps, step):  # 有効な手ではないなら次のループへ
                continue

            if not self.can_solve_brute_force(depth, arrays):  # あと１手で揃う配列ではなかったら次のループへ
                continue

            # print(steps, step) # どの手順を試しているか

            arrays_copy = copy.deepcopy(arrays)
            self.rotate(step, 1, False, arrays_copy)
            if self.brute_force_search(depth - 1, steps + [step], arrays_copy):
                return True
        return False

    def can_solve_brute_force(self, depth, arrays): # 未実装
        return True

    def can_solve_phase1(self, depth, co_index, eo_index, udslice_comb_index):
        # coとudslice_comb, eoとudslice_comb, eoとcoの組み合わせで枝刈り
        if max(CO_UDSLICECOMB_PRUNE_TABLE[co_index][udslice_comb_index], EO_UDSLICECOMB_PRUNE_TABLE[eo_index][udslice_comb_index], EO_CO_PRUNE_TABLE[eo_index][co_index]) > depth:
            return False
        return True

    def can_solve_phase2(self, depth, cp_index, ud_ep_index, udslice_ep_index):
        # cpとudslice, udとudsliceの組み合わせで枝刈り
        if max(PHASE2_CP_UDSLICE_PRUNE_TABLE[cp_index][udslice_ep_index], PHASE2_UD_UDSLICE_PRUNE_TABLE[ud_ep_index][udslice_ep_index]) > depth:
            return False
        return True

    def tpa_start(self, time_limit=1):
        self.max_steps = 24 # 最大許容手数、探索を続ける最大の手数
        self.arrays_copy = []
        self.solutions = [] # 解法を保存するリスト
        self.min_steps = 10000 # 最善手の手数

        if self.is_greedy: # 一番初めに見つけた解を出力する場合
            self.tpa_start_search1()
        else:
            @timeout_decorator.timeout(time_limit) # 時間制限
            def do():
                self.tpa_start_search1()
            try:
                do()
            except timeout_decorator.TimeoutError:
                print("制限時間に達しました。探索を終了します。")


        elapsed_time = time.perf_counter() - self.start_time

        min_solution = [] # 最善手
        for steps in self.solutions:
            if len(steps) == self.min_steps:
                min_solution = steps
                break

        print("----------------------------")
        print (*min_solution)
        print(f"合計探索時間: {elapsed_time:.3f} seconds")
        print(f"合計手数: {self.min_steps} 手")
        print("----------------------------")
        display_steps = " ".join(min_solution)  # 手順を文字列に変換
        messagebox.showinfo("解法", f"{display_steps}\n合計{self.min_steps} 手\n{elapsed_time:.3f} seconds")
        for step in min_solution:
            self.rotate(step, 1, False, [self.cp, self.co, self.ep, self.eo])
        self.root.after(0, self.draw)


    def tpa_start_search1(self):
        depth = 0
        while depth < self.max_steps and depth < self.min_steps: # 最大許容手数以内ならば探索を続ける
            self.arrays_copy = copy.deepcopy([self.cp, self.co, self.ep, self.eo])
            co_index = self.orientation_to_index(self.arrays_copy[1], False) # coをインデックスに変換
            eo_index = self.orientation_to_index(self.arrays_copy[3], True) # eoをインデックスに変換

            boolean_udslice = [False] * 12  # FR(8), FL(9), BL(10), BR(11) の位置にあるエッジがどこにいるか
            for j in range(12):
                if self.arrays_copy[2][j] >= 8:  # UDスライスであるFR, FL, BL, BR
                    boolean_udslice[j] = True # epのUDスライスのエッジの組み合わせをリストに変換
            udslice_comb_index = self.udslice_comb_to_index(boolean_udslice) # インデックスに変換

            if self.tpa_search1(depth, [], co_index, eo_index, udslice_comb_index):
                if self.is_greedy:
                    break
                else:
                    pass # 一つ解が見つかっても探し続ける
            depth += 1
            # print(f"{i} 手目探索終了", end=", ")
            # elapsed_time = time.perf_counter() - self.start_time
            # print(f"elapsed_time: {elapsed_time:.3f} seconds")

    def tpa_start_search2(self, phase1_steps, arrays):
        # print("phase2の探索を開始")
        self.start_time2 = time.perf_counter()
        cp_index = self.permutation_to_index(arrays[0])  # cpをインデックスに変換
        ud_ep_index = self.permutation_to_index(arrays[2][:8])
        udslice_ep_index = self.permutation_to_index(arrays[2][8:])  # UDスライスのエッジをインデックスに変換
        depth = 0
        while (depth < self.max_steps - len(phase1_steps)) and (depth < self.min_steps - len(phase1_steps)): # 最大許容手数以内ならば探索を続ける
            if self.tpa_search2(depth, phase1_steps, [], cp_index, ud_ep_index, udslice_ep_index):
                if self.is_greedy:  # 貪欲法を使う場合はここで探索を終了
                    return True
                break
            depth += 1
            # print(f"{i} 手目探索終了", end=", ")
            # elapsed_time = time.perf_counter() - self.start_time2
            # print(f"elapsed_time: {elapsed_time:.3f} seconds")

    def tpa_search1(self, depth, phase1_steps, co_index, eo_index, udslice_comb_index):
        if depth == 0 and eo_index == 0 and co_index == 0 and udslice_comb_index == 0: # phase1の終了条件
            if not phase1_steps or phase1_steps[-1] in ["R", "L", "F", "B", "R'", "L'", "F'", "B'"]: # これら以外ではeo,co,udslicecombは変化しないため冗長な手順が発生する
                self.arrays_copy = copy.deepcopy([self.cp, self.co, self.ep, self.eo])
                for step in phase1_steps:
                    self.rotate(step, 1, False, self.arrays_copy)
                if self.is_greedy: # 貪欲法を使う場合はここで探索を終了
                    if self.tpa_start_search2(phase1_steps, self.arrays_copy):
                        return True
                return self.tpa_start_search2(phase1_steps, self.arrays_copy)  # phase2の探索を開始

        if depth == 0:
            return False

        # 枝刈り
        if not self.can_solve_phase1(depth, co_index, eo_index, udslice_comb_index):
            return False  # 探索を終了

        for step in TPA_PHASE1_STEPS:
            if not self.is_valid(phase1_steps, step): # 有効な手ではないなら次のループへ
                continue

            # print(phase1_steps, step) # どの手順を試しているか

            next_co_index = CO_TRANSITION_TABLE[co_index][TPA_PHASE1_STEPS.index(step)]
            next_eo_index = EO_TRANSITION_TABLE[eo_index][TPA_PHASE1_STEPS.index(step)]
            next_udslice_comb_index = UDSLICECOMB_TRANSITION_TABLE[udslice_comb_index][TPA_PHASE1_STEPS.index(step)]
            # print(f"co_index: {co_index}, eo_index: {eo_index}, udslice_comb_index: {udslice_comb_index} -> next_co_index: {next_co_index}, next_eo_index: {next_eo_index}, next_udslice_comb_index: {next_udslice_comb_index}")
            if self.tpa_search1(depth - 1, phase1_steps + [step], next_co_index, next_eo_index, next_udslice_comb_index):
                return True
        return False

    def tpa_search2(self, depth, phase1_steps, phase2_steps, cp_index, ud_ep_index, udslice_ep_index):
        if depth == 0 and cp_index == 0 and ud_ep_index == 0 and udslice_ep_index == 0:
            print(f"{len(phase1_steps + phase2_steps)} steps (phase1:{len(phase1_steps)}, phase2:{len(phase2_steps)}), {phase1_steps + phase2_steps}, elapsed_time: {time.perf_counter() - self.start_time:.3f} sec")
            self.min_steps = min(self.min_steps, len(phase1_steps + phase2_steps)) # 最善手の手数を更新
            self.solutions.append(phase1_steps + phase2_steps)  # 解法を保存
            return True

        if depth == 0:
            return False

        # 枝刈り
        if not self.can_solve_phase2(depth, cp_index, ud_ep_index, udslice_ep_index):
            return False

        for step in TPA_PHASE2_STEPS:
            if not self.is_valid(phase2_steps, step): # 有効な手ではないなら次のループへ
                continue

            # print(phase1_steps, step) # どの手順を試しているか

            next_cp_index = PHASE2_CP_TRANSITION_TABLE[cp_index][TPA_PHASE2_STEPS.index(step)]
            next_ud_ep_index = PHASE2_UD_TRANSITION_TABLE[ud_ep_index][TPA_PHASE2_STEPS.index(step)]
            next_udslice_ep_index = PHASE2_UDSLICE_TRANSITION_TABLE[udslice_ep_index][TPA_PHASE2_STEPS.index(step)]
            # print(f"co_index: {co_index}, eo_index: {eo_index}, udslice_comb_index: {udslice_comb_index} -> next_co_index: {next_co_index}, next_eo_index: {next_eo_index}, next_udslice_comb_index: {next_udslice_comb_index}")
            if self.tpa_search2(depth - 1, phase1_steps, phase2_steps + [step], next_cp_index, next_ud_ep_index, next_udslice_ep_index):
                return True
        return False

    def test(self):
        self.cp = [0, 1, 2, 3, 4, 5, 6, 7] # コーナーの位置
        self.co = [0, 0, 0, 0, 0, 0, 0, 0] # コーナーの向き (0=正しい向き, 1=反時計回り, 2=時計回り)
        self.ep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] # エッジの位置
        self.eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # エッジの向き (0=正しい向き, 1=逆向き)
        co_index = self.orientation_to_index(self.co, False)
        for step in ["L"]:
            next_co_index = CO_TRANSITION_TABLE[co_index][TPA_PHASE1_STEPS.index(step)]
        for step in ["F"]:
            nn_co_index = CO_TRANSITION_TABLE[next_co_index][TPA_PHASE1_STEPS.index(step)]
        print(f"co_index: {co_index}, next_co_index: {next_co_index}, nn_co_index: {nn_co_index}")



sys.setrecursionlimit(2000) # 再帰の上限を増やす


INVERSE = {"U": "D", "D": "U", "L": "R", "R": "L", "F": "B", "B": "F"} # 逆面

FACE_COLORS = ["white", "#ff8c00", "lime", "red", "#0000ff", "yellow"]
FACE_NAMES = ["white", "orange", "green", "red", "blue", "yellow"]
# コーナーの各面
CORNER_FACES = [
    [0, 3, 2],  # URF
    [0, 2, 1],  # UFL
    [0, 1, 4],  # ULB
    [0, 4, 3],  # UBR
    [5, 2, 3],  # DFR
    [5, 1, 2],  # DLF
    [5, 4, 1],  # DBL
    [5, 3, 4],  # DRB
]

# コーナーの貼る位置（面, 行, 列）
CORNER_FACE_POSITIONS = [
    [(0, 2, 2), (3, 0, 0), (2, 0, 2)],  # URF
    [(0, 2, 0), (2, 0, 0), (1, 0, 2)],  # UFL
    [(0, 0, 0), (1, 0, 0), (4, 0, 2)],  # ULB
    [(0, 0, 2), (4, 0, 0), (3, 0, 2)],  # UBR
    [(5, 0, 2), (2, 2, 2), (3, 2, 0)],  # DFR
    [(5, 0, 0), (1, 2, 2), (2, 2, 0)],  # DLF
    [(5, 2, 0), (4, 2, 2), (1, 2, 0)],  # DBL
    [(5, 2, 2), (3, 2, 2), (4, 2, 0)],  # DRB
]

# エッジの各面
EDGE_FACES = [
    [0, 3], [0, 2], [0, 1], [0, 4],
    [5, 3], [5, 2], [5, 1], [5, 4],
    [2, 3], [2, 1], [4, 1], [4, 3]
]

# エッジの貼る位置（面, 行, 列）
EDGE_FACE_POSITIONS = [
    [(0, 1, 2), (3, 0, 1)],  # UR
    [(0, 2, 1), (2, 0, 1)],  # UF
    [(0, 1, 0), (1, 0, 1)],  # UL
    [(0, 0, 1), (4, 0, 1)],  # UB
    [(5, 1, 2), (3, 2, 1)],  # DR
    [(5, 0, 1), (2, 2, 1)],  # DF
    [(5, 1, 0), (1, 2, 1)],  # DL
    [(5, 2, 1), (4, 2, 1)],  # DB
    [(2, 1, 2), (3, 1, 0)],  # FR
    [(2, 1, 0), (1, 1, 2)],  # FL
    [(4, 1, 2), (1, 1, 0)],  # BL
    [(4, 1, 0), (3, 1, 2)]  # BR
]

# 遷移表の読み込み
with open("transition_table/co_transition_table.csv", mode='r') as f:
    CO_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open("transition_table/eo_transition_table.csv", mode='r') as f:
    EO_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open ("transition_table/udslicecomb_transition_table.csv") as f:
    UDSLICECOMB_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open("transition_table/phase2_cp_transition_table.csv", mode='r') as f:
    PHASE2_CP_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open("transition_table/phase2_ud_transition_table.csv", mode='r') as f:
    PHASE2_UD_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open("transition_table/phase2_udslice_transition_table.csv", mode='r') as f:
    PHASE2_UDSLICE_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]

# phase1枝刈り表の読み込み
with open("prune_table/co_udslicecomb_prune_table.csv", mode='r') as f:
    CO_UDSLICECOMB_PRUNE_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open("prune_table/eo_udslicecomb_prune_table.csv", mode='r') as f:
    EO_UDSLICECOMB_PRUNE_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open("prune_table/eo_co_prune_table.csv", mode='r') as f:
    EO_CO_PRUNE_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]

# phase2枝刈り表の読み込み 使える手数が少ないため、ファイル名にtpaを付けて区別している
with open("prune_table/phase2_cp_udslice_prune_table.csv", mode='r') as f:
    PHASE2_CP_UDSLICE_PRUNE_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open("prune_table/phase2_ud_udslice_prune_table.csv", mode='r') as f:
    PHASE2_UD_UDSLICE_PRUNE_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]

# TwoPhase Algorithmのphase1で使用する手
TPA_PHASE1_STEPS = ["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]
# TwoPhase Algorithmのphase2で使用する手
TPA_PHASE2_STEPS = ["U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2"]
