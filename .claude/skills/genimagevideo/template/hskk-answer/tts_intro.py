"""Giọng đọc phần mở đầu (câu hỏi, 现在开始, các cụm đáng học) bằng Edge TTS cùng giọng nam trẻ với bài đọc -> public/audio/intro_*.wav + src/intro.json."""
import asyncio, json, subprocess, sys
from pathlib import Path
import edge_tts
sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
out = here / "public" / "audio"
VOICE, RATE, PITCH = "zh-CN-XiaoxiaoNeural", "+0%", "+0Hz"
ITEMS = {
    "q": "如果你有了子女，你会为他或她选择哪种学习方式？",
    "now": "现在开始。",
    "p0": "更倾向于", "p1": "偏科", "p2": "人际交往", "p3": "亲自", "p4": "承受不了", "p5": "出于对孩子将来的考虑",
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
