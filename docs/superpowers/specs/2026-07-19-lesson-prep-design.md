# Thiết kế skill `lesson-prep`

_Ngày: 2026-07-19 · Chinese Learning OS_

## 1. Mục đích

`lesson-prep` là skill chuẩn bị cho việc **học HSK6 của chính user**. Đầu vào là file
`.pptx` bài khóa của cô giáo. Đầu ra là 2 sản phẩm:

1. **Từ vựng** → nạp vào hệ thống học có sẵn (`tier-a.md` + trang `tu-vung.html` của `vocab-study`).
2. **Bài tập + bài viết/HSKK** → 1 file `.docx` để user copy sang Google Docs.

Đây KHÔNG phải skill soạn bài cho học viên HSK1-3 (đó là `exercise-generator` /
`teaching-coach`). Đây là chuẩn bị tài liệu cho việc học của chính user.

## 2. Luồng tổng thể

```
pptx bài khóa
   │  ① CONVERT (doc-analyzer, Tầng 1 — thêm mới)
   ▼
{file}.pptx.txt  (===== SLIDE n =====, kèm [TITLE]/[BODY]/[TABLE]/[NOTES])
   │  ② HIỂU (lesson-prep — Claude đọc, phân loại, tự giải + kiểm tra)
   ▼
vocab_payload.json   +   exercise_payload.json
   │  ③ VOCAB                │  ④ BÀI TẬP/VIẾT
   ▼                         ▼
append tier-a.md (dedup, ⚪)  render .docx (renderer exercise-generator mở rộng)
+ append raw/Từ vựng.xlsx     → lesson-prep/baitap.docx
+ pipeline vocab-study
  → output/study/hsk6/tu-vung.html
```

**Nguyên tắc cốt lõi:**

- `doc-analyzer` chỉ **convert** pptx→text; KHÔNG áp schema tri thức (business rules…) của nó vào bài học.
- Phần "hiểu" (phân loại vocab/bài tập/bài viết, tự giải, kiểm tra đúng sai) là **Claude trong SKILL.md**, không script hoá — vì layout slide của cô mỗi bài mỗi khác.
- Tái dùng tối đa: pipeline `vocab-study` + renderer `.docx` của `exercise-generator`.
- **One Request = One Skill** (CLAUDE.md §3): lesson-prep tự chạy trọn luồng bằng cách **gọi trực tiếp script** của các skill khác, KHÔNG "invoke skill" khác (không chain skill).

## 3. Khâu ① — Convert pptx → text (thuộc doc-analyzer)

Thêm vào skill `doc-analyzer`:

- Script mới `pptx_to_text.py` (đặt cạnh `pdf_to_text.py`), dùng `python-pptx` (1.0.2, đã có).
- Thêm 1 dòng vào bảng conversion trong `doc-analyzer/SKILL.md`: `.pptx → pptx_to_text.py`.
- Output: ghi cạnh file gốc `{file}.pptx.txt`, mỗi slide 1 khối, giữ cấu trúc:

  ```
  ===== SLIDE 7 =====
  [TITLE] 生词
  [BODY] 尴尬 gāngà ...
  [TABLE] 词 | 拼音 | 释义
          尴尬 | gāngà | ...
  [NOTES] (ghi chú của cô nếu có)
  ```

  Trích: text mọi shape (theo thứ tự), bảng (`table`), và speaker notes (`notes_slide`).
- Xử lý lỗi: thiếu `python-pptx` → in `ERROR NOPPTX`; doc-analyzer thử `python -m pip install python-pptx` rồi chạy lại 1 lần (đúng pattern `ERROR NOPYPDF`/`NOPYMUPDF` hiện có). Thất bại → báo hướng dẫn cài + dừng.
- Giữ nguyên hành vi doc-analyzer cũ; chỉ bổ sung khả năng convert (Tầng 1). Tầng 2 (YAML tri thức) không dùng cho luồng này.

## 4. Khâu ② — Hiểu & phân loại (Claude, trong lesson-prep/SKILL.md)

Claude đọc `{file}.pptx.txt`, phân loại từng khối slide và xuất 2 file JSON trung gian
vào `output/hsk6/buoiX_<chude>/lesson-prep/`.

**Xác định `buoiX_<chude>`:** suy từ tên file pptx / tiêu đề slide đầu; nếu không rõ →
hỏi user đúng 1 câu (số buổi + chủ đề ngắn) rồi tạo slug (vd `buoi5_tinhcach`). Nếu
folder `buoiX_*` đã tồn tại thì dùng lại, không đặt tên mới.

### 4.1 Nhận diện loại slide

- **Slide "từ vựng"** = có một từ kèm **giải thích (释义) + ví dụ** cho chính từ đó.
  Đây là tín hiệu nhận diện từ mới. → luồng vocab.
- **Slide "bài tập / bài đọc"** = đục lỗ, đặt câu, sắp xếp, hoặc đoạn đọc dùng lại các
  từ mới. → luồng bài tập. Từ mới xuất hiện lại ở đây chỉ là **ngữ liệu**, KHÔNG nhặt
  làm vocab.
- **Slide "bài viết / HSKK"** = đề viết đoạn/luận hoặc đề nói nâng cao. → luồng bài viết.

> KHÔNG đào từ mới từ đoạn bài đọc. Chỉ lấy từ ở slide có 释义 + ví dụ. Điều này giúp
> khâu phân loại chắc chắn, không phải đoán từ nào "đáng học" trong prose.

### 4.2 `vocab_payload.json`

Mỗi từ chuẩn hoá đúng cột sheet 'Từ vựng' của vocab-study:

```jsonc
{
  "bai": 5,                          // số buổi/bài (user xác nhận hoặc suy từ tên file)
  "words": [
    {
      "w": "尴尬",
      "pinyin": "gāngà",             // ưu tiên lấy từ slide; thiếu thì pypinyin
      "desc": "…",                   // 释义 tiếng Trung ĐƠN GIẢN (học sinh tiểu học hiểu, KHÔNG đồng nghĩa)
      "vi": "…",                     // nghĩa Việt
      "ex": "…"                      // ví dụ TỰ NHIÊN (ưu tiên câu từ slide)
    }
  ]
}
```

### 4.3 `exercise_payload.json`

Theo schema `baitap` của exercise-generator (có mở rộng ở §6), gồm các block:

- Bài tập trích từ slide → map sang block phù hợp: `dien_cho_trong` (đục lỗ),
  `sap_xep`, `dich_dat_cau`, `doc_hieu` (bài đọc), …
- Đáp án:
  - Slide **đã có** đáp án → giữ, gắn `src: "slide"`.
  - Claude **tự giải** → gắn `src: "AI"`.
  - Câu hoàn thành/đặt câu → cung cấp ~3 phương án (xem §6, field `answer_alts`).
- Giải thích ngữ pháp → block mới `grammar_note`.
- Bài viết/HSKK → block mới `writing_prompt` (đề + dàn ý).

**Phong cách đáp án AI (bắt buộc):** tự nhiên, khẩu ngữ, đơn giản nhưng điểm cao.

## 5. Khâu ③ — Vocab: tier-a + trang học

1. **Append `knowledge/vocabulary/tier-a.md`** — chiến lược ghi an toàn:
   - **Append-only**; **dedup theo 生词** (bỏ qua từ đã tồn tại ở bất kỳ tier nào).
   - Từ mới đánh Activation khởi điểm **⚪ (0 — "chưa dùng")**.
   - KHÔNG sửa/ghi đè entry sẵn có → learning-strategist và lesson-prep cùng ghi
     file nhưng không dẫm chân (lesson-prep chỉ thêm dòng mới ở cuối/đúng mục Tier A).
2. **Append `raw/Từ vựng.xlsx`** (sheet 'Từ vựng') các dòng vocab mới (openpyxl), dedup theo 生词.
3. **Chạy pipeline vocab-study** để sinh lại trang học:
   `extract_xlsx → build_hanzi (nếu có chữ mới) → build_md → gen_mnemonic (nếu có từ mới, cần orchestration) → render_html`
   → `output/study/hsk6/tu-vung.html`.
   - Trang học tự hiện trạng thái ⚪ cho từ mới (vì nó đọc tier-a).

## 6. Khâu ④ — Bài tập/viết: mở rộng renderer → .docx

Tái dùng `exercise-generator/worksheet/build_worksheet.py`, **mở rộng**:

- **2 block type mới:**
  - `grammar_note`: `{ "type":"grammar_note", "title", "points":[{"pattern","explain","example"}] }`
  - `writing_prompt`: `{ "type":"writing_prompt", "title", "items":[{"prompt","kind":"viết|HSKK","outline":[str]}] }`
- **Phương án thứ 3:** thêm field tùy chọn `answer_alts: [str]` cho `dich_dat_cau` /
  `sap_xep` (hiện đã có `answer` + `answer_plus` = 2 mức). Tương thích ngược: bỏ field thì render như cũ.
- **`src`**: đã có sẵn trong schema — dùng để đánh dấu `"slide"` vs `"AI"`, in nhãn nguồn cạnh đáp án.

**Output (quyết định thiết kế):**

- **1 file gộp có đáp án**: `output/hsk6/buoiX_<chude>/lesson-prep/baitap.docx` —
  đề + đáp án (đánh dấu nguồn slide/AI) + giải thích ngữ pháp + đề viết/HSKK + dàn ý.
  KHÔNG tách worksheet/đáp án kiểu học viên (vì học cho bản thân).
- **KHÔNG sinh audio** (user copy text sang Google Docs, không cần MP3).

## 7. Kiểm tra đúng đắn

- **Cổng kiểm tra đáp án (bắt buộc):** sau khi Claude tự giải, chạy 1 lượt **tự phản
  biện** — rà từng đáp án `src:"AI"` về đúng ngữ pháp / nghĩa / pinyin trước khi render.
- **Nâng cao (tùy chọn):** nếu user bật orchestration, có thể dùng workflow adversarial
  verify cho các đáp án. Mặc định làm inline.

## 8. Governance (cần user / close-session duyệt)

Cập nhật `CLAUDE.md`:

- **§3 Routing** — thêm soft route cho lesson-prep: "chuẩn bị bài", "bóc bài khóa",
  "lesson-prep", "buổi học của cô", "chuẩn bị buổi X" → `lesson-prep`. Thêm hard route `/lesson-prep`.
- **§6 State Ownership** — ghi rõ quyền của lesson-prep:
  - `knowledge/vocabulary/tier-a.md` — **append-only** (dùng chung với learning-strategist; chỉ thêm từ mới ⚪, không sửa entry cũ).
  - `raw/Từ vựng.xlsx` — append dòng vocab mới.
  - `output/hsk6/**/lesson-prep/` — vocab_payload.json, exercise_payload.json, baitap.docx.
- **§7 Skill Catalog** — cập nhật mô tả lesson-prep (bỏ nhãn "CHƯA làm").

## 9. Cấu trúc file skill (dự kiến)

```
.claude/skills/lesson-prep/
  SKILL.md                 # luồng ①–④ + cổng kiểm tra; Claude điều phối
  scripts/
    append_tier_a.py       # append tier-a.md, dedup theo 生词, đánh ⚪
    append_xlsx.py         # append raw/Từ vựng.xlsx từ vocab_payload.json
  (tái dùng)
    doc-analyzer/pptx_to_text.py            # convert
    vocab-study/scripts/*.py                # sinh trang học
    exercise-generator/worksheet/build_worksheet.py  # render .docx (đã mở rộng)
```

## 10. Phụ thuộc

- `python-pptx` (1.0.2 — đã có)
- `openpyxl`, `pypinyin` (vocab-study — đã có)
- `python-docx` (exercise-generator — đã có)

## 11. Ngoài phạm vi (YAGNI)

- Không xử lý PDF/DOCX bài khóa (chỉ pptx trong V1; các định dạng khác đã có doc-analyzer riêng).
- Không sinh audio.
- Không tự promote/demote tier (đó là việc learning-strategist).
- Không tách file worksheet/đáp án riêng.
