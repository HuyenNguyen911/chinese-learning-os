# -*- coding: utf-8 -*-
# Render output/study/hsk6/tu-vung.md -> tu-vung.html
# Mỗi bài: bảng 生词 (+ tab 生词拓展 nếu có) + nút 🎓 Học (flashcard active-recall + Leitner SRS).
# Trạng thái ôn suy từ knowledge/vocabulary/tier-*.md (Activation). localStorage: nhớ sửa nội dung + tiến độ học.
import re, html, os, sys
from pypinyin import pinyin as _pyf, Style as _Style
for _s in (sys.stdout, sys.stderr):  # console Windows cp1252 → tránh crash khi print 中文/tiếng Việt
    try: _s.reconfigure(encoding="utf-8")
    except Exception: pass

def per_char_py(w):
    w = re.sub(r"[^一-鿿]", "", w)
    if not w:
        return ""
    return " ".join(s[0] for s in _pyf(w, style=_Style.TONE, errors="ignore"))

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(SCRIPT_DIR, "..", "data")
try:
    HZ_JSON = open(os.path.join(DATA, "hanzi.json"), encoding="utf-8").read()
except FileNotFoundError:
    HZ_JSON = "{}"
try:
    MN_JSON = open(os.path.join(DATA, "mnemonic.json"), encoding="utf-8").read()
except FileNotFoundError:
    MN_JSON = "{}"

MD = "output/study/hsk6/tu-vung.md"
OUT = "output/study/hsk6/tu-vung.html"
TIERS = [("A", "knowledge/vocabulary/tier-a.md"),
         ("B", "knowledge/vocabulary/tier-b.md"),
         ("C", "knowledge/vocabulary/tier-c.md")]

def parse_tiers():
    m = {}
    for tier, path in TIERS:
        if not os.path.exists(path):
            continue
        t = open(path, encoding="utf-8").read()
        for blk in t.split("\n## "):
            first = blk.strip().splitlines()[0].strip().lstrip("#").strip() if blk.strip() else ""
            act = re.search(r"Activation:\s*([ABCD])", blk)
            if not first or not act:
                continue
            g = lambda p, d="0": (re.search(p, blk) or [None, d])[1]
            m[first] = {"tier": tier, "act": act.group(1),
                        "last": (re.search(r"Last Studied:\s*(.+)", blk) or [None, "—"])[1].strip(),
                        "seen": g(r"Seen:\s*(\d+)"), "sp": g(r"Speaking:\s*(\d+)"), "wr": g(r"Writing:\s*(\d+)")}
    return m

STAT = parse_tiers()
ACTMAP = {"A": ("A", "a", "Activation A · tự tin dùng"),
          "B": ("B", "b", "Activation B · dùng được"),
          "C": ("C", "c", "Activation C · nhận ra"),
          "D": ("D", "d", "Activation D · mới học")}

txt = open(MD, encoding="utf-8").read()
idx = txt.find("## Bài")
sections = re.split(r"\n(?=## Bài )", txt[idx:])
bai = []
for sec in sections:
    mm = re.match(r"## Bài (\d+)(?:\s*—\s*(.+))?", sec)
    if not mm:
        continue
    num = int(mm.group(1))
    btitle = (mm.group(2) or "").strip()
    header, rows, exp = None, [], []
    for ln in sec.splitlines():
        s = ln.strip()
        if s.startswith("|") and "---" not in s:
            cs = [c.strip() for c in s.strip("|").split("|")]
            if len(cs) == 5:
                if header is None:
                    header = cs
                else:
                    rows.append(cs)
        elif s.startswith("- ") and "**" in s:
            exp.append(s[2:].strip())
    if rows:
        bai.append((num, header, rows, exp, btitle))
bai.sort(key=lambda x: x[0], reverse=True)

def esc(x):
    return html.escape(x)

def status_cell(word):
    st = STAT.get(word)
    if not st:
        return '<span class="st none" title="Chưa đưa vào học (còn ở kho backlog)">○</span>'
    label, cls, tip = ACTMAP.get(st["act"], (st["act"], "d", ""))
    full = "%s · ôn: Seen %s / Nói %s / Viết %s · Last: %s" % (tip, st["seen"], st["sp"], st["wr"], st["last"])
    return '<span class="st %s" title="%s">%s</span>' % (cls, esc(full), label)

def render_exp(line):
    # Sơ đồ cây: chữ gốc bên trái → các nhánh (汉字 · pinyin · nghĩa).
    m = re.match(r"\*\*(.+?)\*\*\s*(\(.*?\))?\s*:\s*(.*)", line)
    if not m:
        return '<div class="grp">%s</div>' % esc(line)
    root, rootgloss, words = m.group(1), (m.group(2) or "").strip("()"), m.group(3)
    branches = []
    for chunk in words.split(" · "):
        chunk = chunk.strip()
        if not chunk:
            continue
        g = ""
        gm = re.search(r"〖(.*?)〗", chunk)
        if gm:
            g = gm.group(1); chunk = (chunk[:gm.start()] + chunk[gm.end():]).strip()
        mm = re.match(r"([一-鿿]+)\s*(.*)", chunk)
        han, pyv = (mm.group(1), mm.group(2).strip()) if mm else (chunk, "")
        branches.append(
            '<div class="branch"><span class="bh">%s</span> <span class="bpy">%s</span>%s</div>'
            % (esc(han), esc(pyv), (' <span class="bg">%s</span>' % esc(g) if g else '')))
    rpy = ""
    if re.fullmatch(r"[一-鿿]+", root or ""):
        try:
            rpy = "".join(x[0] for x in _pyf(root, style=_Style.TONE, errors="ignore"))
        except Exception:
            rpy = ""
    rg = ('<span class="rgloss">%s</span>' % esc(rootgloss)) if rootgloss else ''
    rpys = ('<span class="tr-py">%s</span>' % esc(rpy)) if rpy else ''
    troot = '<div class="troot"><span class="tr-han">%s</span>%s%s</div>' % (esc(root), rpys, rg)
    return '<div class="grp"><div class="tree">%s<div class="branches">%s</div></div></div>' % (
        troot, "".join(branches))

CSS = r"""
:root{--bd:#dcdcdc;--head:#2b3a67;--headtx:#fff;--zebra:#f7f9fc;--accent:#2b6cb0;--study:#6d28d9;}
*{box-sizing:border-box;}
body{margin:0;font-family:"Segoe UI","PingFang SC","Microsoft YaHei",system-ui,sans-serif;color:#1a1a1a;background:#fafafa;line-height:1.5;}
.bar{display:flex;gap:10px;align-items:center;padding:6px 14px;background:#fff;border-bottom:1px solid var(--bd);position:sticky;top:0;z-index:20;}
.bar h1{font-size:15px;margin:0;color:var(--head);white-space:nowrap;}
#voicesel{margin-left:auto;max-width:230px;font-size:12px;padding:3px 6px;border:1px solid var(--bd);border-radius:6px;color:var(--head);background:#fff;}
#q{flex:1;padding:5px 10px;border:1px solid var(--bd);border-radius:6px;font-size:14px;min-width:120px;}
.tip{color:#999;cursor:help;font-size:14px;}
.legend{font-size:11.5px;color:#888;white-space:nowrap;}
.legend b{font-weight:700;border-radius:4px;padding:0 4px;margin:0 1px;}
button{font-family:inherit;}
.gostudy{background:var(--study);border:1px solid var(--study);color:#fff;padding:5px 12px;border-radius:6px;cursor:pointer;font-size:13px;white-space:nowrap;}
main{padding:10px 14px 60px;}
details{margin:8px 0;border:1px solid var(--bd);border-radius:8px;background:#fff;overflow:hidden;}
summary{list-style:none;cursor:pointer;padding:9px 12px;font-size:16px;font-weight:600;color:var(--head);background:#eef1f8;display:flex;align-items:center;gap:8px;min-height:38px;}
summary::-webkit-details-marker{display:none;}
summary .arw{transition:transform .15s;}
details[open] summary .arw{transform:rotate(90deg);}
summary .cnt{margin-left:auto;font-size:12px;font-weight:400;color:#888;}
summary .btitle{font-weight:600;color:var(--accent);margin-left:2px;}
.baitools{display:flex;gap:8px;align-items:center;padding:8px 10px 0;flex-wrap:wrap;}
.studybtn{background:var(--study);border:1px solid var(--study);color:#fff;padding:5px 12px;border-radius:6px;cursor:pointer;font-size:13px;}
.tabbtn{border:1px solid var(--bd);background:#eef1f8;color:#555;padding:5px 14px;border-radius:8px;cursor:pointer;font-size:13.5px;}
.tabbtn.on{background:#fff;color:var(--head);font-weight:600;box-shadow:0 -2px 0 var(--accent) inset;}
.panel{display:none;}
.panel.on{display:block;}
.tw{overflow-x:auto;}
table{border-collapse:collapse;width:max-content;min-width:100%;font-size:15px;}
thead th{background:var(--head);color:var(--headtx);text-align:left;padding:8px 12px;white-space:nowrap;position:sticky;top:0;}
td{border-top:1px solid var(--bd);padding:7px 12px;vertical-align:top;}
tbody tr:nth-child(even){background:var(--zebra);}
tbody tr:hover{background:#eef4ff;}
tbody tr.editing{background:#fffbe6;}
td.act{width:94px;text-align:center;padding:6px 4px;white-space:nowrap;}
.spk{border:none;background:none;cursor:pointer;color:#2b6cb0;font-size:14px;padding:2px 3px;}
.spk:hover{color:#16457a;}
.sspk{flex:none;background:#fff;border:1px solid var(--bd);border-radius:8px;padding:6px 9px;cursor:pointer;font-size:14px;}
.st{display:inline-block;min-width:22px;height:22px;line-height:22px;border-radius:50%;font-weight:700;font-size:13px;color:#fff;}
.st.none{background:#e6e6e6;color:#aaa;font-weight:400;}
.st.a{background:#1e874b;}.st.b{background:#37a86a;}.st.c{background:#d1a015;}.st.d{background:#e8804a;}
.rowedit{border:none;background:none;cursor:pointer;color:#aaa;font-size:14px;padding:2px 4px;margin-left:2px;}
.rowedit:hover{color:var(--accent);}
td.w{font-weight:600;font-size:16px;}
td:nth-child(2),td:nth-child(3),td:nth-child(4),td:nth-child(5){white-space:nowrap;}
td:nth-child(3){color:#2f855a;}
td:nth-child(5){color:#b7791f;}
td:nth-child(6){white-space:normal;min-width:340px;color:#333;}
td[contenteditable="true"]{outline:2px solid var(--accent);border-radius:3px;background:#fff;}
/* xếp 2-3 cây cạnh nhau trên một hàng, không dồn 1 mé trái */
.exp{padding:8px 12px 12px;display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:10px 14px;align-items:start;}
.grp{padding:10px 12px;border:1px solid #edf0f5;border-radius:10px;background:#fff;}
.grp .root{display:inline-block;font-size:19px;font-weight:700;color:var(--head);background:#eef1f8;border-radius:6px;padding:1px 10px;}
.grp .src{font-size:12px;color:#999;}
.chips{margin-top:6px;display:flex;flex-wrap:wrap;gap:6px 10px;}
.chip{background:#f5f7fb;border:1px solid #e4e8f0;border-radius:6px;padding:3px 9px;font-size:14px;}
.chip b{font-size:15px;}
.chip i{color:#2f855a;font-style:normal;}
/* 生词拓展 dạng sơ đồ cây: gốc bên trái → nhánh (汉字 · pinyin · nghĩa) */
.tree{display:flex;align-items:flex-start;gap:14px;}
.troot{flex:0 0 auto;min-width:54px;display:flex;flex-direction:column;align-items:center;
  background:linear-gradient(180deg,#eef1f8,#e3e9f6);border:1px solid #d3d9ea;border-radius:10px;padding:7px 11px;}
.troot .tr-han{font-size:26px;font-weight:800;color:var(--head);line-height:1.1;}
.troot .tr-py{font-size:12px;color:#2f855a;margin-top:2px;}
.troot .rgloss{font-size:11px;color:#7a8194;margin-top:3px;text-align:center;max-width:90px;}
/* nhánh dọc gọn trong mỗi cây (nhiều cây xếp cạnh nhau nhờ .exp grid) */
.branches{flex:1;display:flex;flex-direction:column;gap:5px;border-left:2px solid #d3d9ea;padding-left:14px;}
.branch{position:relative;line-height:1.4;}
.branch::before{content:"";position:absolute;left:-14px;top:0.75em;width:10px;height:2px;background:#d3d9ea;}
.branch .bh{font-size:16px;font-weight:700;color:#1a1a1a;}
.branch .bpy{color:#2f855a;font-size:13px;margin-left:3px;}
.branch .bg{color:#555;font-size:13px;margin-left:7px;}
tr.stale{background:#fffdf5;}
.stalebadge{display:inline-block;margin-left:6px;font-size:10px;color:#b7791f;background:#fff3cd;border:1px solid #f0d98c;border-radius:4px;padding:0 5px;white-space:nowrap;vertical-align:middle;cursor:help;}
.hidden{display:none;}
/* ---- study modal ---- */
#study{position:fixed;inset:0;background:rgba(18,18,28,.8);z-index:100;display:flex;align-items:center;justify-content:center;padding:16px;}
#study.hidden{display:none;}
.scard{background:#fff;border-radius:14px;width:min(680px,96vw);max-height:92vh;overflow:auto;box-shadow:0 20px 60px rgba(0,0,0,.45);}
.shead{display:flex;align-items:center;gap:8px;padding:10px 14px;border-bottom:1px solid var(--bd);font-size:13px;color:#555;position:sticky;top:0;background:#fff;z-index:3;}
#sbadge{flex:none;font-size:12px;}
.sg{flex:none;padding:6px 12px;height:34px;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;border:1px solid var(--bd);line-height:1;white-space:nowrap;}
.sg-again{background:#fdecec;color:#c0392b;border-color:#e6b8b8;}
.sg-again:hover{background:#f7d9d9;}
.sg-good{background:#e7f6ee;color:#1e874b;border-color:#b7e0c8;}
.sg-good:hover{background:#d2efe0;}
.sclose{flex:none;background:#fff;border:1px solid var(--bd);border-radius:8px;padding:6px 10px;cursor:pointer;font-size:13px;}
.shead .prog{flex:1;height:8px;background:#eee;border-radius:6px;overflow:hidden;}
.shead .prog>i{display:block;height:100%;background:var(--study);width:0;transition:width .2s;}
.shead button{padding:4px 10px;font-size:12px;border-radius:6px;border:1px solid var(--bd);background:#fff;cursor:pointer;}
.dirbtn{color:var(--study);border-color:var(--study)!important;}
.sbody{padding:30px 20px;text-align:center;min-height:230px;display:flex;flex-direction:column;justify-content:center;gap:12px;cursor:pointer;}
.sfront{font-size:46px;font-weight:700;}
.sfront.vi{font-size:26px;color:#b7791f;font-weight:600;}
.shint{font-size:12px;color:#aaa;}
.sback{border-top:1px dashed #ddd;padding-top:14px;display:none;}
.sback.on{display:block;}
.sback .py{color:#2f855a;font-size:21px;margin-bottom:4px;}
.sback .zh{font-size:32px;font-weight:700;margin:2px 0;}
.sback .rj{font-size:16px;margin:4px 0;}
.sback .vi{color:#b7791f;font-size:15px;}
.sback .ex{color:#555;font-size:15px;margin-top:10px;}
.sback .sact{margin-top:12px;font-size:13px;color:#555;background:#f4f4f8;border-radius:6px;padding:7px 10px;}
.sback .sacthint{color:#b7791f;}
.sback .ct{margin-top:12px;text-align:left;}
details.ctd{border:1px solid #ece9f7;border-radius:8px;background:#fbfbfe;}
details.ctd>summary{padding:8px 11px;font-size:13px;color:var(--study);font-weight:600;cursor:pointer;list-style:none;}
details.ctd>summary::-webkit-details-marker{display:none;}
.hz{padding:9px 12px;border-top:1px dashed #eee;font-size:14px;line-height:1.5;}
.hz:first-of-type{border-top:none;}
.hzc{font-size:23px;font-weight:700;color:#1a1a1a;}
.hzr{font-size:12px;color:#888;margin-left:8px;}
.hzd{font-size:16px;color:#666;margin-left:8px;letter-spacing:1px;}
.hzcp{margin-top:5px;color:#333;}
.hzcp b{color:var(--head);font-size:17px;}
.hze{margin-top:5px;color:#2f855a;font-size:13px;}
.hzlink{display:inline-block;margin-top:6px;font-size:12px;color:var(--accent);text-decoration:none;}
.hzlink:hover{text-decoration:underline;}
.hzp{font-size:14px;color:#2f855a;margin-left:6px;}
.hzp .hv{color:#b7791f;font-weight:600;}
.hzcp{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 6px;}
.cpc b{color:var(--head);font-size:17px;}
.cpr{color:#2f855a;font-size:13px;}
.cpr .hv{color:#b7791f;font-weight:600;}
.cpc em{color:#999;font-size:12px;font-style:normal;}
.plus{color:#bbb;margin:0 2px;}
.sback .ln{display:flex;gap:8px;align-items:baseline;margin:7px auto;max-width:520px;text-align:left;font-size:15px;}
.sback .ln .lb{flex:none;width:48px;font-size:10.5px;color:#aaa;font-weight:700;text-transform:uppercase;letter-spacing:.4px;padding-top:3px;}
.sback .ln .vi{color:#b7791f;}
.hzhead{display:flex;align-items:baseline;flex-wrap:wrap;gap:3px 8px;}
.role{font-size:10px;padding:0 5px;border-radius:8px;margin-left:2px;vertical-align:middle;}
.role.rn{background:#d5f5e3;color:#1e874b;}
.role.ra{background:#fdeecd;color:#b7791f;}
.hzmn{margin-top:6px;background:#f3f0fb;border-left:3px solid var(--study);padding:6px 10px;border-radius:0 6px 6px 0;font-size:13.5px;color:#333;line-height:1.55;}
.hzmn b{color:var(--head);}
.hzmn-main{margin:2px 0 12px;font-size:15px;background:#eef7f0;border-left:4px solid #1e874b;padding:10px 12px;color:#1a1a1a;}
.hzmn-main b{color:#1e874b;}
.sbtns{display:flex;gap:10px;padding:14px 16px;border-top:1px solid var(--bd);}
.sbtns button{flex:1;padding:12px;font-size:15px;border-radius:8px;cursor:pointer;border:1px solid var(--bd);}
.b-again{background:#fff;color:#c0392b;border-color:#e0b4b4;}
.b-good{background:#1e874b;border-color:#1e874b;color:#fff;}
.b-flip{background:var(--study);border-color:var(--study);color:#fff;}
.sdone{text-align:center;padding:40px 20px;font-size:18px;color:var(--head);line-height:1.7;}
"""

JS = r"""
/* ===== nhớ sửa nội dung ===== */
var KEY='hsk6vocab_edits_v1';
function load(){try{return JSON.parse(localStorage.getItem(KEY))||{};}catch(e){return {};}}
function store(o){localStorage.setItem(KEY,JSON.stringify(o));}
var DB=load();
function rec(w){if(!DB[w])DB[w]={};return DB[w];}
function initRow(tr){var w=tr.getAttribute('data-w');var r=DB[w];if(!r)return;
  var c=tr.querySelectorAll('td.data');for(var i=0;i<c.length;i++){if(r[i]!=null)c[i].textContent=r[i];}
  if(r._stale){tr.classList.add('stale');staleBadge(tr);}}
function staleBadge(tr){if(tr.querySelector('.stalebadge'))return;
  var b=document.createElement('span');b.className='stalebadge';
  b.title='Bạn đã sửa 生词 — Pinyin/释义/Nghĩa/例句 có thể chưa khớp. Chạy lại pipeline hoặc nhờ cập nhật.';
  b.textContent='⚠ cần làm mới';var first=tr.querySelector('td.w');if(first)first.appendChild(b);}
function er(btn){var tr=btn.closest('tr');var on=!tr.classList.contains('editing');
  tr.classList.toggle('editing',on);var c=tr.querySelectorAll('td.data');var w=tr.getAttribute('data-w');
  for(var i=0;i<c.length;i++){var td=c[i];td.contentEditable=on?'true':'false';
    /* sửa ô nào lưu ô đó; riêng ô 生词 (idx 0) đổi → đánh dấu dòng cần làm mới cột sau */
    if(on){td.oninput=(function(idx,cell,row){return function(){var r=rec(w);r[idx]=cell.textContent;
      if(idx===0){r._stale=1;row.classList.add('stale');staleBadge(row);}store(DB);};})(i,td,tr);}}
  btn.textContent=on?'✅':'✏️';if(on)c[0].focus();}
function tab(btn,which){var d=btn.closest('details');
  d.querySelectorAll('.tabbtn').forEach(function(b){b.classList.remove('on');});btn.classList.add('on');
  d.querySelectorAll('.panel').forEach(function(p){p.classList.remove('on');});
  d.querySelector('.panel.p'+which).classList.add('on');}
function filt(){var k=document.getElementById('q').value.trim().toLowerCase();
  document.querySelectorAll('#root details').forEach(function(d){var any=false;
    d.querySelectorAll('tbody tr').forEach(function(tr){var hit=!k||tr.innerText.toLowerCase().indexOf(k)>-1;
      tr.classList.toggle('hidden',!hit);if(hit)any=true;});
    d.querySelectorAll('.grp').forEach(function(g){var hit=!k||g.innerText.toLowerCase().indexOf(k)>-1;
      g.classList.toggle('hidden',!hit);if(hit)any=true;});
    d.open=k?any:false;});}
function esc(s){var d=document.createElement('div');d.textContent=(s==null?'':s);return d.innerHTML;}
/* ===== 🔊 phát âm (Web Speech API) ===== */
var _zhVoices=[],_zhVoice=null,VKEY='hsk6vocab_voice';
function scoreVoice(v){var s=(v.name+' '+v.lang).toLowerCase(),sc=0;
  if(/zh[-_]?cn|zh_cn|普通话|mandarin|chinese \(china|zh-hans/.test(s))sc+=3;
  else if(/^zh|中文|chinese/.test(s))sc+=1;
  /* giọng neural/online chất lượng cao (Edge có sẵn khi online) */
  if(/natural|neural|online|神经|xiaoxiao|yunxi|yunyang|yunjian|xiaoyi|晓晓|云希|云扬/.test(s))sc+=5;
  if(/huihui|kangkang|yaoyao/.test(s))sc-=1; /* giọng local cũ, máy móc */
  return sc;}
function pickVoice(){
  try{var vs=window.speechSynthesis.getVoices();
    _zhVoices=vs.filter(function(v){return /^zh|zh[-_]|Chinese|中文|普通话|Mandarin/i.test(v.lang+' '+v.name);})
                .sort(function(a,b){return scoreVoice(b)-scoreVoice(a);});
    var saved=localStorage.getItem(VKEY);
    _zhVoice=_zhVoices.filter(function(v){return v.name===saved;})[0]||_zhVoices[0]||null;
    buildVoiceSel();
  }catch(e){}
}
function buildVoiceSel(){var bar=document.querySelector('.bar');if(!bar||!_zhVoices.length)return;
  var sel=document.getElementById('voicesel');
  if(!sel){sel=document.createElement('select');sel.id='voicesel';sel.title='Chọn giọng đọc 🔊 (ưu tiên giọng Natural/Online)';
    sel.onchange=function(){_zhVoice=_zhVoices[this.value];localStorage.setItem(VKEY,_zhVoice.name);speak('你好，这是试听');};
    bar.appendChild(sel);}
  sel.innerHTML='';
  _zhVoices.forEach(function(v,i){var o=document.createElement('option');o.value=i;
    o.textContent='🔊 '+v.name.replace('Microsoft ','').replace(' - Chinese (Mainland)','');
    if(v===_zhVoice)o.selected=true;sel.appendChild(o);});
}
if(window.speechSynthesis){pickVoice();window.speechSynthesis.onvoiceschanged=pickVoice;}
function speak(t){
  if(!t||!window.speechSynthesis)return;
  try{
    window.speechSynthesis.cancel();
    var u=new SpeechSynthesisUtterance(t);
    u.lang='zh-CN';u.rate=0.85;
    if(!_zhVoice)pickVoice();
    if(_zhVoice)u.voice=_zhVoice;
    window.speechSynthesis.speak(u);
  }catch(e){}
}
function spkRow(btn){speak(btn.closest('tr').getAttribute('data-w'));}
document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('#root tbody tr').forEach(initRow);});

/* ===== 🎓 Học từ vựng: flashcard active-recall + Leitner ===== */
var SKEY='hsk6srs_v1';
function sload(){try{return JSON.parse(localStorage.getItem(SKEY))||{};}catch(e){return {};}}
var SRS=sload();
function ssave(){localStorage.setItem(SKEY,JSON.stringify(SRS));}
var ACTLVL={none:0,d:1,c:2,b:3,a:4};
var ACTNAME={none:'⚪ kho (chưa học)',d:'D · mới học',c:'C · nhận ra',b:'B · dùng được',a:'A · tự tin dùng'};
function sbox(w){return (SRS[w]&&SRS[w].box)||0;}
var Sq=[],Sdir='zh2vi',Scur=null,Sflip=false,Sdone=0,Stotal=0,Sagain=0,Scapped=0,Slabel='';
function cardsFrom(rows){
  var out=[];
  rows.forEach(function(tr){
    if(tr.classList.contains('hidden'))return;
    var td=tr.querySelectorAll('td');
    if(td.length<6)return;
    var act='none',st=tr.querySelector('.st');
    if(st){['a','b','c','d'].forEach(function(x){if(st.classList.contains(x))act=x;});}
    var w=td[1].textContent.trim();
    if(!w)return;
    out.push({w:w,py:td[2].textContent.trim(),rj:td[3].textContent.trim(),
              vi:td[4].textContent.trim(),ex:td[5].textContent.trim(),act:act,lvl:ACTLVL[act],
              pys:(tr.getAttribute('data-py')||'').split(' ').filter(Boolean)});
  });
  return out;
}
function beginStudy(cards,label){
  if(!cards.length){alert('Không có từ để học.');return;}
  cards.forEach(function(c){if(!SRS[c.w])SRS[c.w]={box:c.lvl};}); // mốc khởi đầu khách quan theo Activation
  ssave();
  cards.sort(function(a,b){return sbox(a.w)-sbox(b.w);});
  Sq=cards.slice();Stotal=cards.length;Sdone=0;Sagain=0;Scapped=0;Slabel=label;
  document.getElementById('study').classList.remove('hidden');
  resetBody();sNext();
}
function startStudy(btn){var det=btn.closest('details');
  var label='Bài '+det.getAttribute('data-bai');
  var _bt=det.getAttribute('data-baititle');if(_bt)label+=' — '+_bt;
  beginStudy(cardsFrom(det.querySelectorAll('.panel.p1 tbody tr')),label);}
function startStudyAll(){
  var rows=[];document.querySelectorAll('#root .panel.p1 tbody tr').forEach(function(tr){rows.push(tr);});
  var q=document.getElementById('q').value.trim();
  beginStudy(cardsFrom(rows), q?('Lọc: '+q):'Tất cả bài');}
function resetBody(){document.getElementById('sbody').innerHTML=
  '<div class="sfront" id="sfront"></div><div class="shint" id="shint">Bấm để lật thẻ</div><div class="sback" id="sback"></div>';}
function sNext(){Sflip=false;
  if(!Sq.length){return sFinish();}
  Scur=Sq[0];
  var f=document.getElementById('sfront');
  if(Sdir==='zh2vi'){f.className='sfront';f.textContent=Scur.w;}
  else{f.className='sfront vi';f.textContent=(Scur.vi||Scur.rj);}
  var bd=document.getElementById('sbadge');
  bd.className='st '+(Scur.act||'none');
  bd.textContent=(Scur.act==='none'?'○':Scur.act.toUpperCase());
  bd.title=ACTNAME[Scur.act]+' · hộp '+sbox(Scur.w)+'/5';
  document.getElementById('sback').className='sback';
  document.getElementById('shint').style.display='';
  sProg();}
function sFlip(){if(Sflip)return;Sflip=true;
  var b=document.getElementById('sback');
  var h='<div class="py">'+esc(Scur.py)+'</div>';
  if(Sdir==='vi2zh')h+='<div class="zh">'+esc(Scur.w)+'</div>';
  h+='<div class="ln"><span class="lb">释义</span><span>'+esc(Scur.rj)+'</span></div>';
  h+='<div class="ln"><span class="lb">Nghĩa</span><span class="vi">'+esc(Scur.vi)+'</span></div>';
  if(Scur.ex)h+='<div class="ln"><span class="lb">Ví dụ</span><span>'+esc(Scur.ex)+'</span></div>';
  h+=chietTu(Scur.w,Scur.pys);
  b.innerHTML=h;b.className='sback on';
  document.getElementById('shint').style.display='none';
  speak(Scur.w);}
function sGrade(good){var w=Scur.w;if(!SRS[w])SRS[w]={box:Scur.lvl};
  var cap=Math.max(1,Scur.lvl+1); // trần theo Activation của vault
  if(good){
    if(sbox(w)>=cap){Scapped++;}            // kịch trần: chưa dùng thật thì không "thuộc hẳn"
    SRS[w].box=Math.min(sbox(w)+1,cap);
    Sq.shift();Sdone++;
  }else{SRS[w].box=1;Sagain++;Sq.push(Sq.shift());}
  ssave();sNext();}
function reading(p,hv){return esc(p||'')+(hv?' · <span class="hv">'+esc(hv)+'</span>':'');}
var IDS={'⿰':'trái–phải','⿱':'trên–dưới','⿲':'trái–giữa–phải','⿳':'trên–giữa–dưới','⿴':'bao kín','⿵':'bao trên','⿶':'bao dưới','⿷':'bao trái','⿸':'góc trên-trái','⿹':'góc trên-phải','⿺':'góc dưới-trái','⿻':'lồng nhau'};
function structLabel(dc){return (dc&&IDS[dc[0]])?IDS[dc[0]]:'';}
function meaningOf(ch){var o=HZ[ch];if(!o)return '';return o.hv?o.hv:(o.d?o.d.split(/[,;]/)[0].trim():'');}
function readOf(ch){var o=HZ[ch];return o?(o.hv||o.p||ch):ch;}
function mnemonic(o){
  if(o.et==='pictophonetic'&&o.sem&&o.phon)
    return 'Hình thanh: bộ <b>'+esc(o.sem)+'</b> ('+esc(meaningOf(o.sem))+') chỉ NGHĨA · <b>'+esc(o.phon)+'</b> ('+esc(readOf(o.phon))+') gợi ÂM.';
  if(o.et==='ideographic'){
    var parts=o.c?o.c.map(function(x){return '<b>'+esc(x[0])+'</b>('+esc(x[3]||x[2]||'')+')';}).join(' + '):'';
    return 'Hội ý: ghép '+parts+(o.e?' — “'+esc(o.e)+'”':'')+'.';
  }
  if(o.et==='pictographic')return 'Tượng hình'+(o.e?': '+esc(o.e):'')+'.';
  return o.e?esc(o.e):'';
}
function chietTu(word,pys){
  var hasMN=(typeof MN!=='undefined' && MN[word]);
  var out='',found=false,hi=0;
  for(var i=0;i<word.length;i++){
    var ch=word[i]; if(!/[一-鿿]/.test(ch))continue;
    var o=(typeof HZ!=='undefined')?HZ[ch]:null;
    var rd=(pys&&pys[hi])?pys[hi]:(o?o.p:''); hi++;
    if(!o){out+='<div class="hz"><div class="hzhead"><span class="hzc">'+esc(ch)+'</span> <span class="hzp">'+esc(rd)+'</span></div></div>';found=true;continue;}
    found=true;
    var comp=o.c?o.c.map(function(x){
      var role=(o.sem===x[0]?'<span class="role rn">nghĩa</span>':(o.phon===x[0]?'<span class="role ra">âm</span>':''));
      return '<span class="cpc"><b>'+esc(x[0])+'</b> <span class="cpr">'+reading(x[2],x[3])+'</span>'+role+(x[1]?' <em>'+esc(x[1])+'</em>':'')+'</span>';
    }).join('<span class="plus">+</span>'):'';
    var st=structLabel(o.dc), mn=hasMN?'':mnemonic(o);
    out+='<div class="hz">'+
      '<div class="hzhead"><span class="hzc">'+esc(ch)+'</span> <span class="hzp">'+reading(rd,o.hv)+'</span>'+
        (o.r?'<span class="hzr">bộ '+esc(o.r)+(st?' · '+st:'')+'</span>':'')+'</div>'+
      (comp?'<div class="hzcp">'+comp+'</div>':'')+
      (mn?'<div class="hzmn">💡 '+mn+'</div>':'')+
      '<a class="hzlink" href="https://hanzicraft.com/character/'+encodeURIComponent(ch)+'" target="_blank" rel="noopener">🔍 tra sâu (thứ tự nét, ảnh)</a>'+
      '</div>';
  }
  if(!found)return '';
  var top=hasMN?'<div class="hzmn hzmn-main">💡 <b>Mẹo nhớ:</b> '+esc(MN[word])+'</div>':'';
  return '<div class="ct"><details class="ctd" open><summary>🧩 Chiết tự / mẹo nhớ</summary>'+top+out+'</details></div>';
}
function sProg(){document.getElementById('sc').textContent=Slabel+' · '+Sdone+'/'+Stotal;
  document.getElementById('sp').style.width=(Stotal?Math.round(Sdone/Stotal*100):0)+'%';}
function sFinish(){
  var extra=Scapped?('<br><small style="color:#c0392b">'+Scapped+' từ kịch trần theo vault — cần dùng thật (nói/viết) để Activation lên hạng.</small>'):'';
  document.getElementById('sbody').innerHTML=
  '<div class="sdone">🎉 Xong '+esc(Slabel)+'!<br>'+Stotal+' từ · '+Sagain+' lần chưa thuộc'+extra+'<br>'+
  '<small style="color:#888">Tiến độ đã lưu (hộp Leitner, mốc theo Activation).</small>'+
  '<br><button class="b-good" style="margin-top:16px;padding:10px 20px;border-radius:8px;border:none;cursor:pointer" onclick="closeStudy()">Đóng</button></div>';
  document.getElementById('sp').style.width='100%';}
function toggleDir(){Sdir=(Sdir==='zh2vi')?'vi2zh':'zh2vi';
  document.getElementById('sdir').textContent=(Sdir==='zh2vi')?'汉 → Việt':'Việt → 汉';
  if(!document.getElementById('study').classList.contains('hidden')&&Sq.length)sNext();}
function closeStudy(){document.getElementById('study').classList.add('hidden');resetBody();}
document.addEventListener('keydown',function(e){
  if(document.getElementById('study').classList.contains('hidden'))return;
  if(!Sq.length)return;
  if(e.key===' '){e.preventDefault();if(!Sflip)sFlip();}
  else if(e.key==='1')sGrade(0);
  else if(e.key==='2')sGrade(1);
  else if(e.key==='s'||e.key==='S')speak(Scur&&Scur.w);
  else if(e.key==='Escape')closeStudy();});
"""

P = ['<!doctype html>', '<html lang="vi"><head><meta charset="utf-8">',
     '<meta name="viewport" content="width=device-width, initial-scale=1">',
     '<title>生词 tích lũy — HSK6</title>', '<style>' + CSS + '</style></head><body>',
     '<div class="bar"><h1>生词 HSK6</h1>',
     '<input id="q" placeholder="Tìm từ / pinyin / nghĩa…" oninput="filt()">',
     '<button class="gostudy" onclick="startStudyAll()">🎓 Học</button>',
     '<span class="legend">Ôn: <b class="st none" style="color:#aaa">○</b>kho '
     '<b style="background:#e8804a;color:#fff">D</b><b style="background:#d1a015;color:#fff">C</b>'
     '<b style="background:#37a86a;color:#fff">B</b><b style="background:#1e874b;color:#fff">A</b></span>',
     '<span class="tip" title="🎓 Học = thẻ lật tự nhớ (active recall) + lặp ngắt quãng Leitner, tiến độ lưu trong trình duyệt. Trạng thái ôn ⚪/D/C/B/A suy từ knowledge/vocabulary. Mỗi bài có nút Học riêng; nút 🎓 Học trên đây học theo từ đang lọc/tất cả.">ⓘ</span>',
     '</div>', '<main id="root">']

for num, header, rows, exp, btitle in bai:
    cnt = ('%d từ · %d nhóm 拓展' % (len(rows), len(exp))) if exp else ('%d từ' % len(rows))
    tlabel = ('<span class="btitle"> — %s</span>' % esc(btitle)) if btitle else ''
    P.append('<details data-bai="%d" data-baititle="%s"><summary><span class="arw">▸</span>Bài %d%s<span class="cnt">%s</span></summary>' % (num, esc(btitle), num, tlabel, cnt))
    P.append('<div class="baitools"><button class="studybtn" onclick="startStudy(this)">🎓 Học bài này</button>')
    if exp:
        P.append('<button class="tabbtn on" onclick="tab(this,1)">Từ vựng (%d)</button>'
                 '<button class="tabbtn" onclick="tab(this,2)">生词拓展 (%d)</button>' % (len(rows), len(exp)))
    P.append('</div>')
    P.append('<div class="panel p1 on"><div class="tw"><table><thead><tr><th></th>'
             + "".join('<th>%s</th>' % esc(h) for h in header) + '</tr></thead><tbody>')
    for r in rows:
        w = r[0]
        cells = '<td class="w data">%s</td>' % esc(w) + "".join('<td class="data">%s</td>' % esc(c) for c in r[1:])
        act = ('<td class="act">%s<button class="spk" title="Nghe" onclick="spkRow(this)">🔊</button>'
               '<button class="rowedit" title="Sửa dòng này" onclick="er(this)">✏️</button></td>') % status_cell(w)
        P.append('<tr data-w="%s" data-py="%s">%s%s</tr>' % (esc(w), esc(per_char_py(w)), act, cells))
    P.append('</tbody></table></div></div>')
    if exp:
        P.append('<div class="panel p2"><div class="exp">')
        for line in exp:
            P.append(render_exp(line))
        P.append('</div></div>')
    P.append('</details>')

P.append('</main>')
# study modal
P.append('<div id="study" class="hidden" onclick="if(event.target.id===\'study\')closeStudy()">'
         '<div class="scard">'
         '<div class="shead">'
         '<span id="sbadge" class="st none" title="Trạng thái ôn (Activation)">○</span>'
         '<span id="sc"></span><div class="prog"><i id="sp"></i></div>'
         '<button class="sspk" onclick="speak(Scur&&Scur.w)" title="Nghe (phím S)">🔊</button>'
         '<button class="sg sg-again" onclick="sGrade(0)" title="Chưa thuộc (phím 1)">❌ Chưa</button>'
         '<button class="sg sg-good" onclick="sGrade(1)" title="Thuộc (phím 2)">✅ Thuộc</button>'
         '<button class="sclose" onclick="closeStudy()" title="Đóng (Esc)">✕</button></div>'
         '<div class="sbody" id="sbody" onclick="sFlip()">'
         '<div class="sfront" id="sfront"></div><div class="shint" id="shint">Bấm / Space để lật thẻ</div>'
         '<div class="sback" id="sback"></div></div>'
         '</div></div>')
P.append('<script>var HZ=' + HZ_JSON + ';var MN=' + MN_JSON + ';</script>')
P.append('<script>' + JS + '</script>')
P.append('</body></html>')

open(OUT, "w", encoding="utf-8").write("\n".join(P))
print("wrote", OUT, "| bai:", len(bai))
