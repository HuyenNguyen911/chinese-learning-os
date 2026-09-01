#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_emoji_icon.py — Render 1 emoji (Windows Segoe UI Emoji, color glyph) lên
nền vuông bo góc màu nhạt, xuất PNG trong suốt xung quanh — dùng làm icon
minh hoạ nhanh, nhất quán màu, không phụ thuộc ảnh CC bên ngoài (nhiều chủ đề
bài học không tìm được ảnh CC liên quan trên Openverse).

Chạy: python gen_emoji_icon.py <emoji> <output.png> [bg_hex]
CHỈ dùng emoji 1 codepoint (không ZWJ) — PIL không ráp được chuỗi ghép.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT = r"C:\Windows\Fonts\seguiemj.ttf"
SIZE = 512


def make_icon(emoji, out_path, bg_hex="F7E4E1"):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r, g, b = (int(bg_hex[i:i+2], 16) for i in (0, 2, 4))
    pad = 18
    d.rounded_rectangle([pad, pad, SIZE - pad, SIZE - pad], radius=64,
                        fill=(r, g, b, 255))
    font = ImageFont.truetype(FONT, 300)
    bbox = d.textbbox((0, 0), emoji, font=font, embedded_color=True)
    w = bbox[2] - bbox[0]; h = bbox[3] - bbox[1]
    x = (SIZE - w) / 2 - bbox[0]
    y = (SIZE - h) / 2 - bbox[1]
    d.text((x, y), emoji, font=font, embedded_color=True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path))


if __name__ == "__main__":
    emoji = sys.argv[1]
    out = Path(sys.argv[2])
    bg = sys.argv[3] if len(sys.argv) > 3 else "F7E4E1"
    make_icon(emoji, out, bg)
    print("OK ->", out)
