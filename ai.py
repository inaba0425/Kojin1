import random

BLACK = 1
WHITE = 2
CORNERS = [(0, 0), (0, 5), (5, 0), (5, 5)]  # 6x6ボード用の四隅（8x8なら変更）

def can_place_x_y(board, stone, x, y):
    """
    石を置けるかどうかを調べる関数。
    """
    if board[y][x] != 0:
        return False  # 既に石がある場合は置けない
    opponent = 3 - stone  # 相手の石 (1なら2、2なら1)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True
        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True  # 石を置ける条件を満たす
    return False

def valid_moves(board, stone):
    """
    石を置けるすべての座標をリストで返す。
    """
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                moves.append((x, y))
    return moves

def score_move(board, x, y, stone):
    """
    特定の手を評価する関数（ひっくり返す石の数だけでなく、エッジや安定性を考慮）。
    """
    score = 0
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        flipped = 0
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            flipped += 1
        if flipped > 0 and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            score += flipped
    return score

def evaluate_board(board, stone):
    """
    ボード全体を評価する関数。
    評価要素：
        - 自分の石の数、相手の石の数
        - コーナー、エッジ、安定した石の数
    """
    opponent = 3 - stone
    score = 0

    # コーナーの評価
    for corner in CORNERS:
        x, y = corner
        if board[y][x] == stone:
            score += 10  # コーナーは非常に強い
        elif board[y][x] == opponent:
            score -= 10

    # エッジの評価（コーナーの隣の石も重要）
    edges = [
        (0, 1), (0, 4), (1, 0), (1, 5),
        (4, 0), (4, 5), (5, 1), (5, 4)
    ]
    for x, y in edges:
        if board[y][x] == stone:
            score += 5
        elif board[y][x] == opponent:
            score -= 5

    # 石の安定性（盤面端や中央の石は安定しやすい）
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                score += 1  # 自分の石が多いと有利
            elif board[y][x] == opponent:
                score -= 1  # 相手の石が多いと不利

    return score

def minimax(board, depth, maximizing_player, stone, alpha, beta):
    if depth == 0 or not valid_moves(board, stone):
        return evaluate_board(board, stone)

    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves(board, stone):
            x, y = move
            new_board = [row[:] for row in board]
            new_board[y][x] = stone
            eval = minimax(new_board, depth - 1, False, 3 - stone, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in valid_moves(board, stone):
            x, y = move
            new_board = [row[:] for row in board]
            new_board[y][x] = stone
            eval = minimax(new_board, depth - 1, True, 3 - stone, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def opponent(stone):
    return 3 - stone

def choose_opening_move(board, stone):
    """
    コーナーに石を置ける場合は、その手を選ぶ。
    """
    for corner in CORNERS:
        x, y = corner
        if board[y][x] == 0:
            return (x, y)
    return None  # コーナーに置ける手がない場合は None を返す

class Kojin3AI:
    def face(self):
        return "💛"  # 強いAIを示すアイコン

    def place(self, board, stone):
        best_move = None
        best_value = float('-inf')

        # コーナーに置ける場合はそれを最優先で選ぶ
        opening_move = choose_opening_move(board, stone)
        if opening_move:
            return opening_move

        # ネガマックスを使って最適な手を決定
        for move in valid_moves(board, stone):
            new_board = [row[:] for row in board]
            x, y = move
            new_board[y][x] = stone
            move_value = minimax(new_board, 3, False, stone, float('-inf'), float('inf'))  # 深さ3で探索
            if move_value > best_value:
                best_value = move_value
                best_move = move

        return best_move
