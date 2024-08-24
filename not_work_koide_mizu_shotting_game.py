from random import randint
import pyxel

WINDOW_H = 120
WINDOW_W = 160
SHIP_H = 16
SHIP_W = 16


class APP:
    def __init__(self):
        self.IMG_ID0 = 0
        self.IMG_ID1 = 1
        self.IMG_ID0_X = 60
        self.IMG_ID0_Y = 65
        self.game_over = False
        self.game_end = False
        self.boss_flug = False
        self.boss_count = 1
        self.score = 0
        self.shots = []
        self.enemys = []
        self.boss_hp = 500
        self.bombs = []
        self.p_ship = Ship()

        pyxel.init(WINDOW_W, WINDOW_H, title="Hello Pyxel")
        # ドット絵を読み込む
        pyxel.load("assets/sample03.pyxres")

        pyxel.mouse(False)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # 自機の更新
        if self.game_over == False:
            self.p_ship.update(pyxel.mouse_x, pyxel.mouse_y)

        shot_count = len(self.shots)
        for j in range(shot_count):
            if self.shots[j].pos_y > 10:
                self.shots[j].pos_y = self.shots[j].pos_y - 3
            else:
                del self.shots[j]
                break
            # 当たり判定
            # 敵と弾
            shot_hit = len(self.shots)
            for h in range(shot_hit):
                enemy_hit = len(self.enemys)
                for e in range(enemy_hit):
                    if ((self.enemys[e].ene_x <= self.shots[h].pos_x
                         <= self.enemys[e].ene_x + 20) and (self.enemys[e].ene_y
                                                            <= self.shots[h].pos_y <= self.enemys[e].ene_y + 20)):
                        # 敵に当たったらその座標に爆発を乗せる
                        new_bomb = Bomb(self.enemys[e].ene_x,
                                        self.enemys[e].ene_y)
                        self.bombs.append(new_bomb)
                        del self.enemys[e]
                        if self.boss_flug == False:
                            self.score = self.score + 100
                        break  # 敵に当たったらbreak
                else:
                    continue
                break  # 敵に当たったらbreak

        # 敵と自機
        enemy_atk = len(self.enemys)
        for e in range(enemy_atk):
            if (((self.enemys[e].ene_x >= self.p_ship.ship_x) and
                 (self.enemys[e].ene_x <= self.p_ship.ship_x + 15) and
                 (self.enemys[e].ene_y >= self.p_ship.ship_y) and
                 (self.enemys[e].ene_y <= self.p_ship.ship_y + 15)) or
                    ((self.enemys[e].ene_x + 15 >= self.p_ship.ship_x) and
                     (self.enemys[e].ene_x + 15 <= self.p_ship.ship_x + 15) and
                     (self.enemys[e].ene_y + 15 >= self.p_ship.ship_y) and
                     (self.enemys[e].ene_y + 15 <= self.p_ship.ship_y + 15))):
                self.game_over = True
                new_bomb = Bomb(self.p_ship.ship_x, self.p_ship.ship_y)
                self.bombs.append(new_bomb)

                # enemy update
        if self.game_end == False:
            if self.boss_flug == False:
                if pyxel.frame_count % 20 == 0:
                    new_enemy = Enemy()
                    self.enemys.append(new_enemy)
            else:
                if pyxel.frame_count % 8 == 0:
                    new_enemy = Enemy()
                    self.enemys.append(new_enemy)

        enemy_count = len(self.enemys)
        for e in range(enemy_count):
            enemy_vec1 = randint(0, 7)
            enemy_vec2 = enemy_vec1 % 2
            if self.enemys[e].ene_y < 115:
                if enemy_vec2 > 0:
                    self.enemys[e].ene_x = self.enemys[e].ene_x + 4
                    self.enemys[e].ene_y = self.enemys[e].ene_y + 1.5
                else:
                    self.enemys[e].ene_x = self.enemys[e].ene_x - 4
                    self.enemys[e].ene_y = self.enemys[e].ene_y + 1.5

            else:
                del self.enemys[e]
                break

        # 画面の爆発が3以上になったら古いものから消していく
        if len(self.bombs) > 3:
            del self.bombs[0]

            # ボス出現フラグ
        if self.boss_flug == False:  # ボス未出現の状態で
            if self.score != 0:  # ゲーム開始直後ではなく
                if self.score % 2000 == 0:  # スコアxxxx点に達したら
                    if self.game_end == False:  # ゲームクリアフラグがない場合にボス発生
                        self.boss_flug = True
                        self.boss_hp = 200 * self.boss_count
        # ボスの当たり判定
        if self.boss_flug == True:
            shot_hit = len(self.shots)
            for h in range(shot_hit):
                if ((70 <= self.shots[h].pos_x <= 85) and
                        (10 <= self.shots[h].pos_y <= 20)):
                    self.boss_hp = self.boss_hp - 1
                    new_bomb = Bomb(self.shots[h].pos_x, self.shots[h].pos_y)
                    self.bombs.append(new_bomb)
                    # ボス消滅
        if self.boss_hp <= 0:
            if self.boss_flug == True:
                self.score = self.score + 5000
                pyxel.cls(0)
                self.boss_flug = False
                # self.game_end = True
                self.boss_count = self.boss_count + 1

    def draw(self):
        pyxel.cls(0)

        # ゲームオーバー
        if self.game_over:
            pyxel.text(60, 40, "Game Over!", pyxel.frame_count % 16)

        # ゲームクリア
        if self.game_end:
            pyxel.text(60, 40, "Completed!", pyxel.frame_count % 16)

        # 得点描写
        pyxel.text(1, 2, "score:" + str(self.score), pyxel.frame_count % 16)
        pyxel.text(120, 2, "boss:" + str(self.boss_hp), pyxel.frame_count % 16)

        # 宇宙船の描画
        pyxel.blt(self.p_ship.ship_x, self.p_ship.ship_y, 0, 0, 0,
                  -SHIP_W, SHIP_H, 15)
        # SPACEが押された際に発射する
        if self.game_over == False:
            if pyxel.btn(pyxel.KEY_SPACE):
                if len(self.shots) < 11:
                    # make shot instance
                    new_shot = Shot()
                    new_shot.update(self.p_ship.ship_x, self.p_ship.ship_y, 8)
                    self.shots.append(new_shot)

        # 弾の描画
        for i in self.shots:
            pyxel.rect(i.pos_x + 7, i.pos_y - 3,
                       i.pos_x + 7, i.pos_y + 0.5, 8)

        # 敵の描画
        for i in self.enemys:
            if self.boss_flug == False:
                enemy_flug = randint(0, 7)
                if enemy_flug % 2 == 0:
                    pyxel.blt(i.ene_x, i.ene_y, 1, 0, 0,
                              -SHIP_W, SHIP_H, 15)
                else:
                    pyxel.blt(i.ene_x, i.ene_y, 1, 16, 0,
                              -SHIP_W, SHIP_H, 15)
            else:
                enemy_flug = randint(0, 7)
                if enemy_flug % 2 == 0:
                    pyxel.blt(i.ene_x, i.ene_y, 1, 0, 32,
                              -SHIP_W, SHIP_H, 15)
                else:
                    pyxel.blt(i.ene_x, i.ene_y, 1, 16, 32,
                              -SHIP_W, SHIP_H, 15)

        # ボスの描画
        if self.boss_flug == True:
            pyxel.blt(50, 10, 1, 0, 16, 63, 16, 15)
            pyxel.blt(95, 25, 1, 32, 32, -SHIP_W, SHIP_H, 15)
            pyxel.blt(85, 25, 1, 32, 32, SHIP_W, SHIP_H, 15)
            pyxel.blt(72, 25, 1, 32, 32, SHIP_W, SHIP_H, 15)
            pyxel.blt(64, 25, 1, 32, 32, -SHIP_W, SHIP_H, 15)
            pyxel.blt(51, 25, 1, 32, 32, SHIP_W, SHIP_H, 15)

        # 爆発の描写
        for i in self.bombs:
            pyxel.blt(i.bomb_x, i.bomb_y, 2, 0, 0,
                      -SHIP_W, SHIP_H, 15)

        # オブジェクトのクラス


class Ship:
    def __init__(self):
        self.ship_x = 0
        self.ship_y = 0

    def update(self, x, y):
        self.ship_x = x
        self.ship_y = y


class Shot:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.color = 8  # 0~15

    def update(self, x, y, color):
        self.pos_x = x
        self.pos_y = y
        self.color = color


class Enemy:
    def __init__(self):
        self.ene_x = randint(30, 125)
        self.ene_y = 5

    def update(self, x, y):
        self.ene_x = x
        self.ene_y = y


class Bomb:
    def __init__(self, x, y):
        self.bomb_x = x
        self.bomb_y = y


APP()