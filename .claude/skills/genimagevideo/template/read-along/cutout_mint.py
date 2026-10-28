"""Tách nền ảnh nhân vật chibi sinh trên NỀN MINT TRƠN (không phải xanh #00FF00).

  python cutout_mint.py                 # mọi ảnh trong assets/raw  (bỏ qua contact*.jpg)
  python cutout_mint.py jx3_smile       # chỉ các tên này (không đuôi)

Cách làm: lấy màu nền = trung vị viền ảnh -> flood-fill từ viền với ngưỡng -> thêm khử mọi pixel
rất gần màu nền (khoảng hở giữa tay-thân) -> viền mềm 1px -> xoá cái bóng elip dưới chân (bóng sẽ do
code vẽ lại). Ra assets/<tên>.png (PNG trong suốt, crop sát) + public/img/<tên>.png + src/sizes.json.
"""
import json, sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
raw, out, pub = here / "assets" / "raw", here / "assets", here / "public" / "img"
out.mkdir(exist_ok=True); pub.mkdir(parents=True, exist_ok=True)

FLOOD_TOL = 42   # xa màu nền tối đa để flood-fill đi qua (gồm cả bóng elip dưới chân)
KEY_TOL = 16     # pixel gần màu nền hơn mức này bị xoá dù không nối với viền


def cut(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int32)
    h, w, _ = a.shape
    edge = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    bg = np.median(edge, axis=0)
    dist = np.sqrt(((a - bg) ** 2).sum(axis=2))
    near = dist < FLOOD_TOL
    seen = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if near[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if near[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and near[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; q.append((ny, nx))
    greenish = ((a[..., 1] - a[..., 0]) > 20) & ((a[..., 1] - a[..., 2]) > 8)  # bóng elip dưới chân còn sót
    bgmask = seen | (dist < KEY_TOL) | greenish
    alpha = np.where(bgmask, 0, 255).astype(np.uint8)
    al = Image.fromarray(alpha).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    rgba = im.convert("RGBA"); rgba.putalpha(al)
    return rgba.crop(rgba.getbbox())


sizes_f = here / "src" / "sizes.json"
sizes = json.loads(sizes_f.read_text(encoding="utf-8")) if sizes_f.exists() else {}
names = sys.argv[1:] or [p.stem for p in sorted(raw.glob("*.png"))]
for n in names:
    im = cut(raw / f"{n}.png")
    im.save(out / f"{n}.png"); im.save(pub / f"{n}.png")
    sizes[n] = [im.width, im.height]
    print(n, im.size)
sizes_f.write_text(json.dumps(sizes, ensure_ascii=False, indent=1), encoding="utf-8")
