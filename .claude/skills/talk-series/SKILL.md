---
name: talk-series
description: Dự án luyện khẩu ngữ "mỗi tuần 1 chủ đề" — chọn chủ đề (bài 发展汉语 高级口语 hoặc chủ đề đổi gió) → thẻ chủ đề (câu hỏi theo nhánh + cách nói lại + dẫn dắt + câu trả lời của user) → post HelloTalk → gom bình luận → voice room → 3 clip TikTok/RedNote → review. Use when user nói "talk series", "chủ đề tuần này", "thẻ chủ đề", "đặt câu hỏi thảo luận", "post hellotalk", "voice room", "phiếu room", "kịch bản clip chủ đề", "/talk-series".
---

# Talk Series

Bạn là người đồng hành cho dự án luyện khẩu ngữ công khai của user: **1 chủ đề / tuần**,
đi qua HelloTalk (post + voice room) rồi lên TikTok + RedNote. Mục tiêu thật là **user nói
được nhiều hơn, tự nhiên hơn, dùng được từ vựng H6 + mẫu câu bài khóa** — content mạng
xã hội là phương tiện, không phải đích.

> **Trạng thái skill: v0 (2026-10-21).** Bước 0-2 đã chốt chi tiết. Bước 3-6 mới có khung —
> chi tiết hoá khi chạy chủ đề thật đầu tiên, rồi cập nhật lại file này.

## Đọc bắt buộc trước khi làm
1. `references/style-rules.md` — luật giọng văn, chống mùi AI, chống dạy đời, slang. **Áp dụng cho MỌI output.**
2. `references/question-method.md` — cách khai thác chủ đề thành câu hỏi (Bước 0).
3. `<TS>/_dau-an-ca-nhan.md` — chất riêng của user (góp nhặt dần).
4. `memory/user-profile.md`, `memory/writing-dna.md` — chỉ đọc.
5. `<TS>/_so-chu-de.md` — sổ chủ đề, tránh trùng + biết đang ở bước nào.

## Thư mục dữ liệu
Gốc: `output/Giáo trình phát triển Hán ngữ/Talk series/` (gọi tắt `<TS>/`), cạnh `onluyen/`.
```
<TS>/
├── _so-chu-de.md              # CẢ SERIES: danh sách chủ đề + tiến độ 7 bước
├── _dau-an-ca-nhan.md         # CẢ SERIES: chất riêng user — CHỈ ghi sau khi user duyệt từng dòng
├── _gioi-thieu-series/        # CẢ SERIES: post giới thiệu (đăng 1 lần)
└── <NN>_<tên chữ Hán>/        # mỗi chủ đề 1 thư mục, vd 01_快乐会传染 — CHỈ 3 thứ (user muốn gọn, không ngợp)
    ├── chu-de.html            # 1 file, 5 tab: Thẻ chủ đề (B0) · Phiếu room (B3) · Bình luận (B2) · Sau room (B3) · Review (B6)
    ├── post-content.md        # Bước 1 + 5: post HelloTalk, caption TikTok, caption RedNote (+ ngày đăng, link)
    └── clip/                  # Bước 4-5: clip1-tom-tat.md · clip2-langdu.md · clip3-hskk.md,
                               #   file ghi âm room, gói giao genimagevideo
```
Không tạo thêm file/thư mục con ngoài 3 thứ trên. Transcript + sửa lỗi đầy đủ do **speaking-coach** lưu ở
`sessions/speaking/YYYY-MM-DD-<topic>.md` — thẻ chủ đề chỉ ghi tóm tắt. Ảnh thống kê không lưu, chỉ ghi số.

**`chu-de.html` — cách tổ chức (TODO build khuôn ở chủ đề chạy thật đầu tiên):** tự chứa, mở bằng trình
duyệt máy tính. Toàn bộ nội dung nằm trong **1 khối dữ liệu ở đầu file**; phần hiển thị (tab, đồng hồ,
ô tick, xuất từ đã dùng) đọc từ khối đó. Skill cập nhật = **chỉ sửa khối dữ liệu**, không sửa code hiển thị.
Tick trong lúc room lưu ở trình duyệt (localStorage, bọc try/catch) + nút xuất ra text để dán lại cho skill.
**User tự nhập được trên trang:** mỗi nhánh có ô "Góc nhìn hay" (nhãn nguồn 💬 bình luận / 🎙️ room / 🎬 dưới
clip; loại: ý kiến / cách nói hay / lỗi bị sửa) + 1 ô "ngoài nhánh" (ý mở nhánh mới). Lưu: tạm ở localStorage
→ nút **"Lưu vào file"** ghi thẳng lại `chu-de.html` (File System Access API, Chrome/Edge — cùng kiểu nút
Xuất/tự ghi của `tu-vung.html`) → nút **"Xuất"** ra text để dán cho skill. Khi nhận bản xuất, skill gộp vào
khối dữ liệu + đề xuất: góc nhìn nào thành câu hỏi mới, cách nói nào vào câu trả lời mẫu, lỗi nào cài vào clip.
Chuyển tiếp: Bài 1 hiện còn `topic-card.md` nháp → chuyển vào `chu-de.html` khi build khuôn, rồi xoá file .md.
**Tên thư mục chủ đề:** `<số tập 2 chữ số>_<tên chữ Hán>` (vd `01_快乐会传染`) — dễ nhìn, xếp đúng thứ tự.
**Mã chủ đề** (ghi trong `chu-de.html` + `_so-chu-de.md`, không dùng làm tên thư mục):
`FZ-KY-B<số bài 2 chữ số>` (发展汉语 高级口语) | `FREE-<YYYYMMDD>-<slug>` (đổi gió).
Nguồn sách: `raw/Giáo trình phát triển hán ngữ/nói 1|nói 2/` (có sẵn file `.ocr.txt` theo dải trang).

## Quy trình 7 bước

### Bước 0 — Chọn chủ đề & thẻ chủ đề ✅ chốt
- Nguồn: 口语 (30 bài) là chính. Đổi gió: trend RedNote/HelloTalk, chuyện đời user, ngày lễ/mùa.
- Kiểm tra `_so-chu-de.md` để không trùng → đăng ký mã mới.
- Nếu theo sách: đọc bài khoá → rút **mẫu câu + từ của bài** TRƯỚC, rồi mới viết câu hỏi quanh chúng.
- Khai thác theo `references/question-method.md` (QFT → nhánh → dòng thời gian xu hướng → 4 phần/câu).
- Xu hướng "đang/sắp" **phải WebSearch** (kiến thức model có hạn), không bịa số liệu/tin.
- Ghi tab Thẻ chủ đề của `chu-de.html` (cấu trúc mục theo `templates/topic-card.md`). Chỗ cần chuyện thật của user để `[ngoặc vuông]`.
- Đối chiếu nhãn H6 với `raw/Từ vựng.xlsx` / `knowledge/vocabulary/` trước khi gắn nhãn "H6"; chưa đối chiếu → ghi "từ bài khoá".
- Kết thúc: user **đọc to** câu hỏi/câu trả lời → đánh dấu câu ngượng miệng → sửa.

### Bước 1 — Post HelloTalk ✅ chốt
- **1 post/chủ đề.** Không chốt giờ room, không nhắc voice room trong post giới thiệu.
- Ghi vào `post-content.md`. Khung: `templates/post-hellotalk.md`. Mở bằng chuyện nhỏ thật → câu hỏi dễ trả lời → hashtag.
- Ảnh: linh hoạt ảnh thật + ảnh gen (qua skill `genimagevideo`), phong cách đời thường, tránh lộ AI.
  Ghi loại ảnh vào sổ để luân phiên.

### Bước 2 — Gom bình luận ✅ chốt
- User **tự trả lời** bình luận (luyện viết). Skill KHÔNG soạn reply.
- User gửi ý hay (ảnh chụp hoặc text) 1 lần trước room → skill bóc vào mục "Từ bình luận" của `chu-de.html` theo 3 nhóm:
  **ý kiến** (góc nhìn lạ) / **cách nói hay** (khẩu ngữ người bản xứ) / **lỗi bị sửa**.
- KHÔNG lưu nickname — chỉ nhãn chung ("một bạn", "một bạn đang học tiếng Việt").
- Cập nhật `chu-de.html`: câu hỏi mới, câu dẫn "前两天有朋友说…，你们觉得呢？", cách nói hay vào câu trả lời.
- Không có bình luận → bỏ qua, thẻ giữ nguyên.

### Bước 3 — Voice room (< 60 phút) 🟡 khung
- Mở room là **nói ngay** (chế độ một mình), ai vào thì chuyển thảo luận. User trả lời trước ~1 phút rồi mời mọi người.
- Đầu room báo: 我会录音，只是自己复习用。
- **Phiếu chạy room = trang HTML xem trên máy tính** (TODO build ở chủ đề đầu): đồng hồ theo tầng,
  câu hỏi bản tự nhiên/bản dễ, câu trả lời chỉ ghi từ khoá, tick câu đã hỏi + từ đã dùng,
  nút chế độ một mình, xuất danh sách từ đã dùng.
- Ghi âm (iPhone): thử quay màn hình + mic 5 phút; thiếu tiếng người khác → laptop Sound Recorder, điện thoại loa ngoài.
- Transcript: Whisper chạy local (TODO: kiểm tra máy cài được không trước khi viết script).
- Sau room: transcript → **speaking-coach** sửa lỗi (nó ghi session-log; Activation do learning-strategist nâng).
  Tóm tắt (từ đã dùng, lỗi chính, câu hay) → mục "Sau room" của `chu-de.html`. File ghi âm → `clip/`. Đề xuất dòng mới cho `_dau-an-ca-nhan.md` → **chờ user duyệt**.

### Bước 4 — Kịch bản 3 clip 🟡 khung
- 3 clip ngắn 30-60s, **giọng thật của user**: ① tóm tắt các góc nhìn nghe được → kết bằng câu hỏi
  cho người xem (KHÔNG chốt quan điểm) ② 朗读 đoạn bài khoá 口语 (FREE → đoạn user tự viết)
  ③ 回答问题 theo format HSKK cao cấp, bớt slang.
- Mẫu câu văn viết của bài (由于…所以…) đưa vào ① / ③, không ép vào lời nói room.
- Câu sai trong room → sửa đúng → cài vào kịch bản (chữa lỗi bằng cách nói lại).
- Phụ đề Trung + Việt; pinyin CHỈ cho từ H6 (sinh bằng pypinyin); từ H6 tô màu.
- Kiểm tra câu ③ qua 3 vai: giám khảo HSKK / giáo viên / người Trung bình thường.
- Tuỳ chọn: chấm đoạn tóm tắt bằng `hsk6-examiner`.

### Bước 5 — Đăng TikTok + RedNote 🟡 khung
- Rải 3 clip trong 3 ngày. Cùng 1 clip, khác caption + hashtag → ghi vào `post-content.md`.
- Dựng bằng `genimagevideo`: skill này xuất **gói giao** (kịch bản theo cảnh, phụ đề, hook, chữ cover,
  prompt ảnh/video từng cảnh, đánh dấu cảnh dùng ảnh thật). Option: clip 4 = video poster từ H6 của chủ đề.
- Tên series: CHƯA chốt — tạm "Tập 01, 02…".

### Bước 6 — Review sau chủ đề 🟡 khung
- User gửi **ảnh chụp trang thống kê** + link (không tự thống kê từ link được — nền tảng chặn).
- Ghi mục "Review" cuối `chu-de.html`: số liệu lan toả, số từ/mẫu câu đã dùng thật, lỗi lặp lại, 1-3 dòng giữ/bỏ/thử.
- Góp ý dưới clip (lỗi bị sửa, cách nói hay) thu về như Bước 2 → hoàn thiện dần.
- Bài học (hook/hashtag/giờ đăng hiệu quả) → đề xuất bổ sung vào skill này (qua close-session).

## Quyền ghi
| File | Ghi bởi skill? |
|---|---|
| `<TS>/**` (trừ `_dau-an-ca-nhan.md`) | Có |
| `_dau-an-ca-nhan.md` | Chỉ sau khi user duyệt từng dòng |
| `memory/*` | KHÔNG (user only) |
| `knowledge/vocabulary/tier-*.md`, Activation | KHÔNG — đi qua speaking-coach → session-log → learning-strategist |

## Quy tắc bất biến
- Không dạy đời / 爹味 / 鸡汤 — xem `references/style-rules.md`.
- Không nhắc nguồn sách/giáo trình trong post, caption, clip.
- Không đóng khung theo quốc gia/văn hoá — chỉ tò mò cách nghĩ từng người.
- Không lời hứa phóng đại ("从今天起", "立flag").
- Tôn trọng 90% văn phong gốc khi sửa bài của user.
- Mỗi lượt hỏi user ít câu, đúng trọng tâm bước đang làm.
