import pyxel
import random


class Bird:
    def __init__(self, app):
        self.x = 10
        self.y = app.window_height // 2
        self.img = 0
        self.u = 0
        self.v = 64
        self.w = 4
        self.h = 4
        self.size = 4
        self.gravity = 0.25
        self.flap_strength = -2
        self.velocity = 0

    def update(self):
        # スペースキーで鳥が上昇
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.velocity = self.flap_strength
        # 重力の影響で鳥が落下
        self.velocity += self.gravity
        self.y += self.velocity

        # 鳥が画面外に出ないように制御
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        if self.y > pyxel.height - self.size:
            self.y = pyxel.height - self.size
            self.velocity = 0

    def draw(self):
        # pyxel.circ(self.x, self.y, self.size, 10)  # 鳥の描画
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w, self.h)  # 鳥の描画


class Pipe:
    def __init__(self, x, gap_y, gap_height):
        self.x = x
        self.gap_y = gap_y
        self.img = 0
        self.u = 0
        self.v = 0
        self.w = 8
        self.h = 32
        self.gap_height = gap_height
        self.pipe_width = 8
        self.pipe_height = 32
        self.speed = 1

    def update(self):
        # パイプを左に移動
        self.x -= self.speed

    def draw(self):
        # 上のパイプ
        pyxel.blt(self.x, self.gap_y - self.pipe_height, self.img, self.u, self.v, self.w, self.h)
        # # 下のパイプ

        pyxel.blt(self.x, self.gap_y + self.gap_height, self.img, self.u, self.v + self.h, self.w, self.h)

    def is_off_screen(self):
        return self.x + self.pipe_width < 0


class App:
    def __init__(self):
        self.window_width = 80
        self.window_height = 60
        self.pipes = []
        self.pipe_gap = 20
        self.pipe_interval = 30
        self.pipe_timer = 0
        self.score = 0
        self.game_over = False

        self.bird = Bird(self)

        pyxel.init(self.window_width, self.window_height, title="Flappy Bird", fps=30)
        pyxel.load('flappy_bird.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over:
            return

        self.bird.update()

        # パイプの出現管理
        self.pipe_timer += 1
        if self.pipe_timer > self.pipe_interval:
            gap_y = random.randint(10, pyxel.height - 30)  # ランダムな位置の調整
            self.pipes.append(Pipe(pyxel.width, gap_y, self.pipe_gap))
            self.pipe_timer = 0

        # パイプの更新と削除
        for pipe in self.pipes[:]:
            pipe.update()
            if pipe.is_off_screen():
                self.pipes.remove(pipe)
                self.score += 1  # パイプを通過するごとにスコアを加算

        # 衝突判定
        self.check_collision()

    def check_collision(self):
        # 鳥とパイプの衝突判定
        for pipe in self.pipes:
            if (pipe.x < self.bird.x + self.bird.size < pipe.x + pipe.pipe_width):
                if self.bird.y < pipe.gap_y or self.bird.y > pipe.gap_y + pipe.gap_height:
                    self.game_over = True

    def draw(self):
        pyxel.cls(0)  # 画面クリア

        # 鳥の描画
        self.bird.draw()

        # パイプの描画
        for pipe in self.pipes:
            pipe.draw()

        # スコアの表示
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)

        # ゲームオーバー時の表示
        if self.game_over:
            pyxel.text(30, 30, "GAME OVER", pyxel.frame_count % 16)


# ゲームの実行
App()
