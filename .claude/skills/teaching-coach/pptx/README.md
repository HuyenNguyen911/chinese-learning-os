# PPTX Helper — teaching-coach

Renderer **data-driven** cho bài giảng tiếng Trung. Bạn soạn 1 file JSON mô tả
bài giảng, chạy 1 lệnh, ra 1 file `.pptx` với design system cố định (font CJK,
layout 汉字 + pinyin + nghĩa Việt, bảng so sánh, khung hội thoại, đọc thêm...).

> Thay thế cho skill pptx cloud (`/mnt/skills/public/pptx/`) vốn **không tồn tại**
> trên máy local. Không cần internet, không cần cài thêm gì.

## Chạy

```bash
# Python thật (đã có python-pptx 1.0.2, pillow, lxml):
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"

"$PY" .claude/skills/teaching-coach/pptx/build_deck.py <lesson.json> <output.pptx>
```

Ví dụ (chính là bộ test, bao trùm cả 8 loại slide):

```bash
"$PY" .claude/skills/teaching-coach/pptx/build_deck.py \
  .claude/skills/teaching-coach/pptx/example-lesson.json \
  output/teaching/demo.pptx
```

Lưu ý encoding console: nếu cần in tiếng Trung ra terminal để debug, đặt
`PYTHONIOENCODING=utf-8`. Bản thân file `.pptx` luôn UTF-8, không ảnh hưởng.

## Quy trình chuẩn (Giai đoạn B của skill)

1. Hoàn thành nội dung ở Giai đoạn A (vai Master Chinese Teacher).
1b. **Chủ động mở rộng chủ đề trước khi soạn** (2026-08-05): dựa vào chủ đề
   buổi học, tự tìm/nghĩ thêm từ vựng/nội dung liên quan có thể bổ sung (không
   chỉ bó trong sách gốc) — rồi **trình danh sách mở rộng cho user duyệt**
   trước, chỉ triển khai vào slide sau khi được đồng ý. Không tự ý thêm rồi
   mới báo.
2. Ánh xạ nội dung sang các block JSON bên dưới — mỗi ý một slide, action title.
   Nếu dùng `word_pair` cho từ vựng mở rộng: ghép cặp theo **CÙNG CHỦ ĐỀ
   NHỎ/LIÊN QUAN NHAU** (vd đối lập 深色/浅色, cùng nhóm trang phục ngủ+ở nhà),
   không ghép máy móc theo thứ tự liệt kê có sẵn — thứ tự gốc thường xen kẽ
   danh từ/tính từ không liên quan (xem ví dụ ở bảng loại slide bên dưới).
2b. **Thứ tự khối nội dung trong 1 buổi (chốt theo Buổi 8, 2026-08-06):**
   Title → 目标 (mục tiêu) → **toàn bộ 生词** (chính rồi tới mở rộng, theo thứ tự
   xuất hiện trong 课文 1→2→3→4) → **课文/hội thoại** (theo đúng thứ tự sách) →
   **语法** (theo đúng thứ tự sách) → luyện tập/口语. Tức là dạy hết từ mới TRƯỚC
   khi học viên gặp trong bài, không xen kẽ "hết 1 đoạn文 → ra từ luôn" theo thứ
   tự sách gốc (cách đó từng bị coi là sai khi làm Buổi 9).
3. Tạo folder buổi `output/hskN/buoiX_<chude>/slide/` rồi ghi `buoiX.json` vào đó
   (ảnh vào `assets/` cùng cấp; path ảnh trong JSON là `assets/<tên>.jpg`).
4. **Duyệt nội dung với user trước khi sinh audio.** Trình bày nội dung text (title +
   items/example từng slide, không cần build pptx) cho user xem — nhất là câu ví dụ (tự
   nhiên/khớp ngữ cảnh chưa) và ảnh đã gắn (khớp nội dung slide chưa). Chờ user OK.
5. Sau khi user duyệt, chạy `slide_audio.py <slide/buoiX.json>` rồi
   `build_deck.py <slide/buoiX.json> <slide/Buoi-X-....pptx>` — **một lần**, tránh
   rebuild lặp lại theo từng chỉnh sửa nhỏ (mỗi lần sinh audio gọi edge-tts qua mạng cho
   toàn bộ slide, khá tốn thời gian/token nếu lặp lại nhiều vòng).
6. Báo đường dẫn file cho học viên.

> **Gom theo buổi:** mỗi buổi 1 folder `output/hskN/buoiX_<chude>/` chứa `slide/`
> (skill này) và `baitap/` (skill exercise-generator). `<chude>` = slug chủ đề,
> vd `buoi2_luongtu_mausac`.

## Schema JSON

```jsonc
{
  "meta":  { "title": "...", "lesson": "Bài X · Quyển Y" },
  "theme": { "accent": "C0392B", "cjk_font": "Microsoft YaHei" },  // optional
  "slides": [ { "type": "...", ... }, ... ]
}
```

`theme` (tùy chọn) override design mặc định — mã màu là hex **không** có `#`.
Keys: `accent`, `accent_soft`, `ink`, `muted`, `bg`, `band`, `cjk_font`,
`text_font`.

### Các loại slide (`type`)

Mọi slide nội dung (trừ `title`/`section`) render với **header dải đỏ
full-width**. Trường `kicker` (tùy chọn) tạo tab nhỏ chứa nhãn CJK phía trước
tiêu đề, vd `"生词"`, `"语法"`, `"会话"`, `"练习"`.

| `type` | Trường chính | Công dụng |
|---|---|---|
| `title` | `title` (+ `subtitle`, `footer`, `image?`) | Slide bìa (nền accent) |
| `section` | `title` (+ `subtitle`) | Chuyển mục |
| `vocab` | `items[]` = `{hz, py, vn}` (+ `image?`, `image_side?`, `color?`, `ex?`, `example?`) | Bảng từ vựng 汉字\|Pinyin\|Nghĩa; nếu item có `color` (hex, vd `"E74C3C"`) → chèn cột **chip màu** (bài dạy màu sắc); nếu item có `ex` (câu ví dụ riêng từng từ) → chèn cột **Ví dụ** cuối bảng; `example?` (cấp SLIDE, không phải item) = `{hz,py,vn}` 1 câu ví dụ chung — render **tách riêng khỏi bảng** (chữ thường, không khung): có ảnh → hiện dưới ảnh; không ảnh → hiện dưới bảng; có `image` → ảnh + bảng. Danh sách dài (>~8 từ) → tách thành 2 slide `vocab` liên tiếp thay vì nhồi 1 bảng (renderer không tự tách). Dùng được cho CẢ CÂU dài, không chỉ từ đơn (vd mỗi item là 1 lời chúc/câu nói) — cột 汉字 tự đủ rộng + hàng tự cao theo số dòng 汉字 cần wrap, Pinyin/Nghĩa co lại/rớt dòng trước (xem lessons learned bên dưới). |
| `wordcard` | `hz`, `py?`, `vn?`, `pos?`, `examples[]` = `{hz, py, vn}` (tối đa 3), `image?` | **1 từ / 1 slide** — 汉字 lớn + pinyin + nghĩa + ảnh sticker minh hoạ bên trái, tối đa 3 câu ví dụ bên dưới. Dùng khi cần đào sâu từng từ thay vì dồn bảng nhiều từ/slide (số từ nhiều → số slide tăng tương ứng, cân nhắc thời lượng buổi học). |
| `word_pair` | `words[]` = `{hz, py?, vn?, pos?, image?, example?}` (tối đa 2), `example` = `{hz, py, vn}` | **2 từ / 1 slide**, xếp cạnh nhau — mỗi cột tự chứa ảnh (trên) + 汉字/pinyin/nghĩa (giữa) + 1 câu ví dụ (dưới). Dùng cho từ vựng CÙNG NHÓM/CHỦ ĐỀ khi số lượng từ lớn (vd 生词拓展) — nén gọn hơn `wordcard` (đổi lại chỉ giữ 1 ví dụ/từ thay vì tối đa 3). Chỉ 1 từ (mảng `words` có 1 phần tử) vẫn hợp lệ — cột còn lại để trống. ⚠️ **Lịch sử (đã sửa 2026-08-06):** handler `_slide_word_pair` được thêm ở `5a2a154`, rồi bị **âm thầm xoá** ở `619229b` (commit message chỉ nói "sửa 3 lỗi renderer", không nhắc việc xoá này) — các bản README trước đó ghi nhầm là "chưa triển khai", thực ra là đã cài rồi bị mất. Đã khôi phục lại nguyên trạng handler. |
| `grammar` | `point?`, `examples[]` = `{hz, py, vn, highlight?}`, `note?`, `source?`, `image?`, `highlight?` | Giảng ngữ pháp. `highlight` (str hoặc list[str], cấp SLIDE — áp dụng mọi ví dụ, hoặc cấp ví dụ để override riêng) = tô màu accent (đỏ) cho đúng chỗ khớp trong `hz` của từng ví dụ, giúp học viên thấy ngay từ/cấu trúc đang học nằm ở đâu trong câu (vd `"highlight": "没有"` tô đỏ mọi chỗ xuất hiện "没有"; 时量补语 nên override theo từng ví dụ vì cụm bổ ngữ khác nhau mỗi câu, vd ví dụ 1 `"highlight": "半个多小时"`, ví dụ 2 `"highlight": "两个小时了"`). |
| `table` | `headers[]`, `rows[][]` (+ `cjk_cols[]`) | Bảng so sánh (vd 了 vs 过) |
| `dialogue` | `turns[]` = `{speaker, hz, py, vn?}` (+ `image?`, `image_side?`) | Khung hội thoại (bong bóng chat 2 phía, hoặc swimlane 1-cột/người nếu >2 speaker) — hội thoại nhiều lượt nên **bỏ `vn`** để bong bóng không tràn/đụng nhau. Có `image` → ảnh ngữ cảnh 1 bên, khung thoại co vào bên còn lại (giúp liên tưởng bối cảnh thay vì chỉ thấy chữ nổi) |
| `passage` | `title`, `sentences[]` = `{hz, py, vn}` (+ `note?`, `image?`, `image_side?`) | Đoạn văn tự sự/kể chuyện (课文 thể 叙述体, câu nối tiếp câu — KHÔNG phải hội thoại qua lại) — mỗi câu 1 khối, không dùng bong bóng thoại |
| `reading` | `groups[]` = `{label, items[]}` | Nguồn đọc thêm (nhóm "trong sách" / "nguồn ngoài") |
| `exercise` | `instructions?`, `items[]` (+ `image?`) | Slide bài tập (đánh số) |
| `answers` | `items[]` | Slide đáp án (đánh số) |
| `bullets` | `bullets[]` (+ `image?`) | Gạch đầu dòng thường |
| `image` | `image`, `caption?`/`captions[]` | Ảnh lớn canh giữa (sơ đồ/biểu đồ tĩnh), không cần bảng/bullet |
| `blank` | `title`, `placeholder?` | Slide để trống có chủ đích |
| `word_groups` | `groups[]` = `{label, items[]}`, mỗi `item` = `{hz, py, vn}` | N nhóm xếp CẠNH NHAU (banner nhãn to 30pt + bảng con 汉字\|Pinyin\|Nghĩa mỗi dòng 1 ví dụ) — tự xếp lưới thích ứng theo số nhóm (≤3 → 1 hàng, 4 → 2×2, >4 → nhiều hàng x4 cột) để cột luôn đủ rộng, không rớt dòng. Dùng cho bảng luyện đọc theo nhóm 声母/韵母 thay vì nhồi nhiều ví dụ vào 1 ô |
| `stroke_group` | `principle`, `chars[]` = `{hanzi, pinyin, meaning, image}` | N chữ Hán CÙNG minh hoạ 1 nguyên tắc viết nét, xếp thẻ ngang (ảnh GIF nét + nhãn) dưới 1 dòng nguyên tắc chung — tránh lặp nguyên tắc giống hệt nhau nhiều slide (vd 一/二/三 đều "nét ngang, trái→phải") |
| `info_grid` | `cards[]` = `{label, image?, py?, caption?}` | N thẻ (ảnh + label CJK đậm + pinyin + caption Việt) xếp LƯỚI trong 1 slide (≤4 thẻ → 1 hàng, >4 → 4 cột nhiều hàng) — dùng khi 1 slide cần NHIỀU ảnh cùng lúc (vd hồ sơ 1 quốc gia: cờ+biểu tượng+thủ đô+ngôn ngữ+tiền tệ), khác mọi type khác chỉ hỗ trợ 1 ảnh/slide |

Ghi chú:
- **`dialogue`**: speaker xuất hiện **đầu tiên** căn trái, các speaker khác căn phải.
- **`table.cjk_cols`**: mảng chỉ số cột (0-based) dùng font CJK. Mặc định (khi bỏ trống/KHÔNG có field): cột 0 là nhãn tiếng Việt, các cột còn lại là CJK. ⚠️ `cjk_cols: []` (mảng RỖNG) khác với bỏ hẳn field — `[]` ép TOÀN BỘ cột về non-CJK, kể cả cột chứa câu Hán thuần. Hậu quả: renderer ước lượng độ rộng chữ theo font Latin (hẹp hơn CJK) → tính thiếu số dòng cần wrap → chữ tràn ô ("rớt dòng"). Bảng có cột chứa câu/từ tiếng Trung PHẢI khai đúng index cột đó vào `cjk_cols` (vd `[0, 1]`), không để `[]` nếu có cột CJK.
- **`image`**: đường dẫn ảnh **tương đối theo thư mục chứa file JSON**. Thiếu file → renderer vẽ khung xám placeholder (không lỗi). Cần `Pillow` để giữ đúng tỉ lệ ảnh (đã có sẵn). Hỗ trợ ở `title/vocab/grammar/dialogue/bullets/exercise/table/image` (không có ở `reading`).
- **`footer_note`** (mọi type): 1 dòng chú thích nhỏ ở đáy slide (vd đối chiếu
  giáo trình khác) — thay cho việc phải làm 1 slide `bullets` đứng riêng.
- **`tip`** (`bullets`/`exercise`/`answers`/`grammar`): mẹo ghi nhớ, LUÔN render
  ở dải footer riêng (đáy slide, có icon 🔑) — **tách khỏi luồng nội dung
  chính**, không chèn vào cuối bullet/ví dụ như trước. Nếu slide có cả `tip`
  và `footer_note`, `tip` nằm ngay trên `footer_note`. Vùng nội dung chính tự
  trừ hao chỗ cho dải này (không cần tính tay).
- Chữ Hán được gắn đúng thuộc tính font Đông Á (`a:ea`/`a:cs`) nên hiển thị chuẩn trong PowerPoint, không bị nhảy về font Latin.

**`vocab` — 2 chế độ render (2026-08-07):** nếu slide có `image` hoặc `example`
cấp SLIDE → tự chuyển sang **chế độ thẻ**: ảnh to (bên trái mặc định, `image_side`
đổi được) + câu ví dụ dùng chung ngay dưới ảnh (cỡ chữ ~28pt, tự co nếu câu dài,
**tự tô đỏ mọi từ trong `items[].hz` xuất hiện trong câu ví dụ** — không cần khai
`highlight` tay), bên phải là danh sách thẻ từ (không bảng) canh GIỮA theo cả
nhóm dù 1-3 từ. Không có `image`/`example` → giữ bảng cũ (`_vocab_table`, hợp
cho liệt kê nhanh nhiều từ không cần ảnh/ví dụ riêng, vd bảng tổng kết cuối
buổi). Thay thế `word_pair` cho trường hợp "2-3 từ ghép chung 1 câu ví dụ tự
nhiên" (khác `word_pair` gốc — mỗi từ ảnh/ví dụ RIÊNG, hợp khi 2 từ không liên
quan nhau).

**Chọn `vocab` (bảng) hay `wordcard`/`word_pair` (1-2 từ/slide) cho 生词 chính (2026-08-06):**
`references/slide-design-best-practices.md` (đóng gói trong `chinese-teaching.skill`) ghi
"từ vựng = BẢNG cân cột, dùng type `vocab`" — quy tắc này có từ trước khi `wordcard`/
`word_pair` tồn tại, chưa từng được đối chiếu lại sau khi 2 type mới ra đời. Thực tế sản
xuất gần đây (Buổi 8, 9) dùng `wordcard`/`word_pair` cho **toàn bộ 生词** (kể cả mở rộng),
đi sâu từng từ + ví dụ + ảnh riêng — quyết định giữ theo hướng này (user chốt 2026-08-06).
Dùng `vocab` (bảng) khi: liệt kê nhanh không cần ảnh/ví dụ riêng từng từ (vd bảng tổng kết
cuối buổi, bảng đối chiếu). Mặc định cho 生词 dạy mới trong 1 buổi: `wordcard` (1 từ, cần
đào sâu) hoặc `word_pair` (2 từ liên quan/slide, khi số lượng lớn cần nén gọn).

Xem [example-lesson.json](example-lesson.json) — mẫu bao trùm mọi loại slide.

## Audio giọng bản địa (nút 🔊)

Thêm key `"audio": "assets/audio/slideNN.mp3"` vào slide → renderer nhúng nút 🔊
ở góc phải header (PowerPoint nhận là **Sound**, bấm/di chuột để phát).

Sinh tự động bằng helper:

```bash
"$PY" .claude/skills/teaching-coach/pptx/slide_audio.py <lesson.json>
```

→ đọc chữ Hán của các slide (vocab / wordcard / grammar / dialogue / passage /
bảng `口语`), gọi `edge-tts` sinh mp3 vào `assets/audio/` và tự gắn key `audio`.
Cần internet; `--force` để sinh lại.

**⚠️ Cổng duyệt bắt buộc (2026-08-04, user nhắc lại 2 lần trong 1 session):**
KHÔNG chạy `slide_audio.py` cho tới khi user đã duyệt **TOÀN BỘ** nội dung JSON
sẽ build (mọi slide, không chỉ phần vừa sửa). Duyệt 1 slide/1 phần nhỏ qua chat
KHÔNG đồng nghĩa "sẵn sàng sinh audio cả deck" — đặc biệt vì chèn/xoá/reorder 1
slide bắt buộc audio TOÀN BỘ phải sinh lại (xem cảnh báo vị trí bên dưới), nên
"duyệt cục bộ" rồi chạy audio cho cả deck sẽ tốn công sinh lại nếu còn slide
khác chưa chốt. Không chắc → hỏi thẳng "nội dung đã chốt hết chưa, sinh audio
bản cuối được chưa?" trước khi chạy, đừng tự suy diễn từ 1 lời duyệt cục bộ.

**Giọng & tốc độ (2026-08-04, sau feedback "giọng cũ nghe mệt/robot"):**
- Slide thường (vocab/wordcard/grammar/table/passage): luân phiên 2 giọng
  `zh-CN-XiaoxiaoNeural` ("Warm") / `zh-CN-XiaoyiNeural` ("Lively"), mặc định
  `--rate=-15%`.
- Hội thoại (`dialogue`): 3 giọng theo người nói (`DIALOGUE_VOICES`), mặc định
  `--rate=-8%` (gần tốc độ tự nhiên hơn — hội thoại ưu tiên nhịp giống người
  thật, không cần chậm như từ vựng). Auto-assign theo THỨ TỰ xuất hiện, không
  theo giới tính — người nói thứ 2 luôn ra giọng thứ 2 cố định (`Yunxi`, nam)
  dù nhân vật đó là nữ (vd hội thoại 2 mẹ con đều nữ). Sai giới tính → thêm
  field `"voices": {"<tên speaker>": "zh-CN-XiaoyiNeural"}` vào slide
  `dialogue` đó để ghi đè, key phải khớp đúng chuỗi `speaker` trong `turns[]`.
  **Chủ động kiểm tra TRƯỚC khi chạy `slide_audio.py`** (2026-08-05): với MỌI
  slide `dialogue`, xác nhận giới tính từng speaker khớp giọng sẽ auto-assign
  theo thứ tự xuất hiện — không đợi user nghe ra rồi mới sửa.
  **Nhân vật TRẺ CON (2026-08-07):** 4 giọng nam/nữ hay dùng (Xiaoxiao/Xiaoyi/
  Yunxi/Yunyang/Yunjian) đều là giọng NGƯỜI LỚN — kể cả Yunxi nghe "trẻ trung"
  vẫn là giọng thanh niên, không phải trẻ em. Dùng riêng **`zh-CN-YunxiaNeural`**
  (mô tả chính thức "Cartoon, Cute", đã xác nhận có trên edge-tts) cho nhân vật
  là trẻ em. **Nhân vật xuất hiện ở NHIỀU 课文 trong cùng 1 buổi phải liệt kê
  hết trước khi gán `voices`** — tránh 2 nhân vật khác nhau (vd bố ở 课文1,
  con ở 课文3) vô tình trùng giọng do chỉ xét từng 课文 riêng lẻ.
- `--rate=...` (CLI) override cho CẢ HAI loại cùng lúc nếu cần đồng nhất (vd
  buổi ngữ âm nhập môn muốn chậm hơn hẳn, `--rate=-30%`).

Text được đọc tự trích theo `type` của slide — không cần field `audio_text`
riêng:
- `vocab` → `hz` của từng `items[]`; nếu có `example` cấp SLIDE (chế độ THẺ,
  xem mục audio) → đọc thêm `hz` của câu ví dụ đó sau cùng
- `wordcard` → `hz` của từ + `hz` của từng `examples[]`
- `word_pair` → `hz` của từng `words[]` + `hz` của `example` (nếu có), theo thứ tự cột trái→phải
- `passage` → `hz` của từng `sentences[]`
- `grammar` → `hz` của từng `examples[]`
- `dialogue` → từng `turns[].hz`, mỗi speaker 1 giọng riêng rồi ghép thành 1 mp3
- `table` kicker `口语` → cột đầu mỗi hàng; kicker `写字` (bảng tham chiếu
  nét/quy tắc) → **bỏ qua**, không phải từ vựng để đọc; các `table` khác →
  quét MỌI ô, trích cụm chữ Hán liên tục đầu tiên trong ô (đủ dùng cho cả
  bảng giới thiệu 声母/韵母 lẫn bảng luyện đọc 汉字/Pinyin/Nghĩa tách cột)
- `table` kicker `练习` mà **không có chữ Hán** (bảng luyện đọc thuần pinyin,
  vd 辨别声母/辨别韵母) → đọc trực tiếp các âm tiết pinyin (bỏ ô nhãn tiếng
  Việt — nhận diện qua dấu đặc trưng đ/ư/ơ/... hoặc dấu ngoặc mô tả nhóm)
- `word_groups` → `hz` của mọi `items[]` trong mọi `groups[]`
- `stroke_group` → `hanzi` của từng `chars[]`
- `bullets` kicker `写字` → cụm chữ Hán đầu tiên tìm được trong `title`
- Còn lại (title/image/reading/blank/`bullets` khác…) → không sinh audio

> ⚠️ **Pinyin PHẢI có dấu thanh mới đọc được.** edge-tts không xử lý tốt
> pinyin không dấu (vd `"ba"` — không biết đọc thanh nào) nên bảng luyện đọc
> kiểu `type: "table"` chứa pinyin trần bị bỏ qua ÂM THẦM (không lỗi, không
> log) nếu không thêm dấu. Buổi ngữ âm chưa dạy thanh điệu thì mặc định gắn
> dấu thanh 1 (ngang cao) cho toàn bộ — vừa nhất quán "ưu tiên thanh 1 khi
> chưa học thanh điệu", vừa để audio đọc được.

> ⚠️ **Sắp lại thứ tự slide sau khi đã sinh audio:** `slide_audio.py` đặt tên file audio
> theo VỊ TRÍ slide tại thời điểm chạy (`slideNN.mp3`), không theo nội dung/hash. Nếu sau
> đó chèn/xoá/di chuyển slide ở vị trí giữa (không phải chỉ thêm cuối), các file cũ vẫn còn
> tên đó nhưng giờ ứng với slide khác — script thấy file "đã tồn tại" nên BỎ QUA, khiến slide
> mới phát nhầm audio cũ, không có cảnh báo. Luôn `rm assets/audio/*.mp3` rồi chạy lại từ đầu
> (không cần `--force`) sau khi đổi thứ tự slide.
>
> ⚠️ **Biến thể khác gây cùng hậu quả (2026-08-07): `slide_audio.py` bị timeout/kill
> giữa chừng.** Các slide đã xử lý XONG trước khi bị kill vẫn ghi mp3 ra đĩa bình
> thường — chạy lại (kể cả chạy nền) thấy file "đã tồn tại" nên bỏ qua y hệt lỗi
> trên, dù không hề đổi thứ tự slide. Sau bất kỳ lần `slide_audio.py` bị timeout/
> kill giữa chừng, PHẢI coi như đã đổi thứ tự slide — `rm assets/audio/*.mp3` rồi
> chạy lại TOÀN BỘ, không tin file "đã tồn tại" là file đúng/đủ.

> **Console tiếng Trung trên Windows:** chạy với `PYTHONIOENCODING=utf-8` ở trước lệnh —
> nếu không, script có thể crash `UnicodeEncodeError` giữa chừng khi `print` tiến độ (mp3
> vẫn sinh ra bình thường trước khi crash; chạy lại với biến này thì các slide đã xong sẽ
> tự skip, chỉ log bị mất dòng đó).

> ⚠️ **Drive/Google Slides KHÔNG phát audio nhúng.** Chỉ nghe được khi mở bằng
> **PowerPoint thật** (desktop hoặc app điện thoại) — tải file về rồi trình chiếu.
> Trình xem trực tiếp trên Drive hoặc Google Slides sẽ không kêu.

## Ảnh minh hoạ (Openverse CC)

Sinh manifest `{name, query}` → chạy `fetch_images.py <manifest.json>` (xem docstring đầu
file) → tải vào `out_dir`, ghi `credits.json`. Sau đó gắn `"image": "assets/<name>.jpg"` vào
từng slide (`title/vocab/grammar/dialogue/bullets/exercise/table/image` hỗ trợ `image` —
`reading` không có).

**Bắt buộc gen ảnh theo TỪNG từ vựng trước khi để trống (2026-08-07):** với mọi
slide có field `image` (đặc biệt `wordcard`/`word_pair` — thiết kế vốn có ảnh sticker
riêng từng từ), luôn chủ động chạy `fetch_images.py` thử tải ảnh thật TRƯỚC — không
được nhảy thẳng sang placeholder chỉ vì tiện. Chỉ sau khi đã đổi query thử **đủ 2 lượt**
(xem mục "Query ngắn mới ra kết quả"/"Quy tắc chọn query khi từ trừu tượng" bên dưới) mà
vẫn không ra ảnh phù hợp/đứng đắn thì mới bỏ field `image` (hoặc gắn placeholder
`assets/words/<slug>_TODO.jpg` theo quy ước ở mục word_pair phía trên) — để chỗ trống
đúng nghĩa "đã cố nhưng không có", không phải "chưa thử".

**Known issues chờ điều tra kỹ hơn (2026-08-07, phát hiện khi làm Buổi 9):**
- **Bong bóng hội thoại (`_slide_dialogue`) quá khổ**: chiều rộng/chiều cao bubble hiện
  rộng rãi hơn cần thiết so với nội dung thật — user phải tự canh lại tay. Cần xem lại
  công thức `_bubble_w`/`_lines_at` để bubble ôm sát nội dung hơn, không chỉ tránh tràn.
- **Header (`_band_header`) vẫn tràn** dù đã khôi phục auto-shrink theo bề rộng ký tự
  ước lượng (`_text_width_pt`) — nghĩa là bản khôi phục đó (xem mục lịch sử `word_pair`
  ở trên) chưa xử lý hết mọi trường hợp tràn thật. Cần đo lại bằng ảnh xuất thật
  (`Slide.Export` qua PowerPoint COM, xem mục QA trong best-practices) thay vì chỉ tin
  công thức ước lượng ký tự.
- **`highlight` (tô đỏ từ ngữ pháp chính) mới chỉ có ở `type: grammar`** — slide
  `table` dùng để so sánh nhiều quy tắc (vd 时量补语 "Tân ngữ đứng ở đâu") chưa hỗ trợ
  tô đỏ từ khoá trong cột Ví dụ. Cân nhắc mở rộng `_set_run_highlighted` sang
  `_fill_cell`/`_slide_table` ở phiên sau.

⚠️ **Query ngắn mới ra kết quả:** `search()` lọc `license_type=commercial&orientation=wide`
— query TIẾNG ANH dài (>3 từ, vd `"world flags icon simple"`) hay ra **0 kết quả** dù chủ đề
phổ biến. Luôn dùng query 1-3 từ đơn giản (`"flags"`, `"Eiffel Tower"`, `"panda"`) — nếu 0
kết quả, rút ngắn lại trước khi đổi hẳn chủ đề tìm.

**Quy trình chọn query khi từ trừu tượng (2026-08-05):** thử query bám sát
NGHĨA TỪ trước; nếu từ là tính từ/khái niệm trừu tượng khó minh hoạ trực tiếp
(vd 过时, 迷人, 有品味, 流行) → đổi sang query bám theo NỘI DUNG CÂU VÍ DỤ của
từ đó thay vì cố tìm ảnh literal cho khái niệm. Không cần hỏi user trước khi
thử — chỉ cần Read lại ảnh tải về để soát (bước 2 dưới) trước khi gắn vào slide.
**Bước cuối nếu cả 2 lượt đều không ra ảnh phù hợp/đứng đắn (2026-08-06):** dừng
lại, KHÔNG cố đổi query thêm nhiều vòng — bỏ hẳn field `"image"` cho slide đó
(để trống, renderer tự vẽ khung xám placeholder), báo user để họ tự tìm/gắn ảnh
tay sau. Đừng chấp nhận ảnh "tạm được" chỉ để có ảnh — khung trống còn hơn ảnh sai.

⚠️ **Soát nội dung ảnh, không chỉ soát đúng chủ đề:** ngoài việc ảnh có khớp
nghĩa từ hay không, phải loại các ảnh phản cảm/hở hang/có chữ không phù hợp
in trên đồ vật, ảnh người mẫu ăn mặc hở dù đúng chủ đề (vd tìm "swimsuit" ra
ảnh bikini người mẫu) — đổi query cụ thể hơn (vd "beach towel", "swim gear
flatlay") thay vì chấp nhận ảnh không phù hợp cho lớp học. Riêng từ nhạy cảm
tự thân (vd 内衣) — cân nhắc bỏ qua ảnh, không cần cố tìm bằng được.

**Bắt buộc 2 bước trước khi `build_deck.py`:**
1. **Convert non-JPEG → JPEG thật.** Openverse đôi khi trả ảnh WEBP nhưng script vẫn lưu
   đuôi `.jpg` → `build_deck.py` sẽ crash `ValueError: unsupported image format ... WEBP`.
   Kiểm tra + convert bằng Pillow trước khi build:
   ```python
   from PIL import Image
   import glob
   for f in glob.glob("assets/*.jpg"):
       im = Image.open(f)
       if im.format != "JPEG":
           im.convert("RGB").save(f, "JPEG", quality=90)
   ```
2. **Xem lại từng ảnh bằng Read tool trước khi build.** Query CC stock photo cho khái niệm
   ngữ pháp trừu tượng (vd "đang xem TV", "dưới bàn") tỷ lệ trả về ảnh lạc đề khá cao (ảnh
   nghệ thuật, ảnh cũ sai bối cảnh, biểu đồ thay vì vật thể...) — đừng tin `OK` của
   `fetch_images.py` là ảnh đúng nội dung. Ảnh nào sai → xoá file, đổi `query` cụ thể hơn,
   chạy lại `fetch_images.py` (đã tải rồi sẽ `CACHED`, chỉ tải lại ảnh bị xoá).

**`build_deck.py` báo `PermissionError` khi ghi file `.pptx`:** file đích đang mở trong
PowerPoint (khoá file) — đóng cửa sổ PowerPoint rồi chạy lại.

**Mở lại file cho user xem sau khi rebuild dễ bị nhầm bản cache cũ:** nếu PowerPoint
đang mở sẵn file đó (kể cả đã tưởng đóng), mở lại bằng script (vd `Invoke-Item`) đôi
khi chỉ đưa cửa sổ CŨ đang mở lên trước, không load lại nội dung mới từ đĩa — user
tưởng bug (audio/nội dung "chưa cập nhật") trong khi file trên đĩa đã đúng. Gặp báo
lỗi kiểu "sao chưa đổi" sau rebuild → nhắc user **đóng hẳn toàn bộ cửa sổ PowerPoint**
(không chỉ đóng tab) rồi mở lại, trước khi kết luận có bug thật.

⚠️ **`dialogue` bong bóng rớt/tràn chữ khi câu dài (2026-08-06):** renderer cũ tính
chiều cao bubble giả định hz/py/vn LUÔN chỉ 1 dòng — sai khi câu dài chạm mức
`max_bubble_w` (7.6in), buộc phải tự wrap xuống ≥2 dòng nhưng bubble vẫn thấp như
1 dòng → chữ tràn/mất ở đáy. Đã sửa: tính lại `bubble_w` trước, rồi dùng
`_wrap_lines` để đếm số dòng THẬT trong đúng bề rộng đó mới suy ra `bubble_h`
(không còn giả định số dòng cố định).

⚠️ **Slide ít nội dung dồn lên đầu, trống cả mảng dưới (2026-08-06):** `grammar`/
`bullets`/`exercise` neo cố định `MSO_ANCHOR.TOP` (để tránh đè header khi nội
dung nhiều) — nhưng khi nội dung ÍT hơn khung (`scale == 1.0`, không cần co),
neo TOP làm chữ dồn hết lên đầu, để trống hẳn nửa dưới slide. Đã sửa: chỉ neo
TOP khi `scale < 1.0` (nội dung thật sự vượt khung); còn lại neo MIDDLE để
phân bổ đều theo chiều dọc.

⚠️ **`passage` đổi layout — bỏ chia cột trái/phải (2026-08-07):** layout cũ (ảnh
1 bên, câu tự sự 1 bên hẹp) khiến câu dài phải wrap nhiều dòng trong cột hẹp,
nhìn như bị "xé thành nhiều cột". Đã đổi: ảnh (nếu có) lên dải TRÊN full-width
(≤32% chiều cao khung), câu văn xuống 1 CỘT RỘNG full-width bên dưới, mỗi câu
đánh số ①②③ ở đầu để tách bạch.

**口语 (khẩu ngữ tự nhiên, cuối buổi) — dùng `type: "grammar"` thay vì `table`
(2026-08-07):** `table` với `image` từng bị hiểu nhầm/khó kiểm soát chiều cao
khi có 5+ hàng ngắn; `grammar` (không cần `point`, chỉ `image` + `examples[]`
= các cụm câu khẩu ngữ) tái dùng đúng layout "ảnh 1 bên + danh sách cụm câu
(Hán tự đậm + pinyin cùng dòng, nghĩa xuống dòng, giãn cách rộng)" đã ổn định
sẵn — không cần code mới, tránh trùng khẩu ngữ với 生词/语法 đã dạy trong buổi.

⚠️ **Bảng `vocab` (hz/py/nghĩa) rớt dòng cột 汉字 khi item là CẢ CÂU (2026-08-06):**
cột 汉字 mặc định chỉ 26% bề rộng — đủ cho 1-2 từ nhưng câu dài (vd lời chúc
"祝您福如东海，寿比南山！") wrap quá nhiều dòng so với chiều cao hàng chia đều
`height/nrow`, chữ Hán bị tràn đáy ô. Đã sửa: cột 汉字 lên 40% + chiều cao mỗi
hàng tính theo số dòng 汉字 THẬT cần wrap (dùng `_wrap_lines`), Pinyin/Nghĩa
được PHÉP hẹp/rớt dòng trước (ưu tiên 汉字 không bao giờ mất chữ).

## Đồng bộ audio vào file .pptx đã bị sửa tay (không rebuild từ JSON)

⚠️ **Bắt buộc hỏi trước khi rebuild sau khi đã mở file cho user xem** (2026-08-05,
sự cố thật: user sửa tay cả buổi sáng trong PowerPoint, bị AI rebuild đè mất — chỉ
cứu được nhờ file autosave tình cờ còn sót lại trong `AppData/Roaming/Microsoft/
PowerPoint/*.tmp`). Ngay khi đã dùng `Invoke-Item`/mở file `.pptx` cho user xem 1
lần, coi như file đó có thể đang/đã bị sửa tay — **trước khi chạy `build_deck.py`
lần tiếp theo, PHẢI hỏi thẳng "bạn có sửa tay gì trong PowerPoint và đã lưu chưa"**.
Có → dừng, xử lý theo quy trình đồng bộ audio bên dưới (không rebuild từ JSON). Chỉ
rebuild thẳng khi chắc chắn user chưa đụng vào file kể từ lần mở gần nhất.

⚠️ **Không suy diễn "an toàn" từ lời user tóm tắt phạm vi sửa (2026-08-06, lặp lại
sự cố trên):** user báo "chỉ xoá 1 slide" (không nhắc ảnh) → tin lời đó là đủ để
`build_deck.py` rebuild lại cho "đồng bộ" → xoá mất ~8 ảnh dán tay không được nhắc
tới trong câu trả lời. Lời tóm tắt của user về phạm vi sửa **không đáng tin bằng
chính file trên đĩa** — luôn coi MỌI hand-edit là có thể kèm ảnh/thay đổi khác chưa
được kể ra, dùng quy trình đồng bộ audio riêng (add_movie trực tiếp vào file hiện
có) thay vì `build_deck.py`, trừ khi đã tự mở file kiểm tra từng slide và xác nhận
không có ảnh/nội dung nào khác ngoài phạm vi họ nói.

User có thể chỉnh tay trực tiếp file `.pptx` đã build (xoá/tách/dời slide, đổi ảnh)
thay vì sửa JSON rồi build lại — hợp lý vì rebuild từ JSON sẽ **xoá sạch** các chỉnh
sửa tay đó (ảnh/layout). Khi đó cần đồng bộ lại audio theo đúng nội dung/thứ tự HIỆN
TẠI của file, không phải build lại.

Cách làm: viết script Python riêng (không sửa `build_deck.py`) —
1. Mở file bằng `Presentation(path)`, đọc text từng slide hiện tại (`shape.text_frame.text`)
   để xác nhận đúng nội dung/thứ tự sau khi user sửa tay (đừng tin lại state cũ).
2. Map từng slide về đúng object trong JSON gốc (theo `kicker`/`title`) để lấy lại text
   cần đọc — nếu 1 slide bị TÁCH thành nhiều slide (vd 1 dialogue dài chia 2), đối
   chiếu NGUYÊN VĂN từng dòng còn lại với `turns[]` gốc để biết chính xác đoạn nào
   thuộc slide nào (khớp theo nội dung, không đoán theo vị trí).
3. Sinh mp3 (dùng lại `slide_audio.tts`/`gen_dialogue` bằng cách `import slide_audio`).
4. **Xoá shape audio cũ trên slide đó trước khi thêm mới** (`shape.shape_type ==
   MSO_SHAPE_TYPE.MEDIA` → remove), rồi `slide.shapes.add_movie(...)`, cuối cùng
   `prs.save()` đè lên chính file đó — KHÔNG gọi `build_deck.py`.

**Script mẫu có sẵn:** [sync_audio_to_pptx.py](sync_audio_to_pptx.py) — dùng ngay
khi thứ tự/nội dung slide KHÔNG đổi (chỉ sửa layout/ảnh/format), map audio theo
INDEX trực tiếp (không cần đối chiếu `kicker`/`title`):
```bash
"$PY" .claude/skills/teaching-coach/pptx/slide_audio.py <slide/buoiX.json>   # sinh mp3 trước
"$PY" .claude/skills/teaching-coach/pptx/sync_audio_to_pptx.py <slide/buoiX.json> <slide/Buoi-X-....pptx>
```
Script tự chặn (báo lỗi, không ghi) nếu số slide trong pptx khác số slide trong JSON —
dấu hiệu slide đã bị tách/xoá, khi đó phải làm theo quy trình đối chiếu NGUYÊN VĂN ở
bước 1-4 phía trên (viết script riêng cho trường hợp đó, không dùng file mẫu này).

**2 lỗi python-pptx đã gặp khi làm việc này (chỉ xảy ra trên file đã qua chỉnh tay
nhiều lần, không xảy ra khi build từ JSON sạch):**
- `add_movie(..., poster_frame_image=<path>)` crash `IndexError` ở
  `_video_part_rIds[1]` → bỏ hẳn tham số này (`poster_frame_image=None`), PowerPoint
  vẫn hiện icon mặc định, chỉ mất icon loa tuỳ biến.
- `_find_by_sha1` (trong `pptx.package`) crash `AttributeError: 'Part' object has no
  attribute 'sha1'` — do PowerPoint để lại 1 relationship MEDIA/VIDEO mồ côi (từ audio
  đã bị xoá thủ công trước đó) trỏ tới part không phải `MediaPart` thật. Vá bằng
  monkeypatch tại chỗ (không sửa thư viện cài đặt):
  ```python
  import pptx.package as _pptx_package
  def _safe_find_by_sha1(self, sha1):
      for media_part in self:
          if getattr(media_part, "sha1", None) == sha1:
              return media_part
      return None
  _pptx_package._MediaParts._find_by_sha1 = _safe_find_by_sha1
  ```

## Nguyên tắc thiết kế (đã nhúng sẵn trong renderer)

Renderer tự áp các nguyên tắc trong `references/slide-design-best-practices.md`
của skill: mỗi slide một ý, action title + gạch accent, giới hạn nội dung,
tránh font-soup/color-rainbow. Việc của người soạn JSON chỉ là **chia nội dung
đúng block + đặt action title tốt** — không phải chỉnh format.

## Mở rộng

Thêm loại slide mới = thêm 1 method `_slide_<type>(self, s)` trong
[build_deck.py](build_deck.py). Renderer tự động route theo tên `type`.
