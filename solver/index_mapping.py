import copy
from math import factorial, comb
# 状態のindex化

# cp,epのインデックス化
# 辞書式で何番目かを求めることでインデックス化
# 求める辞書式よりも前の個数を数え上げる
def permutation_to_index(perm):
    array = copy.deepcopy(perm)  # 元の配列を変更しないようにコピー
    index = 0
    while len(array) > 1:
        a = len([l for l in array if l < array[0]]) # 配列の先頭より小さい数の個数
        index += a * factorial(len(array) - 1)
        array = array[1:] # 計算済みを除外
    return index

# インデックスからcp,ep
# n個の辞書式での順列を求める
def index_to_permutation(index, n):
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
def orientation_to_index(ori, is_edge):
    index = 0
    for i in ori[:-1]: # 最後は他が決まれば一意に決まるから除外
        if is_edge: # エッジの向きは0,1の２種類なので2進数で表現
            index *= 2
        else: # コーナーの向きは0,1,2の３種類なので3進数で表現
            index *= 3
        index += i
    return index

# インデックスからco,eo
def index_to_orientation(index, is_edge):
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
def udslice_comb_to_index(boolean_udslice):
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
def index_to_udslice_comb(index):
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