import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# %matplotlib notebook
matplotlib.use("MacOSX") # pycharmで実行するための記述 TkAggでも可

def draw_cube(ax, position, colors):
    # 立方体の頂点座標を定義
    vertices = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
                     [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])
    vertices += position

    faces = [[vertices[j] for j in [0, 1, 2, 3]],  # D
         [vertices[j] for j in [4, 5, 6, 7]],  # U
         [vertices[j] for j in [0, 1, 5, 4]],  # F
         [vertices[j] for j in [2, 3, 7, 6]],  # B
         [vertices[j] for j in [0, 3, 7, 4]],  # L
         [vertices[j] for j in [1, 2, 6, 5]]]  # R

    poly3d = Poly3DCollection(faces, facecolors=colors, linewidths=1, edgecolors='black')
    ax.add_collection3d(poly3d)

def plot_3d(rubiks):
    B = "black"
    # ブロックを27個作成して組み合わせる。内部の面は黒色にする。
    face_colors = [[rubiks[5][0][0], B, rubiks[2][2][0], B, rubiks[1][2][2], B], # 0
                   [B, B, rubiks[2][1][0], B, rubiks[1][1][2], B], # 1
                   [B, rubiks[0][2][0], rubiks[2][0][0], B, rubiks[1][0][2], B], # 2
                   [rubiks[5][1][0], B, B, B, rubiks[1][2][1], B], # 3
                   [B, B, B, B, rubiks[1][1][1], B],# 4 L面センター
                   [B, rubiks[0][1][0], B, B, rubiks[1][0][1], B], # 5
                    [rubiks[5][2][0], B, B, rubiks[4][2][2], rubiks[1][2][0], B], # 6
                   [B, B, B, rubiks[4][1][2], rubiks[1][1][0], B], # 7
                   [B, rubiks[0][0][0], B, rubiks[4][0][2], rubiks[1][0][0], B], # 8
                   [rubiks[5][0][1], B, rubiks[2][2][1], B, B, B], # 9
                   [B, B, rubiks[2][1][1], B, B, B], # 10 F面センター
                   [B, rubiks[0][2][1], rubiks[2][0][1], B, B, B], # 11
                    [rubiks[5][1][1], B, B, B, B, B], # 12 D面センター
                    [B, B, B, B, B, B], # 中心
                    [B, rubiks[0][1][1], B, B, B, B], # 14 U面センター
                    [rubiks[5][2][1], B, B, rubiks[4][2][1], B, B], # 15
                   [B, B, B, rubiks[4][1][1], B, B], # 16 B面センター
                   [B, rubiks[0][0][1], B, rubiks[4][0][1], B, B], # 17
                    [rubiks[5][0][2], B, rubiks[2][2][2], B, B, rubiks[3][2][0]], # 18
                    [B, B, rubiks[2][1][2], B, B, rubiks[3][1][0]], # 19
                    [B, rubiks[0][2][2], rubiks[2][0][2], B, B, rubiks[3][0][0]], # 20
                    [rubiks[5][1][2], B, B, B, B, rubiks[3][2][1]], # 21
                    [B, B, B, B, B, rubiks[3][1][1]], # 22 R面センター
                    [B, rubiks[0][1][2], B, B, B, rubiks[3][0][1]], # 23
                    [rubiks[5][2][2], B, B, rubiks[4][2][0], B, rubiks[3][2][2]], # 24
                    [B, B, B, rubiks[4][1][0], B, rubiks[3][1][2]], # 25
                    [B, rubiks[0][0][2], B, rubiks[4][0][0], B, rubiks[3][0][2]] # 26
                    ]


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    positions = [(x, y, z) for x in range(3) for y in range(3) for z in range(3)]

    for i, pos in enumerate(positions):
        draw_cube(ax, pos, face_colors[i])

    ax.set_xlim(-1, 4)
    ax.set_ylim(-1, 4)
    ax.set_zlim(-1, 4)
    ax.axis("off")
    plt.show()
