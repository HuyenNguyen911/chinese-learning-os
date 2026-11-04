"""Giọng đọc phần mở đầu (câu hỏi, 现在开始, các cụm đáng học) bằng Edge TTS cùng giọng nam trẻ với bài đọc -> public/audio/intro_*.wav + src/intro.json."""
import asyncio, json, subprocess, sys
from pathlib import Path
import edge_tts
sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
out = here / "public" / "audio"
VOICE, RATE, PITCH = "zh-CN-YunxiaNeural", "+8%", "+4Hz"
ITEMS = {
    "q": "说说你对活人图书馆的看法。",
    "now": "现在开始。",
    "p0": "借阅", "p1": "挑", "p2": "所求不过是", "p3": "最有意思的一点是", "p4": "真诚", "p5": "标签",   # đúng thứ tự S3_LIST trong Full.tsx
}
res = {}
for k, text in ITEMS.items():
    mp3 = out / f"intro_{k}.mp3"
    asyncio.run(edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH).save(str(mp3)))
    wav = out / f"intro_{k}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3), "-ar", "44100", "-ac", "1",
                    "-af", "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=9", str(wav)], check=True)
    mp3.unlink()
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)], capture_output=True, text=True).stdout)
    res[k] = round(d, 3)
(here / "src" / "intro.json").write_text(json.dumps(res), encoding="utf-8")
print(res)
