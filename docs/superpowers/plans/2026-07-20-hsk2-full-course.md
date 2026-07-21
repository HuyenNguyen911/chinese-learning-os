# HSK2 (chuẩn 3.0) Full Course Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây bộ HSK2 chuẩn **3.0** — **15 buổi (bám sát 15 bài New HSK Course 2) + 2 ôn**, trọn gói slide/audio/bài tập(có Viết 3.0)/bài đọc; 生词 + 課文 + 45 ngữ pháp **trích trực tiếp từ `raw/New HSK Course 2.pdf`** (có text layer); footer tham khảo Hán ngữ 第一册·下; không trùng từ HSK1.

**Architecture:** Pipeline nội dung trên tooling vault (teaching-coach, exercise-generator, edge-tts). Mỗi buổi = 1 folder `output/hsk2/buoiXX_<slug>/` với `slide/` · `baitap/` · `doc/`. Buổi = 1 bài sách. Quy trình mỗi buổi giống nhau (Procedure P). Làm 2 pilot (Bài 1 + Bài 7) chốt khuôn, rồi nhân bản.

**Tech Stack:** Python 3.12 (pypdf, python-pptx, Pillow, pypinyin, python-docx), edge-tts, build_deck.py / slide_audio.py / fetch_images.py (teaching-coach), build_worksheet.py / check_baitap.py (exercise-generator), gen_stroke_gif.py (tuỳ chọn, tái dùng HSK1).

**Spec:** `docs/superpowers/specs/2026-07-20-hsk2-full-course-design.md`. **Mục lục sách (nguồn chân lý syllabus):** `docs/superpowers/specs/hsk2-new-hsk-course-2-toc.md`.

## Global Constraints

- **Python:** `PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"`. Chạy từ gốc repo `c:/Tài liệu/ai-vault/CHINESE`.
- **NGUỒN CHÂN LÝ = sách:** 生词/課文/45 ngữ pháp trích từ `raw/New HSK Course 2.pdf` (text layer sạch — dùng pypdf, KHÔNG bịa, KHÔNG web-search). Không tự nghĩ từ vựng.
- **Buổi = bài:** 15 buổi ↔ 15 bài sách (mục lục TOC). Ôn: `on1_bai1-8` (sau bài 8), `on2_bai9-15` (sau bài 15).
- **CHỐNG TRÙNG HSK1 (cứng):** mọi 生词 loại/đánh dấu từ đã có trong 150 từ HSK1 (Task 0.1).
- **Động vật/thú cưng:** lồng **từ mở rộng** vào Bài 5 (thăm nhà bạn), đánh dấu "ngoài 200 từ sách". Không thêm buổi.
- **Mọi từ/câu tiếng Trung** đủ **汉字 + pinyin + nghĩa Việt**.
- **Thứ tự block slide:** `title → ôn buổi trước → mục tiêu → 生词 → ngữ pháp (小语讲堂) → 10 câu khẩu ngữ → hội thoại/課文 → bài đọc → footer Hán ngữ 第一册·下 → lỗi người Việt → preview bài tập`. KHÔNG block ngữ âm.
- **Bài tập đủ 4 phần 3.0:** 听 · 读 · **书写/Viết** (sắp câu, điền chữ, viết câu ngắn) · HSKK.
- **Audio đọc chậm:** slide `--rate=-18%`; baitap `nghe --rate=-22%`, `noi_hskk --rate=-18%`. Giọng chính `zh-CN-XiaoxiaoNeural`. (Nếu user cấp MP3 gốc sách → ưu tiên.)
- **Cổng duyệt:** (a) text 課文 trích từ PDF → trình user duyệt; (b) script 听力/HSKK trình user trước khi sinh MP3; (c) `check_baitap.py` + rà đáp án AI; (d) soát 多音字/儿化 mọi audio.
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

### Task 0.1: Trích 词汇表 + 45 ngữ pháp từ sách + cờ trùng HSK1

**Files:** Create `docs/superpowers/plans/hsk2-vocab-grammar-checklist.md`

- [ ] **Step 1: Bóc 词汇表 tổng (trang 141) + 生词 từng bài từ PDF**
```bash
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
"$PY" -c "import pypdf,sys;sys.stdout.reconfigure(encoding='utf-8');r=pypdf.PdfReader('raw/New HSK Course 2.pdf');[print(f'==P{i+1}==',(r.pages[i].extract_text() or '')) for i in range(140,164)]"
```
Trích bảng `汉字 | pinyin | 词性 | nghĩa | bài`. Đối chiếu 生词 đầu mỗi bài (bóc trang tương ứng theo TOC) để gán từ ↔ bài.

- [ ] **Step 2: Trích 150 từ HSK1 để loại trùng**
```bash
grep -ho '"hz": *"[^"]*"' output/hsk1/*/slide/*.json | sort -u
```

- [ ] **Step 3: Viết checklist** — bảng vocab (thêm cột `trùng HSK1?`) + bảng 45 ngữ pháp `điểm 小语讲堂 | bài`. Đánh dấu từ mở rộng động vật/thú cưng (Bài 5).

- [ ] **Step 4: Verify** — tổng ≈ 200 (+扩展) khớp 词汇表; mọi từ có bài; 45 ngữ pháp đủ; không từ trùng HSK1 lọt vào cột 生词 chính.

- [ ] **Step 5: Commit** `docs(hsk2): trích 200 từ + 45 ngữ pháp từ New HSK Course 2 + cờ trùng HSK1`

### Task 0.2: Đánh giá schema Viết (书写) 3.0 trong exercise-generator

**Files:** Read `.claude/skills/exercise-generator/worksheet/schema.md`, `build_worksheet.py`

- [ ] **Step 1:** Rà dạng mục hỗ trợ; xác định dạng dùng cho Viết 3.0 (连词成句, điền chữ, viết câu theo mẫu/tranh).
- [ ] **Step 2:** Đủ → map dạng mục → phần Viết (không sửa skill). Thiếu → **cổng duyệt user** đề xuất bổ sung dạng mục. Ghi vào README kỹ thuật.
- [ ] **Step 3:** Commit nếu có ghi chú.

### Task 0.3: README syllabus (source of truth)

**Files:** Create `output/hsk2/README.md`

- [ ] **Step 1:** Bảng 15 buổi + 2 ôn từ §4 spec: `# | Bài (课文) | Folder | Ngữ pháp (小语讲堂) | Chủ đề | Hán ngữ 第一册·下`. Header ghi rõ chuẩn 3.0, sách chính New HSK Course 2 (郭风岚/FLTRP), tham khảo Hán ngữ 第一册·下. Mục "Ghi chú kỹ thuật" (schema Viết, GIF nét). Buổi chưa làm "⏳".
- [ ] **Step 2: Verify** — folder đúng convention; ôn 1 sau bài 8, ôn 2 sau bài 15.
- [ ] **Step 3: Commit**

---

## PROCEDURE P — Quy trình sản xuất 1 buổi

> Param mỗi buổi: `XX`, `SLUG`, `DIR=output/hsk2/buoiXX_SLUG`; **bài sách số N**; 生词 (Task 0.1, đã lọc trùng HSK1); ngữ pháp 小语讲堂 (TOC); 課文 sách; dòng Hán ngữ 第一册·下; lỗi người Việt.

**P1 — Master Teacher:** Đóng vai Master Chinese Teacher. Soạn: giải thích 小语讲堂 đúng bản chất; 生词 bài (đủ 汉字/pinyin/nghĩa, đã lọc trùng HSK1); ví dụ khẩu ngữ; **10 câu khẩu ngữ dùng-ngay**; hội thoại; 2–3 lỗi người Việt (đọc `common-vietnamese-mistakes.md`).

**P2 — 課文 (cổng a):** Trích **nguyên văn** 課文 bài N từ `raw/New HSK Course 2.pdf` (pypdf, theo trang trong TOC). Chọn 課文 phù hợp (đối thoại chính + bài tự sự). **Trình user duyệt text đã trích** → ghi `DIR/doc/bai-doc.md` (汉字 nguyên văn + pinyin + dịch Việt).

**P3 — Experience Designer:** Map → `DIR/slide/buoiXX.json` (schema teaching-coach, đúng thứ tự block). Footer Hán ngữ 第一册·下 (bullets/reading); lỗi VN (table). Action title + ghost-deck test.

**P4 — Ảnh:** `DIR/slide/buoiXX-images.json` → `fetch_images.py`. Expected `DONE: N/N`.

**P5 — GIF nét (tuỳ chọn):** chữ mới khó → `gen_stroke_gif.py`.

**P6 — Render slide + audio:** `build_deck.py` + `slide_audio.py --rate=-18%`. Soát 多音字/儿化 (得/着/行/为/教/还/长…).

**P7 — Audio 課文:** edge-tts `--rate=-18%` → `DIR/doc/bai-doc.NN.mp3`. Soát như P6.

**P8 — Bài tập (cổng b/c):** `DIR/baitap/baitap-buoiXX.json` (~25–30 mục) đủ **听/读/书写(Viết 3.0)/HSKK**, không trùng câu, đáp án 2 cấp. Cổng b: trình script audio duyệt. `check_baitap.py`. Sinh audio (`nghe --rate=-22%`, `noi_hskk --rate=-18%`). `build_worksheet.py`. Cổng c: rà đáp án AI. Append `state/session-log.md`.

**P9 — README + commit:** README "⏳"→"✅". `feat(hsk2): buổi XX <chủ đề> — trọn gói`.

**Verify buổi:** pptx mở được; 生词 khớp bài sách & không trùng HSK1; có 10 câu khẩu ngữ; `doc/` có 課文 nguyên văn + audio; bài tập đủ **Viết 3.0**; worksheet KHÔNG có đáp án; dapan có đáp án + 听力文本; audio soát 多音字/儿化.

---

## PHASE 1 — Pilot Bài 1

### Task 1: buoi01_moian_vitquay (Bài 1 她请我们吃了北京烤鸭)
**Param:** `XX=01`, `SLUG=moian_vitquay`. Ngữ pháp: 语气助词"吧"(2) (phỏng đoán) · "是…的"句 · 请/让/叫 (biểu đạt nhờ vả). 生词: bài 1 (Task 0.1). 課文: 4 bài của Lesson 1 (trang 001+). Hán ngữ: L22 请…. Lỗi VN: 是…的 nhấn thời gian/nơi/cách; 吧 phỏng đoán vs đề nghị.
- [ ] Step 1 P1 · Step 2 P2 · Step 3 P3 · Step 4 P4(+P5) · Step 5 P6+P7 · Step 6 P8 (Viết: 是…的) · Step 7 Verify · Step 8 P9.

## PHASE 2 — Pilot Bài 7

### Task 2: buoi07_thethao (Bài 7 他篮球打得很好)
**Param:** `XX=07`, `SLUG=thethao`. Ngữ pháp: **状态补语/得** (打得很好) · **比较句(1)(2)** (比). 生词: bài 7 (thể thao: 篮球/踢/打/运动…). 課文: Lesson 7 (trang 064+). Hán ngữ: L25 状态补语得. Lỗi VN: quên 得 (打篮球好→打得很好); 比 thừa 很 (他比我很高✗).
- [ ] Step 1 P1 · Step 2 P2 · Step 3 P3 · Step 4 P4(+P5) · Step 5 P6+P7 · Step 6 P8 (Viết: câu 得/比) · Step 7 Verify · Step 8 P9.

> **REVIEW GATE:** Sau Task 1+2, trình user 2 pilot (pptx + worksheet + bài đọc). Duyệt khuôn → sản xuất phần còn lại.

---

## PHASE 3 — 13 buổi còn lại + 2 ôn

> Procedure P với Param mỗi bài (ngữ pháp = 小语讲堂 bài đó, 生词/課文 từ PDF). Thứ tự: 02 → 03 → 04 → 05 → 06 → 08 → **[Ôn 1]** → 09 → 10 → 11 → 12 → 13 → 14 → 15 → **[Ôn 2]**.

- [ ] **Task 3 — buoi02_giaothong** (Bài 2 还是打车去北大吧): 兼语句 · 还是…吧 · 多(概数) · cụm làm định ngữ. Hán ngữ L16/L17.
- [ ] **Task 4 — buoi03_dulich_xian** (Bài 3 我想去西安旅游): 结果补语 · 动词重叠(1)(2) · 动态助词"过" · 因为…所以. Hán ngữ L29/L19/L27.
- [ ] **Task 5 — buoi04_trangphuc_mausac** (Bài 4 你穿红色的很好看): "的"字短语 · 简单趋向补语(1)(2) · 都…了. Hán ngữ L19.
- [ ] **Task 6 — buoi05_thamnha** (Bài 5 第一次去中国朋友家): 形容词重叠 · 什么的 · 结构助词"地" · 一…就…. **Lồng động vật/thú cưng (từ mở rộng ngoài 200).** Hán ngữ —.
- [ ] **Task 7 — buoi06_sinhnhat** (Bài 6 小雪，生日快乐！): 状态补语(1)(2) [得]. Hán ngữ L25.
- [ ] **Task 8 — buoi08_trinho_sosanh** (Bài 8 虽然你忘了，但是我记得): 虽然…但是 · 比较句(3) · 动词"离". Hán ngữ L28/L23.
- [ ] **Task 9 — Ôn 1** (`on1_bai1-8`): ôn ngữ pháp bài 1–8 (是…的/吧, 结果补语/动词重叠/过/因为所以, 趋向补语, 形容词重叠/一…就, 得, 比较句1-3, 虽然但是/离). Slide ôn + bài tập tổng hợp (đủ 听/读/书写/HSKK). Không 生词 mới.
- [ ] **Task 10 — buoi09_douong** (Bài 9 我去买杯奶茶): 时量补语(1) · 主谓谓语句 · 选择问句. Hán ngữ L30/L16.
- [ ] **Task 11 — buoi10_thicu** (Bài 10 就要考试了): 要/快/快要/就要…了 · 动态助词"着"(1)(2). Hán ngữ —.
- [ ] **Task 12 — buoi11_monan_yeuthich** (Bài 11 我最喜欢吃中国菜): 程度副词"最". Hán ngữ —.
- [ ] **Task 13 — buoi12_thoitiet** (Bài 12 这里比北京冷多了): 比较句(4)(5)(6). Hán ngữ —.
- [ ] **Task 14 — buoi13_hoctiengtrung** (Bài 13 我们爱上中文课): 双宾语句(2) · 比较句(7)(8). Hán ngữ L17.
- [ ] **Task 15 — buoi14_letet** (Bài 14 一个人过年多没意思啊): 存现句 · 复合趋向补语. Hán ngữ L23.
- [ ] **Task 16 — buoi15_kehoach** (Bài 15 我想再去一次中国): 动量补语(1)(2) · "有"字句(2). Hán ngữ —.
- [ ] **Task 17 — Ôn 2** (`on2_bai9-15`): ôn ngữ pháp bài 9–15 (时量补语/选择问, 要快…了/着, 最, 比较句4-8, 双宾语, 存现/复合趋向, 动量补语/有字句) + từ vựng cụm + capstone hội thoại. Slide ôn + bài tập tổng hợp.

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
- Điểm cần user (không chặn): MP3 gốc sách (nếu có, ưu tiên hơn edge-tts); 第二册 Hán ngữ (footer 比较句…); xác nhận schema Viết (Task 0.2).
