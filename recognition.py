import cv2
import numpy as np

class CubeRecognition:
    def __init__(self):
        self.width = 640 # 画面サイズ 貸与pcでは(1280x720)or(640x480)に固定される
        self.height = 480
        self.rubiks = []  # 色のデータを保存するリスト
        self.face_count = 0
        self.is_unknown = False

    def hsv_to_color_name(self, val, frame, x, y):
        # print(f"HSV値: {val}") # HSV値を表示
        for j in FACE_NAMES: # 色
            is_color = True
            for k in range(3): # HSVの各成分
                if HIGH_COLOR[FACE_NAMES.index(j)][k] <= LOW_COLOR[FACE_NAMES.index(j)][k]: # 赤色のようにHの範囲が0付近をまたぐ場合
                    if not (LOW_COLOR[FACE_NAMES.index(j)][k] <= val[k] or val[k] <= HIGH_COLOR[FACE_NAMES.index(j)][k]):
                        is_color = False
                        break
                else:
                    if not (LOW_COLOR[FACE_NAMES.index(j)][k] <= val[k] <= HIGH_COLOR[FACE_NAMES.index(j)][k]):
                        is_color = False
                        # print("範囲外")
                        break
                # else:
                #     print("範囲内")
            if is_color:
                cv2.circle(frame, (x, y), 15, COLORS[j], thickness=3, lineType=cv2.LINE_8, shift=0) # 検出した色を円で表示
                # cv2.drawMarker(frame, (x, y), COLORS[j], cv2.MARKER_CROSS, 25, thickness=3)
                return j
        return "unknown" # 色が見つからない場合

    def recognize(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width) # 幅を640ピクセルに設定
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height) # 高さを480ピクセルに設定
        while True:
            #カメラからの画像取得
            ret, frame = cap.read()

            frame = cv2.flip(frame, 1)  # 水平反転

            # ルービックキューブ描画するための空間を作成
            draw_space = np.full((self.height, 500, 3), 200, dtype=np.uint8) # 200で埋めた配列(width=500)を作成

            #　ルービックキューブの枠を描画
            sp_x = 150  # U面の左上の座標 startpoint
            sp_y = 100
            side = 30  # １ブロックの一辺の長さ
            space = 10  # 描画する際の面同士の隙間
            cv2.rectangle(draw_space, (sp_x, sp_y), (sp_x + side * 3, sp_y + side * 3), (0, 0, 0))
            cv2.rectangle(draw_space, (sp_x - side * 3 - space, sp_y + side * 3 + space), (sp_x - space, sp_y + side * 6 + space), (0, 0, 0))
            cv2.rectangle(draw_space, (sp_x, sp_y + side * 3 + space), (sp_x + side * 3, sp_y + side * 6 + space), (0, 0, 0))
            cv2.rectangle(draw_space, (sp_x + side * 3 + space, sp_y + side * 3 + space), (sp_x + side * 6 + space, sp_y + side * 6 + space), (0, 0, 0))
            cv2.rectangle(draw_space, (sp_x + side * 6 + space * 2, sp_y + side * 3 + space), (sp_x + side * 9 + space * 2, sp_y + side * 6 + space), (0, 0, 0))
            cv2.rectangle(draw_space, (sp_x, sp_y + side * 6 + space * 2), (sp_x + side * 3, sp_y + side * 9 + space * 2), (0, 0, 0))

            # 読み取り済みの色を表示
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
                            cv2.rectangle(draw_space, (sp_x + side * (column - 1), sp_y + (side * 3 + space) // 2 * (face - 1) + side * (row - 1)),
                                          (sp_x + side * column, sp_y + (side * 3 + space) // 2 * (face - 1) + side * row), (0, 0, 0), thickness=3) # 枠を描画
                            cv2.rectangle(draw_space, (sp_x + side * (column - 1), sp_y + (side * 3 + space) // 2 * (face - 1) + side * (row - 1)),
                                          (sp_x + side * column, sp_y + (side * 3 + space) // 2 * (face - 1) + side * row), COLORS[color], thickness=-1) # 色を塗る
                        elif face == 6:
                            cv2.rectangle(draw_space, (sp_x + side * (column - 1), (sp_y + side * 6 + space * 2) + side * (row - 1)),
                                          (sp_x + side * column, (sp_y + side * 6 + space * 2) + side * row), (0, 0, 0), thickness=3)
                            cv2.rectangle(draw_space, (sp_x + side * (column - 1), (sp_y + side * 6 + space * 2) + side * (row - 1)),
                                          (sp_x + side * column, (sp_y + side * 6 + space * 2) + side * row), COLORS[color], thickness=-1)
                        elif face == 2 or face == 4:
                            cv2.rectangle(draw_space, ((sp_x - side * 3 - space) + (side * 6 + space * 2) // 2 * (face - 2) + side * (column - 1), (sp_y + side * 3 + space) + side * (row - 1)),
                                          ((sp_x - side * 3 - space) + (side * 6 + space * 2) // 2 * (face - 2) + side * column, (sp_y + side * 3 + space) + side * row), (0, 0, 0) , thickness=3)
                            cv2.rectangle(draw_space, ((sp_x - side * 3 - space) + (side * 6 + space * 2) // 2 * (face - 2) + side * (column - 1), (sp_y + side * 3 + space) + side * (row - 1)),
                                          ((sp_x - side * 3 - space) + (side * 6 + space * 2) // 2 * (face - 2) + side * column, (sp_y + side * 3 + space) + side * row), COLORS[color] , thickness=-1)
                        elif face == 5:
                            cv2.rectangle(draw_space, ((sp_x + side * 6 + space * 2) + side * (column - 1), (sp_y + side * 3 + space) + side * (row - 1)),
                                          ((sp_x + side * 6 + space * 2) + side * column, (sp_y + side * 3 + space) + side * row), (0, 0, 0), thickness=3)
                            cv2.rectangle(draw_space, ((sp_x + side * 6 + space * 2) + side * (column - 1), (sp_y + side * 3 + space) + side * (row - 1)),
                                          ((sp_x + side * 6 + space * 2) + side * column, (sp_y + side * 3 + space) + side * row), COLORS[color], thickness=-1)


            # 正方形を描画
            w, h = 300, 300 # 正方形の幅と高さ
            x, y = (self.width - w) // 2, (self.height - h) // 2 # 画面の中央に配置、正方形の左上
            for i in range(3):
                for j in range(3):
                    # 各正方形の座標を計算
                    square_x = x + i * (w // 3)
                    square_y = y + j * (h // 3)
                    cv2.rectangle(frame, (square_x, square_y), (square_x + w // 3, square_y + h // 3), (36, 255, 12), thickness=2, lineType=cv2.LINE_AA)


            # 色の検出
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # opencvではBGRで取得する
            colors = [[], [], []]
            for i in range(3):
                for j in range(3):
                    # xは反転するから逆から確認する
                    circle_x = x + (2 - i) * (w // 3) + (w // 6)
                    circle_y = y + j * (h // 3) + (h // 6)
                    # cv2.circle(frame, (circle_x, circle_y), 10, (0, 0, 0), thickness=2, lineType=cv2.LINE_AA, shift=0)
                    # cv2.drawMarker(frame, (circle_x, circle_y), (0, 0, 0), cv2.MARKER_CROSS, 25, thickness=3)
                    val = hsv[circle_y, circle_x] # 画面の中央の座標からHSV値を取得
                    label = self.hsv_to_color_name(val, frame, circle_x, circle_y)
                    colors[j].append(label)

            # 検出中の面を描画
            row = 0
            face = self.face_count + 1
            for j in colors:  # j:行を取り出す
                row += 1
                column = 0
                for color in j:  # k:色を取り出す
                    column += 1
                    if face == 1 or face == 3:
                        cv2.rectangle(draw_space, (sp_x + side * (column - 1), sp_y + (side * 3 + space) // 2 * (face - 1) + side * (row - 1)),
                                      (sp_x + side * column, sp_y + (side * 3 + space) // 2 * (face - 1) + side * row), COLORS[color], thickness=-1)
                        cv2.rectangle(draw_space, (sp_x + side * (column - 1), sp_y + (side * 3 + space) // 2 * (face - 1) + side * (row - 1)),
                                      (sp_x + side * column, sp_y + (side * 3 + space) // 2 * (face - 1) + side * row), (255, 0, 255), thickness=2)  # 枠を描画
                    if face == 6:
                        cv2.rectangle(draw_space, (sp_x + side * (column - 1), (sp_y + side * 6 + space * 2) + side * (row - 1)),
                                      (sp_x + side * column, (sp_y + side * 6 + space * 2) + side * row), COLORS[color], thickness=-1)
                        cv2.rectangle(draw_space, (sp_x + side * (column - 1), (sp_y + side * 6 + space * 2) + side * (row - 1)),
                                      (sp_x + side * column, (sp_y + side * 6 + space * 2) + side * row), (255, 0, 255), thickness=2)
                    if face == 2 or face == 4:
                        cv2.rectangle(draw_space, ((sp_x - side * 3 - space) + (side * 6 + space * 2) // 2 * (face - 2) + side * (column - 1), (sp_y + side * 3 + space) + side * (row - 1)),
                                      ((sp_x - side * 3 - space) + (side * 6 + space * 2) // 2 * (face - 2) + side * column, (sp_y + side * 3 + space) + side * row), COLORS[color], thickness=-1)
                        cv2.rectangle(draw_space, ((sp_x - side * 3 - space) + (side * 6 + space * 2) // 2 * (face - 2) + side * (column - 1), (sp_y + side * 3 + space) + side * (row - 1)),
                                      ((sp_x - side * 3 - space) + (side * 6 + space * 2) // 2 * (face - 2) + side * column, (sp_y + side * 3 + space) + side * row), (255, 0, 255), thickness=2)
                    if face == 5:
                        cv2.rectangle(draw_space, ((sp_x + side * 6 + space * 2) + side * (column - 1), (sp_y + side * 3 + space) + side * (row - 1)),
                                      ((sp_x + side * 6 + space * 2) + side * column, (sp_y + side * 3 + space) + side * row), COLORS[color], thickness=-1)
                        cv2.rectangle(draw_space, ((sp_x + side * 6 + space * 2) + side * (column - 1), (sp_y + side * 3 + space) + side * (row - 1)),
                                      ((sp_x + side * 6 + space * 2) + side * column, (sp_y + side * 3 + space) + side * row), (255, 0, 255), thickness=2)

            cv2.putText(frame, f"Press [SPACE] - {FACE_NAMES[self.face_count]} center face", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if self.is_unknown:
                cv2.putText(frame, "Please scan again", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            #カメラの画像の出力
            combined = np.hstack((frame, draw_space)) # 空間をカメラと結合
            cv2.imshow("camera" , combined)

            key = cv2.waitKey(1)
            if key == 32:  # スペースキーで保存
                if len(colors) == 3 and all(len(row) == 3 for row in colors):
                    self.is_unknown = False
                    for i in colors:
                        for j in i:
                            if j == "unknown":
                                self.is_unknown = True
                    if self.is_unknown:
                        print("認識されていない色があります。再度スキャンしてください。")
                    else:
                        self.rubiks.append(colors)
                        self.face_count += 1
                        print(f"face {self.face_count}: {colors}")
                        if self.face_count == 6:
                            print("認識完了")
                            # print("認識した色のデータ:", self.rubiks)

                            # メモリを解放して終了する
                            cap.release()
                            cv2.destroyAllWindows()
                            return self.rubiks
            if key == 27: # ESCキーが押されたら終了
                # メモリを解放して終了する
                cap.release()
                cv2.destroyAllWindows()
                return None


# 定数
LOW_COLOR = [[0, 0, 80], [4, 100, 120], [45, 100, 60], [173, 100, 90], [95, 100, 60], [25, 100, 70]]  # 各色のhsvの最小値を設定
HIGH_COLOR = [[179, 80, 255], [22, 255, 255], [80, 255, 255], [2, 255, 255], [130, 255, 255], [37, 255, 255]]  # 各色のhsvの最大値を設定
# 赤色はH=0付近も検知しなければならない
COLORS = {"white": (255, 255, 255), "orange": (0, 140, 255), "green": (0, 255, 0), "red": (0, 0, 255),
          "blue": (255, 0, 0), "yellow": (0, 255, 255), "unknown": (128, 128, 128)}  # 色の名前とBGR値
FACE_NAMES = ["white", "orange", "green", "red", "blue", "yellow"]
