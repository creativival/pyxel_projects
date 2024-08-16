import pyxel

class App:
    def __init__(self):
        # pyxel.init(160, 120, caption="Hello Pyxel")
        # pyxel.image(0).load(0, 0, "assets/cat_16x16.png")
        pyxel.init(160, 120, title="Hello Pyxel")
        pyxel.images[0].load(0, 0, "pyxel_examples/assets/cat_16x16.png")

        # Starting Point
        self.player_x = 72
        self.player_y = 16

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.update_player()

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_AXIS_LEFTX):
            self.player_x = max(self.player_x - 2, 0)

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_AXIS_RIGHTX):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_AXIS_UP):
            self.player_y = max(self.player_y - 2, 0)

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_AXIS_DOWN):
            self.player_y = min(self.player_y + 2, pyxel.height - 16)


    def draw(self):
        pyxel.cls(0)

        # 猫ちゃんを描写
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            0,
            0,
            16,
            16,
            13,  # change from 5
        )
App()