"""Tạo giọng đọc qua ViVibe (= LucyLab JSON-RPC). Key đọc từ scripts/imagegen/.env (VIVIBE_API_KEY, gitignored).

  python scripts/voicegen/vivibe_tts.py --list
  python scripts/voicegen/vivibe_tts.py "眼睛" -v <voiceId> -o out.wav [--speed 0.8]

Lưu ý: phải có User-Agent, nếu không Cloudflare trả 403 cho python-urllib.
Job chạy bất đồng bộ: ttsLongText -> projectExportId -> getExportStatus (poll) -> url wav (+ srtUrl).
"""
import argparse, json, os, sys, time, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
URL = "https://api.lucylab.io/json-rpc"
ENV = Path(__file__).resolve().parent.parent / "imagegen" / ".env"


def key():
    if "VIVIBE_API_KEY" in os.environ:
        return os.environ["VIVIBE_API_KEY"]
    for line in ENV.read_text(encoding="utf-8").splitlines():
        if line.startswith("VIVIBE_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("Thiếu VIVIBE_API_KEY")


def rpc(method, **inp):
    req = urllib.request.Request(
        URL, json.dumps({"method": method, "input": inp}).encode(),
        {"Content-Type": "application/json", "Authorization": "Bearer " + key(), "User-Agent": "curl/8.4.0"})
    d = json.load(urllib.request.urlopen(req, timeout=60))
    if "result" not in d:
        sys.exit(f"API lỗi ({method}): " + json.dumps(d, ensure_ascii=False)[:500])
    return d["result"]


def list_voices():
    return rpc("getUserVoices", limit=50, page=1)["items"]


def tts(text, voice_id, out, speed=1.0, timeout=180):
    job = rpc("ttsLongText", text=text, userVoiceId=voice_id, speed=speed)
    t0 = time.time()
    while time.time() - t0 < timeout:
        st = rpc("getExportStatus", projectExportId=job["projectExportId"])
        if st["state"] == "completed":
            req = urllib.request.Request(st["url"], headers={"User-Agent": "curl/8.4.0"})
            Path(out).write_bytes(urllib.request.urlopen(req, timeout=60).read())
            return {"chars": job["characterCount"], "srt": st.get("srtUrl")}
        if st["state"] == "failed":
            sys.exit("Job thất bại: " + json.dumps(st, ensure_ascii=False))
        time.sleep(2.5)
    sys.exit("Hết thời gian chờ")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("text", nargs="?")
    ap.add_argument("-v", "--voice")
    ap.add_argument("-o", "--out", default="voice.wav")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        for v in list_voices():
            print(v["id"], "|", v["name"], "|", v.get("tags"))
    else:
        if not (a.text and a.voice):
            sys.exit("Cần text và --voice (xem --list)")
        print(tts(a.text, a.voice, a.out, a.speed))
