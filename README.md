# Rubiks-Cube-Solver
Pythonで3×3ルービックキューブをGUIで操作、表示することができるプログラムです。カメラ画像からキューブの状態を認識し、Two-Phase Algorithmで解法を求めることができます。

# Requirements
- Numpy
- Matplotlib
- OpenCV
- timeout-decorator

# Usage
```bash
__init__.pyを実行することでプログラムを起動できます。
Recognizeボタンでキューブを認識できます。スペースボタンで一面ずつ認識します。
展開図通りの向きで認識しなければならないことに注意が必要です。
Matplotlibによる3D表示も可能です。

pycharm環境で開発していましたが、IDLEやVScode環境を試すとエラー（クラッシュ）が多発しました。
クラッシュが続く場合はpycharmを使用してみてください。
```
