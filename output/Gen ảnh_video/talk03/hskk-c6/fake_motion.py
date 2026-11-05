"""Phương án dự phòng khi muse-video chết: dựng "chuyển động giả" từ ảnh tĩnh -> assets/motion/<id>.mp4 (10s, 24fps, 1152x768,
cùng định dạng clip muse nên make_frames.py dùng y nguyên).

  python fake_motion.py K10   # bão: đẩy máy chậm + nhún bước đi + rung gió + mưa xiên chạy thật + nắng đỉnh sáng dần
  python fake_motion.py K12   # đoạn muse cũ (đang nói) tới dòng 28 -> cắt sang cận cảnh tay đặt lên ngực (out/gen/K12h1.png), đẩy máy nhẹ

Bản muse cũ lưu ở out/old_motion/. Khi muse sống lại: python gen_motion.py K10 K12 (ghi đè file này tạo ra).
"""
import math, random, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageChops

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
W, H, FPS, DUR = 1152, 768, 24, 10.0
N = int(FPS * DUR)


def writer(path):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                             "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", str(path)], stdin=subprocess.PIPE)


def view(img, zoom, cx, cy, dx=0.0, dy=0.0):
    """cắt vùng zoom quanh (cx,cy) tỉ lệ 0..1 rồi đưa về W×H"""
    iw, ih = img.size
    cw, ch = iw / zoom, ih / zoom
    x0 = min(max(cx * iw - cw / 2 + dx, 0), iw - cw)
    y0 = min(max(cy * ih - ch / 2 + dy, 0), ih - ch)
    return img.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))


def k10():
    src = Image.open(here / "assets/keyframes/K10.png").convert("RGB")
    src = src.resize((src.width * 2, src.height * 2), Image.LANCZOS)  # dư điểm ảnh cho zoom
    rnd = random.Random(7)
    # mưa: gió thổi từ phải-trên xuống trái-dưới (ngược hướng cô đi)
    vx, vy = -0.55, 1.0
    drops = [[rnd.uniform(-200, W + 400), rnd.uniform(-H, H), rnd.uniform(0.8, 1.6), rnd.uniform(28, 70), rnd.randint(70, 150)] for _ in range(320)]
    gusts = [[rnd.uniform(0, W * 2), rnd.uniform(0.05, 0.9) * H, rnd.uniform(160, 380), rnd.uniform(0.6, 1.2)] for _ in range(10)]
    # quầng nắng góc phải-trên
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    for r in range(700, 0, -20):
        gd.ellipse((W * 0.88 - r, -r * 0.6, W * 0.88 + r, r * 0.6 + 20), fill=int(255 * (1 - r / 700) ** 1.6))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    gold = Image.new("RGB", (W, H), (255, 226, 150))
    p = writer(here / "assets/motion/K10.mp4")
    for i in range(N):
        t = i / FPS
        z = 1.0 + 0.10 * (t / DUR)
        bob = 7 * abs(math.sin(math.pi * t * 1.5))          # nhún theo bước
        sx, sy = 3 * math.sin(t * 23.0), 2 * math.cos(t * 19.0)  # rung gió
        fr = view(src, z, 0.42, 0.45, sx * 2, (sy - bob) * 2)
        # nắng sáng dần
        lv = 0.10 + 0.35 * (t / DUR)
        fr = Image.composite(gold, fr, glow.point(lambda v: int(v * lv)))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for g in gusts:  # vệt gió
            x = (g[0] - t * 900 * g[3]) % (W + 800) - 400
            d.line((x, g[1], x + g[2], g[1] - g[2] * 0.12), fill=(255, 255, 255, 55), width=6)
        for dr in drops:
            sp = 1500 * dr[2]
            y = (dr[1] + t * sp) % (H + 200) - 100
            x = (dr[0] + t * sp * vx) % (W + 600) - 200
            L = dr[3]
            d.line((x, y, x - vx * L, y - L), fill=(235, 242, 255, dr[4]), width=2)
        fr = Image.alpha_composite(fr.convert("RGBA"), ov.filter(ImageFilter.GaussianBlur(0.6))).convert("RGB")
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    print("K10: OK")


def k12(cut=3.575, xf=0.25):
    old = here / "out/old_motion/K12_v1.mp4"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(old), "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-"],
                         capture_output=True).stdout
    fsz = W * H * 3
    olds = [Image.frombytes("RGB", (W, H), raw[k:k + fsz]) for k in range(0, len(raw) - fsz + 1, fsz)]
    still = Image.open(here / "out/gen/K12h1.png").convert("RGB")
    # cận cảnh 瑾玄 (nửa trái ảnh), tỉ lệ 3:2
    sw, sh = still.size  # 1264x848; 瑾玄 ở x≈160-510, đầu y≈170
    box = (0, 70, 780, 590)
    close = still.crop(box)
    close = close.resize((close.width * 2, close.height * 2), Image.LANCZOS)
    p = writer(here / "assets/motion/K12.mp4")
    for i in range(N):
        t = i / FPS
        a = olds[min(i, len(olds) - 1)]
        b = view(close, 1.0 + 0.06 * max(0, t - cut) / (DUR - cut), 0.5, 0.45)
        w = min(1, max(0, (t - cut) / xf))
        fr = a if w == 0 else b if w == 1 else Image.blend(a, b, w)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    print("K12: OK")


for a in sys.argv[1:]:
    {"K10": k10, "K12": k12}[a]()
