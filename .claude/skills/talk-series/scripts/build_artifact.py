"""Dựng bản Artifact (claude.ai) từ trang chủ đề trong máy — để mở được trên điện thoại / máy khác.

    python build_artifact.py "<TS>/01/01_contagious-happiness.html" "<out>.html"

Trang trong máy vẫn là bản gốc (sửa ở đó, commit git). Bản Artifact:
  - bỏ khung <html>/<head>/<body> (claude.ai tự bọc), tên tab cố định "Talk Series";
  - bỏ nút 📱 Điện thoại + 💾 Lưu + mã gọi sync_server.py;
  - tick / chat lưu online qua capability `db` (doc `progress/ep<NN>`), mở máy nào cũng thấy;
  - từ không có nghĩa soạn sẵn (gloss) → hỏi Claude qua capability `sample` (MyMemory bị CSP chặn).
Publish với capabilities {"db": {}, "sample": {}}.
"""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read().replace('\r\n', '\n')


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

ADAPTER = r'''
<style>.syncst{font-size:12.5px;color:var(--mute);white-space:nowrap}</style>
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
