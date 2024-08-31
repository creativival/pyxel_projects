# Peter de Jong Attractor
import pyxel
from math import sin, cos
from random import choice, uniform


class App:
    w = 256  # screen size
    background_color = 0
    dot_color = [3, 6, 9, 10, 14]
    dot_count = 20000
    p_min, p_max = -3, 3

    def __init__(self):
        # Pyxelの初期化
        pyxel.init(self.w, self.w, title='de jong attractor', fps=1)
        pyxel.run(self.update, self.draw)

    def draw(self):
        pyxel.cls(self.background_color)
        col = choice(self.dot_color)
        x, y = 0, 0
        a, b, c, d = [round(uniform(self.p_min, self.p_max), 2) for _ in range(4)]
        pyxel.text(10, 10, "a=" + str(a) + " b=" + str(b) + " c=" + str(c) + " d=" + str(d), 7)
        for _ in range(self.dot_count):
            x, y = sin(a * y) - cos(b * x), sin(c * x) - cos(d * y)
            pyxel.pset(x * self.w / 5 + 128, y * self.w / 5 + 128, col)

    def update(self):
        pass


App()
