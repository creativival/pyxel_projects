import pyxel


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
        self.enemys = []
        self.game_over = False
        pyxel.run(self.update, self.draw)

    def update(self):
        # ここで毎フレームの更新作業をします
        # 敵の作成部分
        if pyxel.frame_count % pyxel.rndi(120, 240) == 0:
            new_enemy_count = pyxel.rndi(1, 3)
            for nw in range(new_enemy_count):
                self.enemys.append(Enemy())

        # 弾の装填部分######################
        self.magazine_count += 1
        if self.magazine_count > 30:
            self.magazine_count = 0
            if self.magazine < 5:
                self.magazine += 1

        # コントロール部分###################
        # 移動部分
        if self.game_over == True:
            if pyxel.btn(pyxel.KEY_SPACE):
                self.enemys = []
                self.bullets = []
                self.game_over = False
        else:
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
                # 残弾がある場合は発射
                if self.magazine > 0:
                    self.magazine -= 1
                    self.bullets.append(Bullet(self.player_pos[0] + 8, self.player_pos[1], 1))

        # 弾の更新部分#########################
        for b in self.bullets:
            self.game_over = b.update(self.player_pos, self.enemys, self.game_over)
            if b.y < 0 or b.y > 250:
                self.bullets.remove(b)
        # 敵の更新部分
        for e in self.enemys:
            if e.update() == True:
                self.bullets.append(Bullet(e.x + 8, e.y, 2))

            if e.t == 1:
                if e.x > 160:
                    self.enemys.remove(e)
            elif e.t == 2:
                if e.x < -16:
                    self.enemys.remove(e)

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

        # 敵の描画
        for e in self.enemys:
            e.draw()

        # ゲームオーバー表記
        if self.game_over == True:
            pyxel.text(20, 50, "GAME OVER!!", 0)
            pyxel.text(21, 51, "GAME OVER!!", 7)
            pyxel.text(20, 70, "PLEASE HIT SPACE-KEY", 0)
            pyxel.text(21, 71, "PLEASE HIT SPACE-KEY", 7)


# 弾クラス
class Bullet:
    def __init__(self, x, y, t):
        # ここでオブジェクト作成時の処理をします
        self.x = x
        self.y = y
        self.w = 3
        self.h = 3
        self.speed = 3
        self.t = t

    def update(self, p, es, g):
        # 各オブジェクトが毎フレーム行う更新処理です
        if self.t == 1:
            self.y -= self.speed
            for e in es:
                if self.x > e.x and self.x < e.x + 16:
                    if self.y > e.y and self.y < e.y + 16:
                        es.remove(e)

        elif self.t == 2:
            self.y += self.speed
            if self.x > p[0] and self.x < p[0] + 16:
                if self.y > p[1] and self.y < p[1] + 16:
                    g = True
                    return g
        return g

    def draw(self):
        # 各オブジェクトが毎フレーム行う描画処理です
        pyxel.rect(self.x, self.y, self.w, self.h, 13)
        pyxel.rectb(self.x, self.y, self.w, self.h, 0)


# 敵クラス
class Enemy:
    def __init__(self):
        # ここでオブジェクト作成時の処理をします
        self.t = pyxel.rndi(1, 2)
        if self.t == 1:
            self.x = pyxel.rndi(-60, -16)
        elif self.t == 2:
            self.x = pyxel.rndi(180, 240)
        self.y = pyxel.rndi(16, 150)
        self.speed = pyxel.rndi(1, 2)

    def update(self):
        # 各オブジェクトが毎フレーム行う更新処理です
        if self.t == 1:
            self.x += self.speed
        elif self.t == 2:
            self.x -= self.speed

        if pyxel.frame_count % pyxel.rndi(30, 90) == 0:
            return True

    def draw(self):
        # 各オブジェクトが毎フレーム行う描画処理です
        if self.t == 1:
            pyxel.blt(self.x, self.y, 0, 0, 48, 16, 16, 14)
        elif self.t == 2:
            pyxel.blt(self.x, self.y, 0, 0, 32, 16, 16, 14)


App()
