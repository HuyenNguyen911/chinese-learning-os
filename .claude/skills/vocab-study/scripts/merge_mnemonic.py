# -*- coding: utf-8 -*-
# Gộp kết quả workflow mẹo nhớ vào data/mnemonic.json.
# Chạy:  python .../merge_mnemonic.py <đường_dẫn_file_output_workflow>
#   file output workflow là JSON {summary,...,"result":{word:mn,...}} hoặc trực tiếp {word:mn}.
import json, os, sys, re
for _s in (sys.stdout, sys.stderr):  # console Windows cp1252 → tránh crash khi print 中文/tiếng Việt
    try: _s.reconfigure(encoding="utf-8")
    except Exception: pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
mp = os.path.join(DATA, "mnemonic.json")

if len(sys.argv) < 2:
    print("Thiếu tham số: đường dẫn file output workflow"); raise SystemExit(1)

raw = open(sys.argv[1], encoding="utf-8").read()
try:
    obj = json.loads(raw)
except Exception:
    obj = json.loads(re.search(r"\{.*\}", raw, re.S).group(0))
res = obj.get("result", obj) if isinstance(obj, dict) else {}

mn = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else {}
added = 0
for k, v in res.items():
    if isinstance(v, str) and v.strip() and '"w":' not in v and '\\"w\\"' not in v and k not in mn:
        mn[k] = v.strip(); added += 1
json.dump(mn, open(mp, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("mnemonic.json:", len(mn), "từ | thêm mới:", added)
