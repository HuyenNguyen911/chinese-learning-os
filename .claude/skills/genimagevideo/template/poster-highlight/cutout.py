"""Tách nền: assets/raw/*.png -> assets/*.png (PNG trong suốt, crop sát, ≤640px) + chép public/img + assets/contact.jpg

  python cutout.py                       # mọi ảnh trong assets/raw
  python cutout.py etou lian             # chỉ các id này
  python cutout.py --method rembg --model birefnet-general-lite

--method auto (mặc định) nhìn viền ảnh:
  * nền XANH LÁ (#00FF00)  -> chroma: tách đúng màu xanh + khử viền xanh. CHÍNH XÁC NHẤT — sinh ảnh
                              trên nền xanh (layout.json "style" đã ghi sẵn).
  * nền trắng              -> flood-fill pixel gần trắng từ viền (ảnh có viền sáng sẽ còn khung nhạt).
--method rembg: AI tách nền (venv riêng của skill). Đã thử 2026-10-21 trên ảnh bộ phận rời:
  isnet-anime xoá mất mắt/trán/nửa mớ tóc; birefnet-general-lite xoá da trán, cắt lệch miệng,
  ~50s/ảnh -> KHÔNG dùng mặc định, chỉ thử khi chroma/flood đều không được.
"""
import argparse, os, subprocess, sys
from collections import deque
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
sys.path.insert(0, str(here))
from _paths import SKILL  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("ids", nargs="*")
ap.add_argument("--method", choices=["auto", "chroma", "flood", "rembg"], default="auto")
ap.add_argument("--model", default="isnet-anime")
a = ap.parse_args()

venv_py = SKILL / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
if a.method == "rembg":
    try:
        import rembg  # noqa: F401
    except ImportError:
        if venv_py.exists() and Path(sys.executable).resolve() != venv_py.resolve():
            sys.exit(subprocess.run([str(venv_py), __file__, *sys.argv[1:]]).returncode)
        sys.exit("Chưa cài rembg — xem SKILL.md mục Cài đặt")

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

TH = 235


def border_kind(im):
    """'chroma' nếu viền ảnh chủ yếu là xanh lá thuần, 'flood' nếu sáng/trắng."""
    arr = np.asarray(im.convert("RGB")).astype(int)
    edge = np.concatenate([arr[0], arr[-1], arr[:, 0], arr[:, -1]])
    green = (edge[:, 1] > 180) & (edge[:, 0] < 120) & (edge[:, 2] < 120)
    return "chroma" if green.mean() > 0.6 else "flood"


def cut_chroma(im):
    arr = np.asarray(im.convert("RGB")).astype(np.float32)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    m = np.maximum(r, b)
    spill = g - m                                   # > 0: ngả xanh
    alpha = np.clip((90 - spill) / 60, 0, 1)        # spill ≥ 90 -> trong suốt, ≤ 30 -> đặc
    g = np.where(spill > 0, m, g)                   # khử viền xanh ở mép
    return Image.fromarray(np.dstack([r, g, b, alpha * 255]).astype(np.uint8), "RGBA")


def cut_flood(im):
    im = im.convert("RGBA"); arr = np.array(im)
    h, w = arr.shape[:2]
    white = (arr[..., :3] >= TH).all(axis=2)
    seen = np.zeros((h, w), bool); q = deque()
    for x in range(w):
        q.extend(((0, x), (h - 1, x)))
    for y in range(h):
        q.extend(((y, 0), (y, w - 1)))
    while q:
        y, x = q.popleft()
        if 0 <= y < h and 0 <= x < w and not seen[y, x] and white[y, x]:
            seen[y, x] = True
            q.extend(((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)))
    arr[seen, 3] = 0
    return Image.fromarray(arr)


_session = None


def cut_rembg(im):
    global _session
    from rembg import new_session, remove
    if _session is None:
        _session = new_session(a.model)
    return remove(im.convert("RGB"), session=_session, post_process_mask=True)


def finish(im):
    alpha = im.getchannel("A").point(lambda v: 255 if v > 8 else 0)
    im = im.crop(alpha.getbbox())
    im.thumbnail((640, 640))
    return im


assets = here / "assets"
pub = here / "public" / "img"
pub.mkdir(parents=True, exist_ok=True)
files = sorted((assets / "raw").glob("*.png"))
if a.ids:
    files = [f for f in files if f.stem in a.ids]
CUT = {"chroma": cut_chroma, "flood": cut_flood, "rembg": cut_rembg}
for f in files:
    src = Image.open(f)
    kind = border_kind(src) if a.method == "auto" else a.method
    im = finish(CUT[kind](src))
    im.save(assets / f.name)
    im.save(pub / f.name)
    print("cut", f.stem, kind, flush=True)

# contact sheet: mọi ảnh đã tách, trên nền hồng để lộ phần nền còn sót
allc = sorted(p for p in assets.glob("*.png"))
cols = 5
rows = max(1, -(-len(allc) // cols))
sheet = Image.new("RGB", (cols * 260, rows * 280), (255, 200, 220))
d = ImageDraw.Draw(sheet)
for i, p in enumerate(allc):
    t = Image.open(p); t.thumbnail((240, 240))
    x, y = (i % cols) * 260 + 10, (i // cols) * 280 + 10
    sheet.paste(t, (x, y), t); d.text((x, y + 250), p.stem, fill=(0, 0, 0))
sheet.save(assets / "contact.jpg")
print(f"{len(files)} ảnh -> assets/contact.jpg")
