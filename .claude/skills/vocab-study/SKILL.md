---
name: vocab-study
description: >
  Sinh trang HỌC TỪ VỰNG theo bài (kiểu Quizlet) từ file Excel từ vựng.
  Output: output/study/hskN/tu-vung.html tự chứa — bảng 生词 + 生词拓展, chế độ học
  flashcard (active recall + Leitner, neo theo Activation của vault), chiết tự +
  mẹo nhớ tiếng Việt, phát âm 🔊. Use when user muốn "học từ vựng", "review từ vựng",
  "sinh trang học từ", "cập nhật từ vựng theo bài".
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
- `output/study/hskN/tu-vung.md` — nguồn (bảng 生词 + 生词拓展), có thể sửa tay.
- `output/study/hskN/tu-vung.html` — trang học tự chứa (mở bằng trình duyệt).
  (Mặc định hsk6; đổi `OUT` trong build_md.py/render_html.py nếu cấp khác.)

## Tính năng trang HTML
- Bảng 生词: `生词 | Pinyin | 释义 | Nghĩa | 例句`; bài mới nhất trên cùng; mặc định thu gọn.
- Tab **生词拓展** (nếu bài có): nhóm họ từ theo chữ gốc + pinyin.
- **Trạng thái ôn** ⚪/D/C/B/A đọc từ `knowledge/vocabulary/tier-*.md` (Activation) — **chỉ đọc**.
- **🎓 Học**: flashcard active-recall + lặp ngắt quãng Leitner (localStorage);
  chấm ❌ Chưa / ✅ Thuộc; **trần thăng hạng = Activation+1** (chưa dùng thật thì không "thuộc hẳn").
- **🧩 Chiết tự / mẹo nhớ**: phân rã bộ/thành phần + **mẹo nhớ tiếng Việt** (kể chuyện) + 🔍 HanziCraft.
- **🔊 Phát âm** (Web Speech API, giọng zh-CN của máy) — bảng + thẻ học (auto đọc khi lật).
- ✏️ Sửa nội dung tại chỗ (lưu localStorage).

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

## Assets (đóng gói sẵn trong data/)
- `hanzi.json` — chiết tự + bộ + 字源(sem/phon) + pinyin + Hán-Việt (~1861 chữ). Nguồn: Make Me a Hanzi + Unihan.
- `mnemonic.json` — mẹo nhớ tiếng Việt theo từ (~1301, sinh bằng workflow). **Tăng dần**.
- `desc_override.json` — 释义 do hệ thống bổ sung cho từ có 描述 trống (vd Bài 1–2).
- `exp_extra.json` — nhóm 生词拓展 thêm tay cho bài sheet 'Chung từ' thiếu (vd Bài 28).
- `bai_titles.json` — map `{"<N>": "<标题 bài khóa>"}`. build_md gắn tên vào heading `## Bài N — <title>`, render_html hiện cạnh mỗi bài + nhãn flashcard. lesson-prep tự ghi khi bóc bài mới.
- `tv.json`, `ct.json` — trung gian, tái sinh mỗi lần chạy bước 1 (không cần giữ tay).

## Nguyên tắc
- Pinyin auto (pypinyin) + luật sửa 多音字 (朴→pǔ…), 儿化 (…儿→r), dấu `'`, âm theo ngữ cảnh từ.
- 释义 **ưu tiên cột 描述 của user**; chỉ tự sinh khi trống.
- Nghĩa Việt giữ theo cột 意义.
- Chỉ **đọc** `knowledge/vocabulary/*` (Activation). Không ghi. State vocabulary do learning-strategist sở hữu (CLAUDE.md §6).
- Mẹo nhớ: workflow cần user bật orchestration; **chỉ sinh cho từ mới** để tiết kiệm token.

## Phụ thuộc
- Python: `pypinyin`, `openpyxl`.
- build_hanzi.py cần mạng lần đầu (tải Make Me a Hanzi + Unihan vào data/_src/); sau đó cache.
- Phát âm: giọng tiếng Trung của HĐH (Web Speech). Không cần cài gì thêm.
