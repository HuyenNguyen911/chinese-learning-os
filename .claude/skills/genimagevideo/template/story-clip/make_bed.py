"""[VÍ DỤ từ talk01-contagious — sửa phần "hiệu ứng" theo cảnh của clip mới; cần public/sfx/*.mp3 + music_*.mp3]
Dựng lớp NỀN âm thanh (nhạc nền không lời + hiệu ứng) -> public/audio/bed.wav, dài đúng TOTAL của clip.
Mốc thời gian lấy từ src/story.json + src/durations.json (cùng công thức chia cảnh với Story.tsx), nên
chạy SAU make_durations.py. Giọng đọc vẫn là các <Audio> riêng; nhạc tự hạ nhỏ khi có giọng (ducking).

  python make_bed.py
Âm thanh lấy từ public/sfx/*.mp3 — Mixkit (mixkit.co, Free License) và Freesound (fs_*, chỉ chọn CC0).
Mỗi hiệu ứng = (file, cắt từ giây a đến b, đặt ở giây t, độ to dB so với đỉnh 0 dB).
"""
import json, re, subprocess, sys, wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
SR, FPS = 44100, 30
SFX = here / "public" / "sfx"

story = json.loads((here / "src" / "story.json").read_text(encoding="utf-8"))["scenes"]
dur = json.loads((here / "src" / "durations.json").read_text(encoding="utf-8"))
han = lambda t: len(re.findall(r"[一-鿿]", t))

# ---- mốc cảnh (giây) — giống layout trong Story.tsx
starts, lens, voice_span, cur = {}, {}, {}, 0
for s in story:
    v = s.get("voice", s["id"])
    g = [x for x in story if x.get("voice", x["id"]) == v]
    gc, idx = sum(han(x["text"]) for x in g), g.index(s)
    if s.get("sec"):
        n = round(s["sec"] * FPS)
    elif v in dur:
        tot = round((dur[v] + 0.5) * FPS)
        cut = lambda k: round(tot * sum(han(x["text"]) for x in g[:k]) / gc)
        n = (tot if idx == len(g) - 1 else cut(idx + 1)) - cut(idx)
    else:
        n = round(max(1.5, han(s["text"]) * 0.24 + 0.5) * FPS)
    starts[s["id"]], lens[s["id"]] = cur / FPS, n / FPS
    if v in dur and v not in voice_span:
        voice_span[v] = (cur / FPS, cur / FPS + dur[v])
    cur += n
SCENES_END = cur / FPS
OUTRO = json.loads((here / "src" / "outro.json").read_text(encoding="utf-8"))["sec"]    # đoạn kết (Outro.tsx): nghỉ 0.4s + max(3.6, giọng + 1)
OUTRO_START = round(SCENES_END * FPS + 0.4 * FPS) / FPS
TOTAL = OUTRO_START + round(max(3.6, OUTRO + 1.0) * FPS) / FPS
voice_span["outro"] = (OUTRO_START + 0.2, OUTRO_START + 0.2 + OUTRO)
N = int(TOTAL * SR)
t_all = np.arange(N) / SR
at = lambda sid, p=0.0: starts[sid] + p * lens[sid]            # mốc trong cảnh theo tỉ lệ

_cache = {}
def load(name):
    if name not in _cache:
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(SFX / f"{name}.mp3"), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
        _cache[name] = x / (np.abs(x).max() + 1e-9)               # chuẩn hoá đỉnh = 0 dB
    return _cache[name]

def clip(name, a=0.0, b=None, fade=0.03):
    x = load(name)[int(a * SR): int(b * SR) if b else None].copy()
    k = min(int(fade * SR), len(x) // 2)
    if k:
        x[:k] *= np.linspace(0, 1, k); x[-k:] *= np.linspace(1, 0, k)
    return x

def put(buf, sig, t0, db):
    i = max(0, int(t0 * SR))
    if i >= len(buf): return
    sig = sig[: len(buf) - i]
    buf[i:i + len(sig)] += sig * 10 ** (db / 20)

sfx = np.zeros(N)
# c2a: bước chân đi vào nhà (Freesound CC0 "Indoor Footsteps") — không xe, không chìa khoá/cửa
put(sfx, clip("fs_indoor_footsteps", 0.0, 2.45, fade=0.1), at("c2a", 0) - 0.1, -20)
# c2b: dấu "?" hiện
put(sfx, clip("pop_bubble"), at("c2b", 0.3), -16)
# ba mẹ cười nói: nhỏ dưới giọng, rõ ở cảnh không thoại c2d.
# Mẹ = cười khúc khích "Girl, female, laughing, giggling" (Freesound CC0) — các tràng: 0-0.7 | 1.4-2.0 | 3.0-3.9 | 5.0-5.7 | 6.8-7.5 | 8.7-9.2
mom = lambda a, b: clip("fs_girl_giggling", a, b, fade=0.05)
put(sfx, mom(0.0, 0.7), at("c2b", 0.1), -26)
put(sfx, clip("laugh_male_casual", 0.05, 1.5, fade=0.1), at("c2c", 0.35), -27)
put(sfx, mom(5.0, 5.7), at("c2c", 0.65), -27)
put(sfx, mom(3.0, 3.9), at("c2d", 0.0), -15)
put(sfx, clip("laugh_male_casual", 0.05, 1.5, fade=0.05), at("c2d", 0.15), -17)
put(sfx, mom(1.4, 2.0), at("c2d", 0.42), -16)
put(sfx, mom(6.8, 7.5), at("c2d", 0.68), -16)
put(sfx, mom(8.7, 9.2), at("c3a", 0.0), -26)
# c3a: điểm sáng + thẻ 不知不觉, rồi nhân vật bật cười
put(sfx, clip("magic_key", 0, 1.6, fade=0.2), at("c3a", 0.1), -24)
put(sfx, clip("pop_whoosh"), at("c3a", 0.2), -16)
put(sfx, clip("giggle", 0.0, 1.0, fade=0.08), at("c3a", 0.62), -20)
put(sfx, clip("laugh_females"), at("c3b", 0.05), -22)
# c4, c5a: thẻ từ
put(sfx, clip("pop_whoosh"), at("c4", 0.2), -16)
put(sfx, clip("pop_whoosh"), at("c5a", 0.3), -16)

# ---- nhạc nền (Mixkit "Happy Home"), hạ nhỏ khi có giọng
music = clip("music_happy_home", 0, TOTAL, fade=0.01)
music = np.pad(music, (0, max(0, N - len(music))))[:N]
duck = np.ones(N)
for a, b in voice_span.values():
    duck[int(max(0, a - 0.1) * SR):int((b + 0.3) * SR)] = 0.5
k = int(0.25 * SR)
duck = np.convolve(duck, np.ones(k) / k, mode="same")
fade = np.minimum(1, t_all / 1.0) * np.minimum(1, (TOTAL - t_all) / 2.0)
music *= duck * fade * 10 ** (-22 / 20)

bed = np.clip(music + sfx, -0.98, 0.98)
out = here / "public" / "audio" / "bed.wav"
with wave.open(str(out), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((bed * 32767).astype(np.int16).tobytes())
print(f"bed.wav {TOTAL:.2f}s | cảnh:", {k: round(v, 2) for k, v in starts.items()})
