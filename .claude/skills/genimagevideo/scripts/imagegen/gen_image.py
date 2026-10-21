"""Sinh ảnh qua 9router (gemini-3.1-flash-image).

Dùng:  python scripts/imagegen/gen_image.py "prompt" -o out.png [--size auto]
Key đọc từ scripts/imagegen/.env (gitignored) hoặc biến môi trường IMAGEGEN_*.
"""
import sys as _s; _s.stdout.reconfigure(encoding="utf-8")
import argparse, base64, json, os, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).parent


def load_env():
    f = HERE / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def main():
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("-o", "--out", default="image.png")
    ap.add_argument("--size", default="auto")
    ap.add_argument("-n", type=int, default=1)
    a = ap.parse_args()

    body = {
        "model": os.environ["IMAGEGEN_MODEL"], "prompt": a.prompt, "n": a.n,
        "size": a.size, "quality": "auto", "background": "auto",
        "image_detail": "high", "output_format": "png",
    }
    req = urllib.request.Request(
        os.environ["IMAGEGEN_URL"], json.dumps(body).encode(),
        {"Content-Type": "application/json",
         "Authorization": "Bearer " + os.environ["IMAGEGEN_KEY"]})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.load(r)

    out = Path(a.out)
    for i, item in enumerate(data["data"]):
        p = out if a.n == 1 else out.with_stem(f"{out.stem}_{i+1}")
        if item.get("b64_json"):
            p.write_bytes(base64.b64decode(item["b64_json"]))
        elif item.get("url"):
            urllib.request.urlretrieve(item["url"], p)
        else:
            sys.exit("Phản hồi không có ảnh: " + json.dumps(data)[:300])
        print("Saved", p)


if __name__ == "__main__":
    main()
