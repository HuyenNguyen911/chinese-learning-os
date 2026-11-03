"""Giọng đọc mẫu bản xứ (Edge TTS) theo kiểu 朗读 HSKK cao cấp -> public/audio/read.wav + src/timing.json.

  python voice_edge.py            # giọng theo giới tính nhân vật trong data.json ("voice" nếu có, mặc định nam)
  python voice_edge.py --voice zh-CN-XiaoxiaoNeural --rate -10%

Nhân vật nam -> zh-CN-YunxiNeural (nam thiếu niên); nữ -> zh-CN-XiaoxiaoNeural.
Tốc độ: gần nhịp bản xứ (-5%). Đọc TỪNG CÂU (tách ở 。！？；：) rồi ghép, nghỉ thêm 0.2s sau 。 / 0.08s sau ；：
— đọc liền cả bài thì đoạn đầu nhanh, nối chữ; tách vụn hơn thì câu đầu lại chậm, đứt nhịp (user chê 2026-10-28).
Mốc từng chữ lấy từ WordBoundary của Edge (cộng thêm mốc đầu mỗi câu). Hậu kỳ: chuẩn độ to -16 LUFS,
tăng nhẹ dải trầm cho giọng dày, nén nhẹ — KHÔNG cắt lặng đầu (giữ đúng mốc). Cần ffmpeg + numpy.
"""
import argparse, asyncio, json, re, subprocess, sys
from pathlib import Path

import edge_tts
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
audio = here / "public" / "audio"
VOICES = {"male": "zh-CN-YunxiNeural", "female": "zh-CN-XiaoxiaoNeural"}

data = json.loads((here / "src" / "data.json").read_text(encoding="utf-8"))
ap = argparse.ArgumentParser()
ap.add_argument("--voice", default=data.get("voice") or VOICES[data.get("gender", "male")])
ap.add_argument("--rate", default="-5%")
a = ap.parse_args()
text = data["text"]


SR = 24000
# tách câu: chỉ sau 。！？；：  (tách thêm ở "——"/trích dẫn thì câu đầu bị chậm, đứt nhịp — user chê)
chunks, cur = [], ""
for i, c in enumerate(text):
    cur += c
    nxt = text[i + 1] if i + 1 < len(text) else ""
    if c in "。！？；：":
        chunks.append(cur); cur = ""
if cur: chunks.append(cur)
PAUSE = lambda ch: 0.2 if ch[-1] in "。！？" else 0.08   # Edge đã có lặng cuối câu sẵn; thêm nhiều nghe "nghỉ lâu giữa nhịp"


async def synth(t):
    com = edge_tts.Communicate(t, a.voice, rate=a.rate, boundary="WordBoundary")
    marks, buf = [], bytearray()
    async for ch in com.stream():
        if ch["type"] == "audio":
            buf += ch["data"]
        elif ch["type"] == "WordBoundary":
            marks.append((ch["offset"] / 1e7, ch["duration"] / 1e7, ch["text"]))
    return bytes(buf), marks

pcm, marks, t0 = [], [], 0.0
for ch in chunks:
    mp3, m = asyncio.run(synth(ch))
    x = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "pipe:0", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                                     input=mp3, capture_output=True, check=True).stdout, np.int16)
    marks += [(t0 + o, d, w) for o, d, w in m]
    pause = np.zeros(int(PAUSE(ch) * SR), np.int16)
    pcm += [x, pause]
    t0 += (len(x) + len(pause)) / SR
raw = np.concatenate(pcm)[: -len(pause)]
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "pipe:0", "-ar", "44100", "-af",
                "highpass=f=70,equalizer=f=180:t=q:w=1:g=3,equalizer=f=3500:t=q:w=1.5:g=1.5,"
                "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=9",
                str(audio / "read.wav")], input=raw.tobytes(), check=True)
print("số câu:", len(chunks))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(audio / "read.wav")],
                           capture_output=True, text=True).stdout)

# gán mốc cho từng chữ: dò lần lượt từng từ trong bài; chữ Hán trong từ chia đều thời lượng từ đó
is_han = [bool(re.match(r"[一-鿿]", c)) for c in text]
chars, k, last = [None] * len(text), 0, 0.0
for off, d, w in marks:
    j = text.find(w, k)
    if j < 0 or j - k > 12:              # không khớp (hiếm) -> bỏ qua
        continue
    hs = [i for i in range(j, j + len(w)) if is_han[i]]
    for n, i in enumerate(hs):
        chars[i] = round(off + d * n / max(1, len(hs)), 3)
    k = j + len(w); last = off + d
miss = 0
for i in range(len(text)):              # chữ chưa có mốc / dấu câu: lấy mốc gần nhất phía trước
    if chars[i] is None:
        miss += is_han[i]
        chars[i] = chars[i - 1] if i else 0.0
(here / "src" / "timing.json").write_text(json.dumps({"chars": chars, "end": round(dur, 3), "voice": a.voice}), encoding="utf-8")
print(f"{a.voice} rate {a.rate} | {dur:.1f}s | {len(marks)} từ | chữ Hán thiếu mốc: {miss}")
