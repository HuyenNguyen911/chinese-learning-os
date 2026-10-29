# -*- coding: utf-8 -*-
# Đồng bộ tiến độ HSK6 qua git: gộp tu-vung-progress.js (trang web ghi) với bản trên origin/main,
# commit + push. Chạy từ gốc repo: python .claude/skills/vocab-study/scripts/sync_progress.py
# Gộp theo luật trong trang: SRS/db theo ts từng từ, cờ đánh dấu theo flagsTs cả bản.
import json, subprocess, sys
from datetime import datetime, timezone

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8")
    except Exception: pass

F = "output/Giáo trình chuẩn/hsk6/study/tu-vung-progress.js"
BRANCH = "main"  # vocab-study là tool dùng chung → luôn main (CLAUDE.md §5.5 mục 7)


def git(*a, check=True):
    r = subprocess.run(["git", "-c", "core.quotepath=off", *a], capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode:
        sys.exit("git %s lỗi:\n%s%s" % (" ".join(a), r.stdout, r.stderr))
    return r.stdout.strip()


def parse(t):
    return json.loads(t[t.index("{"): t.rindex("}") + 1]) if t.strip() else {}


def pick(a, b):
    if not a: return b
    if not b: return a
    ta, tb = a.get("ts", ""), b.get("ts", "")
    if ta == tb: return a if a.get("box", 0) >= b.get("box", 0) else b
    return a if ta > tb else b


def merge(L, R):
    out = {"ver": 2, "srs": {}, "db": {}}
    for w in {**L.get("srs", {}), **R.get("srs", {})}:
        out["srs"][w] = pick(L.get("srs", {}).get(w), R.get("srs", {}).get(w))
    for w in {**L.get("db", {}), **R.get("db", {})}:
        x, y = L.get("db", {}).get(w), R.get("db", {}).get(w)
        out["db"][w] = x or y if not (x and y) else (x if x.get("_ts", "") > y.get("_ts", "") else y)
    lf, rf = L.get("flagsTs", ""), R.get("flagsTs", "")
    out["flags"] = (L if lf >= rf else R).get("flags", {})
    out["flagsTs"] = max(lf, rf)
    return out


cur = git("branch", "--show-current")
if cur != BRANCH:
    sys.exit("Đang ở nhánh '%s', cần '%s' (tiến độ vocab-study là data dùng chung)." % (cur, BRANCH))

git("fetch", "origin")
try:
    local = parse(open(F, encoding="utf-8").read())
except FileNotFoundError:
    local = {}
r = subprocess.run(["git", "show", "origin/%s:%s" % (BRANCH, F)], capture_output=True, text=True, encoding="utf-8")
remote = parse(r.stdout) if r.returncode == 0 else {}

# Tùy chọn: argv[1] = file JSON của document cloud progress/hsk6 (Claude đọc bằng ArtifactData, out_dir) → gộp thêm
if len(sys.argv) > 1:
    cloud = json.loads(json.load(open(sys.argv[1], encoding="utf-8"))["json"])
    local = merge(local, cloud)

merged = merge(local, remote)
merged["exportedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
new_text = "window.__PROGRESS=" + json.dumps(merged, ensure_ascii=False) + ";\n"
def core(d):
    return {k: d.get(k) for k in ("srs", "db", "flags", "flagsTs")}


if remote and core(merged) == core(remote) and core(local) == core(remote):
    print("Tiến độ không đổi so với origin — không có gì để đồng bộ.")
else:
    open(F, "w", encoding="utf-8").write(new_text)
    git("add", F)
    if git("diff", "--cached", "--name-only"):
        git("commit", "-m", "chore(vocab-study): dong bo tien do HSK6\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>")

# Kéo phần còn lại của origin về; file tiến độ đã là bản gộp nên ưu tiên bản local nếu xung đột
git("merge", "origin/%s" % BRANCH, "-X", "ours", "--no-edit", check=False)
git("push", "origin", BRANCH)
print("Đã đồng bộ: %d từ SRS, %d ghi chú sửa, %d cờ. Máy khác chỉ cần git pull rồi mở trang." % (
    len(merged["srs"]), len(merged["db"]), len(merged["flags"])))
