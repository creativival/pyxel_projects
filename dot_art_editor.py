import pyxel
from PIL import Image

# Pyxelの16色パレットをRGBにマッピング
pyxel_palette = [
    (0, 0, 0),  # 0: Black
    (29, 43, 83),  # 1: Dark blue
    (126, 37, 83),  # 2: Dark purple
    (0, 135, 81),  # 3: Dark green
    (171, 82, 54),  # 4: Brown
    (95, 87, 79),  # 5: Dark gray
    (194, 195, 199),  # 6: Light gray
    (255, 241, 232),  # 7: White
    (255, 0, 77),  # 8: Red
    (255, 163, 0),  # 9: Orange
    (255, 236, 39),  # 10: Yellow
    (0, 228, 54),  # 11: Green
    (41, 173, 255),  # 12: Blue
    (131, 118, 156),  # 13: Indigo
    (255, 119, 168),  # 14: Pink
    (255, 204, 170)  # 15: Peach
]


class DotArtEditor:
    def __init__(self):
        pyxel.init(128, 140, title="Dot Art Editor")  # ウィンドウの高さを増やす
        pyxel.mouse(True)
        self.canvas_size = 8
        self.pixel_size = 16
        self.colors = [-1] + [i for i in range(16)]  # -1（透明）を追加
        self.grid = [[-1 for _ in range(self.canvas_size)] for _ in range(self.canvas_size)]  # -1で初期化（透明）
        self.selected_color = -1
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # カラーパレット選択（マウスクリック）
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if pyxel.mouse_y >= 130:  # パレットの位置をクリックした場合
                palette_index = pyxel.mouse_x // 8
                if 0 <= palette_index < len(self.colors):
                    self.selected_color = self.colors[palette_index]
            else:
                # 描画
                x = pyxel.mouse_x // self.pixel_size
                y = pyxel.mouse_y // self.pixel_size
                if 0 <= x < self.canvas_size and 0 <= y < self.canvas_size:
                    self.grid[y][x] = self.selected_color

        # PNGエクスポート
        if pyxel.btnp(pyxel.KEY_E):
            self.export_png()

        # テキストでデータを出力
        if pyxel.btnp(pyxel.KEY_T):
            self.output_text_data()

        # テキストファイルからデータをロード
        if pyxel.btnp(pyxel.KEY_L):
            self.load_text_data()

    def draw(self):
        pyxel.cls(0)

        # 細かいチェック柄で透明部分を表現
        for y in range(self.canvas_size):
            for x in range(self.canvas_size):
                for dy in range(0, self.pixel_size, 2):
                    for dx in range(0, self.pixel_size, 2):
                        color = 7 if (dx // 2 + dy // 2) % 2 == 0 else 13
                        pyxel.pset(x * self.pixel_size + dx, y * self.pixel_size + dy, color)
                        pyxel.pset(x * self.pixel_size + dx + 1, y * self.pixel_size + dy, color)
                        pyxel.pset(x * self.pixel_size + dx, y * self.pixel_size + dy + 1, color)
                        pyxel.pset(x * self.pixel_size + dx + 1, y * self.pixel_size + dy + 1, color)

                # ドットが存在する場合、その色で上書き
                color_id = self.grid[y][x]
                if color_id != -1:
                    pyxel.rect(x * self.pixel_size, y * self.pixel_size, self.pixel_size, self.pixel_size, color_id)

        # セルとセルの間にグリッド線を描画、0.5ピクセル左上にずらす
        for y in range(1, self.canvas_size):
            pyxel.line(-0.5, y * self.pixel_size - 0.5, self.canvas_size * self.pixel_size - 0.5,
                       y * self.pixel_size - 0.5, 1)  # 水平線
        for x in range(1, self.canvas_size):
            pyxel.line(x * self.pixel_size - 0.5, -0.5, x * self.pixel_size - 0.5,
                       self.canvas_size * self.pixel_size - 0.5, 1)  # 垂直線

        # カラーパレットの描画（最初のパレットは透明）
        for i, color in enumerate(self.colors):
            if color == -1:
                for dy in range(0, 8, 2):
                    for dx in range(0, 8, 2):
                        color = 7 if (dx // 2 + dy // 2) % 2 == 0 else 13
                        pyxel.pset(i * 8 + dx, 130 + dy, color)
                        pyxel.pset(i * 8 + dx + 1, 130 + dy, color)
                        pyxel.pset(i * 8 + dx, 130 + dy + 1, color)
                        pyxel.pset(i * 8 + dx + 1, 130 + dy + 1, color)
            else:
                pyxel.rect(i * 8, 130, 8, 8, color)
            if color == self.selected_color:
                pyxel.rectb(i * 8, 130, 8, 8, 7)  # 選択中の色を強調表示

    def export_png(self):
        img = Image.new('RGBA', (self.canvas_size, self.canvas_size))  # RGBAで作成（透明対応）
        for y in range(self.canvas_size):
            for x in range(self.canvas_size):
                color_id = self.grid[y][x]
                if color_id == -1:
                    img.putpixel((x, y), (0, 0, 0, 0))  # 透明ピクセル
                else:
                    rgb = pyxel_palette[color_id]
                    img.putpixel((x, y), (rgb[0], rgb[1], rgb[2], 255))
        img = img.resize((self.canvas_size * self.pixel_size, self.canvas_size * self.pixel_size), Image.NEAREST)
        img.save('dot_art.png')
        print("PNGエクスポート完了: dot_art.png")

    def output_text_data(self):
        # グリッドデータを1行のテキストに変換
        data = []
        for y in range(self.canvas_size):
            for x in range(self.canvas_size):
                data.append(str(self.grid[y][x]))
        text_data = " ".join(data)
        print(f"テキストデータ出力: {text_data}")
        with open("dot_art_data.txt", "w") as f:
            f.write(text_data)
        print("テキストデータが 'dot_art_data.txt' に保存されました。")

    def load_text_data(self):
        try:
            with open("dot_art_data.txt", "r") as f:
                text_data = f.read()
            print(f"テキストデータ読み込み: {text_data}")
            data = text_data.split()
            for y in range(self.canvas_size):
                for x in range(self.canvas_size):
                    self.grid[y][x] = int(data[y * self.canvas_size + x])
            print("テキストデータがグリッドにロードされました。")
        except FileNotFoundError:
            print("ファイルが見つかりませんでした。")
        except Exception as e:
            print(f"エラーが発生しました: {e}")


DotArtEditor()
