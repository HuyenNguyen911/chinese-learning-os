# -*- coding: utf-8 -*-
# Áp dụng hàng chờ "lên hạng C" xuất từ trang flashcard (tu-vung-promote-to-c.json)
# vào knowledge/vocabulary/tier-*.md, rồi recalc state/activation.md.
# Phạm vi CHỈ: Activation D -> C, Seen +1, Last Studied = hôm nay.
# KHÔNG đụng: Confidence, Speaking, Writing, Activation B/A, không thêm entry mới
# (từ chưa có trong tier-*.md nghĩa là chưa được Learning Strategist đưa vào vault -> bỏ qua + báo cáo).
import re, json, sys, os, datetime

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8")
    except Exception: pass

TIERS = ["knowledge/vocabulary/tier-a.md", "knowledge/vocabulary/tier-b.md", "knowledge/vocabulary/tier-c.md"]
ACT_FILE = "state/activation.md"
DEFAULT_INPUT = "output/Giáo trình chuẩn/hsk6/study/tu-vung-promote-to-c.json"
TODAY = datetime.date.today().isoformat()


def find_block(text, word):
    pat = re.compile(r'(^## ' + re.escape(word) + r'\n.*?)(?=\n---|\Z)', re.S | re.M)
    return pat.search(text)


def apply_to_tier(path, remaining, promoted, skipped):
    if not os.path.exists(path) or not remaining:
        return
    text = open(path, encoding="utf-8").read()
    changed = False
    for w in list(remaining):
        m = find_block(text, w)
        if not m:
            continue
        block = m.group(1)
        act_m = re.search(r'Activation:\s*([ABCD])', block)
        if not act_m:
            continue
        if act_m.group(1) != 'D':
            skipped.append((w, act_m.group(1)))
            remaining.discard(w)
            continue
        new_block = re.sub(r'Activation:\s*D', 'Activation: C', block, count=1)
        seen_m = re.search(r'Seen:\s*(\d+)', new_block)
        if seen_m:
            new_block = re.sub(r'Seen:\s*\d+', 'Seen: %d' % (int(seen_m.group(1)) + 1), new_block, count=1)
        new_block = re.sub(r'Last Studied:\s*.+', 'Last Studied: %s' % TODAY, new_block, count=1)
        text = text[:m.start(1)] + new_block + text[m.end(1):]
        changed = True
        promoted.append(w)
        remaining.discard(w)
    if changed:
        open(path, "w", encoding="utf-8").write(text)


def recalc_activation_aggregate():
    total, activated, conf_sum, conf_n = 0, 0, 0.0, 0
    tier_counts = {"A": 0, "B": 0, "C": 0}
    tier_letter = {"knowledge/vocabulary/tier-a.md": "A",
                    "knowledge/vocabulary/tier-b.md": "B",
                    "knowledge/vocabulary/tier-c.md": "C"}
    for path in TIERS:
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        letter = tier_letter[path]
        for blk in text.split("\n## ")[1:]:
            act_m = re.search(r'Activation:\s*([ABCD])', blk)
            if not act_m:
                continue
            total += 1
            tier_counts[letter] += 1
            if act_m.group(1) in ("A", "B"):
                activated += 1
            conf_m = re.search(r'Confidence:\s*(\d+)%', blk)
            if conf_m:
                conf_sum += int(conf_m.group(1))
                conf_n += 1
    rate = round(activated / total * 100) if total else 0
    avg_conf = round(conf_sum / conf_n) if conf_n else 0
    old = open(ACT_FILE, encoding="utf-8").read() if os.path.exists(ACT_FILE) else ""
    tail_m = re.search(r'(Master backlog.*)', old, re.S)
    tail = tail_m.group(1) if tail_m else ""
    content = (
        "# Vocabulary Activation\n"
        "Last Updated: %s\n\n"
        "Total (active, trong tiers): %d | Activated (≥B): %d | Rate: %d%%\n"
        "Avg Confidence: %d%%\n"
        "Tier A: %d | Tier B: %d | Tier C: %d\n\n"
    ) % (TODAY, total, activated, rate, avg_conf, tier_counts["A"], tier_counts["B"], tier_counts["C"])
    open(ACT_FILE, "w", encoding="utf-8").write(content + tail)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
    if not os.path.exists(path):
        print("Không tìm thấy %s. Truyền path làm tham số nếu file ở chỗ khác." % path)
        return
    data = json.load(open(path, encoding="utf-8"))
    words = [w["w"] for w in data.get("words", [])]
    remaining = set(words)
    promoted, skipped = [], []
    for tier_path in TIERS:
        apply_to_tier(tier_path, remaining, promoted, skipped)
    not_found = sorted(remaining)

    recalc_activation_aggregate()

    print("Promoted D -> C: %d" % len(promoted))
    for w in promoted:
        print("  + %s" % w)
    if skipped:
        print("Bo qua (da o hang khac D, khong dung): %d" % len(skipped))
        for w, a in skipped:
            print("  - %s (dang %s)" % (w, a))
    if not_found:
        print("Chua co trong tier-*.md (chua vao vault, bo qua): %d" % len(not_found))
        for w in not_found:
            print("  ? %s" % w)

    os.remove(path)
    print("Da xu ly xong, da xoa %s" % path)


if __name__ == "__main__":
    main()
