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

## Bước 2 — Rà soát Skill (bắt buộc)

Quét **2 nguồn** để tìm thứ cần đưa vào skill:

**Nguồn A — Thay đổi file (git):**
1. Xem file bị tạo/sửa trong session: `.claude/skills/**/SKILL.md`, `.claude/skills/**/references/**`, và `CLAUDE.md`.
2. Với mỗi thay đổi: hỏi "thay đổi này đã nhất quán chưa? có cần phản ánh sang skill khác / routing / catalog không?" (vd sửa 1 skill nhưng quên update §7 Catalog trong CLAUDE.md).

**Nguồn B — Tri thức ẩn trong hội thoại:**
Quét toàn bộ session tìm:
- **Correction lặp lại** — user sửa cùng 1 lỗi/thói quen ≥ 2 lần → nên thành quy tắc trong skill.
- **Pattern / quy tắc mới** — cách làm mới được thống nhất mà skill chưa ghi.
- **Bước thủ công lặp đi lặp lại** — việc tay làm nhiều lần → nên đưa thành command/bước trong skill.

**Map & trình bày:**
Map mỗi phát hiện tới **skill đích**: `learning-strategist`, `hsk6-examiner`, `speaking-coach`, `exercise-generator`, `teaching-coach`, `doc-analyzer`, `close-session`, hoặc `CLAUDE.md`.

Trình bày bảng:

| # | Phát hiện | Nguồn | Skill đích | Đề xuất sửa cụ thể |
|---|---|---|---|---|
| 1 | ... | A/B | ... | ... |

**Cổng duyệt (bắt buộc):**
- Chờ user duyệt **từng mục**. Không tự ý sửa.
- Mục được duyệt → thực hiện sửa vào SKILL.md / CLAUDE.md tương ứng.
- Mục không duyệt → bỏ qua, không lưu.
- Nếu quét xong không có phát hiện nào → nói rõ "không có gì cần update".

## Bước 3 — Đóng
- Nếu không có gì → báo "Session sạch, đã đóng."
- Nếu có sửa → báo tóm tắt: đã sửa mục nào, vào skill nào. Rồi đóng.

## Quy tắc bất biến
- Không tự commit, không tự sửa khi chưa được duyệt.
- Không đụng `memory/*` (thuộc quyền user — xem CLAUDE.md §4).
- Chỉ đề xuất sửa khi có bằng chứng thật trong session (correction lặp lại, pattern rõ) — không bịa việc để "có cái mà sửa".
- Giữ nhẹ: session không có gì mới thì đóng nhanh, đừng kéo dài.
