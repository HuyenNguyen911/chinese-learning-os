"""Cắt từng đoạn clip minh hoạ cho khớp lời đọc rồi tách thành ảnh JPG từng khung -> public/frames/<id>/0001.jpg… + src/frames.json.

  python make_frames.py

Vì sao không phát mp4 trực tiếp: trên máy này OffthreadVideo của Remotion hay lỗi ngẫu nhiên
"No frame found at position …" (lỗi ở clip/khung khác nhau mỗi lần render). Hiển thị ảnh tĩnh thì ổn định.
Tốc độ: giữ tốc độ thật (chỉ giãn nhẹ tới 0.8× khi clip ngắn hơn đoạn đọc); USE = chỉ dùng X giây đầu; dư thì giữ khung cuối.
"""
import json, shutil, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
t = json.loads((here / "src/timing.json").read_text(encoding="utf-8"))
idx = json.loads((here / "src/lines.json").read_text(encoding="utf-8"))["idx"]
CH, ANS = t["chars"], t["end"]
NOW = json.loads((here / "src/intro.json").read_text(encoding="utf-8"))["now"]   # dòng 0 = lúc hiện 现在开始 (K1a)
# phải khớp CLIPS / USE trong src/Full.tsx
CLIPS = [(0, 0, "K1a"), (1, 2, "K1"), (3, 4, "K3"), (5, 6, "K5"), (7, 8, "K6"), (9, 10, "K7"), (11, 12, "K8"), (13, 13, "K9"), (14, 15, "K10"), (16, 17, "K11"), (18, 18, "K13"), (19, 20, "K14"), (21, 21, "K15a"), (22, 22, "K15b")]
VIRT = [0, 3.0, 7.5]   # mốc dòng ảo 21, 22, 23 sau khi đọc xong (K15a 3s, K15b 4,5s) — phải khớp VIRT trong Full.tsx
USE: dict[str, float] = {"K11": 5.0}  # clip muse-video trả ngắn hơn 10s
START: dict[str, float] = {"K15b": 0.3}   # bỏ đoạn đầu lỗi (đổi nền / giật khung)
TAIL = 3.0          # dư thêm (giây) so với đoạn đọc: phủ phần chồng mờ trước/sau + đoạn cuối kéo tới outro

res = {}
for a, b, k in CLIPS:
    line_t = lambda n: -(NOW + 0.7) if n == 0 else CH[idx[n - 1]] if n <= len(idx) else ANS + VIRT[n - len(idx) - 1]
    s, e = line_t(a), line_t(b + 1)
    dur = e - s
    use = USE.get(k, 10)
    rate = min(1.0, max(0.8, use / dur))
    need = dur + TAIL
    d = here / "public/frames" / k
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    st = START.get(k, 0)
    vf = (f"trim={st}:{st + use},setpts=(PTS-STARTPTS)/{rate:.4f},fps=30,tpad=stop_mode=clone:stop_duration=6,"
          f"trim=duration={need:.3f},scale=1000:-2")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(here / "assets/motion" / f"{k}.mp4"), "-vf", vf,
                    "-q:v", "3", str(d / "%04d.jpg")], check=True)
    n = len(list(d.glob("*.jpg")))
    res[k] = n
    print(f"{k}: đọc {dur:.1f}s, tốc độ {rate:.2f}x, {n} khung")
(here / "src/frames.json").write_text(json.dumps(res), encoding="utf-8")
