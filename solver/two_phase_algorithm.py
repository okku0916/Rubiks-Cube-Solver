import time
import copy
from cube.state import CubeState, is_valid_move
from solver.exceptions import SearchCancel, SearchTimeout
import cube.constants as const
from solver.index_mapping import permutation_to_index, orientation_to_index, udslice_comb_to_index

def can_solve_phase1(depth, co_index, eo_index, udslice_comb_index):
    # coとudslice_comb, eoとudslice_comb, eoとcoの組み合わせで枝刈り
    if max(const.CO_UDSLICECOMB_PRUNE_TABLE[co_index][udslice_comb_index], const.EO_UDSLICECOMB_PRUNE_TABLE[eo_index][udslice_comb_index], const.EO_CO_PRUNE_TABLE[eo_index][co_index]) > depth:
        return False
    return True

def can_solve_phase2(depth, cp_index, ud_ep_index, udslice_ep_index):
    # cpとudslice, udとudsliceの組み合わせで枝刈り
    if max(const.PHASE2_CP_UDSLICE_PRUNE_TABLE[cp_index][udslice_ep_index], const.PHASE2_UD_UDSLICE_PRUNE_TABLE[ud_ep_index][udslice_ep_index]) > depth:
        return False
    return True

class TPASolver:
    def __init__(self, state, on_finish_callback, is_cancelled, is_greedy, time_limit=1):
        # 外部から受け取ったものを保持
        self.state = state
        self.on_finish_callback = on_finish_callback
        self.is_cancelled = is_cancelled
        self.is_greedy = is_greedy
        self.time_limit = time_limit
        
        self.max_steps = 24 # 探索する最大手数
        self.solutions = []
        self.min_steps = 10000 # 見つかった解法の最小手数
        self.start_time = 0
        self.state_copy = None # 探索用のコピー

    def start_tpa(self):
        self.start_time = time.perf_counter()
        if self.state.is_complete():
            self.on_finish_callback([], "success", time.perf_counter() - self.start_time)
            return
        try:
            self.tpa_start_search1()
        except SearchTimeout:
            print("制限時間に達しました。探索を終了します。")
            self.finish_with_best_solution()
            return
        except SearchCancel:
            self.on_finish_callback(None, "cancelled", time.perf_counter() - self.start_time)
            return

        if not self.solutions:
            self.on_finish_callback(None, "failed", time.perf_counter() - self.start_time) 
            return

        self.finish_with_best_solution()

    # 最善手を返す関数
    def finish_with_best_solution(self):
        if not self.solutions:
            self.on_finish_callback(None, "failed", time.perf_counter() - self.start_time)
            return
            
        min_solution = []
        for steps in self.solutions:
            if len(steps) == self.min_steps:
                min_solution = steps
                break
        self.on_finish_callback(min_solution, "success", time.perf_counter() - self.start_time)

    def tpa_start_search1(self):
        depth = 0
        while depth < self.max_steps and depth < self.min_steps: # 最大許容手数以内ならば探索を続ける
            self.state_copy = copy.deepcopy(self.state)
            co_index = orientation_to_index(self.state_copy.co, False) # coをインデックスに変換
            eo_index = orientation_to_index(self.state_copy.eo, True) # eoをインデックスに変換

            boolean_udslice = [False] * 12  # FR(8), FL(9), BL(10), BR(11) の位置にあるエッジがどこにいるか
            for j in range(12):
                if self.state_copy.ep[j] >= 8:  # UDスライスであるFR, FL, BL, BR
                    boolean_udslice[j] = True # epのUDスライスのエッジの組み合わせをリストに変換
            udslice_comb_index = udslice_comb_to_index(boolean_udslice) # インデックスに変換

            if self.tpa_search1(depth, [], co_index, eo_index, udslice_comb_index):
                if self.is_greedy:
                    break
                else:
                    pass # 一つ解が見つかっても探し続ける
            depth += 1
            # print(f"{i} 手目探索終了", end=", ")
            # elapsed_time = time.perf_counter() - self.start_time
            # print(f"elapsed_time: {elapsed_time:.3f} seconds")

    def tpa_start_search2(self, phase1_steps, state):
        # print("phase2の探索を開始")
        self.start_time2 = time.perf_counter()
        cp_index = permutation_to_index(state.cp)  # cpをインデックスに変換
        ud_ep_index = permutation_to_index(state.ep[:8])
        udslice_ep_index = permutation_to_index(state.ep[8:])  # UDスライスのエッジをインデックスに変換
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
        # 時間切れ例外を投げる
        if not self.is_greedy and time.perf_counter() - self.start_time >= self.time_limit:
            raise SearchTimeout()
        # キャンセル処理
        if self.is_cancelled():
            raise SearchCancel()
        
        if depth == 0 and eo_index == 0 and co_index == 0 and udslice_comb_index == 0: # phase1の終了条件
            if not phase1_steps or phase1_steps[-1] in ["R", "L", "F", "B", "R'", "L'", "F'", "B'"]: # これら以外ではeo,co,udslicecombは変化しないため冗長な手順が発生する
                self.state_copy = copy.deepcopy(self.state)
                for step in phase1_steps:
                    self.state_copy.rotate(step, 1)
                if self.is_greedy: # 貪欲法を使う場合はここで探索を終了
                    if self.tpa_start_search2(phase1_steps, self.state_copy):
                        return True
                return self.tpa_start_search2(phase1_steps, self.state_copy)  # phase2の探索を開始

        if depth == 0:
            return False

        # 枝刈り
        if not can_solve_phase1(depth, co_index, eo_index, udslice_comb_index):
            return False  # 探索を終了

        for step in const.TPA_PHASE1_STEPS:
            if not is_valid_move(phase1_steps, step): # 有効な手ではないなら次のループへ
                continue

            # print(phase1_steps, step) # どの手順を試しているか

            next_co_index = const.CO_TRANSITION_TABLE[co_index][const.TPA_PHASE1_STEPS.index(step)]
            next_eo_index = const.EO_TRANSITION_TABLE[eo_index][const.TPA_PHASE1_STEPS.index(step)]
            next_udslice_comb_index = const.UDSLICECOMB_TRANSITION_TABLE[udslice_comb_index][const.TPA_PHASE1_STEPS.index(step)]
            # print(f"co_index: {co_index}, eo_index: {eo_index}, udslice_comb_index: {udslice_comb_index} -> next_co_index: {next_co_index}, next_eo_index: {next_eo_index}, next_udslice_comb_index: {next_udslice_comb_index}")
            if self.tpa_search1(depth - 1, phase1_steps + [step], next_co_index, next_eo_index, next_udslice_comb_index):
                return True
        return False

    def tpa_search2(self, depth, phase1_steps, phase2_steps, cp_index, ud_ep_index, udslice_ep_index):
        # 時間切れ例外を投げる
        if not self.is_greedy and time.perf_counter() - self.start_time >= self.time_limit:
            raise SearchTimeout()
        # キャンセル処理
        if self.is_cancelled():
            raise SearchCancel()

        if depth == 0 and cp_index == 0 and ud_ep_index == 0 and udslice_ep_index == 0:
            # print(f"{len(phase1_steps + phase2_steps)} steps (phase1:{len(phase1_steps)}, phase2:{len(phase2_steps)}), {phase1_steps + phase2_steps}, elapsed_time: {time.perf_counter() - self.start_time:.3f} sec")
            self.min_steps = min(self.min_steps, len(phase1_steps + phase2_steps)) # 最善手の手数を更新
            self.solutions.append(phase1_steps + phase2_steps)  # 解法を保存
            return True

        if depth == 0:
            return False

        # 枝刈り
        if not can_solve_phase2(depth, cp_index, ud_ep_index, udslice_ep_index):
            return False

        for step in const.TPA_PHASE2_STEPS:
            if not is_valid_move(phase2_steps, step): # 有効な手ではないなら次のループへ
                continue

            # print(phase1_steps, step) # どの手順を試しているか

            next_cp_index = const.PHASE2_CP_TRANSITION_TABLE[cp_index][const.TPA_PHASE2_STEPS.index(step)]
            next_ud_ep_index = const.PHASE2_UD_TRANSITION_TABLE[ud_ep_index][const.TPA_PHASE2_STEPS.index(step)]
            next_udslice_ep_index = const.PHASE2_UDSLICE_TRANSITION_TABLE[udslice_ep_index][const.TPA_PHASE2_STEPS.index(step)]
            # print(f"co_index: {co_index}, eo_index: {eo_index}, udslice_comb_index: {udslice_comb_index} -> next_co_index: {next_co_index}, next_eo_index: {next_eo_index}, next_udslice_comb_index: {next_udslice_comb_index}")
            if self.tpa_search2(depth - 1, phase1_steps, phase2_steps + [step], next_cp_index, next_ud_ep_index, next_udslice_ep_index):
                return True
        return False