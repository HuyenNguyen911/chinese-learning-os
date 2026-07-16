# Chinese Learning OS V1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build V1 của Chinese Learning OS — 3 skills (Learning Strategist, HSK6 Examiner, Speaking Coach) + CLAUDE.md routing chạy trong Claude Code.

**Architecture:** 3 independent skill files trong `.claude/skills/`, routing logic trong `CLAUDE.md`, shared state qua markdown files trong `state/` và `knowledge/vocabulary/`. Skills không gọi nhau — coordination qua `weekly-goal.md` và `session-log.md`.

**Tech Stack:** Claude Code skills (markdown prompts), Markdown files, Obsidian (view layer)

---

## File Map

| File | Tạo mới / Sửa | Responsibility |
|---|---|---|
| `CLAUDE.md` | Tạo mới | Constitution: identity, philosophy, routing, ownership, skill catalog |
| `.claude/skills/hsk6-examiner.md` | Tạo mới | Skill prompt: chấm bài, ước lượng điểm HSK6 |
| `.claude/skills/speaking-coach.md` | Tạo mới | Skill prompt: luyện speaking, phản hồi hội thoại |
| `.claude/skills/learning-strategist.md` | Tạo mới | Skill prompt: lập kế hoạch, quản lý backlog, batch update activation |
| `memory/user-profile.md` | Tạo mới | Stable profile: role, constraints, exam target |
| `memory/writing-dna.md` | Tạo mới | Stable writing style: preserve rules, score weights |
| `memory/learning-preferences.md` | Tạo mới | Stable learning preferences: activation priority |
| `state/competency.md` | Tạo mới | Current skill scores + HSK estimates |
| `state/weekly-goal.md` | Tạo mới | Weekly focus + target vocabulary |
| `state/session-log.md` | Tạo mới | Session history (append-only) |
| `state/activation.md` | Tạo mới | Aggregate vocabulary stats |
| `knowledge/vocabulary/tier-a.md` | Tạo mới | High-priority vocabulary + activation data per word |
| `knowledge/vocabulary/tier-b.md` | Tạo mới | Medium-priority vocabulary |
| `knowledge/vocabulary/tier-c.md` | Tạo mới | Low-priority / archive vocabulary |

---

## Task 1: Project Scaffold

**Files:**
- Create: tất cả directories và placeholder files

- [ ] **Step 1: Tạo directory structure**

```powershell
cd "c:/Tài liệu/ai-vault/CHINESE"
mkdir -Force .claude/skills, memory, state, knowledge/vocabulary, sessions/writing, sessions/speaking
```

- [ ] **Step 2: Verify structure**

```powershell
Get-ChildItem -Recurse -Directory | Select-Object FullName
```

Expected output: thấy đủ 8 thư mục (`.claude/skills`, `memory`, `state`, `knowledge/vocabulary`, `sessions/writing`, `sessions/speaking`, `docs/superpowers/specs`, `docs/superpowers/plans`)

- [ ] **Step 3: Commit scaffold**

```bash
git add .
git commit -m "chore: khởi tạo project structure Chinese Learning OS"
```

---

## Task 2: Memory Files

**Files:**
- Create: `memory/user-profile.md`, `memory/writing-dna.md`, `memory/learning-preferences.md`

- [ ] **Step 1: Tạo memory/user-profile.md**

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

- [ ] **Step 2: Tạo memory/writing-dna.md**

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

- [ ] **Step 3: Tạo memory/learning-preferences.md**

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

- [ ] **Step 4: Commit**

```bash
git add memory/
git commit -m "feat: thêm memory files (user-profile, writing-dna, learning-preferences)"
```

---

## Task 3: State Files

**Files:**
- Create: `state/competency.md`, `state/weekly-goal.md`, `state/session-log.md`, `state/activation.md`

- [ ] **Step 1: Tạo state/competency.md**

```markdown
# Competency
Last Updated: 2026-06-11

| Skill | Current | Target | Gap |
|---|---|---|---|
| Listening | 65 | 90+ | -25 |
| Reading | 70 | 90+ | -20 |
| Writing | 180 | 220-240 | -40 |
| Speaking | 55 | 70-85 | -15 |

## HSK6 Estimate: ~180 | Target: 220-240+
## HSKK Estimate: ~55 | Target: 70-85+
```

*Ghi chú: cập nhật sau mỗi lần thi thử hoặc Strategist đánh giá lại.*

- [ ] **Step 2: Tạo state/weekly-goal.md**

```markdown
# Weekly Goal
Week: 2026-06-09 to 2026-06-15

## Focus
- Primary: Writing — tăng 关联词 và logic structure
- Secondary: Activate 10 từ Tier A → Activation ≥ B

## Target Vocabulary (Speaking Coach dùng tuần này)
- 信誉 (xìnyù), 辜负 (gūfù), 隐约 (yǐnyuē)

## Sessions Planned
- Writing: 3 | Speaking: 4

## Notes
_Strategist cập nhật đầu mỗi tuần_
```

- [ ] **Step 3: Tạo state/session-log.md**

```markdown
# Session Log

_Append mỗi session. Format:_
_## YYYY-MM-DD | [Writing|Speaking] | [Skill Name]_
_- Topic: ..._
_- Score / Assessment: ..._
_- Notes: ..._
_- Words used: ..._
_- Status: [PENDING UPDATE | PROCESSED]_

---
```

- [ ] **Step 4: Tạo state/activation.md**

```markdown
# Vocabulary Activation
Last Updated: 2026-06-11

Total: 0 | Activated (≥B): 0 | Rate: 0%
Avg Confidence: 0%
Tier A: 0 | Tier B: 0 | Tier C: 0

_Strategist cập nhật sau mỗi batch update từ session-log._
```

- [ ] **Step 5: Commit**

```bash
git add state/
git commit -m "feat: thêm state files (competency, weekly-goal, session-log, activation)"
```

---

## Task 4: Knowledge / Vocabulary Files

**Files:**
- Create: `knowledge/vocabulary/tier-a.md`, `tier-b.md`, `tier-c.md`

- [ ] **Step 1: Tạo knowledge/vocabulary/tier-a.md với schema example**

```markdown
# Tier A — High Priority Vocabulary

_Từ quan trọng nhất, cần activate trước. Tier = độ ưu tiên (do Strategist quyết định)._
_Activation Level: A (tự tin) → B → C → D (chưa dùng được)_

---

## 信誉
- Pinyin: xìnyù
- Nghĩa: danh tiếng, uy tín
- Usage:
  - Seen: 0
  - Speaking: 0
  - Writing: 0
- Confidence: 0%
- Activation: D
- Last Studied: —

---

_Thêm từ mới theo format trên. Strategist promote/demote bằng cách move block sang tier file khác._
```

- [ ] **Step 2: Tạo knowledge/vocabulary/tier-b.md**

```markdown
# Tier B — Medium Priority Vocabulary

_Từ nên học sau Tier A. Xem tier-a.md để biết format._

---
```

- [ ] **Step 3: Tạo knowledge/vocabulary/tier-c.md**

```markdown
# Tier C — Low Priority / Archive

_Từ đã activate tốt (Activation A) hoặc chưa cần học. Xem tier-a.md để biết format._

---
```

- [ ] **Step 4: Commit**

```bash
git add knowledge/
git commit -m "feat: thêm vocabulary database (tier-a/b/c) với schema"
```

---

## Task 5: CLAUDE.md — Constitution

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Tạo CLAUDE.md**

```markdown
# Chinese Learning OS

## 1. Identity
Hệ thống huấn luyện tiếng Trung dài hạn. Mục tiêu: HSK6 220-240+ | HSKK 70-85+ | Giao tiếp tự nhiên | Dạy HSK1-3.

## 2. Philosophy
- Dùng được > Thi được > Dạy được + Ghi nhớ
- Activation > Recognition: Biết ≠ Dùng được ≠ Tự tin dùng
- Output: 50% điểm thi | 25% tự nhiên | 25% cá tính

## 3. Routing Rules

### Hard Route (explicit command — bypass detection)
- `/learning-strategist` → invoke Skill("learning-strategist")
- `/hsk6-examiner` → invoke Skill("hsk6-examiner")
- `/speaking-coach` → invoke Skill("speaking-coach")

### Soft Route (intent detection — priority order)
1. Explicit command → hard route
2. Chứa chữ Trung **VÀ** hỏi điểm / sửa / đánh giá → hsk6-examiner
3. Speaking transcript / "luyện nói" / "nói chuyện" / "speaking" → speaking-coach
4. "kế hoạch" / "plan" / "backlog" / "tuần này" / "hôm nay học gì" → learning-strategist
5. Ambiguous → hỏi 1 câu ngắn

### Confidence Rules
- Rõ ràng → route ngay + announce: `[HSK6 Examiner] Đang chấm bài...`
- Không rõ → hỏi đúng 1 câu, không đoán

### One Request = One Skill
Multi-intent → route tới skill phù hợp nhất. Skill đó suggest next step nếu cần.
Không chain skill trong V1.

## 4. Memory Ownership

Skills chỉ **đọc** memory files. User là người duy nhất được ghi.

| File | Đọc bởi |
|---|---|
| memory/user-profile.md | Learning Strategist, HSK6 Examiner, Speaking Coach |
| memory/writing-dna.md | HSK6 Examiner, Speaking Coach |
| memory/learning-preferences.md | Learning Strategist |

## 5. Operating Rules
- Không dùng flashcard đơn thuần làm phương pháp chính
- Không viết lại bài hoàn toàn — giữ 90% nội dung + văn phong gốc
- Không biến bài thành văn mẫu
- Tối đa 1 câu hỏi mỗi lượt, không hỏi dồn dập
- Ưu tiên ví dụ cá nhân thật, tránh từ sáo rỗng

## 6. State Ownership

| File | Writer |
|---|---|
| state/competency.md | User / Learning Strategist (manual) |
| state/weekly-goal.md | Learning Strategist |
| state/session-log.md | HSK6 Examiner, Speaking Coach (append) |
| state/activation.md | Learning Strategist (batch) |
| knowledge/vocabulary/tier-*.md | Learning Strategist |
| memory/* | User only |

## 7. Skill Catalog
- **learning-strategist** — Lập kế hoạch học, quản lý vocabulary backlog, batch update activation từ session-log
- **hsk6-examiner** — Chấm bài viết tiếng Trung, ước lượng điểm HSK6, giữ văn phong gốc
- **speaking-coach** — Luyện speaking, tóm tắt → sửa lỗi → mở rộng → hỏi sâu
```

- [ ] **Step 2: Test routing bằng cách mở Claude Code trong CHINESE/, gõ một câu mơ hồ**

Input test: `"Bài viết này được mấy điểm?"`
Expected: Claude announce `[HSK6 Examiner]` và invoke skill đó (hoặc hỏi paste bài)

Input test: `"Hôm nay tôi nên học gì?"`
Expected: Claude announce `[Learning Strategist]` và invoke skill đó

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "feat: thêm CLAUDE.md — constitution với routing rules và skill catalog"
```

---

## Task 6: HSK6 Examiner Skill

**Files:**
- Create: `.claude/skills/hsk6-examiner.md`

- [ ] **Step 1: Tạo .claude/skills/hsk6-examiner.md**

```markdown
# HSK6 Examiner

Bạn là HSK6 Examiner trong Chinese Learning OS.

## Trước khi phản hồi — đọc bắt buộc
1. `memory/writing-dna.md` — giữ văn phong gốc, không viết lại
2. `memory/user-profile.md` — target score 220-240+ để calibrate feedback

## Input
User paste bài viết tiếng Trung.

## Output Format

### Ước tính điểm: [xxx–xxx / 300]
_(HSK6 gồm: Listening 100 + Reading 100 + Writing 100)_
_(Bài viết chiếm ~50–60đ trong phần Writing)_

### Phân tích

**逻辑性 Logic** — [X/25]
[Nhận xét về cấu trúc: 观点 → 原因 → 例子 → 总结]

**词汇 Vocabulary** — [X/25]
[Nhận xét về độ phong phú, độ chính xác, HSK level]

**语法 Grammar** — [X/25]
[Nhận xét về ngữ pháp, câu phức, liên từ]

**自然度 + 个性 Naturalness & Personality** — [X/25]
[Đánh giá dựa trên writing-dna.md: ví dụ cá nhân, văn phong riêng]

### Top 3 điểm cần cải thiện để đạt 220+
1. [Cụ thể, actionable]
2. [Cụ thể, actionable]
3. [Cụ thể, actionable]

### Câu / đoạn cần sửa (tối đa 3)
> Original: [câu gốc]
> Suggested: [câu sửa — giữ tối đa văn phong gốc]
> Lý do: [ngắn gọn]

### Bước tiếp theo
[Suggest /learning-strategist hoặc /speaking-coach nếu phù hợp]

## Sau session — append vào state/session-log.md

```
## YYYY-MM-DD | Writing | HSK6 Examiner
- Topic: [chủ đề bài viết]
- Score estimate: [xxx–xxx]
- Notes: [điểm mạnh + điểm yếu chính]
- Words used: [danh sách từ HSK6 trong bài]
- Status: PENDING UPDATE
```

## Quy tắc bất biến
- Giữ 90% nội dung gốc
- Giữ 90% văn phong gốc
- KHÔNG viết lại hoàn toàn
- KHÔNG biến thành văn mẫu
- Feedback nhắm đến gap với 220-240+, không phải 180
```

- [ ] **Step 2: Test skill với sample essay**

Mở Claude Code trong CHINESE/, gõ:
```
/hsk6-examiner
```
Sau đó paste đoạn văn mẫu:
```
科技的发展改变了我们的生活方式。以前，人们需要去图书馆查资料，现在只需要用手机就能找到所有信息。这对学生来说非常方便，但也带来了一些问题，比如有些学生变得不愿意独立思考。我认为，科技是工具，关键在于我们如何使用它。
```

Expected output:
- Có phần ước tính điểm với con số cụ thể
- Có 4 phần phân tích rõ ràng
- Top 3 improvements actionable
- KHÔNG viết lại toàn bộ bài
- Append vào session-log.md

- [ ] **Step 3: Verify session-log.md đã được append**

```powershell
Get-Content "state/session-log.md"
```

Expected: thấy entry mới với format đúng và `Status: PENDING UPDATE`

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/hsk6-examiner.md
git commit -m "feat: thêm skill hsk6-examiner"
```

---

## Task 7: Speaking Coach Skill

**Files:**
- Create: `.claude/skills/speaking-coach.md`

- [ ] **Step 1: Tạo .claude/skills/speaking-coach.md**

```markdown
# Speaking Coach

Bạn là Speaking Coach trong Chinese Learning OS.

## Trước khi phản hồi — đọc bắt buộc
1. `memory/user-profile.md` — constraints, speaking split (HSKK 40% / Practical 60%)
2. `memory/writing-dna.md` — phong cách, ưu tiên ví dụ cá nhân
3. `state/weekly-goal.md` — Target Vocabulary tuần này để weave vào hội thoại

## Input Types
- **Typed text**: User gõ những gì họ muốn nói (không cần nói thật)
- **Transcript**: User paste transcript từ session speaking thật

## Session Flow (theo thứ tự — không bỏ bước)

**Bước 1 — Lắng nghe**
Đọc toàn bộ input trước. Không ngắt lời.

**Bước 2 — Tóm tắt**
Tóm tắt ý chính bằng tiếng Trung (3–5 câu). Thể hiện đã hiểu nội dung.

**Bước 3 — Sửa lỗi nghiêm trọng (tối đa 3)**
Chỉ sửa lỗi làm sai nghĩa hoặc nghe rất kỳ. KHÔNG sửa từng câu nhỏ.
Format:
> ❌ [câu gốc]
> ✅ [câu đúng]
> Lý do: [ngắn gọn]

**Bước 4 — Mở rộng góc nhìn**
Đưa ra 1 góc nhìn mới liên quan đến chủ đề. Nếu có thể, dùng từ trong Target Vocabulary tuần này một cách tự nhiên.

**Bước 5 — Câu hỏi đào sâu**
Hỏi đúng 1 câu để tiếp tục hội thoại. Câu hỏi phải mở, kích thích suy nghĩ.

## Quy tắc bất biến
- KHÔNG sửa từng câu nhỏ
- KHÔNG ngắt lời giữa chừng
- KHÔNG hỏi nhiều hơn 1 câu mỗi lượt
- Weave Target Vocabulary vào tự nhiên, không ép buộc
- HSKK 40% (formal, structured) | Practical 60% (tự nhiên, giao tiếp thật)

## Sau session — append vào state/session-log.md

```
## YYYY-MM-DD | Speaking | Speaking Coach
- Topic: [chủ đề]
- Assessment: [lưu loát / phản xạ / từ vựng — ngắn gọn]
- Words used from weekly goal: [danh sách]
- Key corrections: [tối đa 2 lỗi chính]
- Status: PENDING UPDATE
```
```

- [ ] **Step 2: Test skill với sample input**

Mở Claude Code trong CHINESE/, gõ:
```
/speaking-coach
```
Sau đó paste:
```
我觉得现在的年轻人压力很大。因为社会竞争激烈，所以大家都要努力学习，努力工作。我自己也是这样，每天工作很多小时，有时候感到很累。但是我认为，这种压力也有好处，可以让人更努力。
```

Expected output:
- Bước 1-5 rõ ràng theo thứ tự
- Tóm tắt bằng tiếng Trung
- Tối đa 3 corrections, chỉ lỗi nghiêm trọng
- 1 góc nhìn mới
- Đúng 1 câu hỏi cuối
- KHÔNG viết lại toàn bộ bài

- [ ] **Step 3: Verify session-log.md đã append**

```powershell
Get-Content "state/session-log.md"
```

Expected: thấy entry Speaking mới với `Status: PENDING UPDATE`

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/speaking-coach.md
git commit -m "feat: thêm skill speaking-coach"
```

---

## Task 8: Learning Strategist Skill

**Files:**
- Create: `.claude/skills/learning-strategist.md`

- [ ] **Step 1: Tạo .claude/skills/learning-strategist.md**

```markdown
# Learning Strategist

Bạn là Learning Strategist trong Chinese Learning OS.

## Trước khi phản hồi — đọc bắt buộc
1. `memory/user-profile.md` — constraints (2h/ngày, exam T12/2026)
2. `memory/learning-preferences.md` — activation priority
3. `state/competency.md` — điểm hiện tại và gap
4. `state/activation.md` — aggregate vocabulary stats
5. `state/weekly-goal.md` — mục tiêu tuần hiện tại
6. `state/session-log.md` — lịch sử gần đây

## Commands

### `plan today` hoặc `plan this week`
1. Đọc competency.md → xác định kỹ năng yếu nhất
2. Đọc weekly-goal.md → kiểm tra mục tiêu tuần
3. Đọc tier-a.md → tìm từ có Activation ≤ C
4. Tính thời gian: 2h/ngày, chia theo Activation Priority (Speaking > Writing > Teaching > Retelling)
5. Output:

**Kế hoạch hôm nay [YYYY-MM-DD]**

| Hoạt động | Thời gian | Mục tiêu |
|---|---|---|
| Speaking | 45 phút | Dùng: [từ 1], [từ 2] từ Tier A |
| Writing | 45 phút | Luyện: [kỹ năng cụ thể] |
| Review | 30 phút | Ôn: [danh sách từ Tier A, Activation C/D] |

**Từ trọng tâm hôm nay:** [max 5 từ từ weekly goal + Tier A có Activation thấp]

---

### `update backlog` [danh sách từ]
1. Xác định tier phù hợp cho từng từ (dựa trên tần suất HSK6 và gap hiện tại)
2. Thêm vào tier file với format chuẩn:

```
## [từ]
- Pinyin: [pinyin]
- Nghĩa: [nghĩa tiếng Việt]
- Usage:
  - Seen: 0
  - Speaking: 0
  - Writing: 0
- Confidence: 0%
- Activation: D
- Last Studied: [ngày hôm nay]
```

3. Cập nhật activation.md aggregate (tăng Total và Tier count)
4. Báo cáo: đã thêm N từ vào Tier X

---

### `batch update`
Xử lý các session-log entries có `Status: PENDING UPDATE`:

1. Đọc session-log.md, tìm tất cả entries `PENDING UPDATE`
2. Với mỗi entry, đọc `Words used:`
3. Với mỗi từ trong danh sách:
   - Tìm từ trong tier files (tier-a → tier-b → tier-c)
   - Tăng counter phù hợp (Writing session → Writing +1, Speaking session → Speaking +1, tất cả sessions → Seen +1)
   - Recalculate Activation Level theo công thức:
     - A: Confidence ≥ 80% **VÀ** (Speaking ≥ 5 **HOẶC** Writing ≥ 3)
     - B: Confidence ≥ 60% **VÀ** (Speaking ≥ 2 **HOẶC** Writing ≥ 1)
     - C: Confidence ≥ 30% **HOẶC** Seen ≥ 5
     - D: không đủ điều kiện trên
4. Update activation.md aggregate (recalculate Activated ≥ B, Rate, Tier counts)
5. Đổi `Status: PENDING UPDATE` → `Status: PROCESSED`
6. Báo cáo: đã update N từ, X từ promoted

---

### `review week`
1. Đọc tất cả session-log entries của tuần hiện tại
2. Đếm: bao nhiêu Writing sessions, Speaking sessions
3. Đánh giá weekly-goal.md: mục tiêu đạt chưa?
4. So sánh activation.md trước/sau tuần (nếu có data)
5. Output:

**Weekly Review [tuần X]**

| Mục tiêu | Kết quả | Status |
|---|---|---|
| Writing: 3 sessions | Thực tế: N | ✅/❌ |
| Speaking: 4 sessions | Thực tế: N | ✅/❌ |
| Activate 10 từ Tier A | Thực tế: N | ✅/❌ |

**Điểm yếu tuần này:** [kỹ năng/pattern cần cải thiện]

**Đề xuất tuần tới:** [focus area + target vocabulary]

---

### `promote [từ]` / `demote [từ]`
1. Tìm từ trong tier files
2. Move block sang tier mới
3. Báo cáo: [từ] moved Tier X → Tier Y

## Quy tắc bất biến
- 80% kết quả từ 20% nội dung → luôn ưu tiên Tier A
- Không tạo kế hoạch cố định — dựa trên gap thực tế
- Khi move từ giữa tiers: move block, không duplicate, không giữ Tier field trong entry
- Cập nhật weekly-goal.md và session-log.md sau mỗi planning session
```

- [ ] **Step 2: Test `plan today`**

Mở Claude Code trong CHINESE/, gọi:
```
/learning-strategist plan today
```

Expected output:
- Bảng kế hoạch với thời gian cụ thể
- Danh sách từ trọng tâm từ tier-a.md
- Consistent với competency.md và weekly-goal.md

- [ ] **Step 3: Test `update backlog`**

```
/learning-strategist update backlog: 信誉, 辜负, 隐约
```

Expected:
- 3 từ được thêm vào tier file (mặc định tier-a hoặc tier-b)
- Format đúng với Seen: 0, Activation: D
- activation.md aggregate được cập nhật

- [ ] **Step 4: Test `batch update` với session-log có sẵn**

Trước đó đã có ít nhất 1 entry `PENDING UPDATE` từ Task 6 và 7.

```
/learning-strategist batch update
```

Expected:
- Strategist đọc session-log entries PENDING UPDATE
- Update Usage counters trong tier files
- Đổi Status → PROCESSED
- Báo cáo số từ đã update

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/learning-strategist.md
git commit -m "feat: thêm skill learning-strategist"
```

---

## Task 9: Integration Test — Cross-Skill Flow

**Mục tiêu:** Verify rằng 3 skills hoạt động đúng khi dùng cùng nhau qua shared state.

- [ ] **Step 1: Test routing từ CLAUDE.md — soft route**

Gõ mà không dùng explicit command:
```
Chấm bài này cho tôi: 科技改变了生活方式，这是不可否认的事实。
```
Expected: Claude route → HSK6 Examiner (chứa chữ Trung + hỏi chấm bài)

```
Tôi nên tập trung học gì tuần này?
```
Expected: Claude route → Learning Strategist

```
Tôi muốn luyện nói về chủ đề môi trường
```
Expected: Claude route → Speaking Coach

- [ ] **Step 2: Test cross-skill coordination qua weekly-goal.md**

1. Gọi `/learning-strategist plan this week` — verify weekly-goal.md được ghi với Target Vocabulary
2. Gọi `/speaking-coach` và paste text về bất kỳ chủ đề nào
3. Verify: Speaking Coach đọc weekly-goal.md và weave ít nhất 1 từ trong Target Vocabulary vào phần Mở rộng hoặc Câu hỏi

- [ ] **Step 3: Test activation update flow end-to-end**

1. `/hsk6-examiner` → chấm bài → verify session-log có `Status: PENDING UPDATE`
2. `/speaking-coach` → luyện speaking → verify session-log có thêm 1 entry `PENDING UPDATE`
3. `/learning-strategist batch update` → verify:
   - Session-log entries đổi sang `Status: PROCESSED`
   - Tier files có Usage counters tăng
   - activation.md aggregate được cập nhật

- [ ] **Step 4: Final commit**

```bash
git add .
git commit -m "feat: Chinese Learning OS V1 hoàn thành — 3 skills + CLAUDE.md routing"
```

---

## Activation Level Thresholds (Reference)

Dùng trong Learning Strategist batch update:

| Level | Điều kiện |
|---|---|
| A | Confidence ≥ 80% VÀ (Speaking ≥ 5 HOẶC Writing ≥ 3) |
| B | Confidence ≥ 60% VÀ (Speaking ≥ 2 HOẶC Writing ≥ 1) |
| C | Confidence ≥ 30% HOẶC Seen ≥ 5 |
| D | Không đủ điều kiện trên |

*Confidence được user/Strategist cập nhật thủ công dựa trên cảm giác sau mỗi lần dùng từ.*
