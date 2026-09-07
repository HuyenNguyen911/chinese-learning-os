#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_images.py — Tải ảnh minh hoạ (ảnh chụp thật, không lẫn minh hoạ/clip-art)
theo nội dung bài giảng.

Nguồn: Pexels API (api.pexels.com) — toàn bộ nội dung là ảnh chụp thật (không có
mục illustration/vector như Openverse/Pixabay). Cần API key miễn phí (lấy tức thì,
không cần duyệt) tại https://www.pexels.com/api/ — đặt vào biến môi trường
`PEXELS_API_KEY` trước khi chạy.

Nhận 1 manifest JSON: {"out_dir": "...", "images": [{"name","query"}, ...]}
Với mỗi mục: search Pexels, chọn ảnh phù hợp, tải về <out_dir>/<name>.jpg,
ghi attribution vào <out_dir>/credits.json.

Chạy:
    PEXELS_API_KEY=xxxx python fetch_images.py <manifest.json>

Cần: internet + Pillow (kiểm tra ảnh hợp lệ). In ra dòng trạng thái cho mỗi ảnh.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
import urllib.parse
from pathlib import Path

try:
    from PIL import Image
    _HAS_PIL = True
except Exception:
    _HAS_PIL = False

UA = "teaching-coach-fetch/1.0 (educational; Chinese lesson slides)"
API = "https://api.pexels.com/v1/search"

ORIENTATION_MAP = {
    "wide": "landscape",
    "landscape": "landscape",
    "tall": "portrait",
    "portrait": "portrait",
    "square": "square",
}


def _api_key():
    key = os.environ.get("PEXELS_API_KEY", "").strip()
    if not key:
        print(
            "LOI: thieu bien moi truong PEXELS_API_KEY. "
            "Lay key mien phi tai https://www.pexels.com/api/ roi chay lai "
            "voi PEXELS_API_KEY=xxxx.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return key


def _get(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def search(query, api_key, page_size=8, orientation="wide"):
    qs = urllib.parse.urlencode({
        "query": query,
        "per_page": page_size,
        "orientation": ORIENTATION_MAP.get(orientation, "landscape"),
    })
    for attempt in range(4):
        try:
            data = json.loads(_get(API + "?" + qs, headers={"Authorization": api_key}))
            return data.get("photos", [])
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and attempt < 3:
                time.sleep(4 * (attempt + 1))
                continue
            return []
        except Exception:
            return []
    return []


def download(query, dest, api_key, orientation="wide"):
    """Thử lần lượt các kết quả cho tới khi tải + mở được 1 ảnh hợp lệ."""
    for res in search(query, api_key, orientation=orientation):
        src = res.get("src", {})
        url = src.get("large") or src.get("original") or src.get("medium")
        if not url:
            continue
        try:
            raw = _get(url, timeout=35)
            if len(raw) < 4000:      # quá nhỏ -> nghi ảnh lỗi
                continue
            dest.write_bytes(raw)
            if _HAS_PIL:
                # Pexels trả JPEG thật, nhưng vẫn ép lại cho chắc (đồng nhất
                # với hành vi cũ, phòng trường hợp CDN trả format khác).
                with Image.open(str(dest)) as im:
                    im.load()
                    if im.format != "JPEG":
                        im.convert("RGB").save(str(dest), "JPEG", quality=90)
            return {
                "title": query,
                "creator": res.get("photographer"),
                "license": "Pexels License",
                "source": res.get("url"),
                "attribution": "Photo by %s on Pexels" % res.get("photographer", "?"),
            }
        except Exception:
            if dest.exists():
                dest.unlink(missing_ok=True)
            continue
    return None


def main(argv):
    if len(argv) != 2:
        print("Usage: python fetch_images.py <manifest.json>", file=sys.stderr)
        return 2
    api_key = _api_key()
    spec = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    out_dir = Path(spec["out_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    credits_path = out_dir / "credits.json"
    credits = json.loads(credits_path.read_text(encoding="utf-8")) if credits_path.exists() else {}
    ok = 0
    for img in spec.get("images", []):
        name, query = img["name"], img["query"]
        orientation = img.get("orientation", "wide")
        dest = out_dir / (name + ".jpg")
        if dest.exists() and dest.stat().st_size > 4000:
            print("CACHED %s" % name); ok += 1
            continue
        info = download(query, dest, api_key, orientation=orientation)
        if info:
            credits[name] = {**info, "query": query}
            print("OK     %s  <- %s" % (name, query))
            ok += 1
        else:
            print("FAIL   %s  (query: %s)" % (name, query))
        time.sleep(1)   # tránh vượt rate-limit Pexels (200 req/gio)
    credits_path.write_text(
        json.dumps(credits, ensure_ascii=False, indent=2), encoding="utf-8")
    print("DONE: %d/%d images -> %s" % (ok, len(spec.get("images", [])), out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
