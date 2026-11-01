"""Dựng bản Artifact (claude.ai) từ trang chủ đề trong máy — để mở được trên điện thoại / máy khác.

    python build_artifact.py "<TS>/01/01_contagious-happiness.html" "<TS>/02/02_homeschool.html" … "<out>.html"

Truyền MỌI trang tập theo thứ tự (tập cuối = khuôn + mở mặc định). Ô chọn tập ở thanh trên; link `…#ep01` mở thẳng tập đó.

Trang trong máy vẫn là bản gốc (sửa ở đó, commit git). Bản Artifact:
  - bỏ khung <html>/<head>/<body> (claude.ai tự bọc), tên tab cố định "Talk Series";
  - bỏ nút 📱 Điện thoại + 💾 Lưu + mã gọi sync_server.py;
  - tick / chat lưu online qua capability `db` (doc `progress/ep<NN>`), mở máy nào cũng thấy;
  - từ không có nghĩa soạn sẵn (gloss) → hỏi Claude qua capability `sample` (MyMemory bị CSP chặn).
Publish với capabilities {"db": {}, "sample": {}}.
"""
import re
import sys

srcs, dst = sys.argv[1:-1], sys.argv[-1]
assert srcs, 'cần ít nhất 1 trang'
DATA_RE = r'<script id="data" type="application/json">(.*?)</script>'
# khuôn = trang cuối (tập mới nhất); dữ liệu của mọi tập nhúng kèm để chọn tập
s = open(srcs[-1], encoding='utf-8').read().replace('\r\n', '\n')
eps = [re.search(DATA_RE, open(p, encoding='utf-8').read(), re.S).group(1).strip() for p in srcs]


def cut(pattern, repl='', count=1, flags=re.S):
    global s
    s, n = re.subn(pattern, repl, s, count=count, flags=flags)
    assert n == count, pattern


# khung tài liệu
cut(r'<!doctype html>\s*<html[^>]*>\s*<head>\s*', flags=re.S | re.I)
cut(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*')
cut(r'<title>.*?</title>', '<title>Talk Series</title>')
cut(r'</head>\s*<body>\s*')
cut(r'</body>\s*</html>\s*$')
# thanh trên dính mép an toàn của điện thoại
cut(r'header\{position:sticky;top:0;', 'header{position:sticky;top:env(safe-area-inset-top, 0px);')
# nút + mã chỉ dùng với sync_server.py
cut(r'\s*<button class="btn" id="btnPhone".*?</button>\s*<button class="btn" id="btnSave".*?</button>',
    '\n  <span class="syncst" id="syncSt"></span>')
cut(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/qrcode-generator/[^"]*"></script>\n')
cut(r'/\* ---------- Lưu: ghi vào file.*?(?=markSave\(\);\nrender\(\);)')

# chọn tập: nhúng dữ liệu mọi tập, chép tập đang chọn (#ep02 trên link / lần chọn trước) vào #data trước khi trang chạy
PICK = ''.join(f'\n<script type="application/json" class="ep-data">\n{e}\n</script>' for e in eps) + r'''
<script>
(function(){
  const all = [...document.querySelectorAll('script.ep-data')].map(x => x.textContent);
  const ids = all.map(t => JSON.parse(t).ep);
  let want = (location.hash.match(/^#ep(\d+)/) || [])[1] || '';
  if (!ids.includes(want)) { try { want = localStorage.getItem('talkseries:curEp') || ''; } catch(e) {} }
  const i = ids.includes(want) ? ids.indexOf(want) : all.length - 1;
  document.getElementById('data').textContent = all[i];
  window.TS_EPS = all.map(t => { const d = JSON.parse(t); return {ep: d.ep, t: d.title_zh}; });
})();
</script>'''
m = re.search(DATA_RE, s, re.S)
s = s[:m.end()] + PICK + s[m.end():]
cut(r'<div class="ttl zh" id="ttl"></div>', '<select class="epsel zh" id="epSel"></select><div class="ttl zh" id="ttl"></div>')

ADAPTER = r'''
<style>.syncst{font-size:12.5px;color:var(--mute);white-space:nowrap}
.epsel{font:inherit;font-weight:700;font-size:16px;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:8px;padding:3px 6px;max-width:60vw}
.epsel + .ttl{display:none}</style>
<script>
/* Ô chọn tập: đổi tập = ghi nhớ lựa chọn rồi tải lại trang. */
(function(){
  const sel = document.getElementById('epSel');
  if(!sel || !window.TS_EPS) return;
  sel.innerHTML = TS_EPS.map(e => `<option value="${esc(e.ep)}"${e.ep === D.ep ? ' selected' : ''}>Tập ${esc(e.ep)} · ${esc(e.t)}</option>`).join('');
  sel.onchange = () => {
    try { localStorage.setItem('talkseries:curEp', sel.value); } catch(e) {}
    location.hash = 'ep' + sel.value;
    location.reload();
  };
})();
</script>
<script>
/* Bản Artifact: lưu tick/chat online (db) + tra nghĩa từ ngoài danh sách bằng Claude (sample). */
(async function(){
  if(!window.claude) return;
  const st = document.getElementById('syncSt');
  const show = t => { if(st) st.textContent = t; };
  let db = null; try { db = await claude.use('db'); } catch(e) {}
  if(db){
    const ref = db.doc('progress/ep' + D.ep);
    try {
      const snap = await ref.get();
      const remote = snap.exists ? snap.data().state : null;
      if(remote && (remote.ts || '') > (S.ts || '')){
        Object.assign(S, remote);
        try { localStorage.setItem(KEY, JSON.stringify(S)); } catch(e) {}
        render();
      }
      show('☁️ Đã đồng bộ');
    } catch(e) { show('⚠️ Chưa tải được tiến độ'); }
    let timer = null;
    window.TS_onSave = () => {
      show('⏳ Đang lưu…');
      clearTimeout(timer);
      timer = setTimeout(async () => {
        try { await ref.set({state: JSON.parse(JSON.stringify(S))}); show('☁️ Đã lưu'); }
        catch(e) { show('⚠️ Chưa lưu được — thao tác lại sau'); }
      }, 1200);
    };
  } else show('Chỉ lưu trên máy này');
  let sample = null; try { sample = await claude.use('sample'); } catch(e) {}
  if(sample) window.TS_MEANING = async text => {
    const sel = getSelection();
    const el = sel && sel.anchorNode && (sel.anchorNode.nodeType === 3 ? sel.anchorNode.parentElement : sel.anchorNode);
    const ctx = el ? (el.closest('p,.txt,.q,.msg') || el).innerText.slice(0, 300) : '';
    const r = await sample('Giải nghĩa ngắn gọn bằng tiếng Việt (tối đa 15 từ, không pinyin, không giải thích thêm) cụm tiếng Trung "' + text + '" theo đúng nghĩa trong câu sau:\n' + ctx, {modelTier: 'quick'});
    return r.text.trim();
  };
})();
</script>
'''
s = s.rstrip() + '\n' + ADAPTER
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, len(s))
