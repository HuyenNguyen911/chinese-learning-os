"""Cắt từng đoạn clip minh hoạ cho khớp lời đọc rồi tách thành ảnh JPG từng khung -> public/frames/<id>/0001.jpg… + src/frames.json.

  python make_frames.py

Vì sao không phát mp4 trực tiếp: trên máy này OffthreadVideo của Remotion hay lỗi ngẫu nhiên
"No frame found at position …" (lỗi ở clip/khung khác nhau mỗi lần render). Hiển thị ảnh tĩnh thì ổn định.
Tốc độ: clip gốc 10s được nén/giãn (0.8–1.6×) cho vừa đoạn đọc; USE = chỉ dùng X giây đầu; dư thì giữ khung cuối.
"""
import json, shutil, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
t = json.loads((here / "src/timing.json").read_text(encoding="utf-8"))
idx = json.loads((here / "src/lines.json").read_text(encoding="utf-8"))["idx"]
CH, ANS = t["chars"], t["end"]
# phải khớp CLIPS / USE trong src/Full.tsx
CLIPS = [(1, 2, "K1"), (3, 3, "K2"), (4, 6, "K3"), (7, 8, "K4"), (9, 10, "K5"), (11, 11, "K6"), (12, 13, "K7"), (14, 15, "K8"),
         (16, 17, "K9"), (18, 20, "K10"), (21, 21, "K11"), (22, 23, "K12"), (24, 24, "K13"), (25, 25, "K13b"), (26, 26, "K14"), (27, 28, "K15")]
USE: dict[str, float] = {"K9": 9.0, "K12": 6.0, "K13": 5.5, "K13b": 5.0}
START: dict[str, float] = {"K9": 1.0}   # bỏ đoạn đầu lỗi (đổi nền / giật khung)
TAIL = 3.0          # dư thêm (giây) so với đoạn đọc: phủ phần chồng mờ trước/sau + đoạn cuối kéo tới outro

res = {}
for a, b, k in CLIPS:
    s = CH[idx[a - 1]]
    e = CH[idx[b]] if b < len(idx) else ANS
    dur = e - s
    use = USE.get(k, 10)
    rate = min(1.6, max(0.8, use / dur))
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
