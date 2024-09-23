import pyxel


class Player:
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


# ゲームの実行
Game()
