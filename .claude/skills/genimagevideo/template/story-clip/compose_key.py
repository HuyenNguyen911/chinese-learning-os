"""Ghép khung khởi đầu: nền công viên trống (assets/bg_park.png) + cặp nhân vật đã tách nền (assets/<pair>.png).
  python compose_key.py <pair> <out_id> [h=0.42] [feet=0.74] [cx=0.5]
h = chiều cao nhân vật / chiều cao khung; feet = vị trí chân (0..1 từ trên); cx = tâm ngang.
-> assets/keyframes/<out_id>.png (cùng cỡ nền, đưa thẳng vào gen_motion.py)."""
import sys
from PIL import Image, ImageDraw, ImageFilter
pair, oid = sys.argv[1], sys.argv[2]
h = float(sys.argv[3]) if len(sys.argv) > 3 else 0.42
feet = float(sys.argv[4]) if len(sys.argv) > 4 else 0.74
cx = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
bg = Image.open("assets/bg_park.png").convert("RGBA"); W, H = bg.size
ch = Image.open(f"assets/{pair}.png").convert("RGBA")
th = int(H * h); tw = int(ch.width * th / ch.height); ch = ch.resize((tw, th), Image.LANCZOS)
x = int(W * cx - tw / 2); y = int(H * feet - th)
# bóng mềm dưới chân
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
d.ellipse((x + tw * 0.06, y + th - 22, x + tw * 0.94, y + th + 14), fill=(90, 80, 60, 70))
bg = Image.alpha_composite(bg, sh.filter(ImageFilter.GaussianBlur(9)))
bg.alpha_composite(ch, (x, y))
bg.convert("RGB").save(f"assets/keyframes/{oid}.png"); print(oid, (W, H), (tw, th), (x, y))
