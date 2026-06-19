from pathlib import Path

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
BASE_DIR = Path(__file__).resolve().parent.parent # 基準ディレクトリ
TRANSITION_TABLE_DIR = BASE_DIR / "data" / "transition_table"
with open(TRANSITION_TABLE_DIR / "co_transition_table.csv", mode='r') as f:
    CO_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open(TRANSITION_TABLE_DIR / "eo_transition_table.csv", mode='r') as f:
    EO_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open (TRANSITION_TABLE_DIR / "udslicecomb_transition_table.csv") as f:
    UDSLICECOMB_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open(TRANSITION_TABLE_DIR / "phase2_cp_transition_table.csv", mode='r') as f:
    PHASE2_CP_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open(TRANSITION_TABLE_DIR / "phase2_ud_transition_table.csv", mode='r') as f:
    PHASE2_UD_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open(TRANSITION_TABLE_DIR / "phase2_udslice_transition_table.csv", mode='r') as f:
    PHASE2_UDSLICE_TRANSITION_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]

# phase1枝刈り表の読み込み
PRUNE_TABLE_DIR = BASE_DIR / "data" / "prune_table"
with open(PRUNE_TABLE_DIR / "co_udslicecomb_prune_table.csv", mode='r') as f:
    CO_UDSLICECOMB_PRUNE_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open(PRUNE_TABLE_DIR / "eo_udslicecomb_prune_table.csv", mode='r') as f:
    EO_UDSLICECOMB_PRUNE_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open(PRUNE_TABLE_DIR / "eo_co_prune_table.csv", mode='r') as f:
    EO_CO_PRUNE_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]

# phase2枝刈り表の読み込み 使える手数が少ないため、ファイル名にtpaを付けて区別している
with open(PRUNE_TABLE_DIR / "phase2_cp_udslice_prune_table.csv", mode='r') as f:
    PHASE2_CP_UDSLICE_PRUNE_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]
with open(PRUNE_TABLE_DIR / "phase2_ud_udslice_prune_table.csv", mode='r') as f:
    PHASE2_UD_UDSLICE_PRUNE_TABLE = [list(map(int, line.strip().split(','))) for line in f.readlines()]

# TwoPhase Algorithmのphase1で使用する手
TPA_PHASE1_STEPS = ["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]
# TwoPhase Algorithmのphase2で使用する手
TPA_PHASE2_STEPS = ["U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2"]