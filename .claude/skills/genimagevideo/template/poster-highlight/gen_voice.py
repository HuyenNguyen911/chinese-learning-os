"""Chuẩn bị giọng đọc từng từ -> public/audio/<id>.wav và ghi thời lượng vào src/durations.json (giây).

Thứ tự ưu tiên cho mỗi từ:
  1. Đã có public/audio/<id>.wav            -> dùng luôn
  2. Có file TỰ THU ÂM public/audio/<id>.{mp3,m4a,ogg,webm,aac,flac}
                                            -> ffmpeg đổi sang wav + cắt khoảng lặng đầu/cuối
  3. Không có gì                            -> gọi TTS (provider trong .env của skill)

Chạy lại an toàn (xoá <id>.wav để làm lại từ đó). TTS tuần tự vì tài khoản LucyLab chỉ cho 1 job/lần.
  python gen_voice.py [--speed 0.85] [--no-tts]
"""
import argparse, json, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
sys.path.insert(0, str(here))
from _paths import VOICEGEN  # noqa: E402
sys.path.insert(0, str(VOICEGEN))

REC_EXT = (".mp3", ".m4a", ".ogg", ".webm", ".aac", ".flac")
# cắt lặng đầu, đảo ngược cắt lặng cuối, đảo lại; ngưỡng -45dB
TRIM = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
        "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse")

ap = argparse.ArgumentParser()
ap.add_argument("--speed", type=float, default=0.85)
ap.add_argument("--no-tts", action="store_true", help="chỉ dùng file thu âm, báo thiếu thay vì gọi TTS")
a = ap.parse_args()

out_dir = here / "public" / "audio"
out_dir.mkdir(parents=True, exist_ok=True)
words = json.loads((here / "words.json").read_text(encoding="utf-8"))
durs, missing = {}, []
for w in words:
    f = out_dir / f"{w['id']}.wav"
    if not f.exists():
        rec = next((out_dir / f"{w['id']}{e}" for e in REC_EXT if (out_dir / f"{w['id']}{e}").exists()), None)
        if rec:
            print("REC", rec.name, flush=True)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(rec), "-af", TRIM,
                            "-ac", "1", "-ar", "48000", str(f)], check=True)
        elif a.no_tts:
            missing.append(w["id"])
            continue
        else:
            import tts  # noqa: E402  (chỉ nạp khi thật sự cần TTS)
            print("TTS", w["han"], flush=True)
            tts.synth(w["han"], str(f), speed=a.speed)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                       capture_output=True, text=True, check=True)
    durs[w["id"]] = round(float(r.stdout), 3)
if missing:
    sys.exit("Thiếu file thu âm cho: " + ", ".join(missing))
(here / "src" / "durations.json").write_text(json.dumps(durs, indent=1), encoding="utf-8")
print(durs)
