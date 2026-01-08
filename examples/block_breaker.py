#!/usr/bin/env python3
"""
ブロック崩しゲーム (Block Breaker)
Raspberry Pi 5で動作するPygameゲーム

操作方法:
- 左右矢印キー or A/D: パドルを移動
- スペースキー: ゲーム開始/ボールを発射
- ESC: ゲーム終了
"""

import pygame
import sys
import random

# 初期化
pygame.init()

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)
CYAN = (0, 255, 255)

# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# ゲーム要素のサイズ
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_SIZE = 10
BLOCK_WIDTH = 75
BLOCK_HEIGHT = 20
BLOCK_ROWS = 5
BLOCK_COLS = 10

# 速度設定
PADDLE_SPEED = 8
BALL_SPEED_X = 5
BALL_SPEED_Y = -5


class Paddle:
    """パドルクラス"""
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = PADDLE_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        """パドルを移動"""
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == "right" and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        """パドルを描画"""
        pygame.draw.rect(screen, BLUE, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)  # 枠線


class Ball:
    """ボールクラス"""
    def __init__(self, paddle):
        self.size = BALL_SIZE
        self.reset(paddle)

    def reset(self, paddle):
        """ボールをリセット"""
        self.x = paddle.rect.centerx
        self.y = paddle.rect.top - self.size
        self.speed_x = 0
        self.speed_y = 0
        self.active = False
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def launch(self):
        """ボールを発射"""
        if not self.active:
            self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
            self.speed_y = BALL_SPEED_Y
            self.active = True

    def move(self, paddle):
        """ボールを移動"""
        if not self.active:
            # パドルに追従
            self.rect.centerx = paddle.rect.centerx
            self.rect.bottom = paddle.rect.top
        else:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            # 壁との衝突判定
            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.speed_x *= -1
            if self.rect.top <= 0:
                self.speed_y *= -1

    def draw(self, screen):
        """ボールを描画"""
        pygame.draw.circle(screen, RED, self.rect.center, self.size // 2)


class Block:
    """ブロッククラス"""
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.color = color
        self.active = True

    def draw(self, screen):
        """ブロックを描画"""
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 1)  # 枠線


class Game:
    """ゲームメインクラス"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ブロック崩し - Block Breaker")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.reset_game()

    def reset_game(self):
        """ゲームをリセット"""
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.blocks = self.create_blocks()
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_won = False

    def create_blocks(self):
        """ブロックを生成"""
        blocks = []
        colors = [RED, ORANGE, YELLOW, GREEN, CYAN]

        offset_x = (SCREEN_WIDTH - (BLOCK_COLS * BLOCK_WIDTH + (BLOCK_COLS - 1) * 5)) // 2
        offset_y = 50

        for row in range(BLOCK_ROWS):
            for col in range(BLOCK_COLS):
                x = offset_x + col * (BLOCK_WIDTH + 5)
                y = offset_y + row * (BLOCK_HEIGHT + 5)
                color = colors[row % len(colors)]
                blocks.append(Block(x, y, color))

        return blocks

    def check_collisions(self):
        """衝突判定"""
        # パドルとの衝突
        if self.ball.rect.colliderect(self.paddle.rect) and self.ball.speed_y > 0:
            self.ball.speed_y *= -1
            # パドルのどこに当たったかで角度を変える
            hit_pos = (self.ball.rect.centerx - self.paddle.rect.left) / self.paddle.rect.width
            self.ball.speed_x = (hit_pos - 0.5) * 10

        # ブロックとの衝突
        for block in self.blocks:
            if block.active and self.ball.rect.colliderect(block.rect):
                block.active = False
                self.ball.speed_y *= -1
                self.score += 10
                break

        # ボールが画面下に落ちた
        if self.ball.rect.top >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.ball.reset(self.paddle)

        # 全ブロック破壊
        if all(not block.active for block in self.blocks):
            self.game_won = True

    def draw(self):
        """画面描画"""
        self.screen.fill(BLACK)

        # ゲーム要素の描画
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

        for block in self.blocks:
            block.draw(self.screen)

        # スコアとライフの表示
        score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.small_font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))

        # ゲーム開始前のメッセージ
        if not self.ball.active and not self.game_over and not self.game_won:
            start_text = self.small_font.render("Press SPACE to start", True, YELLOW)
            text_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(start_text, text_rect)

        # ゲームオーバー
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.small_font.render("Press R to Restart or ESC to Quit", True, WHITE)
            self.screen.blit(game_over_text,
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text,
                           (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 + 20))

        # ゲームクリア
        if self.game_won:
            win_text = self.font.render("YOU WIN!", True, GREEN)
            score_text = self.small_font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.small_font.render("Press R to Restart or ESC to Quit", True, WHITE)
            self.screen.blit(win_text,
                           (SCREEN_WIDTH // 2 - win_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 - 60))
            self.screen.blit(score_text,
                           (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                            SCREEN_HEIGHT // 2))
            self.screen.blit(restart_text,
                           (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 + 40))

        pygame.display.flip()

    def handle_input(self):
        """入力処理"""
        keys = pygame.key.get_pressed()

        if not self.game_over and not self.game_won:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.paddle.move("left")
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.paddle.move("right")

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
                        if not self.game_over and not self.game_won:
                            self.ball.launch()

                    if event.key == pygame.K_r:
                        if self.game_over or self.game_won:
                            self.reset_game()

            if not self.game_over and not self.game_won:
                self.handle_input()
                self.ball.move(self.paddle)
                self.check_collisions()

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """メイン関数"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
