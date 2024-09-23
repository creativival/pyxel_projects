import pyxel
import time
# from voxelamming import Voxelamming
from voxelamming_local import Voxelamming  # ローカルで開発している場合はこちらを使う


class Cat:
    name = 'cat_8x8'
    dot_data = (
        '-1 -1 9 -1 9 -1 -1 -1 -1 -1 9 9 9 9 -1 -1 '
        '-1 -1 9 0 9 0 9 -1 -1 -1 9 9 7 7 7 -1 -1 -1 '
        '9 9 9 -1 -1 -1 9 9 9 9 9 9 9 -1 -1 -1 9 9 7 '
        '-1 -1 -1 -1 9 9 -1 9 9 -1 -1'
    )

    def __init__(self, window_width, window_height):
        self.direction = 0
        self.x = window_width // 2 - 4
        self.y = window_height // 2 - 4
        self.img = 0
        self.u = 0
        self.v = 0
        self.w = 8
        self.h = 8
        self.speed = 0.1  # 猫の移動速度
        self.scale = 0.5  # 初期の猫のサイズ（デフォルトの0.5倍）

    def chase(self, mouse):
        # 猫がマウスを追いかける
        if self.x < mouse.x:
            self.x += self.speed
            self.w = 8
            self.h = 8
            self.direction = 0
        elif self.x > mouse.x:
            self.x -= self.speed
            self.w = -8
            self.h = 8
            self.direction = -180  # 画像を反転させる

        if self.y < mouse.y:
            self.y += self.speed
        elif self.y > mouse.y:
            self.y -= self.speed

        # 猫のサイズを徐々に大きくする
        self.scale += 0.005


class Mouse:
    name = 'mouse_8x8'
    dot_data = (
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 13 -1 -1 13 -1 -1 -1 '
        '-1 13 13 13 -1 -1 -1 -1 -1 13 13 13 13 0 13 -1 '
        '13 13 13 13 13 13 13 0 -1 13 13 13 13 0 13 -1 '
        '-1 13 13 13 -1 -1 -1 -1 -1 13 -1 -1 13 -1 -1 -1'
    )

    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.direction = 0
        self.x = (self.window_width // 2 - 4) + 20
        self.y = self.window_height // 2 - 4
        self.img = 0
        self.u = 0
        self.v = 8
        self.w = 8
        self.h = 8
        self.speed = 0.5  # マウスの移動速度
        self.scale = 1  # マウスのサイズ（デフォルトサイズ）

    def move(self):
        # 矢印キーでマウスを動かす
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
            self.u = 0
            self.v = 8
            self.w = -8
            self.h = 8
            self.direction = 180  # 180度回転させる
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
            self.u = 0
            self.v = 8
            self.w = 8
            self.h = 8
            self.direction = 0
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
            self.u = 8
            self.v = 8
            self.w = 8
            self.h = 8
            self.direction = 90
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed
            self.u = 8
            self.v = 8
            self.w = 8
            self.h = -8
            self.direction = -90

        # 画面内に動きを制限する
        self.x = max(-4, min(self.window_width - 4, self.x))
        self.y = max(-4, min(self.window_height - 4, self.y))


class App:
    def __init__(self):
        # Pyxelの設定
        self.window_width = 64 * 4 // 3  # ARウインドウの横幅はself.dot_sizeを掛けた値になる（センチメートル）
        self.window_height = 64  # ARウインドウの縦幅はself.dot_sizeを掛けた値になる（センチメートル）
        self.score = 0  # 初期スコア
        self.last_score_update_time = 0  # スコアを更新するためのタイマー
        self.game_started = False
        self.game_over = False

        # インスタンスを作成
        self.cat = Cat(self.window_width, self.window_height)
        self.mouse = Mouse(self.window_width, self.window_height)

        # ボクセラミングの設定（Pyxelの初期化の前に実行）
        self.dot_size = 1  # AR空間で表示されるスプライトのドットのサイズ（センチメートル）
        self.window_angle = 80  # ARウインドウの傾き（度）
        self.vox = Voxelamming('1000')
        self.init_voxelamming()

        # Pyxelの初期化
        pyxel.init(self.window_width, self.window_height, title='Cat Game')
        pyxel.mouse(True)
        pyxel.load('cat_game.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.game_started or self.game_over:
            # カーソル表示
            pyxel.mouse(True)

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.reset_game()
            return

        # カーソルの非表示
        pyxel.mouse(False)

        self.mouse.move()  # マウスを動かす
        self.cat.chase(self.mouse)  # 猫がマウスを追いかける

        # 衝突判定: 猫の円がマウスに触れるとゲームオーバー
        cat_radius = self.cat.scale * 4
        mouse_radius = self.mouse.scale * 4
        if ((self.cat.x - self.mouse.x) ** 2 + (self.cat.y - self.mouse.y) ** 2) < (
                cat_radius + mouse_radius) ** 2:
            self.game_over = True

        # スコアを1秒ごとに加算
        delta_time = pyxel.frame_count - self.last_score_update_time
        if delta_time >= 30:  # PyxelのデフォルトFPSは30
            self.score += 1
            self.last_score_update_time = pyxel.frame_count

        # ボクセラミングの更新
        self.update_voxelamming()

    def draw(self):
        pyxel.cls(1)

        # スコアを左上に表示する
        pyxel.text(2, 2, f"Score: {self.score}", pyxel.COLOR_WHITE)

        if not self.game_started:
            pyxel.text(self.window_width // 2 - 26, self.window_height // 2 - 8, "Click to start",
                       pyxel.frame_count % 16)
            return

        if self.game_over:
            pyxel.text(self.window_width // 2 - 26, self.window_height // 2 - 8, "Game Over!", pyxel.frame_count % 16)
            pyxel.text(self.window_width // 2 - 26, self.window_height // 2 + 8, "Click to start",
                       pyxel.frame_count % 16)
            return

        # 猫のスプライトを描画する
        pyxel.blt(self.cat.x, self.cat.y, self.cat.img, self.cat.u, self.cat.v, self.cat.w, self.cat.h, 1, 0,
                  self.cat.scale)
        # マウスのスプライトを描画する
        pyxel.blt(self.mouse.x, self.mouse.y, self.mouse.img, self.mouse.u, self.mouse.v, self.mouse.w, self.mouse.h, 1)

    def reset_game(self):
        self.score = 0  # スコアをリセット
        self.last_score_update_time = pyxel.frame_count  # タイマーをリセット
        self.cat = Cat(self.window_width, self.window_height)  # 猫の初期化(位置、サイズ)
        self.mouse = Mouse(self.window_width, self.window_height)  # マウスの初期化(位置)
        self.game_started = True
        self.game_over = False

    def init_voxelamming(self):
        self.vox.set_box_size(self.dot_size)
        self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1, blue=0,
                                 alpha=0.8)
        # スコアはサイズ24x2として、中心基準で表示する位置を計算する
        self.vox.set_game_score(self.score, -28, 26)
        self.vox.set_command('liteRender')

        # 猫とマウスのスプライトを作成
        self.vox.create_sprite(self.cat.name, self.cat.dot_data, visible=False)
        self.vox.create_sprite(self.mouse.name, self.mouse.dot_data, visible=False)

        self.vox.send_data()
        self.vox.clear_data()

    def update_voxelamming(self):
        # スプライトの情報を0.1秒ごとに送信
        if pyxel.frame_count % 3 == 0 or self.game_over:  # PyxelのデフォルトFPSは30
            self.vox.set_box_size(self.dot_size)
            self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1,
                                     blue=0, alpha=0.5)
            self.vox.set_game_score(self.score, -28, 26)
            self.vox.set_command('liteRender')

            cat_x, cat_y = self.convert_position_to_voxelamming(self.cat.x, self.cat.y, self.cat.w, self.cat.h)
            cat_scale = self.cat.scale
            self.vox.move_sprite(self.cat.name, cat_x, cat_y, self.cat.direction, cat_scale)

            mouse_x, mouse_y = self.convert_position_to_voxelamming(self.mouse.x, self.mouse.y, self.cat.w, self.cat.h)
            mouse_scale = self.mouse.scale
            self.vox.move_sprite(self.mouse.name, mouse_x, mouse_y, self.mouse.direction, mouse_scale)

            self.vox.send_data()

            # ゲームオーバーの表示と画面を赤に変更
            if self.game_over:
                self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=0,
                                         blue=0, alpha=0.8)
                self.vox.send_game_over()

            self.vox.send_data()

            # ゲームオーバー時に1秒待ってから再度データを送信
            if self.game_over:
                time.sleep(1)
                self.vox.send_data()

            self.vox.clear_data()

    def convert_position_to_voxelamming(self, x, y, width=1, height=1):
        return x - self.window_width // 2 + width // 2, self.window_height // 2 - (y + height // 2)


App()
