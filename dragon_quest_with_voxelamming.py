import pyxel
import random
import time
# from voxelamming import Voxelamming
from voxelamming_local import Voxelamming  # ローカルで開発している場合はこちらを使う


# プレイヤークラス
class Player:
    name_front = 'warrior_front_8x8'
    dot_data_front = (
        '-1 -1 8 -1 -1 8 -1 7 -1 -1 8 8 8 8 -1 7 -1 -1 15 15 15 15 -1 7 -1 -1 4 15 15 4 -1 7 8 8 15 15 15 15 8 8 -1 -1 '
        '8 8 8 8 -1 -1 -1 -1 8 8 8 8 -1 -1 -1 4 4 -1 -1 4 4 -1'
    )
    name_back = 'warrior_back_8x8'
    dot_data_back = (
        '7 -1 8 -1 -1 8 -1 -1 7 -1 8 8 8 8 -1 -1 7 -1 8 8 8 8 -1 -1 7 -1 4 4 4 4 -1 -1 8 8 4 4 4 4 8 8 -1 -1 8 8 8 8 '
        '-1 -1 -1 -1 8 8 8 8 -1 -1 -1 4 4 -1 -1 4 4 -1'
    )

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
            self.y_direction = -1
            self.y = max(0, self.y - 2)
        else:
            self.y_direction = 1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y = min(pyxel.height - self.h, self.y + 2)

    def draw(self):
        # プレイヤーの描画
        print(self.x, self.y)
        if self.y_direction == 1:
            pyxel.blt(self.window_width // 2, self.window_height // 2, self.img, self.u, self.v, self.w, self.h, 0)
        else:
            pyxel.blt(self.window_width // 2, self.window_height // 2, self.img, self.u + 8, self.v, self.w, self.h, 0)


# スライムクラス（敵）
class Slime:
    name = 'slime_8x8'
    dot_data = (
        '-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 10 -1 -1 -1 -1 -1 -1 10 10 10 -1 -1 -1 -1 10 10 10 10 10 -1 -1 10 10 10 '
        '10 10 10 -1 -1 10 9 10 10 9 10 -1 -1 10 10 10 10 10 10 -1 -1 10 7 9 9 7 10 -1'
    )

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


# スライムクラス（敵）
class Dragon:
    name = 'dragon_16x16'
    dot_data = (
        '-1 -1 -1 -1 -1 -1 -1 3 3 3 3 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 3 3 3 3 3 3 3 -1 -1 -1 -1 -1 -1 -1 -1 -1 3 3 7 3 '
        '3 7 3 3 -1 -1 -1 -1 -1 -1 -1 3 3 3 0 3 3 0 3 3 3 -1 3 3 -1 -1 -1 3 3 3 3 3 3 3 3 3 3 -1 3 -1 -1 -1 -1 3 3 3 7 '
        '8 8 8 8 8 7 -1 3 -1 -1 -1 -1 3 3 3 7 3 3 3 3 3 7 -1 3 -1 -1 -1 -1 3 3 3 7 3 3 -1 -1 -1 7 -1 3 3 -1 -1 -1 3 3 '
        '3 3 3 3 -1 -1 -1 -1 -1 3 3 3 -1 3 3 11 11 3 3 3 11 11 -1 -1 -1 3 3 3 -1 3 3 11 11 11 3 3 11 11 11 -1 -1 3 3 3 '
        '3 3 3 3 11 11 3 3 3 11 11 -1 -1 -1 3 3 3 3 3 3 3 3 3 3 3 -1 -1 -1 -1 -1 -1 3 3 3 3 3 3 3 3 3 3 -1 -1 -1 -1 -1 '
        '-1 -1 3 3 3 3 3 3 3 3 3 3 -1 -1 -1 -1 -1 3 3 3 -1 -1 -1 -1 -1 -1 -1 3 3 -1 -1'
    )

    def __init__(self, player, window_width, window_height):
        self.player = player
        self.window_width = window_width
        self.window_height = window_height
        self.x = random.randint(10, window_width - 42)
        self.y = random.randint(10, window_height - 42)
        self.img = 0
        self.u = 0
        self.v = 24
        self.w = 16
        self.h = 16
        self.hp = 100
        self.attack = 5
        self.visible = False

    def draw(self):
        if self.visible:
            # スライムの描画
            x = self.x - self.player.x + self.window_width // 2
            y = self.y - self.player.y + self.window_height // 2
            pyxel.blt(x, y, self.img, self.u, self.v, self.w, self.h, 0)


# 樹木クラス（障害物）
class Tree:
    name = 'tree_8x8'
    dot_data = (
        '-1 -1 11 11 11 11 -1 -1 -1 11 11 3 3 11 11 -1 -1 11 3 3 3 3 11 -1 -1 11 3 3 3 3 11 -1 -1 11 3 4 4 3 11 -1 -1 '
        '11 11 4 4 11 11 -1 -1 -1 11 4 4 11 -1 -1 -1 -1 -1 4 4 -1 -1 -1'
    )

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
        self.dragon = Dragon(self.player, self.window_width, self.window_height)
        self.in_battle = False
        self.game_over = False
        self.game_clear = False
        self.current_enemy = None  # 現在戦闘中の敵
        self.current_enemy_name = ""
        self.battle_turn = "player"  # 戦闘のターン ("player" or "slime")
        self.battle_message = ""
        self.battle_log = []  # 戦闘のログを保存
        self.battle_options = ["Attack", "Run"]
        self.selected_option = 0
        self.log_display_time = 0  # ログ表示のためのタイマー

        # ボクセラミングの設定（Pyxelの初期化の前に実行）
        self.dot_size = 1  # AR空間で表示されるスプライトのドットのサイズ（センチメートル）
        self.window_angle = 80  # ARウインドウの傾き（度）
        self.vox = Voxelamming('1000')
        self.init_voxelamming()

        pyxel.init(self.window_width, self.window_height, title="Dragon Quest", fps=30)
        pyxel.load("dragon_quest.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over or self.game_clear:
            return

        if not self.in_battle:
            # プレイヤーの移動
            self.player.update()

            if len([slime for slime in self.slimes if slime.visible]) == 0:  # スライムが全滅した時
                self.current_enemy_name = "Dragon"
                # ドラゴンを表示
                self.dragon.visible = True
                # ドラゴンとの接触判定
                if self.check_collision(self.player, self.dragon):
                    self.in_battle = True
                    self.current_enemy = self.dragon
                    self.battle_message = "A Dragon appears!"
                    self.battle_log.append(self.battle_message)
            else:
                self.current_enemy_name = "Slime"
                # スライムとの接触判定
                for slime in self.slimes:
                    if slime.visible and self.check_collision(self.player, slime):
                        self.in_battle = True
                        self.current_enemy = slime
                        self.battle_message = "A Slime appears!"
                        self.battle_log.append(self.battle_message)
                        break
        else:
            self.log_display_time = pyxel.frame_count  # ログ表示開始時のフレーム数を保存
            # 戦闘モード（ターン制）
            if self.battle_turn == "player":
                self.handle_player_turn()
            else:
                self.handle_enemy_turn()

        # ボクセラミングの更新
        self.update_voxelamming()

    def handle_player_turn(self):
        # プレイヤーのターンでの選択
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.selected_option = (self.selected_option + 1) % len(self.battle_options)
        if pyxel.btnp(pyxel.KEY_UP):
            self.selected_option = (self.selected_option - 1) % len(self.battle_options)

        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.selected_option == 0:  # Attackを選択
                player_attack = self.player.attack * random.randint(1, 3)
                self.current_enemy.hp -= player_attack
                self.battle_message = f"Player attacks! {self.current_enemy_name} takes {player_attack} damage."
                self.battle_log.append(self.battle_message)
                if self.current_enemy.hp <= 0:
                    self.current_enemy.visible = False
                    self.battle_message = f"You defeated the {self.current_enemy_name}!"
                    self.battle_log.append(self.battle_message)
                    self.in_battle = False
                    self.current_enemy = None

                    if self.current_enemy_name == "Dragon":
                        self.game_clear = True
                    else:
                        self.player.hp += 10  # スライムに勝利したらHPを回復
                else:
                    self.battle_turn = "enemy"  # 敵のターンに変更
            elif self.selected_option == 1:  # Runを選択
                self.battle_message = "You ran away!"
                self.battle_log.append(self.battle_message)
                self.in_battle = False

                # ドラゴンから逃げる場合はスライムを再配置
                if self.current_enemy_name == "Dragon":
                    self.dragon.visible = False

                    for slime in self.slimes:
                        slime.x = random.randint(10, self.window_width - 10)
                        slime.y = random.randint(10, self.window_height - 10)
                        slime.hp = 10
                        slime.visible = True

    def handle_enemy_turn(self):
        # 敵のターンで攻撃
        enemy_attack = self.current_enemy.attack * random.randint(1, 3)
        self.player.hp -= enemy_attack
        self.battle_message = f"{self.current_enemy_name} attacks! Player takes {enemy_attack} damage."
        self.battle_log.append(self.battle_message)
        if self.player.hp <= 0:
            self.battle_message = "You were defeated!"
            self.battle_log.append(self.battle_message)
            self.in_battle = False
            self.game_over = True
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

        # ドラゴンの描画
        self.dragon.draw()

        # HPの表示
        pyxel.text(100, 10, f"Player HP: {self.player.hp}", 9)

        # 戦闘メッセージの表示
        if self.in_battle:
            # 敵のHPを表示
            pyxel.text(100, 20, f"{self.current_enemy_name} HP: {self.current_enemy.hp}", 8)

            # オプションを表示
            pyxel.text(10, 40, "Choose action:", 7)
            for i, option in enumerate(self.battle_options):
                color = 7 if i == self.selected_option else 6
                pyxel.text(10, 50 + i * 10, option, color)

        # 戦闘ログの表示
        if pyxel.frame_count - self.log_display_time < 90:
            y_offset = 70
            for log in self.battle_log[-3:]:  # 最新の3件を表示
                pyxel.text(10, y_offset, log, 7)
                y_offset += 10

        # ゲームオーバー時の表示
        if self.game_over:
            pyxel.text(60, 30, "GAME OVER", pyxel.frame_count % 16)

        # ゲームクリア時の表示
        if self.game_clear:
            pyxel.text(60, 30, "GAME CLEAR!", pyxel.frame_count % 16)

    def init_voxelamming(self):
        # ボクセラミングの初期化
        self.vox.set_box_size(self.dot_size)
        self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1, blue=0,
                                 alpha=0.8)
        self.vox.set_command('liteRender')

        # スプライトを表示
        self.vox.create_sprite(self.player.name_front, self.player.dot_data_front, visible=False)
        self.vox.create_sprite(self.player.name_back, self.player.dot_data_back, visible=False)
        self.vox.create_sprite(Slime.name, Slime.dot_data, visible=False)
        self.vox.create_sprite(Tree.name, Tree.dot_data, visible=False)
        self.vox.create_sprite(Dragon.name, Dragon.dot_data, visible=False)

        self.vox.send_data()
        self.vox.clear_data()

    def update_voxelamming(self):
        # スプライトの情報を0.1秒ごとに送信
        if pyxel.frame_count % 2 == 0 or self.game_clear or self.game_over:  # PyxelのデフォルトFPSは30
            self.vox.set_box_size(self.dot_size)
            self.vox.set_game_screen(self.window_width, self.window_height, self.window_angle, red=1, green=1,
                                     blue=0, alpha=0.5)
            self.vox.set_command('liteRender')

            # プレイヤーのスプライトの移動
            vox_x, vox_y = self.convert_position_to_voxelamming(
                self.player.x, self.player.y, self.player.w, self.player.h)
            if self.player.y_direction == 1:
                self.vox.move_sprite(self.player.name_front, vox_x, vox_y, 0, 1)
            else:
                self.vox.move_sprite(self.player.name_back, vox_x, vox_y, 0, 1)

            # スライムのスプライトを移動
            for slime in self.slimes:
                if slime.visible and \
                        (-pyxel.width / 2 < slime.x - self.player.x < pyxel.width / 2
                         and -pyxel.height / 2 < slime.y - self.player.y < pyxel.height / 2):
                    vox_x, vox_y = self.convert_position_to_voxelamming(
                        slime.x, slime.y, slime.w, slime.h)
                    self.vox.move_sprite(slime.name, vox_x, vox_y, 0, 1)

            # 木のスプライトを移動
            for tree in self.trees:
                if (-pyxel.width / 2 < tree.x - self.player.x < pyxel.width / 2
                        and -pyxel.height / 2 < tree.y - self.player.y < pyxel.height / 2):
                    vox_x, vox_y = self.convert_position_to_voxelamming(
                        tree.x, tree.y, tree.w, tree.h)
                    self.vox.move_sprite(tree.name, vox_x, vox_y, 0, 1)

            # ドラゴンの移動
            if self.dragon.visible and \
                    (-pyxel.width / 2 < self.dragon.x - self.player.x < pyxel.width / 2
                     and -pyxel.height / 2 < self.dragon.y - self.player.y < pyxel.height / 2):
                vox_x, vox_y = self.convert_position_to_voxelamming(
                    self.dragon.x, self.dragon.y, self.dragon.w, self.dragon.h)
                self.vox.move_sprite(self.dragon.name, vox_x, vox_y, 0, 1)

            # HPの表示
            self.vox.display_text(f"Player HP: {self.player.hp}", 50, 50, color_id=9)

            # 戦闘メッセージの表示
            if self.in_battle:
                # 敵のHPを表示
                self.vox.display_text(f"{self.current_enemy_name} HP: {self.current_enemy.hp}", 50, 40, color_id=8)

                # オプションを表示
                self.vox.display_text("Choose action:", -50, 50, color_id=7)
                for i, option in enumerate(self.battle_options):
                    color = 7 if i == self.selected_option else 6
                    self.vox.display_text(option, -60, 40 - i * 10, color_id=color, align="left")

            # 戦闘ログの表示
            if pyxel.frame_count - self.log_display_time < 90:
                y_offset = 0
                for log in self.battle_log[-3:]:  # 最新の3件を表示
                    self.vox.display_text(log, -60, y_offset, color_id=7, align="left")
                    y_offset -= 10

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
        x = x - self.player.x + self.window_width // 2  # プレイヤーを中心に固定
        y = y - self.player.y + self.window_height // 2  # プレイヤーを中心に固定
        return x - self.window_width // 2 + width // 2, self.window_height // 2 - (y + height // 2)


# ゲームの実行
Game()
