"""Chạy thử trang chủ đề bằng Chrome/Edge ngầm (headless) — BẮT BUỘC trước khi báo "đã sửa".

    python check_page.py "<TS>/NN/NN_<tên>.html" [--select 过瘾]

In ra: số dòng Mở đầu + Kết thúc, số chip từ H6 ở cột Mục tiêu, lỗi JS (phải rỗng).
--select <cụm>: giả lập bôi đen cụm đó → in nội dung popup pinyin + nghĩa.
Không sửa trang; file thử nằm trong thư mục tạm.
"""
import argparse, os, re, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ap = argparse.ArgumentParser()
ap.add_argument('page')
ap.add_argument('--select', default='')
a = ap.parse_args()

BROWSERS = [r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe']
exe = next((b for b in BROWSERS if os.path.exists(b)), None)
if not exe:
    sys.exit('Không thấy Chrome/Edge.')

s = Path(a.page).read_text(encoding='utf-8')
head = '<script>window.__e=[];addEventListener("error",e=>__e.push(e.message+"@"+e.lineno));</script>'
sel = a.select.replace('\\', '\\\\').replace('"', '\\"')
probe = r'''<script>
setTimeout(function(){
  var out=[];
  var lines=document.querySelectorAll('.v.intro .txt').length;
  out.push('dong_mo_dau_ket_thuc='+lines, 'chip_H6='+document.querySelectorAll('#goal .chip').length);
  var W="%s";
  if(W){
    var tn=document.createTreeWalker(document.getElementById('main'),NodeFilter.SHOW_TEXT), n;
    while((n=tn.nextNode())){ if(n.data.indexOf(W)>=0) break; }
    if(!n){ out.push('select=KHÔNG THẤY "'+W+'" trong 1 đoạn chữ liền'); }
    else {
      var i=n.data.indexOf(W), r=document.createRange(); r.setStart(n,i); r.setEnd(n,i+W.length);
      var sl=getSelection(); sl.removeAllRanges(); sl.addRange(r);
      document.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));
    }
  }
  setTimeout(function(){
    if(W) out.push('popup='+document.getElementById('lp-body').innerText.replace(/\n/g,' | '));
    out.push('loi_JS='+(__e.join(' || ')||'không'));
    document.body.setAttribute('data-res', out.join('\n'));
  },2500);
},1000);
</script></body>''' % sel
t = s.replace('<head>', '<head>' + head, 1).replace('</body>', probe, 1)
with tempfile.TemporaryDirectory() as d:
    f = Path(d) / 'check.html'
    f.write_text(t, encoding='utf-8')
    r = subprocess.run([exe, '--headless=new', '--disable-gpu', f'--user-data-dir={d}/prof',
                        '--virtual-time-budget=8000', '--dump-dom', f.as_uri()],
                       capture_output=True, timeout=90)
dom = r.stdout.decode('utf-8', 'replace')
m = re.search(r'data-res="([^"]*)"', dom)
print(m.group(1).replace('&quot;', '"').replace('&amp;', '&') if m else 'Không lấy được kết quả (trang không chạy tới cuối?)')
