import pyxel
import random

# プレイヤークラス
class Player:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.x = window_width // 2
        self.y = window_height // 2
        self.img = 0
        self.u = 0
        self.v = 0
        self.w = 8
        self.h = 8
        self.hp = 20
        self.attack = 5
        self.y_direction = 1

    def update(self):
        # 移動操作
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(0, self.x - 2)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(pyxel.width - self.w, self.x + 2)
        if pyxel.btn(pyxel.KEY_UP):
            self.y = max(0, self.y - 2)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y = min(pyxel.height - self.h, self.y + 2)

    def draw(self):
        # プレイヤーの描画
        print(self.x, self.y)
        pyxel.blt(self.window_width // 2, self.window_height // 2, self.img, self.u, self.v, self.w, self.h, 0)


# スライムクラス（敵）
class Slime:
    def __init__(self, player, window_width, window_height):
        self.player = player
        self.window_width = window_width
        self.window_height = window_height
        self.x = random.randint(10, window_width - 10)
        self.y = random.randint(10, window_height - 10)
        self.img = 0
        self.u = 0
        self.v = 8
        self.w = 8
        self.h = 8
        self.hp = 10
        self.attack = 2
        self.visible = True

    def draw(self):
        if self.visible:
            # スライムの描画
            x = self.x - self.player.x + self.window_width // 2
            y = self.y - self.player.y + self.window_height // 2
            pyxel.blt(x, y, self.img, self.u, self.v, self.w, self.h, 0)


# 樹木クラス（障害物）
class Tree:
    def __init__(self, player, window_width, window_height):
        self.player = player
        self.window_width = window_width
        self.window_height = window_height
        self.x = random.randint(10, window_width - 10)
        self.y = random.randint(10, window_height - 10)
        self.img = 0
        self.u = 0
        self.v = 16
        self.w = 8
        self.h = 8

    def draw(self):
        x = self.x - self.player.x + self.window_width // 2
        y = self.y - self.player.y + self.window_height // 2
        pyxel.blt(x, y, self.img, self.u, self.v, self.w, self.h, 0)


# ゲームクラス
class Game:
    def __init__(self):
        self.window_width = 160
        self.window_height = 120
        self.player = Player(self.window_width, self.window_height)
        self.slimes = [Slime(self.player, self.window_width, self.window_height) for _ in range(3)]  # 3匹のスライムをランダムに配置
        self.trees = [Tree(self.player, self.window_width, self.window_height) for _ in range(10)]  # 樹木を10本ランダムに配置
        self.in_battle = False
        self.current_slime = None  # 現在戦闘中のスライム
        self.battle_turn = "player"  # 戦闘のターン ("player" or "slime")
        self.battle_message = ""
        self.battle_log = []  # 戦闘のログを保存
        self.battle_options = ["Attack", "Run"]
        self.selected_option = 0

        pyxel.init(self.window_width, self.window_height, title="Dragon Quest", fps=30)
        pyxel.load("dragon_quest.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.in_battle:
            # プレイヤーの移動
            self.player.update()

            # スライムとの接触判定
            for slime in self.slimes:
                if slime.visible and self.check_collision(self.player, slime):
                    self.in_battle = True
                    self.current_slime = slime
                    self.battle_message = "A Slime appears!"
                    self.battle_log.append(self.battle_message)
                    break
        else:
            # 戦闘モード（ターン制）
            if self.battle_turn == "player":
                self.handle_player_turn()
            else:
                self.handle_slime_turn()

    def handle_player_turn(self):
        # プレイヤーのターンでの選択
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.selected_option = (self.selected_option + 1) % len(self.battle_options)
        if pyxel.btnp(pyxel.KEY_UP):
            self.selected_option = (self.selected_option - 1) % len(self.battle_options)

        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.selected_option == 0:  # Attackを選択
                self.current_slime.hp -= self.player.attack
                self.battle_message = "Player attacks!"
                self.battle_log.append(self.battle_message)
                if self.current_slime.hp <= 0:
                    self.current_slime.visible = False
                    self.battle_message = "You defeated the Slime!"
                    self.battle_log.append(self.battle_message)
                    self.in_battle = False
                    self.current_slime = None
                else:
                    self.battle_turn = "slime"  # スライムのターンに変更
            elif self.selected_option == 1:  # Runを選択
                self.battle_message = "You ran away!"
                self.battle_log.append(self.battle_message)
                self.in_battle = False

    def handle_slime_turn(self):
        # スライムのターンで攻撃
        self.player.hp -= self.current_slime.attack
        self.battle_message = f"Slime attacks! Player takes {self.current_slime.attack} damage."
        self.battle_log.append(self.battle_message)
        if self.player.hp <= 0:
            self.battle_message = "You were defeated!"
            self.battle_log.append(self.battle_message)
            self.in_battle = False
        else:
            self.battle_turn = "player"  # プレイヤーのターンに戻す

    def check_collision(self, player, enemy):
        # プレイヤーとスライムの衝突判定
        return (player.x < enemy.x + enemy.w and
                player.x + player.w > enemy.x and
                player.y < enemy.y + enemy.h and
                player.y + player.h > enemy.y)

    def draw(self):
        pyxel.cls(0)

        # プレイヤーの描画
        self.player.draw()

        # スライムの描画
        for slime in self.slimes:
            if slime.visible:
                slime.draw()

        # 樹木の描画
        for tree in self.trees:
            tree.draw()

        # 戦闘メッセージの表示
        if self.in_battle:
            pyxel.text(10, 10, self.battle_message, 7)
            pyxel.text(10, 20, "Choose action:", 7)
            for i, option in enumerate(self.battle_options):
                color = 7 if i == self.selected_option else 6
                pyxel.text(10, 30 + i * 10, option, color)

            pyxel.text(10, 50, f"Slime HP: {self.current_slime.hp}", 8)
            pyxel.text(10, 60, f"Player HP: {self.player.hp}", 9)

        # 戦闘ログの表示
        y_offset = 70
        for log in self.battle_log[-3:]:  # 最新の3件を表示
            pyxel.text(10, y_offset, log, 7)
            y_offset += 10


# ゲームの実行
Game()
