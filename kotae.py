""""
今日のテーマ
その１：敵を作って動かしてみよう！！！
その２：時間があればモジュールもやりたい！！
"""
import pygame
import os

TATE = 900
YOKO = 1200
TITLE = "TAKOYAKI OISHI"
# ディレクトリを設定しよう！BASE_DIRとかでいいよ
BASE_DIR = os.path.dirname(__file__)
# 画像のディレクトリを設定
IMG_DIR = os.path.join(BASE_DIR, "imgs")
# プレイヤーの画像を指定
PLAYER_DIR = os.path.join(IMG_DIR, "resized_ningen2025.png")
"""
PART01
"""
# スプライトシートのディレクトリを指定
# ここには画像の名前を指定！
#SPRITESHEET_DIR = os.path.join(IMG_DIR, "")

# ステップ３
# 色々と初期化をしよう
# 初期化って何？
# 答え：つかえるじょうたいにすること
# pygameを初期化
# pygame.init()で初期化できるよ。覚えなくていい！
pygame.init()
# ゲームウインドウを初期化
# pygame.display.set_mode((よこはば,たてはば))で作れるよ。覚えなくていいよ！
screen = pygame.display.set_mode((YOKO, TATE))

# ステップ５：プレイヤーを作ろう
class Player(pygame.sprite.Sprite):
    def __init__(self):
        """
        コンストラクタ: プレイヤーオブジェクトを初期化します。
        Args:
            width (int): プレイヤー画像の幅。
            height (int): プレイヤー画像の高さ。
        プレイヤーオブジェクトを初期化し、プレイヤーの外観、位置、および他の属性を設定します。
        このコンストラクタはプレイヤーオブジェクトを作成する際に自動的に呼び出され、
        プレイヤーの初期設定を行うために使用されます。
        """
        # 親クラス(Sprite)のコンストラクタを実行
        pygame.sprite.Sprite.__init__(self)
        """
        PART02
        """
        # プレイヤーを表示するためのキャンバスを用意
        # Surface（画像を表示させるクラス）をインスタンス化して変数に保存（初期化）
        self.image = pygame.Surface((32, 32))
        # 画像のサイズと同じキャンバスを用意
        """
        PART03
        """
        # 使う画像のパスを取得。
        # pygame.image.load(SPRITESHEET_DIR).convert()でパスを取得できる
        # それを変数に保存。クラス内の変数だよ！
        self.gazou = pygame.image.load(PLAYER_DIR).convert()
        """
        PART04
        """
        # 作成したキャンバス(self.image)に使う画像をスプライトシートから指定して貼り付け
        # self.image.blit(#使う画像のパス, (0, 0), (0, 0, 横幅, 縦幅))
        # 第３引数の３番目と４番目の値を画像のサイズに変更！
        self.image.blit(self.gazou, (0,0),(0,0,32,32))
        """
        PART05
        背景色を透明にする
        """
        # 透明にする色を指定。self.image.get_at((0, 0))としてキャンバスの左上の色を取得
        # 取得したいろを変数に保存。これはselfなくていい。でもあってもいける。
        iro = self.image.get_at((0,0))
        # 画像の背景色を透過する。
        # 上で取得した色を使って背景色を透明にする
        # キャンバス名.set_colorkey(上で取得した色)
        self.image.set_colorkey(iro)
        """
        PART06
        キャンバスサイズを調整
        """
        # キャンバスのサイズを小さくしてキャンバス名に再度保存。
        # キャンバス名 = pygame.transform.scale(キャンバス名, (リサイズしたい横幅, リサイズしたい縦幅))
        
        # 画像の位置を取得。Rect型範囲は常に(0,0)座標を起点としてる
        self.rect = self.image.get_rect()
        # プレイヤーのx座標を設定
        self.rect.x = 100
        # プレイヤーのy座標を設定
        self.rect.y = 100
        # 横移動のスピードを保存する変数
        self.vx = 0
        # 縦移動のスピードを保存する変数
        self.vy = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] == True:
            self.vx = 1
        elif keys[pygame.K_LEFT] == True:
            self.vx = -1
        elif keys[pygame.K_UP] == True:
            self.vy = -1
        elif keys[pygame.K_DOWN] == True:
            self.vy = 1
        else:
            self.vx = 0
            self.vy = 0
        self.rect.x += self.vx
        self.rect.y += self.vy

"""
てきを作ろう！
敵はとりまシンプルに移動するだけでいい
STEP01
"""
class Teki(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32,32))
        self.gazou = pygame.image.load(PLAYER_DIR).convert()
        self.image.blit(self.gazou, (0,0), (0,0,32,32))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        import random
        self.rect.y = random.randint(0,900)
        self.vx = 1

    def update(self):
        self.rect.x += self.vx

player = Player()
t = Teki()
"""
STEP02
敵を初期化しよう！
"""

all_sprites = pygame.sprite.Group()
# このはこにプレイヤーを入れる
all_sprites.add(player)
# 気合いと根性
all_sprites.add(t)
"""
STEP03
ただし、みてるだけ
敵が出てくるタイミングを決めよう！
"""
# 敵が出てくる間隔を決める（秒）
teki_detekuru_kankaku = 0

# 最後に敵を生成してからの経過時間を追跡する変数
saigo_teki_detekara_keika_jikan = 0


kurikaeshi = True
while kurikaeshi:
    # 現在の時間を取得。pygame.time.get_ticks() / 1000を使うとできるよ！
    current_time = pygame.time.get_ticks() / 1000  # ミリ秒を秒に変換
    # ここはちょっとでむずいので説明します(for_loop.py)をみよう！
    for event in pygame.event.get():
        # もしも赤バツボタンが押されたら(pygame.QUIT)繰り返しを終了する
        if event.type == pygame.QUIT:
            # 繰り返しを終了する
            kurikaeshi = False
        #print(f"Enemy spawned at {current_time} seconds")  # 敵が生成された時刻を出力
    """
    STEP04
    敵が出てくるタイミングを決めよう！
    random.randintでもいいし、もっと細かく(0.2秒とか)設定したいならrandom.uniformとかもあり！
    """

    if current_time - saigo_teki_detekara_keika_jikan > teki_detekuru_kankaku:
        """
        やること
        その１：時間が経ったら敵を作成(初期化) ヒント player = Player()
        その２：敵をゲーム上でキャラクターを管理する箱にしまう ヒント all_sprites.add(player)
        その３：saigo_teki_detekara_keika_jikanをcurrent_timeで更新 ヒント そんなもんないわあああああああああ！！
        """
        t = Teki()
        all_sprites.add(t)

    # 背景を真っ黒に塗りつぶす
    screen.fill((0, 0, 0))
    # 星を描画する（例えば、100個の星）
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
