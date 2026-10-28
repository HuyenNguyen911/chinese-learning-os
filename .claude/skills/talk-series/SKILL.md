---
name: talk-series
description: Dự án luyện khẩu ngữ "mỗi tuần 1 chủ đề" — chọn chủ đề (bài 发展汉语 高级口语 hoặc chủ đề đổi gió) → trang chủ đề `NN_<tên>.html` (mở đầu dẫn dắt + khối câu hỏi: tui kể trước → mời → giải thích khi chưa hiểu/bí → hỏi sâu; checklist mục tiêu; chế độ chưa ai vào = luyện đọc) → post HelloTalk → gom bình luận → voice room → 3 clip TikTok/RedNote → review. Use when user nói "talk series", "chủ đề tuần này", "thẻ chủ đề", "đặt câu hỏi thảo luận", "post hellotalk", "voice room", "phiếu room", "kịch bản clip chủ đề", "/talk-series".
---

# Talk Series

Bạn là người đồng hành cho dự án luyện khẩu ngữ công khai của user: **1 chủ đề / tuần**,
đi qua HelloTalk (post + voice room) rồi lên TikTok + RedNote. Mục tiêu thật là **user nói
được nhiều hơn, tự nhiên hơn, dùng được từ vựng H6 + mẫu câu bài khóa** — content mạng
xã hội là phương tiện, không phải đích.

> **Trạng thái skill: v1 (2026-10-22).** Bước 0-2 chốt; trang chủ đề đã có khuôn (chủ đề 01).
> Bước 3-6 còn khung — chi tiết hoá khi chạy room/clip thật. Đồng bộ đa thiết bị: **TODO đang mở** (xem cuối file).

## Đọc bắt buộc trước khi làm
1. `references/style-rules.md` — luật giọng văn, chống mùi AI, chống dạy đời, slang, luật trang chủ đề. **Áp dụng cho MỌI output.**
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
└── <NN>/                      # mỗi chủ đề 1 thư mục đặt theo số tập (01, 02…) — CHỈ 2 thứ (user muốn gọn, không ngợp)
    ├── <NN>_<tên-tiếng-Anh>.html  # vd 01_contagious-happiness.html — 1 trang dùng trực tiếp trên máy + trong room; tab 📝 Bài đăng chứa post HelloTalk + caption (xem bên dưới)
    └── clip/                  # Bước 4-5: clip1-tom-tat.md · clip2-langdu.md · clip3-hskk.md,
                               #   file ghi âm room, gói giao genimagevideo
```
Không tạo thêm file/thư mục con ngoài 2 thứ trên (cùng cấp trong `<NN>/`). Post/caption KHÔNG có file .md riêng — nằm trong khối dữ liệu `post` của trang. Transcript + sửa lỗi đầy đủ do **speaking-coach** lưu ở
`sessions/speaking/YYYY-MM-DD-<topic>.md`. Ảnh thống kê không lưu, chỉ ghi số.

### Trang chủ đề `<NN>_<tên>.html` — khuôn (mẫu: `01/01_contagious-happiness.html`)
Copy khuôn của chủ đề trước, **chỉ thay khối dữ liệu** `<script id="data" type="application/json">` — không sửa code hiển thị.
Trang là công cụ user dùng thật, **không phải chỗ ghi chú của AI** (xem `style-rules.md` §7).

**Bố cục — 1 trang, không tab, trải hết chiều ngang:**
- Thanh trên: tên tập · nút 👥 **Có người vào** / 🙋 **Chưa ai vào** / 📝 **Bài đăng** · nút lưu.
- Cột trái **Mục tiêu** chỉ hiện ở 👥 (🙋 và 📝 ẩn cột này). Bôi đen chữ Hán ở mọi tab → popup pinyin + nghĩa.
- Cột trái **Mục tiêu** (checklist thực hiện): Từ khoá bài (chip H6) · Mẫu câu bài khoá · Nói hết gợi ý (1 dòng/khối).
  Tick đồng bộ 2 chiều với nội dung; tick cả khối → tự tick từ + mẫu câu trong khối; bỏ tick khối → bỏ theo
  (trừ từ còn nằm trong khối khác đã tick). Mục tiêu đổi theo chế độ.
- Nội dung **👥 Có người vào**: Mở đầu = các dòng đánh số, mỗi dòng 1 nút copy. `intro.fixed` ①②③ **CỐ ĐỊNH mọi tập, chép nguyên**
  (chào + tên 瑾玄 · câu slogan "同一件事，每个人想法都不一样…" · nhờ sửa nhẹ nhàng); `intro.group` ④⑤ đổi theo tập
  (④ dẫn chủ đề bằng chuyện/quan sát → nêu chủ đề, ⑤ mời mọi người cùng nói)
  → các nhóm khối → **Kết thúc** (cuối trang, cùng kiểu dòng đánh số): `outro.fixed` (hết giờ + cảm ơn đã sửa lỗi) và
  `outro.fixed_end` (cảm ơn + hẹn gặp + 拜拜，晚安) **CỐ ĐỊNH mọi tập**; `outro.group` = 1 câu đùa nối về chủ đề tập đó.
  Không có khối "Chốt" hỏi câu cuối (user bỏ 2026-10-22). → các nhóm
  Khởi động / Quan điểm / Đào sâu. Mỗi **khối** = tiêu đề là câu hỏi (bấm để thu gọn) +
  ① Tui kể trước · ② Mời (1 dòng gộp `invite` + `follow` — user thấy mời và hỏi sâu như nhau) · Họ chưa hiểu / bí + **khung chat** (user gõ ý hay /
  cách nói hay / lỗi được sửa, Enter) + nút 📋 copy từng đoạn.
- Nội dung **🙋 Chưa ai vào** = **luyện đọc to**, thứ tự: 朗读 (HSKK) → 课文一 → 课文二 → 课文三
  (mỗi 课文: đọc to → kể lại theo ý → câu hỏi người nghe). KHÔNG lặp lại khối câu hỏi của chế độ 👥.

**Cú pháp chữ trong khối dữ liệu:** `**từ H6**` (tô đỏ, bấm để tick) · `{pN|đoạn dùng mẫu câu số N}` (nền xanh, bấm để tick) ·
`{s|slang}` (hiện chữ thường, KHÔNG dịch nghĩa) · `[chỗ thay chuyện thật]`.
Trường của khối: `id, name, q, story, invite, help, follow`; khối đọc: `id, type:"read", name, paras, keys, end`.
Trạng thái người dùng nằm ở `chat` + `room_state` (có `ts`); trang lấy bản mới hơn giữa file và trình duyệt.

**Tên:** thư mục = số tập 2 chữ số (`01`); trang = `<số tập>_<tên tiếng Anh, chữ thường, nối bằng dấu gạch>.html` (vd `01_contagious-happiness.html`) —
chỉ chữ Latin để đường dẫn không lỗi mã hoá. Không dùng mã chủ đề; nguồn (bài 口语 số mấy / đổi gió) ghi ở cột "Nguồn" trong `_so-chu-de.md`.
**Nguồn bài 口语: `output/Giáo trình phát triển Hán ngữ/onluyen/on-luyen.html`** — đã OCR + làm sạch, **không OCR lại sách**:
`LESSON_TEXTS[n]` (课文 nguyên văn) · `LANGUAGE_POINTS[n]` (表达方式) · `HSKK_LESSONS[n]` (`p2Text` 朗读, `p3` 回答问题) ·
`hskk_p1_scripts.json` (`n_1..n_3`) + audio `hskk{n}_p1_q*.mp3` (bài 1 không có số: `hskk_p1_q*.mp3`).

## Quy trình 7 bước

### Lời nói của user — LUÔN xin ý tiếng Việt trước (rút từ session 2026-10-22: 4 lần bị chê "gượng")
Câu kể "Tui kể trước", Mở đầu ④⑤, Kết thúc, post, caption, bio: **xin user nói ý bằng tiếng Việt** (lộn xộn cũng được) →
dịch sang khẩu ngữ, giữ ~90% ý + giọng gốc → kèm mục **"những chỗ mình chỉnh"** (vì sao đổi) để user duyệt.
KHÔNG tự soạn sẵn cả khung rồi đưa user sửa — bản AI tự soạn bị chê khuôn sáo/gượng mọi lần.
Khi dịch: lọc từ H6 trong `raw/Từ vựng.xlsx` (khẩu ngữ trước); từ không có trong danh sách thì nói rõ.

### Công cụ sửa trang (bắt buộc)
- Sửa khối dữ liệu: `python scripts/patch_data.py <page.html> <changes.json>`
  (`blocks` / `replace` / `gloss` — xem docstring). **Mỗi `**từ**` hoặc `{s|…}` phải có `gloss` (pinyin + nghĩa tự soạn,
  không dựa dịch máy)** — script báo "THIẾU gloss" nếu sót.
- Kiểm tra: `python scripts/check_page.py <page.html> [--select <từ>] [--tab group|solo|post]` → **chạy xong, không lỗi JS, mới báo "đã sửa"**
  (session 2026-10-22 lọt 2 lỗi cú pháp vì chỉ `node --check`).

### Bước 0 — Chọn chủ đề & trang chủ đề ✅ chốt
- Nguồn: 口语 (30 bài) là chính. Đổi gió: trend RedNote/HelloTalk, chuyện đời user, ngày lễ/mùa.
- Kiểm tra `_so-chu-de.md` để không trùng → đăng ký tập mới (số tập + tên thư mục).
- Nếu theo sách: lấy bài từ `on-luyen.html` → rút **mẫu câu + từ của bài** TRƯỚC, rồi mới viết câu hỏi quanh chúng.
- Từ H6: lọc trong **toàn bộ** `raw/Từ vựng.xlsx`, ưu tiên từ **khẩu ngữ** hợp chủ đề; từ 书面 chỉ khi bí → dành clip ③.
- Khai thác theo `references/question-method.md` (QFT tuỳ chọn → nhánh → dòng thời gian xu hướng → khối 4 bước).
  User có thể nhờ skill đề xuất luôn bộ câu hỏi, không bắt buộc tự đặt trước.
- Xu hướng "đang/sắp" **phải WebSearch** (kiến thức model có hạn), không bịa số liệu/tin. Số liệu chỉ dùng để nghĩ câu hỏi, KHÔNG đưa lên trang.
- Ghi vào khối dữ liệu trang chủ đề. Chỗ cần chuyện thật của user để `[ngoặc vuông]`.
- Kết thúc: user **đọc to** → câu ngượng miệng (gõ vào khung chat của khối) → sửa.

### Bước 1 — Post HelloTalk ✅ chốt
- **1 post/chủ đề.** Không chốt giờ room, không nhắc voice room trong post giới thiệu.
- Ghi vào khối dữ liệu `post` của trang chủ đề (tab 📝 Bài đăng, mỗi đoạn có nút 📋 copy + nút Copy cả bài). Khung: `templates/post-hellotalk.md`. Mở bằng chuyện nhỏ thật → câu hỏi dễ trả lời → hashtag.
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
- Dùng trang chủ đề. Chưa ai vào → chế độ 🙋 (luyện đọc); ai vào → 👥. Ở 👥: user kể trước ~1 phút rồi mời mọi người.
- KHÔNG báo ghi âm đầu room, KHÔNG có bước "tóm tắt 1 phút" trong room (clip ① lấy từ bản ghi âm).
- Ghi âm (iPhone): thử quay màn hình + mic 5 phút; thiếu tiếng người khác → laptop Sound Recorder, điện thoại loa ngoài.
- Transcript: Whisper chạy local (TODO: kiểm tra máy cài được không trước khi viết script).
- Sau room: đọc `chat` + `room_state` trong trang chủ đề (từ chưa nói, ghi chú) + transcript → **speaking-coach** sửa lỗi
  (nó ghi session-log; Activation do learning-strategist nâng). Tóm tắt (từ đã dùng, lỗi chính, câu hay) → mục tập đó
  trong `_so-chu-de.md`. File ghi âm → `clip/`. Đề xuất dòng mới cho `_dau-an-ca-nhan.md` → **chờ user duyệt**.

### Bước 4 — 1 video + 1 bộ ảnh (chốt 2026-10-23) 🟡 đang dựng khuôn
- **Mỗi tuần CHỈ 1 video dọc 9:16 (20-30s) + 1 bộ ảnh 3:4 (1080×1440)**, dùng chung cho mọi kênh — không làm content riêng
  từng nền tảng (user mệt + tốn token). Bộ ảnh = các cảnh của video xuất tĩnh.
- **Nhân vật chibi cử động** (không dùng ảnh tĩnh — "chán"): tấm gốc + các tấm "lật" (miệng mở, mắt nhắm…) vẽ đè bằng code,
  nhép miệng theo **âm lượng** giọng thật, chớp mắt, nhún nhẹ. Nhân vật lấy từ `output/Gen ảnh_video/nhan-vat/` (xem genimagevideo).
- **Kịch bản:** chia câu theo cảnh `c1…cN`; user thu **mỗi câu 1 file** `cN.m4a` → độ dài cảnh = độ dài file, phụ đề tự khớp.
  Phải **thể hiện đúng ý chủ đề** (vd 传染 = có chuỗi lây người→người) và đặt user là người trong cuộc, không đứng nhìn.
  Có thể lấy tình huống từ `onluyen/bai-mau-cau5-6.md` (giữ cụm đắt giá, BỎ câu kêu gọi kiểu 让我们…吧 / 正能量).
- **Chữ trên video: toàn tiếng Trung**; từ khó (2-4 từ/clip) hiện thẻ 汉字 + pinyin + **nghĩa tiếng Anh** (user chốt 2026-10-28) đúng cảnh. Chữ do code vẽ.
- **Phụ đề đặt ở ĐẦU khung** (~200px từ mép trên), thẻ từ nằm ngay dưới — đặt ở đáy thì dễ bị nội dung post/nút nền tảng che và kém nổi bật (user chốt 2026-10-28). Mỗi đoạn phụ đề ≤ ~12 chữ Hán, tách ở dấu phẩy; 1 câu thoại có thể chia nhiều cảnh (vẫn 1 file giọng).
- **Câu trong clip ↔ bài đăng 6 kênh phải đồng bộ:** sửa câu ở clip thì grep câu đó trong `NN_*.html` và sửa cả các khối post (tập 01: 5 chỗ).
- Câu sai trong room → sửa đúng → cài vào kịch bản (chữa lỗi bằng cách nói lại).
- Dựng bằng `genimagevideo`: clip kể chuyện = khuôn `story-clip`; **clip ② 朗读 = khuôn `read-along`** (bài `p2Text` của bài 口语 tương ứng, 2 bản thẻ nghĩa EN + VI, nhân vật luân phiên theo bài).
- **Mọi video** có nhạc nền nhẹ + hiệu ứng âm thật, chống copy (禁止搬运 + @瑾玄在练嘴 + dấu chìm nhỏ) và **đoạn kết Follow → ✓ Followed** bằng giọng 瑾玄 — genimagevideo `design-rules.md` §10–11.

### Bước 5 — Đăng 6 kênh 🟡 khung
- Caption từng kênh nằm trong khối `post` của trang (mỗi kênh 1 thẻ copy; RedNote tách thẻ tiêu đề). Luật từng kênh: `style-rules.md` §6.
- Định dạng: TikTok = video · Instagram = Reels (+ carousel, Story bình chọn) · Facebook = bài ảnh + chữ (Reels tự chia sẻ từ IG)
  · Threads = chữ + 1 ảnh · RedNote = bài ảnh 图文 (từ khoá trong tiêu đề/thân) · HelloTalk = moment chữ + **file đọc to** (được sửa phát âm).
- Quá sức → ưu tiên HelloTalk (được sửa) + TikTok (luyện nói khi quay).
- Tên series: CHƯA chốt — đang dùng "📚 每周一个话题｜Vol. 01".

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

## Đồng bộ đa thiết bị + điện thoại — ĐANG THỬ phương án Artifact (từ 2026-10-22)
Yêu cầu: mở ở bất kỳ máy/điện thoại nào, làm tiếp đúng chỗ cũ; copy được nội dung sang HelloTalk trên điện thoại.
- **Artifact (đang thử):** 1 link cố định https://claude.ai/artifact/Em2nw9iBDNvNu9n42hf3QW (riêng tư, tên "Talk Series",
  mở trong app Claude hoặc trình duyệt). Trang trong máy vẫn là **bản gốc**; dựng bản Artifact bằng
  `python scripts/build_artifact.py "<TS>/NN/NN_<tên>.html" "<out>.html"` rồi publish lại **cùng url**, capabilities `{"db": {}, "sample": {}}`.
  Tập mới → build từ trang tập mới, publish đè cùng link (tiến độ tập cũ vẫn còn trong db).
  **Nhịp đẩy:** lúc đang sửa từng khối CHỈ sửa trang trong máy; build + publish 1 lần khi user nói "xong" / "đẩy lên" /
  sắp mở trên điện thoại (user chốt 2026-10-22 — đừng publish sau mỗi khối).
  - Tick/chat lưu ở db doc `progress/ep<NN>` (field `state` = S của trang) → sau room đọc bằng ArtifactData (`get`, collection `progress`, doc `ep<NN>`).
  - Từ không có trong `gloss` → hỏi Claude qua `sample` (MyMemory bị CSP chặn trên claude.ai).
  - Trang gốc có 2 móc rỗng `window.TS_onSave` / `window.TS_MEANING` cho bản Artifact gắn vào — đừng xoá.
- **Cách cũ (giữ tới khi Artifact chạy ổn):** `<TS>/Mo-Talk-series.bat` → `scripts/sync_server.py` (localhost, nút Lưu commit+push, QR cùng Wi-Fi —
  chưa vào được từ điện thoại). Artifact ổn → gỡ .bat + sync_server + nút 📱/💾 khỏi khuôn.
