# HSK6 阅读 — Trang học 第一部分 病句 (Pilot) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây 1 trang HTML tự chứa dạy chiến thuật + luyện phần 第一部分 病句 của 阅读 HSK6, bám cơ chế đề thi.

**Architecture:** OCR có target phần 病句 trong PDF "6级攻略阅读" (doc-analyzer) → web research bổ sung mẹo → Claude soạn nội dung có cấu trúc (JSON dữ liệu) → render thành 1 file HTML tự chứa (CSS/JS inline, kiểu vocab-study). Nội dung do Claude rà & sửa lỗi OCR; cơ chế thi thắng nếu mâu thuẫn.

**Tech Stack:** Python (pypdf/pdf2image + Tesseract chi_sim+vie+eng qua doc-analyzer), HTML/CSS/JS thuần (không framework, không CDN — self-contained offline).

## Global Constraints
- Trang HTML **tự chứa 1 file**, mở offline chạy được, KHÔNG dùng CDN/asset ngoài.
- Ngôn ngữ giải thích: **tiếng Việt**; nội dung tiếng Trung là chữ Hán (chi_sim) + pinyin khi cần.
- Mọi câu hỏi/đáp án phải **đúng cơ chế đề thi HSK6 第一部分**: mỗi câu 4 lựa chọn A/B/C/D, chọn **1 câu SAI ngữ pháp**; 10 câu/phần trong đề thật.
- Output pilot: `output/study/hsk6/doc-hieu/phan1-benh-cau.html`.
- File OCR/nghiên cứu trung gian để trong scratchpad, KHÔNG commit rác vào vault.
- Không đụng `memory/`, không sửa skill khác.

---

### Task 1: OCR có target phần 病句 từ PDF

**Files:**
- Read: `raw/tiengtrungthuonghai.vn_Sách chinh phục phần Đọc HSK6_6级攻略阅读.pdf` (269 trang, scan)
- Create: `<scratchpad>/benh-cau-ocr.txt` (text OCR đã gom)

**Interfaces:**
- Produces: file text OCR các trang thuộc phần 第一部分/病句 (chiến thuật + ví dụ + câu luyện trong sách), để Task 3 chắt lọc.

- [ ] **Step 1: Structure-scan tìm khoảng trang phần 病句**

Dùng skill doc-analyzer (Structure Scan): OCR nhanh mục lục + tiêu đề trang để xác định trang bắt đầu/kết thúc phần "第一部分 / 病句 / chọn câu sai". Ghi lại dải trang (vd trang X–Y).

- [ ] **Step 2: OCR target dải trang đó**

Render dải trang X–Y sang ảnh (pdf2image ~300dpi) → Tesseract `-l chi_sim+vie+eng`. Gom kết quả vào `<scratchpad>/benh-cau-ocr.txt`.

- [ ] **Step 3: Verify OCR đọc được**

Đọc `benh-cau-ocr.txt`. Expected: nhận ra được ít nhất các tiêu đề loại lỗi (语序/搭配/成分…) và một số câu ví dụ tiếng Trung. Nếu OCR rác toàn bộ → tăng dpi / đổi preprocessing, chạy lại. Ghi chú các đoạn nghi sai nét để Task 3 rà.

- [ ] **Step 4: (không commit — file trong scratchpad)**

---

### Task 2: Web research mẹo 病句 (xulaoshihsk + kênh uy tín)

**Files:**
- Create: `<scratchpad>/benh-cau-research.md` (ghi chú + nguồn)

**Interfaces:**
- Produces: danh sách mẹo/khung phân loại 语病 và quy trình làm bài từ nguồn ngoài, có ghi nguồn; để Task 3 đối chiếu.

- [ ] **Step 1: Search xulaoshihsk 阅读/病句**

WebSearch: `xulaoshihsk HSK6 阅读 病句`, `徐老师 HSK6 病句 技巧`. Nếu tìm được video/bài → WebFetch tóm mẹo.

- [ ] **Step 2: Search các kênh/tài liệu HSK6 病句 uy tín**

WebSearch: `HSK6 阅读第一部分 病句 类型 技巧`, `HSK6 语病 六大类`, các blog/kênh đánh giá cao. WebFetch 2–3 nguồn tốt.

- [ ] **Step 3: Tổng hợp vào research.md**

Ghi: các loại 语病 phổ biến, dấu hiệu, mẹo loại trừ, quy trình thời gian. Kèm URL nguồn. Nếu KHÔNG tìm được xulaoshihsk cụ thể → ghi rõ "không truy được, dùng kiến thức nội tại + nguồn khác".

- [ ] **Step 4: Verify**

research.md có ≥1 khung phân loại loại lỗi + ≥3 mẹo làm bài, mỗi mục có nguồn hoặc nhãn "nội tại".

---

### Task 3: Soạn nội dung có cấu trúc (data JSON)

**Files:**
- Create: `<scratchpad>/phan1-benh-cau-data.json`
- Input: `benh-cau-ocr.txt`, `benh-cau-research.md`

**Interfaces:**
- Produces: object JSON với các khóa: `co_che` (cơ chế thi), `trap_map` (mảng loại lỗi: {ten_vi, ten_zh, dau_hieu, cach_xu_ly, vi_du_sai, vi_du_dung}), `chien_thuat` (mảng bước), `vi_du_giai` (mảng {cau_zh, pinyin?, dap_an, giai_thich_vi, loai_bay}), `drill` (mảng câu: {id, options:[{zh, pinyin?}]×4, dap_an_sai_index, giai_thich_vi, loai_bay}). Task 4 render từ object này.

- [ ] **Step 1: Viết `co_che` + `chien_thuat`**

Từ OCR + research + kiến thức: mô tả cơ chế 第一部分 (10 câu, mỗi câu 4 lựa chọn, chọn câu SAI, ~0.5–1 phút/câu) và quy trình làm bài từng bước (đọc chủ ngữ-vị ngữ-tân ngữ, soi 搭配, soi 关联词, soi 语序…).

- [ ] **Step 2: Viết `trap_map` phủ đủ loại 语病 chính**

Tối thiểu các loại: 语序不当, 搭配不当, 成分残缺, 成分赘余, 句式杂糅, 结构混乱, 不合逻辑, 关联词误用, 重复啰嗦, 表意不明. Mỗi loại: dấu hiệu + cách xử lý + 1 ví dụ sai / 1 ví dụ sửa đúng.

- [ ] **Step 3: Viết `vi_du_giai` (5–8 câu) và `drill` (15–20 câu)**

Ví dụ + drill đúng form thi: mỗi câu drill là 4 phương án A–D, đúng 1 phương án SAI ngữ pháp, ghi rõ index câu sai + loại bẫy + giải thích tiếng Việt. Ưu tiên câu lấy/chỉnh từ OCR sách; câu tự viết phải chuẩn form. Rà lỗi OCR tiếng Trung từng chữ.

- [ ] **Step 4: Verify nội dung & cơ chế**

Tự rà: (a) mỗi câu drill có đúng 1 đáp án "câu sai" xác định; (b) chữ Hán không còn lỗi OCR; (c) mỗi drill gắn 1 loại bẫy có trong trap_map; (d) JSON hợp lệ (parse được). Sửa inline tới khi đạt.

---

### Task 4: Render trang HTML tự chứa

**Files:**
- Create: `output/study/hsk6/doc-hieu/phan1-benh-cau.html`
- Input: `<scratchpad>/phan1-benh-cau-data.json`

**Interfaces:**
- Consumes: object JSON từ Task 3 (nhúng inline vào `<script>` trong HTML).
- Produces: 1 file HTML tự chứa mở offline.

- [ ] **Step 1: Dựng khung HTML 5 khối**

Cấu trúc section: (1) Cơ chế thi, (2) Bản đồ bẫy (accordion/card từ trap_map), (3) Chiến thuật (list bước), (4) Ví dụ có giải (bấm reveal), (5) Drill (chọn A–D, chấm ngay). CSS inline gọn, responsive, light/dark ổn. Nhúng data JSON inline.

- [ ] **Step 2: JS tương tác drill**

Mỗi câu drill: click chọn phương án → đánh dấu đúng/sai (câu SAI = đáp án đúng của bài), hiện giải thích + loại bẫy, cập nhật bộ đếm điểm tổng. Nút "hiện đáp án" cho ví dụ.

- [ ] **Step 3: Verify mở offline**

Mở file trong trình duyệt (hoặc kiểm tra bằng cách đọc + mô tả). Expected: 5 khối hiển thị; bấm 1 câu drill → chấm đúng/sai + giải thích hiện ra; bộ đếm cộng. Không lỗi console, không gọi asset ngoài.

- [ ] **Step 4: Báo user duyệt định dạng**

Trình bày cho user: đường dẫn file + tóm tắt nội dung. Chờ user xem/góp ý trước khi nhân khuôn ra 3 phần còn lại. (Commit theo yêu cầu user, không tự commit trên `main`.)

---

## Follow-on (ngoài pilot, sau khi user duyệt)
Nhân khuôn Task 3–4 cho: 第二部分 选词填空, 第三部分 语篇填空, 第四部分 阅读理解 — mỗi phần lặp OCR-target + research + data + render, dùng đúng cơ chế thi từng phần.

## Self-Review
- **Spec coverage:** 5 khối nội dung (spec §4) → Task 3+4. Nguồn OCR (§3.1)→Task1, web (§3.3)→Task2, cơ chế thi thắng (§3)→Task3 Step4 & Global Constraints. Output path (§5)→Task4. Pilot-first (§2)→plan chỉ pilot + follow-on. ✅
- **Placeholder scan:** không có TBD/TODO; mỗi task có deliverable + bước verify cụ thể. ✅
- **Type consistency:** khóa JSON (`trap_map/vi_du_giai/drill`, `dap_an_sai_index`, `loai_bay`) dùng nhất quán giữa Task 3 (produces) và Task 4 (consumes). ✅
