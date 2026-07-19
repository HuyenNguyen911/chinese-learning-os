# -*- coding: utf-8 -*-
"""append_tier_a.py — append từ mới (Activation: D) vào knowledge/vocabulary/tier-a.md.

Append-only, dedup theo 生词 trên tier-a/b/c.md. Không sửa entry cũ.
Chạy từ gốc repo:  python append_tier_a.py <vocab_payload.json>
"""
import sys, json, re
from pathlib import Path

TIER_FILES = ["tier-a.md", "tier-b.md", "tier-c.md"]
FOOTER_PREFIX = "_Thêm từ mới"

ENTRY = """## {w}
- Pinyin: {pinyin}
- Nghĩa: {vi}
- Usage:
  - Seen: 0
  - Speaking: 0
  - Writing: 0
- Confidence: 0%
- Activation: D
- Last Studied: —

---

"""


def existing_words(vocab_dir):
    vocab_dir = Path(vocab_dir)
    words = set()
    for fn in TIER_FILES:
        p = vocab_dir / fn
        if p.exists():
            for m in re.finditer(r"^##\s+(.+?)\s*$",
                                 p.read_text(encoding="utf-8"), re.M):
                words.add(m.group(1).strip())
    return words


def append_words(payload, vocab_dir):
    vocab_dir = Path(vocab_dir)
    have = existing_words(vocab_dir)
    seen, entries = set(), []
    for it in payload.get("words", []):
        w = (it.get("w") or "").strip()
        if not w or w in have or w in seen:
            continue
        seen.add(w)
        entries.append(ENTRY.format(w=w, pinyin=it.get("pinyin", ""),
                                    vi=it.get("vi", "")))
    if not entries:
        return 0
    tier_a = vocab_dir / "tier-a.md"
    text = tier_a.read_text(encoding="utf-8")
    block = "".join(entries)
    lines = text.splitlines(keepends=True)
    idx = next((i for i, ln in enumerate(lines)
                if ln.lstrip().startswith(FOOTER_PREFIX)), None)
    if idx is not None:
        new_text = "".join(lines[:idx]) + block + "".join(lines[idx:])
    else:
        sep = "" if text.endswith("\n") else "\n"
        new_text = text + sep + block
    tier_a.write_text(new_text, encoding="utf-8")
    return len(entries)


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    if len(argv) != 2:
        print("Usage: python append_tier_a.py <vocab_payload.json>",
              file=sys.stderr); return 2
    payload = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    n = append_words(payload, Path("knowledge") / "vocabulary")
    print("append_tier_a: +%d từ mới -> tier-a.md" % n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
