# HSK1 Full Course Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hoàn thiện bộ HSK1 12 buổi — sản xuất 9 buổi mới (3 nền tảng có GIF + 6 chủ đề), trọn gói slide/audio/bài tập/bài đọc, đồng bộ đánh số syllabus.

**Architecture:** Pipeline nội dung dựa trên tooling có sẵn của vault. Mỗi buổi = 1 folder `output/hsk1/buoiXX_<slug>/` với `slide/` (teaching-coach `build_deck.py`), `baitap/` (exercise-generator `build_worksheet.py`), `doc/` (bài đọc HSK SC1 + audio edge-tts). Quy trình mỗi buổi giống nhau (Procedure P) — chỉ khác dữ liệu (từ vựng/ngữ pháp/课文). Làm 2 pilot trước để chốt khuôn, rồi nhân bản.

**Tech Stack:** Python 3.12 (python-pptx, Pillow, pypinyin, openpyxl, python-docx), edge-tts, build_deck.py / slide_audio.py / fetch_images.py (teaching-coach), build_worksheet.py / check_baitap.py (exercise-generator).

**Spec:** `docs/superpowers/specs/2026-07-19-hsk1-full-course-design.md` — nguồn chân lý về syllabus (§4), vocab lõi mỗi buổi (§5), cấu trúc slide (§6), GIF (§7), bài đọc (§8), Hán ngữ mapping (§9), pipeline (§10), đặt tên (§11).

## Global Constraints

- **Python:** `PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"`. Chạy mọi lệnh **từ gốc repo** `c:/Tài liệu/ai-vault/CHINESE`.
- **Đánh số:** tất cả 12 buổi dùng prefix 2 chữ số `buoiXX` theo vị trí syllabus (§11). Folder mới: `buoi01_nguam`, `buoi02_daitu_chaohoi`, `buoi03_so_thoigian_diadiem`, `buoi04_giadinh`, `buoi05_nghe_quoctich`, `buoi07_anuong`, `buoi08_nha_vitri`, `buoi09_sothich`, `buoi11_muasam_tinhtu`.
- **Mọi từ/câu tiếng Trung mới** phải có đủ **汉字 + pinyin + nghĩa Việt**.
- **Lượng từ mới:** 8–12 từ/buổi (nhịp người mới). Ví dụ **khẩu ngữ, đời thường, thông dụng** — không sáo rỗng.
- **Thứ tự block slide (§6):** `title → ôn buổi trước → mục tiêu → 生词 → ngữ pháp → 10 câu khẩu ngữ → hội thoại/课文 → bài đọc → footer đối chiếu Hán ngữ Q1 → lỗi người Việt → preview bài tập`. Buổi 1 (ngữ âm) không có "10 câu khẩu ngữ" — thay bằng luyện âm.
- **Audio đọc chậm:** slide `slide_audio.py --rate=-18%`; baitap `nghe` `--rate=-25%`, `noi_hskk` `--rate=-18%`. KHÔNG để +0%. Giọng chính `zh-CN-XiaoxiaoNeural`.
- **Cổng duyệt bắt buộc:** (a) text 课文 HSK SC1 web-search đối chiếu bản gốc trước khi dùng; (b) script 听力/HSKK trình text cho user trước khi sinh MP3; (c) đáp án bài tập kiểm tra (`check_baitap.py`) trước khi giao; (d) soát phát âm 多音字/儿化 mọi audio trước khi giao.
- **Không tái soạn** nội dung dạy buổi existing (06/10/12) — chỉ đổi tên/nhãn.
- **Console Windows:** khi in 中文 để debug, đặt `PYTHONIOENCODING=utf-8`.
- **Git:** commit sau mỗi task với message tiếng Việt + trailer `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

---

## File Structure

```
output/hsk1/
  README.md                          # [Task 0.4] bảng syllabus 12 buổi + 2 ôn (source of truth)
  buoi06_.../ buoi10_.../ buoi12_.../ # [Task 0.3] existing đổi tên
  buoiXX_<slug>/                      # mỗi buổi mới:
    slide/
      buoiXX.json                     # JSON teaching-coach (mình soạn)
      buoiXX-images.json              # manifest fetch ảnh {out_dir, images[]}
      Buoi-XX-<Ten>.pptx              # render
      assets/                         # *.jpg (fetch), *.gif (foundation), audio/slideNN.mp3
    baitap/
      baitap-buoiXX.json              # JSON exercise-generator (mình soạn)
      hocsinh/worksheet.docx + audio/*.mp3
      dapan/dapan.docx
    doc/
      bai-doc-hsksc1.md               # 课文 HSK SC1: hán+pinyin+dịch
      bai-doc-hsksc1.NN.mp3           # audio edge-tts
docs/superpowers/plans/hsk1-150-checklist.md   # [Task 0.1] checklist phủ 150 từ
scripts/hsk1/gen_tone_gif.py         # [Task 0.2] sinh GIF thanh điệu
scripts/hsk1/gen_stroke_gif.py       # [Task 0.2] sinh GIF thứ tự nét
```

Vocab-study phase (§14 spec) **tách plan riêng** — xem "Out of scope / follow-up" cuối file.

---

## PHASE 0 — Infrastructure

### Task 0.1: Checklist phủ 150 từ HSK1

**Files:**
- Create: `docs/superpowers/plans/hsk1-150-checklist.md`

**Interfaces:**
- Produces: bảng 150 từ HSK1 ↔ buổi phụ trách, dùng làm checklist phủ từ cho mọi task buổi.

- [ ] **Step 1: Lấy danh sách 150 từ HSK1 chính thức**

WebSearch "HSK 1 vocabulary list 150 words official" → lấy danh sách chuẩn (150 từ, có 汉字 + pinyin). Đối chiếu tối thiểu 2 nguồn (vd chinesetest.cn / hsk.academy / HSK Standard Course 1 word index) cho khớp.

- [ ] **Step 2: Trích vocab đã có từ buổi existing**

Run:
```bash
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
grep -ho '"hz": *"[^"]*"' output/hsk1/buoi1*/slide/*.json output/hsk1/buoi2*/slide/buoi2.json output/hsk1/buoi3*/slide/buoi3.json
```
Expected: danh sách 汉字 của buổi 6/10/12 (năng nguyện, lượng từ/màu, thời tiết).

- [ ] **Step 3: Viết checklist**

Bảng markdown: cột `汉字 | pinyin | nghĩa | buổi phụ trách (theo spec §4/§5) | trạng thái`. Mỗi từ gán đúng 1 buổi (nền tảng/existing/mới). Đánh dấu từ nào nằm trong nền tảng raw (CĐ1/CĐ2) → gán buổi 02/03.

- [ ] **Step 4: Verify — đủ 150, không trùng, không sót**

Đếm số dòng = 150. Không từ nào gán 2 buổi (trừ từ ôn lại có chủ đích, ghi rõ "ôn"). Mọi từ có buổi phụ trách. Nếu lệch (thiếu/thừa) → chỉnh phân bổ vocab lõi trong plan tương ứng và ghi chú.

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/plans/hsk1-150-checklist.md
git commit -m "docs(hsk1): checklist phủ 150 từ HSK1 theo buổi"
```

### Task 0.2: Spike — GIF động trong PPTX + script sinh GIF

**Files:**
- Create: `scripts/hsk1/gen_tone_gif.py`, `scripts/hsk1/gen_stroke_gif.py`
- Create (tạm): `scratchpad` test deck

**Interfaces:**
- Produces: `gen_tone_gif.py` (sinh GIF đường cong 5 mức thanh điệu), `gen_stroke_gif.py` (sinh GIF thứ tự nét từ dữ liệu Make Me a Hanzi). Kết luận: GIF nhúng qua key `image` có **phát động** trong PowerPoint không → nếu không, chốt fallback.

- [ ] **Step 1: Viết `gen_tone_gif.py`**

Script Pillow: vẽ đường cong thanh điệu (1: ngang cao; 2: đi lên; 3: xuống-lên; 4: đi xuống; nhẹ: chấm) trên lưới 5 mức, xuất GIF động (nhiều frame vẽ dần đường + con trỏ chạy). Đầu file `sys.stdout.reconfigure(encoding="utf-8")`. CLI: `gen_tone_gif.py <tone:1-5> <out.gif>`.

- [ ] **Step 2: Viết `gen_stroke_gif.py`**

Tải dữ liệu nét Make Me a Hanzi (`graphics.txt`, cache vào `scripts/hsk1/_src/`), với 1 chữ → render từng nét thành frame → GIF động. CLI: `gen_stroke_gif.py <hanzi> <out.gif>`. (Nếu build_hanzi.py của vocab-study đã cache dữ liệu ở `.claude/skills/vocab-study/data/_src/` thì tái dùng.)

- [ ] **Step 3: Sinh mẫu + nhúng vào deck test**

```bash
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
mkdir -p output/hsk1/_spike/assets
"$PY" scripts/hsk1/gen_tone_gif.py 2 output/hsk1/_spike/assets/tone2.gif
"$PY" scripts/hsk1/gen_stroke_gif.py 你 output/hsk1/_spike/assets/ni.gif
```
Tạo `output/hsk1/_spike/deck.json` với 1 slide `bullets` có `"image": "assets/tone2.gif"` và 1 slide có `"image": "assets/ni.gif"`, rồi:
```bash
"$PY" .claude/skills/teaching-coach/pptx/build_deck.py output/hsk1/_spike/deck.json output/hsk1/_spike/spike.pptx
```
Expected: render OK, không lỗi.

- [ ] **Step 4: Verify — GIF có phát động trong PowerPoint?**

Mở `spike.pptx` bằng PowerPoint desktop, trình chiếu slide chứa GIF. Quan sát: GIF **động** hay đứng yên 1 frame.
- Nếu **động** → chốt: nhúng GIF qua key `image`. Ghi kết luận vào `output/hsk1/README.md` (mục ghi chú kỹ thuật).
- Nếu **đứng yên** (renderer flatten qua Pillow) → **fallback:** ghép các frame thành 1 dải sprite tĩnh (ảnh nhiều bước cạnh nhau) + mô tả bằng lời + audio; ghi rõ fallback đã chọn. (Không sửa build_deck.py — thuộc teaching-coach.)

- [ ] **Step 5: Commit**

```bash
rm -rf output/hsk1/_spike
git add scripts/hsk1/gen_tone_gif.py scripts/hsk1/gen_stroke_gif.py
git commit -m "feat(hsk1): script sinh GIF thanh điệu/thứ tự nét + spike nhúng pptx"
```

### Task 0.3: Đổi tên buổi existing 1/2/3 → 06/10/12

**Files:**
- Rename: `output/hsk1/buoi1_nangnguyen_phuongtien` → `buoi06_nangnguyen_phuongtien`
- Rename: `output/hsk1/buoi2_luongtu_mausac` → `buoi10_luongtu_mausac`
- Rename: `output/hsk1/buoi3_le_thoitiet` → `buoi12_le_thoitiet`
- Modify: `slide/*.json` `meta.lesson`, tên file `.json`/`.pptx` bên trong

- [ ] **Step 1: git mv 3 folder**

```bash
git mv "output/hsk1/buoi1_nangnguyen_phuongtien" "output/hsk1/buoi06_nangnguyen_phuongtien"
git mv "output/hsk1/buoi2_luongtu_mausac" "output/hsk1/buoi10_luongtu_mausac"
git mv "output/hsk1/buoi3_le_thoitiet" "output/hsk1/buoi12_le_thoitiet"
```

- [ ] **Step 2: Đổi tên file JSON/PPTX bên trong cho khớp**

```bash
git mv "output/hsk1/buoi06_nangnguyen_phuongtien/slide/buoi1.json" "output/hsk1/buoi06_nangnguyen_phuongtien/slide/buoi06.json"
git mv "output/hsk1/buoi10_luongtu_mausac/slide/buoi2.json" "output/hsk1/buoi10_luongtu_mausac/slide/buoi10.json"
git mv "output/hsk1/buoi12_le_thoitiet/slide/buoi3.json" "output/hsk1/buoi12_le_thoitiet/slide/buoi12.json"
```
(Đổi cả `buoi2-images.json`→`buoi10-images.json`, `buoi3-images.json`→`buoi12-images.json`, `baitap-buoiX.json`→ số mới, và các `.pptx` `Buoi-1-*`→`Buoi-06-*` nếu có. Liệt kê file thực tế bằng `find output/hsk1/buoi06_* output/hsk1/buoi10_* output/hsk1/buoi12_* -type f` rồi git mv từng cái.)

- [ ] **Step 3: Cập nhật `meta.lesson` trong 3 JSON**

Sửa `"lesson": "HSK1 · Buổi 1"`→`"HSK1 · Buổi 6"`, `Buổi 2`→`Buổi 10`, `Buổi 3`→`Buổi 12`. **Không đụng phần nội dung dạy khác.**

- [ ] **Step 4: Grep & cập nhật tham chiếu cũ toàn repo**

```bash
grep -rn "buoi1_nangnguyen\|buoi2_luongtu\|buoi3_le_thoitiet\|buoi1.json\|buoi2.json\|buoi3.json" --include=*.md --include=*.json state/ knowledge/ docs/ output/ 2>/dev/null
```
Cập nhật mọi tham chiếu đường dẫn cũ (state, docs). (Memory `MEMORY.md` do user sở hữu — nếu thấy tham chiếu, báo user, không tự sửa.)

- [ ] **Step 5: Verify — render lại 3 deck existing OK**

```bash
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
"$PY" .claude/skills/teaching-coach/pptx/build_deck.py "output/hsk1/buoi06_nangnguyen_phuongtien/slide/buoi06.json" "output/hsk1/buoi06_nangnguyen_phuongtien/slide/Buoi-06-Nangnguyen-HoatDong.pptx"
```
Expected: render OK. Lặp cho buoi10, buoi12. (Không bắt buộc regenerate audio.)

- [ ] **Step 6: Commit**

```bash
git add -A output/hsk1
git commit -m "refactor(hsk1): đổi tên buổi 1/2/3 -> 06/10/12 theo syllabus"
```

### Task 0.4: README syllabus (source of truth)

**Files:**
- Create: `output/hsk1/README.md`

- [ ] **Step 1: Viết bảng syllabus 12 buổi + 2 ôn**

Copy bảng §4 spec: cột `# | Buổi | Folder | Nguồn | Ngữ pháp | Bài đọc HSK SC1 | Hán ngữ Q1`. Map vị trí ↔ folder (01–12 + on1/on2). Thêm mục "Ghi chú kỹ thuật" (kết luận GIF từ Task 0.2).

- [ ] **Step 2: Verify**

Mỗi dòng buổi trỏ đúng folder tồn tại (với buổi mới: folder sẽ tạo sau — đánh dấu "⏳ chưa làm"). 3 buổi existing + 2 ôn trỏ folder có thật.

- [ ] **Step 3: Commit**

```bash
git add output/hsk1/README.md
git commit -m "docs(hsk1): README syllabus 12 buổi (source of truth thứ tự dạy)"
```

---

## PROCEDURE P — Quy trình sản xuất 1 buổi (dùng lại cho mọi task buổi)

> Mỗi task buổi cung cấp **Param** rồi chạy đúng các bước P1–P9. Lệnh giống hệt nhau, chỉ khác đường dẫn theo `SLUG`/`XX`. Đây KHÔNG phải placeholder — là tham số của quy trình.

**Param mỗi buổi:**
- `XX` = số syllabus 2 chữ số; `SLUG` = slug folder; `DIR=output/hsk1/buoiXX_SLUG`
- Danh sách **生词** (từ spec §5) + nhóm; **điểm ngữ pháp** (§4); **课文 HSK SC1** cần trích (§4); **dòng Hán ngữ Q1** (§4/§9); ghi chú lỗi người Việt liên quan.

**P1 — Master Teacher (nội dung):** Đóng vai Master Chinese Teacher (teaching-coach Giai đoạn A). Soạn: giải thích ngữ pháp đúng bản chất; 8–12 生词 (đủ 汉字/pinyin/nghĩa); ví dụ khẩu ngữ đời thường; **10 câu khẩu ngữ thông dụng** dùng-ngay; hội thoại mẫu; 2–3 lỗi người Việt hay mắc (đọc `.claude/skills/teaching-coach/references/common-vietnamese-mistakes.md`). Đối chiếu `hsk1-150-checklist.md` — đảm bảo phủ đúng từ được giao, không lấn từ buổi khác.

**P2 — Nguồn 课文 HSK SC1 (cổng duyệt a):** WebSearch/WebFetch bản gốc 课文 các bài HSK SC1 được giao. Đối chiếu ≥1 nguồn tin cậy. **Trình user text 课文 + nguồn để duyệt.** Nếu không tìm được bản đáng tin → hỏi user (paraphrase có ghi chú vs bỏ bài đọc buổi đó — §15 spec). Ghi `DIR/doc/bai-doc-hsksc1.md` (汉字 + pinyin + dịch Việt) sau khi duyệt.

**P3 — Experience Designer (JSON slide):** Map nội dung P1+P2 → `DIR/slide/buoiXX.json` theo schema teaching-coach (`.claude/skills/teaching-coach/pptx/README.md`) và **đúng thứ tự block** (Global Constraints). Block "10 câu khẩu ngữ" dùng type `vocab` hoặc `dialogue`/`bullets` tùy nội dung; footer Hán ngữ Q1 dùng `bullets`/`reading`; lỗi người Việt dùng `table` (Sai|Đúng|Vì sao). Foundation thêm slide GIF (`bullets` có key `image: assets/xxx.gif`). Đặt **action title** + chạy ghost-deck test.

**P4 — Ảnh minh hoạ:** Viết `DIR/slide/buoiXX-images.json` = `{"out_dir":"DIR/slide/assets","images":[{"name":...,"query":...}]}`. Chạy:
```bash
"$PY" .claude/skills/teaching-coach/pptx/fetch_images.py DIR/slide/buoiXX-images.json
```
Expected: `DONE: N/N images`. (Ảnh thiếu → renderer vẽ placeholder xám, không chặn.)

**P5 — GIF (chỉ buổi nền tảng 01/02/03):** Sinh GIF vào `DIR/slide/assets/` bằng `gen_tone_gif.py`/`gen_stroke_gif.py` (Task 0.2) theo kết luận nhúng/fallback. Buổi 01: đủ 5 thanh điệu + vài âm khó + nét chữ số. Buổi 02/03: thứ tự nét chữ trọng tâm.

**P6 — Render slide + audio:**
```bash
"$PY" .claude/skills/teaching-coach/pptx/build_deck.py DIR/slide/buoiXX.json DIR/slide/Buoi-XX-<Ten>.pptx
"$PY" .claude/skills/teaching-coach/pptx/slide_audio.py DIR/slide/buoiXX.json --rate=-18%
```
Expected: build_deck in đường dẫn pptx; slide_audio `DONE: N mp3 mới`. **Soát phát âm (cổng d):** nghe lại các file chứa 多音字/儿化 (觉/乐/行/了/会, …儿) — sai thì đổi câu/thêm ngữ cảnh rồi `--force`.

**P7 — Audio bài đọc 课文:** Sinh mp3 cho `DIR/doc/bai-doc-hsksc1.md` bằng edge-tts, đọc chậm:
```bash
"$PY" -m edge_tts --voice zh-CN-XiaoxiaoNeural --rate=-18% --text "<课文>" --write-media DIR/doc/bai-doc-hsksc1.01.mp3
```
Soát phát âm như P6.

**P8 — Bài tập (exercise-generator):** Soạn `DIR/baitap/baitap-buoiXX.json` (schema `.claude/skills/exercise-generator/worksheet/schema.md`), ~25–27 mục, đủ 听/读/书写 + HSKK, không câu trùng, phủ rộng vốn từ, đáp án 2 cấp cho tự luận. **Cổng b:** trình script 听力/HSKK cho user duyệt trước khi sinh MP3. Kiểm tra:
```bash
"$PY" .claude/skills/exercise-generator/worksheet/check_baitap.py DIR/baitap/baitap-buoiXX.json
```
Expected: không báo trùng. Sinh audio (sau duyệt) `nghe` `--rate=-25%`, `noi_hskk` `--rate=-18%` vào `DIR/baitap/hocsinh/audio/`. Render:
```bash
"$PY" .claude/skills/exercise-generator/worksheet/build_worksheet.py DIR/baitap/baitap-buoiXX.json DIR/baitap
```
Expected: `hocsinh/worksheet.docx` + `dapan/dapan.docx`. **Cổng c:** rà đáp án AI đúng trước khi coi là xong. Append 1 dòng `state/session-log.md`.

**P9 — Cập nhật README + commit:** Đổi trạng thái buổi trong `output/hsk1/README.md` từ "⏳" → "✅". Commit cả buổi:
```bash
git add output/hsk1/buoiXX_SLUG output/hsk1/README.md state/session-log.md
git commit -m "feat(hsk1): buổi XX <chủ đề> — trọn gói (slide+audio+bài tập+bài đọc)"
```

**Verify hoàn thành buổi:** pptx mở được; số 生词 = 8–12 & khớp checklist; có block 10 câu khẩu ngữ (trừ buổi 01); `doc/` có 课文 đã duyệt + audio; worksheet.docx KHÔNG chứa đáp án; dapan.docx có đáp án + 听力文本; audio đã soát 多音字/儿化.

---

## PHASE 1 — Pilot buổi 01 (ngữ âm + GIF)

### Task 1: buoi01_nguam

**Files:**
- Create: `output/hsk1/buoi01_nguam/slide/buoi01.json` (+ `buoi01-images.json`, `assets/`, `.pptx`)
- Create: `output/hsk1/buoi01_nguam/baitap/...`, `output/hsk1/buoi01_nguam/doc/...`

**Param:**
- `XX=01`, `SLUG=nguam`, `DIR=output/hsk1/buoi01_nguam`
- Nội dung: 声母/韵母/声调, quy tắc pinyin, 变调 (三声连读, 一/不 biến điệu), 轻声, 儿化. **Không tính 生词 HSK** → thay block "10 câu khẩu ngữ" bằng luyện âm (cặp tối thiểu, chào hỏi cơ bản để đọc thử).
- 课文 HSK SC1: **không có** (buổi ngữ âm) → P2 bỏ qua, `doc/` chứa bảng luyện âm thay thế.
- Hán ngữ Q1: Bài 1–5 (ngữ âm).
- GIF (P5): 4 đường cong thanh điệu + khinh thanh; âm khó zh/ch/sh/r, j/q/x, ü, e; thứ tự nét 一二三人口你好.
- Lỗi người Việt: nhầm thanh 2/3, âm zh/z, ü/u, thanh điệu bị "phẳng".

- [ ] **Step 1:** P1 — soạn nội dung ngữ âm (bảng thanh mẫu/vận mẫu/thanh điệu, quy tắc biến điệu, luyện âm).
- [ ] **Step 2:** P3 — viết `buoi01.json` (bỏ P2). Slide GIF là trọng tâm.
- [ ] **Step 3:** P4 — ảnh minh hoạ (khẩu hình/lưỡi nếu fetch được; nếu không, để GIF/placeholder).
- [ ] **Step 4:** P5 — sinh GIF thanh điệu + nét + (web-search GIF khẩu hình âm khó, cổng duyệt bản quyền; không có nguồn → sơ đồ tĩnh).
- [ ] **Step 5:** P6 — render pptx + audio slide (đọc chậm), soát phát âm.
- [ ] **Step 6:** P8 — bài tập ngữ âm (nghe phân biệt thanh điệu/âm, chép pinyin, đọc theo) + audio (cổng duyệt) + render + check.
- [ ] **Step 7:** Verify hoàn thành buổi (mở pptx, GIF phát/fallback đúng kết luận Task 0.2).
- [ ] **Step 8:** P9 — README ✅ + commit.

## PHASE 2 — Pilot buổi 02 (đại từ · chào hỏi · làm quen)

### Task 2: buoi02_daitu_chaohoi

**Files:**
- Create: `output/hsk1/buoi02_daitu_chaohoi/{slide,baitap,doc}/...`

**Param:**
- `XX=02`, `SLUG=daitu_chaohoi`, `DIR=output/hsk1/buoi02_daitu_chaohoi`
- 生词 (§5): 你好, 谢谢, 不客气, 再见, 对不起, 没关系, 我/你/他/她, 们, 是, 叫, 名字, 什么, 认识, 高兴, 请, 老师, 学生, 吗, 呢 (gom nhóm, giữ 8–12 từ *mới trọng tâm* + nhắc pinyin đã học ở buổi 01).
- Ngữ pháp: 是 · 吗 · 呢 · 叫…名字 · 很高兴认识你.
- 课文 HSK SC1: L1 你好 · L2 谢谢你 · L3 你叫什么名字.
- Hán ngữ Q1: Bài 1, 3, 5.
- GIF (P5): thứ tự nét 你好我是叫.
- Lỗi người Việt: lẫn 你/您, thiếu 吗 khi hỏi, đọc sai thanh 你好 (biến điệu 3+3).

- [ ] **Step 1:** P1 — nội dung + 10 câu khẩu ngữ chào hỏi/làm quen.
- [ ] **Step 2:** P2 — web-search L1/L2/L3 課文, trình user duyệt, ghi `doc/bai-doc-hsksc1.md`.
- [ ] **Step 3:** P3 — viết `buoi02.json` đủ block đúng thứ tự (có 10 câu khẩu ngữ + footer Hán ngữ + lỗi VN).
- [ ] **Step 4:** P4 — ảnh; P5 — GIF nét.
- [ ] **Step 5:** P6 — render pptx + audio slide, soát phát âm; P7 — audio 課文.
- [ ] **Step 6:** P8 — bài tập trọn gói (cổng duyệt script + check + render).
- [ ] **Step 7:** Verify hoàn thành buổi.
- [ ] **Step 8:** P9 — README ✅ + commit.

> **REVIEW GATE (bắt buộc):** Sau Task 1 + Task 2, **trình user 2 pilot** (pptx + worksheet + bài đọc). User duyệt khuôn (bố cục, chất lượng nội dung, GIF, độ khó) → mới sản xuất 7 buổi còn lại. Chỉnh khuôn nếu user yêu cầu.

---

## PHASE 3 — Sản xuất 7 buổi còn lại (sau khi duyệt pilot)

> Mỗi task chạy đúng **Procedure P** với Param của buổi. Thứ tự: 03 → 04 → 05 → 07 → 08 → 09 → 11. Giao theo lô + review giữa các lô.

### Task 3: buoi03_so_thoigian_diadiem (nền tảng)
**Param:** `XX=03`, `SLUG=so_thoigian_diadiem`. 生词: 一~十, 零, 百, 几, 点, 分, 号, 月, 星期, 年, 今天, 明天, 昨天, 现在, 上午, 下午, 中午, 这儿, 那儿, 哪儿, 在 (chia nhóm số / thời gian / địa điểm; giữ nhịp — có thể tách slide 生词 nhiều nhóm). Ngữ pháp: 几点 · 号/月/星期 · 这儿/那儿/哪儿 · 在. 课文: L7 今天几号, L11 现在几点. Hán ngữ Q1: Bài 8. GIF: thứ tự nét chữ số 一二三…十. Lỗi VN: thứ tự ngày-tháng, 二/两, đọc số điện thoại.
- [ ] **Step 1:** P1. **Step 2:** P2 (L7,L11, duyệt). **Step 3:** P3. **Step 4:** P4+P5. **Step 5:** P6+P7. **Step 6:** P8. **Step 7:** Verify. **Step 8:** P9.

### Task 4: buoi04_giadinh
**Param:** `XX=04`, `SLUG=giadinh`. 生词: 家, 爸爸, 妈妈, 儿子, 女儿, 口, 有, 没有, 和, 都, 岁, 多大. Ngữ pháp: 有/没有 · 几口人 · 和 · 都 · 多大/几岁. 课文: L5 她女儿今年二十岁. Hán ngữ Q1: Q1 Hạ (gia đình). Lỗi VN: 有 phủ định dùng 没 (không 不), thiếu 口 khi đếm người.
- [ ] **Step 1:** P1. **Step 2:** P2 (L5). **Step 3:** P3. **Step 4:** P4. **Step 5:** P6+P7. **Step 6:** P8. **Step 7:** Verify. **Step 8:** P9. *(không GIF — không phải nền tảng)*

### Task 5: buoi05_nghe_quoctich
**Param:** `XX=05`, `SLUG=nghe_quoctich`. 生词: 中国, 中国人, 医生, 工作, 学习, 说, 汉语, 字, 人, 哪, 是, 谁. Ngữ pháp: 是 (X是Y) · 说+ngôn ngữ · 哪国人. 课文: L4 她是我的汉语老师, L6 我会说汉语, L9 你儿子在哪儿工作. Hán ngữ Q1: Bài 6, 11, 12. Lỗi VN: 说/会 lẫn lộn, 是 thừa với tính từ.
- [ ] **Step 1:** P1. **Step 2:** P2 (L4,L6,L9). **Step 3:** P3. **Step 4:** P4. **Step 5:** P6+P7. **Step 6:** P8. **Step 7:** Verify. **Step 8:** P9.

### Task 6: buoi07_anuong
**Param:** `XX=07`, `SLUG=anuong`. 生词: 吃, 喝, 饭, 米饭, 菜, 水, 茶, 水果, 苹果, 东西, 好吃. Ngữ pháp: 想/要+V · 吃饭了吗 · 好吃/好喝. 课文: L8 我想喝茶. Hán ngữ Q1: Bài 7. Lỗi VN: 吃/喝 chọn sai, 想 vs 要.
- [ ] **Step 1:** P1. **Step 2:** P2 (L8). **Step 3:** P3. **Step 4:** P4. **Step 5:** P6+P7. **Step 6:** P8. **Step 7:** Verify. **Step 8:** P9.

### Task 7: buoi08_nha_vitri
**Param:** `XX=08`, `SLUG=nha_vitri`. 生词: 桌子, 椅子, 电视, 电脑, 书, 在, 里, 上, 家, 前面, 后面. Ngữ pháp: 在 (tồn tại) · …里/…上 · 前面/后面. 课文: L9 你儿子在哪儿工作 (nhấn 在). Hán ngữ Q1: Bài 10, 12. Lỗi VN: 在 vị trí trong câu, thiếu 里/上.
- [ ] **Step 1:** P1. **Step 2:** P2 (L9). **Step 3:** P3. **Step 4:** P4. **Step 5:** P6+P7. **Step 6:** P8. **Step 7:** Verify. **Step 8:** P9.

### Task 8: buoi09_sothich
**Param:** `XX=09`, `SLUG=sothich`. 生词: 喜欢, 看, 书, 电影, 听, 读, 写, 爱, 学习, 唱歌 *(đối chiếu checklist Task 0.1 — 唱歌 nếu ngoài 150 từ thì thay bằng từ HSK1 phù hợp, vd 说话/做)*. Ngữ pháp: 喜欢+V · 爱 · ôn 会/想. 课文: L13 他在学做中国菜. Hán ngữ Q1: Q1 Hạ (sở thích). Lỗi VN: 喜欢 + V trực tiếp (không thêm 是), 看/读.
- [ ] **Step 1:** P1. **Step 2:** P2 (L13). **Step 3:** P3. **Step 4:** P4. **Step 5:** P6+P7. **Step 6:** P8. **Step 7:** Verify. **Step 8:** P9.

### Task 9: buoi11_muasam_tinhtu
**Param:** `XX=11`, `SLUG=muasam_tinhtu`. 生词: 买, 钱, 块, 多少, 太, 大, 小, 多, 少, 好, 漂亮, 很, 不, 商店. Ngữ pháp: 多少钱 · 太…了 · 买 · 很+Adj (vị ngữ tính từ, không 是) · 不 · số lớn. 课文: L14 她买了不少东西, L15 我在这儿买的. Hán ngữ Q1: Bài 8, 9, 15. Capstone hội thoại tổng hợp toàn khoá. Lỗi VN: 很 bắt buộc trước tính từ, 太…了, 是 thừa với tính từ.
- [ ] **Step 1:** P1. **Step 2:** P2 (L14,L15). **Step 3:** P3. **Step 4:** P4. **Step 5:** P6+P7. **Step 6:** P8. **Step 7:** Verify. **Step 8:** P9.

> **FINAL GATE:** Sau 7 buổi, chạy verify tổng: `hsk1-150-checklist.md` — mọi từ đã "✅ có buổi phụ trách + đã soạn"; `output/hsk1/README.md` mọi buổi ✅; đối chiếu đủ 150 từ. Trình user bàn giao.

---

## Out of scope / follow-up

**Phase từ vựng HSK1 theo buổi (§14 spec)** — trang `output/study/hsk1/buoiXX/tu-vung.html` kiểu Quizlet, bỏ neo Activation vault. **Tách plan riêng** (`writing-plans` lần sau), viết **sau khi vocab 9 buổi đã chốt** (nguồn = `生词` trong các `buoiXX.json`). Lý do tách: (1) phụ thuộc toàn bộ vocab buổi đã ổn định; (2) cần điều chỉnh tooling vocab-study (hardcode `hsk6`, đọc `raw/Từ vựng.xlsx`, đọc Activation `tier-*.md`) → quyết định adapter vs biến thể renderer khi tới nơi. Đưa vào backlog, không chặn Phase 0–3.

## Self-review notes
- Spec §4 syllabus → Task 0.4 (README) + mọi task buổi. §5 vocab → Param từng task + Task 0.1 checklist. §6 thứ tự block → Global Constraints + P3. §7 GIF → Task 0.2 + P5. §8 bài đọc → P2/P7. §9 Hán ngữ → P3 footer + Param. §10 pipeline → Procedure P (P1–P9). §11 đặt tên → Global Constraints + Task 0.3. §13 verify → "Verify hoàn thành buổi" + FINAL GATE. §14 vocab-study → follow-up plan. §15 rủi ro → Task 0.2 fallback GIF, P2 xử lý 课文.
- Từ 唱歌 (Task 8) gắn cờ đối chiếu 150-từ (Task 0.1) — tránh đưa từ ngoài HSK1.
