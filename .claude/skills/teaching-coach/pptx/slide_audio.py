#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
slide_audio.py — Sinh audio giọng bản địa cho slide bài giảng và gắn vào JSON.

Với mỗi slide có nội dung chữ Hán đáng đọc (vocab / grammar / dialogue / bảng
口语), gom text Hán -> gọi edge-tts sinh 1 file mp3 -> ghi vào
<thư mục JSON>/assets/audio/slideNN.mp3, rồi thêm key "audio" vào slide đó.

Đa dạng giọng:
  - Slide thường: LUÂN PHIÊN giọng theo VOICE_POOL (mỗi slide 1 giọng khác nhau).
  - Hội thoại: mỗi người nói 1 giọng riêng (A/B…), ghép các lượt thành 1 mp3.
Tốc độ: chậm lại cho học viên qua --rate (mặc định -18%).

Sau bước này chạy build_deck.py: mỗi slide có "audio" sẽ có nút 🔊 (PowerPoint
nhận là Sound, bấm để phát). CHỈ phát khi mở bằng PowerPoint thật (desktop/app),
trình xem Drive/Google Slides không phát audio nhúng.

Chạy:
    python slide_audio.py <lesson.json> [--rate=-18%] [--force]

Cần: edge-tts (internet). Không sinh lại file đã có trừ khi --force.
"""

import json
import subprocess
import sys
from pathlib import Path

# Giọng luân phiên cho slide thường (nữ/nam xen kẽ cho đa dạng)
VOICE_POOL = [
    "zh-CN-XiaoxiaoNeural",   # nữ, ấm
    "zh-CN-YunxiNeural",      # nam, trẻ
    "zh-CN-XiaoyiNeural",     # nữ, trong
    "zh-CN-YunjianNeural",    # nam, trầm
]
# Giọng gán cho từng người trong hội thoại (theo thứ tự xuất hiện)
DIALOGUE_VOICES = ["zh-CN-XiaoxiaoNeural", "zh-CN-YunxiNeural", "zh-CN-XiaoyiNeural"]
RATE_DEFAULT = "-18%"


def read_text(s):
    """Chuỗi chữ Hán cần đọc cho slide thường (không phải dialogue)."""
    t = s.get("type")
    if t == "vocab":
        xs = [it.get("hz", "") for it in s.get("items", [])]
    elif t == "grammar":
        xs = [ex.get("hz", "") for ex in s.get("examples", [])]
    elif t == "table" and s.get("kicker") == "口语":
        xs = [row[0] for row in s.get("rows", []) if row]
    else:
        return None
    xs = [x.strip() for x in xs if x and x.strip()]
    return "，".join(xs) if xs else None


def tts(text, voice, rate, out):
    r = subprocess.run(
        [sys.executable, "-m", "edge_tts", "--voice", voice,
         "--rate=%s" % rate, "--text", text, "--write-media", str(out)],
        capture_output=True, text=True)
    return r.returncode == 0 and out.exists()


def gen_dialogue(turns, rate, audio_dir, out, tag):
    """Mỗi speaker 1 giọng riêng; ghép các lượt thành 1 mp3."""
    voices, order = {}, []
    for tn in turns:
        spk = tn.get("speaker", "")
        if spk not in voices:
            voices[spk] = DIALOGUE_VOICES[len(voices) % len(DIALOGUE_VOICES)]
        order.append((tn.get("hz", "").strip(), voices[spk]))
    data = b""
    for j, (text, voice) in enumerate(order):
        if not text:
            continue
        tmp = audio_dir / ("_%s_%02d.mp3" % (tag, j))
        if not tts(text, voice, rate, tmp):
            return False, voices
        data += tmp.read_bytes()
        tmp.unlink()
    if not data:
        return False, voices
    out.write_bytes(data)
    return True, voices


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    opts = [a for a in argv[1:] if a.startswith("--")]
    if not args:
        print("Usage: python slide_audio.py <lesson.json> [--rate=-18%] [--force]",
              file=sys.stderr)
        return 2
    src = Path(args[0])
    rate = RATE_DEFAULT
    for o in opts:
        if o.startswith("--rate="):
            rate = o.split("=", 1)[1]
    force = "--force" in opts

    spec = json.loads(src.read_text(encoding="utf-8"))
    audio_dir = src.parent / "assets" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    made = 0
    pool_idx = 0
    for i, s in enumerate(spec.get("slides", []), start=1):
        rel = "assets/audio/slide%02d.mp3" % i
        out = src.parent / rel
        is_dialogue = s.get("type") == "dialogue"
        text = None if is_dialogue else read_text(s)
        if not is_dialogue and not text:
            continue
        if is_dialogue and not s.get("turns"):
            continue

        if force or not out.exists():
            if is_dialogue:
                ok, voices = gen_dialogue(s["turns"], rate, audio_dir, out,
                                          tag="d%02d" % i)
                label = "dialogue " + "/".join(
                    v.split("-")[-1].replace("Neural", "") for v in voices.values())
            else:
                voice = VOICE_POOL[pool_idx % len(VOICE_POOL)]
                pool_idx += 1
                ok = tts(text, voice, rate, out)
                label = "%s %s" % (s.get("type"),
                                   voice.split("-")[-1].replace("Neural", ""))
            if not ok:
                print("FAIL slide %02d" % i)
                continue
            made += 1
            print("OK   slide %02d [%s] <- %s" % (i, label,
                  (text or s["turns"][0].get("hz", ""))[:26]))
        s["audio"] = rel

    src.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print("DONE: %d mp3 mới (rate %s) -> %s" % (made, rate, audio_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
