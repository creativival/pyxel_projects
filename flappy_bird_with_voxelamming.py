import pyxel
import random
import time
# from voxelamming import Voxelamming
from voxelamming_local import Voxelamming  # ローカルで開発している場合はこちらを使う


class Bird:
    name = 'bird_4x4'
    dot_data = (
        '-1 10 10 7 7 10 10 0 10 10 8 8 -1 10 10 -1'
    )

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
    name_top = 'pipe_top_32x32'
    dot_data_top = (
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 7 7 7 7 7 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 '
        '11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 '
        '11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 '
        '11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 '
        '11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 7 7 7 7 7 3 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 3 3 3 3 3 3 3 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1'
    )
    name_bottom = 'pipe_bottom_32x32'
    dot_data_bottom = (
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 7 7 7 7 7 7 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 7 11 11 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '7 11 11 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 3 3 3 3 3 3 3 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 '
        '11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 '
        '11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 7 11 11 11 11 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '7 3 3 3 3 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1'
    )

    def __init__(self, x, gap_y, gap_height):
        self.width = 8
        self.height = 32
        self.x = x
        self.gap_y = gap_y
        self.gap_height = gap_height
        self.y_top = self.gap_y - self.height
        self.y_bottom = self.gap_y + self.gap_height
        self.img = 0
        self.u = 0
        self.v = 0
        self.w = 8
        self.h = 32
        self.speed = 1

    def update(self):
        # パイプを左に移動
        self.x -= self.speed

    def draw(self):
        # 上のパイプ
        pyxel.blt(self.x, self.gap_y - self.height, self.img, self.u, self.v, self.w, self.h)
        # # 下のパイプ

        pyxel.blt(self.x, self.gap_y + self.gap_height, self.img, self.u, self.v + self.h, self.w, self.h)

    def is_off_screen(self):
        return self.x + self.width < 0


class App:
    def __init__(self):
        self.window_width = 80
        self.window_height = 60
        self.pipes = []
        self.pipe_gap = 30  # パイプ間の隙間の高さ
        self.pipe_interval = 30  # パイプの出現間隔
        self.pipe_position_variation = 5  # パイプ位置のばらつき範囲をインスタンス変数に設定
        self.pipe_timer = 0
        self.score = 0
        self.game_over = False
        self.bird = Bird(self)

        # ボクセラミングの設定（Pyxelの初期化の前に実行）
        self.dot_size = 1  # AR空間で表示されるスプライトのドットのサイズ（センチメートル）
        self.window_angle = 80  # ARウインドウの傾き（度）
        self.vox = Voxelamming('1000')
        self.init_voxelamming()

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
            # パイプの位置にばらつきを持たせるオフセット
            pipe_position_offset = random.randint(-self.pipe_position_variation, self.pipe_position_variation)
            gap_y = (self.window_height - self.pipe_gap) // 2 + pipe_position_offset  # ランダムな位置の調整
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

        # ボクセラミングの更新
        self.update_voxelamming()

    def check_collision(self):
        # 鳥とパイプの衝突判定
        for pipe in self.pipes:
            if (pipe.x < self.bird.x + self.bird.size < pipe.x + pipe.width):
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
            pyxel.text(24, 30, "GAME OVER", pyxel.frame_count % 16)

    def init_voxelamming(self):
        # ボクセラミングの初期化
        self.vox.set_box_size(self.dot_size)
        self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1, blue=0,
                                 alpha=0.8)
        self.vox.set_game_score(self.score, -24, 26)
        self.vox.set_command('liteRender')

        # バードのスプライトを表示
        self.vox.create_sprite(self.bird.name, self.bird.dot_data, visible=False)

        # パイプのスプライトを作成
        self.vox.create_sprite(Pipe.name_top, Pipe.dot_data_top, visible=False)
        self.vox.create_sprite(Pipe.name_bottom, Pipe.dot_data_bottom, visible=False)

        self.vox.send_data()
        self.vox.clear_data()

    def update_voxelamming(self):
        # スプライトの情報を0.1秒ごとに送信
        if pyxel.frame_count % 3 == 0 or self.game_over:  # PyxelのデフォルトFPSは30
            self.vox.set_box_size(self.dot_size)
            self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1,
                                     blue=0, alpha=0.5)
            self.vox.set_game_score(self.score, -24, 26)
            self.vox.set_command('liteRender')

            # バードのスプライトの移動
            vox_x, vox_y = self.convert_position_to_voxelamming(
                self.bird.x, self.bird.y, self.bird.size, self.bird.size)
            self.vox.move_sprite(self.bird.name, vox_x, vox_y, 0, 1)

            # パイプの移動はテンプレートを複数箇所に表示する
            for pipe in self.pipes[:]:
                # 上のパイプ
                vox_x, vox_y = self.convert_position_to_voxelamming(
                    pipe.x, pipe.y_top, pipe.width, pipe.height)
                self.vox.move_sprite(pipe.name_top, vox_x, vox_y, 0, 1)
                # 下のパイプ
                vox_x, vox_y = self.convert_position_to_voxelamming(
                    pipe.x, pipe.y_bottom, pipe.width, pipe.height)
                self.vox.move_sprite(pipe.name_bottom, vox_x, vox_y, 0, 1)

            # ゲームオーバーの表示と画面を赤に変更
            if self.game_over:
                self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=0,
                                         blue=0, alpha=0.8)
                self.vox.send_game_over()

            self.vox.send_data()

            # ゲームクリア、ゲームオーバー時に1秒待ってから再度データを送信
            if self.game_over:
                time.sleep(1)
                self.vox.send_data()

            self.vox.clear_data()

    def convert_position_to_voxelamming(self, x, y, width=1, height=1):
        return x - self.window_width // 2 + width // 2, self.window_height // 2 - (y + height // 2)


# ゲームの実行
App()
