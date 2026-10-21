"""Tạo giọng đọc, chọn nhà cung cấp bằng TTS_PROVIDER (lucylab | elevenlabs) — cùng quy ước với repo Auto-Create-Video.

  python scripts/voicegen/tts.py "眼睛" -o yanjing.wav                  # dùng TTS_PROVIDER + voice trong .env
  python scripts/voicegen/tts.py "眼睛" -o a.mp3 --provider elevenlabs
  python scripts/voicegen/tts.py --list [--provider lucylab]

Cấu hình trong scripts/imagegen/.env (gitignored):
  TTS_PROVIDER=lucylab
  VIVIBE_API_KEY=...            LUCYLAB_VOICE_ID=...        (ViVibe = LucyLab, api.lucylab.io)
  ELEVENLABS_API_KEY=...        ELEVENLABS_VOICE_ID=...     ELEVENLABS_MODEL_ID=eleven_multilingual_v2

Định dạng ra: lucylab -> WAV (+ SRT), elevenlabs -> MP3. Đặt đuôi -o khớp provider.
"""
import argparse, json, os, sys, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import vivibe_tts as lucylab  # noqa: E402

UA = "curl/8.4.0"


def env(name, default=None):
    if name in os.environ:
        return os.environ[name]
    try:
        for line in lucylab.ENV.read_text(encoding="utf-8").splitlines():
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip()
    except FileNotFoundError:
        pass
    return default


def _el_request(path, body=None):
    k = env("ELEVENLABS_API_KEY")
    if not k:
        sys.exit("Thiếu ELEVENLABS_API_KEY trong .env")
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1" + path,
        json.dumps(body).encode() if body is not None else None,
        {"xi-api-key": k, "Content-Type": "application/json", "User-Agent": UA})
    return urllib.request.urlopen(req, timeout=120).read()


def synth(text, out, provider=None, voice=None, speed=1.0):
    provider = provider or env("TTS_PROVIDER", "lucylab")
    if provider == "lucylab":
        voice = voice or env("LUCYLAB_VOICE_ID") or sys.exit("Thiếu LUCYLAB_VOICE_ID")
        return lucylab.tts(text, voice, out, speed)
    if provider == "elevenlabs":
        voice = voice or env("ELEVENLABS_VOICE_ID") or sys.exit("Thiếu ELEVENLABS_VOICE_ID")
        body = {"text": text, "model_id": env("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")}
        if speed != 1.0:
            body["voice_settings"] = {"speed": speed, "stability": 0.5, "similarity_boost": 0.75}
        Path(out).write_bytes(_el_request(f"/text-to-speech/{voice}?output_format=mp3_44100_128", body))
        return {"chars": len(text), "srt": None}
    sys.exit(f"Provider không hỗ trợ: {provider}")


def list_voices(provider=None):
    provider = provider or env("TTS_PROVIDER", "lucylab")
    if provider == "lucylab":
        return [(v["id"], v["name"], v.get("tags")) for v in lucylab.list_voices()]
    d = json.loads(_el_request("/voices"))
    return [(v["voice_id"], v["name"], v.get("labels")) for v in d["voices"]]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("text", nargs="?")
    ap.add_argument("-o", "--out", default="voice.wav")
    ap.add_argument("--provider", choices=["lucylab", "elevenlabs"])
    ap.add_argument("-v", "--voice")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        for row in list_voices(a.provider):
            print(*row, sep=" | ")
    elif a.text:
        print(synth(a.text, a.out, a.provider, a.voice, a.speed))
    else:
        ap.error("cần text hoặc --list")
