# Chinese Learning OS — Test Guide

Checklist kiểm tra hệ thống. Chạy trong Claude Code từ thư mục `CHINESE/`.

---

## Test 1: Hard Routing

### T1.1 — HSK6 Examiner (explicit invoke)

**Input:**
```
/hsk6-examiner

科技发展让生活更便利，但也带来了隐私问题。我认为，科技公司应该保护用户数据。首先，用户把信誉交给公司，公司不能辜负这份信任。如果公司滥用数据，就会失去用户的信赖，最终影响到整个行业的发展。总的来说，技术进步和隐私保护不是对立的，而是可以并存的。
```

**Expect:**
- [ ] Có ước tính điểm dạng `xxx/300`
- [ ] 4 phần phân tích: Logic, Vocab, Grammar, Naturalness
- [ ] Ít nhất 1 Top 3 improvements cho 220+
- [ ] Có section sửa lỗi (nếu có lỗi) hoặc ghi nhận "không có lỗi cần sửa"
- [ ] `state/session-log.md` có thêm entry mới với `Status: PENDING UPDATE`

---

### T1.2 — Speaking Coach (explicit invoke)

**Input:**
```
/speaking-coach

我觉得工作压力真的越来越大。每天上班，老板总是要求我们做更多。有时候我辜负了他的期望，心里很内疚。但我也觉得，信誉很重要，所以我尽量按时完成任务。你觉得怎么办才好？
```

**Expect:**
- [ ] Bước 2: Tóm tắt bằng tiếng Trung (3-5 câu)
- [ ] Bước 3: Sửa lỗi tối đa 3 (format ❌/✅/Lý do)
- [ ] Bước 4: Có dùng ít nhất 1 từ từ `state/weekly-goal.md` Target Vocabulary
- [ ] Bước 5: Đúng 1 câu hỏi cuối (không hơn, không kém)
- [ ] `state/session-log.md` có thêm entry mới với `Status: PENDING UPDATE`

---

### T1.3 — Learning Strategist (explicit invoke)

**Input:**
```
/learning-strategist plan today
```

**Expect:**
- [ ] Bảng kế hoạch với ít nhất 2 hoạt động (Speaking, Writing, Review)
- [ ] Có cột Thời gian cụ thể (phút)
- [ ] Có "Từ trọng tâm hôm nay:" với tối đa 5 từ
- [ ] Từ được lấy từ `knowledge/vocabulary/tier-a.md`

---

## Test 2: Soft Routing

### T2.1 — Tự routing sang HSK6 Examiner

**Input:**
```
Bài này tôi tự viết, bạn cho tôi điểm được không?

在现代社会，人们越来越依赖手机。这种依赖性让我们在社交媒体上花费大量时间，有时候会忽略现实生活中的人际关系。我认为，保持适度使用手机是很重要的。
```

**Expect:**
- [ ] Claude tự route sang HSK6 Examiner (announce: `[HSK6 Examiner] Đang chấm bài...` hoặc tương tự)
- [ ] Output đúng format của HSK6 Examiner (điểm + 4 phần phân tích)

---

### T2.2 — Tự routing sang Speaking Coach

**Input:**
```
Tôi vừa nói chuyện với bạn người Trung, tôi nói: "我昨天看了一个很有意思的电影，主角是一个很聪明的科学家。他发明了一个机器，可以让人们记忆消失。" — bạn sửa giúp tôi
```

**Expect:**
- [ ] Claude tự route sang Speaking Coach
- [ ] Output đúng 5-step format

---

### T2.3 — Tự routing sang Learning Strategist

**Input:**
```
tuần này tôi nên học gì?
```

**Expect:**
- [ ] Claude route sang Learning Strategist (plan this week)
- [ ] Output có kế hoạch tuần

---

### T2.4 — Ambiguous → hỏi lại

**Input:**
```
帮我看一下这个
```

**Expect:**
- [ ] Claude hỏi 1 câu làm rõ (không đoán, không route)

---

## Test 3: Cross-Skill Coordination

### T3.1 — Speaking Coach weave Target Vocab

**Setup:** Kiểm tra `state/weekly-goal.md` → ghi nhớ danh sách Target Vocabulary.

**Input:**
```
/speaking-coach

最近我在想，工作和生活的平衡很难做到。
```

**Expect:**
- [ ] Bước 4 (Mở rộng) có sử dụng ít nhất 1 từ từ Target Vocabulary trong weekly-goal.md
- [ ] Từ được dùng trong ngữ cảnh tự nhiên (không chỉ list ra)

---

### T3.2 — Batch Update flow

**Setup:** Cần có ít nhất 1 entry `Status: PENDING UPDATE` trong session-log.md (từ T1.1 hoặc T1.2).

**Input:**
```
/learning-strategist batch update
```

**Expect:**
- [ ] Claude đọc session-log, tìm PENDING UPDATE entries
- [ ] Báo cáo: "đã update N từ, X từ promoted"
- [ ] `state/session-log.md`: entries cũ đổi sang `Status: PROCESSED`
- [ ] `knowledge/vocabulary/tier-a.md`: Seen/Speaking/Writing tăng cho từ được dùng
- [ ] `state/activation.md`: Last Updated cập nhật

---

## Test 4: Edge Cases

### T4.1 — Promote từ chưa có trong backlog

**Input:**
```
/learning-strategist promote 明显
```

**Expect:**
- [ ] Claude báo: "từ 明显 chưa có trong backlog — dùng `update backlog` trước"
- [ ] Không thay đổi bất kỳ tier file nào

---

### T4.2 — Update backlog

**Input:**
```
/learning-strategist update backlog 隐约, 辜负, 坚持
```

**Expect:**
- [ ] 3 từ mới được thêm vào 1 tier file với format chuẩn
- [ ] Mỗi từ có: Pinyin, Nghĩa, Usage (Seen/Speaking/Writing = 0), Confidence: 0%, Activation: D
- [ ] Không có field `Tier:` trong entry
- [ ] `state/activation.md` cập nhật Total

---

## Kết quả

| Test | Pass | Fail | Ghi chú |
|---|---|---|---|
| T1.1 HSK6 Examiner | | | |
| T1.2 Speaking Coach | | | |
| T1.3 Learning Strategist | | | |
| T2.1 Soft → HSK6 | | | |
| T2.2 Soft → Speaking | | | |
| T2.3 Soft → Strategist | | | |
| T2.4 Ambiguous | | | |
| T3.1 Weave vocab | | | |
| T3.2 Batch update | | | |
| T4.1 Promote missing | | | |
| T4.2 Update backlog | | | |
