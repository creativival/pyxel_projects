# -*- coding: utf-8 -*-
# mtr.py

import pyxel
import numpy as np
from random import randint


class APP:
    # アルファベットのリスト（小文字と大文字）
    # alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet = ("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデド"
                "バビブベボパピプペポ：：。。・・／／￥￥ーー　　　　　　　　　　　　　")

    def __init__(self):
        self.w = 196
        self.x = 0
        self.y = -self.w
        self.send_string_num = 20
        self.length_string = 20
        # ランダムなインデックスの配列を生成
        random_indices = np.random.randint(0, len(self.alphabet), (self.send_string_num, self.length_string))
        self.pos_x = np.random.randint(0, self.w, (self.send_string_num, 1))
        self.pos_y = np.random.randint(0, 40, (self.send_string_num, 1))
        # インデックスをアルファベットにマッピングして文字列を生成
        self.random_strings = [[self.alphabet[idx] for idx in row] for row in random_indices]
        # ビットマップフォントの読み込み
        self.font = pyxel.Font("assets/misaki_mincho.bdf")
        self.font_size = 8
        # self.font = pyxel.Font("assets/umplus_j10r.bdf")
        # self.font_size = 10
        # self.font = pyxel.Font("assets/umplus_j12r.bdf")
        # self.font_size = 12

        pyxel.init(self.w, self.w, title="mtr", display_scale=6, fps=30)
        pyxel.mouse(False)
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)

        for i in range(int(self.send_string_num)):  # 複数箇所に文字列を配置する
            for ii in range(self.length_string):  # 縦方向に文字を繋げる
                c1 = randint(1, 20)
                if c1 == 1:
                    c = 11
                else:
                    c = 3

                x = self.x + self.pos_x[i][0]
                y = self.y + self.pos_y[i][0] + self.font_size * ii
                # フォントを指定してテキスト表示
                pyxel.text(x, y, str(self.random_strings[i][ii]), c, self.font)

        self.y += 1
        if self.y > self.w:
            self.y = -self.w
            self.pos_x = np.random.randint(0, self.w, (self.send_string_num, 1))


APP()
