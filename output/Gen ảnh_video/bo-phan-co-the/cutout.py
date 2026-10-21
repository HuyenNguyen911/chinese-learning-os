"""Tách nền trắng (flood-fill từ viền) + crop + thu nhỏ: assets/raw/*.png -> assets/*.png, và sinh contact sheet."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import numpy as np
from collections import deque

here = Path(__file__).parent / "assets"
TH = 235

def cut(im):
    im = im.convert("RGBA"); a = np.array(im)
    h, w = a.shape[:2]
    white = (a[..., :3] >= TH).all(axis=2)
    seen = np.zeros((h, w), bool); q = deque()
    for x in range(w):
        for y in (0, h - 1): q.append((y, x))
    for y in range(h):
        for x in (0, w - 1): q.append((y, x))
    while q:
        y, x = q.popleft()
        if 0 <= y < h and 0 <= x < w and not seen[y, x] and white[y, x]:
            seen[y, x] = True
            q.extend(((y+1,x),(y-1,x),(y,x+1),(y,x-1)))
    a[seen, 3] = 0
    out = Image.fromarray(a)
    out = out.crop(out.getchannel("A").point(lambda v: 255 if v > 0 else 0).getbbox())
    out.thumbnail((640, 640))
    return out

files = sorted((here / "raw").glob("*.png"))
for f in files:
    im = cut(Image.open(f))
    im.save(here / f.name)
    pub = here.parent / "public" / "img"
    pub.mkdir(parents=True, exist_ok=True)
    im.save(pub / f.name)
sheet = Image.new("RGB", (5 * 260, 3 * 280), (255, 200, 220))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    t = Image.open(here / f.name); t.thumbnail((240, 240))
    x, y = (i % 5) * 260 + 10, (i // 5) * 280 + 10
    sheet.paste(t, (x, y), t); d.text((x, y + 250), f.stem, fill=(0, 0, 0))
sheet.save(here / "contact.jpg")
