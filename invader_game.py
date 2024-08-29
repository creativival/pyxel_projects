import pyxel
import random


class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.img = 0
        self.u = 0
        self.v = 0
        self.w = 8
        self.h = 8
        self.speed = speed

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = 0
        self.u = 0
        self.v = 8
        self.w = 8
        self.h = 8


class Bullet:
    def __init__(self, x, y, color_id):
        self.x = x
        self.y = y
        self.color_id = color_id


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Invader Game", fps=30)
        pyxel.load("invader_game.pyxres")

        # プレイヤーの設定
        self.player = Player(pyxel.width // 2, pyxel.height - 10, 2)
        self.missiles = []

        # 敵の設定
        self.enemy_rows = 3
        self.enemy_cols = 6
        self.enemy_speed = 1
        self.enemy_direction = 1
        self.enemies = []
        self.enemy_missiles = []
        self.enemy_missile_speed = 2

        # 敵の初期化
        for row in range(self.enemy_rows):
            for col in range(self.enemy_cols):

                enemy_x = col * 16 + 20
                enemy_y = row * 12 + 20
                self.enemies.append([enemy_x, enemy_y])

        self.running = True
        self.score = 0
        self.game_clear = False
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.running:
            return

        # プレイヤーの操作
        self.player.update()

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.missiles.append([self.player.x + 3, self.player.y])

        # ミサイルの移動
        for missile in self.missiles[:]:
            missile[1] -= 2
            if missile[1] < 0:
                self.missiles.remove(missile)

        # 敵の移動
        move_down = False
        for enemy in self.enemies:
            enemy[0] += self.enemy_speed * self.enemy_direction
            if enemy[0] > pyxel.width - 16 or enemy[0] < 0:
                self.enemy_direction *= -1
                move_down = True

        if move_down:
            for enemy in self.enemies:
                enemy[1] += 8

        # 敵のミサイル発射
        if random.random() < 0.02 and self.enemies:
            shooting_enemy = random.choice(self.enemies)
            self.enemy_missiles.append([shooting_enemy[0] + 4, shooting_enemy[1] + 8])

        # 敵ミサイルの移動
        for missile in self.enemy_missiles[:]:
            missile[1] += self.enemy_missile_speed
            if missile[1] > pyxel.height:
                self.enemy_missiles.remove(missile)

        # ミサイルと敵の衝突判定
        for missile in self.missiles[:]:
            for enemy in self.enemies[:]:
                if (enemy[0] < missile[0] < enemy[0] + 16 and
                        enemy[1] < missile[1] < enemy[1] + 12):
                    self.missiles.remove(missile)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break

        # プレイヤーと敵ミサイルの衝突判定
        for missile in self.enemy_missiles[:]:
            if (self.player.x < missile[0] < self.player.x + 8 and
                    self.player.y < missile[1] < self.player.y + 8):
                self.running = False

        # プレイヤーと敵の衝突判定
        for enemy in self.enemies:
            if (self.player.x < enemy[0] < self.player.x + 8 and
                    self.player.y < enemy[1] < self.player.y + 8):
                self.running = False

        # ゲームクリア判定
        if not self.enemies:
            self.game_clear = True

    def draw(self):
        pyxel.cls(0)
        pyxel.text(5, 4, f"Score: {self.score}", 7)

        if self.game_clear:
            pyxel.text(pyxel.width // 2 - 20, pyxel.height // 2, "GAME CLEAR!", pyxel.frame_count % 16)
        elif not self.running:
            pyxel.text(pyxel.width // 2 - 20, pyxel.height // 2, "GAME OVER", pyxel.frame_count % 16)
        else:

            # プレイヤーの描画
            pyxel.blt(self.player.x, self.player.y, 0, 0, 0, 8, 8, 0)

            # ミサイルの描画
            for missile in self.missiles:
                pyxel.rect(missile[0], missile[1], 2, 4, 10)

            # 敵の描画
            for enemy in self.enemies:
                pyxel.blt(enemy[0], enemy[1], 0, 0, 8, 8, 8, 0)

            # 敵ミサイルの描画
            for missile in self.enemy_missiles:
                pyxel.rect(missile[0], missile[1], 2, 4, 8)


if __name__ == "__main__":
    App()
