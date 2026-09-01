#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_articulation_gif.py — tô lại theo theme + crop cận cảnh + GIF pulse
tại điểm cấu âm, thay 7 ảnh tĩnh vị trí phát âm (buổi 01 ngữ âm).

Nguồn: Richard Weiss, Wikimedia Commons, public domain (xem
credits_articulation.json) — silhouette đầu người nhìn nghiêng, khoang
miệng là vùng TRONG SUỐT (không phải trắng — đã kiểm chứng bằng getcolors
RGBA), có 1 chấm đỏ đánh dấu điểm cấu âm. Ảnh gốc để nguyên cả đầu người,
thu nhỏ vào 1 cột bảng slide thì điểm cấu âm bé xíu, khó xem, lại đen trắng
đơn điệu — user feedback buổi 01 rework 2026-07-24.

Script này KHÔNG vẽ lại giải phẫu từ đầu (rủi ro amateur cao hơn ảnh gốc
chuẩn ngôn ngữ học) mà biến ảnh gốc thành asset khớp theme + động:
  1. Tô lại: silhouette đen -> ACCENT_DARK (theme), giữ nguyên kênh alpha
     (khoang trong suốt vẫn trong suốt khi đặt lên slide trắng, cạnh
     anti-alias vẫn mượt vì chỉ đổi RGB không đổi alpha).
  2. Tìm bbox chấm đỏ gốc -> crop vuông cận cảnh quanh điểm cấu âm rồi
     upscale — phóng to đúng chỗ cần nhìn thay vì cả đầu người.
  3. Animate: vòng tròn pulse (giãn + mờ dần) lặp tại điểm cấu âm, dùng màu
     accent đỏ của theme — GIF thể hiện rõ "âm phát ra ở ĐÂY".

CLI:
    gen_articulation_gif.py <in.png> <out.gif>
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ACCENT_DARK = (95, 22, 13)
ACCENT = (142, 43, 32)
OUT_SIZE = 640
CROP_FRAC = 0.36  # nửa cạnh ô crop = tỉ lệ này * min(W, H) ảnh gốc
N_FRAMES = 16
DURATION = 75
HOLD_FRAMES = 4  # giữ khung không pulse trước khi lặp lại, dễ đọc hơn


def _is_red(r, g, b):
    return r > 150 and g < 100 and b < 100


def find_dot_center(im):
    """Trọng tâm các pixel đỏ (chấm điểm cấu âm) trên ảnh GỐC (trước khi
    tô lại) — sample lưới thưa cho nhanh, ảnh chỉ có 1 cụm đỏ nên đủ chính
    xác."""
    w, h = im.size
    px = im.load()
    xs, ys = [], []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b, a = px[x, y]
            if a > 0 and _is_red(r, g, b):
                xs.append(x)
                ys.append(y)
    if not xs:
        return w / 2, h / 2
    return sum(xs) / len(xs), sum(ys) / len(ys)


def recolor(im):
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            if _is_red(r, g, b):
                px[x, y] = (ACCENT[0], ACCENT[1], ACCENT[2], a)
            else:
                px[x, y] = (ACCENT_DARK[0], ACCENT_DARK[1], ACCENT_DARK[2], a)
    return im


def crop_and_scale(im, dot_x, dot_y):
    w, h = im.size
    half = CROP_FRAC * min(w, h)
    x0, y0 = dot_x - half, dot_y - half
    x1, y1 = dot_x + half, dot_y + half
    # dồn khung crop vào trong biên ảnh (không co dãn kích thước) nếu chấm
    # nằm sát mép — vd artic_moi có chấm gần mép trái.
    if x0 < 0:
        x1 -= x0; x0 = 0
    if y0 < 0:
        y1 -= y0; y0 = 0
    if x1 > w:
        x0 -= (x1 - w); x1 = w
    if y1 > h:
        y0 -= (y1 - h); y1 = h
    x0 = max(0, x0); y0 = max(0, y0)
    crop = im.crop((int(x0), int(y0), int(x1), int(y1)))
    crop = crop.resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS)
    scale = OUT_SIZE / (x1 - x0)
    new_dot = ((dot_x - x0) * scale, (dot_y - y0) * scale)
    return crop, new_dot


def build_frames(base, dot):
    dx, dy = dot
    frames = []
    r_min, r_max = 16, 130
    for i in range(N_FRAMES):
        t = i / (N_FRAMES - 1)
        frame = base.copy()
        overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)
        radius = r_min + (r_max - r_min) * t
        alpha = int(200 * (1 - t))
        width = max(2, int(9 * (1 - 0.6 * t)))
        d.ellipse([dx - radius, dy - radius, dx + radius, dy + radius],
                  outline=(*ACCENT, alpha), width=width)
        frame = Image.alpha_composite(frame, overlay)
        frames.append(frame.convert("RGB"))
    frames.extend([frames[0].copy() for _ in range(HOLD_FRAMES)])
    return frames


def build(in_path, out_path):
    orig = Image.open(in_path).convert("RGBA")
    dot_x, dot_y = find_dot_center(orig)
    colored = recolor(orig)
    crop, dot = crop_and_scale(colored, dot_x, dot_y)
    # nền trắng đặc dưới lớp trong suốt trước khi lưu GIF (GIF palette-based
    # không giữ alpha mượt cho ảnh có antialiasing) — khớp nền trắng của
    # slide nên không lộ viền.
    bg = Image.new("RGBA", crop.size, (255, 255, 255, 255))
    crop = Image.alpha_composite(bg, crop)
    frames = build_frames(crop, dot)
    frames[0].save(
        out_path, format="GIF", save_all=True, append_images=frames[1:],
        duration=DURATION, loop=0, optimize=False, disposal=2,
    )
    return len(frames)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: gen_articulation_gif.py <in.png> <out.gif>")
    n = build(sys.argv[1], sys.argv[2])
    print(f"OK: {sys.argv[2]} ({n} frames)")


if __name__ == "__main__":
    main()
