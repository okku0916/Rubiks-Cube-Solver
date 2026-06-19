import random
from cube.constants import INVERSE
# 3×3 コーナー、エッジの位置と向きだけで表現する版
class CubeState:
    def __init__(self):
        self.rubiks = [[[None for _ in range(3)] for _ in range(3)] for _ in range(6)] # 配列での表現
        self.cp = [0, 1, 2, 3, 4, 5, 6, 7] # コーナーの位置
        self.co = [0, 0, 0, 0, 0, 0, 0, 0] # コーナーの向き (0=正しい向き, 1=反時計回り, 2=時計回り)
        self.ep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] # エッジの位置
        self.eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # エッジの向き (0=正しい向き, 1=逆向き)

    def update_state(self, cp, co, ep, eo):
        self.cp, self.co, self.ep, self.eo = cp, co, ep, eo

    # 回転
    def rotate(self, how, num_rotate):
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
                self.cp = [self.cp[j] for j in rotate[0]] # 位置は置き換え
                self.co = [(self.co[j] + rotate[1][k]) % 3 for k, j in enumerate(rotate[0])] # 向きは操作で捻れる
                self.ep = [self.ep[j] for j in rotate[2]]
                self.eo = [(self.eo[j] + rotate[3][k]) % 2 for k, j in enumerate(rotate[2])]

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
                if is_valid_move(scramble, new):
                    self.rotate(new, 1)
                    scramble.append(new)
                    break
        scramble_label = ""
        for i in scramble:
            scramble_label += f"{i} "

        return scramble_label

    def is_complete(self):
        # for i in self.state.rubiks:
        #     for j in i:
        #         for k in j:
        #             if k != i[0][0]: # 面(i)のすべての色が同じでない場合
        #                 print("完成していません")
        #                 return False
        # print("完成しています")
        # return True

        if self.cp == [0, 1, 2, 3, 4, 5, 6, 7] and self.co == [0] * 8 and \
                self.ep == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] and self.eo == [0] * 12:
            # print("完成しています")
            return True
        else:
            # print("完成していません")
            return False

def is_valid_move(steps, step):
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