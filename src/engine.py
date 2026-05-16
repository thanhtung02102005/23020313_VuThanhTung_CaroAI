# src/engine.py
import time
from src.config import BOARD_SIZE, WIN_CONDITION, PLAYER_HUMAN, PLAYER_AI, TIME_LIMIT

class CaroEngine:
    def __init__(self):
        self.nodes_visited = 0
        self.start_time = 0
        self.best_move_so_far = None
        self.best_score_so_far = 0
        self._current_test_depth = 0

    def check_winner(self, b):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if b[r][c] == "": continue
                p = b[r][c]
                for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                    path = []
                    for i in range(WIN_CONDITION):
                        nr, nc = r + dr*i, c + dc*i
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and b[nr][nc] == p:
                            path.append((nr, nc))
                        else: break
                    if len(path) == WIN_CONDITION: return (p, path)
        return None

    def find_urgent_move(self, board):
        moves = self.get_possible_moves(board)
        for r, c in moves:
            board[r][c] = PLAYER_AI
            if self.check_winner(board):
                board[r][c] = ""; return (r, c)
            board[r][c] = ""
        for r, c in moves:
            board[r][c] = PLAYER_HUMAN
            if self.check_winner(board):
                board[r][c] = ""; return (r, c)
            board[r][c] = ""
        return None

    def minimax(self, board, depth, is_max):
        if time.time() - self.start_time > TIME_LIMIT: raise Exception("Timeout")
        self.nodes_visited += 1
        res = self.check_winner(board)
        if res or depth == 0: return self.evaluate_board(board), None
        
        moves = self.get_possible_moves(board)
        best_move = None
        val = -float('inf') if is_max else float('inf')
        
        for r, c in moves:
            board[r][c] = PLAYER_AI if is_max else PLAYER_HUMAN
            score, _ = self.minimax(board, depth - 1, not is_max)
            board[r][c] = ""
            if is_max:
                if score > val: 
                    val, best_move = score, (r, c)
                    if depth == self._current_test_depth: 
                        self.best_move_so_far = (r, c)
            else:
                if score < val: val, best_move = score, (r, c)
        return val, best_move

    def alpha_beta(self, board, depth, alpha, beta, is_max):
        if time.time() - self.start_time > TIME_LIMIT: raise Exception("Timeout")
        self.nodes_visited += 1
        res = self.check_winner(board)
        if res or depth == 0: return self.evaluate_board(board), None
        
        moves = self.get_possible_moves(board)
        best_move = None
        val = -float('inf') if is_max else float('inf')
        
        for r, c in moves:
            board[r][c] = PLAYER_AI if is_max else PLAYER_HUMAN
            score, _ = self.alpha_beta(board, depth - 1, alpha, beta, not is_max)
            board[r][c] = ""
            if is_max:
                if score > val: 
                    val, best_move = score, (r, c)
                    if depth == self._current_test_depth: 
                        self.best_move_so_far = (r, c)
                alpha = max(alpha, val)
            else:
                if score < val: val, best_move = score, (r, c)
                beta = min(beta, val)
            if beta <= alpha: break
        return val, best_move

    def evaluate_board(self, board):
        score = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] != "":
                    p = board[r][c]
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        prev_r, prev_c = r - dr, c - dc
                        if 0 <= prev_r < BOARD_SIZE and 0 <= prev_c < BOARD_SIZE:
                            if board[prev_r][prev_c] == p: continue
                        score += self.get_score_dir(board, r, c, dr, dc)
        return score

    def get_score_dir(self, board, r, c, dr, dc):
        p = board[r][c]
        opponent = PLAYER_HUMAN if p == PLAYER_AI else PLAYER_AI
        count = 1
        block = 0
        prev_r, prev_c = r - dr, c - dc
        if not (0 <= prev_r < BOARD_SIZE and 0 <= prev_c < BOARD_SIZE) or board[prev_r][prev_c] == opponent:
            block += 1
        for i in range(1, WIN_CONDITION + 1):
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                if board[nr][nc] == p: count += 1
                elif board[nr][nc] == opponent: block += 1; break
                else: break
            else: block += 1; break

        is_ai = (p == PLAYER_AI)
        if count >= 4: return 1000000 if is_ai else -1000000
        if count == 3:
            if block == 0: return 50000 if is_ai else -180000
            if block == 1: return 5000 if is_ai else -10000
        if count == 2 and block == 0: return 500 if is_ai else -1500
        return 0

    def get_possible_moves(self, board):
        moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == "":
                    near = False
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] != "":
                                near = True; break
                        if near: break
                    if near: moves.append((r, c))
        if not moves: return [(4, 4)]
        return sorted(moves, key=lambda x: abs(x[0]-4) + abs(x[1]-4))
