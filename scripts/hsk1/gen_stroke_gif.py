#!/usr/bin/env python3
"""gen_stroke_gif.py — sinh GIF động thứ tự nét chữ Hán.

CLI:
    gen_stroke_gif.py <hanzi> <out.gif>

Nguồn dữ liệu nét: Make Me a Hanzi (`graphics.txt`, mỗi dòng 1 JSON object
`{"character": "...", "strokes": [<SVG path fill>, ...], "medians": [[[x,y],...], ...]}`).
Toạ độ SVG nằm trong hệ 1024x1024, cần lật trục y (y' = 900 - y) để hiển thị
đúng chiều trên ảnh raster (đã kiểm chứng bằng cách render thử ký tự 你).

Cách render (đầy đủ, không phải fallback):
    - Mỗi nét: parse SVG path (lệnh M/L/Q/C/Z, có sample bezier bậc 2 và 3)
      thành đa giác rồi tô đặc (ImageDraw.polygon) — đây chính là outline nét
      chữ thật của Make Me a Hanzi, không phải hình chữ nhật/khối xấp xỉ.
    - Dùng thêm `medians` (đường xương trung tâm của nét, cũng cùng hệ toạ độ)
      để vẽ hiệu ứng "đầu bút chạy dọc nét" trước khi nét đó tô đặc — cho cảm
      giác viết tay thay vì chỉ hiện phẳng.
    - Frame cuối mỗi nét: các nét trước + nét hiện tại đều tô đen (cumulative
      reveal đúng yêu cầu "mỗi frame hiện thêm 1 nét").
    - Có vẽ khung ô vuông + đường tim ngang/dọc kiểu 田字格 làm nền tham chiếu.

Giới hạn đã biết:
    - Chỉ chấp nhận 1 ký tự Hán mỗi lần chạy (không xử lý cụm từ nhiều chữ).
    - Polygon fill dùng luật tô đơn giản của Pillow; với các nét có phần nét
      tự giao cắt phức tạp, hình có thể tô hơi khác 1 chút so với font gốc —
      chấp nhận được cho mục đích minh hoạ thứ tự nét trong slide.

Chỉ dùng Pillow + stdlib (urllib để tải cache nếu thiếu, không cài package).
"""
import sys
import argparse
import json
import re
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from PIL import Image, ImageDraw

GRAPHICS_URL = "https://raw.githubusercontent.com/skishore/makemeahanzi/master/graphics.txt"

_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent.parent
VOCAB_STUDY_CACHE = _REPO_ROOT / ".claude/skills/vocab-study/data/_src/graphics.txt"
LOCAL_CACHE = _SCRIPT_DIR / "_src" / "graphics.txt"

# --- Canvas / transform -------------------------------------------------
# Vẽ ở độ phân giải gấp SS lần rồi downsize LANCZOS về OUT_CANVAS trước khi
# ghép GIF — Pillow polygon/line không có anti-alias ở độ phân giải gốc nên
# nét cong/móc bị răng cưa ("gãy gãy"); supersample+downsize là cách rẻ nhất
# để làm mượt mà không phải tự viết rasterizer AA.
SS = 3
OUT_CANVAS = 440
CANVAS = OUT_CANVAS * SS
MARGIN = 40 * SS
PLOT = CANVAS - 2 * MARGIN
GRID_COLOR = (222, 222, 222)
STROKE_COLOR = (25, 25, 25)
TRAIL_COLOR = (196, 30, 40)
BG = (255, 255, 255)


def resolve_graphics_path():
    """Tìm graphics.txt: cache vocab-study -> cache local -> tải mới."""
    if VOCAB_STUDY_CACHE.exists():
        return VOCAB_STUDY_CACHE
    if LOCAL_CACHE.exists():
        return LOCAL_CACHE
    LOCAL_CACHE.parent.mkdir(parents=True, exist_ok=True)
    print(f"[gen_stroke_gif] Không tìm thấy graphics.txt cache, đang tải từ "
          f"Make Me a Hanzi ({GRAPHICS_URL}) về {LOCAL_CACHE} ...", file=sys.stderr)
    urllib.request.urlretrieve(GRAPHICS_URL, LOCAL_CACHE)
    return LOCAL_CACHE


def find_character(hanzi, graphics_path):
    with open(graphics_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # short-circuit trước khi json.loads để đỡ tốn cho 30MB file
            if f'"character":"{hanzi}"' not in line:
                continue
            obj = json.loads(line)
            if obj.get("character") == hanzi:
                return obj
    return None


# --- SVG path parser (M / L / Q / C / Z) --------------------------------
_TOKEN_RE = re.compile(r"[MLQCZ]|-?\d+(?:\.\d+)?")


def parse_svg_path(d):
    """Flatten 1 path SVG (outline nét, đã fill) thành list điểm (x,y)."""
    tokens = _TOKEN_RE.findall(d)
    i = 0
    cmd = None
    cur = (0.0, 0.0)
    start = (0.0, 0.0)
    pts = []

    def quad(p0, p1, p2, n=22):
        for k in range(n + 1):
            t = k / n
            mt = 1 - t
            x = mt * mt * p0[0] + 2 * mt * t * p1[0] + t * t * p2[0]
            y = mt * mt * p0[1] + 2 * mt * t * p1[1] + t * t * p2[1]
            pts.append((x, y))

    def cubic(p0, p1, p2, p3, n=26):
        for k in range(n + 1):
            t = k / n
            mt = 1 - t
            x = mt ** 3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t ** 3 * p3[0]
            y = mt ** 3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t ** 3 * p3[1]
            pts.append((x, y))

    while i < len(tokens):
        tk = tokens[i]
        if tk in "MLQCZ":
            cmd = tk
            i += 1
            continue
        if cmd == "M":
            x, y = float(tokens[i]), float(tokens[i + 1])
            i += 2
            cur = (x, y)
            start = cur
            pts.append(cur)
        elif cmd == "L":
            x, y = float(tokens[i]), float(tokens[i + 1])
            i += 2
            cur = (x, y)
            pts.append(cur)
        elif cmd == "Q":
            x1, y1, x, y = (float(tokens[i]), float(tokens[i + 1]),
                             float(tokens[i + 2]), float(tokens[i + 3]))
            i += 4
            quad(cur, (x1, y1), (x, y))
            cur = (x, y)
        elif cmd == "C":
            x1, y1, x2, y2, x, y = (float(tokens[i]), float(tokens[i + 1]),
                                     float(tokens[i + 2]), float(tokens[i + 3]),
                                     float(tokens[i + 4]), float(tokens[i + 5]))
            i += 6
            cubic(cur, (x1, y1), (x2, y2), (x, y))
            cur = (x, y)
        elif cmd == "Z":
            pts.append(start)
            cur = start
        else:
            i += 1
    return pts


def to_canvas(pt):
    """Toạ độ Make Me a Hanzi (1024 box, y lên trên) -> pixel canvas.

    Đã kiểm chứng bằng cách render thử ký tự 你: dùng y' = 900 - y thì chữ
    hiện đúng chiều (không lộn ngược).
    """
    x, y = pt
    yy = 900 - y
    return (MARGIN + x / 1024 * PLOT, MARGIN + yy / 1024 * PLOT)


def smooth_polyline(points, samples_per_seg=10):
    """Catmull-Rom qua các điểm median (thường chỉ 2-5 điểm/nét, thẳng đơ) ->
    đường cong mượt. median gốc là polyline thẳng nối các điểm rời rạc nên
    "đầu bút chạy" theo nó trông GÃY KHÚC ở mỗi điểm gấp; nội suy Catmull-Rom
    cho tiếp tuyến liên tục nên trail cong mượt tự nhiên như nét bút thật."""
    n = len(points)
    if n < 3:
        return list(points)

    def cr(p0, p1, p2, p3, t):
        t2 = t * t
        t3 = t2 * t
        x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                   (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                   (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
        y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                   (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                   (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
        return (x, y)

    ext = [points[0]] + list(points) + [points[-1]]
    out = [ext[1]]
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for k in range(1, samples_per_seg + 1):
            out.append(cr(p0, p1, p2, p3, k / samples_per_seg))
    return out


def sample_polyline_fraction(points, t_max):
    """Trả về đoạn đầu của polyline `points` ứng với tỉ lệ t_max (0..1),
    nội suy tuyến tính điểm cuối cho mượt (theo index, không theo arc-length —
    đủ dùng cho hiệu ứng "đầu bút chạy" ở mức spike)."""
    if not points or t_max <= 0:
        return []
    n = len(points)
    if n == 1:
        return [points[0]]
    pos = t_max * (n - 1)
    idx = int(pos)
    frac = pos - idx
    result = [points[j] for j in range(min(idx + 1, n))]
    if idx + 1 < n and frac > 0:
        x0, y0 = points[idx]
        x1, y1 = points[idx + 1]
        result.append((x0 + (x1 - x0) * frac, y0 + (y1 - y0) * frac))
    return result


def draw_grid(draw):
    x0, y0, x1, y1 = MARGIN, MARGIN, MARGIN + PLOT, MARGIN + PLOT
    draw.rectangle([x0, y0, x1, y1], outline=GRID_COLOR, width=2 * SS)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    draw.line([(cx, y0), (cx, y1)], fill=GRID_COLOR, width=1 * SS)
    draw.line([(x0, cy), (x1, cy)], fill=GRID_COLOR, width=1 * SS)
    draw.line([(x0, y0), (x1, y1)], fill=GRID_COLOR, width=1 * SS)
    draw.line([(x1, y0), (x0, y1)], fill=GRID_COLOR, width=1 * SS)


def build_frames(strokes_raw, medians_raw, trail_steps=6, hold=8):
    strokes_px = [[to_canvas(p) for p in parse_svg_path(s)] for s in strokes_raw]
    medians_px = [smooth_polyline([to_canvas((p[0], p[1])) for p in m])
                  for m in medians_raw]

    frames = []

    def new_canvas():
        img = Image.new("RGB", (CANVAS, CANVAS), BG)
        d = ImageDraw.Draw(img)
        draw_grid(d)
        return img, d

    def fill_upto(d, upto_idx):
        for i in range(upto_idx + 1):
            pts = strokes_px[i]
            if len(pts) > 2:
                d.polygon(pts, fill=STROKE_COLOR)

    def downsize(img):
        return img.resize((OUT_CANVAS, OUT_CANVAS), Image.LANCZOS)

    n = len(strokes_px)
    for i in range(n):
        median = medians_px[i] if i < len(medians_px) else []
        for step in range(1, trail_steps + 1):
            img, d = new_canvas()
            fill_upto(d, i - 1)
            t_max = step / trail_steps
            trail = sample_polyline_fraction(median, t_max)
            if len(trail) > 1:
                d.line(trail, fill=TRAIL_COLOR, width=9 * SS, joint="curve")
            if trail:
                tx, ty = trail[-1]
                r = 6 * SS
                d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=TRAIL_COLOR)
            frames.append(downsize(img))
        # nét thứ i hoàn tất -> tô đặc
        img, d = new_canvas()
        fill_upto(d, i)
        frames.append(downsize(img))

    frames.extend([frames[-1].copy() for _ in range(hold)])
    return frames


def build_gif(hanzi, out_path, duration=110):
    graphics_path = resolve_graphics_path()
    obj = find_character(hanzi, graphics_path)
    if obj is None:
        raise SystemExit(f"Không tìm thấy '{hanzi}' trong Make Me a Hanzi graphics.txt")

    strokes_raw = obj["strokes"]
    medians_raw = obj.get("medians", [[] for _ in strokes_raw])
    frames = build_frames(strokes_raw, medians_raw)

    frames[0].save(
        out_path,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=False,
        disposal=2,
    )
    return len(frames), len(strokes_raw)


def main():
    parser = argparse.ArgumentParser(description="Sinh GIF thứ tự nét chữ Hán (Make Me a Hanzi).")
    parser.add_argument("hanzi", help="1 chữ Hán, vd 你")
    parser.add_argument("out", help="Đường dẫn file .gif xuất ra")
    args = parser.parse_args()

    if len(args.hanzi) != 1:
        raise SystemExit("Chỉ hỗ trợ đúng 1 ký tự Hán mỗi lần chạy (spike chưa hỗ trợ cụm từ).")

    n_frames, n_strokes = build_gif(args.hanzi, args.out)
    print(f"OK: {args.out} ({n_frames} frames, {n_strokes} nét, chữ {args.hanzi})")


if __name__ == "__main__":
    main()
