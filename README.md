# Pixel Projects

Pixelのゲームを作成します。

## 環境

- Mac OS X 10.15.7
- MiniConda
- Python 3.10
- Pygame 2.1.8

## インストール

```bash
$ conda create -n pixel_projects python=3.10
$ conda activate pixel_projects
$ pip install pygame
```

## サンプルプロジェクト

`pyxel copy_examples`コマンドでサンプルプロジェクトをコピーできます。

コピーされるサンプルは以下の通りです。

|ファイル名|内容|
| ---- | ---- |
|01_hello_pyxel.py|シンプルなアプリケーション|
|02_jump_game.py|Pyxel リソースファイルを使ったジャンプゲーム|
|03_draw_api.py|描画 API のデモ|
|04_sound_api.py|サウンド API のデモ|
|05_color_palette.py|カラーパレット一覧|
|06_click_game.py|マウスクリックゲーム|
|07_snake.py|BGM 付きスネークゲーム|
|08_triangle_api.py|三角形描画 API のデモ|
|09_shooter.py|画面遷移のあるシューティングゲーム|
|10_platformer.py|マップのある横スクロールアクションゲーム|
|11_offscreen.py|Image クラスによるオフスクリーン描画|
|12_perlin_noise.py|パーリンノイズアニメーション|
|13_bitmap_font.py|ビットマップフォント描画|
|14_synthesizer.py|オーディオ拡張機によるシンセサイザー|
|15_tiled_map_file.py|タイルマップファイル (.tmx) の読み込みと描画|
|99_flip_animation.py|flip 関数によるアニメーション (非 Web 環境のみ)|
|30SecondsOfDaylight.pyxapp|第 1 回 Pyxel Jam 優勝ゲーム (Adam制作)|
|megaball.pyxapp|アーケードボール物理ゲーム (Adam制作)|
|8bit-bgm-gen.pyxapp|BGM自動作成ツール (frenchbread制作)|

サンプルの実行方法は以下の通りです。

```bash
$ pyxel copy_examples
$ cd pyxel_examples
$ pyxel run 01_hello_pyxel.py
$ pyxel play 30SecondsOfDaylight.pyxapp
```

## プロジェクト

- [x] [Pixel Invaders]()
- [x] [Pixel Snake]()
- [x] [Pixel Tetris]()
- [x] [Pixel Breakout]()
- [x] [Pixel Pong]()

## Voxelammingとの連携

VoxelammingのゲームモードのホストとしてPixelを使用します。

### インストール

```bash
$ pip install voxelamming
```

#### メソッドの説明

| メソッド名                                                                               | 説明 | 引数                                                                                                                                                                |
|-------------------------------------------------------------------------------------|---|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `set_game_screen_size(width, height, angle=90, r=1, g=1, b=0, alpha=0.5)`           | ゲーム画面を設定します。 | `width`, `height`: 画面サイズ (float), `angle`: 角度 (float) , `r`, `g`, `b`, `alpha`: 色 (float, 0-1)                                                                    |
| `set_game_score(score)`                                                             | ゲームスコアを設定します。 | `score`: ゲームのスコア(int)                                                                                                                                             |
| `send_game_over()`                                                                  | ゲームオーバーを設定します。 |                                                                                                                                                                   |
| `create_sprite(sprite_name, color_list, x, y, direction=90, scale=1, visible=True)` | スプライトを作成します。 | `sprite_name`: スプライトの名前 (string), `color_list`: ドットの色データ (string), `x`, `y`: 位置 (float), `direction`: 角度 (float), `sclae`: スケール (float), `visiable`: 表示 (boolean) |
| `move_sprite(sprite_name, x, y, direction=90, scale=1, visible=True)`               | スプライトを移動します。 | `sprite_name`: スプライトの名前 (string), `x`, `y`: 位置 (float), `direction`: 角度 (float), `sclae`: スケール (float), `visiable`: 表示 (boolean)                                  |

### サンプル

cat_game_with_pixel.pyを参照してください。

### 実行

```bash
$ python cat_game_with_pixel.py
```


## ライセンス

MIT
