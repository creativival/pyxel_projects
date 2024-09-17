import pyxel
import time
# from voxelamming import Voxelamming
from voxelamming_local import Voxelamming  # ローカルで開発している場合はこちらを使う


class Player:
    name = 'mario_8x8'
    dot_data = (
        '-1 8 8 8 8 8 -1 -1 -1 8 8 8 8 8 8 -1 -1 4 4 15 4 15 -1 -1 -1 4 15 15 15 15 15 -1 -1 4 15 15 15 4 -1 -1 15 8 8 '
        '8 8 8 15 -1 -1 8 8 8 8 8 -1 -1 -1 4 4 -1 -1 4 4 -1'
    )

    def __init__(self):
        self.x = 10
        self.y = 80
        self.img = 0
        self.u = 0
        self.v = 0
        self.w = 8
        self.h = 8
        self.speed = 2
        self.jump_power = -4
        self.gravity = 0.2
        self.dy = 0
        self.on_ground = False
        self.x_direction = 1

    def update(self, blocks):
        # 左右移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
            self.x_direction = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
            self.x_direction = 1

        # ジャンプ
        if pyxel.btnp(pyxel.KEY_SPACE) and self.on_ground:
            self.dy = self.jump_power

        # 重力
        self.dy += self.gravity
        self.y += self.dy

        # 地面との接触判定（簡易的な実装）
        self.on_ground = False
        for block in blocks:
            if (self.x + self.w > block.x and self.x < block.x + block.w and
                    self.y + self.h > block.y and self.y < block.y + block.h):
                if self.dy > 0:  # 落下中のみ接触を検知
                    self.y = block.y - self.h
                    self.dy = 0
                    self.on_ground = True

    def draw(self, camera_x):
        w = self.w * self.x_direction
        pyxel.blt(self.x - camera_x, self.y, self.img, self.u, self.v, w, self.h, 0)  # プレイヤーの描画


class Enemy:
    name = 'goomba_8x8'
    dot_data = (
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 4 4 -1 -1 -1 -1 -1 4 4 4 4 -1 -1 -1 4 0 4 4 0 4 -1 -1 4 4 4 4 4 4 -1 -1 4 7 '
        '4 4 7 4 -1 -1 -1 15 15 15 15 -1 -1 -1 4 4 -1 -1 4 4 -1'
    )

    def __init__(self, x, y, distance):
        self.x = x
        self.y = y
        self.img = 0
        self.u = 0
        self.v = 8
        self.w = 8
        self.h = 8
        self.speed = 1
        self.visible = True
        self.start_x = x
        self.end_x = x + distance  # 移動範囲を追加

    def update(self):
        # 左右移動（簡易的に往復）
        self.x += self.speed
        if self.x < self.start_x or self.x > self.end_x:  # スクロールに対応して敵の範囲を修正
            self.speed *= -1

    def draw(self, camera_x):
        if self.visible:
            pyxel.blt(self.x - camera_x, self.y, self.img, self.u, self.v, self.w, self.h, 0)

    @classmethod
    def create_enemies(cls, positions):
        # ブロックを作成
        enemies = []
        for position in positions:
            enemies.append(cls(*position))
        return enemies


class Brick:
    name_16x16 = 'mario_blocks_16x16'
    dot_data_16x16 = (
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 7 7 7 7 7 7 7 7 7 7 7 7 '
        '7 7 7 7 13 13 13 13 13 13 0 7 13 13 13 13 13 13 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 '
        '4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 1 1 1 1 1 1 0 7 1 1 1 1 1 1 0 0 '
        '0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1'
    )
    name_32x32 = 'mario_blocks_32x32'
    dot_data_32x32 = (
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 '
        '7 7 7 7 7 7 7 7 7 7 7 7 7 7 13 13 13 13 13 1 0 7 13 13 13 13 13 1 0 7 13 13 13 13 13 1 0 7 13 13 13 13 13 1 0 '
        '7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 '
        '4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 '
        '0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 4 4 4 4 1 0 7 13 1 1 1 1 1 0 7 13 1 1 1 1 1 0 7 13 1 1 1 1 1 0 7 13 '
        '1 1 1 1 1 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 '
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1'
    )

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.img = 0
        self.u = 0
        self.v = 24
        self.w = w
        self.h = h

    def draw(self, camera_x):
        pyxel.blt(self.x - camera_x, self.y, self.img, self.u, self.v, self.w, self.h, 0)

    @classmethod
    def create_bricks(cls, positions):
        # ブロックを作成
        bricks = []
        for position in positions:
            bricks.append(cls(*position))
        return bricks


class Coin:
    name = 'coin_8x8'
    dot_data = (
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 10 10 10 10 -1 -1 -1 10 9 9 9 9 10 -1 -1 10 9 10 10 10 10 -1 -1 10 9 10 10 10 '
        '10 -1 -1 10 9 9 9 9 10 -1 -1 -1 10 10 10 10 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1'
    )

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = 0
        self.u = 0
        self.v = 16
        self.w = 8
        self.h = 8
        self.visible = True

    def draw(self, camera_x):
        if self.visible:
            pyxel.blt(self.x - camera_x, self.y, self.img, self.u, self.v, self.w, self.h, 0)

    @classmethod
    def create_coins(cls, positions):
        # コインを作成
        coins = []
        for position in positions:
            coins.append(cls(*position))
        return coins


class Flag:
    name = 'mario_flag_8x8'
    dot_data = (
        '7 7 7 7 7 7 7 7 7 7 11 11 11 11 11 7 7 7 11 7 11 7 11 7 7 7 11 7 11 7 11 7 7 7 11 11 11 11 11 7 7 7 7 7 7 7 7 '
        '7 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1'
    )

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.img = 0
        self.u = 0
        self.v = 32
        self.w = w
        self.h = h

    def draw(self, camera_x):
        pyxel.blt(self.x - camera_x, self.y, self.img, self.u, self.v, self.w, self.h)


class Game:
    def __init__(self):
        self.window_width = 160
        self.window_height = 120
        self.game_over = False
        self.game_clear = False  # ゲームクリアフラグ
        self.flag = Flag(464, 30, 8, 90)  # ゴールの旗を右端に配置
        self.camera_x = 0  # カメラの位置（スクロール）

        # インスタンスを作成
        self.player = Player()
        enemy_positions = [(40, 92, 90), (130, 92, 90)]
        self.enemies = Enemy.create_enemies(enemy_positions)
        block_positions = [(0, 100, 32, 8), (32, 100, 32, 8), (80, 100, 32, 8), (112, 100, 32, 8), (150, 100, 32, 8),
                           (182, 100, 32, 8), (240, 100, 32, 8), (300, 100, 32, 8)]
        self.blocks = Brick.create_bricks(block_positions)
        stair_positions = [(332, 92, 16, 8), (340, 84, 16, 8), (348, 76, 16, 8), (356, 68, 16, 8),
                           (364, 60, 16, 8)]
        self.stairs = Brick.create_bricks(stair_positions)
        coin_positions = [(60, 80), (120, 70), (180, 60)]
        self.coins = Coin.create_coins(coin_positions)

        # ボクセラミングの設定（Pyxelの初期化の前に実行）
        self.dot_size = 1  # AR空間で表示されるスプライトのドットのサイズ（センチメートル）
        self.window_angle = 80  # ARウインドウの傾き（度）
        self.vox = Voxelamming('1000')
        self.init_voxelamming()

        pyxel.init(self.window_width, self.window_height, title="Super Mario", fps=30)
        pyxel.load('super_mario.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over or self.game_clear:
            return

        self.player.update(self.blocks + self.stairs)
        for enemy in self.enemies:
            enemy.update()

        # カメラ（スクロール）の処理
        self.camera_x = max(0, min(self.player.x - 80,
                                   self.flag.x - pyxel.width + self.flag.w))  # フラッグの位置までスクロール

        # コインブロックとの接触判定
        for coin in self.coins:
            if coin.visible and (self.player.x + self.player.w > coin.x and
                    self.player.x < coin.x + coin.w and
                    self.player.y + self.player.h > coin.y and
                    self.player.y < coin.y + coin.h):
                coin.visible = False

        # 敵キャラとの衝突判定
        for enemy in self.enemies:
            if enemy.visible and (self.player.x + self.player.w > enemy.x and
                    self.player.x < enemy.x + enemy.w and
                    self.player.y + self.player.h > enemy.y and
                    self.player.y < enemy.y + enemy.h):

                # 上から接触した場合（プレイヤーの底部が敵の上部に接触）
                if self.player.dy > 0 and self.player.y + self.player.h - 1 < enemy.y:
                    # 敵をやっつける
                    enemy.visible = False
                    self.player.dy = -2  # ジャンプしたようにプレイヤーが跳ね返る
                else:
                    # 横や下から接触した場合はゲームオーバー
                    self.game_over = True

        # プレイヤーがフラッグに大ジャンプして到達した場合
        if (self.player.x + self.player.w > self.flag.x and
                self.player.y < self.flag.y + self.flag.h):
            self.game_clear = True  # フラッグに捕まったらゲームクリア

        # プレイヤーが画面の高さを超えたらゲームオーバー
        if self.player.y > pyxel.height:
            self.game_over = True

        # ボクセラミングの更新
        self.update_voxelamming()

    def draw(self):
        pyxel.cls(0)

        # プレイヤーの描画
        self.player.draw(self.camera_x)

        # 敵キャラの描画
        for enemy in self.enemies:
            enemy.draw(self.camera_x)

        # ブロックの描画
        for block in self.blocks:
            block.draw(self.camera_x)

        # 階段の描画
        for block in self.stairs:
            block.draw(self.camera_x)

        # コインブロックの描画
        for coin in self.coins:
            coin.draw(self.camera_x)

        # ゴールの旗の描画
        self.flag.draw(self.camera_x)

        # ゲームオーバー時の表示
        if self.game_over:
            pyxel.text(62, 60, "GAME OVER", pyxel.frame_count % 16)

        # ゲームクリア時の表示
        if self.game_clear:
            pyxel.text(62, 60, "YOU WIN!", pyxel.frame_count % 16)

    def init_voxelamming(self):
        # ボクセラミングの初期化
        self.vox.set_box_size(self.dot_size)
        self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1, blue=0,
                                 alpha=0.8)
        self.vox.set_command('liteRender')

        # プレイヤーのスプライトを表示
        self.vox.create_sprite(self.player.name, self.player.dot_data, visible=False)

        # 敵のスプライトを作成
        self.vox.create_sprite(Enemy.name, Enemy.dot_data, visible=False)

        # bricksのスプライトを作成
        self.vox.create_sprite(Brick.name_16x16, Brick.dot_data_16x16, visible=False)
        self.vox.create_sprite(Brick.name_32x32, Brick.dot_data_32x32, visible=False)

        # コインのスプライトを作成
        self.vox.create_sprite(Coin.name, Coin.dot_data, visible=False)

        # フラッグのスプライトを作成
        self.vox.create_sprite(Flag.name, Flag.dot_data, visible=False)

        self.vox.send_data()
        self.vox.clear_data()

    def update_voxelamming(self):
        # スプライトの情報を0.1秒ごとに送信
        if pyxel.frame_count % 3 == 0 or self.game_clear or self.game_over:  # PyxelのデフォルトFPSは30
            self.vox.set_box_size(self.dot_size)
            self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1,
                                     blue=0, alpha=0.5)
            self.vox.set_command('liteRender')

            # プレイヤーのスプライトの移動
            vox_x, vox_y = self.convert_position_to_voxelamming(
                self.player.x, self.player.y, self.player.w, self.player.h)

            if self.player.x_direction == -1:
                self.vox.move_sprite(self.player.name, vox_x, vox_y, -180, 1)
            else:
                self.vox.move_sprite(self.player.name, vox_x, vox_y, 0, 1)

            # 敵のスプライトを移動
            for enemy in self.enemies:
                if enemy.visible and (-20 < enemy.x - self.camera_x < pyxel.width):
                    vox_x, vox_y = self.convert_position_to_voxelamming(
                        enemy.x, enemy.y, enemy.w, enemy.h)
                    self.vox.move_sprite(enemy.name, vox_x, vox_y, 0, 1)

            # blocksの移動はテンプレートを複数箇所に表示する
            for brick in self.blocks:
                if -20 < brick.x - self.camera_x < pyxel.width:
                    vox_x, vox_y = self.convert_position_to_voxelamming(
                        brick.x, brick.y, brick.w, brick.h)
                    self.vox.move_sprite(brick.name_32x32, vox_x, vox_y, 0, 1)

            # stairsの移動はテンプレートを複数箇所に表示する
            for brick in self.stairs:
                if -20 < brick.x - self.camera_x < pyxel.width:
                    vox_x, vox_y = self.convert_position_to_voxelamming(
                        brick.x, brick.y, brick.w, brick.h)
                    self.vox.move_sprite(brick.name_16x16, vox_x, vox_y, 0, 1)

            # コインのスプライトを移動
            for coin in self.coins:
                if coin.visible and (-20 < coin.x - self.camera_x < pyxel.width):
                    vox_x, vox_y = self.convert_position_to_voxelamming(
                        coin.x, coin.y, coin.w, coin.h)
                    self.vox.move_sprite(coin.name, vox_x, vox_y, 0, 1)

            # フラッグのスプライトの移動
            if -20 < self.flag.x - self.camera_x < pyxel.width:
                # フラッグ
                flag_vox_x, flag_vox_y = self.convert_position_to_voxelamming(
                    self.flag.x, self.flag.y, self.flag.w, 8)
                self.vox.move_sprite(self.flag.name, flag_vox_x, flag_vox_y, 0, 1)

                # 支柱
                pole_vox_x, pole_vox_y = self.convert_position_to_voxelamming(
                    self.flag.x, self.flag.y, 1, self.flag.h)
                self.vox.display_dot(pole_vox_x, pole_vox_y, 0, 11, 1, self.flag.h)

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
        x = x - self.camera_x
        return x - self.window_width // 2 + width // 2, self.window_height // 2 - (y + height // 2)


# ゲームの実行
Game()
