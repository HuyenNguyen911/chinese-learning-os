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
4. Chạy `build_deck.py <slide/buoiX.json> <slide/Buoi-X-....pptx>`.
5. Báo đường dẫn file cho học viên.

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
| `vocab` | `items[]` = `{hz, py, vn}` (+ `image?`, `image_side?`, `color?`, `ex?`) | Bảng từ vựng 汉字\|Pinyin\|Nghĩa; nếu item có `color` (hex, vd `"E74C3C"`) → chèn cột **chip màu**; nếu có `ex` (câu ví dụ dùng từ) → chèn cột **Ví dụ** cuối bảng; có `image` → ảnh + bảng. Danh sách dài (>~8 từ) → tách thành 2 slide `vocab` liên tiếp thay vì nhồi 1 bảng (renderer không tự tách). |
| `wordcard` | `hz`, `py?`, `vn?`, `pos?`, `examples[]` = `{hz, py, vn}` (tối đa 3), `image?` | **1 từ / 1 slide** — 汉字 lớn + pinyin + nghĩa + ảnh sticker minh hoạ bên trái, tối đa 3 câu ví dụ bên dưới. Dùng khi cần đào sâu từng từ thay vì dồn bảng nhiều từ/slide (số từ nhiều → số slide tăng tương ứng, cân nhắc thời lượng buổi học). |
| `grammar` | `point?`, `examples[]` = `{hz, py, vn}`, `note?`, `source?`, `image?` | Giảng ngữ pháp |
| `table` | `headers[]`, `rows[][]` (+ `cjk_cols[]`) | Bảng so sánh (vd 了 vs 过) |
| `dialogue` | `turns[]` = `{speaker, hz, py, vn?}` | Khung hội thoại (bong bóng chat 2 phía) — hội thoại nhiều lượt nên **bỏ `vn`** để bong bóng không tràn/đụng nhau |
| `passage` | `title`, `sentences[]` = `{hz, py, vn}` (+ `note?`, `image?`, `image_side?`) | Đoạn văn tự sự/kể chuyện (课文 thể 叙述体, câu nối tiếp câu — KHÔNG phải hội thoại qua lại) — mỗi câu 1 khối, không dùng bong bóng thoại |
| `reading` | `groups[]` = `{label, items[]}` | Nguồn đọc thêm (nhóm "trong sách" / "nguồn ngoài") |
| `exercise` | `instructions?`, `items[]` (+ `image?`) | Slide bài tập (đánh số) |
| `answers` | `items[]` | Slide đáp án (đánh số) |
| `bullets` | `bullets[]` (+ `image?`) | Gạch đầu dòng thường |
| `blank` | `title`, `placeholder?` | Slide để trống có chủ đích |

Ghi chú:
- **`dialogue`**: speaker xuất hiện **đầu tiên** căn trái, các speaker khác căn phải.
- **`table.cjk_cols`**: mảng chỉ số cột (0-based) dùng font CJK. Mặc định (khi bỏ trống): cột 0 là nhãn tiếng Việt, các cột còn lại là CJK.
- **`image`**: đường dẫn ảnh **tương đối theo thư mục chứa file JSON**. Thiếu file → renderer vẽ khung xám placeholder (không lỗi). Cần `Pillow` để giữ đúng tỉ lệ ảnh (đã có sẵn).
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
bảng `口语`), gọi `edge-tts` (giọng `zh-CN-XiaoxiaoNeural`) sinh mp3 vào
`assets/audio/` và tự gắn
key `audio`. Cần internet; `--force` để sinh lại; `--voice=...` để đổi giọng.

> ⚠️ **Drive/Google Slides KHÔNG phát audio nhúng.** Chỉ nghe được khi mở bằng
> **PowerPoint thật** (desktop hoặc app điện thoại) — tải file về rồi trình chiếu.
> Trình xem trực tiếp trên Drive hoặc Google Slides sẽ không kêu.

## Nguyên tắc thiết kế (đã nhúng sẵn trong renderer)

Renderer tự áp các nguyên tắc trong `references/slide-design-best-practices.md`
của skill: mỗi slide một ý, action title + gạch accent, giới hạn nội dung,
tránh font-soup/color-rainbow. Việc của người soạn JSON chỉ là **chia nội dung
đúng block + đặt action title tốt** — không phải chỉnh format.

## Mở rộng

Thêm loại slide mới = thêm 1 method `_slide_<type>(self, s)` trong
[build_deck.py](build_deck.py). Renderer tự động route theo tên `type`.
