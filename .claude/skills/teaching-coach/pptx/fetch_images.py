#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_images.py — Tải ảnh minh hoạ (Creative Commons) theo nội dung bài giảng.

Nguồn: Openverse API (api.openverse.org) — ảnh CC, không cần API key cho search.
Nhận 1 manifest JSON: {"out_dir": "...", "images": [{"name","query"}, ...]}
Với mỗi mục: search Openverse, chọn ảnh phù hợp (lọc mature), tải về <out_dir>/<name>.jpg,
ghi attribution vào <out_dir>/credits.json.

Chạy:
    python fetch_images.py <manifest.json>

Cần: internet + Pillow (kiểm tra ảnh hợp lệ). In ra dòng trạng thái cho mỗi ảnh.
"""

import json
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

try:
    from PIL import Image
    _HAS_PIL = True
except Exception:
    _HAS_PIL = False

UA = "teaching-coach-fetch/1.0 (educational; Chinese lesson slides)"
API = "https://api.openverse.org/v1/images/"


def _get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def search(query, page_size=8, orientation="wide"):
    qs = urllib.parse.urlencode({
        "q": query,
        "license_type": "commercial",   # cho phép dùng rộng rãi
        "mature": "false",
        "page_size": page_size,
        "orientation": orientation,
    })
    # Openverse ẩn danh có rate-limit -> thử lại có backoff khi bị 403/429
    for attempt in range(4):
        try:
            data = json.loads(_get(API + "?" + qs))
            return data.get("results", [])
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and attempt < 3:
                time.sleep(4 * (attempt + 1))
                continue
            return []
        except Exception:
            return []
    return []


def download(query, dest, orientation="wide"):
    """Thử lần lượt các kết quả cho tới khi tải + mở được 1 ảnh hợp lệ."""
    for res in search(query, orientation=orientation):
        url = res.get("url") or res.get("thumbnail")
        if not url:
            continue
        try:
            raw = _get(url, timeout=35)
            if len(raw) < 4000:      # quá nhỏ -> nghi ảnh lỗi
                continue
            dest.write_bytes(raw)
            if _HAS_PIL:
                # Openverse trả về nhiều format (WEBP/PNG/GIF...) dù URL đuôi
                # .jpg -> python-pptx chỉ nhận BMP/GIF/JPEG/PNG/TIFF/WMF, nên
                # luôn ép về JPEG thật sau khi tải (re-encode, không chỉ đổi tên).
                with Image.open(str(dest)) as im:
                    im.load()
                    if im.format != "JPEG":
                        im.convert("RGB").save(str(dest), "JPEG", quality=90)
            return {
                "title": res.get("title"),
                "creator": res.get("creator"),
                "license": "%s %s" % (res.get("license", ""),
                                      res.get("license_version", "")),
                "source": res.get("foreign_landing_url"),
                "attribution": res.get("attribution"),
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
    spec = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    out_dir = Path(spec["out_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    credits = {}
    ok = 0
    for img in spec.get("images", []):
        name, query = img["name"], img["query"]
        orientation = img.get("orientation", "wide")
        dest = out_dir / (name + ".jpg")
        if dest.exists() and dest.stat().st_size > 4000:
            print("CACHED %s" % name); ok += 1
            continue
        info = download(query, dest, orientation=orientation)
        if info:
            credits[name] = {**info, "query": query}
            print("OK     %s  <- %s" % (name, query))
            ok += 1
        else:
            print("FAIL   %s  (query: %s)" % (name, query))
        time.sleep(2)   # tránh rate-limit Openverse ẩn danh
    (out_dir / "credits.json").write_text(
        json.dumps(credits, ensure_ascii=False, indent=2), encoding="utf-8")
    print("DONE: %d/%d images -> %s" % (ok, len(spec.get("images", [])), out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
