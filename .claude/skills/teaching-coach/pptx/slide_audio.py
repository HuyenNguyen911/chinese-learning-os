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
import re
import subprocess
import sys
from pathlib import Path

_CJK_RUN_RE = re.compile(r"[一-鿿]+")
_VN_DIACRITIC_RE = re.compile(
    "[đĐưƯơƠạảãắằẳẵặầấẩẫậẹẽềếểễệịĩọồốổỗộờớởỡợụũừứửữựỳỹỷ]"
)
_PINYIN_TOKEN_RE = re.compile(r"[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]+")


def _first_cjk_run(text):
    m = _CJK_RUN_RE.search(str(text))
    return m.group(0) if m else None


def _pinyin_tokens(cell):
    """Trích âm tiết pinyin (có dấu thanh) từ 1 ô — dùng cho bảng luyện đọc
    thuần pinyin (không có chữ Hán làm neo, vd 辨别声母/辨别韵母). Ô nhãn tiếng
    Việt (có dấu đặc trưng đ/ư/ơ/... hoặc dấu ngoặc mô tả nhóm) bị loại để
    không đọc nhầm tiếng Việt bằng giọng tiếng Trung."""
    text = str(cell)
    if _VN_DIACRITIC_RE.search(text) or "(" in text:
        return []
    return _PINYIN_TOKEN_RE.findall(text)

# Luân phiên giọng cho slide thường — feedback buổi HSK2 Buổi 2: giọng cũ
# 1-voice + rate -30% nghe "mệt mệt, như người máy đọc" → thêm Xiaoxiao/Xiaoyi.
# Feedback buổi HSK2 Buổi 3: 2 giọng nữ (Xiaoxiao/Xiaoyi) nghe vẫn giống nhau,
# muốn "nhiều lên" → mở thêm 2 giọng nam (Yunxi/Yunjian) xen kẽ nam/nữ mỗi
# slide cho rõ khác biệt, không chỉ đổi màu giọng nữ với nhau.
VOICE_POOL = [
    "zh-CN-XiaoxiaoNeural",
    "zh-CN-YunxiNeural",
    "zh-CN-XiaoyiNeural",
    "zh-CN-YunjianNeural",
]
# Giọng gán cho từng người trong hội thoại (theo thứ tự xuất hiện)
DIALOGUE_VOICES = ["zh-CN-XiaoxiaoNeural", "zh-CN-YunxiNeural", "zh-CN-XiaoyiNeural"]
# Rate mặc định theo loại nội dung — slide thường (từ vựng/ngữ pháp cần nghe rõ
# từng chữ) chậm hơn hội thoại (ưu tiên nhịp tự nhiên, giống người thật nói
# chuyện) một chút. -30% cũ bị chê quá chậm/không tự nhiên; hạ xuống -15%/-8%.
RATE_DEFAULT = "-15%"
DIALOGUE_RATE_DEFAULT = "-8%"


def read_text(s):
    """Chuỗi chữ Hán cần đọc cho slide thường (không phải dialogue).
    Vocab: CHỈ đọc 生词 (items), KHÔNG đọc câu ví dụ — tránh lẫn nhịp đọc
    (từ rời rạc xen với câu liền mạch nghe rối).

    Buổi ngữ âm (hsk1) dùng schema riêng (table nhiều kicker khác nhau,
    word_groups, stroke_group) không có field cố định như vocab/grammar —
    xử lý thêm 3 nhánh: bảng bất kỳ (trích cụm CJK đầu tiên mỗi ô, ô thuần
    pinyin tự động bị bỏ qua vì không match), word_groups (items[].hz),
    stroke_group (chars[].hanzi)."""
    t = s.get("type")
    if t == "vocab":
        xs = [it.get("hz", "") for it in s.get("items", [])]
    elif t == "grammar":
        xs = [ex.get("hz", "") for ex in s.get("examples", [])]
    elif t == "table" and s.get("kicker") == "口语":
        xs = [row[0] for row in s.get("rows", []) if row]
    elif t == "wordcard":
        xs = [s.get("hz", "")] + [ex.get("hz", "") for ex in s.get("examples", [])]
    elif t == "passage":
        xs = [sent.get("hz", "") for sent in s.get("sentences", [])]
    elif t == "table" and s.get("kicker") == "写字":
        return None  # bảng tham chiếu nét/quy tắc viết chữ — không phải từ vựng để đọc
    elif t == "table":
        xs = []
        for row in s.get("rows", []):
            for cell in row:
                hz = _first_cjk_run(cell)
                if hz:
                    xs.append(hz)
        if not xs and s.get("kicker") == "练习":
            # Bảng luyện đọc thuần pinyin (không có chữ Hán, vd 辨别声母/
            # 辨别韵母/vần phức) — đọc trực tiếp âm tiết pinyin đã có dấu
            # thanh thay vì bỏ qua hẳn.
            for row in s.get("rows", []):
                for cell in row:
                    xs.extend(_pinyin_tokens(cell))
    elif t == "info_grid":
        xs = [c.get("label", "") for c in s.get("cards", [])]
    elif t == "word_groups":
        xs = [it.get("hz", "") for grp in s.get("groups", []) for it in grp.get("items", [])]
    elif t == "stroke_group":
        xs = [c.get("hanzi", "") for c in s.get("chars", [])]
    elif t == "bullets" and s.get("kicker") == "写字":
        hz = _first_cjk_run(s.get("title", ""))
        xs = [hz] if hz else []
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
    rate_override = None
    for o in opts:
        if o.startswith("--rate="):
            rate_override = o.split("=", 1)[1]
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
                rate = rate_override or DIALOGUE_RATE_DEFAULT
                ok, voices = gen_dialogue(s["turns"], rate, audio_dir, out,
                                          tag="d%02d" % i)
                label = "dialogue " + "/".join(
                    v.split("-")[-1].replace("Neural", "") for v in voices.values())
            else:
                rate = rate_override or RATE_DEFAULT
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
    rate_note = rate_override or ("%s thường / %s hội thoại" % (RATE_DEFAULT, DIALOGUE_RATE_DEFAULT))
    print("DONE: %d mp3 mới (rate %s) -> %s" % (made, rate_note, audio_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
