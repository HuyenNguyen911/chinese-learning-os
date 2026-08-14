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
- `/exercise-generator` → invoke Skill("exercise-generator")
- `/close-session` → invoke Skill("close-session")
- `/vocab-study` → invoke Skill("vocab-study")
- `/lesson-prep` → invoke Skill("lesson-prep")

### Soft Route (intent detection — priority order)
1. Explicit command → hard route
2. Chứa chữ Trung **VÀ** hỏi điểm / đánh giá / có dấu hiệu bài viết (đoạn văn dài, có cấu trúc luận điểm) → hsk6-examiner
3. Chứa "luyện nói" / "nói chuyện" / "speaking" / "transcript" / **hoặc** "sửa" + văn phong hội thoại → speaking-coach
   _(Nếu cùng match rule 2 và 3: ưu tiên speaking-coach nếu có từ khóa speaking rõ ràng)_
4. "kế hoạch" / "plan" / "backlog" / "tuần này" / "hôm nay học gì" → learning-strategist
4b. "tạo bài tập" / "bài tập" / "làm đề" / "worksheet" / "bài tập buổi X" → exercise-generator
4c. "đóng session" / "kết thúc buổi" / "kết thúc session" / "close session" → close-session
4d. "học từ vựng" / "review từ vựng" / "sinh trang học từ" / "cập nhật từ vựng theo bài" / "tu-vung" → vocab-study
4e. "chuẩn bị bài" / "bóc bài khóa" / "lesson-prep" / "chuẩn bị buổi X" / "bài khóa của cô" → lesson-prep
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
| memory/user-profile.md | Learning Strategist, HSK6 Examiner, Speaking Coach, Exercise Generator |
| memory/writing-dna.md | HSK6 Examiner, Speaking Coach |
| memory/learning-preferences.md | Learning Strategist |

## 4.5 Model Policy (tiết kiệm token)
Default = **Sonnet** (nhanh, rẻ, đủ tốt cho ~80% việc: sinh slide, trang từ vựng,
bài tập, bóc pptx, sửa lỗi nhẹ). Khi gặp việc KHÓ dưới đây, **chủ động nhắc user**:
`💡 Việc này nên /model opus để chất lượng cao hơn`:
- hsk6-examiner (chấm bài viết, ước lượng điểm)
- thiết kế / spec giáo trình mới, quyết định kiến trúc
- suy luận nhiều bước / gỡ lỗi phức tạp

Không tự ý escalate; chỉ gợi ý 1 dòng rồi làm tiếp bằng Sonnet nếu user không đổi.

## 5. Operating Rules
- Không dùng flashcard đơn thuần làm phương pháp chính
- Không viết lại bài hoàn toàn — giữ 90% nội dung + văn phong gốc
- Không biến bài thành văn mẫu
- Tối đa 1 câu hỏi mỗi lượt, không hỏi dồn dập
- Ưu tiên ví dụ cá nhân thật, tránh từ sáo rỗng

## 5.5 Git Hygiene (chống commit/push nhầm nhánh)
User không kiểm soát được git flow — TÔI phải tự kỷ luật. Bắt buộc:

1. **Trước MỌI thao tác ghi git** (commit / rebase / reset / push) → chạy
   `git branch --show-current` và xác nhận đang đứng đúng nhánh. Đây là bước bắt buộc,
   không bỏ qua (bài học: từng rebase nhầm vì đứng sai nhánh).
2. **Commit đúng phạm vi session:** thay đổi thuộc chủ đề session nào thì commit vào
   nhánh của session/chủ đề đó. KHÔNG commit ghép việc lạ vào nhánh đang checkout chỉ vì
   tiện.
3. **Thay đổi meta/infra** (model config, `.claude/settings*.json`, sửa SKILL.md/CLAUDE.md,
   tooling) KHÔNG phải feature work → về `main` (hoặc nhánh chore riêng cắt từ main),
   TUYỆT ĐỐI không nhét vào nhánh feature dang dở.
4. **Push:** chỉ push nhánh liên quan trực tiếp việc đang làm. KHÔNG push các nhánh
   dang dở của session/chủ đề khác. KHÔNG force-push nhánh chia sẻ. Khi push bị từ chối
   → fetch + rebase nhánh ĐANG đứng, không đổi nhánh giữa chừng.
5. **Trước khi rebase/reset:** nêu rõ đang ở nhánh nào + sẽ ảnh hưởng commit nào, rồi mới
   chạy. Nghi ngờ → hỏi 1 câu, đừng đoán.
6. **Trước khi khẳng định "đã mới nhất" / "đã pull đủ":** bắt buộc `git fetch` rồi so
   `git status -sb` hoặc `git log HEAD..origin/main --oneline` — KHÔNG chỉ dựa vào
   `git status` sạch (bài học: `git status` chỉ cho biết thay đổi chưa commit ở máy này,
   không cho biết máy có đang chậm hơn `origin/main` hay không).
7. **Vocab-study / HSK6 là tool + data dùng chung mọi cấp**, không gắn riêng khóa nào.
   Thay đổi `.claude/skills/vocab-study/**`, `output/study/hskN/**`,
   `knowledge/vocabulary/**` → luôn về `main`, KHÔNG commit vào nhánh
   `feat/hskN-full-course` (nhánh đó chỉ chứa nội dung khóa học N). Đã xảy ra 2 lần
   (733ac6a, và 4 commit khác lỡ vào `feat/hsk2-full-course`) — user phải tự phát hiện.
8. **Feature branch theo khóa học (`feat/hskN-full-course`) tách khỏi `main` và KHÔNG
   tự nhận nội dung mới của `main`** (vd HSK6 bài mới, cập nhật vocab-study) — vì đó là
   2 nhánh git riêng, không phải 2 thư mục con của cùng 1 cây. Muốn thấy nội dung mới
   nhất của các phần dùng chung khi đang đứng trên nhánh feature → merge `main` vào
   nhánh đang đứng (không tạo worktree/bản sao trừ khi thật sự cần xem song song).
   Nếu chính AI vừa tạo commit trên `main` trong cùng session mà nhánh đang đứng là
   `feat/hskN-full-course` → tự động merge `main` vào ngay sau đó, không đợi user hỏi
   lại "sao tôi không thấy" (đã xảy ra 2 lần trong 1 session — Bài 31-34, rồi Bài 30).
   **Ngoại lệ HSK2 (từ 2026-08-12):** đã merge hẳn `feat/hsk2-full-course` vào `main`
   và xoá nhánh — HSK2 giờ build THẲNG trên `main` (không còn nhánh riêng), theo yêu
   cầu user vì nhánh/worktree riêng gây rối khi xem trên VS Code. Mục 8 này chỉ còn áp
   dụng cho HSK1 và các khoá tương lai chưa đổi mô hình.
9. **User tư duy theo thư mục nhìn thấy trên đĩa** (vd `output/hsk6`), không theo khái
   niệm nhánh git — khi giải thích "X thuộc về đâu", luôn quy chiếu về đường dẫn thư mục
   cụ thể, đừng chỉ nói tên nhánh (dễ hiểu lầm "H6" = tên nhánh trong khi user đang chỉ
   đường dẫn `output/hsk6`).

## 6. State Ownership

| File | Writer |
|---|---|
| state/competency.md | User / Learning Strategist (manual) |
| state/weekly-goal.md | Learning Strategist |
| state/session-log.md | HSK6 Examiner, Speaking Coach, Exercise Generator (append) |
| state/activation.md | Learning Strategist (batch) |
| knowledge/vocabulary/tier-*.md | Learning Strategist |
| sessions/writing/ | HSK6 Examiner (tạo file YYYY-MM-DD-topic.md) |
| sessions/speaking/ | Speaking Coach (tạo file YYYY-MM-DD-topic.md) |
| output/hskN/buoiX_&lt;chude&gt;/slide/ | Teaching Coach (buoiX.json + .pptx + assets/) |
| output/hskN/buoiX_&lt;chude&gt;/baitap/ | Exercise Generator (baitap.json + hocsinh/worksheet.docx + audio + dapan/dapan.docx) |
| knowledge/hsk-exam-bank/ | Exercise Generator (seed có review gate) |
| output/study/hskN/tu-vung.{md,html} | Vocab Study (đọc raw/Từ vựng.xlsx; CHỈ ĐỌC knowledge/vocabulary để lấy Activation) |
| .claude/skills/vocab-study/data/* | Vocab Study (hanzi.json, mnemonic.json — tích lũy; desc_override + vi_override = lấp 释义/意义 trống, ex_override = **ghi đè** 例句 cá nhân hoá; exp_extra) |
| .claude/skills/**/SKILL.md, CLAUDE.md | Close Session (chỉ sửa sau khi user duyệt từng mục; không đụng memory) |
| knowledge/vocabulary/tier-a.md | User / Learning Strategist / Lesson Prep (append-only, chỉ thêm từ mới ⚪→Activation D; **ghi đè** luật tier-*.md ở trên cho riêng file này) |
| raw/Từ vựng.xlsx | User / Lesson Prep (append dòng vocab mới) |
| output/hsk6/**/lesson-prep/ | Lesson Prep (vocab_payload.json, exercise_payload.json, baitap.docx) |
| memory/* | User only |

> **Cấu trúc output gom theo buổi:** mỗi buổi 1 folder `output/hskN/buoiX_<chude>/`
> chứa `slide/` (Teaching Coach) và `baitap/` (Exercise Generator). `<chude>` = slug
> chủ đề buổi, vd `buoi2_luongtu_mausac`. Đưa học sinh: cả folder `baitap/hocsinh/`
> (worksheet + audio, KHÔNG có đáp án).
>
> **Lesson Prep & tier-a.md:** Lesson Prep chỉ **thêm** entry mới vào
> `knowledge/vocabulary/tier-a.md` (dedup theo 生词, không trùng từ đã có), không
> sửa/xóa entry do Learning Strategist đang quản lý.
>
> Buổi HSK6 tự học thêm `lesson-prep/` (Lesson Prep: vocab_payload.json, exercise_payload.json, baitap.docx).
>
> **Lesson Prep ghi chéo vào data Vocab Study:** append `bai_titles.json` (tên bài) và
> `exp_extra.json` (nhóm 生词拓展 + nghĩa) trong `.claude/skills/vocab-study/data/` — append-only,
> dùng chung với Vocab Study; rồi chạy pipeline vocab-study để sinh lại `tu-vung.html`.

## 7. Skill Catalog
- **learning-strategist** — Lập kế hoạch học, quản lý vocabulary backlog, batch update activation từ session-log
- **hsk6-examiner** — Chấm bài viết tiếng Trung, ước lượng điểm HSK6, giữ văn phong gốc
- **speaking-coach** — Luyện speaking, tóm tắt → sửa lỗi → mở rộng → hỏi sâu
- **exercise-generator** — Sinh bài tập HSK1-3 cho học viên (đủ 听/读/书写 + HSKK), bám buổi dạy, ưu tiên kho đề真题, render .docx tương tác + file đáp án; audio nghe/nói qua cổng xác nhận
- **close-session** — Đóng session: hygiene check (git status) + phân loại file theo nhánh đích (main cho meta/shared-data, nhánh gốc cho content) + rà soát session tìm tri thức/pattern mới cần đưa vào skill hiện có, rồi gộp tất cả vào 1 bảng commit+push duy nhất chờ user duyệt 1 lần (meta-skill, được sửa SKILL.md/CLAUDE.md sau duyệt, không đụng memory)
- **vocab-study** — Sinh trang học từ vựng theo bài (Quizlet-style) từ `raw/Từ vựng.xlsx` → `output/study/hskN/tu-vung.html`: bảng 生词 + 生词拓展 (**sơ đồ cây**: gốc → nhánh có nghĩa), flashcard active-recall + Leitner (neo Activation), chiết tự + mẹo nhớ tiếng Việt (~1350 từ), tên bài, phát âm 🔊 (chọn giọng). Chỉ đọc knowledge/vocabulary.
- **lesson-prep** — Bóc tách pptx bài khóa HSK6: convert (doc-analyzer) → phân loại → nạp từ vựng (tier-a + vocab-study) + xuất bài tập/bài viết ra .docx. Kiểm tra đáp án AI trước khi xuất.
