#!/usr/bin/env bash
# SessionStart hook: so bản Artifact học từ vựng (điện thoại) với nội dung repo.
# Render biến thể Artifact -> sha256 -> so với .claude/skills/vocab-study/artifact-published.sha
# (hash của bản ĐÃ publish lần cuối). Lệch -> nhắc Claude republish + ghi lại hash.
# Hook không tự publish được (Artifact là tool của Claude) nên chỉ phát hiện + nhắc.

cd "$(dirname "$0")/../.." || exit 0
STATE=.claude/skills/vocab-study/artifact-published.sha
TMP=.git/_vocab-artifact-check.html

VOCAB_ARTIFACT_OUT="$TMP" PYTHONIOENCODING=utf-8 python .claude/skills/vocab-study/scripts/render_html.py >/dev/null 2>&1 || { rm -f "$TMP"; exit 0; }
NEW=$(sha256sum "$TMP" | cut -d' ' -f1)
OLD=$(cat "$STATE" 2>/dev/null | tr -d '[:space:]')
[ "$NEW" = "$OLD" ] && { rm -f "$TMP"; exit 0; }

MSG="Bản Artifact học từ vựng trên điện thoại (https://claude.ai/artifact/9R3nYoyks9WtC73VdhDPm4) đang LỆCH nội dung repo. User đã duyệt tự động cập nhật: sau khi xong yêu cầu đầu tiên của phiên, tự republish (không hỏi lại), theo SKILL.md vocab-study mục 'Bản Artifact':
1. VOCAB_ARTIFACT_OUT=<file trong scratchpad> python .claude/skills/vocab-study/scripts/render_html.py
2. Artifact read url trên (action read, path index.html), rồi Read vài dòng cuối file đã lưu để được tính là đã xem; publish file mới lên cùng url (KHÔNG truyền capabilities — giữ nguyên db).
3. Ghi sha256 của file vừa publish vào ${STATE} (sha256sum <file> | cut -d' ' -f1). Hash hiện tại của repo: ${NEW}. Nếu render lại ra hash khác (đang có tiến trình sửa data) thì ghi hash của file thực sự đã publish.
4. Commit ${STATE} về main (meta, theo Git Hygiene — chạy git branch --show-current trước), hoặc để close-session gom.
Báo user 1 dòng cuối câu trả lời: 'Đã cập nhật bản điện thoại'."

ESCAPED=$(printf '%s' "$MSG" | sed 's/\\/\\\\/g; s/"/\\"/g' | awk '{printf "%s\\n", $0}' | sed 's/\\n$//')
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "$ESCAPED"
rm -f "$TMP"
