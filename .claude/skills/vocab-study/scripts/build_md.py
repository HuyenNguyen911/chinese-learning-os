# -*- coding: utf-8 -*-
# Build output/study/hsk6/tu-vung.md từ raw/Từ vựng.xlsx (2 sheet: 'Từ vựng' + 'Chung từ')
import json, re, os, sys
from collections import Counter
from pypinyin import pinyin, Style
for _s in (sys.stdout, sys.stderr):  # console Windows cp1252 → tránh crash khi print 中文/tiếng Việt
    try: _s.reconfigure(encoding="utf-8")
    except Exception: pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
tv = json.load(open(os.path.join(DATA, "tv.json"), encoding="utf-8"))
ct = json.load(open(os.path.join(DATA, "ct.json"), encoding="utf-8"))
OV = json.load(open(os.path.join(DATA, "desc_override.json"), encoding="utf-8"))
# Nghĩa Việt do hệ thống bổ sung cho từ có cột 意义 trống (song song desc_override cho 释义)
_vi_ov = os.path.join(DATA, "vi_override.json")
VI_OV = json.load(open(_vi_ov, encoding="utf-8")) if os.path.exists(_vi_ov) else {}
# 例句 cá nhân hoá (bám user-profile) — ƯU TIÊN thay câu bài khóa cho từ có trong file
_ex_ov = os.path.join(DATA, "ex_override.json")
EX_OV = json.load(open(_ex_ov, encoding="utf-8")) if os.path.exists(_ex_ov) else {}
# Tên mỗi bài khóa (标题) — hiển thị cạnh "Bài N". Thiếu file thì bỏ qua (tương thích ngược).
_titles_path = os.path.join(DATA, "bai_titles.json")
TITLES = json.load(open(_titles_path, encoding="utf-8")) if os.path.exists(_titles_path) else {}
# 拓展 bổ sung tay cho bài sheet 'Chung từ' thiếu (vd Bài 28)
_exp = os.path.join(DATA, "exp_extra.json")
if os.path.exists(_exp):
    for k, v in json.load(open(_exp, encoding="utf-8")).items():
        ct.setdefault(k, [])
        ct[k].extend(v)
OUT = "output/study/hsk6/tu-vung.md"

HAN = r"[一-鿿]"

ER_KEEP = {"婴儿", "女儿", "儿子", "儿童", "幼儿", "孤儿", "育儿", "宠儿",
           "健儿", "男儿", "混血儿", "少儿", "托儿所", "儿女"}
PINYIN_OVERRIDE = {"古朴": "gǔpǔ", "简朴": "jiǎnpǔ", "巴不得": "bābude",
                   "恨不得": "hènbude", "堵得慌": "dǔdehuāng",
                   "琢磨": "zuómo"}  # nghĩa "suy nghĩ, cân nhắc" (không phải zhuómó = đẽo gọt)
_VOWEL = set("aāáǎàoōóǒòeēéěê")

def py(w):
    w = re.sub(r"[^一-鿿]", "", w)
    if not w:
        return ""
    if w in PINYIN_OVERRIDE:
        return PINYIN_OVERRIDE[w]
    sylls = [s[0] for s in pinyin(w, style=Style.TONE, errors="ignore")]
    if not sylls:
        return ""
    if "朴" in w:  # 朴 hầu như luôn đọc pǔ, pypinyin hay nhầm piáo
        sylls = ["pǔ" if s == "piáo" else s for s in sylls]
    # 儿化: bỏ âm 'ér' cuối, thêm 'r' vào âm trước (trừ các từ 儿=âm thật)
    if w.endswith("儿") and w not in ER_KEEP and len(sylls) >= 2 and sylls[-1] in ("ér", "er"):
        sylls = sylls[:-1]
        sylls[-1] = sylls[-1] + "r"
    out = sylls[0]
    for s in sylls[1:]:
        out += ("'" + s) if (s and s[0] in _VOWEL) else s
    return out

def cell(s):
    return (s or "").replace("|", "／").replace("\n", " ").strip()

def clean_ex(ex):
    ex = (ex or "").split("//")[0].split(" / ")[0].split("//")[0]
    ex = re.sub(r"（[^）]*[A-Za-z][^）]*）", "", ex)
    ex = re.sub(r"\([^)]*[A-Za-z][^)]*\)", "", ex)
    return ex.strip()

def norm_w(w):
    return (w or "").strip().strip("·•.").strip()

def is_seed(w, ex):
    return len(w) == 1 and (ex.strip() == "" or ("、" in ex and not re.search(r"[。！？!?]", ex)))

def shared_char(members):
    cnt = Counter()
    for m in members:
        for ch in set(re.findall(HAN, m)):
            cnt[ch] += 1
    if cnt:
        ch, c = cnt.most_common(1)[0]
        if c >= 2:
            return ch
    return ""

def split_members(grp):
    return [x.strip() for x in re.split(r"[、\-/／]", grp) if x.strip()]

def chip(member):
    # member: dict {"w":..., "g":...} — g = nghĩa tiếng Việt (tùy chọn), mã hoá 〖g〗
    w = member["w"] if isinstance(member, dict) else member
    g = (member.get("g") if isinstance(member, dict) else "") or ""
    m = re.match(r"(" + HAN + r"+)(.*)", w.strip())
    if not m:
        base = cell(w)
    else:
        han, rest = m.group(1), m.group(2).strip()
        base = cell("%s %s%s" % (han, py(han), (" " + rest if rest else "")))
    g = g.strip()
    return base + ("〖%s〗" % cell(g) if g else "")

def exp_line(members, note, label):
    chips = " · ".join(chip(m) for m in members)
    head = "**%s**" % cell(label if label else "拓展")
    if note:
        head += " (%s)" % cell(note)
    return "- %s: %s" % (head, chips)

def build_bai(n):
    rows = tv.get(str(n), [])
    words, seeds = [], []
    for r in rows:
        w = norm_w(r["w"])
        if not w:
            continue
        if is_seed(w, r["ex"]):
            if r["ex"].strip():  # single-char + 、list => 拓展 seed có thành viên
                seeds.append((w, r["ex"]))
            # single-char rỗng: bỏ (đã có trong 'Chung từ')
            continue
        words.append(r)
    # ---- 生词 table ----
    _t = TITLES.get(str(n), "").strip()
    heading = "## Bài %d — %s" % (n, _t) if _t else "## Bài %d" % n
    out = [heading, "", "### 生词", "",
           "| 生词 | Pinyin | 释义 | Nghĩa | 例句 |", "| --- | --- | --- | --- | --- |"]
    for r in words:
        w = norm_w(r["w"])
        rj = r["desc"].strip() if r["desc"].strip() else OV.get(w, "")
        vv = r["vi"].strip() if r["vi"].strip() else VI_OV.get(w, "")
        exv = EX_OV.get(w) or clean_ex(r["ex"])  # câu cá nhân hoá ưu tiên thay câu bài khóa
        out.append("| %s | %s | %s | %s | %s |" % (cell(w), py(w), cell(rj), cell(vv), cell(exv)))
    # ---- 生词拓展 ----
    groups = []
    for g in ct.get(str(n), []):
        if "members" in g:  # format giàu: root + từng từ con có nghĩa (vd exp_extra Bài 29)
            mem = [{"w": m["w"], "g": m.get("g", "")} for m in g["members"]]
            groups.append((mem, g.get("vi", "").strip(), g.get("root", "").strip()))
            continue
        grp = g["grp"].strip()
        note = g["vi"].strip()
        if re.search(r"\bvs\b| và |[A-Za-zÀ-ỹ]{2,}", grp) and "、" not in grp and "-" not in grp:
            groups.append(([{"w": grp, "g": ""}], note, "⇄ so sánh"))
        else:
            mem = [{"w": x, "g": ""} for x in split_members(grp)]
            groups.append((mem, note, shared_char([m["w"] for m in mem])))
    for w, ex in seeds:  # seed 1 chữ trong 'Từ vựng' (vd 宠/染/恋…)
        mem = [{"w": x, "g": ""} for x in split_members(ex)]
        groups.append((mem, "", w))
    if groups:
        out += ["", "### 生词拓展", ""]
        for mem, note, label in groups:
            out.append(exp_line(mem, note, label))
    out.append("")
    return "\n".join(out)

HEAD = ("# 生词 tích lũy — HSK6 (theo bài khóa)\n\n"
        "> Nguồn: `raw/Từ vựng.xlsx` (sheet 'Từ vựng' = 生词, sheet 'Chung từ' = 生词拓展).\n"
        "> Cột 释义 lấy từ cột 描述 của bạn; Bài 1–2 và vài từ lẻ do hệ thống bổ sung. Pinyin auto (pypinyin — có thể sai vài chữ đa âm).\n"
        "> Nghĩa Việt giữ theo cột 意义; chỗ nào Excel để trống thì lấy từ `vi_override.json` (dịch bổ sung, review được).\n"
        "> 例句 ưu tiên câu cá nhân hoá trong `ex_override.json` (bám user-profile); còn lại giữ câu bài khóa gốc.\n"
        "> Bài mới nhất hiển thị trên cùng trong bản HTML.\n\n---\n")

parts = [HEAD]
# Số bài lấy động theo dữ liệu (trước hardcode 28 → rớt bài mới như Bài 29 do lesson-prep thêm)
_maxn = max((int(k) for k in tv if str(k).isdigit()), default=0)
for n in range(1, _maxn + 1):
    if str(n) in tv:
        parts.append(build_bai(n))
open(OUT, "w", encoding="utf-8").write("\n".join(parts))
print("built", OUT, "| bài:", sum(1 for n in range(1, _maxn + 1) if str(n) in tv))
