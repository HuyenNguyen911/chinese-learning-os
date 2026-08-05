---
name: close-session
description: Đóng session Chinese Learning OS — chạy hygiene check (git status), phân loại file thay đổi theo nhánh đích (main cho meta/shared-data, nhánh gốc cho content), rà soát session tìm tri thức/pattern mới cần phản ánh vào skill hiện có, rồi gộp TẤT CẢ vào 1 bảng commit+push duy nhất chờ user duyệt 1 lần. Use when user gõ "/close-session" hoặc nói "đóng session" / "kết thúc buổi".
---

# Close Session

Bạn là routine đóng session của Chinese Learning OS. Chạy checklist tuần tự, không bỏ bước. Skill này là skill **meta**: nó được phép sửa các `SKILL.md` khác và `CLAUDE.md` — nhưng **chỉ sau khi user duyệt từng mục**. Không đụng `memory/*`.

## Bước 1 — Hygiene check + phân loại file
1. `git branch --show-current` → ghi nhớ **nhánh gốc** (nhánh đang đứng khi bắt đầu close-session).
2. Chạy `git status` (và `git status --short` nếu output dài).
3. Với mỗi file thay đổi/chưa commit, phân vào 1 trong 3 nhóm theo CLAUDE.md §5.5 và §6:
   - **Nhóm meta** → đích `main`. Gồm `.claude/skills/**/SKILL.md`, `.claude/skills/**/references/**`, `CLAUDE.md`. (Nhóm này sẽ được bổ sung thêm ở Bước 3 nếu có mục được duyệt.)
   - **Nhóm shared-data** → đích `main` (CLAUDE.md §5.5 quy tắc 7, dùng chung mọi cấp, không gắn riêng khóa nào). Gồm `.claude/skills/vocab-study/**`, `output/study/hskN/**`, `knowledge/vocabulary/**`.
   - **Nhóm feature-content** → đích **nhánh gốc** (nhánh đang đứng). Mọi file còn lại thuộc phạm vi công việc của session (vd `output/hskN/buoiX_.../**`, nội dung riêng của `feat/hskN-full-course`).
   - **Không phân loại được** (không khớp rõ pattern nào ở trên, hoặc nằm ngoài các thư mục đã biết trong CLAUDE.md §6) → để riêng, **không** đưa vào bảng push ở Bước 4 — báo cho user tự xử lý.
4. Báo cáo ngắn kết quả phân loại (chưa commit/push gì ở bước này).

## Bước 2 — Xác định phạm vi session (bắt buộc, làm trước khi rà soát)
1. Dựa vào skill đã dùng + file đã sửa trong session (Bước 1), xác định session này thuộc (những) **chủ đề/skill nào**.
2. Nếu session chạm nhiều chủ đề tách biệt (vd vừa làm `lesson-prep` vừa làm `vocab-study`), liệt kê riêng từng phạm vi — đừng gộp chung.
3. Phạm vi này là ranh giới cho Bước 3: **không** kéo phát hiện/tri thức thuộc session hoặc chủ đề khác đang dang dở (từ hội thoại trước, từ memory, v.v.) vào bảng rà soát — chỉ xét những gì thật sự thuộc phạm vi vừa xác định.

## Bước 3 — Rà soát Skill (bắt buộc)

Quét **2 nguồn** để tìm thứ cần đưa vào skill, **giới hạn trong phạm vi đã xác định ở Bước 2**:

**Nguồn A — Thay đổi file (git):**
1. Xem file bị tạo/sửa trong session: `.claude/skills/**/SKILL.md`, `.claude/skills/**/references/**`, và `CLAUDE.md`.
2. Với mỗi thay đổi: hỏi "thay đổi này đã nhất quán chưa? có cần phản ánh sang skill khác / routing / catalog không?" (vd sửa 1 skill nhưng quên update §7 Catalog trong CLAUDE.md).

**Nguồn B — Tri thức ẩn trong hội thoại:**
Quét toàn bộ session tìm:
- **Correction lặp lại** — user sửa cùng 1 lỗi/thói quen ≥ 2 lần → nên thành quy tắc trong skill.
- **Pattern / quy tắc mới** — cách làm mới được thống nhất mà skill chưa ghi.
- **Bước thủ công lặp đi lặp lại** — việc tay làm nhiều lần → nên đưa thành command/bước trong skill.

**Map & trình bày:**
Map mỗi phát hiện tới **skill đích**: `learning-strategist`, `hsk6-examiner`, `speaking-coach`, `exercise-generator`, `teaching-coach`, `doc-analyzer`, `vocab-study`, `lesson-prep`, `close-session`, hoặc `CLAUDE.md`.

Trình bày bảng:

| # | Phát hiện | Nguồn | Skill đích | Đề xuất sửa cụ thể |
|---|---|---|---|---|
| 1 | ... | A/B | ... | ... |

**Cổng duyệt (bắt buộc):**
- Chờ user duyệt **từng mục**. Không tự ý sửa.
- Mục được duyệt → thực hiện sửa vào SKILL.md / CLAUDE.md tương ứng.
- Mục không duyệt → bỏ qua, không lưu.
- Nếu quét xong không có phát hiện nào → nói rõ "không có gì cần update".

## Bước 4 — Bảng tổng hợp Commit + Push (1 lần duyệt duy nhất)

Mục tiêu: gộp **mọi** thay đổi cần push của session (meta + shared-data + feature-content, đã phân loại ở Bước 1, cộng với mục được duyệt ở Bước 3) vào **một bảng duy nhất**, user duyệt 1 lần rồi thực hiện hết — tránh tình trạng push xong nội dung rồi close-session lại push tiếp riêng phần meta.

1. Gộp file của Bước 3 (mục được duyệt) vào **nhóm meta**.
2. Với mỗi nhóm còn file (meta / shared-data / feature-content), tự sinh 1 commit message ngắn mô tả đúng nội dung đã đổi trong nhóm đó.
3. Trình bày bảng:

| Nhóm | File | Nhánh đích | Commit message đề xuất |
|---|---|---|---|
| meta | ... | main | ... |
| shared-data | ... | main | ... |
| feature-content | ... | (nhánh gốc) | ... |

   - Nhóm nào không có file thì bỏ khỏi bảng.
   - Liệt kê rõ file **không phân loại được** (nếu có, từ Bước 1) ngay dưới bảng — nói rõ sẽ không đụng tới, user tự xử lý.
4. Chờ **1 lần duyệt duy nhất** cho toàn bảng. User có thể sửa message hoặc gạch bỏ riêng từng nhóm trước khi OK. Không tự push khi chưa duyệt.
5. Sau khi duyệt, thực hiện theo thứ tự — **nhóm đích = nhánh gốc trước** (không phải chuyển nhánh), rồi tới các nhóm đích = `main`:
   - **Nhóm đích = nhánh gốc:** `git add <file nhóm>` → commit với message đã duyệt → `git push`.
   - **Nhóm đích = `main` (meta / shared-data):**
     a. Nếu nhánh gốc đã là `main` → bỏ qua stash/checkout, add+commit+push thẳng.
     b. Ngược lại: `git add <file nhóm>` → `git stash push -u -- <các file đó>` → `git checkout main` → `git stash pop` (conflict → dừng, báo user, không tự resolve) → `git add <file nhóm>` → commit với message đã duyệt → `git push` → `git checkout <nhánh gốc>`.
   - Nếu có cả 2 nhóm đích `main` (meta và shared-data), có thể gộp làm 1 lần chuyển nhánh (stash cả 2 nhóm file cùng lúc, commit tách riêng theo message của từng nhóm, rồi push).
6. Báo cáo: đã commit+push nhóm nào vào nhánh nào, đã quay lại đúng nhánh gốc.

## Bước 5 — Đóng
- Nếu không có gì → báo "Session sạch, đã đóng."
- Nếu có sửa/push → báo tóm tắt: đã sửa mục nào (vào skill nào), đã commit+push nhóm nào vào nhánh nào. Rồi đóng.

## Quy tắc bất biến
- Không tự sửa SKILL.md/CLAUDE.md khi mục ở Bước 3 chưa được duyệt.
- Không commit/push bất kỳ nhóm nào khi chưa qua bảng duyệt ở Bước 4 — kể cả khi phân loại đã rõ ràng.
- File **không phân loại được** ở Bước 1 → tuyệt đối không đụng, để user tự quyết định.
- Không đụng `memory/*` (thuộc quyền user — xem CLAUDE.md §4).
- Chỉ đề xuất sửa skill khi có bằng chứng thật trong session (correction lặp lại, pattern rõ) — không bịa việc để "có cái mà sửa".
- Rà soát chỉ trong phạm vi session đã xác định ở Bước 2 — không gom tri thức từ chủ đề/session khác đang dang dở.
- Giữ nhẹ: session không có gì mới/không có gì cần push thì đóng nhanh, đừng kéo dài.
