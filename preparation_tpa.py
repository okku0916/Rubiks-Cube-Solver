from math import factorial
from math import comb
import csv
import copy

class TpaPreparation:
    def __init__(self):
        self.cp = [0, 1, 2, 3, 4, 5, 6, 7]  # コーナーの位置
        self.co = [0, 0, 0, 0, 0, 0, 0, 0]  # コーナーの向き (0=正しい向き, 1=反時計回り, 2=時計回り)
        self.ep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # エッジの位置
        self.eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # エッジの向き (0=正しい向き, 1=逆向き)

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
                cp[:] = [cp[j] for j in rotate[0]] # 位置は置き換え
                co[:] = [(co[j] + rotate[1][k]) % 3 for k, j in enumerate(rotate[0])] # 向きは操作で捻れる
                ep[:] = [ep[j] for j in rotate[2]]
                eo[:] = [(eo[j] + rotate[3][k]) % 2 for k, j in enumerate(rotate[2])]

    # ---------- 状態のindex化-----------

    # cp,epのインデックス化
    # 辞書式で何番目かを求めることでインデックス化
    # 求めるより辞書式よりも前の個数を数え上げる
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
    # ---------- 遷移表の作成 -------------
    # cpの遷移表

    # epが処理完了できないので、normalのepは使用していない
    def create_cp_normal_transition_table(self):
        cp_transition_table = [[0 for _ in range(18)] for _ in range(factorial(8))] # 8!のコーナー位置について18種類の手の遷移表
        for i in range(factorial(8)): # 8!通りのコーナー位置のインデックス
            cp = self.index_to_permutation(i, 8) # コーナー位置をインデックスから取得
            for step_index, j in enumerate(["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]):
                # 各手を適用して新しい位置を取得
                self.rotate(j, 1, False, [cp, self.co, self.ep, self.eo])
                index = self.permutation_to_index(cp) # 新しい位置をインデックスに変換
                cp_transition_table[i][step_index] = index # 遷移表にインデックスを保存
                self.rotate(j, 3, False, [cp, self.co, self.ep, self.eo]) # 元に戻す
        with open('cp_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in cp_transition_table:
                writer.writerow(line)

    # two phase algorithmのphase2で使用するcpの遷移表を作成
    def create_cp_tpa_transition_table(self): # two phase algorithmのphase2では使える手数が少ないから別に定義
        cp_transition_table = [[0 for _ in range(18)] for _ in range(factorial(8))] # 8!のコーナー位置について18種類の手の遷移表
        for i in range(factorial(8)): # 8!通りのコーナー位置のインデックス
            cp = self.index_to_permutation(i, 8) # コーナー位置をインデックスから取得
            for step_index, j in enumerate(["U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2"]):
                # 各手を適用して新しい位置を取得
                self.rotate(j, 1, False, [cp, self.co, self.ep, self.eo])
                index = self.permutation_to_index(cp) # 新しい位置をインデックスに変換
                cp_transition_table[i][step_index] = index # 遷移表にインデックスを保存
                self.rotate(j, 3, False, [cp, self.co, self.ep, self.eo]) # 元に戻す
        with open('phase2_cp_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in cp_transition_table:
                writer.writerow(line)

    # coの遷移表 Two Phase Algorithmのphase1で使用する
    def create_co_transition_table(self):
        print("yes")
        co_transition_table = [[0 for _ in range(18)] for _ in range(3**7)] # 3^7のコーナー向きについて18種類の手の遷移表
        for i in range(3**7): # 3^7通りのコーナー向きのインデックス
            co = self.index_to_orientation(i, False) # コーナー向きをインデックスから取得
            for step_index, j in enumerate(["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]):
                # 各手を適用して新しい向きを取得
                self.rotate(j, 1, False, [self.cp, co, self.ep, self.eo]) # ここではco以外は何でも良い
                index = self.orientation_to_index(co, False)
                co_transition_table[i][step_index] = index # 遷移表にインデックスを保存
                print(f"i: {i}, j: {j}, index: {index}") # デバッグ用
                self.rotate(j, 3, False, [self.cp, co, self.ep, self.eo]) # 元に戻す
        with open('co_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in co_transition_table:
                writer.writerow(line)

    # eoの遷移表 Two Phase Algorithmのphase1で使用する
    def create_eo_transition_table(self):
        eo_transition_table = [[0 for _ in range(18)] for _ in range(2**11)]
        for i in range(2**11): # 2^11通りのエッジ向きのインデックス
            eo = self.index_to_orientation(i, True) # エッジ向きをインデックスから取得
            for step_index, j in enumerate(["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]):
                # 各手を適用して新しい向きを取得
                self.rotate(j, 1, False, [self.cp, self.co, self.ep, eo]) # ここではeo以外は何でも良い
                index = self.orientation_to_index(eo, True)
                eo_transition_table[i][step_index] = index # 遷移表にインデックスを保存
                self.rotate(j, 3, False, [self.cp, self.co, self.ep, eo]) # 元に戻す
        with open('eo_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in eo_transition_table:
                writer.writerow(line)

    # epの遷移表
    # 12!=479001600はメモリが足りず、処理が不可能だった
    def create_ep_normal_transition_table(self):
        ep_transition_table = [[0 for _ in range(18)] for _ in range(factorial(12))]
        for i in range(factorial(12)):
            ep = self.index_to_permutation(i, 12)
            for step_index, j in enumerate(["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]):
                self.rotate(j, 1, False, [self.cp, self.co, ep, self.eo])
                index = self.permutation_to_index(ep)
                ep_transition_table[i][step_index] = index
                self.rotate(j, 3, False, [self.cp, self.co, ep, self.eo])
        with open('ep_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in ep_transition_table:
                writer.writerow(line)

    # udslice_combの遷移表 Two Phase Algorithmのphase1で使用する
    def create_udslice_comb_transition_table(self):
        udslice_comb_transition_table = [[0 for _ in range(18)] for _ in range(comb(12, 4))]
        for i in range(comb(12, 4)):
            udslice_comb = self.index_to_udslice_comb(i)
            for step_index, j in enumerate(["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]):
                self.rotate(j, 1, False, [self.cp, self.co, udslice_comb, self.eo])
                index = self.udslice_comb_to_index(udslice_comb)
                udslice_comb_transition_table[i][step_index] = index
                self.rotate(j, 3, False, [self.cp, self.co, udslice_comb, self.eo])
        with open('udslicecomb_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in udslice_comb_transition_table:
                writer.writerow(line)


    def create_ud_ep_tpa_transition_table(self): # UD面のみのエッジ
        ep_transition_table = [[0 for _ in range(12)] for _ in range(factorial(8))] # UD面の8!のエッジ位置について12種類の手の遷移表
        for i in range(factorial(8)):
            ep = self.index_to_permutation(i, 8) + [0] * 4 # UDsliceは関係ないから0で埋める
            for step_index, j in enumerate(["U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2"]):
                self.rotate(j, 1, False, [self.cp, self.co, ep, self.eo])
                index = self.permutation_to_index(ep[:8]) # 先頭8つのみ確認
                ep_transition_table[i][step_index] = index
                self.rotate(j, 3, False, [self.cp, self.co, ep, self.eo])
        with open('phase2_ud_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in ep_transition_table:
                writer.writerow(line)

    def create_udslice_ep_tpa_transition_table(self): # UDスライスのエッジ
        ep_transition_table = [[0 for _ in range(12)] for _ in range(factorial(4))] # UDsliceの4!のエッジについて12手
        for i in range(factorial(4)):
            ep = [0] * 8 + self.index_to_permutation(i, 4) # UD面は関係ないから0で埋める
            for step_index, j in enumerate(["U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2"]):
                self.rotate(j, 1, False, [self.cp, self.co, ep, self.eo])
                index = self.permutation_to_index(ep[8:]) # 末尾4つのみ確認
                ep_transition_table[i][step_index] = index
                self.rotate(j, 3, False, [self.cp, self.co, ep, self.eo])
        with open('phase2_udslice_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in ep_transition_table:
                writer.writerow(line)
    # -----------------------------------

    # ---------- phase1 枝刈り表の作成 -----------
    # それぞれがどの手数で揃えられるかを記録する表を作成
    # 距離を１ずつ増やしながら、すべての状態を訪れるまでループする(BFS幅優先探索)
    # cpの枝刈り表
    def create_eo_prune_table(self):
        eo_prune_table = [-1 for _ in range(2**11)]
        eo_prune_table[0] = 0  # EOが正しい向きの状態は距離0
        distance = 0 # 現在の距離、1ずつ増やす
        filled = 1 # すでに訪れた状態の数
        while filled < len(eo_prune_table): # すべての状態を訪れるまで繰り返す
            print(f"Distance: {distance}, Filled: {filled}/{len(eo_prune_table)}")
            for i in range(2**11): # すべてのeo状態でループ
                if eo_prune_table[i] == distance: # distanceと一致するなら
                    for step_index, j in enumerate(TPA_PHASE1_STEPS): # 一手で進めるすべての手順でループし、未訪問の状態はdistance+1
                        next_eo = EO_TRANSITION_TABLE[i][step_index]
                        if eo_prune_table[next_eo] == -1:
                            eo_prune_table[next_eo] = distance + 1
                            filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{len(eo_prune_table)}")

        with open('eo_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(eo_prune_table)

    def create_co_prune_table(self):
        co_prune_table = [-1 for _ in range(3**7)]
        co_prune_table[0] = 0
        distance = 0
        filled = 1
        while filled < len(co_prune_table):
            print(f"Distance: {distance}, Filled: {filled}/{len(co_prune_table)}")
            for i in range(3**7):
                if co_prune_table[i] == distance:
                    for step_index, j in enumerate(TPA_PHASE1_STEPS):
                        next_co = CO_TRANSITION_TABLE[i][step_index]
                        if co_prune_table[next_co] == -1:
                            co_prune_table[next_co] = distance + 1
                            filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{len(co_prune_table)}")
        with open('co_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(co_prune_table)

    def create_udslicecomb_prune_table(self):
        udslice_comb_prune_table = [-1 for _ in range(comb(12, 4))]
        udslice_comb_prune_table[0] = 0
        distance = 0
        filled = 1
        while filled < len(udslice_comb_prune_table):
            print(f"Distance: {distance}, Filled: {filled}/{len(udslice_comb_prune_table)}")
            for i in range(comb(12, 4)):
                if udslice_comb_prune_table[i] == distance:
                    for step_index, j in enumerate(TPA_PHASE1_STEPS):
                        next_udslice_comb = UDSLICECOMB_TRANSITION_TABLE[i][step_index]
                        if udslice_comb_prune_table[next_udslice_comb] == -1:
                            udslice_comb_prune_table[next_udslice_comb] = distance + 1
                            filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{len(udslice_comb_prune_table)}")
        with open('prune_table/udslicecomb_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(udslice_comb_prune_table)

    # coとudslice_combの組み合わせの枝刈り表
    def create_co_udslicecomb_prune_table(self):
        co_and_udslice_comb_prune_table = [[-1 for _ in range(comb(12, 4))] for _ in range(3**7)]
        co_and_udslice_comb_prune_table[0][0] = 0
        distance = 0
        filled = 1
        while filled < comb(12, 4) * (3**7):
            print(f"Distance: {distance}, Filled: {filled}/{comb(12, 4) * (3**7)}")
            for i in range(3**7):
                for j in range(comb(12, 4)):
                    if co_and_udslice_comb_prune_table[i][j] == distance:
                        for step_index, k in enumerate(TPA_PHASE1_STEPS):
                            next_co = CO_TRANSITION_TABLE[i][step_index]
                            next_udslice_comb = UDSLICECOMB_TRANSITION_TABLE[j][step_index]
                            if co_and_udslice_comb_prune_table[next_co][next_udslice_comb] == -1:
                                co_and_udslice_comb_prune_table[next_co][next_udslice_comb] = distance + 1
                                filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{(2 ** 11) * (3 ** 7)}")
        with open('prune_table/co_udslicecomb_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in co_and_udslice_comb_prune_table:
                writer.writerow(line)

    # eoとudslice_combの組み合わせの枝刈り表
    def create_eo_udslicecomb_prune_table(self):
        eo_and_udslice_comb_prune_table = [[-1 for _ in range(comb(12, 4))] for _ in range(2**11)]
        eo_and_udslice_comb_prune_table[0][0] = 0
        distance = 0
        filled = 1
        while filled < comb(12, 4) * (2**11):
            print(f"Distance: {distance}, Filled: {filled}/{comb(12, 4) * (2**11)}")
            for i in range(2**11):
                for j in range(comb(12, 4)):
                    if eo_and_udslice_comb_prune_table[i][j] == distance:
                        for step_index, k in enumerate(TPA_PHASE1_STEPS):
                            next_eo = EO_TRANSITION_TABLE[i][step_index]
                            next_udslice_comb = UDSLICECOMB_TRANSITION_TABLE[j][step_index]
                            if eo_and_udslice_comb_prune_table[next_eo][next_udslice_comb] == -1:
                                eo_and_udslice_comb_prune_table[next_eo][next_udslice_comb] = distance + 1
                                filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{(2 ** 11) * (3 ** 7)}")
        with open('prune_table/eo_udslicecomb_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in eo_and_udslice_comb_prune_table:
                writer.writerow(line)

    # eoとcoの組み合わせの枝刈り表
    def create_eo_co_prune_table(self):
        eo_and_co_prune_table = [[-1 for _ in range(3**7)] for _ in range(2**11)]
        eo_and_co_prune_table[0][0] = 0
        distance = 0
        filled = 1
        while filled < (2**11) * (3**7):
            print(f"Distance: {distance}, Filled: {filled}/{(2**11) * (3**7)}")
            for i in range(2**11):
                for j in range(3**7):
                    if eo_and_co_prune_table[i][j] == distance:
                        for step_index, k in enumerate(TPA_PHASE1_STEPS):
                            next_eo = EO_TRANSITION_TABLE[i][step_index]
                            next_co = CO_TRANSITION_TABLE[j][step_index]
                            if eo_and_co_prune_table[next_eo][next_co] == -1:
                                eo_and_co_prune_table[next_eo][next_co] = distance + 1
                                filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{(2 ** 11) * (3 ** 7)}")
        with open('prune_table/eo_co_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in eo_and_co_prune_table:
                writer.writerow(line)

    # co,eo,udslice_combの組み合わせの枝刈り表
    # 作成時にメモリが足りなかった。仮にファイルができたとしても5GB近くなる。
    def create_co_eo_udslicecomb_prune_table(self):
        co_eo_and_udslice_comb_prune_table = [[[-1 for _ in range(comb(12, 4))] for _ in range(3**7)] for _ in range(2**11)]
        co_eo_and_udslice_comb_prune_table[0][0][0] = 0
        distance = 0
        filled = 1
        while filled < comb(12, 4) * (2**11) * (3**7):
            print(f"Distance: {distance}, Filled: {filled}/{comb(12, 4) * (2**11) * (3**7)}")
            for i in range(2**11):
                for j in range(3**7):
                    for k in range(comb(12, 4)):
                        if co_eo_and_udslice_comb_prune_table[i][j][k] == distance:
                            for step_index, l in enumerate(TPA_PHASE1_STEPS):
                                next_eo = EO_TRANSITION_TABLE[i][step_index]
                                next_co = CO_TRANSITION_TABLE[j][step_index]
                                next_udslice_comb = UDSLICECOMB_TRANSITION_TABLE[k][step_index]
                                if co_eo_and_udslice_comb_prune_table[next_eo][next_co][next_udslice_comb] == -1:
                                    co_eo_and_udslice_comb_prune_table[next_eo][next_co][next_udslice_comb] = distance + 1
                                    filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{(2 ** 11) * (3 ** 7)}")
        with open('prune_table/co_eo_udslicecomb_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in co_eo_and_udslice_comb_prune_table:
                writer.writerow(line)
    # ------------------------------------------

    # ---------- phase2 枝刈り表の作成 -----------
    def create_phase2_cp_prune_table(self):
        cp_tpa_prune_table = [-1 for _ in range(factorial(8))]
        cp_tpa_prune_table[0] = 0
        distance = 0
        filled = 1
        while filled < factorial(8):
            print(f"Distance: {distance}, Filled: {filled}/{len(cp_tpa_prune_table)}")
            for i in range(factorial(8)):
                if cp_tpa_prune_table[i] == distance:
                    for step_index, j in enumerate(TPA_PHASE2_STEPS):
                        next_cp = PHASE2_CP_TRANSITION_TABLE[i][step_index]
                        if cp_tpa_prune_table[next_cp] == -1:
                            cp_tpa_prune_table[next_cp] = distance + 1
                            filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{len(cp_tpa_prune_table)}")
        with open('prune_table/phase2_cp_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(cp_tpa_prune_table)

    def create_phase2_ud_prune_table(self):
        ud_ep_tpa_prune_table = [-1 for _ in range(factorial(8))]
        ud_ep_tpa_prune_table[0] = 0
        distance = 0
        filled = 1
        while filled < factorial(8):
            print(f"Distance: {distance}, Filled: {filled}/{len(ud_ep_tpa_prune_table)}")
            for i in range(factorial(8)):
                if ud_ep_tpa_prune_table[i] == distance:
                    for step_index, j in enumerate(TPA_PHASE2_STEPS):
                        next_ud_ep = PHASE2_UD_TRANSITION_TABLE[i][step_index]
                        if ud_ep_tpa_prune_table[next_ud_ep] == -1:
                            ud_ep_tpa_prune_table[next_ud_ep] = distance + 1
                            filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{len(ud_ep_tpa_prune_table)}")
        with open('prune_table/phase2_ud_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(ud_ep_tpa_prune_table)

    def create_phase2_udslice_prune_table(self):
        udslice_ep_tpa_prune_table = [-1 for _ in range(factorial(4))]
        udslice_ep_tpa_prune_table[0] = 0
        distance = 0
        filled = 1
        while filled < factorial(4):
            print(f"Distance: {distance}, Filled: {filled}/{len(udslice_ep_tpa_prune_table)}")
            for i in range(factorial(4)):
                if udslice_ep_tpa_prune_table[i] == distance:
                    for step_index, j in enumerate(TPA_PHASE2_STEPS):
                        next_udslice_ep = PHASE2_UDSLICE_TRANSITION_TABLE[i][step_index]
                        if udslice_ep_tpa_prune_table[next_udslice_ep] == -1:
                            udslice_ep_tpa_prune_table[next_udslice_ep] = distance + 1
                            filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{len(udslice_ep_tpa_prune_table)}")
        with open('prune_table/phase2_udslice_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(udslice_ep_tpa_prune_table)

    # cpとudの組み合わせの枝刈り表
    # 状態数16億。メモリが足りない。
    def create_phase2_cp_ud_prune_table(self):
        cp_and_ud_ep_tpa_prune_table = [[-1 for _ in range(factorial(8))] for _ in range(factorial(8))]
        cp_and_ud_ep_tpa_prune_table[0][0] = 0
        distance = 0
        filled = 1
        while filled < factorial(8) * factorial(8):
            print(f"Distance: {distance}, Filled: {filled}/{factorial(8) * factorial(8)}")
            for i in range(factorial(8)):
                for j in range(factorial(8)):
                    if cp_and_ud_ep_tpa_prune_table[i][j] == distance:
                        for step_index, k in enumerate(TPA_PHASE2_STEPS):
                            next_cp = PHASE2_CP_TRANSITION_TABLE[i][step_index]
                            next_ud_ep = PHASE2_UD_TRANSITION_TABLE[j][step_index]
                            if cp_and_ud_ep_tpa_prune_table[next_cp][next_ud_ep] == -1:
                                cp_and_ud_ep_tpa_prune_table[next_cp][next_ud_ep] = distance + 1
                                filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{factorial(8) * factorial(8)}")
        with open('prune_table/phase2_cp_ud_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in cp_and_ud_ep_tpa_prune_table:
                writer.writerow(line)

    def create_phase2_cp_udslice_prune_table(self):
        cp_and_udslice_ep_tpa_prune_table = [[-1 for _ in range(factorial(4))] for _ in range(factorial(8))]
        cp_and_udslice_ep_tpa_prune_table[0][0] = 0
        distance = 0
        filled = 1
        while filled < factorial(8) * factorial(4):
            print(f"Distance: {distance}, Filled: {filled}/{factorial(8) * factorial(4)}")
            for i in range(factorial(8)):
                for j in range(factorial(4)):
                    if cp_and_udslice_ep_tpa_prune_table[i][j] == distance:
                        for step_index, k in enumerate(TPA_PHASE2_STEPS):
                            next_cp = PHASE2_CP_TRANSITION_TABLE[i][step_index]
                            next_udslice_ep = PHASE2_UDSLICE_TRANSITION_TABLE[j][step_index]
                            if cp_and_udslice_ep_tpa_prune_table[next_cp][next_udslice_ep] == -1:
                                cp_and_udslice_ep_tpa_prune_table[next_cp][next_udslice_ep] = distance + 1
                                filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{factorial(8) * factorial(4)}")
        with open('prune_table/phase2_cp_udslice_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in cp_and_udslice_ep_tpa_prune_table:
                writer.writerow(line)

    def create_phase2_ud_udslice_prune_table(self):
        ud_and_udslice_ep_tpa_prune_table = [[-1 for _ in range(factorial(4))] for _ in range(factorial(8))]
        ud_and_udslice_ep_tpa_prune_table[0][0] = 0
        distance = 0
        filled = 1
        while filled < factorial(8) * factorial(4):
            print(f"Distance: {distance}, Filled: {filled}/{factorial(8) * factorial(4)}")
            for i in range(factorial(8)):
                for j in range(factorial(4)):
                    if ud_and_udslice_ep_tpa_prune_table[i][j] == distance:
                        for step_index, k in enumerate(TPA_PHASE2_STEPS):
                            next_ud_ep = PHASE2_UD_TRANSITION_TABLE[i][step_index]
                            next_udslice_ep = PHASE2_UDSLICE_TRANSITION_TABLE[j][step_index]
                            if ud_and_udslice_ep_tpa_prune_table[next_ud_ep][next_udslice_ep] == -1:
                                ud_and_udslice_ep_tpa_prune_table[next_ud_ep][next_udslice_ep] = distance + 1
                                filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{factorial(8) * factorial(4)}")
        with open('prune_table/phase2_ud_udslice_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in ud_and_udslice_ep_tpa_prune_table:
                writer.writerow(line)
    # ------------------------------------------

# 定数
TPA_PHASE1_STEPS = ["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]
TPA_PHASE2_STEPS = ["U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2"]
with open("transition_table/co_transition_table.csv", mode='r') as f:
    CO_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open("transition_table/eo_transition_table.csv", mode='r') as f:
    EO_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open("transition_table/udslicecomb_transition_table.csv") as f:
    UDSLICECOMB_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open("transition_table/phase2_cp_transition_table.csv", mode='r') as f:
    PHASE2_CP_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open("transition_table/phase2_ud_transition_table.csv", mode='r') as f:
    PHASE2_UD_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open("transition_table/phase2_udslice_transition_table.csv", mode='r') as f:
    PHASE2_UDSLICE_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]