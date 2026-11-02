#!/usr/bin/env bash
# SessionStart hook: nhắc Claude tự dùng agentmemory (MCP, .mcp.json) — recall đầu phiên, save khi có điều đáng nhớ.
# Chạy cả khi startup/resume/compact nên chỉ dẫn không mất sau khi nén ngữ cảnh.

MSG="agentmemory (MCP server 'agentmemory') — TỰ dùng, user không cần nhắc:
1. Ngay khi nhận yêu cầu đầu tiên của phiên: gọi memory_recall (hoặc memory_smart_search) với từ khóa của yêu cầu đó, dùng kết quả làm bối cảnh. Không có kết quả liên quan thì làm tiếp, không báo.
2. Trong phiên, gọi memory_save NGAY (không đợi cuối phiên) khi có: quyết định/chốt phương án của user; sở thích hoặc lời sửa cách làm; tiến độ việc dở dang (đang làm tới đâu, bước tiếp theo); bài học sau lỗi/gỡ rối. Mỗi bản ghi 1-3 câu tiếng Việt, có ngày (YYYY-MM-DD) + chủ đề/đường dẫn liên quan.
3. KHÔNG lưu: API key/secret/nội dung .env; thứ repo đã ghi (code, git log, CLAUDE.md); chuyện vặt chỉ đúng trong lượt này.
4. Lưu im lặng, chỉ nhắc 1 dòng ngắn cuối câu trả lời (vd: '💾 đã lưu agentmemory: ...'). Tool agentmemory không phản hồi thì bỏ qua, không làm gián đoạn việc chính."

ESCAPED=$(printf '%s' "$MSG" | sed 's/\\/\\\\/g; s/"/\\"/g' | awk '{printf "%s\\n", $0}' | sed 's/\\n$//')
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "$ESCAPED"
