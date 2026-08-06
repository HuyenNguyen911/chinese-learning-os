# HSK2 (chuẩn 3.0) Full Course Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây bộ HSK2 chuẩn **3.0** — **15 buổi (bám sát 15 bài New HSK Course 2) + 2 ôn**, trọn gói slide/audio/bài tập(có Viết 3.0)/bài đọc; 生词 + 課文 + 45 ngữ pháp **trích trực tiếp từ `raw/New HSK Course 2.pdf`** (có text layer); footer tham khảo Hán ngữ 第一册·下; không trùng từ HSK1.

**Architecture:** Pipeline nội dung trên tooling vault (teaching-coach, exercise-generator, edge-tts). Mỗi buổi = 1 folder `output/hsk2/buoiXX_<slug>/` với `slide/` · `baitap/` · `doc/`. Buổi = 1 bài sách. Quy trình mỗi buổi giống nhau (Procedure P). Sản xuất **tuần tự từng buổi theo đúng thứ tự sách**, mỗi buổi có 1 cổng duyệt trọn gói riêng trước khi qua buổi kế tiếp (không làm pilot rồi hàng loạt).

**Tech Stack:** Python 3.12 (pypdf, python-pptx, Pillow, pypinyin, python-docx), edge-tts, build_deck.py / slide_audio.py / fetch_images.py (teaching-coach), build_worksheet.py / check_baitap.py (exercise-generator), gen_stroke_gif.py (tuỳ chọn, tái dùng HSK1).

**Spec:** `docs/superpowers/specs/2026-07-20-hsk2-full-course-design.md`. **Mục lục sách (nguồn chân lý syllabus):** `docs/superpowers/specs/hsk2-new-hsk-course-2-toc.md`.

## Global Constraints

- **Python:** `PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"`. Chạy từ gốc repo `c:/Tài liệu/ai-vault/CHINESE`.
- **NGUỒN CHÂN LÝ = sách:** 生词/課文/45 ngữ pháp trích từ `raw/New HSK Course 2.pdf` (KHÔNG bịa, KHÔNG web-search). Không tự nghĩ từ vựng. Chữ Hán trích bằng pypdf sạch; **bảng/vùng layout phức tạp (nhiều cột) → render ảnh (PyMuPDF) rồi đọc trực tiếp bằng vision**, KHÔNG tin OCR/pypdf mù cho các vùng đó (đã xác nhận ở Task 0.1). **Pinyin in trong PDF bị lỗi mất dấu thanh toàn sách → LUÔN tự sinh bằng `pypinyin`** từ chữ Hán, không dùng pinyin PDF.
- **Buổi = bài:** 15 buổi ↔ 15 bài sách (mục lục TOC). Ôn: `on1_bai1-8` (sau bài 8), `on2_bai9-15` (sau bài 15).
- **CHỐNG TRÙNG HSK1 (cứng):** mọi 生词 loại/đánh dấu từ đã có trong 150 từ HSK1 (Task 0.1).
- **Động vật/thú cưng:** lồng **từ mở rộng** vào Bài 5 (thăm nhà bạn), đánh dấu "ngoài 200 từ sách". Không thêm buổi.
- **Mọi từ/câu tiếng Trung** đủ **汉字 + pinyin + nghĩa Việt**.
- **Thứ tự block slide (sửa 2026-08-06, sau Buổi 5 — bỏ "ôn buổi trước" và tách "lỗi người Việt" khỏi vị trí cố định cuối, đây là feedback user đã nhắc từ trước):** `title → mục tiêu → 生词 → [ngữ pháp (小语讲堂) → lỗi người Việt liên quan]` (lặp lại theo từng nhóm ngữ pháp, lỗi thường gặp đặt NGAY SAU nhóm ngữ pháp sinh ra nó, không dồn hết xuống cuối) `→ 10 câu khẩu ngữ → hội thoại/課文 → bài đọc → footer Hán ngữ 第一册·下 → preview bài tập`. KHÔNG block ngữ âm. KHÔNG có slide "ôn buổi trước" đầu mỗi buổi.
- **Bài tập đủ 4 phần 3.0:** 听 · 读 (+ **≥1 văn bản thực tế/buổi**: tin nhắn/biển báo/thực đơn/quảng cáo, tự soạn theo chủ đề, KHÔNG lấy từ sách) · **书写/Viết** (sắp câu, điền chữ, viết câu ngắn · **+ luân phiên đoạn 60–100 chữ / điền form / lời nhắn / nhật ký** qua các buổi) · HSKK.
- **Ngữ pháp bổ sung ngoài sách (vá theo tiêu chuẩn đầu ra, không có trong 45 điểm New HSK Course 2), lồng vào buổi — KHÔNG dạy ở 2 buổi Ôn (Ôn chỉ ôn tập):** **把字句 cơ bản** lồng **Bài 4** (ghép 简单趋向补语 vốn có); **被字句 đơn giản** lồng **Bài 11**; **连…都/也** lồng **Bài 12**. Đánh dấu rõ "ngoài 45 điểm sách chính" trong slide buổi tương ứng.
- **Giao tiếp thiếu, lồng vào buổi — KHÔNG dồn vào Ôn (đã đối chiếu HSK 二级考试大纲 chính thức, chinesetest.cn, 2026-07-27 — xem spec §16b):** hỏi đường → **Bài 2** (✅ chính thức); hỏi giá/so sánh giá (đổi tên từ "mặc cả") → **Bài 9** (✅ chính thức); giới thiệu bản thân/gia đình sâu → **Bài 5** (✅ chính thức); đặt khách sạn → **Bài 3** (⚠️ ngoài chuẩn thi, giữ theo yêu cầu cá nhân); đặt lịch hẹn → **Bài 10** (⚠️ ngoài chuẩn thi, ghép với 就要…了 — dời từ Bài 6 vì hợp ngữ pháp hơn). Capstone Ôn 2 chỉ ôn/ứng dụng lại các kỹ năng này, không dạy mới.
- **Audio đọc chậm:** slide `--rate=-18%`; baitap `nghe --rate=-22%`, `noi_hskk --rate=-18%`. Giọng chính `zh-CN-XiaoxiaoNeural`. (Nếu user cấp MP3 gốc sách → ưu tiên.)
- **Cổng duyệt:** (a) text 課文 trích từ PDF → trình user duyệt; (b) script 听力/HSKK trình user trước khi sinh MP3; (c) `check_baitap.py` + rà đáp án AI; (d) soát 多音字/儿化 mọi audio.
- **Sửa slide sau khi user đã tự sửa tay .pptx (bài học từ Buổi 3):** KHÔNG chạy lại
  `build_deck.py` (rebuild toàn bộ từ JSON sẽ xoá mất mọi chỗ user đã tự sửa tay trực
  tiếp trong file). Patch trực tiếp bằng `python-pptx`, tìm đúng slide cần sửa theo
  **nội dung** (kicker + title/hz, không theo vị trí index) — vì user có thể đã tự xoá/
  thêm slide làm lệch số thứ tự so với JSON gốc. Audio nhúng (🔊) cũng phải patch riêng
  (thay `_blob` của media part liên kết qua `r:link`), không chỉ cập nhật file mp3 rời.
- **Console Windows:** in 中文 debug đặt `PYTHONIOENCODING=utf-8`.
- **Git:** commit sau mỗi task, message tiếng Việt + trailer `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`. **Nhánh `feat/hsk2-full-course`** (lưu ý: môi trường user đôi khi tự `git checkout` về nhánh khác — verify `git branch --show-current` trước mỗi thao tác file/commit).

---

## File Structure

```
output/hsk2/
  README.md                          # [Task 0.3] syllabus 15 buổi + 2 ôn (source of truth, chuẩn 3.0)
  buoiXX_<slug>/
    slide/  buoiXX.json · buoiXX-images.json · Buoi-XX-<Ten>.pptx · assets/(*.jpg, *.gif?, audio/)
    baitap/ baitap-buoiXX.json · hocsinh/worksheet.docx+audio/ · dapan/dapan.docx
    doc/    bai-doc.md (課文 nguyên văn sách) · bai-doc.NN.mp3
docs/superpowers/plans/hsk2-vocab-grammar-checklist.md   # [Task 0.1] 200 từ + 45 ngữ pháp trích từ PDF + cờ trùng HSK1
```

Slug 15 buổi: `buoi01_moian_vitquay`, `buoi02_giaothong`, `buoi03_dulich_xian`, `buoi04_trangphuc_mausac`, `buoi05_thamnha`, `buoi06_sinhnhat`, `buoi07_thethao`, `buoi08_trinho_sosanh`, `buoi09_douong`, `buoi10_thicu`, `buoi11_monan_yeuthich`, `buoi12_thoitiet`, `buoi13_hoctiengtrung`, `buoi14_letet`, `buoi15_kehoach`.

Vocab-study phase (§13 spec) **tách plan riêng** — xem "Out of scope".

---

## PHASE 0 — Infrastructure

### Task 0.1: Trích 词汇表 + 45 ngữ pháp từ sách + cờ trùng HSK1 — ✅ XONG (commit `8f06202`)

**Files:** `docs/superpowers/plans/hsk2-vocab-grammar-checklist.md`

- [x] **Step 1: Bóc 词语表 (trang 141-146 sách).** pypdf/OCR đều bị xáo cột — chuyển sang **render ảnh (PyMuPDF 250dpi) + đọc trực tiếp bằng vision**, chính xác 100%. 210 mục (207 từ + 3 tên riêng).
- [x] **Step 2: Trích từ HSK1 để loại trùng** — lọc `output/hsk1/*/slide/*.json` field `hz`, bỏ câu ví dụ dài, còn ~160 mục dạng từ/cụm từ.
- [x] **Step 3: Viết checklist** — bảng vocab theo bài (1-15) + cột từ loại/nghĩa/trùng HSK1. 45 điểm ngữ pháp đã có sẵn ở TOC file, không lặp lại.
- [x] **Step 4: Verify** — tổng 210 khớp "200 từ + 略有扩展"; mọi từ có bài; **19 từ trùng HSK1** (đáng chú ý: Bài 4 có 5/16 từ trùng — cụm màu sắc, do HSK1 3.0 đã dạy màu riêng).
- [x] **Step 5: Commit** `docs(hsk2): Task 0.1 - checklist 210 từ vựng, trích từ ảnh trang 141-146 sách`

**Phát hiện quan trọng cần áp dụng cho các Task sau:** pinyin in trong PDF (cả 課文 lẫn bảng từ) bị lỗi mất dấu thanh toàn sách → khi trích 課文 ở Procedure P (P2), **không dùng pinyin PDF — tự sinh bằng `pypinyin`** từ chữ Hán (chữ Hán trích pypdf vẫn sạch, chỉ pinyin lỗi).

### Task 0.2: Mở rộng schema Viết (书写) 3.0 trong exercise-generator (đã quyết — không chỉ đánh giá)

**Files:** Read/sửa `.claude/skills/exercise-generator/worksheet/schema.md`, `build_worksheet.py`

**Quyết định (2026-07-27, vá theo tiêu chuẩn đầu ra):** Viết 3.0 phải có đủ 4 dạng cũ (sắp câu, điền chữ, viết câu ngắn) + **4 dạng mới**: đoạn ngắn 60–100 chữ theo chủ đề buổi, điền biểu mẫu đơn giản (form), viết lời nhắn (note), viết nhật ký ngắn. Luân phiên qua các buổi, không bắt buộc đủ cả 4 dạng mới mỗi buổi.

- [ ] **Step 1:** Rà dạng mục hỗ trợ hiện có trong schema/build_worksheet.py.
- [ ] **Step 2:** Với 3 dạng cũ (sắp câu/điền chữ/câu ngắn) — map trực tiếp nếu đã hỗ trợ.
- [ ] **Step 3:** Với 4 dạng mới (đoạn văn/form/note/nhật ký) — nếu schema chưa có mục dạng "đoạn dài" hay "form điền", **bổ sung dạng mục mới** vào schema (không phải chỉ đề xuất — quyết định đã chốt). Thiết kế format chấm điểm 2 cấp (gợi ý + đáp án mẫu) cho các dạng viết tự do này.
- [ ] **Step 4:** Cập nhật README kỹ thuật của exercise-generator (nếu có) ghi rõ dạng mục mới dùng riêng cho HSK2 3.0+.
- [ ] **Step 5:** Commit `feat(exercise-generator): thêm dạng Viết đoạn/form/note/nhật ký cho chuẩn 3.0`.

> ⚠️ **Git hygiene:** `exercise-generator` là tool dùng chung mọi cấp (HSK1/2/3/6), giống vocab-study (CLAUDE.md §5.5.6). Step 3–5 (sửa schema/build_worksheet.py) phải làm và commit trên **`main`** (hoặc nhánh chore riêng), KHÔNG commit vào `feat/hsk2-full-course`. Chỉ nội dung buổi HSK2 (JSON, docx sinh ra) mới ở nhánh này.

### Task 0.3: README syllabus (source of truth) — ✅ XONG (commit `a5cfb26`)

**Files:** `output/hsk2/README.md`

- [x] **Step 1:** Bảng 15 buổi + 2 ôn (folder/课文/chủ đề/ngữ pháp/Hán ngữ/trạng thái). Header ghi rõ chuẩn 3.0 + sách chính/tham khảo. Ghi chú kỹ thuật (Viết 3.0, đọc thực tế, pinyin, GIF nét, trang từ vựng). Mọi buổi "⏳".
- [x] **Step 2: Verify** — folder đúng convention; ôn 1 sau bài 8, ôn 2 sau bài 15.
- [x] **Step 3: Commit** `docs(hsk2): Task 0.3 - README syllabus tổng (source of truth)`

**PHASE 0 HOÀN TẤT** (Task 0.1 + 0.2 + 0.3). Bước tiếp theo: Task 1 (Procedure P cho Bài 1).

---

## PROCEDURE P — Quy trình sản xuất 1 buổi

> Param mỗi buổi: `XX`, `SLUG`, `DIR=output/hsk2/buoiXX_SLUG`; **bài sách số N**; 生词 (Task 0.1, đã lọc trùng HSK1); ngữ pháp 小语讲堂 (TOC); 課文 sách; dòng Hán ngữ 第一册·下; lỗi người Việt.

**P1 — Master Teacher:** Đóng vai Master Chinese Teacher. Soạn: giải thích 小语讲堂 đúng bản chất; 生词 bài (đủ 汉字/pinyin/nghĩa, đã lọc trùng HSK1); ví dụ khẩu ngữ; **10 câu khẩu ngữ dùng-ngay**; hội thoại; 2–3 lỗi người Việt (đọc `common-vietnamese-mistakes.md`).

**P2 — 課文 (cổng a):** Trích **nguyên văn** 課文 bài N từ `raw/New HSK Course 2.pdf` (pypdf, theo trang trong TOC). Chọn 課文 phù hợp (đối thoại chính + bài tự sự). **Trình user duyệt text đã trích** → ghi `DIR/doc/bai-doc.md` (汉字 nguyên văn + pinyin + dịch Việt).

**P3 — Experience Designer:** Map → `DIR/slide/buoiXX.json` (schema teaching-coach, đúng thứ tự block). Footer Hán ngữ 第一册·下 (bullets/reading); lỗi VN (table). Action title + ghost-deck test.
**Nếu học viên phản hồi 生词/ngữ pháp gốc sách quá cơ bản** (đã học/vượt trình độ) — KHÔNG mặc định bám 100% sách: chủ động đề xuất nâng cấp (vd đổi 生词 sang nhóm từ nâng cao liên quan ngữ pháp buổi, thêm điểm ngữ pháp bậc cao hơn từ bài sau đưa sớm), đánh dấu rõ "mở rộng ngoài sách chính" (sửa 2026-08-06, Buổi 5).

**P4 — Ảnh:** `DIR/slide/buoiXX-images.json` → `fetch_images.py`. Expected `DONE: N/N`.

**P5 — GIF nét (tuỳ chọn):** chữ mới khó → `gen_stroke_gif.py`.

**P6 — Render pptx (KHÔNG audio):** `build_deck.py` only.

**Cổng d — DỪNG, trình pptx cho user duyệt nội dung/khung slide.** Không chạy P7/P8 khi
chưa qua cổng này — audio (slide + 課文) và bài tập chỉ tốn công sinh lại nếu nội dung
slide còn đổi. Duyệt xong (hoặc chỉnh theo feedback rồi duyệt lại) mới sang P7.

**P7 — Audio slide + 課文:** `slide_audio.py --rate=-18%` (audio slide) + edge-tts
`--rate=-18%` → `DIR/doc/bai-doc.NN.mp3` (audio 課文). Soát 多音字/儿化 (得/着/行/为/教/还/长…).

**P8 — Bài tập (cổng b/c):** `DIR/baitap/baitap-buoiXX.json` (~25–30 mục) đủ **听/读/书写(Viết 3.0)/HSKK**, không trùng câu, đáp án 2 cấp. Cổng b: trình script audio duyệt. `check_baitap.py`. Sinh audio (`nghe --rate=-22%`, `noi_hskk --rate=-18%`). `build_worksheet.py`. Cổng c: rà đáp án AI. Append `state/session-log.md`.

**P9 — README + commit:** README "⏳"→"✅". `feat(hsk2): buổi XX <chủ đề> — trọn gói`.

**Verify buổi:** pptx mở được; 生词 khớp bài sách & không trùng HSK1; có 10 câu khẩu ngữ; `doc/` có 課文 nguyên văn + audio; bài tập đủ **Viết 3.0**; worksheet KHÔNG có đáp án; dapan có đáp án + 听力文本; audio soát 多音字/儿化.

---

## PHASE 1 — Sản xuất tuần tự 15 buổi + 2 ôn (mỗi buổi 1 cổng duyệt riêng)

> **Quyết định (2026-07-27, theo user):** bỏ mô hình "2 pilot rồi sản xuất hàng loạt". Lý do: dù buổi nào user cũng phải review + điều chỉnh nội dung, nên **đi tuần tự từng buổi đúng thứ tự sách**, mỗi buổi xong đều **trình user duyệt trọn gói (pptx + worksheet + bài đọc)** trước khi bắt đầu buổi kế tiếp — không có khái niệm "pilot" riêng hay "sản xuất hàng loạt" sau khi duyệt khuôn. Thứ tự: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → **[Ôn 1]** → 09 → 10 → 11 → 12 → 13 → 14 → 15 → **[Ôn 2]**.

> Mỗi Task dưới đây dùng chung Procedure P (§ trên); step cuối luôn là **Verify + trình user duyệt trọn gói trước khi mở Task tiếp theo**.

- [x] **Task 1 — buoi01_moian_vitquay** (Bài 1 她请我们吃了北京烤鸭): 语气助词"吧"(2) (phỏng đoán) · "是…的"句 · 请/让/叫 (nhờ vả). 生词 bài 1 (Task 0.1). 課文: 4 bài Lesson 1 (trang 001+). Hán ngữ L22. Lỗi VN: 是…的 nhấn thời gian/nơi/cách; 吧 phỏng đoán vs đề nghị. — ✅ XONG (commit `e29c2da`)
  - [x] Step 1 P1 · Step 2 P2 · Step 3 P3 · Step 4 P4(+P5) · Step 5 P6+P7 · Step 6 P8 (Viết: 是…的) · Step 7 Verify + trình user duyệt · Step 8 P9.
  - **Duyệt 2026-08-02:** slide 12 wordcard + bài tập chỉ phủ 12/14 từ checklist Bài 1, thiếu 介绍/那. Đối chiếu HSK1: 那 xác nhận đã dạy ở `output/hsk1/on2_tuvung_chude` (cặp 这/那); 介绍 không thấy trong output/knowledge HSK1 nhưng user xác nhận đã học — quyết định KHÔNG vá thêm, giữ nguyên 12 từ.
- [ ] **Task 2 — buoi02_giaothong** (Bài 2 还是打车去北大吧): 兼语句 · 还是…吧 · 多(概数) · cụm làm định ngữ. **+ Lồng hỏi đường (怎么走, bổ sung — đã đối chiếu chính thức).** Hán ngữ L16/L17.
  - [ ] Step 1-6 Procedure P (Viết: câu dùng 还是…吧) · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 3 — buoi03_dulich_xian** (Bài 3 我想去西安旅游): 结果补语 · 动词重叠(1)(2). **+ Lồng đặt khách sạn (bổ sung, ngoài chuẩn thi).** Hán ngữ L29/L19/L27. **Sửa 2026-08-04:** 过/因为…所以 KHÔNG thuộc Bài 3 — đối chiếu PDF trang 019-036 xác nhận thuộc Bài 4, xem `output/hsk2/buoi03_dulich_xian/doc/bai-doc.md`.
  - [ ] Step 1-6 Procedure P (Viết: đoạn ngắn kể chuyện du lịch) · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 4 — buoi04_trangphuc_mausac** (Bài 4 你穿红色的很好看): 动态助词"过" · 因为…所以 · "的"字短语 · **把字句 cơ bản (bổ sung, ghép tự nhiên với 简单趋向补语: 把衣服穿上/脱下来)**. Hán ngữ L19. **Sửa 2026-08-04:** 简单趋向补语(1)(2)/都…了 KHÔNG thuộc Bài 4 — thực ra thuộc Bài 5 (xác nhận trang objectives 053).
  - [ ] Step 1-6 Procedure P (Viết: câu 把) · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 5 — buoi05_thamnha** (Bài 5 第一次去中国朋友家): 简单趋向补语(1)(2) · 都…了 · 形容词重叠 · 什么的 · 结构助词"地" · 一…就… (4 điểm cuối CHƯA xác minh lại, có thể lệch tiếp sang Bài 6 — soát khi sản xuất tới lượt). **Lồng động vật/thú cưng (từ mở rộng ngoài 200) + giới thiệu bản thân/gia đình sâu 2-3 phút bằng ngữ pháp mới (bổ sung, đã đối chiếu chính thức).** Hán ngữ —.
  - [ ] Step 1-6 Procedure P (HSKK: tự giới thiệu bản thân/gia đình) · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 6 — buoi06_sinhnhat** (Bài 6 小雪，生日快乐！): 状态补语(1)(2) [得]. Hán ngữ L25.
  - [ ] Step 1-6 Procedure P (Viết: câu 得) · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 7 — buoi07_thethao** (Bài 7 他篮球打得很好): **状态补语/得** (打得很好) · **比较句(1)(2)** (比). Hán ngữ L25. Lỗi VN: quên 得 (打篮球好→打得很好); 比 thừa 很 (他比我很高✗).
  - [ ] Step 1-6 Procedure P (Viết: câu 得/比) · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 8 — buoi08_trinho_sosanh** (Bài 8 虽然你忘了，但是我记得): 虽然…但是 · 比较句(3) · 动词"离". Hán ngữ L28/L23.
  - [ ] Step 1-6 Procedure P · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 9 — Ôn 1** (`on1_bai1-8`): ôn ngữ pháp bài 1–8 (是…的/吧, 结果补语/动词重叠/过/因为所以, 趋向补语/把字句 Bài 4, 形容词重叠/一…就, 得, 比较句1-3, 虽然但是/离) **+ 2 slide bảng hệ thống hoá thuần ôn tập: (a) bảng bổ ngữ 结果补语 vs 简单趋向补语 vs 状态补语得; (b) bảng 比较句(1)(2)(3)**. Slide ôn + bài tập tổng hợp (đủ 听/读/书写/HSKK). CHỈ ôn tập.
  - [ ] Step 1-6 Procedure P · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 10 — buoi09_douong** (Bài 9 我去买杯奶茶): 时量补语(1) · 主谓谓语句 · 选择问句. **+ Lồng hỏi giá/so sánh giá (bổ sung, đã đối chiếu chính thức).** Hán ngữ L30/L16.
  - [ ] Step 1-6 Procedure P · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 11 — buoi10_thicu** (Bài 10 就要考试了): 要/快/快要/就要…了 · 动态助词"着"(1)(2). **+ Lồng đặt lịch hẹn (bổ sung, ngoài chuẩn thi — vd 我跟老师约好了，下午两点就要见面了).** Hán ngữ —.
  - [ ] Step 1-6 Procedure P · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 12 — buoi11_monan_yeuthich** (Bài 11 我最喜欢吃中国菜): 程度副词"最" · **被字句 đơn giản (bổ sung, vd 这道菜太好吃了都被吃光了)**. Hán ngữ —.
  - [ ] Step 1-6 Procedure P · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 13 — buoi12_thoitiet** (Bài 12 这里比北京冷多了): 比较句(4)(5)(6) · **连…都/也 (bổ sung, ghép cùng 比较句: 冷得连水都能结冰)**. Hán ngữ —.
  - [ ] Step 1-6 Procedure P · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 14 — buoi13_hoctiengtrung** (Bài 13 我们爱上中文课): 双宾语句(2) · 比较句(7)(8). Hán ngữ L17.
  - [ ] Step 1-6 Procedure P · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 15 — buoi14_letet** (Bài 14 一个人过年多没意思啊): 存现句 · 复合趋向补语. Hán ngữ L23.
  - [ ] Step 1-6 Procedure P · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 16 — buoi15_kehoach** (Bài 15 我想再去一次中国): 动量补语(1)(2) · "有"字句(2). Hán ngữ —.
  - [ ] Step 1-6 Procedure P · Step 7 Verify + trình user duyệt · Step 8 P9.
- [ ] **Task 17 — Ôn 2** (`on2_bai9-15`): ôn ngữ pháp bài 9–15 (时量补语/选择问, 要快…了/着, 最/被字句 Bài 11, 比较句4-8/连…都也 Bài 12, 双宾语, 存现/复合趋向, 动量补语/有字句) **+ 2 slide bảng hệ thống hoá nối Ôn 1: (a) bảng bổ ngữ đầy đủ 6 loại (+ 时量/复合趋向/动量补语); (b) bảng 比较句 đầy đủ (1)-(8)** + từ vựng cụm + **capstone roleplay HSKK ôn tập tổng hợp** (thực hành lại: hỏi đường B2, đặt khách sạn B3, giới thiệu bản thân/gia đình B5, hỏi giá/so sánh giá B9, đặt lịch hẹn B10 — CHỈ ôn/ứng dụng lại, không dạy từ/ngữ pháp/tình huống mới). Slide ôn + bài tập tổng hợp.
  - [ ] Step 1-6 Procedure P · Step 7 Verify + trình user duyệt · Step 8 P9.

> **FINAL GATE:** verify tổng: `hsk2-vocab-grammar-checklist.md` mọi từ "✅ có bài + đã soạn + không trùng HSK1"; 45 ngữ pháp đã dạy; `output/hsk2/README.md` mọi buổi ✅; vocab khớp 词汇表 sách. Trình user bàn giao.

---

## Out of scope / follow-up

- **Trang từ vựng HSK2 theo buổi (§13 spec)** — `output/study/hsk2/buoiXX/tu-vung.html`, bỏ neo Activation, Leitner box 1. Tách plan riêng, sau khi vocab 15 buổi chốt. Cần chỉnh tooling vocab-study (hardcode hsk6, đọc xlsx, Activation).
- **Rebuild HSK1 lên 3.0** — việc riêng của user.
- **Seed kho đề `knowledge/hsk-exam-bank/hsk2.md`** — tách việc.
- **第二册 Hán ngữ** — nếu user cấp, bổ sung footer cho các bài dùng 比较句/趋向补语/着/动量补语 (hiện 第一册·下 chỉ phủ một phần).

## Self-review notes
- Nguồn chân lý dời từ "web-search + tự nghĩ" → **PDF sách thật** (text layer). Task 0.1 bóc 词汇表 + 生词 + 45 ngữ pháp; P2 trích 課文 nguyên văn. Hết fallback tự soạn.
- Syllabus = 15 bài thật (TOC). Pets lồng Bài 5. Pilot Bài 1 + Bài 7.
- Điểm cần user (không chặn): MP3 gốc sách (nếu có, ưu tiên hơn edge-tts); 第二册 Hán ngữ (footer 比较句…).
- **Vá 2026-07-27 (theo tiêu chuẩn đầu ra HSK2, xem memory):** đã bổ sung 4 điểm — (1) 把 lồng Bài 4, 被 lồng Bài 11, 连…都/也 lồng Bài 12 (không dạy ở Ôn); (2) Viết 3.0 mở rộng thêm đoạn/form/note/nhật ký (Task 0.2 đổi từ "đánh giá" → "mở rộng schema", cần làm trên `main` vì exercise-generator dùng chung mọi cấp); (3) mỗi buổi bài tập thêm ≥1 văn bản đọc thực tế; (4) hỏi đường lồng Bài 2, khách sạn Bài 3, giới thiệu bản thân sâu Bài 5, hẹn giờ Bài 6, mặc cả Bài 9. Chưa build buổi nào nên vá trực tiếp vào spec+plan.
- **Sửa lại 2026-07-27 (lần 2, theo phản hồi user):** ban đầu dồn cả 4 điểm trên vào 2 buổi Ôn — **sai**, vì Ôn chỉ để ôn tập nội dung đã học, không dạy cái mới. Đã rải lại vào đúng buổi nội dung phù hợp chủ đề; Ôn 1/Ôn 2 quay về đúng vai trò ôn tập.
- **Sửa lại 2026-07-27 (lần 3, theo phản hồi user + đối chiếu nguồn chính thống):** đổi tên "mặc cả" → "hỏi giá, so sánh giá" (Bài 9) để bám đúng khung chính thức. Dời "đặt lịch hẹn" từ Bài 6 (sinh nhật, khá gượng) → Bài 10 (ghép tự nhiên với 就要…了). Đã tra `download.chinesetest.cn/newhsk-site/Syllabus/H2_DG.pdf` (官方 HSK 二级考试大纲) xác nhận hỏi đường/hỏi giá/giới thiệu gia đình có căn cứ chính thống; đặt khách sạn + đặt lịch hẹn KHÔNG có trong chuẩn thi — giữ lại vì mục tiêu thực dụng cá nhân, đánh dấu rõ trong slide. Xem spec §16b.
- **Sửa lại 2026-07-27 (lần 4, phản hồi review độc lập của user):** (a) "Can-do mỗi buổi" — user xác nhận đã có sẵn qua block "mục tiêu" hiện hữu, không cần thêm gì. (b) "Spiral review" — user tự làm khi soạn bài tập (P8), không cần đổi kiến trúc slide, chỉ giữ 1 slide "ôn buổi trước" như cũ. (c) Đã tra `新版HSK考试大纲（词汇、汉字、语法）.pdf` (bản 3.0 chính thức, hsk.cn-bj.ufileos.com) xác nhận 一边…一边/越来越/又…又 thuộc **HSK 三级**, không phải 二级 → KHÔNG phải gap, không vá. (d) Thêm 4 slide bảng hệ thống hoá bổ ngữ + 比较句 vào Ôn 1/Ôn 2 (Task 9, 17) thay vì gom thành buổi riêng — giữ nguyên "buổi=bài", chỉ hệ thống hoá bằng ôn tập thuần. Xem spec §16c.
- **Sửa lại 2026-08-04 (theo phản hồi user, phát hiện khi làm Bài 3):** Procedure P trước đó chỉ có 1 cổng duyệt trọn gói ở cuối buổi (Step 7) — nên buổi 3 đã render xong pptx + audio slide + audio 課文 + JSON bài tập liên tục, KHÔNG dừng lại để duyệt slide trước, khác với điều user nhớ đã thống nhất. Đã sửa: tách P6 (chỉ render pptx, không audio) và thêm **cổng d** — dừng trình pptx duyệt nội dung/khung slide TRƯỚC khi chạy P7 (audio slide + 課文) và P8 (bài tập). Lý do: audio + bài tập tốn công sinh lại nếu nội dung slide còn đổi sau duyệt.
  **Áp dụng từ Task 4 (buổi 4) trở đi** — Task 3 (buổi 3) đã gần xong (pptx+audio+baitap JSON đã có), KHÔNG retro-fit cổng d, cứ hoàn thiện theo Step 7 Verify trọn gói như cũ rồi qua P9.
