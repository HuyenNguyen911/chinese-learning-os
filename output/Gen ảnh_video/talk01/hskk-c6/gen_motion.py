"""Khung tĩnh -> đoạn video cử động thật bằng muse-video (9router, image-to-video).

  python gen_motion.py              # mọi clip trong src/motion.json chưa có assets/motion/<id>.mp4
  python gen_motion.py c2b c4       # chỉ (gen lại) các clip này

Ảnh mẫu: assets/keyframes/<id>.png (xuất bằng `npx remotion still ... --props='{"clean":true}'` — không chữ/logo,
vì AI làm méo chữ). Model nhận ảnh qua `image` / `image_url` / `input_reference` (gửi cả 3) và giữ tỉ lệ ảnh mẫu.
Mỗi lần ~4 phút, trả 10s mp4 dạng base64. Key: scripts/imagegen/.env (IMAGEGEN_KEY, VIDEOGEN_URL, VIDEOGEN_MODEL).
"""
import base64, json, os, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from _paths import IMAGEGEN

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
for line in (IMAGEGEN.parent / ".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip())

cfg = json.loads((here / "src" / "motion.json").read_text(encoding="utf-8"))
out = here / "assets" / "motion"; out.mkdir(parents=True, exist_ok=True)
ids = sys.argv[1:] or [i for i in cfg["clips"] if not (out / f"{i}.mp4").exists()]


def gen(cid):
    t0 = time.time()
    url = "data:image/png;base64," + base64.b64encode((here / "assets" / "keyframes" / f"{cid}.png").read_bytes()).decode()
    body = {"model": os.environ.get("VIDEOGEN_MODEL", "muse-web/muse-video"), "prompt": cfg["common"] + " " + cfg["clips"][cid],
            "image": url, "image_url": url, "input_reference": url}
    req = urllib.request.Request(os.environ["VIDEOGEN_URL"], json.dumps(body).encode(),
                                 {"Content-Type": "application/json", "Authorization": "Bearer " + os.environ["IMAGEGEN_KEY"]})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            d = json.load(r)
        v = d["video"]
        raw = out / f"{cid}_raw.mp4"
        raw.write_bytes(base64.b64decode(v["url"].split(",", 1)[1]))
        # user không cần tiếng cười nói/âm gốc của clip: bỏ stream audio, giữ nguyên hình (không mã hoá lại)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(raw), "-an", "-c:v", "copy", str(out / f"{cid}.mp4")], check=True)
        raw.unlink()
        return f"{cid}: OK {v.get('width')}x{v.get('height')} ({time.time() - t0:.0f}s)"
    except Exception as e:
        return f"{cid}: LỖI {e}"


with ThreadPoolExecutor(1) as ex:
    for msg in ex.map(gen, ids):
        print(msg, flush=True)
