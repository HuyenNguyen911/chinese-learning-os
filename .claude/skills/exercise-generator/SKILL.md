---
name: exercise-generator
description: Sinh bài tập tiếng Trung HSK1-3 cho học viên (đủ 听/读/书写 + HSKK), bám theo từng buổi dạy, ưu tiên câu từ kho đề真题/đề mẫu, render ra .docx tương tác + file đáp án riêng. Use when user muốn "tạo bài tập", "làm đề", "worksheet", "bài tập buổi X".
---

# Exercise Generator — Bài tập HSK1-3

## Vai trò
Master Chinese Teacher soạn bài tập cho học viên đang học HSK1-3. Bài tập bám
theo nội dung từng buổi (会/想/能 · lượng từ · 了...), phủ đủ 4 kỹ năng theo đúng
format thi HSK và HSKK 初级.

## Nguyên tắc nội dung
- **Ưu tiên kho đề:** rút/biến tấu câu từ `knowledge/hsk-exam-bank/hskN.md` trước.
  Chỗ kho thiếu mới tự sinh, gắn nhãn `[phỏng theo 真题]`.
- **Độ khó:** ~70% đúng cấp của buổi + ~30% cao hơn 1 bậc (HSK1 → điểm xuyết HSK2).
- **Cá nhân hóa:** dùng `.claude/skills/teaching-coach/references/interest-personalization.md`
  để ví dụ bám sở thích học viên, tránh câu sáo rỗng.
- **Không trùng lặp (user rất ghét):** KHÔNG câu nào trùng nguyên văn giữa các
  block. Cạm bẫy hay gặp: `sap_xep` và `dich_dat_cau` đặt trùng câu, hoặc câu
  `nghe`/`听后重复` lặp lại câu ở block khác. Mỗi câu một từ/vật khác nhau.
- **Gọn, đừng dài (user không thích đề dài):** cỡ **~25–27 mục/buổi** là vừa —
  giữ đủ 8 loại (phủ 听/读/书写 + HSKK) nhưng ít câu mỗi block (vd dien 4, sap 3,
  dich 3, nghe 3, HSKK 3+2). Đừng bê nguyên độ dài đề thi thật.
- **Phủ rộng vốn từ để nhớ:** trải câu qua NHIỀU từ đã dạy (nhiều màu, nhiều
  lượng từ, nhiều từ thời tiết…), đừng chỉ xoay quanh 3–4 từ. Ít câu + mỗi câu
  một từ mới = phủ rộng hơn mà vẫn ngắn.
- **Đáp án 2 cấp (khối tự luận):** với `dich_dat_cau`, `sap_xep`, `noi_hskk`
  (`回答问题`) — điền `answer`/`hint` (Chuẩn, đủ điểm) + `answer_plus`/`hint_plus`
  (Nâng cao, điểm cao) theo band chấm thi. Xem `worksheet/schema.md`.
- **Dàn bài chuẩn HSKK 初级 cho `noi_hskk` part `回答问题`** (mặc định mọi buổi,
  **đổi 2026-08-06 — buổi 8 HSK2, user thấy dàn bài 3-câu cũ "hơi khó"/khô,
  yêu cầu đổi hẳn sang kiểu mở bài/thân bài/kết bài với câu hỏi gợi ý cho từng
  phần**): `instructions` của block ghi chung 1 dòng ngắn `"Nghe câu hỏi rồi trả
  lời theo dàn bài gợi ý dưới mỗi câu (mở bài - thân bài - kết bài)."`; còn dàn
  bài CHI TIẾT (3 câu hỏi gợi mở, riêng theo từng câu hỏi nói) đặt vào field
  `hint` của chính item đó — mẫu:
  `"开头 (Mở bài): <câu hỏi gợi ai/việc gì/ở đâu> — 主体 (Thân bài): <câu hỏi
  gợi lý do/chi tiết/cảm giác> — 结尾 (Kết bài): <câu hỏi gợi kết quả/bài học>"`.
  `hint_plus` đổi thành 1 đoạn văn mẫu HOÀN CHỈNH (3-5 câu) đi theo đúng 3 phần
  mở-thân-kết đó, không còn là "1 câu cảm nghĩ thêm" như kiểu cũ. Câu hỏi nói
  (`script`) nên là câu hỏi trải nghiệm cá nhân cụ thể (vd "bạn gần đây đã làm
  gì/mua gì/gặp chuyện gì") thay vì câu hỏi giả định trừu tượng ("nếu...")
  — dễ trả lời và tự nhiên hơn cho người mới.
- Chỉ **đọc** `memory/*`. Không tự sửa memory (CLAUDE.md §4).
- **Tham khảo phong cách đề online (Pandarin):** trước khi soạn câu cho buổi
  HSK*N*, fetch 1-2 trang tương ứng cấp đó tại `pandarin.net`
  (`hsk/level{N}/` và/hoặc `belajar/hsk{N}-chapterX/`) để xem dạng câu/độ
  khó/văn phong. CHỈ dùng làm cảm hứng — KHÔNG copy nguyên văn câu hỏi/đáp án
  vào bài tập. Soạn câu mới bám vốn từ + ngữ pháp của buổi hiện tại theo
  phong cách tham khảo được.

## Cấu trúc thư mục (gom theo buổi)
Mỗi buổi 1 folder `output/hskN/buoiX_<chude>/` (do teaching-coach tạo trước), gồm:
- `slide/` — `buoiX.json`, `.pptx`, `assets/` (của teaching-coach).
- `baitap/` — nơi skill này ghi:
  - `baitap-buoiX.json` (nguồn)
  - `hocsinh/worksheet.docx` + `hocsinh/audio/*.mp3` (đưa học sinh)
  - `dapan/dapan.docx`

`<chude>` = slug chủ đề của buổi (vd `buoi1_nangnguyen_phuongtien`). Tìm folder
`buoiX_*` đã có sẵn; không tự đặt tên mới nếu teaching-coach đã tạo.

## Giai đoạn A — Soạn bài tập
1. Đọc nội dung buổi: `output/hskN/buoiX_<chude>/slide/buoiX.json` (do
   teaching-coach tạo) để lấy từ vựng + điểm ngữ pháp trọng tâm.
2. Chọn các block phù hợp (xem `references/exercise-types.md`) — thường đủ 7 loại:
   `noi`, `dien_cho_trong`, `doc_hieu`, `sap_xep`, `dich_dat_cau`, `nghe`,
   `noi_hskk`.
3. Ghi file `output/hskN/buoiX_<chude>/baitap/baitap-buoiX.json` theo `worksheet/schema.md`.
4. **Tự soát trước khi trình user** (bắt buộc — session Buổi 2/3 lộ trùng do bỏ
   bước này): quét mọi câu sản sinh/nghe (dien/sap/dich/nghe/听后重复) →
   (a) KHÔNG câu nào trùng nguyên văn; (b) đếm độ phủ vốn từ đã dạy. Có lỗi thì
   sửa rồi mới đi tiếp. Xem `worksheet/check_baitap.py`.
4b. **Đối chiếu từ vựng với TOÀN BỘ nội dung đã dạy, không chỉ 生词 card**
   (2026-08-05, buổi 4: user tự phát hiện 8+ từ ngoài phạm vi mà bước 4 không
   bắt được). Bước 4 chỉ đếm "phủ" chứ không chặn từ LẠ chưa dạy lọt vào câu tự
   sinh — cần thêm: gom toàn bộ text (`hz`) từ MỌI `buoiX.json` từ buổi 1 tới
   buổi hiện tại (không chỉ field từ vựng `wordcard`/`word_pair`/`vocab`, mà cả
   `dialogue.turns[].hz`, `passage.sentences[].hz`, `grammar.examples[].hz`,
   `bullets`/`table` có chữ Hán — học viên tiếp xúc từ qua ví dụ/hội thoại dù
   không phải thẻ 生词 riêng), rồi rà từng câu vừa soạn xem có từ/cụm nào KHÔNG
   xuất hiện trong kho văn bản đó không (trừ hư từ/đại từ/số đếm cơ bản HSK1
   hiển nhiên đã biết trước khóa). Từ lạ → đổi sang từ đã có trong kho, không
   giữ nguyên rồi hy vọng học viên đoán được nghĩa.
4c. **Đối chiếu MỌI câu tự soạn (không riêng nghe/HSKK) với TOÀN BỘ câu trong
   slide buổi đó** (2026-08-06, buổi 5 HSK2 rồi lại buổi 6: user phát hiện lần 2
   — buổi 5 chỉ vá phạm vi `听后重复`/课文/口语, buổi 6 lại lộ trùng ở cả
   `dien_cho_trong`, `sap_xep`, `dich_dat_cau` với ví dụ trong `wordcard`/`vocab`/
   `grammar.examples` — không riêng `dialogue`/`口语`. `check_baitap.py` chỉ soát
   trùng NỘI BỘ baitap, không so với slide). Gom TOÀN BỘ chuỗi `hz` xuất hiện bất
   kỳ đâu trong `buoiX.json` (đệ quy mọi field `hz`, cộng `table.rows`) thành 1
   tập câu/cụm slide → rà từng câu vừa soạn ở MỌI block sản sinh (`dien_cho_trong`,
   `sap_xep`, `dich_dat_cau`, `nghe`, `noi_hskk`, cả câu trong `doc_hieu.passage`)
   xem có **trùng nguyên văn HOẶC gần trùng** (chỉ đổi 1-2 chữ, giữ nguyên khung
   câu) với câu nào trong slide không — không chỉ so từ vựng dùng chung. Trùng/
   gần trùng → đổi tình huống/chủ ngữ/động từ để thành câu mới, chỉ giữ chung
   từ vựng + điểm ngữ pháp, không giữ khung câu.
5. **Với block `nghe` / `noi_hskk`:** trình 听力文本 / câu hỏi nói dạng text cho
   user duyệt. **KHÔNG sinh MP3 ngay.**

## Cổng xác nhận audio (bắt buộc)
- Chỉ sau khi user duyệt script, mới sinh MP3:
  - Kiểm tra `edge-tts`: `python -c "import edge_tts"`. Nếu thiếu → **dừng**,
    hướng dẫn `python -m pip install edge-tts`, KHÔNG tự cài.
  - Lấy job list: `audio_manifest.build_audio_manifest(spec)`.
  - Sinh từng file (nhớ `--rate`, xem policy dưới):
    `python -m edge_tts --voice zh-CN-XiaoxiaoNeural --rate=-25%
    --text "<script>" --write-media output/hskN/buoiX_<chude>/baitap/hocsinh/audio/<file>`.
- Audio PHẢI nằm trong `baitap/hocsinh/audio/` (cạnh worksheet.docx) vì link trong
  .docx là tương đối (`audio/...`). Đường dẫn `audio` trong JSON để dạng `audio/<file>`.

### Chất lượng giọng đọc (bắt buộc theo, cho người mới HSK1-3)
- **Tốc độ (`--rate`)** — luôn set, đừng để mặc định +0% (quá nhanh):
  - block `nghe` (听力 nghe hiểu): **`--rate=-25%`**
  - block `noi_hskk` (听后重复 / trả lời): **`--rate=-18%`**
  - Không bao giờ dùng +0% cho học viên mới.
- **Giọng**: mặc định 1 giọng rõ, ổn định `zh-CN-XiaoxiaoNeural` (nữ, ấm) cho
  toàn bộ bài tập. KHÔNG xoay nhiều giọng trong bài tập (gây rối cho người mới).
- **Đọc trong ngữ cảnh, không đọc chữ trơ**: script đã là câu hoàn chỉnh → giữ
  vậy. Nếu cần đọc một từ đơn, gói vào câu ngắn để TTS chọn đúng âm.
- **Soát phát âm TRƯỚC khi giao** (edge-tts KHÔNG ép được `<phoneme>`, nên phải
  nghe kiểm) — chú ý các điểm hay sai:
  - 多音字: 觉 (睡觉 = jiào), 乐 (音乐 = yuè), 行 (银行 = háng, 自行车 = xíng),
    了 (le/liǎo), 会 (huì), 得/地/着…
  - 儿化: 一点儿·这儿·哪儿·那儿 (phải cuốn lưỡi liền, không tách "ér");
    lưu ý 女儿 = nǚ'ér thì 儿 LÀ âm riêng — không xử lý cào bằng.
  - Nghe lại đúng các file có token trên; sai thì thử đổi câu/thêm ngữ cảnh.
- **Cửa thoát `say`** (tùy chọn): nếu một câu đọc mãi vẫn sai, thêm field `say`
  vào item (text đọc riêng, khác `script` hiển thị) và feed `say` cho edge-tts.
- **Nâng cấp tương lai**: muốn ép đọc đúng tuyệt đối (多音字/儿化) cần Azure Speech
  + SSML `<phoneme>` (có API key) — edge-tts free không làm được.

## Giai đoạn B — Render
```bash
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
"$PY" .claude/skills/exercise-generator/worksheet/build_worksheet.py \
  output/hskN/buoiX_<chude>/baitap/baitap-buoiX.json \
  output/hskN/buoiX_<chude>/baitap
```
→ `hocsinh/worksheet.docx` (cho học viên) + `dapan/dapan.docx` (đáp án + 听力文本).
Renderer tự tạo 2 thư mục con. PDF tự xuất nếu có LibreOffice, không thì báo user
"Save as PDF".

- **worksheet.docx KHÔNG BAO GIỜ chứa đáp án hay 听力文本** (renderer đã tách).
- Chiếu lớp (tùy chọn): có thể tái dùng `teaching-coach/pptx/build_deck.py` với
  một deck riêng — không bắt buộc trong luồng bài tập.

## Gây dựng kho đề (1 lần, có review gate)
Khi kho `knowledge/hsk-exam-bank/hskN.md` còn trống:
1. WebSearch/WebFetch nguồn uy tín: chinesetest.cn (CTI 官方), đề mẫu Hanban/Viện
   Khổng Tử, bài tập bộ HSK Standard Course.
2. Dùng skill `doc-analyzer` bóc câu hỏi.
3. **Trình user duyệt** danh sách câu + nguồn trước khi ghi vào `hskN.md` +
   `sources.md` (nguồn + ngày). Không lấy 真题 sách bản quyền từ nguồn lậu.

## Ghi log
Sau khi render, append 1 dòng vào `state/session-log.md`: buổi, các block, cấp độ.

## Báo kết quả
Báo user đường dẫn `hocsinh/worksheet.docx` / `dapan/dapan.docx` (+ PDF nếu có).
