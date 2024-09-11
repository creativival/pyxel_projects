import pyxel

WINDOW_WIDTH = 80
WINDOW_HEIGHT = 64


class Cat:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = 0
        self.u = 0
        self.v = 0
        self.w = 8
        self.h = 8
        self.speed = 0.1  # 猫の移動速度
        self.diameter = 4  # 初期の猫のサイズ（円の直径）

    def chase(self, mouse):
        # 猫がマウスを追いかける
        if self.x < mouse.x:
            self.x += self.speed
            self.w = 8
            self.h = 8
        elif self.x > mouse.x:
            self.x -= self.speed
            self.w = -8
            self.h = 8

        if self.y < mouse.y:
            self.y += self.speed
        elif self.y > mouse.y:
            self.y -= self.speed

        # 猫のサイズを徐々に大きくする
        self.diameter += 0.05


class Mouse:
    def __init__(self):
        self.x = 20
        self.y = 0
        self.img = 0
        self.u = 0
        self.v = 8
        self.w = 8
        self.h = 8
        self.speed = 0.5  # マウスの移動速度
        self.diameter = 8  # マウスのサイズ（円の直径）

    def move(self):
        # 矢印キーでマウスを動かす
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
            self.u = 0
            self.v = 8
            self.w = -8
            self.h = 8
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
            self.u = 0
            self.v = 8
            self.w = 8
            self.h = 8
        if pyxel.btn(pyxel.KEY_UP):
            self.y += self.speed
            self.u = 8
            self.v = 8
            self.w = 8
            self.h = 8
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y -= self.speed
            self.u = 8
            self.v = 8
            self.w = 8
            self.h = -8

        # 画面内に動きを制限する
        self.x = max(-WINDOW_WIDTH // 2, min(WINDOW_WIDTH // 2, self.x))
        self.y = max(-WINDOW_HEIGHT // 2, min(WINDOW_HEIGHT // 2, self.y))


def get_sprite_position(x, y):
    return WINDOW_WIDTH // 2 + x - 4, WINDOW_HEIGHT // 2 - y - 4


class App:
    def __init__(self):
        self.cat = Cat()
        self.mouse = Mouse()
        self.game_started = False
        self.game_over = False
        self.score = 0  # 初期スコア
        self.last_score_update_time = 0  # スコアを更新するためのタイマー

        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title='Cat Game')

        pyxel.load('cat_game.pyxres')

        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.game_started:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.reset_game()
            return

        if self.game_over:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.reset_game()
            return

        self.mouse.move()  # マウスの位置を更新
        self.cat.chase(self.mouse)  # 猫がマウスを追いかける

        # 衝突判定: 猫の円がマウスに触れるとゲームオーバー
        if ((self.cat.x - self.mouse.x) ** 2 + (self.cat.y - self.mouse.y) ** 2) < (
                self.cat.diameter / 2 + self.mouse.diameter / 2) ** 2:
            self.game_over = True

        # スコアを1秒ごとに加算
        if pyxel.frame_count - self.last_score_update_time >= 30:  # PyxelのデフォルトFPSは30
            self.score += 1
            self.last_score_update_time = pyxel.frame_count

    def draw(self):
        pyxel.cls(1)

        # スコアを左上に表示する
        pyxel.text(2, 2, f"Score: {self.score}", pyxel.COLOR_WHITE)

        if not self.game_started:
            pyxel.text(WINDOW_WIDTH // 2 - 26, WINDOW_HEIGHT // 2 - 8, "Click to start", pyxel.frame_count % 16)
            self.draw_cursor()  # カスタムカーソルの描画
            return

        if self.game_over:
            pyxel.text(WINDOW_WIDTH // 2 - 30, WINDOW_HEIGHT // 2 - 8, "Game Over!", pyxel.frame_count % 16)
            pyxel.text(WINDOW_WIDTH // 2 - 30, WINDOW_HEIGHT // 2 + 8, "Click to start", pyxel.frame_count % 16)
            self.draw_cursor()  # カスタムカーソルの描画
            return

        # 徐々に大きくなる円を描画する
        cat_x, cat_y = get_sprite_position(self.cat.x, self.cat.y)
        pyxel.circ(cat_x + 4, cat_y + 4, self.cat.diameter / 2, pyxel.COLOR_RED)

        # 猫のスプライトを描画する
        pyxel.blt(cat_x, cat_y, self.cat.img, self.cat.u, self.cat.v, self.cat.w, self.cat.h, 1)

        # マウスのスプライトを描画する
        mouse_x, mouse_y = get_sprite_position(self.mouse.x, self.mouse.y)
        pyxel.blt(mouse_x, mouse_y, self.mouse.img, self.mouse.u, self.mouse.v, self.mouse.w, self.mouse.h, 1)

    def reset_game(self):
        self.score = 0  # スコアをリセット
        self.last_score_update_time = pyxel.frame_count  # タイマーをリセット
        self.cat = Cat()  # 猫の初期化(位置、サイズ)
        self.mouse = Mouse()  # マウスの初期化(位置)
        self.game_started = True
        self.game_over = False

    def draw_cursor(self):
        cursor_x = pyxel.mouse_x
        cursor_y = pyxel.mouse_y
        pyxel.blt(cursor_x - 4, cursor_y - 4, 0, 0, 16, 8, 8, 1)


App()
