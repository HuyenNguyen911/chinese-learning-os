#!/usr/bin/env python3
"""gen_overview_diagram.py — sơ đồ cây tĩnh tổng quan cấu trúc 拼音,
dùng cho slide "tổng quan" thay bullet "Mục tiêu hôm nay" (buổi 01 ngữ âm).

Vẽ 3 tầng: 拼音 (root) -> 声母/韵母/声调 (nhánh) -> nhóm con (lá), nối bằng
đường thẳng đơn giản (không cần org-chart connector 2 đoạn) để giữ code gọn.
Màu lấy theo đúng theme mặc định của build_deck.py (accent đỏ) cho đồng bộ.

CLI:
    gen_overview_diagram.py <out.png>
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 2000, 980
BG = (255, 255, 255)
ACCENT = (142, 43, 32)
ACCENT_SOFT = (247, 228, 225)
INK = (31, 41, 51)
MUTED = (107, 118, 131)
BAND = (244, 245, 247)
LINE = (196, 150, 145)


def _font(size, bold=False):
    names = (["arialbd.ttf", "Arial Bold.ttf"] if bold else []) + ["arial.ttf", "Arial.ttf", "DejaVuSans.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _font_cjk(size, bold=False):
    # Arial không có glyph Hán -> tofu (□). Dùng Microsoft YaHei (đúng
    # cjk_font mặc định của build_deck.py) cho các nhãn thuần chữ Hán.
    names = (["msyhbd.ttc"] if bold else []) + ["msyh.ttc", "simhei.ttf", "arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


F_ROOT = _font_cjk(38, bold=True)
F_ROOT_SUB = _font(20)
F_BRANCH = _font_cjk(29, bold=True)
F_BRANCH_SUB = _font(19)
F_LEAF = _font(21, bold=True)
F_LEAF_SUB = _font(17)
F_DEMO_LABEL = _font(19, bold=True)
F_DEMO_HZ = _font_cjk(64, bold=True)
F_DEMO_PART = _font_cjk(30, bold=True)
F_DEMO_PLUS = _font(26, bold=True)
F_DEMO_TAG = _font_cjk(15, bold=True)
F_DEMO_SUB = _font(15)


def text_center(draw, xy, text, font, fill):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((x - w / 2, y - bbox[1] - (bbox[3] - bbox[1]) / 2), text, font=font, fill=fill)


def wrap_words(draw, text, font, max_w):
    words = text.split(" ")
    lines, line = [], ""
    for w_ in words:
        trial = (line + " " + w_).strip()
        if draw.textlength(trial, font=font) > max_w and line:
            lines.append(line); line = w_
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


def box(draw, cx, cy, w, h, fill, outline, radius=14, width=2):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)


BRANCHES = [
    {
        "label": "声母", "sub": "21 âm · 6 nhóm",
        "leaves": [
            ("Môi", "b p m f"),
            ("Đầu lưỡi", "d t n l"),
            ("Gốc lưỡi", "g k h"),
            ("Mặt lưỡi phẳng", "j q x"),
            ("Cong lưỡi", "zh ch sh r"),
            ("Đầu lưỡi phẳng", "z c s"),
        ],
    },
    {
        "label": "韵母", "sub": "nguyên âm",
        "leaves": [
            ("Đơn", "a o e i u ü"),
            ("Kép", "ai ei ao ou"),
            ("Mũi", "an en ang eng in ing"),
        ],
    },
    {
        "label": "声调", "sub": "4 thanh + khinh thanh",
        "leaves": [
            ("1", "ngang cao"),
            ("2", "đi lên"),
            ("3", "xuống-lên"),
            ("4", "đi xuống"),
            ("5", "nhẹ"),
        ],
    },
]


# Ví dụ ghép âm tiết thật (妈 mā) để lấp vùng trống dưới 韵母/声调 (2 nhánh
# chỉ có 1 hàng lá, trong khi 声母 có 2 hàng) — đồng thời minh hoạ trực quan
# câu caption "3 phần ghép thành 1 âm tiết" thay vì chỉ nói suông.
DEMO_PARTS = [
    ("m", "声母"),
    ("a", "韵母"),
    ("tonebar", "声调 1"),
]


def build(out_path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    root_cx, root_cy = W / 2, 110
    box(d, root_cx, root_cy, 380, 130, ACCENT, ACCENT)
    text_center(d, (root_cx, root_cy - 20), "拼音", F_ROOT, (255, 255, 255))
    text_center(d, (root_cx, root_cy + 28), "pīnyīn — phiên âm", F_ROOT_SUB, (247, 228, 225))

    n = len(BRANCHES)
    col_w = W / n
    branch_cy = 300
    leaf_top = 480
    leaf_h = 190
    row_gap = 16

    for i, br in enumerate(BRANCHES):
        bcx = col_w * i + col_w / 2
        d.line([(root_cx, root_cy + 65), (bcx, branch_cy - 64)], fill=LINE, width=3)
        box(d, bcx, branch_cy, col_w - 60, 128, ACCENT_SOFT, ACCENT)
        text_center(d, (bcx, branch_cy - 22), br["label"], F_BRANCH, ACCENT)
        text_center(d, (bcx, branch_cy + 24), br["sub"], F_BRANCH_SUB, INK)

        leaves = br["leaves"]
        m = len(leaves)
        # >5 lá (vd 声母 có 6 nhóm) thì xếp 2 hàng — 1 hàng bị chật, tên nhóm
        # dài ("Mặt lưỡi phẳng") đè lên ô bên cạnh.
        cols = m if m <= 5 else -(-m // 2)
        leaf_w = (col_w - 60) / cols
        for j, (lab, sub) in enumerate(leaves):
            r, c = divmod(j, cols)
            lcx = col_w * i + 30 + leaf_w * c + leaf_w / 2
            lcy = leaf_top + leaf_h / 2 + r * (leaf_h + row_gap)
            if r == 0:
                d.line([(bcx, branch_cy + 64), (lcx, leaf_top - 10)], fill=LINE, width=2)
            box(d, lcx, lcy, leaf_w - 14, leaf_h - 14, BAND, MUTED, radius=10, width=1)
            lab_lines = wrap_words(d, lab, F_LEAF, leaf_w - 24)
            ly_ = lcy - leaf_h / 2 + 42
            for ln in lab_lines:
                text_center(d, (lcx, ly_), ln, F_LEAF, INK)
                ly_ += 27
            sub_lines = wrap_words(d, sub, F_LEAF_SUB, leaf_w - 26)
            sy = ly_ + 12
            for ln in sub_lines:
                text_center(d, (lcx, sy), ln, F_LEAF_SUB, MUTED)
                sy += 23

    # --- demo ghép âm tiết: lấp vùng trống hàng 2 dưới 韵母 + 声调 ---
    demo_top = leaf_top + leaf_h + row_gap
    demo_bottom = H - 40
    demo_left = col_w * 1 + 30
    demo_right = col_w * 3 - 30
    demo_cx = (demo_left + demo_right) / 2
    demo_cy = (demo_top + demo_bottom) / 2
    box(d, demo_cx, demo_cy, demo_right - demo_left, demo_bottom - demo_top,
        (255, 255, 255), ACCENT, radius=16, width=2)
    text_center(d, (demo_cx, demo_top + 30), "Ví dụ ghép âm tiết", F_DEMO_LABEL, ACCENT)

    row_y = demo_cy + 14
    part_w = 150
    gap_w = 70
    total_parts_w = len(DEMO_PARTS) * part_w + (len(DEMO_PARTS) - 1) * gap_w
    eq_w = 90
    result_w = 420
    total_w = total_parts_w + eq_w + result_w
    x = demo_cx - total_w / 2 + part_w / 2

    for idx, (part, tag) in enumerate(DEMO_PARTS):
        box(d, x, row_y, part_w, 118, ACCENT_SOFT, ACCENT, radius=12, width=2)
        if part == "tonebar":
            # Vẽ thanh ngang thay vì trông cậy glyph macron (dễ tofu/khó đọc)
            # — trực quan hoá đúng hình dáng thanh 1 (ngang cao, phẳng).
            bw = 64
            d.line([(x - bw / 2, row_y - 14), (x + bw / 2, row_y - 14)],
                  fill=ACCENT, width=7)
        else:
            text_center(d, (x, row_y - 14), part, F_DEMO_PART, ACCENT)
        text_center(d, (x, row_y + 36), tag, F_DEMO_TAG, MUTED)
        x += part_w / 2
        if idx < len(DEMO_PARTS) - 1:
            x += gap_w / 2
            text_center(d, (x, row_y), "+", F_DEMO_PLUS, INK)
            x += gap_w / 2 + part_w / 2
        else:
            x += gap_w / 2

    x += eq_w / 2
    text_center(d, (x, row_y), "=", F_DEMO_PLUS, INK)
    x += eq_w / 2

    result_cx = x + result_w / 2
    box(d, result_cx, row_y, result_w, 130, ACCENT, ACCENT, radius=14, width=2)
    text_center(d, (result_cx - 90, row_y), "妈", F_DEMO_HZ, (255, 255, 255))
    text_center(d, (result_cx + 65, row_y - 22), "mā", F_DEMO_PART, (255, 255, 255))
    text_center(d, (result_cx + 65, row_y + 22), "mẹ", F_DEMO_SUB, ACCENT_SOFT)

    img.save(out_path)
    return out_path


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: gen_overview_diagram.py <out.png>")
    build(sys.argv[1])
    print(f"OK: {sys.argv[1]}")


if __name__ == "__main__":
    main()
