# Schema JSON bài tập (`baitap-buoiX.json`)

```jsonc
{
  "meta": { "lesson": "Buổi 1: 会/想/能", "hsk": 1, "student": "tên (tùy chọn)" },
  "theme": { /* tùy chọn, override DEFAULT_THEME của build_worksheet.py */ },
  "blocks": [ /* danh sách block, mỗi block 1 "type" bên dưới */ ]
}
```

## Các block
- `noi`: `{ "type":"noi", "title", "instructions"?, "pairs":[{"left","right"}] }`
- `dien_cho_trong`: `{ "type":"dien_cho_trong", "title", "instructions"?,
  "word_bank":[str], "items":[{"q" (có "{}" đánh dấu chỗ trống), "answer", "src"?}] }`
- `doc_hieu`: `{ "type":"doc_hieu", "title", "instructions"?, "passage",
  "questions":[{"q","options":[str,str,str],"answer":"A|B|C","src"?}] }`
- `sap_xep`: `{ "type":"sap_xep", "title", "instructions"?,
  "items":[{"words":[str],"answer","answer_plus"?,"src"?}] }`
- `dich_dat_cau`: `{ "type":"dich_dat_cau", "title", "instructions"?,
  "items":[{"prompt","given":[str]?,"answer","answer_plus"?,"src"?}] }`
- `nghe`: `{ "type":"nghe", "title", "instructions"?,
  "items":[{"script" (chỉ vào đáp án), "q", "options":[str], "answer":"A|B|C",
  "audio"?, "audio_url"?, "src"?}] }`
- `noi_hskk`: `{ "type":"noi_hskk", "title", "part":"听后重复|回答问题",
  "instructions"?, "items":[{"script","hint"?,"hint_plus"?,"audio"?}] }`
- `grammar_note`: `{ "type":"grammar_note", "title", "instructions"?,
  "points":[{"pattern","explain"?,"example"?}] }` — hộp giải thích ngữ pháp (chỉ hiển thị).
- `writing_prompt`: `{ "type":"writing_prompt", "title", "instructions"?,
  "items":[{"prompt","kind"?:str,"target_length"?:str,"outline"?:[str]}] }` —
  đề viết/HSKK + dàn ý. `kind` tự do (vd `"viết"`, `"HSKK"`, `"đoạn văn"`,
  `"lời nhắn"`, `"nhật ký"` — dùng cho Viết 3.0 HSK2+). `target_length`
  tự do (vd `"60-100 chữ"`) hiển thị ngay sau đề bài, không bắt buộc.
- `dien_bieu_mau`: `{ "type":"dien_bieu_mau", "title", "instructions"?,
  "fields":[{"label","sample"?}] }` — điền biểu mẫu (Viết 3.0 HSK2+, vd đăng
  ký/form thông tin cá nhân). Không có 1 đáp án đúng duy nhất: worksheet in
  nhãn + dòng trống; đáp án (nếu có `sample`) in câu mẫu tham khảo, không
  phải đáp án bắt buộc.

## Đáp án 2 cấp (chỉ khối viết: `dich_dat_cau`, `sap_xep`)
2 khối này hỗ trợ đáp án 2 cấp, khớp cách chấm band điểm HSK. Bản đáp án
(`dapan.docx`) in cả hai; worksheet không đổi:
- **Chuẩn (đủ điểm)** = trường `answer` — câu tối thiểu đúng, đạt điểm.
- **Nâng cao (điểm cao)** = trường `answer_plus` (tùy chọn) — câu dài hơn, tự
  nhiên hơn, dùng thêm từ nối/vốn từ (thường chạm HSK cao hơn 1 bậc).
Nếu bỏ trường `_plus` thì chỉ in mức chuẩn (tương thích ngược). Khối trắc nghiệm /
điền / nghe / nối chỉ có 1 đáp án đúng nên không dùng cơ chế này.

**`noi_hskk` (`回答问题`) KHÔNG dùng cơ chế 2 cấp này** (đổi 2026-08-07, xem
`SKILL.md`) — `hint` chỉ chứa dàn bài gợi mở (Mở/Thân/Kết), không phải đáp án;
`hint_plus`/đáp án mẫu không còn dùng cho phần này.

`dich_dat_cau`/`sap_xep` có thêm field tùy chọn `answer_alts:[str]` — in dưới
nhãn "Phương án khác" (dùng cho lesson-prep khi muốn ~3 phương án). Ghi chú:
`render_study()` xuất 1 doc gộp (đề + đáp án), khác luồng worksheet/dapan của
exercise-generator.

Xem ví dụ đầy đủ: `worksheet/example-baitap.json`.
