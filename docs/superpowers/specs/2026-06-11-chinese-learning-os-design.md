# Chinese Learning OS — Design Spec
**Date:** 2026-06-11  
**Version:** V1.0  
**Scope:** V1 — Skills phase (3 core skills + CLAUDE.md routing)

---

## 1. Overview

**Chinese Learning OS** là hệ thống huấn luyện tiếng Trung dài hạn chạy trên Claude Code.

**Mục tiêu:**
- HSK6: 220-240+
- HSKK Cao cấp: 70-85+
- Giao tiếp tự nhiên với người bản ngữ
- Dạy được HSK1-3

**Platform:** Hybrid — V1 là bộ skills trong Claude Code, V2+ scale thành web app.

---

## 2. Philosophy

Thứ tự ưu tiên:

```
Dùng được > Thi được > Dạy được + Ghi nhớ
```

Activation > Recognition:

```
Biết ≠ Dùng được ≠ Tự tin dùng
```

Output target:

```
50% Điểm thi | 25% Tự nhiên | 25% Cá tính
```

---

## 3. Architecture

**Approach:** 3 independent skills, explicit invocation. Routing logic trong CLAUDE.md (không có router.md riêng).

**Lý do bỏ router.md:** Nếu router chỉ "announce" mà không invoke skill, handover trở thành friction. CLAUDE.md luôn được đọc trước — routing logic đặt ở đây hoạt động mượt hơn và không cần file trung gian.

---

## 4. File Structure

```
CHINESE/
├── CLAUDE.md                          ← constitution: identity, philosophy, routing, ownership
├── .claude/
│   └── skills/
│       ├── learning-strategist.md
│       ├── hsk6-examiner.md
│       └── speaking-coach.md
├── memory/                            ← stable DNA, skills đọc, không ghi
│   ├── user-profile.md
│   ├── writing-dna.md
│   └── learning-preferences.md
├── state/                             ← current state, thay đổi theo session
│   ├── competency.md                  ← Listening/Reading/Writing/Speaking scores
│   ├── activation.md                  ← aggregate: total vocab, rate, avg confidence
│   ├── weekly-goal.md                 ← mục tiêu tuần + từ cần dùng
│   └── session-log.md                 ← lịch sử sessions
├── knowledge/
│   └── vocabulary/
│       ├── tier-a.md                  ← ưu tiên cao nhất
│       ├── tier-b.md
│       └── tier-c.md
├── sessions/
│   ├── writing/                       ← YYYY-MM-DD-topic.md
│   └── speaking/                      ← YYYY-MM-DD-topic.md
└── docs/
    └── superpowers/
        └── specs/
```

---

## 5. Vocabulary Schema

Tier được encode bởi filename (`tier-a.md`, `tier-b.md`, `tier-c.md`).  
**Không lưu Tier trong word entry** — tránh duplicate source of truth.

```markdown
## 信誉
- Pinyin: xìnyù
- Nghĩa: danh tiếng, uy tín
- Usage:
  - Seen: 12
  - Speaking: 5
  - Writing: 3
- Confidence: 80%
- Activation: B
- Last Studied: 2026-06-10
```

**Activation Levels:** A (tự tin dùng) → B → C → D (chưa activate)

**Tier semantics:**
- Tier = độ ưu tiên hiện tại (thay đổi khi Strategist promote/demote)
- Activation = năng lực hiện tại (thay đổi khi dùng từ)
- Strategist query điển hình: "Tier A AND Activation ≤ C" = từ quan trọng nhưng chưa dùng được

**Usage extensibility:** Thêm field vào Usage khi cần (Teaching, Retelling, Listening...) mà không break schema.

**state/activation.md** chỉ chứa aggregate:
```
Total Vocabulary: 2200
Activated (≥B): 750
Activation Rate: 34%
Average Confidence: 68%
Tier A: 120 | Tier B: 450 | Tier C: 1630
```

---

## 6. Skill Interfaces

| Skill | Reads | Writes |
|---|---|---|
| **learning-strategist** | competency, activation, weekly-goal, tier files, session-log, user-profile | weekly-goal, session-log, tier files, activation |
| **hsk6-examiner** | writing-dna, user-profile | sessions/writing/ |
| **speaking-coach** | user-profile, writing-dna, weekly-goal | sessions/speaking/ |

**Cross-skill coordination qua shared state:**  
`weekly-goal.md` là điểm kết nối: Strategist giao từ mục tiêu tuần → Speaking Coach đọc và tự động weave từ đó vào hội thoại.

---

## 7. Routing Rules (CLAUDE.md)

**Hard route** — explicit command, bypass detection:
```
/learning-strategist [args]
/hsk6-examiner [args]
/speaking-coach [args]
```

**Soft route** — intent detection, priority order:

| Priority | Signal | Route |
|---|---|---|
| 1 | Explicit command | → direct |
| 2 | Chứa chữ Trung **VÀ** hỏi điểm/sửa/đánh giá | → hsk6-examiner |
| 3 | Speaking transcript / luyện nói | → speaking-coach |
| 4 | Kế hoạch / backlog / plan / tuần này | → learning-strategist |
| 5 | Ambiguous | → hỏi 1 câu |

**Rules:**
- Confidence cao → route + announce: `[HSK6 Examiner] Đang chấm bài...`
- Confidence thấp → hỏi 1 câu, không đoán
- **One Request = One Skill** — multi-intent request route tới skill phù hợp nhất, skill đó suggest tiếp nếu cần
- **No skill chaining** trong V1

---

## 8. Memory File Templates

Memory files là stable DNA — skills đọc, không ghi. User tự cập nhật khi thay đổi.

### memory/user-profile.md
```markdown
# User Profile
- Role: Business Analyst
- Chinese level: ~3 years
- Exam: HSK6 (target 220-240+) + HSKK Cao cấp (70-85+)
- Exam date: T12/2026 - T01/2027
- Long-term goals: giao tiếp tự nhiên, môi trường công việc Trung, dạy HSK1-3

## Current Constraints
- Tự học: 2h/ngày (sáng)
- Học trung tâm: 3 buổi/tuần
- Dạy HSK1: 3 buổi/tuần

## Speaking Split
- HSKK: 40%
- Practical Communication: 60%
```

### memory/writing-dna.md
```markdown
# Writing DNA

## Style
- Dẫn nhập ngắn → lập luận rõ → ví dụ cá nhân → kết luận suy ngẫm
- Quan điểm trực tiếp, không lòng vòng
- Framework: 观点 → 原因 → 例子 → 总结

## Writing Principles
- Đơn giản nhưng điểm cao
- Tự nhiên nhưng ấn tượng
- Ưu tiên ví dụ cá nhân thật
- Tránh từ quá hoa mỹ, sáo rỗng

## Preserve Rules
- Giữ 90% nội dung gốc
- Giữ 90% văn phong gốc
- KHÔNG viết lại hoàn toàn
- KHÔNG biến thành văn mẫu

## Score Weights
- 50% điểm thi | 25% tự nhiên | 25% cá tính
```

### memory/learning-preferences.md
```markdown
# Learning Preferences

## Thích
- Tương tác, tranh luận, triển khai ý, speaking

## Không thích
- Học thuộc máy móc
- Flashcard đơn thuần

## Knowledge Activation Priority
1. Speaking
2. Writing
3. Teaching
4. Retelling
5. Flashcard
```

---

## 9. CLAUDE.md Structure (7 sections)

| # | Section | Nội dung |
|---|---|---|
| 1 | **Identity** | Hệ thống là gì, mục tiêu tổng quát |
| 2 | **Philosophy** | Dùng được > Thi được, Activation > Recognition, 50/25/25 |
| 3 | **Routing Rules** | Intent detection, priority order, confidence rules |
| 4 | **Memory Ownership** | Skill nào đọc memory file nào (không "đọc hết") |
| 5 | **Operating Rules** | Không flashcard-first, không văn mẫu, One Request = One Skill... |
| 6 | **State Ownership** | File nào tồn tại, skill nào cập nhật — không có schema |
| 7 | **Skill Catalog** | Danh sách 3 skills + 1 dòng mô tả |

---

## 10. State Schema

### state/competency.md
Cập nhật thủ công (user hoặc Strategist sau khi thi/test). Skills chỉ đọc.

```markdown
# Competency
Last Updated: YYYY-MM-DD

| Skill | Current | Target | Gap |
|---|---|---|---|
| Listening | 65 | 90+ | -25 |
| Reading | 70 | 90+ | -20 |
| Writing | 180 | 220-240 | -40 |
| Speaking | 55 | 70-85 | -15 |

## HSK6 Estimate: ~180 | Target: 220-240+
## HSKK Estimate: ~55 | Target: 70-85+
```

### state/weekly-goal.md
Strategist ghi. Speaking Coach đọc để weave từ mục tiêu vào hội thoại.

```markdown
# Weekly Goal
Week: YYYY-MM-DD to YYYY-MM-DD

## Focus
- Primary: [skill focus] — [lý do cụ thể]
- Secondary: [mục tiêu activation]

## Target Vocabulary (Speaking Coach dùng tuần này)
- 词1, 词2, 词3, ...

## Sessions Planned
- Writing: N | Speaking: N
```

### state/session-log.md
Examiner và Speaking Coach append sau mỗi session. Strategist đọc để review tuần.

```markdown
## YYYY-MM-DD | [Writing|Speaking] | [Skill Name]
- Topic: ...
- Score / Assessment: ...
- Notes: ...
- Words used: ...
```

### state/activation.md
Strategist tính toán và cập nhật (batch, không real-time). Chỉ chứa aggregate.

```markdown
# Vocabulary Activation
Last Updated: YYYY-MM-DD

Total: 0 | Activated (≥B): 0 | Rate: 0%
Avg Confidence: 0%
Tier A: 0 | Tier B: 0 | Tier C: 0
```

---

## 11. State Ownership

**Write ownership — ai được ghi vào file nào:**

| File | Writer | Reader |
|---|---|---|
| competency.md | User / Strategist (manual) | Strategist |
| weekly-goal.md | Strategist | Speaking Coach, Strategist |
| session-log.md | HSK6 Examiner, Speaking Coach | Strategist |
| activation.md | Strategist (batch update) | Strategist |
| knowledge/vocabulary/tier-*.md | Strategist (promote/demote + batch update từ session-log) | Strategist, Speaking Coach |
| sessions/writing/ | HSK6 Examiner | — |
| sessions/speaking/ | Speaking Coach | — |
| memory/* | User only | All skills |

**Activation update flow (Option C):**
```
HSK6 Examiner / Speaking Coach
  → append "Words used: ..." vào session-log.md

Strategist (khi được gọi)
  → đọc session-log entries chưa processed
  → update Seen/Speaking/Writing trong tier files
  → recalculate Activation level
  → update activation.md aggregate
```

---

## 12. Out of Scope (V1)

- Grammar knowledge base
- Router.md (replaced by CLAUDE.md routing)
- Skill chaining / multi-skill orchestration
- Web application layer
- Audio/voice input
- Roles: Vocabulary Coach, Teaching Coach, Retelling Coach, Cognitive Coach, HSKK Examiner, Writing Coach
- Automated weekly reports

---

## 13. V2 Signals

Trigger mở rộng khi:
- Backlog vượt 500 từ → cân nhắc index/search trong tier files
- Cần thêm role → thêm skill file + update CLAUDE.md Skill Catalog
- State query phức tạp → migrate từ markdown sang structured format
- Muốn skill chaining → implement router.md với Skill() invocation
