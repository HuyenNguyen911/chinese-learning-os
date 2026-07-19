# -*- coding: utf-8 -*-
# Sinh file workflow data/wf_mnemonic.js CHỈ cho các từ CHƯA có trong data/mnemonic.json.
# Sau đó gọi tool Workflow({scriptPath: ".../data/wf_mnemonic.js"}) để sinh mẹo nhớ,
# rồi chạy merge_mnemonic.py để gộp kết quả vào data/mnemonic.json.
import json, re, os, sys
from pypinyin import pinyin as _py, Style
for _s in (sys.stdout, sys.stderr):  # console Windows cp1252 → tránh crash khi print 中文/tiếng Việt
    try: _s.reconfigure(encoding="utf-8")
    except Exception: pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

def clean(s):
    return re.sub(r"[\x00-\x1f  ﻿​-‏]", " ", str(s or "")).strip()

def pyw(w):
    w = re.sub(r"[^一-鿿]", "", w)
    return "".join(s[0] for s in _py(w, style=Style.TONE, errors="ignore")) if w else ""

def is_seed(w, ex):
    return len(w) == 1 and (ex.strip() == "" or ("、" in ex and not re.search(r"[。！？!?]", ex)))

tv = json.load(open(os.path.join(DATA, "tv.json"), encoding="utf-8"))
mn = {}
mp = os.path.join(DATA, "mnemonic.json")
if os.path.exists(mp):
    mn = json.load(open(mp, encoding="utf-8"))

DATAW = {}
for n in tv:
    lst = []
    for x in tv[n]:
        w = clean(x["w"]).strip("·•.").strip()
        if not w or is_seed(w, clean(x["ex"])) or w in mn:
            continue
        lst.append({"w": w, "py": clean(pyw(w)), "vi": clean(x["vi"]), "rj": clean(x["desc"])[:40]})
    if lst:
        DATAW[n] = lst

total = sum(len(v) for v in DATAW.values())
if total == 0:
    print("Không có từ mới cần sinh mẹo nhớ.")
    raise SystemExit(0)

INSTR = [
 "Ban la giao vien tieng Trung day nguoi Viet. Voi MOI tu HSK6 (Bai {N}) duoi day, viet MOT meo nho bang TIENG VIET, NGAN (1-2 cau), de toi muc hoc sinh tieu hoc cung hieu:",
 "- Chiet tu: tach chu Han thanh bo/thanh phan, noi nghia tung phan bang tieng Viet roi GHEP LAI thanh hinh anh lien he nghia cua tu.",
 "- Co the dung am Han-Viet khi huu ich; neu la chu hinh thanh co the nhac nhe phan goi am.",
 "- CAM dung thuat ngu kho (semantic / phonetic / hinh thanh / pictophonetic). Ke tu nhien, sinh dong, dung nghia cua tu (bam nghia Viet cho san).",
 "- Voi thanh ngu 4 chu: giai thich ngan y nghia + hinh anh goi nho.",
 "- Moi tu 1-2 cau, khong lan man. Viet DAU TIENG VIET day du.",
 "",
 "Vi du giong van (co dau day du trong cau tra loi):",
 "港 (gang) = cang -> \"氵 la nuoc, 巷 la con hem; ben CANG nhu nhung con hem tren mat nuoc cho tau thuyen luon vao dau.\"",
 "",
 "Danh sach tu (chu | pinyin | nghia Viet | 释义):",
]
TAIL = ["", "Tra JSON {items:[{w, mn}]} du moi tu tren; mn la cau meo nho TIENG VIET CO DAU."]
META = ('export const meta = { name: "hsk6-mnemonics", '
        'description: "Sinh meo nho tieng Viet (chiet tu) cho tu vung HSK6", '
        'phases: [{ title: "Sinh meo nho" }] };\n')
SCHEMA = ('{type:"object",additionalProperties:false,properties:{items:{type:"array",'
          'items:{type:"object",additionalProperties:false,properties:{w:{type:"string"},'
          'mn:{type:"string"}},required:["w","mn"]}}},required:["items"]}')

logic = (
 "const DATA = " + json.dumps(DATAW, ensure_ascii=False) + ";\n"
 "const SCHEMA = " + SCHEMA + ";\n"
 "const NL = String.fromCharCode(10);\n"
 "const INSTR = " + json.dumps(INSTR, ensure_ascii=False) + ";\n"
 "const TAIL = " + json.dumps(TAIL, ensure_ascii=False) + ";\n"
 "function buildPrompt(n, words){\n"
 "  const head = INSTR.map(function(s){return s.replace('{N}', String(n));}).join(NL);\n"
 "  const list = words.map(function(x){return x.w + ' | ' + x.py + ' | ' + x.vi + (x.rj ? ' | '+x.rj : '');}).join(NL);\n"
 "  return head + NL + list + NL + TAIL.join(NL);\n"
 "}\n"
 "const bais = (typeof args !== 'undefined' && args && args.bais) ? args.bais.map(String) : Object.keys(DATA);\n"
 "phase('Sinh meo nho');\n"
 "log('Sinh meo nho cho bai: ' + bais.join(', '));\n"
 "const chunks = await parallel(bais.map(function(n){ return function(){ return agent(buildPrompt(n, DATA[n]||[]), {schema: SCHEMA, label: 'Bai '+n}); }; }));\n"
 "const out = {};\n"
 "chunks.filter(Boolean).forEach(function(r){ (r.items||[]).forEach(function(it){ if (it && it.w) out[it.w] = it.mn; }); });\n"
 "log('Xong: ' + Object.keys(out).length + ' meo nho');\n"
 "return out;\n"
)
txt = (META + logic).replace("\r\n", "\n").replace("\r", "\n")
out_path = os.path.join(DATA, "wf_mnemonic.js")
open(out_path, "wb").write(txt.encode("utf-8"))
print("Đã ghi", out_path)
print("Cần sinh mẹo nhớ cho", total, "từ mới, ở bài:", ", ".join(sorted(DATAW, key=int)))
print(">> Gọi: Workflow({scriptPath: \"" + out_path.replace("\\", "/") + "\"})")
