import pyxel
import time
# from voxelamming import Voxelamming
from voxelamming_local import Voxelamming  # ローカルで開発している場合はこちらを使う


class Paddle:
    name = 'arkanoid_paddle_32x32'
    dot_data = (
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 '
        '7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1'
    )

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
    width = 8
    height = 4
    name = 'arkanoid_bricks_8x8'
    dot_data = (
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 '
        '9 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1'
    )

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

        # ボクセラミングの設定（Pyxelの初期化の前に実行）
        self.dot_size = 1  # AR空間で表示されるスプライトのドットのサイズ（センチメートル）
        self.window_angle = 80  # ARウインドウの傾き（度）
        self.vox = Voxelamming('1000')
        self.init_voxelamming()

        pyxel.init(self.window_width, self.window_height, title="Arkanoid", fps=30)
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over or self.game_clear:
            return

        # パドルの操作
        self.paddle.update()

        # ボールの操作
        self.ball.update()

        # ボクセラミングの更新
        self.update_voxelamming()

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

    def init_voxelamming(self):
        # ボクセラミングの初期化
        self.vox.set_box_size(self.dot_size)
        self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1, blue=0,
                                 alpha=0.8)
        self.vox.set_game_score(self.score, -24, 26)
        self.vox.display_text(f"LIVES: {self.lives}", 26, 26)
        self.vox.set_command('liteRender')

        # パドルのスプライトを表示
        self.vox.create_sprite(self.paddle.name, self.paddle.dot_data, visible=False)

        # bricksのスプライトを作成
        self.vox.create_sprite(Brick.name, Brick.dot_data, visible=False)

        self.vox.send_data()
        self.vox.clear_data()

    def update_voxelamming(self):
        # スプライトの情報を0.1秒ごとに送信
        if pyxel.frame_count % 2 == 0 or self.game_clear or self.game_over:  # PyxelのデフォルトFPSは30
            self.vox.set_box_size(self.dot_size)
            self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1,
                                     blue=0, alpha=0.5)
            self.vox.set_game_score(self.score, -24, 26)
            self.vox.display_text(f"LIVES: {self.lives}", 26, 26)
            self.vox.set_command('liteRender')

            # パドルのスプライトの移動
            vox_x, vox_y = self.convert_position_to_voxelamming(
                self.paddle.x, self.paddle.y, self.paddle.width, self.paddle.height)
            self.vox.move_sprite(self.paddle.name, vox_x, vox_y, 0, 1)

            # bricksの移動はテンプレートを複数箇所に表示する
            for brick in self.bricks:
                vox_x, vox_y = self.convert_position_to_voxelamming(
                    brick.x, brick.y, brick.width, brick.height)
                self.vox.move_sprite(brick.name, vox_x, vox_y, 0, 1)

            # ボールのスプライトを移動
            vox_x, vox_y = self.convert_position_to_voxelamming(
                self.ball.x, self.ball.y, self.ball.radius * 2, self.ball.radius * 2)
            self.vox.display_dot(vox_x, vox_y, 0, 8, self.ball.radius * 2, self.ball.radius * 2)

            # ゲームクリアの表示と画面を青に変更
            if self.game_clear:
                self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=0, green=0,
                                         blue=1, alpha=0.8)
                self.vox.send_game_clear()

            # ゲームオーバーの表示と画面を赤に変更
            if self.game_over:
                self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=0,
                                         blue=0, alpha=0.8)
                self.vox.send_game_over()

            self.vox.send_data()

            # ゲームクリア、ゲームオーバー時に1秒待ってから再度データを送信
            if self.game_clear or self.game_over:
                time.sleep(1)
                self.vox.send_data()

            self.vox.clear_data()

    def convert_position_to_voxelamming(self, x, y, width=1, height=1):
        return x - self.window_width // 2 + width // 2, self.window_height // 2 - (y + height // 2)


# ゲームの実行
App()
