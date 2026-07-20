#!/usr/bin/env python3
"""gen_tone_gif.py — sinh GIF động minh hoạ đường cong thanh điệu tiếng Trung.

CLI:
    gen_tone_gif.py <tone:1-5> <out.gif>

Thanh:
    1 = ngang cao (55, flat)
    2 = đi lên (35, rising)
    3 = xuống rồi lên (214, dip)
    4 = đi xuống (51, falling)
    5 = khinh thanh (neutral, vẽ như một chấm ngắn, không có đường cong)

Chỉ dùng Pillow + stdlib. Vẽ lưới 5 mức thanh điệu (1 thấp nhất .. 5 cao nhất)
rồi "vẽ dần" đường cong tương ứng qua nhiều frame, xuất GIF động loop vô hạn.
"""
import sys
import argparse

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from PIL import Image, ImageDraw, ImageFont

# --- Cấu hình canvas ---------------------------------------------------
W, H = 640, 420
MARGIN_LEFT = 90
MARGIN_RIGHT = 50
MARGIN_TOP = 70
MARGIN_BOTTOM = 50

PLOT_X0 = MARGIN_LEFT
PLOT_X1 = W - MARGIN_RIGHT
PLOT_Y0 = MARGIN_TOP           # tương ứng level 5 (cao nhất)
PLOT_Y1 = H - MARGIN_BOTTOM    # tương ứng level 1 (thấp nhất)

BG = (255, 255, 255)
GRID = (215, 215, 215)
AXIS = (90, 90, 90)
CURVE = (196, 30, 40)
POINTER = (30, 90, 196)
TEXT = (40, 40, 40)

# Định nghĩa 5 mức Chao tone letters cho mỗi thanh (1=thấp nhất, 5=cao nhất).
# Số điểm control quyết định bậc bezier: 2 điểm = đường thẳng, 3 điểm = bezier bậc 2.
TONE_LEVELS = {
    1: [5, 5],       # 55 - ngang cao
    2: [3, 5],       # 35 - đi lên
    3: [2, 1, 4],    # 214 - xuống rồi lên (dip)
    4: [5, 1],       # 51 - đi xuống
    5: [2],          # khinh thanh - chấm, không có contour
}

TONE_LABEL = {
    1: "Thanh 1 · ngang cao (55)",
    2: "Thanh 2 · đi lên (35)",
    3: "Thanh 3 · xuống-lên (214)",
    4: "Thanh 4 · đi xuống (51)",
    5: "Thanh 5 · khinh thanh (nhẹ)",
}


def _font(size):
    for name in ("arial.ttf", "Arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = _font(22)
FONT_LABEL = _font(16)


def level_to_y(level):
    """level 1..5 -> toạ độ y trên canvas (5 = trên cùng)."""
    frac = (level - 1) / 4.0
    return PLOT_Y1 - frac * (PLOT_Y1 - PLOT_Y0)


def lerp(a, b, t):
    return a + (b - a) * t


def bezier_xy(levels, t):
    """De Casteljau trên danh sách level (x đặt đều 0..1)."""
    n = len(levels)
    pts = [(i / (n - 1) if n > 1 else 0.0, level_to_y(lv)) for i, lv in enumerate(levels)]
    while len(pts) > 1:
        pts = [
            (lerp(pts[i][0], pts[i + 1][0], t), lerp(pts[i][1], pts[i + 1][1], t))
            for i in range(len(pts) - 1)
        ]
    return pts[0]


def draw_base(draw, tone):
    # Lưới 5 mức thanh điệu.
    for level in range(1, 6):
        y = level_to_y(level)
        draw.line([(PLOT_X0, y), (PLOT_X1, y)], fill=GRID, width=1)
        draw.text((MARGIN_LEFT - 30, y - 9), str(level), font=FONT_LABEL, fill=AXIS)
    # Trục dọc bên trái.
    draw.line([(PLOT_X0, PLOT_Y0), (PLOT_X0, PLOT_Y1)], fill=AXIS, width=2)
    draw.text((18, MARGIN_TOP - 4), "cao", font=FONT_LABEL, fill=AXIS)
    draw.text((18, PLOT_Y1 - 10), "thấp", font=FONT_LABEL, fill=AXIS)
    # Tiêu đề.
    draw.text((MARGIN_LEFT, 20), TONE_LABEL[tone], font=FONT_TITLE, fill=TEXT)


def render_contour_frames(tone, steps=24, hold=8, dot_radius=7, line_width=6):
    levels = TONE_LEVELS[tone]
    frames = []

    for i in range(steps + 1):
        t_max = i / steps
        img = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(img)
        draw_base(draw, tone)

        # Vẽ polyline theo các điểm mẫu từ t=0 đến t_max.
        n_samples = max(2, int(120 * t_max) + 1)
        pts = [bezier_xy(levels, (j / (n_samples - 1)) * t_max) for j in range(n_samples)]
        pts_px = [(PLOT_X0 + x * (PLOT_X1 - PLOT_X0), y) for x, y in pts]
        if len(pts_px) > 1:
            draw.line(pts_px, fill=CURVE, width=line_width, joint="curve")

        # Con trỏ chạy ở đầu mút đường cong hiện tại.
        tip = pts_px[-1]
        r = dot_radius
        draw.ellipse([tip[0] - r, tip[1] - r, tip[0] + r, tip[1] + r], fill=POINTER)

        frames.append(img)

    # Giữ frame cuối vài nhịp để mắt kịp thấy trước khi lặp lại.
    frames.extend([frames[-1].copy() for _ in range(hold)])
    return frames


def render_dot_frames(tone, level=2, steps=14, hold=6, max_radius=14):
    """Thanh 5 (khinh thanh): không có contour, chỉ một chấm phồng lên rồi biến mất."""
    frames = []
    x_center = (PLOT_X0 + PLOT_X1) / 2
    y_center = level_to_y(level)

    radii = list(range(0, max_radius + 1, max(1, max_radius // steps)))
    radii = radii + radii[::-1][1:]  # phồng lên rồi xẹp xuống

    for r in radii:
        img = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(img)
        draw_base(draw, tone)
        if r > 0:
            draw.ellipse(
                [x_center - r, y_center - r, x_center + r, y_center + r],
                fill=CURVE,
            )
        frames.append(img)

    frames.extend([frames[-1].copy() for _ in range(hold)])

    # Frame đầu (chấm chưa xuất hiện) để loop mượt.
    blank = Image.new("RGB", (W, H), BG)
    draw_base(ImageDraw.Draw(blank), tone)
    frames = [blank] + frames
    return frames


def build_gif(tone, out_path, duration=90):
    if tone == 5:
        frames = render_dot_frames(tone)
    else:
        frames = render_contour_frames(tone)

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
    return len(frames)


def main():
    parser = argparse.ArgumentParser(description="Sinh GIF đường cong thanh điệu tiếng Trung.")
    parser.add_argument("tone", type=int, choices=[1, 2, 3, 4, 5], help="Thanh điệu 1-5")
    parser.add_argument("out", help="Đường dẫn file .gif xuất ra")
    args = parser.parse_args()

    n_frames = build_gif(args.tone, args.out)
    print(f"OK: {args.out} ({n_frames} frames, thanh {args.tone})")


if __name__ == "__main__":
    main()
