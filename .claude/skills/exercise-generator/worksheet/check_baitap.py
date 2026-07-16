#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_baitap.py — Tự soát 1 file baitap-buoiX.json TRƯỚC khi trình user / render.

Kiểm 2 thứ user quan tâm nhất:
  1) KHÔNG câu nào trùng nguyên văn giữa các block (dien/sap/dich/nghe/听后重复).
  2) Tổng số mục (nhắc "gọn": ~25–27 là vừa) + liệt kê câu để soi độ phủ vốn từ.

Tùy chọn: truyền thêm các từ cần phủ (--cover 红色 蓝色 个 口 …) để in tỉ lệ phủ.

Chạy:
    python check_baitap.py <baitap.json> [--cover w1 w2 ...]
Thoát mã 1 nếu có câu trùng (để hook/chặn được).
"""

import json
import sys
from collections import Counter
from pathlib import Path


def prod_sentences(spec):
    """Các câu học viên tự sản sinh / nghe — nơi dễ trùng nhất."""
    out = []
    for b in spec.get("blocks", []):
        t = b.get("type")
        if t == "dien_cho_trong":
            out += [it.get("q", "").replace("{}", it.get("answer", ""))
                    for it in b.get("items", [])]
        elif t == "sap_xep":
            out += [it.get("answer", "") for it in b.get("items", [])]
        elif t == "dich_dat_cau":
            out += [it.get("answer", "") for it in b.get("items", [])]
        elif t == "nghe":
            out += [it.get("script", "") for it in b.get("items", [])]
        elif t == "noi_hskk" and b.get("part") == "听后重复":
            out += [it.get("script", "") for it in b.get("items", [])]
    return [s for s in out if s]


def n_items(spec):
    n = 0
    for b in spec.get("blocks", []):
        if b.get("type") == "noi":
            n += len(b.get("pairs", []))
        elif b.get("type") == "doc_hieu":
            n += len(b.get("questions", []))
        else:
            n += len(b.get("items", []))
    return n


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print("Usage: python check_baitap.py <baitap.json> [--cover w1 w2 ...]",
              file=sys.stderr)
        return 2
    spec = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    sents = prod_sentences(spec)
    dups = [x for x, c in Counter(sents).items() if c > 1]

    total = n_items(spec)
    print("Tổng mục: %d  (%s)" % (
        total, "gọn ✅" if total <= 29 else "hơi dài ⚠️ (>29, nên cắt bớt)"))
    print("Câu sản sinh/nghe: %d" % len(sents))
    if dups:
        print("TRÙNG NGUYÊN VĂN ⚠️ (phải sửa):")
        for d in dups:
            print("   -", d)
    else:
        print("Trùng nguyên văn: KHÔNG ✅")

    cover = argv[argv.index("--cover") + 1:] if "--cover" in argv else []
    if cover:
        blob = json.dumps(spec, ensure_ascii=False)
        hit = [w for w in cover if w in blob]
        miss = [w for w in cover if w not in blob]
        print("Độ phủ vốn từ: %d/%d  →  có: %s" % (
            len(hit), len(cover), " ".join(hit)))
        if miss:
            print("   chưa dùng: %s" % " ".join(miss))

    return 1 if dups else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
