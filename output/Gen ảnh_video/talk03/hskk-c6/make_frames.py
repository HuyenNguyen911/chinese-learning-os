"""Cắt từng đoạn clip minh hoạ cho khớp lời đọc rồi tách JPG từng khung -> public/frames/<id>/0001.jpg… + src/frames.json.

  python make_frames.py

Lịch cảnh đọc từ src/plan.json (Full.tsx dùng CHUNG file này -> không lệch): clips = [dòng đầu, dòng cuối, id] (dòng 1-based;
0 = lúc 现在开始; > số dòng = dòng ảo sau khi đọc xong theo virt); ["gap","gap",id] = khoảng lặng chèn TRƯỚC dòng gapLine
(giọng đọc ngắt ra, người đối diện nhép miệng hỏi). Giữ tốc độ thật (giãn nhẹ tới 0.8× khi clip ngắn hơn đoạn đọc), dư thì giữ khung cuối.
Không phát mp4 trực tiếp vì OffthreadVideo hay lỗi "No frame found" trên máy này.
"""
import json, shutil, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
t = json.loads((here / "src/timing.json").read_text(encoding="utf-8"))
idx = json.loads((here / "src/lines.json").read_text(encoding="utf-8"))["idx"]
NOW = json.loads((here / "src/intro.json").read_text(encoding="utf-8"))["now"]
P = json.loads((here / "src/plan.json").read_text(encoding="utf-8"))
CH, ANS, N = t["chars"], t["end"], len(idx)
GL, GAP = P["gapLine"], P["gap"]
CUT = CH[idx[GL - 1]]
chT = lambda i: CH[i] + (GAP if i >= idx[GL - 1] else 0)
lineT = lambda n: -(NOW + 0.7) if n == 0 else chT(idx[n - 1]) if n <= N else ANS + GAP + P["virt"][n - N - 1]
TAIL = 3.0

res = {}
for a, b, k in P["clips"]:
    s, e = (CUT, CUT + GAP) if a == "gap" else (lineT(a), CUT if b + 1 == GL else lineT(b + 1))
    dur = e - s
    use = P["use"].get(k, 10); st = P["start"].get(k, 0)
    rate = min(1.0, max(0.8, use / dur))
    d = here / "public/frames" / k
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    vf = (f"trim={st}:{st + use},setpts=(PTS-STARTPTS)/{rate:.4f},fps=30,tpad=stop_mode=clone:stop_duration=6,"
          f"trim=duration={dur + TAIL:.3f},scale=1000:-2")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(here / "assets/motion" / f"{k}.mp4"), "-vf", vf,
                    "-q:v", "3", str(d / "%04d.jpg")], check=True)
    res[k] = len(list(d.glob("*.jpg")))
    print(f"{k}: {s:.1f}–{e:.1f}s ({dur:.1f}s), tốc độ {rate:.2f}x, {res[k]} khung")
(here / "src/frames.json").write_text(json.dumps(res), encoding="utf-8")
