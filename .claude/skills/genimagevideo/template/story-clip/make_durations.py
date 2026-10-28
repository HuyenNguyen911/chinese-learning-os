"""Từ file giọng user thu (public/audio/<id>.m4a|mp3|wav...) -> wav 44.1k (cắt lặng đầu/cuối) +
src/durations.json (giây mỗi cảnh) + src/envelope.json (âm lượng 0-1 mỗi khung hình, để nhân vật nhún theo giọng).

  python make_durations.py         # id lấy từ src/story.json
Chưa có file nào -> ghi {} (clip dùng defaultSec, không tiếng). Cần ffmpeg + numpy.
"""
import json, subprocess, sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
audio = here / "public" / "audio"
audio.mkdir(parents=True, exist_ok=True)
ids = list(dict.fromkeys(s.get("voice", s["id"]) for s in json.loads((here / "src" / "story.json").read_text(encoding="utf-8"))["scenes"] if not s.get("silent")))  # 1 file giọng / câu, có thể chia nhiều cảnh
FPS, SR = 30, 44100
exts = (".m4a", ".mp3", ".wav", ".aac", ".ogg", ".flac", ".mp4")
durations, envelope, missing = {}, {}, []
for i in ids:
    plain = audio / f"{i}.wav"
    if plain.exists() and not (audio / f"{i}.src.wav").exists() and any((audio / f"{i}{e}").exists() for e in exts if e != ".wav") is False:
        plain.rename(audio / f"{i}.src.wav")          # user thu thẳng .wav -> giữ bản gốc
    src = next((p for p in [audio / f"{i}.src.wav", *[audio / f"{i}{e}" for e in exts if e != ".wav"]] if p.exists()), None)
    if src is None:
        missing.append(i); continue
    tmp = audio / f"{i}.tmp.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ar", str(SR), "-ac", "1",
                    "-af", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
                           "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse", str(tmp)], check=True)
    out = audio / f"{i}.wav"
    tmp.replace(out)
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(out), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    durations[i] = round(len(x) / SR, 3)
    spf = SR // FPS
    rms = np.array([np.sqrt(np.mean(x[k:k + spf] ** 2) + 1e-12) for k in range(0, len(x), spf)])
    rms = np.convolve(rms, np.ones(3) / 3, mode="same")
    envelope[i] = [round(float(v), 3) for v in np.clip(rms / (np.percentile(rms, 95) + 1e-9), 0, 1)]
(here / "src" / "durations.json").write_text(json.dumps(durations, indent=1), encoding="utf-8")
(here / "src" / "envelope.json").write_text(json.dumps(envelope), encoding="utf-8")
print("có giọng:", list(durations) or "chưa có", "| thiếu:", missing or "không")
