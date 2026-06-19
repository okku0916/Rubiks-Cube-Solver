# 探索時間切れ時に投げる例外
class SearchTimeout(Exception):
    pass

# 探索キャンセル時に投げる例外
class SearchCancel(Exception):
    pass