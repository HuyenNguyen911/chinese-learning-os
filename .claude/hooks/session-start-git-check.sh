#!/usr/bin/env bash
# SessionStart hook: fetch + report + auto-pull main before first request.
cd "$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0

git fetch origin main >/dev/null 2>&1

BRANCH=$(git branch --show-current 2>/dev/null)
BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null)
DIRTY=$(git status --porcelain 2>/dev/null)

if [ -z "$BEHIND" ] || [ "$BEHIND" = "0" ]; then
  MSG="Git check: nhánh '$BRANCH' đã cập nhật ngang origin/main."
elif [ -n "$DIRTY" ]; then
  MSG="⚠️ Git check: nhánh '$BRANCH' đang chậm hơn origin/main $BEHIND commit, NHƯNG có thay đổi chưa commit — KHÔNG tự pull. Cần xử lý thủ công trước khi làm tiếp."
else
  if [ "$BRANCH" = "main" ]; then
    if git pull --ff-only origin main >/dev/null 2>&1; then
      MSG="✅ Git check: đã pull $BEHIND commit mới từ origin/main vào '$BRANCH'."
    else
      MSG="⚠️ Git check: nhánh '$BRANCH' chậm hơn origin/main $BEHIND commit nhưng pull --ff-only thất bại (có thể diverge) — cần xử lý thủ công."
    fi
  else
    MSG="ℹ️ Git check: đang ở nhánh '$BRANCH' (không phải main), origin/main có $BEHIND commit mới. Không tự pull nhánh feature — nhắc theo Git Hygiene rule (mục 9 CLAUDE.md) nếu cần merge main vào nhánh này."
  fi
fi

ESCAPED=$(printf '%s' "$MSG" | sed 's/\\/\\\\/g; s/"/\\"/g')
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"},"systemMessage":"%s"}\n' "$ESCAPED" "$ESCAPED"
