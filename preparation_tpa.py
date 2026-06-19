# 事前計算用のプログラムであり、実行する必要はない。

from math import factorial
from math import comb
import csv
from solver.index_mapping import permutation_to_index, index_to_permutation, orientation_to_index, index_to_orientation, udslice_comb_to_index, index_to_udslice_comb
import cube.constants as const
from cube.state import CubeState

class TpaPreparation:
    def __init__(self):
        self.state = CubeState()

    # ---------- 遷移表の作成 -------------
    # cpの遷移表

    # epが処理完了できないので、normalのepは使用していない
    def create_cp_normal_transition_table(self):
        cp_transition_table = [[0 for _ in range(18)] for _ in range(factorial(8))] # 8!のコーナー位置について18種類の手の遷移表
        for i in range(factorial(8)): # 8!通りのコーナー位置のインデックス
            cp = index_to_permutation(i, 8) # コーナー位置をインデックスから取得
            for step_index, j in enumerate(["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]):
                # 各手を適用して新しい位置を取得
                self.state.rotate(j, 1)
                index = permutation_to_index(cp) # 新しい位置をインデックスに変換
                cp_transition_table[i][step_index] = index # 遷移表にインデックスを保存
                self.state.rotate(j, 3) # 元に戻す
        with open('cp_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in cp_transition_table:
                writer.writerow(line)

    # two phase algorithmのphase2で使用するcpの遷移表を作成
    def create_cp_tpa_transition_table(self): # two phase algorithmのphase2では使える手数が少ないから別に定義
        cp_transition_table = [[0 for _ in range(18)] for _ in range(factorial(8))] # 8!のコーナー位置について18種類の手の遷移表
        for i in range(factorial(8)): # 8!通りのコーナー位置のインデックス
            cp = index_to_permutation(i, 8) # コーナー位置をインデックスから取得
            for step_index, j in enumerate(["U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2"]):
                # 各手を適用して新しい位置を取得
                self.state.rotate(j, 1)
                index = permutation_to_index(cp) # 新しい位置をインデックスに変換
                cp_transition_table[i][step_index] = index # 遷移表にインデックスを保存
                self.state.rotate(j, 3) # 元に戻す
        with open('phase2_cp_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in cp_transition_table:
                writer.writerow(line)

    # coの遷移表 Two Phase Algorithmのphase1で使用する
    def create_co_transition_table(self):
        print("yes")
        co_transition_table = [[0 for _ in range(18)] for _ in range(3**7)] # 3^7のコーナー向きについて18種類の手の遷移表
        for i in range(3**7): # 3^7通りのコーナー向きのインデックス
            co = index_to_orientation(i, False) # コーナー向きをインデックスから取得
            for step_index, j in enumerate(["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]):
                # 各手を適用して新しい向きを取得
                self.state.rotate(j, 1) # ここではco以外は何でも良い
                index = orientation_to_index(co, False)
                co_transition_table[i][step_index] = index # 遷移表にインデックスを保存
                print(f"i: {i}, j: {j}, index: {index}") # デバッグ用
                self.state.rotate(j, 3) # 元に戻す
        with open('co_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in co_transition_table:
                writer.writerow(line)

    # eoの遷移表 Two Phase Algorithmのphase1で使用する
    def create_eo_transition_table(self):
        eo_transition_table = [[0 for _ in range(18)] for _ in range(2**11)]
        for i in range(2**11): # 2^11通りのエッジ向きのインデックス
            eo = index_to_orientation(i, True) # エッジ向きをインデックスから取得
            for step_index, j in enumerate(["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]):
                # 各手を適用して新しい向きを取得
                self.state.rotate(j, 1) # ここではeo以外は何でも良い
                index = orientation_to_index(eo, True)
                eo_transition_table[i][step_index] = index # 遷移表にインデックスを保存
                self.state.rotate(j, 3) # 元に戻す
        with open('eo_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in eo_transition_table:
                writer.writerow(line)

    # epの遷移表
    # 12!=479001600はメモリが足りず、処理が不可能だった
    def create_ep_normal_transition_table(self):
        ep_transition_table = [[0 for _ in range(18)] for _ in range(factorial(12))]
        for i in range(factorial(12)):
            ep = index_to_permutation(i, 12)
            for step_index, j in enumerate(["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]):
                self.state.rotate(j, 1)
                index = permutation_to_index(ep)
                ep_transition_table[i][step_index] = index
                self.state.rotate(j, 3)
        with open('ep_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in ep_transition_table:
                writer.writerow(line)

    # udslice_combの遷移表 Two Phase Algorithmのphase1で使用する
    def create_udslice_comb_transition_table(self):
        udslice_comb_transition_table = [[0 for _ in range(18)] for _ in range(comb(12, 4))]
        for i in range(comb(12, 4)):
            udslice_comb = index_to_udslice_comb(i)
            for step_index, j in enumerate(["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]):
                self.state.rotate(j, 1)
                index = udslice_comb_to_index(udslice_comb)
                udslice_comb_transition_table[i][step_index] = index
                self.state.rotate(j, 3)
        with open('udslicecomb_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in udslice_comb_transition_table:
                writer.writerow(line)

    def create_ud_ep_tpa_transition_table(self): # UD面のみのエッジ
        ep_transition_table = [[0 for _ in range(12)] for _ in range(factorial(8))] # UD面の8!のエッジ位置について12種類の手の遷移表
        for i in range(factorial(8)):
            ep = index_to_permutation(i, 8) + [0] * 4 # UDsliceは関係ないから0で埋める
            for step_index, j in enumerate(["U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2"]):
                self.state.rotate(j, 1)
                index = permutation_to_index(ep[:8]) # 先頭8つのみ確認
                ep_transition_table[i][step_index] = index
                self.state.rotate(j, 3)
        with open('phase2_ud_transition_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in ep_transition_table:
                writer.writerow(line)

    def create_udslice_ep_tpa_transition_table(self): # UDスライスのエッジ
        ep_transition_table = [[0 for _ in range(12)] for _ in range(factorial(4))] # UDsliceの4!のエッジについて12手
        for i in range(factorial(4)):
            ep = [0] * 8 + index_to_permutation(i, 4) # UD面は関係ないから0で埋める
            for step_index, j in enumerate(["U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2"]):
                self.state.rotate(j, 1)
                index = permutation_to_index(ep[8:]) # 末尾4つのみ確認
                ep_transition_table[i][step_index] = index
                self.state.rotate(j, 3)
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
                    for step_index, j in enumerate(const.TPA_PHASE1_STEPS): # 一手で進めるすべての手順でループし、未訪問の状態はdistance+1
                        next_eo = const.EO_TRANSITION_TABLE[i][step_index]
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
                    for step_index, j in enumerate(const.TPA_PHASE1_STEPS):
                        next_co = const.CO_TRANSITION_TABLE[i][step_index]
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
                    for step_index, j in enumerate(const.TPA_PHASE1_STEPS):
                        next_udslice_comb = const.UDSLICECOMB_TRANSITION_TABLE[i][step_index]
                        if udslice_comb_prune_table[next_udslice_comb] == -1:
                            udslice_comb_prune_table[next_udslice_comb] = distance + 1
                            filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{len(udslice_comb_prune_table)}")
        with open('udslicecomb_prune_table.csv', mode='w') as f:
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
                        for step_index, k in enumerate(const.TPA_PHASE1_STEPS):
                            next_co = const.CO_TRANSITION_TABLE[i][step_index]
                            next_udslice_comb = const.UDSLICECOMB_TRANSITION_TABLE[j][step_index]
                            if co_and_udslice_comb_prune_table[next_co][next_udslice_comb] == -1:
                                co_and_udslice_comb_prune_table[next_co][next_udslice_comb] = distance + 1
                                filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{(2 ** 11) * (3 ** 7)}")
        with open('co_udslicecomb_prune_table.csv', mode='w') as f:
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
                        for step_index, k in enumerate(const.TPA_PHASE1_STEPS):
                            next_eo = const.EO_TRANSITION_TABLE[i][step_index]
                            next_udslice_comb = const.UDSLICECOMB_TRANSITION_TABLE[j][step_index]
                            if eo_and_udslice_comb_prune_table[next_eo][next_udslice_comb] == -1:
                                eo_and_udslice_comb_prune_table[next_eo][next_udslice_comb] = distance + 1
                                filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{(2 ** 11) * (3 ** 7)}")
        with open('eo_udslicecomb_prune_table.csv', mode='w') as f:
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
                        for step_index, k in enumerate(const.TPA_PHASE1_STEPS):
                            next_eo = const.EO_TRANSITION_TABLE[i][step_index]
                            next_co = const.CO_TRANSITION_TABLE[j][step_index]
                            if eo_and_co_prune_table[next_eo][next_co] == -1:
                                eo_and_co_prune_table[next_eo][next_co] = distance + 1
                                filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{(2 ** 11) * (3 ** 7)}")
        with open('eo_co_prune_table.csv', mode='w') as f:
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
                            for step_index, l in enumerate(const.TPA_PHASE1_STEPS):
                                next_eo = const.EO_TRANSITION_TABLE[i][step_index]
                                next_co = const.CO_TRANSITION_TABLE[j][step_index]
                                next_udslice_comb = const.UDSLICECOMB_TRANSITION_TABLE[k][step_index]
                                if co_eo_and_udslice_comb_prune_table[next_eo][next_co][next_udslice_comb] == -1:
                                    co_eo_and_udslice_comb_prune_table[next_eo][next_co][next_udslice_comb] = distance + 1
                                    filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{(2 ** 11) * (3 ** 7)}")
        with open('co_eo_udslicecomb_prune_table.csv', mode='w') as f:
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
                    for step_index, j in enumerate(const.TPA_PHASE2_STEPS):
                        next_cp = const.PHASE2_CP_TRANSITION_TABLE[i][step_index]
                        if cp_tpa_prune_table[next_cp] == -1:
                            cp_tpa_prune_table[next_cp] = distance + 1
                            filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{len(cp_tpa_prune_table)}")
        with open('phase2_cp_prune_table.csv', mode='w') as f:
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
                    for step_index, j in enumerate(const.TPA_PHASE2_STEPS):
                        next_ud_ep = const.PHASE2_UD_TRANSITION_TABLE[i][step_index]
                        if ud_ep_tpa_prune_table[next_ud_ep] == -1:
                            ud_ep_tpa_prune_table[next_ud_ep] = distance + 1
                            filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{len(ud_ep_tpa_prune_table)}")
        with open('phase2_ud_prune_table.csv', mode='w') as f:
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
                    for step_index, j in enumerate(const.TPA_PHASE2_STEPS):
                        next_udslice_ep = const.PHASE2_UDSLICE_TRANSITION_TABLE[i][step_index]
                        if udslice_ep_tpa_prune_table[next_udslice_ep] == -1:
                            udslice_ep_tpa_prune_table[next_udslice_ep] = distance + 1
                            filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{len(udslice_ep_tpa_prune_table)}")
        with open('phase2_udslice_prune_table.csv', mode='w') as f:
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
                        for step_index, k in enumerate(const.TPA_PHASE2_STEPS):
                            next_cp = const.PHASE2_CP_TRANSITION_TABLE[i][step_index]
                            next_ud_ep = const.PHASE2_UD_TRANSITION_TABLE[j][step_index]
                            if cp_and_ud_ep_tpa_prune_table[next_cp][next_ud_ep] == -1:
                                cp_and_ud_ep_tpa_prune_table[next_cp][next_ud_ep] = distance + 1
                                filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{factorial(8) * factorial(8)}")
        with open('phase2_cp_ud_prune_table.csv', mode='w') as f:
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
                        for step_index, k in enumerate(const.TPA_PHASE2_STEPS):
                            next_cp = const.PHASE2_CP_TRANSITION_TABLE[i][step_index]
                            next_udslice_ep = const.PHASE2_UDSLICE_TRANSITION_TABLE[j][step_index]
                            if cp_and_udslice_ep_tpa_prune_table[next_cp][next_udslice_ep] == -1:
                                cp_and_udslice_ep_tpa_prune_table[next_cp][next_udslice_ep] = distance + 1
                                filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{factorial(8) * factorial(4)}")
        with open('phase2_cp_udslice_prune_table.csv', mode='w') as f:
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
                        for step_index, k in enumerate(const.TPA_PHASE2_STEPS):
                            next_ud_ep = const.PHASE2_UD_TRANSITION_TABLE[i][step_index]
                            next_udslice_ep = const.PHASE2_UDSLICE_TRANSITION_TABLE[j][step_index]
                            if ud_and_udslice_ep_tpa_prune_table[next_ud_ep][next_udslice_ep] == -1:
                                ud_and_udslice_ep_tpa_prune_table[next_ud_ep][next_udslice_ep] = distance + 1
                                filled += 1
            distance += 1
        print(f"Distance: {distance}, Filled: {filled}/{factorial(8) * factorial(4)}")
        with open('phase2_ud_udslice_prune_table.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in ud_and_udslice_ep_tpa_prune_table:
                writer.writerow(line)

# tp = TpaPreparation()
# tp.create_phase2_ud_udslice_prune_table()