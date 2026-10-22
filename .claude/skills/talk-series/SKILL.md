---
name: talk-series
description: Dự án luyện khẩu ngữ "mỗi tuần 1 chủ đề" — chọn chủ đề (bài 发展汉语 高级口语 hoặc chủ đề đổi gió) → trang chủ đề chu-de.html (mở đầu dẫn dắt + khối câu hỏi: tui kể trước → mời → giải thích khi chưa hiểu/bí → hỏi sâu; checklist mục tiêu; chế độ chưa ai vào = luyện đọc) → post HelloTalk → gom bình luận → voice room → 3 clip TikTok/RedNote → review. Use when user nói "talk series", "chủ đề tuần này", "thẻ chủ đề", "đặt câu hỏi thảo luận", "post hellotalk", "voice room", "phiếu room", "kịch bản clip chủ đề", "/talk-series".
---

# Talk Series

Bạn là người đồng hành cho dự án luyện khẩu ngữ công khai của user: **1 chủ đề / tuần**,
đi qua HelloTalk (post + voice room) rồi lên TikTok + RedNote. Mục tiêu thật là **user nói
được nhiều hơn, tự nhiên hơn, dùng được từ vựng H6 + mẫu câu bài khóa** — content mạng
xã hội là phương tiện, không phải đích.

> **Trạng thái skill: v1 (2026-10-22).** Bước 0-2 chốt; `chu-de.html` đã có khuôn (chủ đề 01).
> Bước 3-6 còn khung — chi tiết hoá khi chạy room/clip thật. Đồng bộ đa thiết bị: **TODO đang mở** (xem cuối file).

## Đọc bắt buộc trước khi làm
1. `references/style-rules.md` — luật giọng văn, chống mùi AI, chống dạy đời, slang, luật trang chu-de.html. **Áp dụng cho MỌI output.**
2. `references/question-method.md` — cách khai thác chủ đề thành khối câu hỏi (Bước 0).
3. `<TS>/_dau-an-ca-nhan.md` — chất riêng của user (góp nhặt dần).
4. `memory/user-profile.md`, `memory/writing-dna.md` — chỉ đọc.
5. `<TS>/_so-chu-de.md` — sổ chủ đề, tránh trùng + biết đang ở bước nào.

## Thư mục dữ liệu
Gốc: `output/Giáo trình phát triển Hán ngữ/Talk series/` (gọi tắt `<TS>/`), cạnh `onluyen/`.
```
<TS>/
├── _so-chu-de.md              # CẢ SERIES: danh sách chủ đề + tiến độ 7 bước + Sau room / Review từng tập
├── _dau-an-ca-nhan.md         # CẢ SERIES: chất riêng user — CHỈ ghi sau khi user duyệt từng dòng
├── _gioi-thieu-series/        # CẢ SERIES: post giới thiệu (đăng 1 lần)
├── Mo-Talk-series.bat         # (tạm, xem TODO đồng bộ) mở trang qua sync_server.py
└── <NN>_<tên chữ Hán>/        # mỗi chủ đề 1 thư mục, vd 01_快乐会传染 — CHỈ 3 thứ (user muốn gọn, không ngợp)
    ├── chu-de.html            # 1 trang dùng trực tiếp trên máy + trong room (xem bên dưới)
    ├── post-content.md        # Bước 1 + 5: post HelloTalk, caption TikTok, caption RedNote (+ ngày đăng, link)
    └── clip/                  # Bước 4-5: clip1-tom-tat.md · clip2-langdu.md · clip3-hskk.md,
                               #   file ghi âm room, gói giao genimagevideo
```
Không tạo thêm file/thư mục con ngoài 3 thứ trên. Transcript + sửa lỗi đầy đủ do **speaking-coach** lưu ở
`sessions/speaking/YYYY-MM-DD-<topic>.md`. Ảnh thống kê không lưu, chỉ ghi số.

### `chu-de.html` — khuôn (mẫu: `01_快乐会传染/chu-de.html`)
Copy khuôn của chủ đề trước, **chỉ thay khối dữ liệu** `<script id="data" type="application/json">` — không sửa code hiển thị.
Trang là công cụ user dùng thật, **không phải chỗ ghi chú của AI** (xem `style-rules.md` §7).

**Bố cục — 1 trang, không tab, trải hết chiều ngang:**
- Thanh trên: tên tập · nút 👥 **Có người vào** / 🙋 **Chưa ai vào** · nút lưu.
- Cột trái **Mục tiêu** (checklist thực hiện): Từ khoá bài (chip H6) · Mẫu câu bài khoá · Nói hết gợi ý (1 dòng/khối).
  Tick đồng bộ 2 chiều với nội dung; tick cả khối → tự tick từ + mẫu câu trong khối; bỏ tick khối → bỏ theo
  (trừ từ còn nằm trong khối khác đã tick). Mục tiêu đổi theo chế độ.
- Nội dung **👥 Có người vào**: Mở đầu (đoạn dẫn dắt bằng chuyện nhỏ thật → nêu chủ đề) → các nhóm
  Khởi động / Quan điểm / Đào sâu / Chốt. Mỗi **khối** = tiêu đề là câu hỏi (bấm để thu gọn) +
  ① Tui kể trước · ② Mời · Họ chưa hiểu / bí · ③ Hỏi sâu (kèm câu nối ngay trong bước) + **khung chat** (user gõ ý hay /
  cách nói hay / lỗi được sửa, Enter) + nút 📋 copy từng đoạn.
- Nội dung **🙋 Chưa ai vào** = **luyện đọc to**, thứ tự: 朗读 (HSKK) → 课文一 → 课文二 → 课文三
  (mỗi 课文: đọc to → kể lại theo ý → câu hỏi người nghe). KHÔNG lặp lại khối câu hỏi của chế độ 👥.

**Cú pháp chữ trong khối dữ liệu:** `**từ H6**` (tô đỏ, bấm để tick) · `{pN|đoạn dùng mẫu câu số N}` (nền xanh, bấm để tick) ·
`{s|slang}` (hiện chữ thường, KHÔNG dịch nghĩa) · `[chỗ thay chuyện thật]`.
Trường của khối: `id, name, q, story, invite, help, follow`; khối đọc: `id, type:"read", name, paras, keys, end`.
Trạng thái người dùng nằm ở `chat` + `room_state` (có `ts`); trang lấy bản mới hơn giữa file và trình duyệt.

**Tên thư mục chủ đề:** `<số tập 2 chữ số>_<tên chữ Hán>` (vd `01_快乐会传染`) — dễ nhìn, xếp đúng thứ tự.
**Mã chủ đề** (ghi trong `chu-de.html` + `_so-chu-de.md`, không dùng làm tên thư mục):
`FZ-KY-B<số bài 2 chữ số>` (发展汉语 高级口语) | `FREE-<YYYYMMDD>-<slug>` (đổi gió).
**Nguồn bài 口语: `output/Giáo trình phát triển Hán ngữ/onluyen/on-luyen.html`** — đã OCR + làm sạch, **không OCR lại sách**:
`LESSON_TEXTS[n]` (课文 nguyên văn) · `LANGUAGE_POINTS[n]` (表达方式) · `HSKK_LESSONS[n]` (`p2Text` 朗读, `p3` 回答问题) ·
`hskk_p1_scripts.json` (`n_1..n_3`) + audio `hskk{n}_p1_q*.mp3` (bài 1 không có số: `hskk_p1_q*.mp3`).

## Quy trình 7 bước

### Bước 0 — Chọn chủ đề & trang chủ đề ✅ chốt
- Nguồn: 口语 (30 bài) là chính. Đổi gió: trend RedNote/HelloTalk, chuyện đời user, ngày lễ/mùa.
- Kiểm tra `_so-chu-de.md` để không trùng → đăng ký mã mới.
- Nếu theo sách: lấy bài từ `on-luyen.html` → rút **mẫu câu + từ của bài** TRƯỚC, rồi mới viết câu hỏi quanh chúng.
- Từ H6: lọc trong **toàn bộ** `raw/Từ vựng.xlsx`, ưu tiên từ **khẩu ngữ** hợp chủ đề; từ 书面 chỉ khi bí → dành clip ③.
- Khai thác theo `references/question-method.md` (QFT tuỳ chọn → nhánh → dòng thời gian xu hướng → khối 4 bước).
  User có thể nhờ skill đề xuất luôn bộ câu hỏi, không bắt buộc tự đặt trước.
- Xu hướng "đang/sắp" **phải WebSearch** (kiến thức model có hạn), không bịa số liệu/tin. Số liệu chỉ dùng để nghĩ câu hỏi, KHÔNG đưa lên trang.
- Ghi vào khối dữ liệu `chu-de.html`. Chỗ cần chuyện thật của user để `[ngoặc vuông]`.
- Kết thúc: user **đọc to** → câu ngượng miệng (gõ vào khung chat của khối) → sửa.

### Bước 1 — Post HelloTalk ✅ chốt
- **1 post/chủ đề.** Không chốt giờ room, không nhắc voice room trong post giới thiệu.
- Ghi vào `post-content.md`. Khung: `templates/post-hellotalk.md`. Mở bằng chuyện nhỏ thật → câu hỏi dễ trả lời → hashtag.
- Ảnh: linh hoạt ảnh thật + ảnh gen (qua skill `genimagevideo`), phong cách đời thường, tránh lộ AI.
  Ghi loại ảnh vào sổ để luân phiên.

### Bước 2 — Gom bình luận ✅ chốt
- User **tự trả lời** bình luận (luyện viết). Skill KHÔNG soạn reply.
- User gửi ý hay (ảnh chụp hoặc text) 1 lần trước room → skill ghi vào `chat` của khối liên quan (mở đầu bằng 💬),
  phân 3 loại: **ý kiến** (góc nhìn lạ) / **cách nói hay** (khẩu ngữ người bản xứ) / **lỗi bị sửa**.
- KHÔNG lưu nickname — chỉ nhãn chung ("một bạn", "một bạn đang học tiếng Việt").
- Cập nhật khối: câu hỏi mới, câu dẫn "前两天有朋友说…，你们觉得呢？", cách nói hay vào câu kể.
- Không có bình luận → bỏ qua.

### Bước 3 — Voice room (< 60 phút) 🟡 khung
- Dùng `chu-de.html`. Chưa ai vào → chế độ 🙋 (luyện đọc); ai vào → 👥. Ở 👥: user kể trước ~1 phút rồi mời mọi người.
- KHÔNG báo ghi âm đầu room, KHÔNG có bước "tóm tắt 1 phút" trong room (clip ① lấy từ bản ghi âm).
- Ghi âm (iPhone): thử quay màn hình + mic 5 phút; thiếu tiếng người khác → laptop Sound Recorder, điện thoại loa ngoài.
- Transcript: Whisper chạy local (TODO: kiểm tra máy cài được không trước khi viết script).
- Sau room: đọc `chat` + `room_state` trong `chu-de.html` (từ chưa nói, ghi chú) + transcript → **speaking-coach** sửa lỗi
  (nó ghi session-log; Activation do learning-strategist nâng). Tóm tắt (từ đã dùng, lỗi chính, câu hay) → mục tập đó
  trong `_so-chu-de.md`. File ghi âm → `clip/`. Đề xuất dòng mới cho `_dau-an-ca-nhan.md` → **chờ user duyệt**.

### Bước 4 — Kịch bản 3 clip 🟡 khung
- 3 clip ngắn 30-60s, **giọng thật của user**: ① tóm tắt các góc nhìn nghe được (từ bản ghi âm) → kết bằng câu hỏi
  cho người xem (KHÔNG chốt quan điểm) ② 朗读 đoạn bài khoá 口语 (FREE → đoạn user tự viết)
  ③ 回答问题 theo format HSKK cao cấp, bớt slang.
- Mẫu câu văn viết của bài (由于…所以…) + từ H6 书面 đưa vào ① / ③, không ép vào lời nói room.
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
- Ghi mục Review của tập trong `_so-chu-de.md`: số liệu lan toả, số từ/mẫu câu đã dùng thật, lỗi lặp lại, 1-3 dòng giữ/bỏ/thử.
- Góp ý dưới clip (lỗi bị sửa, cách nói hay) thu về như Bước 2 (chat, mở đầu 🎬) → hoàn thiện dần.
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

## TODO đang mở — đồng bộ đa thiết bị + dùng trên điện thoại (CHƯA chốt, user đang cân nhắc)
Yêu cầu: mở ở bất kỳ máy/điện thoại nào, làm tiếp đúng chỗ cũ; copy được nội dung sang HelloTalk trên điện thoại.
- **Hiện có (tạm):** `<TS>/Mo-Talk-series.bat` → `scripts/sync_server.py` (git pull → mở trang qua localhost:8765;
  nút Lưu = ghi `chat`/`room_state` vào file + commit + push khi đứng `main`; nút 📱 = QR cho điện thoại cùng Wi-Fi).
  Hạn chế: máy tính phải bật + chạy .bat, điện thoại cùng Wi-Fi (thử thật chưa vào được — có thể do tường lửa), máy khác cần Python + git.
- **Phương án đề xuất:** đưa trang lên claude.ai (Artifact, riêng tư) + lưu tick/chat online → link mở được mọi nơi, không cần .bat; skill đọc dữ liệu qua ArtifactData.
- Chốt xong → cập nhật mục này + khuôn `chu-de.html`, gỡ phần không dùng.
