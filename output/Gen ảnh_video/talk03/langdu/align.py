"""Giọng đọc cả bài -> public/audio/read.wav (lọc nhẹ, cắt lặng đầu/cuối) + src/timing.json (giây bắt đầu của từng chữ).

  python align.py
Nguồn: public/audio/read.src.wav (TTS) hoặc read.m4a|mp3|wav do user thu.
Cách khớp: dò chỗ ngắt hơi (đoạn lặng >= MIN_PAUSE) -> ghép với ranh giới vế câu (dấu ，。、：；！？) bằng quy hoạch
động (mỗi ranh giới lấy chỗ ngắt gần mốc dự kiến nhất, theo đúng thứ tự; chỗ ngắt thừa bỏ qua) -> trong mỗi vế chia
đều thời gian cho từng chữ Hán. Dấu câu lấy mốc của chữ ngay trước nó. Cần ffmpeg + numpy.
"""
import json, re, subprocess, sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
audio = here / "public" / "audio"
SR, HOP = 16000, 160                 # 10 ms / khung
MIN_PAUSE, SIL_DB = 0.12, -32        # ngắt hơi tối thiểu (s), ngưỡng lặng so với đỉnh (dB)
BREAK = "，。、：；！？"

text = json.loads((here / "src" / "data.json").read_text(encoding="utf-8"))["text"]
src = next((p for p in [audio / "read.m4a", audio / "read.mp3", audio / "read.src.wav"] if p.exists()), None) or sys.exit("Thiếu file giọng")
out = audio / "read.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ar", "44100", "-ac", "1", "-af",
                "highpass=f=90,afftdn=nr=12:nf=-50:tn=1,"
                "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
                "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse", str(out)], check=True)
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(out), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
dur = len(x) / SR
rms = np.array([np.sqrt(np.mean(x[i:i + HOP * 2] ** 2) + 1e-12) for i in range(0, len(x) - HOP, HOP)])
db = 20 * np.log10(rms / (np.percentile(rms, 98) + 1e-9))
quiet = db < SIL_DB
pauses, i = [], 0                    # (bắt đầu, kết thúc) giây
while i < len(quiet):
    if quiet[i]:
        j = i
        while j < len(quiet) and quiet[j]: j += 1
        if (j - i) * HOP / SR >= MIN_PAUSE and i > 0 and j < len(quiet): pauses.append((i * HOP / SR, j * HOP / SR))
        i = j
    else:
        i += 1

# vế câu: [đầu, cuối) theo chỉ số chữ; ranh giới sau mỗi dấu ngắt
is_han = [bool(re.match(r"[一-鿿]", c)) for c in text]
cuts = [k + 1 for k, c in enumerate(text) if c in BREAK and k + 1 < len(text)]
spans = list(zip([0] + cuts, cuts + [len(text)]))
han_before = np.cumsum([0] + is_han)
H = han_before[-1]
expect = [han_before[c] / H * dur for c in cuts]          # mốc dự kiến: tỉ lệ số chữ Hán

# quy hoạch động: gán ranh giới -> chỗ ngắt (đơn điệu), ranh giới không ngắt bị phạt
B, P, MISS = len(cuts), len(pauses), 1.2
INF = 1e9
cost = np.full((B + 1, P + 1), INF); cost[0, :] = 0
back = np.zeros((B + 1, P + 1), dtype=np.int64)
mids = [(a + b) / 2 for a, b in pauses]
for bi in range(1, B + 1):
    for pj in range(0, P + 1):
        best, arg = cost[bi - 1, pj] + MISS, -1                  # ranh giới bi không có chỗ ngắt
        if pj > 0:
            c = cost[bi - 1, pj - 1] + abs(mids[pj - 1] - expect[bi - 1])
            if c < best: best, arg = c, pj - 1                   # ranh giới bi dùng chỗ ngắt pj-1
        if pj > 0 and cost[bi, pj - 1] < best: best, arg = cost[bi, pj - 1], -2   # bỏ qua chỗ ngắt pj-1
        cost[bi, pj], back[bi, pj] = best, arg
assign, bi, pj = [None] * B, B, P
while bi > 0:
    a = back[bi, pj]
    if a == -2: pj -= 1
    elif a == -1: bi -= 1
    else: assign[bi - 1] = pauses[a]; bi -= 1; pj = a
# mốc đầu/cuối mỗi vế
starts, ends, t = [], [], 0.0
for k, (s, e) in enumerate(spans):
    starts.append(t)
    if k < B:
        if assign[k]: ends.append(assign[k][0]); t = assign[k][1]
        else:
            tb = expect[k]; ends.append(tb); t = tb
    else:
        ends.append(dur)
chars = [0.0] * len(text)
for (s, e), a, b in zip(spans, starts, ends):
    hs = [k for k in range(s, e) if is_han[k]]
    step = (b - a) / max(1, len(hs))
    last = a
    for k in range(s, e):
        if is_han[k]:
            last = a + hs.index(k) * step; chars[k] = round(last, 3)
        else:
            chars[k] = round(last + step * 0.9, 3)
(here / "src" / "timing.json").write_text(json.dumps({"chars": chars, "end": round(dur, 3)}), encoding="utf-8")
hit = sum(1 for a in assign if a)
print(f"giọng {dur:.1f}s | chỗ ngắt dò được {P} | ranh giới vế {B}, khớp {hit}, nội suy {B - hit}")
