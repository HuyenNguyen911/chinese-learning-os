# -*- coding: utf-8 -*-
# Dựng/bổ sung data/hanzi.json cho các chữ Hán trong data/tv.json.
#   Nguồn: Make Me a Hanzi (dictionary.txt) + Unihan (kVietnamese, kTraditionalVariant).
#   Tự tải nguồn vào data/_src/ nếu thiếu (cần mạng). hanzi.json đã có sẵn 1861 chữ;
#   script này chỉ cần chạy khi có CHỮ MỚI chưa có dữ liệu.
# Chạy:  python .claude/skills/vocab-study/scripts/build_hanzi.py
import json, re, os, sys, urllib.request, zipfile, io
from pypinyin import pinyin as _py, Style
for _s in (sys.stdout, sys.stderr):  # console Windows cp1252 → tránh crash khi print 中文/tiếng Việt
    try: _s.reconfigure(encoding="utf-8")
    except Exception: pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
SRC = os.path.join(DATA, "_src")
os.makedirs(SRC, exist_ok=True)
HAN = re.compile(r"[一-鿿]")
STRUCT = set("⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻")

def fetch(url, path):
    if not os.path.exists(path):
        print("tải", url)
        urllib.request.urlretrieve(url, path)

def ensure_sources():
    fetch("https://raw.githubusercontent.com/skishore/makemeahanzi/master/dictionary.txt",
          os.path.join(SRC, "dictionary.txt"))
    uz = os.path.join(SRC, "Unihan.zip")
    fetch("https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip", uz)
    for f in ("Unihan_Readings.txt", "Unihan_Variants.txt"):
        if not os.path.exists(os.path.join(SRC, f)):
            with zipfile.ZipFile(uz) as z:
                z.extract(f, SRC)

def load_hanviet():
    cp = lambda x: chr(int(x[2:], 16))
    HV, T2 = {}, {}
    for line in open(os.path.join(SRC, "Unihan_Readings.txt"), encoding="utf-8"):
        if "\tkVietnamese\t" in line:
            p = line.rstrip("\n").split("\t"); HV[cp(p[0])] = p[2].split()[0]
    for line in open(os.path.join(SRC, "Unihan_Variants.txt"), encoding="utf-8"):
        if "\tkTraditionalVariant\t" in line:
            p = line.rstrip("\n").split("\t")
            t = re.findall(r"U\+[0-9A-F]+", p[2])
            if t: T2[cp(p[0])] = cp(t[0])
    def hv(ch):
        if ch in HV: return HV[ch]
        if ch in T2 and T2[ch] in HV: return HV[T2[ch]]
        return ""
    return hv

def py1(ch):
    r = _py(ch, style=Style.TONE, errors="ignore")
    return r[0][0] if r and r[0] else ""

def comps(dc):
    return [c for c in dc if HAN.match(c) and c not in STRUCT and c != "？"]

def main():
    ensure_sources()
    D = {}
    for line in open(os.path.join(SRC, "dictionary.txt"), encoding="utf-8"):
        line = line.strip()
        if line:
            o = json.loads(line); D[o["character"]] = o
    hv = load_hanviet()
    tv = json.load(open(os.path.join(DATA, "tv.json"), encoding="utf-8"))
    chars = set()
    for n in tv:
        for x in tv[n]:
            chars |= set(HAN.findall(x["w"]))
    need = set(chars)
    for ch in list(chars):
        o = D.get(ch)
        if o: need |= set(comps(o.get("decomposition", "")))
    HZ = {}
    p = os.path.join(DATA, "hanzi.json")
    if os.path.exists(p):
        HZ = json.load(open(p, encoding="utf-8"))
    added = 0
    for ch in need:
        if ch in HZ:
            continue
        o = D.get(ch)
        if not o:
            continue
        ety = o.get("etymology") or {}
        e = {"d": (o.get("definition") or "").strip(), "p": py1(ch), "hv": hv(ch),
             "dc": o.get("decomposition", ""), "r": o.get("radical", ""),
             "e": ety.get("hint", ""), "et": ety.get("type", "")}
        if ety.get("semantic"): e["sem"] = ety["semantic"]
        if ety.get("phonetic"): e["phon"] = ety["phonetic"]
        cs = []
        for cc in comps(o.get("decomposition", "")):
            if cc == ch: continue
            co = D.get(cc)
            cs.append([cc, (co.get("definition", "").strip() if co else ""), py1(cc), hv(cc)])
        if cs: e["c"] = cs
        HZ[ch] = e; added += 1
    json.dump(HZ, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("hanzi.json:", len(HZ), "chữ | thêm mới:", added)

if __name__ == "__main__":
    main()
