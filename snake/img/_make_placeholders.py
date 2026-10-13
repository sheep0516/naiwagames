# -*- coding: utf-8 -*-
"""生成贪吃蛇占位贴图：head / body / tail / apple（128x128 透明 PNG）"""
import os
from PIL import Image, ImageDraw, ImageFilter

OUT = r"C:/Users/30227/Desktop/games/snake/img"
os.makedirs(OUT, exist_ok=True)

SS = 4                 # 4 倍超采样，边缘更顺滑
S = 128
W = S * SS


def canvas():
    return Image.new("RGBA", (W, W), (0, 0, 0, 0))


def layer():
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def save(im, name):
    im.resize((S, S), Image.LANCZOS).save(os.path.join(OUT, name))
    print("saved", name)


GREEN_DARK = (36, 137, 98, 255)
GREEN_MID = (47, 165, 110, 255)
GREEN_LIGHT = (108, 214, 148, 255)
RED = (239, 75, 82, 255)
LEAF = (63, 181, 111, 255)
STEM = (128, 90, 56, 255)
DARK = (18, 50, 40, 255)

# ---------------- 蛇头（默认朝右） ----------------
im = canvas()
d = ImageDraw.Draw(im)
d.rounded_rectangle((20, 20, W - 20, W - 20), radius=132, fill=GREEN_DARK)

hl, hd = layer()                                    # 顶部柔光
hd.ellipse((70, 34, W - 90, 240), fill=(255, 255, 255, 46))
hd.ellipse((108, 56, W - 230, 168), fill=(255, 255, 255, 52))
hl = hl.filter(ImageFilter.GaussianBlur(10))
im.alpha_composite(hl)

d = ImageDraw.Draw(im)
for cy in (176, 336):                               # 眼睛（朝右）
    d.ellipse((286, cy - 46, 378, cy + 46), fill=(255, 255, 255, 255))
    d.ellipse((322, cy - 25, 372, cy + 25), fill=DARK)
save(im, "head.png")

# ---------------- 蛇身 ----------------
im = canvas()
d = ImageDraw.Draw(im)
d.rounded_rectangle((16, 16, W - 16, W - 16), radius=138, fill=GREEN_MID)

hl, hd = layer()
hd.ellipse((70, 34, W - 90, 250), fill=(255, 255, 255, 52))
sh, sd = layer()                                    # 底部暗面
sd.ellipse((70, 300, W - 70, W - 20), fill=(16, 88, 60, 40))
im.alpha_composite(hl.filter(ImageFilter.GaussianBlur(10)))
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
save(im, "body.png")

# ---------------- 蛇尾（默认朝右，尖端在右） ----------------
im = canvas()
d = ImageDraw.Draw(im)
N = 90                                                        # 沿轴线堆叠圆，得到平滑收尖
for i in range(N):
    t = i / (N - 1)
    x = 150 + t * 316
    r = 176 * (1 - t) ** 0.82 + 16
    d.ellipse((x - r, 256 - r, x + r, 256 + r), fill=GREEN_LIGHT)
d.rounded_rectangle((74, 80, 220, 432), radius=88, fill=GREEN_LIGHT)

hl, hd = layer()
hd.ellipse((110, 118, 330, 300), fill=(255, 255, 255, 60))
im.alpha_composite(hl.filter(ImageFilter.GaussianBlur(12)))
save(im, "tail.png")

# ---------------- 苹果 ----------------
im = canvas()
d = ImageDraw.Draw(im)
d.rounded_rectangle((240, 44, 276, 126), radius=18, fill=STEM)   # 果柄

leaf, ld = layer()                                               # 叶子
ld.ellipse((0, 0, 196, 96), fill=LEAF)
leaf = leaf.rotate(-30, resample=Image.BICUBIC, center=(98, 48))
im.alpha_composite(leaf, (284, 24))

d = ImageDraw.Draw(im)
d.ellipse((76, 104, W - 44, W - 40), fill=RED)                   # 果身

sh, sd = layer()                                                 # 底部暗面
sd.ellipse((124, 296, W - 96, W - 54), fill=(198, 48, 56, 66))
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))

hl, hd = layer()                                                 # 高光
hd.ellipse((136, 168, 244, 272), fill=(255, 255, 255, 160))
hd.ellipse((256, 194, 300, 238), fill=(255, 255, 255, 96))
im.alpha_composite(hl.filter(ImageFilter.GaussianBlur(8)))
save(im, "apple.png")

print("done ->", OUT)
