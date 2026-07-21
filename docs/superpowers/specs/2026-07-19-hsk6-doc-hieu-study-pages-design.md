# Giáo án HTML luyện 阅读 HSK6 — Design

Ngày: 2026-07-19
Trạng thái: Design (chờ user duyệt)

## 1. Mục tiêu
Bạn hay sai phần Đọc hiểu (阅读) HSK6. Xây **chuỗi trang HTML tự học tương tác**
(kiểu vocab-study) dạy chiến thuật + luyện từng phần trong 4 phần của 阅读, bám
đúng cơ chế đề thi HSK6.

## 2. Phạm vi & phi phạm vi
**Trong phạm vi**
- 4 phần của 阅读 HSK6, mỗi phần 1 trang HTML tự chứa:
  - 第一部分 病句 (chọn câu sai) — 10 câu
  - 第二部分 选词填空 (điền bộ từ) — 10 câu
  - 第三部分 语篇填空 (điền câu vào đoạn) — 10 câu
  - 第四部分 阅读理解 (đọc đoạn dài trả lời) — 20 câu
- **Pilot**: build 第一部分 病句 trọn vẹn TRƯỚC làm bản mẫu; chốt định dạng rồi
  nhân khuôn ra 3 phần còn lại (mỗi phần một session sau).

**Ngoài phạm vi (V1)**
- Không tạo bộ đề đầy đủ 50 câu như đề thật; drill là tập câu chọn lọc đủ phủ các loại bẫy.
- Không chấm điểm quy đổi ra thang HSK6 chính thức.
- Không đụng memory, không sửa skill khác.

## 3. Nguồn nội dung (ưu tiên giảm dần)
1. **PDF "6级攻略阅读"** (`raw/tiengtrungthuonghai.vn_...6级攻略阅读.pdf`, 269 trang, **bản scan → OCR**).
   Dùng doc-analyzer: structure-scan tìm đúng khoảng trang của phần → OCR có target
   (Tesseract chi_sim+vie+eng). KHÔNG OCR mù cả 269 trang.
2. **Kiến thức HSK6 阅读 của Claude** — chuẩn hóa, sửa lỗi OCR tiếng Trung, đảm bảo
   ví dụ đúng form thi.
3. **Web research** — xulaoshihsk (YouTube) + tổng hợp các kênh/tài liệu luyện đọc
   HSK6 uy tín, đối chiếu & bổ sung mẹo. (Ghi nguồn trong ghi chú, không nhồi rác.)
4. **Sách 900 病句** — CHƯA có file (chỉ có ảnh bìa). Nếu sau này có, bổ sung vào
   trang 第一部分. V1 không phụ thuộc nguồn này.

Nguyên tắc: nội dung OCR sai nét được Claude sửa; mọi ví dụ/đáp án phải **đúng cơ
chế đề thi HSK6** (số câu, dạng hỏi, cách chọn đáp án) — cơ chế thi thắng nếu mâu
thuẫn với OCR.

## 4. Cấu trúc mỗi trang HTML (khuôn chung)
Trang tự chứa 1 file (CSS/JS inline, chạy offline), tiếng Việt là ngôn ngữ giải thích:

1. **Cơ chế phần thi** — cấu trúc, số câu, thời gian gợi ý/câu, tiêu chí đúng-sai.
2. **Bản đồ bẫy (trap map)** — liệt kê từng loại lỗi/bẫy đặc trưng của phần, dấu
   hiệu nhận biết, cách xử lý. (VD 病句: 语序不当 / 搭配不当 / 成分残缺 / 成分赘余 /
   句式杂糅 / 不合逻辑 / 重复啰嗦 / 关联词误用 …)
3. **Chiến thuật làm bài** — quy trình từng bước (đọc gì trước, loại trừ ra sao,
   quản lý thời gian).
4. **Ví dụ mẫu có giải** — vài câu thật/chuẩn form, bấm để hiện lời giải + tô đúng
   chỗ dính bẫy + tên loại bẫy.
5. **Drill tương tác** — bộ câu bấm chọn đáp án, chấm ngay, hiện giải thích + gắn
   nhãn loại bẫy; có đếm đúng/sai.

Định dạng UI: bám phong cách vocab-study (self-contained, nút bấm, reveal, đếm điểm).

## 5. Output & vị trí file
- `output/study/hsk6/doc-hieu/phan1-benh-cau.html` (pilot)
- Về sau: `phan2-chon-tu.html`, `phan3-dien-cau.html`, `phan4-doc-hieu.html`
- Tài sản OCR trung gian (nếu lưu) để trong scratchpad, không commit rác vào vault.

## 6. Pipeline pilot 第一部分
1. doc-analyzer structure-scan PDF → xác định trang phần "第一部分/病句".
2. OCR target các trang đó.
3. Web research: mẹo 病句 của xulaoshihsk + kênh uy tín.
4. Claude soạn: cơ chế + trap map (các loại 语病) + chiến thuật + 5–8 ví dụ giải +
   drill ~15–20 câu chọn lọc phủ đủ loại bẫy. Sửa OCR, kiểm đúng form thi.
5. Render HTML tự chứa → `output/study/hsk6/doc-hieu/phan1-benh-cau.html`.
6. User xem, góp ý định dạng → chốt khuôn.

## 7. Rủi ro
- OCR tiếng Trung scan có thể sai nhiều nét → Claude phải rà tay, tốn công. Giảm
  thiểu bằng OCR target thay vì toàn bộ.
- Web research có thể không tìm đúng kênh xulaoshihsk → fallback dùng kiến thức nội tại,
  ghi rõ nếu không lấy được.
- Trang HTML lớn tốn token → build pilot 1 phần trước, tránh làm lại cả 4.

## 8. Tiêu chí hoàn thành pilot
- Trang `phan1-benh-cau.html` mở được offline, đủ 5 khối mục 4.
- Trap map phủ đủ các loại 语病 chính của 病句.
- Drill chấm được, mọi đáp án đúng cơ chế thi và đã rà lỗi OCR/nội dung.
- User duyệt định dạng để nhân ra 3 phần còn lại.
