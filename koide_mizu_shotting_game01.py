# https://note.com/koide_mizu1433/n/n1d86b2826583
import pyxel


class App:
    def __init__(self):
        # ここで起動時の処理をします
        pyxel.init(160, 250)
        pyxel.load('assets/sample03.pyxres')
        self.player_pos = [5, 200]
        self.speed = 2
        self.moving_flag = False
        pyxel.run(self.update, self.draw)

    def update(self):
        # ここで毎フレームの更新作業をします
        # コントロール部分###################
        if pyxel.btn(pyxel.KEY_RIGHT):
            if self.player_pos[0] + self.speed < 160 - 16:
                self.player_pos[0] += self.speed
                self.moving_flag = True

        elif pyxel.btn(pyxel.KEY_LEFT):
            if self.player_pos[0] - self.speed > 0:
                self.player_pos[0] -= self.speed
                self.moving_flag = True

        else:
            self.moving_flag = False

    def draw(self):
        # ここで毎フレームの描画作業をします
        pyxel.cls(1)
        if self.moving_flag == True:
            pyxel.blt(self.player_pos[0], self.player_pos[1], 0, 16, 0, 16, 16, 14)
        else:
            pyxel.blt(self.player_pos[0], self.player_pos[1], 0, 0, 0, 16, 16, 14)


App()
