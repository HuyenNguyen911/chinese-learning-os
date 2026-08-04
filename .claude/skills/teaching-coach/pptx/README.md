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
2. Ánh xạ nội dung sang các block JSON bên dưới — mỗi ý một slide, action title.
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
| `vocab` | `items[]` = `{hz, py, vn}` (+ `image?`, `image_side?`, `color?`, `ex?`, `example?`) | Bảng từ vựng 汉字\|Pinyin\|Nghĩa; nếu item có `color` (hex, vd `"E74C3C"`) → chèn cột **chip màu** (bài dạy màu sắc); nếu item có `ex` (câu ví dụ riêng từng từ) → chèn cột **Ví dụ** cuối bảng; `example?` (cấp SLIDE, không phải item) = `{hz,py,vn}` 1 câu ví dụ chung — render **tách riêng khỏi bảng** (chữ thường, không khung): có ảnh → hiện dưới ảnh; không ảnh → hiện dưới bảng; có `image` → ảnh + bảng. Danh sách dài (>~8 từ) → tách thành 2 slide `vocab` liên tiếp thay vì nhồi 1 bảng (renderer không tự tách). |
| `wordcard` | `hz`, `py?`, `vn?`, `pos?`, `examples[]` = `{hz, py, vn}` (tối đa 3), `image?` | **1 từ / 1 slide** — 汉字 lớn + pinyin + nghĩa + ảnh sticker minh hoạ bên trái, tối đa 3 câu ví dụ bên dưới. Dùng khi cần đào sâu từng từ thay vì dồn bảng nhiều từ/slide (số từ nhiều → số slide tăng tương ứng, cân nhắc thời lượng buổi học). |
| `grammar` | `point?`, `examples[]` = `{hz, py, vn}`, `note?`, `source?`, `image?` | Giảng ngữ pháp |
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

**Giọng & tốc độ (2026-08-04, sau feedback "giọng cũ nghe mệt/robot"):**
- Slide thường (vocab/wordcard/grammar/table/passage): luân phiên 2 giọng
  `zh-CN-XiaoxiaoNeural` ("Warm") / `zh-CN-XiaoyiNeural` ("Lively"), mặc định
  `--rate=-15%`.
- Hội thoại (`dialogue`): 3 giọng theo người nói (`DIALOGUE_VOICES`), mặc định
  `--rate=-8%` (gần tốc độ tự nhiên hơn — hội thoại ưu tiên nhịp giống người
  thật, không cần chậm như từ vựng).
- `--rate=...` (CLI) override cho CẢ HAI loại cùng lúc nếu cần đồng nhất (vd
  buổi ngữ âm nhập môn muốn chậm hơn hẳn, `--rate=-30%`).

Text được đọc tự trích theo `type` của slide — không cần field `audio_text`
riêng:
- `vocab` → `hz` của từng `items[]` (không đọc câu ví dụ)
- `wordcard` → `hz` của từ + `hz` của từng `examples[]`
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

⚠️ **Query ngắn mới ra kết quả:** `search()` lọc `license_type=commercial&orientation=wide`
— query TIẾNG ANH dài (>3 từ, vd `"world flags icon simple"`) hay ra **0 kết quả** dù chủ đề
phổ biến. Luôn dùng query 1-3 từ đơn giản (`"flags"`, `"Eiffel Tower"`, `"panda"`) — nếu 0
kết quả, rút ngắn lại trước khi đổi hẳn chủ đề tìm.

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

## Nguyên tắc thiết kế (đã nhúng sẵn trong renderer)

Renderer tự áp các nguyên tắc trong `references/slide-design-best-practices.md`
của skill: mỗi slide một ý, action title + gạch accent, giới hạn nội dung,
tránh font-soup/color-rainbow. Việc của người soạn JSON chỉ là **chia nội dung
đúng block + đặt action title tốt** — không phải chỉnh format.

## Mở rộng

Thêm loại slide mới = thêm 1 method `_slide_<type>(self, s)` trong
[build_deck.py](build_deck.py). Renderer tự động route theo tên `type`.
