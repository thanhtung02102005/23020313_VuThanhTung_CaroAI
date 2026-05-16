# src/gui.py
import time
from tkinter import *
from tkinter import ttk
from src.config import BOARD_SIZE, PLAYER_HUMAN, PLAYER_AI
from src.engine import CaroEngine

class CaroGUI:
    def __init__(self, root):
        self.window = root
        self.window.title("CỜ CARO")
        self.engine = CaroEngine()
        self.last_ai_move = None 
        
        self.setup_ui()
        self.new_game()

    def setup_ui(self):
        self.header = Frame(self.window, bg="#e1e1e1", padx=10, pady=5)
        self.header.pack(side="top", fill="x")

        self.algo_var = StringVar(value="Alpha-Beta")
        Label(self.header, text="Thuật toán:", bg="#e1e1e1").pack(side="left")
        ttk.Combobox(self.header, textvariable=self.algo_var, values=["Minimax", "Alpha-Beta"], width=10).pack(side="left", padx=5)

        self.depth_var = IntVar(value=3)
        Label(self.header, text="Độ sâu:", bg="#e1e1e1").pack(side="left", padx=5)
        ttk.Spinbox(self.header, from_=1, to=4, textvariable=self.depth_var, width=5).pack(side="left")

        btn_style = {"font": ('Arial', 9, 'bold'), "relief": "raised", "borderwidth": 2}
        Button(self.header, text="Thoát", **btn_style, bg="#f8d7da", fg="red", command=self.window.destroy).pack(side="right", padx=5)
        Button(self.header, text="Ván mới", **btn_style, bg="#f0f0f0", command=self.new_game).pack(side="right", padx=5)
        Button(self.header, text="So sánh", **btn_style, bg="#d4edda", command=self.compare_algorithms).pack(side="right", padx=5)

        self.status_label = Label(self.window, text="Lượt của Người", font=('Arial', 12, 'bold'), pady=10)
        self.status_label.pack()

        self.board_frame = Frame(self.window, bg="#7f8c8d", padx=1, pady=1)
        self.board_frame.pack(padx=20, pady=10)
        
        self.btns = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                b = Button(self.board_frame, text="", font=('Arial', 14, 'bold'), width=3, height=1,
                           relief="ridge", bg="white", command=lambda row=r, col=c: self.player_turn(row, col))
                b.grid(row=r, column=c)
                self.btns[r][c] = b

        self.stats_text = Text(self.window, height=16, font=('Consolas', 10), bg="#f8f9fa")
        self.stats_text.pack(side="bottom", fill="x", padx=20, pady=10)
        self.stats_text.tag_configure("timeout", foreground="red")

    def log(self, msg, tag=None):
        if tag: self.stats_text.insert(END, msg + "\n", tag)
        else: self.stats_text.insert(END, msg + "\n")
        self.stats_text.see(END)

    def get_board_state(self):
        return [[self.btns[r][c]['text'] for c in range(BOARD_SIZE)] for r in range(BOARD_SIZE)]

    def player_turn(self, r, c):
        if self.btns[r][c]['text'] == "" and not self.engine.check_winner(self.get_board_state()):
            self.place_mark(r, c, PLAYER_HUMAN)
            winner_data = self.engine.check_winner(self.get_board_state())
            if not winner_data:
                self.status_label.config(text="Máy đang nghĩ...")
                self.window.update()
                self.ai_turn()
            else:
                self.handle_end(winner_data)

    def ai_turn(self):
        board = self.get_board_state()
        depth = self.depth_var.get()
        self.engine.nodes_visited = 0
        self.engine.start_time = time.time()
        self.engine.best_move_so_far = None
        self.engine._current_test_depth = depth
        is_timeout = False
        
        try:
            urgent_move = self.engine.find_urgent_move(board)
            if urgent_move:
                move, score = urgent_move, 999999
            else:
                if self.algo_var.get() == "Minimax":
                    score, move = self.engine.minimax(board, depth, True)
                else:
                    score, move = self.engine.alpha_beta(board, depth, -float('inf'), float('inf'), True)
        except Exception:
            is_timeout = True
            move = self.engine.best_move_so_far if self.engine.best_move_so_far else (4, 4)
            score = self.engine.best_score_so_far

        duration = time.time() - self.engine.start_time
        r, c = move
        self.highlight_move(r, c)
        self.place_mark(r, c, PLAYER_AI)
        self.last_ai_move = (r, c)
        self.log(f"- [AI] Hàng {r+1}, Cột {c+1} | Score: {score} | Nodes: {self.engine.nodes_visited} | Time: {duration:.2f}s", 
                 tag="timeout" if is_timeout else None)
        
        winner_data = self.engine.check_winner(self.get_board_state())
        if winner_data: self.handle_end(winner_data)
        else: self.status_label.config(text="Lượt của Người")

    def highlight_move(self, r, c):
        if self.last_ai_move:
            lr, lc = self.last_ai_move
            if self.btns[lr][lc].cget("bg") != "#2ecc71":
                self.btns[lr][lc].config(bg="white")
        self.btns[r][c].config(bg="#fff9c4")

    def place_mark(self, r, c, p):
        self.btns[r][c].config(text=p, fg="#d63031" if p == "X" else "#0984e3")

    def handle_end(self, winner_data):
        winner = "NGƯỜI" if winner_data[0] == "X" else "MÁY"
        self.status_label.config(text=f"KẾT THÚC: {winner} THẮNG!", fg="#2ecc71")
        for r, c in winner_data[1]: self.btns[r][c].config(bg="#2ecc71")

    def new_game(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE): self.btns[r][c].config(text="", bg="white")
        self.stats_text.delete('1.0', END)
        self.last_ai_move = None
        self.status_label.config(text="Lượt của Người", fg="black")

    def compare_algorithms(self):
        current_board = self.get_board_state()
        if self.last_ai_move:
            r, c = self.last_ai_move
            current_board[r][c] = ""
            
        self.stats_text.delete('1.0', END)
        self.log(f"{'D':<2} | {'Algorithm':<11} | {'Move (H,C)':<10} | {'Score':<10} | {'Nodes':<7} | {'Time'}")
        self.log("-" * 75)
        
        urgent = self.engine.find_urgent_move(current_board)

        for d in range(1, 5):
            self.engine._current_test_depth = d
            for algo in ["Minimax", "Alpha-Beta"]:
                self.engine.nodes_visited = 0
                self.engine.start_time = time.time()
                is_timeout = False
                
                try:
                    if urgent:
                        move, score = urgent, 999999
                    else:
                        if algo == "Minimax" and d > 3:
                            self.log(f"{d:<2} | {algo:<11} | {'SKIP':<10} | {'-':<10} | {'-':<7} | {'-'}")
                            continue
                        
                        if algo == "Minimax": 
                            score, move = self.engine.minimax(current_board, d, True)
                        else: 
                            score, move = self.engine.alpha_beta(current_board, d, -float('inf'), float('inf'), True)
                except Exception:
                    is_timeout = True
                    move = self.engine.best_move_so_far if self.engine.best_move_so_far else (4, 4)
                    score = "Err"

                dur = time.time() - self.start_time
                m_str = f"H{move[0]+1},C{move[1]+1}" if move else "N/A"
                tag = "timeout" if is_timeout else None
                self.log(f"{d:<2} | {algo:<11} | {m_str:<10} | {score:<10} | {self.engine.nodes_visited:<7} | {dur:.2f}s", tag=tag)
            self.log("-" * 75)
