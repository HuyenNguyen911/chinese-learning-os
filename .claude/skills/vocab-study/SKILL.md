---
name: vocab-study
description: >
  Sinh trang HỌC TỪ VỰNG theo bài (kiểu Quizlet) từ file Excel từ vựng.
  Output: output/Giáo trình chuẩn/hsk6/study/tu-vung.html tự chứa — bảng 生词 + 生词拓展, chế độ học
  flashcard (active recall + Leitner, neo theo Activation của vault, resume đúng thẻ khi lỡ đóng
  giữa chừng), chiết tự + mẹo nhớ tiếng Việt, phát âm 🔊. Cũng xử lý lệnh "áp dụng lên hạng" để ghi
  hàng chờ D→C (từ flashcard) vào tier-a.md. Use when user muốn "học từ vựng", "review từ vựng",
  "sinh trang học từ", "cập nhật từ vựng theo bài", "áp dụng lên hạng".
author: Chinese Learning OS
---

# vocab-study — Trang học từ vựng theo bài (Quizlet-style)

> Chuyên dụng cho **review/học từ vựng theo bài**. KHÔNG bóc tách bài khóa —
> phần đó thuộc skill `lesson-prep` (chưa làm). Skill này nhận **file Excel từ vựng**
> và sinh 1 file HTML tự chứa để học.

## Input
`raw/Từ vựng.xlsx` — 2 sheet:
- **'Từ vựng'**: cột `Bài, 生词, Pinyin, 描述, 意义, 例如, 复习, 检查`
  (描述 = 释义 tiếng Trung; 意义 = nghĩa Việt; 例如 = ví dụ). Đây là 生词.
- **'Chung từ'**: cột `Bài, 生词(=chuỗi nhóm họ từ ngăn bởi 、hoặc -), …, 意义(ghi chú Việt)`.
  Đây là **生词拓展**.

## Output
- `output/Giáo trình chuẩn/hsk6/study/tu-vung.md` — nguồn (bảng 生词 + 生词拓展), có thể sửa tay.
- `output/Giáo trình chuẩn/hsk6/study/tu-vung.html` — trang học tự chứa (mở bằng trình duyệt).
  (Mặc định hsk6; đổi `OUT` trong build_md.py/render_html.py nếu cấp khác.)

## Tính năng trang HTML
- Bảng 生词: `生词 | Pinyin | 释义 | Nghĩa | 例句`; bài mới nhất trên cùng; mặc định thu gọn.
- Tab **生词拓展** (nếu bài có): nhóm họ từ theo chữ gốc + pinyin.
- **Trạng thái ôn** ⚪/D/C/B/A đọc từ `knowledge/vocabulary/tier-*.md` (Activation).
- **🎓 Học**: flashcard active-recall + lặp ngắt quãng Leitner (localStorage);
  chấm ❌ Chưa / ✅ Thuộc; **trần thăng hạng = Activation+1** (chưa dùng thật thì không "thuộc hẳn").
- **Resume đúng thẻ**: đóng popup giữa chừng (lỡ tay / đổi ý) → mở lại đúng bài sẽ hỏi tiếp tục từ
  vị trí dừng (localStorage `hsk6study_resume_v1`), không bắt học lại từ đầu. Tự xoá khi học xong hẳn.
- **Lên hạng C (chỉ D→C, recognition-only)**: bấm "Thuộc" lần đầu với 1 từ đang D → queue ngay
  (localStorage `hsk6vocab_promote_v1`, banner xanh hiện số từ đang chờ). Xuất file
  `tu-vung-promote-to-c.json` (nút "Xuất danh sách"), git add/commit/push, rồi nhờ Claude chạy lệnh
  **`áp dụng lên hạng`** ở phiên làm việc kế — Claude/script mới thật sự ghi vào `tier-a.md` (trang
  HTML tĩnh không tự ghi file được). **Không đụng B/A** — 2 mức đó vẫn chỉ lên qua dùng thật
  (viết/nói được chấm, do Learning Strategist batch update từ session-log).
- **🧩 Chiết tự / mẹo nhớ**: phân rã bộ/thành phần + **mẹo nhớ tiếng Việt** (kể chuyện) + 🔍 HanziCraft.
- **🔊 Phát âm** (Web Speech API, giọng zh-CN của máy) — bảng + thẻ học (auto đọc khi lật).
- ✏️ Sửa nội dung tại chỗ (lưu localStorage).
- **🚩 Đánh dấu dòng đang học**: cờ per-dòng (bật/tắt tự do, localStorage) để tracking vị trí dừng bài giữa các buổi; badge 🚩N hiện trên summary mỗi Bài.

## Pipeline (chạy từ gốc repo; `PY` = python có pypinyin + openpyxl)
```bash
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
SK=".claude/skills/vocab-study/scripts"
# 1) Excel -> data/tv.json + data/ct.json
"$PY" "$SK/extract_xlsx.py"            # hoặc truyền đường dẫn xlsx khác
# 2) (chỉ khi có CHỮ MỚI) bổ sung dữ liệu chiết tự/Hán-Việt
"$PY" "$SK/build_hanzi.py"
# 3) dựng markdown nguồn
"$PY" "$SK/build_md.py"
# 4) (chỉ khi có TỪ MỚI) sinh mẹo nhớ — TĂNG DẦN, không chạy lại từ đã có
"$PY" "$SK/gen_mnemonic_wf.py"         # -> tạo data/wf_mnemonic.js cho từ còn thiếu
#    rồi gọi tool: Workflow({scriptPath: ".../data/wf_mnemonic.js"})   # cần user bật orchestration
#    lưu <output> workflow, rồi:
"$PY" "$SK/merge_mnemonic.py" <file_output_workflow>
# 5) render HTML
"$PY" "$SK/render_html.py"
```
Lần cập nhật thông thường (không có chữ/từ mới) chỉ cần **1 → 3 → 5**.

## `áp dụng lên hạng` [file, mặc định `output/Giáo trình chuẩn/hsk6/study/tu-vung-promote-to-c.json`]
Áp dụng hàng chờ D→C mà user export từ nút "🎓 Xuất danh sách" trên trang flashcard (xem mục
Resume/Lên hạng ở trên). Trang HTML tĩnh không tự ghi được `tier-a.md`, nên bước này luôn cần chạy
tay ở phiên Claude Code kế tiếp (gợi ý: gộp vào lúc `/close-session`).
```bash
"$PY" ".claude/skills/vocab-study/scripts/apply_promote.py"   # hoặc truyền path file khác
```
- Chỉ đổi `Activation: D` → `C`, `Seen` +1, `Last Studied` = hôm nay cho từ đã có entry trong
  `tier-a.md`/`tier-b.md`/`tier-c.md`. Từ đang B/A thì **bỏ qua, không đụng** (báo cáo riêng).
  Từ chưa có entry nào (chưa được Learning Strategist đưa vào vault) thì **bỏ qua**, không tự thêm.
- Recalc lại `state/activation.md` (Total/Activated/Rate/Avg Confidence/Tier counts) sau khi ghi.
- Xoá file JSON đã xử lý xong (tránh áp dụng lại 2 lần).
- Báo cáo cho user: đã promote từ nào, bỏ qua từ nào và vì sao — để user tự đối chiếu.

## Sinh override bằng workflow (nghĩa Việt / 例句 cá nhân hoá)
Khi cột 意义 trống nhiều hoặc cần thay 例句 bài khóa bằng câu cá nhân hoá — dùng workflow (cần user bật orchestration):
1. **Trích payload theo bài** ra scratchpad: mỗi bài 1 file JSON `[{w, zh(=释义), vi}]` (lọc bỏ seed 拓展).
2. **Workflow**: `pipeline` theo bài, mỗi agent 1 bài, `schema` ép trả `{items:[{w, vi|ex}]}`.
   - Nghĩa Việt: prompt "biên soạn từ điển Hán-Việt, chắt nghĩa cốt lõi từ 释义, ngắn gọn".
   - 例句 cá nhân hoá: **nạp `memory/user-profile.md` vào prompt** làm bối cảnh; câu đủ chủ-vị, khẩu ngữ, bám đời sống user, ~12-22 chữ.
3. **Merge** kết quả (đọc `result` trong task output) → ghi `vi_override.json` / `ex_override.json` (map `{w: value}`).
4. Build lại **3 → 5**, rồi **verify**: `html.escape(value) in html` cho mọi entry (phải 100%); đếm 意义 trống = 0.

> ⚠️ **Gotcha `user-profile` cho 例句:** bản đầy đủ (khối "Đời sống & Cá nhân") có thể nằm ở nhánh khác
> (`feat/personalization-doc-hieu`). Nếu nhánh hiện tại chỉ có bản tối thiểu → đọc qua
> `git show feat/personalization-doc-hieu:memory/user-profile.md` (CHỈ đọc, không ghi memory).

## Assets (đóng gói sẵn trong data/)
- `hanzi.json` — chiết tự + bộ + 字源(sem/phon) + pinyin + Hán-Việt (~1861 chữ). Nguồn: Make Me a Hanzi + Unihan.
- `mnemonic.json` — mẹo nhớ tiếng Việt theo từ (~1301, sinh bằng workflow). **Tăng dần**.
- `desc_override.json` — 释义 do hệ thống bổ sung cho từ có 描述 trống (vd Bài 1–2). **Chỉ lấp trống** (Excel ưu tiên).
- `vi_override.json` — Nghĩa Việt do hệ thống bổ sung cho từ có 意义 trống. **Chỉ lấp trống** (Excel ưu tiên).
- `ex_override.json` — 例句 cá nhân hoá (bám `memory/user-profile.md`). **GHI ĐÈ** câu bài khóa cho từ có trong file (vd Bài 15–28).
- `exp_extra.json` — nhóm 生词拓展 thêm tay cho bài sheet 'Chung từ' thiếu (vd Bài 28).
- `bai_titles.json` — map `{"<N>": "<标题 bài khóa>"}`. build_md gắn tên vào heading `## Bài N — <title>`, render_html hiện cạnh mỗi bài + nhãn flashcard. lesson-prep tự ghi khi bóc bài mới.
- `tv.json`, `ct.json` — trung gian, tái sinh mỗi lần chạy bước 1 (không cần giữ tay).

## Nguyên tắc
- Pinyin auto (pypinyin) + luật sửa 多音字 (朴→pǔ…), 儿化 (…儿→r), dấu `'`, âm theo ngữ cảnh từ.
- 释义 **ưu tiên cột 描述 của user**; chỉ tự sinh khi trống (`desc_override.json`).
- Nghĩa Việt **ưu tiên cột 意义**; chỉ tự sinh khi trống, có verify chéo trước khi merge (`vi_override.json`).
- 例句 mặc định theo cột 例如; nếu từ có trong `ex_override.json` thì **ghi đè** bằng câu cá nhân hoá.
- **Hàng phân cách bảng markdown** = mọi ô chỉ gồm `---`/`:`; render KHÔNG được bỏ dòng dữ liệu chỉ vì ô có chứa `---` (bug cũ đã sửa: 勉强 Bài 5).
- **Đọc** `knowledge/vocabulary/*` (Activation) khi render trang. Chỉ **ghi** qua lệnh `áp dụng lên hạng`
  ở trên, và ghi hẹp: riêng field Seen/Activation(D→C)/Last Studied của entry đã có sẵn — không thêm
  entry mới, không đụng Confidence/Speaking/Writing/Activation B/A. Ngoài phạm vi đó, state vocabulary
  vẫn do learning-strategist sở hữu (CLAUDE.md §6).
- Mẹo nhớ: workflow cần user bật orchestration; **chỉ sinh cho từ mới** để tiết kiệm token.
- **Mọi script phải `reconfigure(utf-8)` stdout/stderr ở đầu file** — console Windows mặc định cp1252, in 中文/tiếng Việt sẽ crash `UnicodeEncodeError` nếu thiếu.
- **Sau mỗi lần build, nhắc user `Ctrl+Shift+R`** — trình duyệt cache file HTML rất mạnh; mở lại/`start` chỉ focus tab cũ, dễ tưởng "update mất tiêu".

## Phụ thuộc
- Python: `pypinyin`, `openpyxl`.
- build_hanzi.py cần mạng lần đầu (tải Make Me a Hanzi + Unihan vào data/_src/); sau đó cache.
- Phát âm: giọng tiếng Trung của HĐH (Web Speech). Không cần cài gì thêm.
