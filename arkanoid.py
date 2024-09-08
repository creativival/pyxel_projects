import pyxel
import random


class GameState:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_clear = False
        self.ball_attached = True


class Paddle:
    def __init__(self):
        self.x = 30
        self.y = 55
        self.width = 16
        self.height = 2
        self.speed = 2

    def update(self):
        # パドルの操作
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(self.x - self.speed, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(self.x + self.speed, pyxel.width - self.width)

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 7)


class Bricks:
    def __init__(self):
        self.width = 8
        self.height = 4
        self.brick_list = []

    def create(self):
        # ブロックを作成
        for i in range(5):  # 5行
            for j in range(8):  # 8列
                brick_x = j * (self.width + 1) + 5  # 左に5pxの余白を追加
                brick_y = i * (self.height + 1) + 10  # 縦方向も調整
                self.brick_list.append([brick_x, brick_y, self.width, self.height])

    def draw(self):
        for brick in self.brick_list:
            brick_x, brick_y, brick_width, brick_height = brick
            pyxel.rect(brick_x, brick_y, brick_width, brick_height, 9)


class Ball:
    def __init__(self, paddle, bricks, game_state):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.paddle = paddle
        self.bricks = bricks
        self.game_state = game_state
        self.radius = 1  # ボールの半径を半分に
        self.reset()

    def reset(self):
        self.x = self.paddle.x + self.paddle.width // 2
        self.y = self.paddle.y - self.radius - 1
        self.game_state.ball_attached = True
        self.dx = random.choice([-0.5, 0.5])
        self.dy = -0.5

    def update(self):
        if self.game_state.game_over or self.game_state.game_clear:
            return

        if self.game_state.ball_attached:
            self.x = self.paddle.x + self.paddle.width // 2
            self.y = self.paddle.y - self.radius - 1

            # スペースキーを押すとボールが発射される
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.game_state.ball_attached = False
                self.dx = random.choice([-0.5, 0.5])
                self.dy = -0.5
        else:
            self.x += self.dx
            self.y += self.dy

            # ボールの壁との当たり判定
            if self.x < 0 or self.x > pyxel.width - self.radius:
                self.dx *= -1  # x方向の速度を反転
            if self.y < 0:
                self.dy *= -1  # y方向の速度を反転

            # ボールがパドルに当たった場合の処理
            if (self.paddle.x < self.x < self.paddle.x + self.paddle.width and
                    self.paddle.y < self.y + self.radius < self.paddle.y + self.paddle.height):
                self.dy *= -1  # y方向の速度を反転

            # ボールがブロックに当たった場合の処理
            for brick in self.bricks.brick_list[:]:
                brick_x, brick_y, brick_width, brick_height = brick
                if (brick_x < self.x < brick_x + brick_width and
                        brick_y < self.y < brick_y + brick_height):
                    self.bricks.brick_list.remove(brick)
                    self.dy *= -1  # ボールのy方向の速度を反転
                    self.game_state.score += 10  # スコア加算
                    break

            # 全てのブロックが破壊されたらゲームクリア
            if len(self.bricks.brick_list) == 0:
                self.game_state.game_clear = True

            # ボールが下まで落ちた場合
            if self.y > pyxel.height:
                self.game_state.lives -= 1  # 残機を減らす
                if self.game_state.lives > 0:
                    self.reset()
                else:
                    self.game_state.game_over = True  # 残機がなくなったらゲームオーバー

    def draw(self):
        pyxel.rect(self.x, self.y, self.radius * 2, self.radius * 2, 8)


class App:
    def __init__(self):
        self.window_width = 80
        self.window_height = 60
        self.game_state = GameState()
        self.paddle = Paddle()
        self.bricks = Bricks()
        self.bricks.create()
        self.ball = Ball(self.paddle, self.bricks, self.game_state)

        pyxel.init(self.window_width, self.window_height, title="Arkanoid", fps=30)
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_state.game_over or self.game_state.game_clear:
            return

        # パドルの操作
        self.paddle.update()

        # ボールの操作
        self.ball.update()

    def draw(self):
        pyxel.cls(0)  # 画面クリア
        self.paddle.draw()
        self.ball.draw()
        self.bricks.draw()

        # スコアの表示
        pyxel.text(1, 2, f"SCORE: {self.game_state.score}", 7)

        # 残機の表示
        pyxel.text(48, 2, f"LIVES: {self.game_state.lives}", 7)

        # ゲームオーバー時の表示
        if self.game_state.game_over:
            pyxel.text(20, 30, "GAME OVER", pyxel.frame_count % 16)

        # ゲームクリア時の表示
        if self.game_state.game_clear:
            pyxel.text(20, 30, "YOU WIN!", pyxel.frame_count % 16)


# ゲームの実行
App()
