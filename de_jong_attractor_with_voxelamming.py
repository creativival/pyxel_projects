# Peter de Jong Attractor
import pyxel
from math import sin, cos
from random import choice, uniform
# from voxelamming import Voxelamming
from voxelamming_local import Voxelamming  # ローカルで開発している場合はこちらを使う


class App:
    w = 256  # screen size
    background_color = 0
    dot_color = [3, 6, 9, 10, 14]
    dot_count = 5000
    p_min, p_max = -3, 3

    def __init__(self):
        # ボクセラミングの初期化
        self.dot_size = 0.5  # AR空間で表示されるスプライトのドットのサイズ（センチメートル）
        self.window_angle = 80
        self.image_dots = []
        self.vox = Voxelamming('1000')

        # Pyxelの初期化
        pyxel.init(self.w, self.w, title='de jong attractor', fps=1)
        pyxel.run(self.update, self.draw)

    def draw(self):
        if pyxel.frame_count % 5 == 0:
            self.image_dots = []
            pyxel.cls(self.background_color)
            col = choice(self.dot_color)
            x, y = 0, 0
            a, b, c, d = [round(uniform(self.p_min, self.p_max), 2) for _ in range(4)]
            pyxel.text(10, 10, "a=" + str(a) + " b=" + str(b) + " c=" + str(c) + " d=" + str(d), 7)
            pyxel.text(10, 20, "Tap to send image to voxelamming", 7)
            for _ in range(self.dot_count):
                x, y = sin(a * y) - cos(b * x), sin(c * x) - cos(d * y)
                point_x = x * self.w / 5 + 128
                point_y = y * self.w / 5 + 128
                pyxel.pset(point_x, point_y, col)
                self.image_dots.append([point_x, point_y, col])

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.vox.set_box_size(self.dot_size)
            self.vox.set_game_screen(self.w, self.w, self.window_angle, red=1, green=1,
                                     blue=1, alpha=0.1)

            for dot in self.image_dots:
                x, y, col = dot
                vox_x, vox_y = self.convert_dot_position_to_voxelamming(x, y)
                self.vox.display_dot(vox_x, vox_y, 0, col)
            self.vox.send_data()
            self.vox.clear_data()

    def update(self):
        pass

    def convert_dot_position_to_voxelamming(self, x, y, height=1):
        return x - self.w // 2 + 0.5, self.w // 2 - (y + height / 2)


App()
