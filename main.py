'''
五子连诛(v0.01)
制作者：陈邦羽
主程序
'''

import pygame
import sys
from game_logic import Game
from constants import *

# 初始化pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("五子连诛")
font = pygame.font.SysFont('SimHei', FONT_SIZE)
large_font = pygame.font.SysFont('SimHei', 48)  # 用于显示获胜信息

# 加载背景图片
try:
    bg_image = pygame.image.load("bg.png")
    bg_image = pygame.transform.scale(bg_image, (BOARD_SIZE * GRID_SIZE + 2 * MARGIN, BOARD_SIZE * GRID_SIZE + 2 * MARGIN))
except:
    bg_image = None

# 游戏规则文本
RULES_TEXT = [
    "五子连诛游戏规则:",
    "1. 15x15棋盘，每人30颗棋子",
    "2. 剩余棋子用完一方输",
    "3. 形成五子连珠后:",
    "   - 收回这五颗子",
    "   - 杀掉对方棋盘上一子放入死子盒",
    "   - 被杀方下一手不能落被杀位",
    "4. 连珠后己方棋子+5，对方棋子-1"
]

def draw_board(game):
    # 绘制背景
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(BG_COLOR)

    # 绘制棋盘网格
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR,
                         (MARGIN, MARGIN + i * GRID_SIZE),
                         (MARGIN + (BOARD_SIZE - 1) * GRID_SIZE, MARGIN + i * GRID_SIZE))
        pygame.draw.line(screen, LINE_COLOR,
                         (MARGIN + i * GRID_SIZE, MARGIN),
                         (MARGIN + i * GRID_SIZE, MARGIN + (BOARD_SIZE - 1) * GRID_SIZE))

    # 绘制棋子
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if game.board[row][col] == 1:
                pygame.draw.circle(screen, BLACK,
                                  (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE),
                                  GRID_SIZE // 2 - 2)
            elif game.board[row][col] == 2:
                pygame.draw.circle(screen, WHITE,
                                  (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE),
                                  GRID_SIZE // 2 - 2)

    # 绘制信息栏
    info_x = BOARD_SIZE * GRID_SIZE + 2 * MARGIN + 10
    black_text = font.render(f"黑方剩余: {game.black_pieces}", True, BLACK)
    white_text = font.render(f"白方剩余: {game.white_pieces}", True, BLACK)
    dead_text = font.render(f"死子数: {game.dead_pieces}", True, BLACK)
    player_text = font.render(f"当前: {'黑方' if game.current_player == 1 else '白方'}", True, BLACK)

    screen.blit(black_text, (info_x, 50))
    screen.blit(white_text, (info_x, 100))
    screen.blit(dead_text, (info_x, 150))
    screen.blit(player_text, (info_x, 200))

    # 绘制规则按钮
    pygame.draw.rect(screen, (100, 100, 255), (info_x, 250, 150, 40))
    rules_text = font.render("游戏规则", True, WHITE)
    screen.blit(rules_text, (info_x + 75 - rules_text.get_width() // 2, 260))

def show_winner(winner):
    text = large_font.render(f"{'黑方' if winner == 1 else '白方'}获胜!", True, RED)
    restart_text = font.render("按空格键重新开始", True, BLACK)

    # 创建半透明背景
    s = pygame.Surface((400, 150), pygame.SRCALPHA)
    s.fill((255, 255, 255, 128))
    screen.blit(s, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 75))

    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
    screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 20))

def show_rules():
    # 创建规则窗口
    rule_window = pygame.Surface((500, 400))
    rule_window.fill((240, 240, 240))

    # 绘制标题
    title_font = pygame.font.SysFont('SimHei', 32)
    title = title_font.render("五子连诛游戏规则", True, (0, 0, 0))
    rule_window.blit(title, (250 - title.get_width() // 2, 20))

    # 绘制规则文本
    rule_font = pygame.font.SysFont('SimHei', 20)
    for i, line in enumerate(RULES_TEXT):
        text = rule_font.render(line, True, (0, 0, 0))
        rule_window.blit(text, (30, 70 + i * 30))

    # 绘制关闭按钮
    pygame.draw.rect(rule_window, (255, 100, 100), (200, 350, 100, 40))
    close_text = rule_font.render("关闭", True, (255, 255, 255))
    rule_window.blit(close_text, (250 - close_text.get_width() // 2, 360))

    # 显示规则窗口
    screen.blit(rule_window, (WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 - 200))
    pygame.display.flip()

    # 等待关闭
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (WINDOW_WIDTH // 2 - 50 <= x <= WINDOW_WIDTH // 2 + 50 and
                    WINDOW_HEIGHT // 2 + 150 <= y <= WINDOW_HEIGHT // 2 + 190):
                    waiting = False

def main():
    game = Game()
    state = "place"  # place: 落子, kill: 杀子
    winner = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if winner and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # 重新开始游戏
                game = Game()
                state = "place"
                winner = None
                continue

            if not winner and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # 检查是否点击了规则按钮
                info_x = BOARD_SIZE * GRID_SIZE + 2 * MARGIN + 10
                if info_x <= x <= info_x + 150 and 250 <= y <= 290:
                    show_rules()
                    continue

                if MARGIN <= x < MARGIN + BOARD_SIZE * GRID_SIZE and MARGIN <= y < MARGIN + BOARD_SIZE * GRID_SIZE:
                    col = round((x - MARGIN) / GRID_SIZE)
                    row = round((y - MARGIN) / GRID_SIZE)
                    col = max(0, min(col, BOARD_SIZE - 1))
                    row = max(0, min(row, BOARD_SIZE - 1))

                    if state == "place":
                        # 检查是否是刚被杀的禁止位置
                        if game.last_killed_pos and game.last_killed_pos == (row, col):
                            continue

                        if game.place_piece(row, col):
                            if game.check_five_in_a_row(row, col):
                                removed = game.handle_five_in_a_row(row, col)
                                state = "kill"
                            else:
                                game.current_player = 3 - game.current_player
                                game.last_killed_pos = None

                            winner = game.check_winner()

                    elif state == "kill":
                        if game.kill_piece(row, col):
                            game.current_player = 3 - game.current_player
                            state = "place"
                            winner = game.check_winner()

        draw_board(game)
        if state == "kill":
            kill_text = font.render("请选择要杀的棋子", True, RED)
            screen.blit(kill_text, (WINDOW_WIDTH // 2 - 100, 10))
        if winner:
            show_winner(winner)
        pygame.display.flip()

if __name__ == "__main__":
    main()