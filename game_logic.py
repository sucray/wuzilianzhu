from constants import *

class Game:
    def __init__(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.black_pieces = 30
        self.white_pieces = 30
        self.dead_pieces = 0
        self.current_player = 1  # 1: 黑方, 2: 白方
        self.last_killed_pos = None

    def place_piece(self, row, col):
        if self.board[row][col] is not None:
            return False

        self.board[row][col] = self.current_player
        if self.current_player == 1:
            self.black_pieces -= 1
        else:
            self.white_pieces -= 1
        return True

    def check_five_in_a_row(self, row, col):
        directions = [
            [(0, 1), (0, -1)],  # 水平
            [(1, 0), (-1, 0)],  # 垂直
            [(1, 1), (-1, -1)],  # 左斜
            [(1, -1), (-1, 1)]   # 右斜
        ]
        for dir_pair in directions:
            count = 1
            for dr, dc in dir_pair:
                r, c = row + dr, col + dc
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == self.current_player:
                    count += 1
                    r += dr
                    c += dc
            if count >= 5:
                return True
        return False

    def handle_five_in_a_row(self, row, col):
        # 移除五子连珠的棋子
        directions = [
            [(0, 1), (0, -1)],  # 水平
            [(1, 0), (-1, 0)],  # 垂直
            [(1, 1), (-1, -1)],  # 左斜
            [(1, -1), (-1, 1)]   # 右斜
        ]
        removed_positions = []
        for dir_pair in directions:
            positions = [(row, col)]
            for dr, dc in dir_pair:
                r, c = row + dr, col + dc
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == self.current_player:
                    positions.append((r, c))
                    r += dr
                    c += dc
            if len(positions) >= 5:
                removed_positions = positions[:5]
                break

        for r, c in removed_positions:
            self.board[r][c] = None

        # 玩家棋子数加5
        if self.current_player == 1:
            self.black_pieces += 5
        else:
            self.white_pieces += 5

        return removed_positions

    def kill_piece(self, row, col):
        if self.board[row][col] is None or self.board[row][col] == self.current_player:
            return False

        self.board[row][col] = None
        self.dead_pieces += 1
        self.last_killed_pos = (row, col)
        return True

    def check_winner(self):
        if self.black_pieces == 0:
            return 2  # 白方胜
        elif self.white_pieces == 0:
            return 1  # 黑方胜
        return None