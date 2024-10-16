import pyxel
import random
import time
# from voxelamming import Voxelamming
from voxelamming_local import Voxelamming  # ローカルで開発している場合はこちらを使う


class Player:
    name = 'spaceship_8x8'
    dot_data = (
        '-1 -1 -1 8 8 -1 -1 -1 -1 -1 3 7 7 3 -1 -1 -1 -1 -1 7 7 -1 -1 -1 -1 -1 7 7 7 7 -1 -1 -1 7 7 7 7 7 7 -1 3 7'
        ' 7 7 7 7 7 3 -1 8 8 7 7 8 8 -1 -1 -1 -1 8 8 -1 -1 -1'
    )

    def __init__(self, x, y, speed):
        self.direction = 0
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
            x = self.x - self.speed
            self.x = max(0, x)
        if pyxel.btn(pyxel.KEY_RIGHT):
            x = self.x + self.speed
            self.x = min(pyxel.width - 8, x)


class Enemy:
    name = 'enemy_8x8'
    dot_data = (
        '-1 -1 3 -1 -1 3 -1 -1 -1 3 -1 3 3 -1 3 -1 3 -1 3 3 3 3 -1 3 3 3 3 3 3 3 3 3 3 3 -1 3 3 -1 3 3 3 3 3 3 3 3'
        ' 3 3 -1 3 3 -1 -1 3 3 -1 3 -1 -1 -1 -1 -1 -1 3'
    )

    def __init__(self, x, y):
        self.direction = 0
        self.x = x
        self.y = y
        self.img = 0
        self.u = 0
        self.v = 8
        self.w = 8
        self.h = 8

    @classmethod
    def create_enemies(cls, enemy_rows, enemy_cols):
        enemies = []
        for row in range(enemy_rows):
            for col in range(enemy_cols):
                enemy_x = col * 16 + 20
                enemy_y = row * 12 + 20
                enemy = Enemy(enemy_x, enemy_y)
                enemies.append(enemy)
        return enemies


class Missile:
    def __init__(self, x, y, color_id, direction=0, width=1, height=1):
        self.x = x
        self.y = y
        self.direction = direction
        self.color_id = color_id
        self.width = width
        self.height = height


class App:
    def __init__(self):
        # Pyxelの設定
        self.window_width = 160  # ARウインドウの横幅はself.dot_sizeを掛けた値になる（センチメートル）
        self.window_height = 120  # ARウインドウの縦幅はself.dot_sizeを掛けた値になる（センチメートル）
        self.score = 0
        self.game_over = False
        self.game_clear = False
        self.missile_shot_time = 0

        # プレイヤーの設定
        self.player = Player(self.window_width // 2, self.window_height - 10, 2)
        self.missiles = []
        self.player_missile_speed = 2

        # 敵の設定
        self.enemy_rows = 3
        self.enemy_cols = 6
        self.enemy_default_speed = 1
        self.enemy_direction = 1
        self.enemies = Enemy.create_enemies(self.enemy_rows, self.enemy_cols)
        self.enemy_missiles = []
        self.enemy_missile_speed = 2

        # ボクセラミングの設定（Pyxelの初期化の前に実行）
        self.dot_size = 1  # AR空間で表示されるスプライトのドットのサイズ（センチメートル）
        self.window_angle = 80  # ARウインドウの傾き（度）
        self.vox = Voxelamming('1000')
        self.init_voxelamming()

        # Pyxelの初期化
        pyxel.init(self.window_width, self.window_height, title="Pyxel Invader Game", fps=30)
        pyxel.mouse(True)
        pyxel.load("invader_game.pyxres")
        # BGMの再生
        pyxel.play(0, 0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over or self.game_clear:
            # カーソル表示
            pyxel.mouse(True)

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.reset_game()
            return

        # カーソルの非表示
        pyxel.mouse(False)

        # プレイヤーの操作
        self.player.update()

        if pyxel.btnp(pyxel.KEY_SPACE):
            if pyxel.frame_count - self.missile_shot_time > 15:
                self.missile_shot_time = pyxel.frame_count
                pyxel.play(1, 1)
                missile_x = self.player.x + self.player_missile_speed
                missile_y = self.player.y
                missile_clor_id = 10  # 青色
                missile_direction = 0
                missile_width = 2
                missile_height = 4
                self.missiles.append(
                    Missile(missile_x, missile_y, missile_clor_id, missile_direction, missile_width, missile_height))

        # ミサイルの移動
        for missile in self.missiles[:]:
            missile.y -= 2
            if missile.y < 0:
                self.missiles.remove(missile)

        # 敵の移動速度
        enemy_num = len(self.enemies)
        if enemy_num < 10:
            enemy_speed = 1.5 * self.enemy_default_speed
        else:
            enemy_speed = self.enemy_default_speed

        # 敵の移動
        move_down = False
        for enemy in self.enemies:
            enemy.x += enemy_speed * self.enemy_direction

        for enemy in self.enemies:
            if enemy.x > pyxel.width - 8 or enemy.x < 0:
                self.enemy_direction *= -1
                move_down = True
                break  # 端に到達したらすぐに方向を変える

        if move_down:
            for enemy in self.enemies:
                enemy.y += 8

                # 敵が画面下部に到達したらゲームオーバー
                if enemy.y > pyxel.height - 16:
                    self.game_over = True

        # 敵のミサイル発射
        if random.random() < 0.03 and self.enemies:
            shooting_enemy = random.choice(self.enemies)
            missile_x = shooting_enemy.x + 4
            missile_y = shooting_enemy.y + 8
            missile_clor_id = 8  # 赤色
            missile_direction = 0
            missile_width = 2
            missile_height = 4
            self.enemy_missiles.append(
                Missile(missile_x, missile_y, missile_clor_id, missile_direction, missile_width, missile_height))

        # 敵ミサイルの移動
        for missile in self.enemy_missiles[:]:
            missile.y += self.enemy_missile_speed
            if missile.y > pyxel.height * 2:
                self.enemy_missiles.remove(missile)

        # ミサイルと敵の衝突判定
        for missile in self.missiles[:]:
            for enemy in self.enemies[:]:
                if (enemy.x < missile.x < enemy.x + 16 and
                        enemy.y < missile.y < enemy.y + 12):
                    pyxel.play(2, 2)
                    self.missiles.remove(missile)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break

        # プレイヤーと敵ミサイルの衝突判定
        for missile in self.enemy_missiles[:]:
            if (self.player.x < missile.x < self.player.x + 8 and
                    self.player.y < missile.y < self.player.y + 8):
                pyxel.stop(0)
                pyxel.play(0, 4)
                self.game_over = True

        # プレイヤーと敵の衝突判定
        for enemy in self.enemies:
            if (self.player.x < enemy.x < self.player.x + 8 and
                    self.player.y < enemy.y < self.player.y + 8):
                pyxel.stop(0)
                pyxel.play(0, 4)
                self.game_over = True

        # ゲームクリア判定
        if not self.enemies:
            pyxel.stop(0)
            pyxel.play(0, 3)
            self.game_clear = True

        # ボクセラミングの更新
        self.update_voxelamming()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(5, 4, f"Score: {self.score}", 7)

        if self.game_clear:
            pyxel.text(pyxel.width // 2 - 20, pyxel.height // 2, "GAME CLEAR!", pyxel.frame_count % 16)
            pyxel.text(self.window_width // 2 - 26, self.window_height // 2 + 8, "Click to start",
                       pyxel.frame_count % 16)
        elif self.game_over:
            pyxel.text(pyxel.width // 2 - 20, pyxel.height // 2, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(self.window_width // 2 - 26, self.window_height // 2 + 8, "Click to start",
                       pyxel.frame_count % 16)
        else:
            # プレイヤーの描画
            pyxel.blt(self.player.x, self.player.y, self.player.img, self.player.u, self.player.v, self.player.w,
                      self.player.h, 0)

            # 敵の描画
            for enemy in self.enemies:
                pyxel.blt(enemy.x, enemy.y, enemy.img, enemy.u, enemy.v, enemy.w, enemy.h, 0)

            # ミサイルの描画
            for missile in self.missiles:
                pyxel.rect(missile.x, missile.y, missile.width, missile.height, missile.color_id)

            # 敵ミサイルの描画
            for missile in self.enemy_missiles:
                pyxel.rect(missile.x, missile.y, missile.width, missile.height, missile.color_id)

    def reset_game(self):
        self.score = 0  # スコアをリセット
        self.game_over = False
        self.game_clear = False

        # プレイヤーの設定
        self.player = Player(self.window_width // 2, self.window_height - 10, 2)
        self.missiles = []

        # 敵の設定
        self.enemy_direction = 1
        self.enemy_speed = 1
        self.enemies = Enemy.create_enemies(self.enemy_rows, self.enemy_cols)
        self.enemy_missiles = []

        # BGMの再生
        pyxel.play(0, 0, loop=True)

    def init_voxelamming(self):
        # ボクセラミングの初期化
        self.vox.set_box_size(self.dot_size)
        self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1, blue=0,
                                 alpha=0.8)
        self.vox.set_game_score(self.score, -64, 54)
        self.vox.set_command('liteRender')

        # プレイヤーのスプライトを作成
        self.vox.create_sprite(self.player.name, self.player.dot_data, visible=False)

        # 敵のスプライトを作成
        self.vox.create_sprite(Enemy.name, Enemy.dot_data, visible=False)

        self.vox.send_data()
        self.vox.clear_data()

    def update_voxelamming(self):
        # スプライトの情報を0.1秒ごとに送信
        if pyxel.frame_count % 3 == 0 or self.game_clear or self.game_over:  # PyxelのデフォルトFPSは30
            self.vox.set_box_size(self.dot_size)
            self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1,
                                     blue=0, alpha=0.5)
            self.vox.set_game_score(self.score, -64, 54)
            self.vox.set_command('liteRender')

            # スプライトの移動
            vox_x, vox_y = self.convert_position_to_voxelamming(self.player.x, self.player.y, self.player.w, self.player.h)
            self.vox.move_sprite(self.player.name, vox_x, vox_y, self.player.direction, 1)

            # 敵の移動はテンプレートを複数箇所に表示する
            for enemy in self.enemies:
                vox_x, vox_y = self.convert_position_to_voxelamming(enemy.x, enemy.y, enemy.w, enemy.h)
                self.vox.move_sprite_clone(enemy.name, vox_x, vox_y, enemy.direction, 1)

            # ミサイルはdotとして表示
            for missile in self.missiles + self.enemy_missiles:
                vox_x, vox_y = self.convert_position_to_voxelamming(missile.x, missile.y, missile.width, missile.height)
                self.vox.display_dot(vox_x, vox_y, missile.direction, missile.color_id, missile.width,
                                     missile.height)

            # ゲームクリアの表示と画面を青に変更
            if self.game_clear:
                self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=0, green=0,
                                         blue=1, alpha=0.8)
                self.vox.send_game_clear()

            # ゲームオーバーの表示と画面を赤に変更
            if self.game_over:
                self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=0,
                                         blue=0, alpha=0.8)
                self.vox.send_game_over()

            self.vox.send_data()

            # ゲームクリア、ゲームオーバー時に1秒待ってから再度データを送信
            if self.game_clear or self.game_over:
                time.sleep(1)
                self.vox.send_data()

            self.vox.clear_data()

    def convert_position_to_voxelamming(self, x, y, width=1, height=1):
        return x - self.window_width // 2 + width / 2, self.window_height // 2 - (y + height / 2)


if __name__ == "__main__":
    App()
