"""Tách khung JPG cho từng đoạn muse-video (mỗi câu 1 đoạn) -> public/frames/<clip>/0001.jpg…
Độ dài lấy theo src/durations.json + bảng SC (phải khớp SC trong src/Clip.tsx). Chạy lại sau khi đổi giọng/clip.
public/frames/ gitignored — máy khác phải chạy lại."""
import json, os, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
D = json.load(open("src/durations.json")); GAP = 0.3
SC = [("m_walk", 2.4), ("m_ask", "l1b"), ("m_p2", "l2"), ("m_p3", "l3"), ("m_p4", "l4"), ("m_p5", "l5"), ("m_p6", "l6"), ("m_p7", "l7"), ("m_look", 1.6), ("m_q", "l9")]
secs = {}
for c, v in SC: secs[c] = secs.get(c, 0) + (v if isinstance(v, float) else D[v] + GAP)
for c, s in secs.items():
    s += 0.9; d = f"public/frames/{c}"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"assets/motion/{c}.mp4", "-t", str(s), "-vf", "fps=30", "-q:v", "3", f"{d}/%04d.jpg"], check=True)
    print(c, round(s, 2), len(os.listdir(d)))
