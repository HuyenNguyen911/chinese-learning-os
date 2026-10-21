"""Sinh giọng đọc từng từ -> public/audio/<id>.wav và ghi thời lượng vào src/durations.json (giây).
Chạy lại an toàn: bỏ qua file đã có (xoá file để sinh lại). Tài khoản chỉ chạy 1 job/lần nên tuần tự.
  python gen_voice.py [--speed 0.85]
"""
import argparse, json, subprocess, sys
from pathlib import Path

here = Path(__file__).parent
sys.path.insert(0, str(here.parent.parent / "voicegen"))
import tts  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--speed", type=float, default=0.85)
a = ap.parse_args()

out_dir = here / "public" / "audio"
out_dir.mkdir(parents=True, exist_ok=True)
words = json.loads((here / "words.json").read_text(encoding="utf-8"))
durs = {}
for w in words:
    f = out_dir / f"{w['id']}.wav"
    if not f.exists():
        print("TTS", w["han"], flush=True)
        tts.synth(w["han"], str(f), speed=a.speed)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                       capture_output=True, text=True, check=True)
    durs[w["id"]] = round(float(r.stdout), 3)
(here / "src" / "durations.json").write_text(json.dumps(durs, indent=1), encoding="utf-8")
print(durs)
