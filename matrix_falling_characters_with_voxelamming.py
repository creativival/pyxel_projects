# -*- coding: utf-8 -*-
# mtr.py

import pyxel
import numpy as np
from random import randint
# from voxelamming import Voxelamming
from voxelamming_local import Voxelamming  # ローカルで開発している場合はこちらを使う


class APP:
    # アルファベットのリスト（小文字と大文字）
    # alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ：：。。・・／／　　　　　"

    # ランダムなインデックスの配列を生成
    random_indices = np.random.randint(0, len(alphabet), (20, 20))  # 20行20列のランダムなインデックスの配列

    def __init__(self):
        self.w = 196
        self.x = 0
        self.y = -self.w
        self.pos_x = np.random.randint(0, self.w, (20, 1))
        self.pos_y = np.random.randint(0, 40, (20, 1))
        # インデックスをアルファベットにマッピングして文字列を生成
        self.random_strings = [[self.alphabet[idx] for idx in row] for row in self.random_indices]
        self.dot_size = 0.5
        self.window_angle = 80
        self.vox = Voxelamming('1000')
        self.send_data_num = 8  # 送信するデータの数を少しずつ増やしていく（クラッシュ防止）

        # ビットマップフォントの読み込み
        self.font = pyxel.Font("assets/misaki_mincho.bdf")
        self.font_size = 8
        # self.font = pyxel.Font("assets/umplus_j10r.bdf")
        # self.font_size = 10
        # self.font = pyxel.Font("assets/umplus_j12r.bdf")
        # self.font_size = 12

        # フォントを指定してテキスト表示
        pyxel.init(self.w, self.w, title="mtr", display_scale=6, fps=30)
        pyxel.mouse(False)
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)

        for i in range(int(self.send_data_num)):  # 複数箇所に文字列を配置する
            for ii in range(20):  # 縦方向に文字を繋げる
                c1 = randint(1, 20)
                if c1 == 1:
                    c = 11
                else:
                    c = 3

                x = self.x + self.pos_x[i][0]
                y = self.y + self.pos_y[i][0] + self.font_size * ii
                pyxel.text(x, y, str(self.random_strings[i][ii]), c, self.font)

        # # 30フレームごとに送信する
        # if pyxel.frame_count % 30 == 0:
        #     self.vox.set_box_size(self.dot_size)
        #     self.vox.set_game_screen(self.w, self.w, self.window_angle, red=1, green=1,
        #                              blue=1, alpha=0.1)
        #
        #     for i in range(int(self.send_data_num)):
        #         x = self.x + self.pos_x[i][0]
        #         y = self.y + self.pos_y[i][0]
        #         direction = 0
        #         scale = 3
        #         col = 11
        #         text = "".join(self.random_strings[i])  # 1行分の文字列を結合（20文字）
        #         vox_x, vox_y = self.convert_text_position_to_voxelamming(x, y, text, is_vertical=True)
        #         self.vox.display_text(text, vox_x, vox_y, direction, scale, col, is_vertical=True)
        #
        #     self.vox.send_data()
        #     self.vox.clear_data()

        self.y += 1
        if self.y > self.w:
            self.y = -self.w
            self.pos_x = np.random.randint(0, self.w, (20, 1))

    def convert_text_position_to_voxelamming(self, x, y, text, is_vertical=False):
        if is_vertical:
            width = 6  # Pyxelのフォントサイズ
            height = 6 * len(text)
        else:
            width = 6 * len(text)
            height = 6
        return x - self.w // 2 + width / 2, self.w // 2 - (y + height / 2)


APP()
