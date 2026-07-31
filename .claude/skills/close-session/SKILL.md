---
name: close-session
description: Đóng session Chinese Learning OS — chạy hygiene check (git status) rồi rà soát session tìm tri thức/pattern mới cần phản ánh vào các skill hiện có. Trình bày bảng, chờ user duyệt từng mục trước khi sửa. Use when user gõ "/close-session" hoặc nói "đóng session" / "kết thúc buổi".
---

# Close Session

Bạn là routine đóng session của Chinese Learning OS. Chạy checklist tuần tự, không bỏ bước. Skill này là skill **meta**: nó được phép sửa các `SKILL.md` khác và `CLAUDE.md` — nhưng **chỉ sau khi user duyệt từng mục**. Không đụng `memory/*`.

## Bước 1 — Hygiene check
1. Chạy `git status` (và `git status --short` nếu output dài).
2. Báo cáo ngắn: file nào đã thay đổi / chưa commit trong session này.
3. **Không** tự commit — chỉ báo cáo để user quyết định.

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

## Bước 4 — Commit + Push meta files (chỉ khi có mục được duyệt ở Bước 3)

Mục tiêu: đồng bộ `SKILL.md`/`CLAUDE.md` sang các thiết bị khác ngay, vì đây là meta/infra dùng chung mọi nơi (CLAUDE.md §5.5 quy tắc 3: meta luôn về `main`).

1. `git branch --show-current` → ghi nhớ đây là **nhánh gốc** (vd `feat/hsk1-full-course`).
2. `git add` đúng các file meta vừa sửa (chỉ `SKILL.md`/`CLAUDE.md` bị đổi ở Bước 3 — không add file khác).
3. Tách riêng thay đổi này khỏi nhánh gốc: `git stash push -u -- <các file meta đó>`.
4. `git checkout main`.
5. `git stash pop` để áp thay đổi meta lên `main`.
   - Nếu conflict khi pop → dừng lại, báo user, không tự ý resolve.
6. `git add <các file meta>` rồi commit với message ngắn mô tả đúng nội dung đã duyệt.
7. `git push`.
8. `git checkout <nhánh gốc>` để quay lại đúng chỗ đang làm dở.
9. Báo cáo: đã commit+push gì vào `main`, đã quay lại nhánh gốc.

Nếu nhánh gốc vốn đã là `main` thì bỏ qua bước stash/checkout, commit thẳng và push.

## Bước 5 — Đóng
- Nếu không có gì → báo "Session sạch, đã đóng."
- Nếu có sửa → báo tóm tắt: đã sửa mục nào, vào skill nào, đã commit+push vào `main` chưa. Rồi đóng.

## Quy tắc bất biến
- Không tự sửa file khi chưa được duyệt.
- Chỉ tự commit + push các file **meta đã được duyệt** (`SKILL.md`/`CLAUDE.md`, theo Bước 4) — không commit/push bất kỳ file nào khác (output, work-in-progress của session) dù cùng đứng chung working tree lúc đó; những file đó vẫn do user tự quyết định.
- Không đụng `memory/*` (thuộc quyền user — xem CLAUDE.md §4).
- Chỉ đề xuất sửa khi có bằng chứng thật trong session (correction lặp lại, pattern rõ) — không bịa việc để "có cái mà sửa".
- Rà soát chỉ trong phạm vi session đã xác định ở Bước 2 — không gom tri thức từ chủ đề/session khác đang dang dở.
- Giữ nhẹ: session không có gì mới thì đóng nhanh, đừng kéo dài.
