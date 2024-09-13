import pyxel


class Paddle:
    def __init__(self):
        self.x = 30
        self.y = 55
        self.width = 32
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


class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = True

    def draw(self):
        if self.visible:
            pyxel.rect(self.x, self.y, self.width, self.height, 9)

    @classmethod
    def create_bricks(cls):
        # ブロックを作成
        bricks = []
        for i in range(5):
            for j in range(8):
                x = j * (cls.width + 1) + 5
                y = i * (cls.height + 1) + 10
                bricks.append(cls(x, y))
        return bricks


class Ball:
    def __init__(self, app, paddle, bricks):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.app = app
        self.paddle = paddle
        self.bricks = bricks
        self.radius = 1  # ボールの半径を半分に
        self.reset()

    def reset(self):
        self.x = self.paddle.x + self.paddle.width // 2
        self.y = self.paddle.y - self.radius - 1
        self.app.ball_attached = True
        self.dx = 0.5
        self.dy = -0.5

    def update(self):
        if self.app.game_over or self.app.game_clear:
            return

        if self.app.ball_attached:
            self.x = self.paddle.x + self.paddle.width // 2
            self.y = self.paddle.y - self.radius - 1

            # スペースキーを押すとボールが発射される
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.app.ball_attached = False
                self.dx = 0.5
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
            for brick in self.bricks[:]:
                if (brick.visible and brick.x < self.x < brick.x + brick.width and
                        brick.y < self.y < brick.y + brick.height):
                    brick.visible = False  # ブロックを非表示にする
                    self.dy *= -1  # ボールのy方向の速度を反転
                    self.app.score += 10  # スコア加算
                    break

            # 全てのブロックが破壊されたらゲームクリア
            visible_bricks = [brick for brick in self.bricks if brick.visible]
            if len(visible_bricks) == 0:
                self.app.game_clear = True

            # ボールが下まで落ちた場合
            if self.y > pyxel.height:
                self.app.lives -= 1  # 残機を減らす
                if self.app.lives > 0:
                    self.reset()
                else:
                    self.app.game_over = True  # 残機がなくなったらゲームオーバー

    def draw(self):
        pyxel.rect(self.x, self.y, self.radius * 2, self.radius * 2, 8)


class App:
    def __init__(self):
        self.window_width = 80
        self.window_height = 60
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_clear = False
        self.ball_attached = True

        # インスタンスを作成
        self.paddle = Paddle()
        self.bricks = Brick.create_bricks()
        self.ball = Ball(self, self.paddle, self.bricks)

        pyxel.init(self.window_width, self.window_height, title="Arkanoid", fps=30)
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over or self.game_clear:
            return

        # パドルの操作
        self.paddle.update()

        # ボールの操作
        self.ball.update()

    def draw(self):
        pyxel.cls(0)  # 画面クリア
        self.paddle.draw()
        self.ball.draw()
        for brick in self.bricks:
            brick.draw()

        # スコアの表示
        pyxel.text(1, 2, f"SCORE: {self.score}", 7)

        # 残機の表示
        pyxel.text(48, 2, f"LIVES: {self.lives}", 7)

        # ゲームオーバー時の表示
        if self.game_over:
            pyxel.text(20, 30, "GAME OVER", pyxel.frame_count % 16)

        # ゲームクリア時の表示
        if self.game_clear:
            pyxel.text(20, 30, "YOU WIN!", pyxel.frame_count % 16)


# ゲームの実行
App()
