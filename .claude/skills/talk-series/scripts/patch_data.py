"""Sửa khối dữ liệu trang chủ đề: python patch_data.py <page.html> <changes.json>
changes.json: {"blocks": {"<id>": {"story": "..."}}, "replace": [["old", "new"]], "gloss": {"từ": ["pinyin", "nghĩa"]}}
"replace" chạy trên text JSON của khối dữ liệu (mỗi chuỗi phải xuất hiện đúng 1 lần)."""
import sys, json, re
p, ch = sys.argv[1], json.load(open(sys.argv[2], encoding='utf-8'))
s = open(p, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s else '\n'
s = s.replace('\r\n', '\n')
m = re.search(r'(<script id="data" type="application/json">)(.*?)(</script>)', s, re.S)
d = json.loads(m.group(2))
for bid, fields in ch.get('blocks', {}).items():
    b = next(x for x in d['blocks'] + d['solo_blocks'] if x['id'] == bid)
    b.update(fields)
for k, (py, vi) in ch.get('gloss', {}).items():
    d['gloss'][k] = {"py": py, "vi": vi}
js = json.dumps(d, ensure_ascii=False, indent=2)
for old, new in ch.get('replace', []):
    o, n = json.dumps(old, ensure_ascii=False)[1:-1], json.dumps(new, ensure_ascii=False)[1:-1]
    assert js.count(o) == 1, (old, js.count(o))
    js = js.replace(o, n)
json.loads(js)
words = set(re.findall(r'\*\*(.+?)\*\*', js)) | set(re.findall(r'\{s\|(.+?)\}', js))
missing = words - set(json.loads(js)['gloss'])
js = js.replace('</', '<\\/')
s = s[:m.start(2)] + '\n' + js + '\n' + s[m.end(2):]
open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', NL))
print('ok', 'THIẾU gloss: ' + ','.join(sorted(missing)) if missing else 'gloss đủ')
