# https://note.com/koide_mizu1433/n/n1d86b2826583
import pyxel


# プレイヤーの弾クラス
class Bullet:
    def __init__(self, x, y):
        # ここでオブジェクト作成時の処理をします
        self.x = x
        self.y = y
        self.w = 3
        self.h = 3
        self.speed = 3

    def update(self):
        # 各オブジェクトが毎フレーム行う更新処理です
        self.y -= self.speed

    def draw(self):
        # 各オブジェクトが毎フレーム行う描画処理です
        pyxel.rect(self.x, self.y, self.w, self.h, 13)
        pyxel.rectb(self.x, self.y, self.w, self.h, 0)


class App:
    def __init__(self):
        # ここで起動時の処理をします
        pyxel.init(160, 250)
        pyxel.load('assets/sample03.pyxres')
        self.player_pos = [5, 200]
        self.speed = 2
        self.moving_flag = False
        self.bullets = []
        self.magazine = 5
        self.magazine_count = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        # ここで毎フレームの更新作業をします
        # 弾の装填部分######################
        self.magazine_count += 1
        if self.magazine_count > 30:
            self.magazine_count = 0
            if self.magazine < 5:
                self.magazine += 1

        # コントロール部分###################
        # 移動部分
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

        # 攻撃部分
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 斬弾がある場合は発射
            if self.magazine > 0:
                self.magazine -= 1
                self.bullets.append(Bullet(self.player_pos[0] + 8, self.player_pos[1]))

        # プレイヤーの弾の更新部分#########################
        for b in self.bullets:
            b.update()
            if b.y < 0:
                self.bullets.remove(b)

    def draw(self):
        # ここで毎フレームの描画作業をします
        pyxel.cls(1)
        # プレイヤーの描画
        if self.moving_flag == True:
            pyxel.blt(self.player_pos[0], self.player_pos[1], 0, 16, 0, 16, 16, 14)
        else:
            pyxel.blt(self.player_pos[0], self.player_pos[1], 0, 0, 0, 16, 16, 14)

        # 残弾表記部分の描画
        pyxel.rect(0, 228, 160, 22, 0)
        pyxel.rectb(0, 228, 160, 22, 7)
        for i in range(5):
            if i + 1 > self.magazine:
                pyxel.blt(5 + 8 * i, 232, 0, 0, 16, 8, 16, 14)
            else:
                pyxel.blt(5 + 8 * i, 232, 0, 8, 16, 8, 16, 14)

        # プレイヤーの弾の描画
        for b in self.bullets:
            b.draw()


App()
