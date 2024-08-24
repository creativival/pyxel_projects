import pyxel

WINDOW_WIDTH = 80
WINDOW_HEIGHT = 64


class Cat:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 0.1  # 猫の移動速度

    def chase(self, mouse):
        # 猫がマウスを追いかけるためのロジック
        if self.x < mouse.x:
            self.x += self.speed
        elif self.x > mouse.x:
            self.x -= self.speed

        if self.y < mouse.y:
            self.y += self.speed
        elif self.y > mouse.y:
            self.y -= self.speed


class Mouse:
    def __init__(self):
        self.x = 20
        self.y = 0
        self.speed = 0.5  # マウスの移動速度

    def move(self):
        # 矢印キーでマウスを動かす
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
        if pyxel.btn(pyxel.KEY_UP):
            self.y += self.speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y -= self.speed

        # 画面内に動きを制限する
        self.x = max(-WINDOW_WIDTH // 2, min(WINDOW_WIDTH // 2, self.x))
        self.y = max(-WINDOW_HEIGHT // 2, min(WINDOW_HEIGHT // 2, self.y))


def get_sprite_position(x, y):
    return WINDOW_WIDTH // 2 + x - 4, WINDOW_HEIGHT // 2 - y - 4


def draw_cursor():
    cursor_x = pyxel.mouse_x
    cursor_y = pyxel.mouse_y
    pyxel.blt(cursor_x - 4, cursor_y - 4, 0, 0, 16, 8, 8, 1)


class App:
    def __init__(self):
        self.cat = Cat()
        self.mouse = Mouse()
        self.game_started = False
        self.game_over = False

        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title='Cat Game')

        pyxel.load('my_resource.pyxres')

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

        # 衝突判定
        if abs(self.cat.x - self.mouse.x) < 4 and abs(self.cat.y - self.mouse.y) < 4:
            self.game_over = True

    def draw(self):
        pyxel.cls(1)

        if not self.game_started:
            pyxel.text(WINDOW_WIDTH // 2 - 26, WINDOW_HEIGHT // 2 - 8, "Click to start", pyxel.frame_count % 16)
            draw_cursor()  # カスタムカーソルの描画
            return

        if self.game_over:
            pyxel.text(WINDOW_WIDTH // 2 - 26, WINDOW_HEIGHT // 2 - 8, "Game Over!", pyxel.frame_count % 16)
            pyxel.text(WINDOW_WIDTH // 2 - 26, WINDOW_HEIGHT // 2 + 8, "Click to start", pyxel.frame_count % 16)
            draw_cursor()  # カスタムカーソルの描画
            return

        # スプライトを配置する
        cat_x, cat_y = get_sprite_position(self.cat.x, self.cat.y)
        pyxel.blt(cat_x, cat_y, 0, 0, 0, 8, 8, 1)

        mouse_x, mouse_y = get_sprite_position(self.mouse.x, self.mouse.y)
        pyxel.blt(mouse_x, mouse_y, 0, 0, 8, 8, 8, 1)

        if not self.game_started:
            draw_cursor()  # カスタムカーソルの描画

    def reset_game(self):
        self.cat = Cat()
        self.mouse = Mouse()
        self.game_started = True
        self.game_over = False


App()
