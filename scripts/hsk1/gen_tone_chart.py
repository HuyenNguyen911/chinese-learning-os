#!/usr/bin/env python3
"""gen_tone_chart.py — ảnh tĩnh so sánh 4 đường cong thanh điệu + thanh 5,
dùng thay bullet-wall ở slide tổng quan 声调 (buổi 01 ngữ âm).

Tái dùng toạ độ/bezier từ gen_tone_gif.py (cùng canvas, cùng công thức
level_to_y/bezier_xy) để không lặp code — khác ở chỗ vẽ CẢ 4 đường cong
CÙNG 1 khung tĩnh (không animate).

Layout (rework theo feedback buổi 01 2026-07-24): mỗi ví dụ đặt NGAY BÊN
PHẢI, ngang hàng với ĐIỂM CUỐI của đường cong tương ứng (thay vì gom hết
xuống 1 dải chú giải bên dưới) — nhìn phát biết ví dụ nào khớp đường cong
nào. Bỏ dòng "người Việt hay lẫn..." (chuyển thành note gắn vào slide luyện
đọc thanh điệu liên quan, không in cứng vào ảnh).

Chú giải/caption trộn chữ Hán + tiếng Việt có dấu trong CÙNG 1 dòng — không
font nào Windows có sẵn phủ được cả 2 (Arial thiếu glyph Hán, Microsoft YaHei
thiếu vài dấu tiếng Việt như ẹ/ự/ắ/ỏ) nên phải tách RUN theo từng đoạn
CJK/Latin rồi vẽ nối tiếp bằng font tương ứng (draw_mixed).

CLI:
    gen_tone_chart.py <out.png>
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image, ImageDraw, ImageFont
from gen_tone_gif import (
    H, PLOT_Y0, PLOT_Y1, MARGIN_LEFT, MARGIN_TOP,
    BG, GRID, AXIS, TONE_LEVELS, level_to_y, bezier_xy, _font,
)

# Canvas rộng hơn bản gốc — dành hẳn 1 dải bên phải cho nhãn ví dụ thay vì
# 1 dải chú giải nằm ngang bên dưới.
PLOT_W = 560
LABEL_W = 360
W = MARGIN_LEFT + PLOT_W + LABEL_W
PLOT_X0 = MARGIN_LEFT
PLOT_X1 = MARGIN_LEFT + PLOT_W

CURVE_COLORS = {
    1: (196, 30, 40),    # đỏ - ngang cao
    2: (30, 130, 60),    # xanh lá - đi lên
    3: (30, 90, 196),    # xanh dương - xuống-lên
    4: (150, 60, 170),   # tím - đi xuống
}
TONE_EXAMPLE = {1: "妈", 2: "麻", 3: "马", 4: "骂", 5: "吗"}
TONE_PINYIN = {1: "mā", 2: "má", 3: "mǎ", 4: "mà", 5: "ma"}
TONE_MEANING = {1: "mẹ", 2: "cây gai", 3: "ngựa", 4: "mắng", 5: "(trợ từ hỏi)"}


def _font_cjk(size):
    for name in ("msyh.ttc", "simhei.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return _font(size)


FONT_TITLE = _font(24)
FONT_LABEL = _font(16)
FONT_EX_NUM = _font(19)
FONT_EX_HZ = _font_cjk(22)
FONT_EX_PY = _font(17)
FONT_EX_VN = _font(15)

_CJK_RE = re.compile(r"[一-鿿]")


def _segments(text):
    """Tách text thành các đoạn liên tiếp cùng loại (CJK / không-CJK)."""
    segs, cur, cur_cjk = [], "", None
    for ch in text:
        is_cjk = bool(_CJK_RE.match(ch))
        if cur_cjk is None:
            cur_cjk = is_cjk
        if is_cjk != cur_cjk:
            segs.append((cur, cur_cjk)); cur = ch; cur_cjk = is_cjk
        else:
            cur += ch
    if cur:
        segs.append((cur, cur_cjk))
    return segs


def draw_mixed(draw, xy, text, font_latin, font_cjk, fill):
    x, y = xy
    for seg, is_cjk in _segments(text):
        f = font_cjk if is_cjk else font_latin
        draw.text((x, y), seg, font=f, fill=fill)
        x += draw.textlength(seg, font=f)
    return x


def draw_axes(draw):
    for level in range(1, 6):
        y = level_to_y(level)
        draw.line([(PLOT_X0, y), (PLOT_X1, y)], fill=GRID, width=1)
        draw.text((MARGIN_LEFT - 30, y - 9), str(level), font=FONT_LABEL, fill=AXIS)
    draw.line([(PLOT_X0, PLOT_Y0), (PLOT_X0, PLOT_Y1)], fill=AXIS, width=2)
    draw.text((18, 20), "cao", font=FONT_LABEL, fill=AXIS)
    draw.text((16, PLOT_Y1 - 10), "thấp", font=FONT_LABEL, fill=AXIS)
    draw.text((MARGIN_LEFT, 20), "4 thanh điệu — so sánh đường cong",
              font=FONT_TITLE, fill=AXIS)


def curve_points(tone, n_samples=120):
    levels = TONE_LEVELS[tone]
    pts = [bezier_xy(levels, j / (n_samples - 1)) for j in range(n_samples)]
    return [(PLOT_X0 + x * (PLOT_X1 - PLOT_X0), y) for x, y in pts]


def draw_curve(draw, tone):
    pts_px = curve_points(tone)
    draw.line(pts_px, fill=CURVE_COLORS[tone], width=6, joint="curve")
    tx, ty = pts_px[-1]
    r = 8
    draw.ellipse([tx - r, ty - r, tx + r, ty + r], fill=CURVE_COLORS[tone])
    return tx, ty


def resolve_label_ys(ends, min_gap):
    """Nhận [(tone, end_y)] -> [(tone, end_y, label_y)] đã né chồng nhãn khi
    2 thanh kết thúc cùng mức (vd thanh 1 và 2 đều chạm mức 5/cao nhất)."""
    order = sorted(ends, key=lambda t: t[1])
    ys = [y for _, y in order]
    for i in range(1, len(ys)):
        if ys[i] - ys[i - 1] < min_gap:
            ys[i] = ys[i - 1] + min_gap
    return [(order[i][0], order[i][1], ys[i]) for i in range(len(order))]


H_TOTAL = H + 140  # thêm chỗ dưới đáy plot cho nhãn thanh 5 (không có contour)


def build_chart(out_path):
    img = Image.new("RGB", (W, H_TOTAL), BG)
    draw = ImageDraw.Draw(img)
    draw_axes(draw)

    ends = []
    for tone in (1, 2, 3, 4):
        tx, ty = draw_curve(draw, tone)
        ends.append((tone, ty))

    label_x = PLOT_X1 + 26
    resolved = resolve_label_ys(ends, min_gap=58)
    for tone, curve_y, label_y in resolved:
        # đường nối mảnh từ điểm cuối đường cong -> vị trí nhãn (khi bị né)
        if abs(label_y - curve_y) > 4:
            draw.line([(PLOT_X1 + 10, curve_y), (label_x - 8, label_y)],
                      fill=CURVE_COLORS[tone], width=1)
        r = 7
        cy = label_y
        draw.ellipse([label_x, cy - r, label_x + 2 * r, cy + r], fill=CURVE_COLORS[tone])
        tx = label_x + 2 * r + 10
        tx = draw_mixed(draw, (tx, cy - 13), f"{tone}  {TONE_EXAMPLE[tone]}",
                        FONT_EX_NUM, FONT_EX_HZ, AXIS)
        tx += 8
        draw_mixed(draw, (tx, cy - 11), TONE_PINYIN[tone], FONT_EX_PY, FONT_EX_PY,
                  CURVE_COLORS[tone])
        draw_mixed(draw, (label_x + 2 * r + 10, cy + 12),
                  f"— {TONE_MEANING[tone]}", FONT_EX_VN, FONT_EX_VN, (90, 90, 90))

    # Thanh 5 (khinh thanh, không đường cong) — đặt riêng dưới cùng dải nhãn,
    # đánh dấu bằng gạch ngang thay vì chấm tròn để phân biệt "không có contour".
    last_y = max(ly for _, _, ly in resolved) if resolved else level_to_y(3)
    y5 = max(last_y + 60, PLOT_Y1 - 20)
    draw.line([(label_x, y5), (label_x + 14, y5)], fill=AXIS, width=4)
    tx = label_x + 2 * 7 + 10
    tx = draw_mixed(draw, (tx, y5 - 13), f"5  {TONE_EXAMPLE[5]}", FONT_EX_NUM, FONT_EX_HZ, AXIS)
    tx += 8
    draw_mixed(draw, (tx, y5 - 11), TONE_PINYIN[5], FONT_EX_PY, FONT_EX_PY, (90, 90, 90))
    draw_mixed(draw, (label_x + 2 * 7 + 10, y5 + 12),
              f"— khinh thanh, {TONE_MEANING[5]}", FONT_EX_VN, FONT_EX_VN, (90, 90, 90))

    # Cắt bớt khoảng trắng dư ở đáy (chiều cao canvas ước lượng dư ra để chắc
    # chắn không tràn nhãn thanh 5, thường thừa hơn thực tế cần).
    gray = img.convert("L")
    bbox = Image.eval(gray, lambda p: 255 - p).getbbox()
    if bbox:
        img = img.crop((0, 0, W, min(H_TOTAL, bbox[3] + 24)))

    img.save(out_path)
    return out_path


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: gen_tone_chart.py <out.png>")
    build_chart(sys.argv[1])
    print(f"OK: {sys.argv[1]}")


if __name__ == "__main__":
    main()
