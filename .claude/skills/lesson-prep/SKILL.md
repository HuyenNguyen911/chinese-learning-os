---
name: lesson-prep
description: >
  Bóc tách file .pptx bài khóa HSK6 của cô → (1) nạp từ vựng vào tier-a + trang học
  vocab-study, (2) xuất bài tập + bài viết/HSKK ra 1 file .docx để copy sang Google Docs.
  Use when user muốn "chuẩn bị bài", "bóc bài khóa", "lesson-prep", "chuẩn bị buổi X".
author: Chinese Learning OS
---

# lesson-prep — Chuẩn bị bài khóa từ pptx

> Chuẩn bị cho việc HỌC HSK6 của user. KHÔNG phải soạn bài cho học viên HSK1-3
> (đó là exercise-generator/teaching-coach). Gọi trực tiếp script của skill khác,
> KHÔNG invoke skill khác (One Request = One Skill).

## Input
File `.pptx` bài khóa của cô (mặc định tìm trong `raw/`, chọn file mới nhất nếu nhiều).

## Biến môi trường
```
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
DA=".claude/skills/doc-analyzer"
VS=".claude/skills/vocab-study/scripts"
LP=".claude/skills/lesson-prep/scripts"
```

## Luồng

### ① Convert pptx → text
```
"$PY" "$DA/pptx_to_text.py" "raw/<file>.pptx"
```
→ đọc `raw/<file>.pptx.txt` (mỗi slide 1 khối [TITLE]/[BODY]/[TABLE]/[NOTES]).

### ② Hiểu & phân loại (Claude tự đọc file .txt)
Xác định `buoiX_<chude>` (suy từ tên file/tiêu đề slide; không rõ → hỏi user 1 câu).
Tạo `output/hsk6/buoiX_<chude>/lesson-prep/`.

Phân loại từng slide:
- **Slide "từ vựng"** = từ có 释义 + ví dụ đi kèm → nhặt vào `vocab_payload.json`.
  KHÔNG đào từ trong đoạn bài đọc; chỉ lấy từ ở slide có giải thích + ví dụ.
- **Slide "生词拓展"** (chữ gốc + họ từ ghép, vd 庸→平庸/庸俗…) → nhóm vào
  `.claude/skills/vocab-study/data/exp_extra.json` key `"<N>"` (format giàu `{root, vi, members:[{w,g}]}`,
  `g` = nghĩa Việt từng từ con) → build_md/render_html hiện sơ đồ cây.
- **Slide "bài tập"** (đục lỗ, hoàn thành câu, 改写, 判断对错…) → `exercise_payload.json`.
- **Slide "bài viết/HSKK"** → `writing` (đề bài viết lớn) trong `exercise_payload.json`.

**`vocab_payload.json`:** `{ "bai": <N>, "bai_title": "<标题 bài khóa>", "words":[{"w","pinyin","desc","vi","ex"}] }`
- `bai_title` = **tên bài khóa (标题) lấy từ pptx** — thường ở slide tiêu đề (vd `第29课: "笑"的备忘录` → `"笑"的备忘录`). LUÔN bắt tên này.
- `desc` = 释义 tiếng Trung ĐƠN GIẢN (học sinh tiểu học hiểu, KHÔNG đồng nghĩa).
- `pinyin` ưu tiên lấy từ slide.
- `ex` = **例句 CÁ NHÂN HOÁ tự viết** (đủ chủ-vị, khẩu ngữ, sát đời sống user: tự học/luyện thi
  HSK6-HSKK, làm việc môi trường TQ, dạy HSK1-3; ưu tiên từ trong kho). **KHÔNG lấy câu từ slide** (bị trùng).

**`exercise_payload.json`** (theo mẫu `raw/bai tap mau.docx`, render bằng `render_baitap.py`):
```
{ "meta":{"lesson":"..."},
  "writing":{"title":"Bài viết lớn (作文)","prompt":"..."},   ← XẾP ĐẦU, chỉ đề, KHÔNG giải
  "exercises":[ {"title","type","note"?,"items":[{"q","answer","hl"?:[..],"opts"?:[..],"vi"?}]} ] }
```
- **BỎ QUA** bài luyện đọc từ / đặt câu với từ.
- `type`: `complete` (hoàn thành câu — thêm `opts` ~3 câu khác tự đặt); `rewrite` (改写 — 1 đáp án);
  `judge` (判断对错 — đáp án đúng/sai + lý do); `cloze` (đục lỗ — 1 đáp án). Bài bắt buộc 1 đáp án thì KHÔNG có `opts`.
- `hl` = từ/cấu trúc trọng tâm **tô ĐỎ** trong đáp án (vd `["也好","也罢"]`, `["预先"]`) — lấy từ chữ
  trong ngoặc của đề (改写) hoặc kết cấu đang luyện.
- Đáp án ưu tiên đáp án của bài; AI tự giải phần còn lại (判断/opts) — tự nhiên, khẩu ngữ, đơn giản nhưng điểm cao.

### ③ Kiểm tra đúng đắn (BẮT BUỘC trước khi ghi/render)
Rà lại từng đáp án `src:"AI"`: đúng ngữ pháp, đúng nghĩa, pinyin chuẩn. Sửa nếu sai.
(Nâng cao tùy chọn: nếu user bật orchestration, dùng workflow adversarial verify.)

### ④ Xuất
Vocab:
```
"$PY" "$LP/append_tier_a.py" "output/hsk6/buoiX_<chude>/lesson-prep/vocab_payload.json"
"$PY" "$LP/append_xlsx.py"   "output/hsk6/buoiX_<chude>/lesson-prep/vocab_payload.json"
# Ghi TÊN BÀI vào .claude/skills/vocab-study/data/bai_titles.json (map {"<N>": "<bai_title>"}):
#   thêm/ cập nhật khoá "<N>" = bai_title từ vocab_payload → build_md/render_html sẽ hiện tên bài.
# rồi chạy pipeline vocab-study (tối thiểu 1→3→5; thêm 2/4 nếu có chữ/từ mới):
"$PY" "$VS/extract_xlsx.py"
"$PY" "$VS/build_md.py"
"$PY" "$VS/render_html.py"
```
→ `output/study/hsk6/tu-vung.html` (từ mới hiện trạng thái D vì đọc tier-a).

Bài tập/viết (theo mẫu — writing đầu, tô đỏ từ trọng tâm):
```
"$PY" "$LP/render_baitap.py" \
  "output/hsk6/buoiX_<chude>/lesson-prep/exercise_payload.json" \
  "output/hsk6/buoiX_<chude>/lesson-prep/baitap.docx"
```

## Báo kết quả
Báo user: số từ mới thêm (tier-a + xlsx), đường dẫn `tu-vung.html` và `baitap.docx`.

## Nguyên tắc
- Chỉ đọc `memory/*`. Ghi tier-a.md **append-only** (dedup, Activation D) — không sửa entry cũ.
- Không sinh audio. Không tự promote/demote tier (việc của learning-strategist).
- Chỉ xử lý pptx trong V1.

## Phụ thuộc
`python-pptx`, `python-docx`, `openpyxl`, `pypinyin` (đều đã có).
