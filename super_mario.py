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

    def update(self, blocks):
        # 左右移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed

        # ジャンプ
        if pyxel.btnp(pyxel.KEY_SPACE) and self.on_ground:
            self.dy = self.jump_power

        # 重力
        self.dy += self.gravity
        self.y += self.dy

        # 地面との接触判定（簡易的な実装）
        self.on_ground = False
        for block in blocks:
            if (self.x + self.w > block[0] and self.x < block[0] + block[2] and
                    self.y + self.h > block[1] and self.y < block[1] + block[3]):
                if self.dy > 0:  # 落下中のみ接触を検知
                    self.y = block[1] - self.h
                    self.dy = 0
                    self.on_ground = True

    def draw(self, camera_x):
        pyxel.blt(self.x - camera_x, self.y, self.img, self.u, self.v, self.w, self.h)  # プレイヤーの描画


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = 0
        self.u = 0
        self.v = 8
        self.w = 8
        self.h = 8
        self.speed = 1

    def update(self):
        # 左右移動（簡易的に往復）
        self.x += self.speed
        if self.x < 40 or self.x > 220:  # スクロールに対応して敵の範囲を修正
            self.speed *= -1

    def draw(self, camera_x):
        pyxel.blt(self.x - camera_x, self.y, self.img, self.u, self.v, self.w, self.h)  # 敵キャラの描画


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


class Game:
    def __init__(self):
        pyxel.init(160, 120, title="Super Mario", fps=30)
        self.player = Player()
        self.enemy = Enemy(100, 92)  # 敵キャラクターの位置を修正
        self.blocks = [(0, 100, 40, 8), (60, 100, 40, 8), (120, 100, 40, 8), (180, 100, 40, 8), (240, 100, 40, 8),
                       (300, 100, 40, 8)]  # ステージをさらに伸ばす
        self.stairs = [(332, 92, 16, 8), (340, 84, 16, 8), (348, 76, 16, 8), (356, 68, 16, 8),
                       (364, 62, 16, 8)]  # 階段のブロック
        self.coin_block_positions = [(60, 80)]  # コインブロックの位置
        self.coin_blocks = []  # コインブロック
        self.coin_collected = False
        self.game_over = False
        self.game_clear = False  # ゲームクリアフラグ
        self.goal_flag = (464, 30, 8, 100)  # ゴールの旗を右端に配置
        self.camera_x = 0  # カメラの位置（スクロール）

        for position in self.coin_block_positions:
            self.coin_blocks.append(Coin(position[0], position[1]))

        pyxel.load('super_mario.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over or self.game_clear:
            return

        self.player.update(self.blocks + self.stairs)
        self.enemy.update()

        # カメラ（スクロール）の処理
        self.camera_x = max(0, min(self.player.x - 80,
                                   self.goal_flag[0] - pyxel.width + self.goal_flag[2]))  # フラッグの位置までスクロール

        # # コインブロックとの接触判定
        # if not self.coin_collected and (
        #         self.player.x + self.player.w > self.coin_block[0] and
        #         self.player.x < self.coin_block[0] + self.coin_block[2] and
        #         self.player.y + self.player.h > self.coin_block[1] and
        #         self.player.y < self.coin_block[1] + self.coin_block[3]):
        #     self.coin_collected = True

        # 敵キャラとの衝突判定
        if (self.player.x + self.player.w > self.enemy.x and
                self.player.x < self.enemy.x + self.enemy.w and
                self.player.y + self.player.h > self.enemy.y and
                self.player.y < self.enemy.y + self.enemy.h):
            self.game_over = True

        # プレイヤーがフラッグに大ジャンプして到達した場合
        if (self.player.x + self.player.w > self.goal_flag[0] and
                self.player.y < self.goal_flag[1] + self.goal_flag[3]):
            self.game_clear = True  # フラッグに捕まったらゲームクリア

        # プレイヤーが画面の高さを超えたらゲームオーバー
        if self.player.y > pyxel.height:
            self.game_over = True

    def draw(self):
        pyxel.cls(0)

        # プレイヤーの描画
        self.player.draw(self.camera_x)

        # 敵キャラの描画
        self.enemy.draw(self.camera_x)

        # ブロックの描画
        for block in self.blocks:
            pyxel.rect(block[0] - self.camera_x, block[1], block[2], block[3], 7)

        # 階段の描画
        for step in self.stairs:
            pyxel.rect(step[0] - self.camera_x, step[1], step[2], step[3], 7)

        # コインブロックの描画
        for coin in self.coin_blocks:
            if coin.visible:
                pyxel.blt(coin.x - self.camera_x, coin.y, coin.img, coin.u, coin.v, coin.w, coin.h)

        # ゴールの旗の描画
        pyxel.rect(self.goal_flag[0] - self.camera_x, self.goal_flag[1], self.goal_flag[2], self.goal_flag[3], 11)

        # ゲームオーバー時の表示
        if self.game_over:
            pyxel.text(50, 60, "GAME OVER", pyxel.frame_count % 16)

        # ゲームクリア時の表示
        if self.game_clear:
            pyxel.text(50, 60, "YOU WIN!", pyxel.frame_count % 16)


# ゲームの実行
Game()
