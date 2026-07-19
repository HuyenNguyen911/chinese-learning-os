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
- **Slide "bài tập/bài đọc"** (đục lỗ, đặt câu, sắp xếp, đoạn đọc dùng lại từ mới)
  → `exercise_payload.json`. Từ mới ở đây chỉ là ngữ liệu, KHÔNG nhặt làm vocab.
- **Slide "bài viết/HSKK"** → block `writing_prompt` trong `exercise_payload.json`.

**`vocab_payload.json`:** `{ "bai": <N>, "words":[{"w","pinyin","desc","vi","ex"}] }`
- `desc` = 释义 tiếng Trung ĐƠN GIẢN (học sinh tiểu học hiểu, KHÔNG đồng nghĩa).
- `pinyin` ưu tiên lấy từ slide; `ex` ưu tiên câu ví dụ từ slide (tự nhiên).

**`exercise_payload.json`:** theo `.claude/skills/exercise-generator/worksheet/schema.md`
(gồm block mới `grammar_note`, `writing_prompt`; item tự luận có thể thêm `answer_alts`).
- Trích đề từ slide → block phù hợp (`dien_cho_trong`, `sap_xep`, `dich_dat_cau`, `doc_hieu`).
- Slide đã có đáp án → giữ, gắn `src:"slide"`. Đáp án AI tự giải → `src:"AI"`.
- Câu hoàn thành/đặt câu → cung cấp ~3 phương án (`answer` + `answer_plus` + `answer_alts`).
- Kèm `grammar_note` giải thích điểm ngữ pháp trọng tâm.
- Phong cách đáp án: tự nhiên, khẩu ngữ, đơn giản nhưng điểm cao.

### ③ Kiểm tra đúng đắn (BẮT BUỘC trước khi ghi/render)
Rà lại từng đáp án `src:"AI"`: đúng ngữ pháp, đúng nghĩa, pinyin chuẩn. Sửa nếu sai.
(Nâng cao tùy chọn: nếu user bật orchestration, dùng workflow adversarial verify.)

### ④ Xuất
Vocab:
```
"$PY" "$LP/append_tier_a.py" "output/hsk6/buoiX_<chude>/lesson-prep/vocab_payload.json"
"$PY" "$LP/append_xlsx.py"   "output/hsk6/buoiX_<chude>/lesson-prep/vocab_payload.json"
# rồi chạy pipeline vocab-study (tối thiểu 1→3→5; thêm 2/4 nếu có chữ/từ mới):
"$PY" "$VS/extract_xlsx.py"
"$PY" "$VS/build_md.py"
"$PY" "$VS/render_html.py"
```
→ `output/study/hsk6/tu-vung.html` (từ mới hiện trạng thái D vì đọc tier-a).

Bài tập/viết:
```
"$PY" "$LP/render_lesson_docx.py" \
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
