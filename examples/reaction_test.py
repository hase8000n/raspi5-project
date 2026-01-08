#!/usr/bin/env python3
"""
反射神経測定ゲーム (Reaction Time Test)
Raspberry Pi 5で動作するPygameゲーム

ゲーム説明:
- 緑色の丸が表示されます
- 3-10秒後にランダムなタイミングで青色に変化します
- 青色に変わったらすぐにスペースキーを押してください
- 反応時間（ミリ秒）が表示されます

操作方法:
- スペースキー: 反応時間を測定
- R: もう一度プレイ
- ESC: ゲーム終了
"""

import pygame
import sys
import random
import time

# 初期化
pygame.init()

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 円のサイズ
CIRCLE_RADIUS = 100


class ReactionGame:
    """反射神経測定ゲームクラス"""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("反射神経測定ゲーム - Reaction Time Test")
        self.clock = pygame.time.Clock()

        # 日本語対応フォントを使用
        try:
            # Raspberry Pi OSの標準日本語フォントを試す
            self.font_large = pygame.font.Font("/usr/share/fonts/truetype/fonts-japanese-gothic.ttf", 72)
            self.font_medium = pygame.font.Font("/usr/share/fonts/truetype/fonts-japanese-gothic.ttf", 48)
            self.font_small = pygame.font.Font("/usr/share/fonts/truetype/fonts-japanese-gothic.ttf", 32)
        except:
            try:
                # 別の日本語フォントを試す
                self.font_large = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 72)
                self.font_medium = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 48)
                self.font_small = pygame.font.Font("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 32)
            except:
                # システムのデフォルトフォントを使用
                self.font_large = pygame.font.SysFont("notosanscjk", 72)
                self.font_medium = pygame.font.SysFont("notosanscjk", 48)
                self.font_small = pygame.font.SysFont("notosanscjk", 32)

        self.best_time = None
        self.state = "menu"  # 最初はメニュー画面

    def reset_game(self):
        """ゲームをリセット"""
        self.state = "waiting"  # menu, waiting, blue, result, too_early
        self.circle_color = GREEN
        self.wait_time = random.uniform(3.0, 10.0)  # 3-10秒のランダムな待機時間
        self.start_time = time.time()
        self.reaction_time = None
        self.blue_change_time = None

    def handle_space_press(self):
        """スペースキーが押された時の処理"""
        if self.state == "waiting":
            # 青になる前に押した場合
            self.state = "too_early"

        elif self.state == "blue":
            # 青になった後に押した場合（正しい反応）
            current_time = time.time()
            self.reaction_time = (current_time - self.blue_change_time) * 1000  # ミリ秒に変換
            self.state = "result"

            # ベストタイムを更新
            if self.best_time is None or self.reaction_time < self.best_time:
                self.best_time = self.reaction_time

    def update(self):
        """ゲーム状態を更新"""
        if self.state == "waiting":
            # 待機中: 設定時間が経過したら青に変更
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= self.wait_time:
                self.circle_color = BLUE
                self.state = "blue"
                self.blue_change_time = time.time()

    def draw(self):
        """画面描画"""
        self.screen.fill(BLACK)

        # 円の描画
        circle_x = SCREEN_WIDTH // 2
        circle_y = SCREEN_HEIGHT // 2

        if self.state in ["waiting", "blue"]:
            pygame.draw.circle(self.screen, self.circle_color,
                             (circle_x, circle_y), CIRCLE_RADIUS)

        # 状態に応じたメッセージ表示
        if self.state == "menu":
            # メニュー画面
            title_text = self.font_large.render("反射神経測定", True, YELLOW)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(title_text, title_rect)

            subtitle_text = self.font_medium.render("Reaction Time Test", True, WHITE)
            subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 230))
            self.screen.blit(subtitle_text, subtitle_rect)

            # 説明文
            desc1 = self.font_small.render("緑色の丸が青色に変わったら", True, GRAY)
            desc2 = self.font_small.render("素早くスペースキーを押してください", True, GRAY)
            desc1_rect = desc1.get_rect(center=(SCREEN_WIDTH // 2, 320))
            desc2_rect = desc2.get_rect(center=(SCREEN_WIDTH // 2, 360))
            self.screen.blit(desc1, desc1_rect)
            self.screen.blit(desc2, desc2_rect)

            # スタートボタン風の表示
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 440, 300, 60)
            pygame.draw.rect(self.screen, GREEN, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 3)

            start_text = self.font_medium.render("スタート", True, BLACK)
            start_rect = start_text.get_rect(center=button_rect.center)
            self.screen.blit(start_text, start_rect)

            # 操作説明
            instruction_text = self.font_small.render("スペースキーを押してスタート", True, GRAY)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 540))
            self.screen.blit(instruction_text, instruction_rect)

        elif self.state == "waiting":
            # 待機中のメッセージ
            title_text = self.font_medium.render("準備してください...", True, WHITE)
            instruction_text = self.font_small.render("青色に変わったらスペースキーを押してください", True, GRAY)

            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 150))

            self.screen.blit(title_text, title_rect)
            self.screen.blit(instruction_text, instruction_rect)

        elif self.state == "blue":
            # 青色表示中（反応待ち）
            instruction_text = self.font_medium.render("今だ！スペースキーを押せ！", True, BLUE)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(instruction_text, instruction_rect)

        elif self.state == "result":
            # 結果表示
            result_text = self.font_large.render("結果", True, WHITE)
            result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(result_text, result_rect)

            # 反応時間の表示
            time_text = self.font_medium.render(f"{self.reaction_time:.0f} ミリ秒", True, YELLOW)
            time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
            self.screen.blit(time_text, time_rect)

            # 評価メッセージ
            if self.reaction_time < 200:
                evaluation = "素晴らしい！"
                eval_color = GREEN
            elif self.reaction_time < 300:
                evaluation = "良好！"
                eval_color = GREEN
            elif self.reaction_time < 400:
                evaluation = "普通"
                eval_color = YELLOW
            else:
                evaluation = "もう少し頑張ろう"
                eval_color = RED

            eval_text = self.font_medium.render(evaluation, True, eval_color)
            eval_rect = eval_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
            self.screen.blit(eval_text, eval_rect)

            # ベストタイム表示
            if self.best_time is not None:
                best_text = self.font_small.render(f"ベストタイム: {self.best_time:.0f} ms", True, WHITE)
                best_rect = best_text.get_rect(center=(SCREEN_WIDTH // 2, 380))
                self.screen.blit(best_text, best_rect)

            # 再プレイの案内
            retry_text = self.font_small.render("Rキー: もう一度 / Mキー: メニュー / ESC: 終了", True, GRAY)
            retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
            self.screen.blit(retry_text, retry_rect)

        elif self.state == "too_early":
            # 早すぎた場合のメッセージ
            warning_text = self.font_large.render("早すぎ！", True, RED)
            warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
            self.screen.blit(warning_text, warning_rect)

            instruction_text = self.font_small.render("青色に変わってから押してください", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
            self.screen.blit(instruction_text, instruction_rect)

            # 再プレイの案内
            retry_text = self.font_small.render("Rキー: もう一度 / Mキー: メニュー / ESC: 終了", True, GRAY)
            retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
            self.screen.blit(retry_text, retry_rect)

        pygame.display.flip()

    def run(self):
        """メインループ"""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_SPACE:
                        if self.state == "menu":
                            # メニューからゲーム開始
                            self.reset_game()
                        else:
                            # ゲーム中のスペース処理
                            self.handle_space_press()

                    if event.key == pygame.K_r:
                        if self.state in ["result", "too_early"]:
                            self.reset_game()

                    if event.key == pygame.K_m:
                        if self.state in ["result", "too_early"]:
                            self.state = "menu"

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """メイン関数"""
    game = ReactionGame()
    game.run()


if __name__ == "__main__":
    main()
