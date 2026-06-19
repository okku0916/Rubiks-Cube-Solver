import time
import copy
from cube.state import CubeState, is_valid_move
from solver.exceptions import SearchCancel

def start_brute_force(state, on_finish_callback, is_cancelled):
    start_time = time.perf_counter()
    state_copy = CubeState()
    if state.is_complete():
        on_finish_callback([], "success", time.perf_counter() - start_time)
        return
    try:
        for depth in range(1, 21):
            state_copy = copy.deepcopy(state)
            result_steps = brute_force_search(depth, [], state_copy, is_cancelled)
            if result_steps:
                elapsed_time = time.perf_counter() - start_time
                on_finish_callback(result_steps, "success", elapsed_time)
                return
            print(f"{depth} 手目探索終了")
    except SearchCancel:
        on_finish_callback(None, "cancelled", time.perf_counter() - start_time)

def brute_force_search(depth, steps, state, is_cancelled):
    if is_cancelled():
        raise SearchCancel()
    
    if state.is_complete():
        return steps

    if depth == 0:
        return False

    for step in ["U", "R", "L", "F", "B", "D", "U'", "R'", "L'", "F'", "B'", "D'", "U2", "R2", "L2", "F2", "B2", "D2"]:
        if not is_valid_move(steps, step):  # 有効な手ではないなら次のループへ
            continue

        # print(steps, step) # どの手順を試しているか

        state.rotate(step, 1)
        result_steps = brute_force_search(depth - 1, steps + [step], state, is_cancelled)

        if result_steps is not False:
            return result_steps
        
        state.rotate(step, 3) # 逆回転で元に戻す
    return False