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
| `exercise` | `instructions?`, `items[]` (+ `image?`, `word_bank?`) | Slide bài tập (đánh số) |
| `answers` | `items[]` (+ `word_bank?`) | Slide đáp án (đánh số) |
| `bullets` | `bullets[]` (+ `image?`, `word_bank?`) | Gạch đầu dòng thường |

**`exercise`/`answers`/`bullets` — item 2 dòng "nhãn\ncâu" (2026-08-13):** mỗi phần tử
trong `items[]`/`bullets[]` có thể là 1 chuỗi chứa `\n` — dòng ĐẦU (trước `\n`) render
đậm + cỡ lớn hơn (vai trò nhãn/tóm tắt ngắn), dòng SAU render cỡ thường (vai trò nội
dung chi tiết/bài tập của nhãn đó). Khoảng cách TRƯỚC mỗi item (cụm) rộng hơn khoảng
cách nội bộ giữa 2 dòng trong cùng 1 item, để mắt phân biệt được cụm nào với cụm nào —
dùng khi cần format "tóm tắt ngắn gọn ngay trên đầu bài tập/gạch đầu dòng của chính nó"
(vd buổi ôn tập tổng hợp: mỗi điểm ngữ pháp 1 dòng tóm tắt + 1 dòng bài tập kiểm tra).
Item chỉ 1 dòng (không có `\n`) vẫn hoạt động như cũ, không bị ảnh hưởng.
| `image` | `image`, `caption?`/`captions[]` | Ảnh lớn canh giữa (sơ đồ/biểu đồ tĩnh), không cần bảng/bullet |
| `blank` | `title`, `placeholder?` | Slide để trống có chủ đích |
| `word_groups` | `groups[]` = `{label, items[]}`, mỗi `item` = `{hz, py, vn}` | N nhóm xếp CẠNH NHAU (banner nhãn to 30pt + bảng con 汉字\|Pinyin\|Nghĩa mỗi dòng 1 ví dụ) — tự xếp lưới thích ứng theo số nhóm (≤3 → 1 hàng, 4 → 2×2, >4 → nhiều hàng x4 cột) để cột luôn đủ rộng, không rớt dòng. Dùng cho bảng luyện đọc theo nhóm 声母/韵母 thay vì nhồi nhiều ví dụ vào 1 ô |
| `stroke_group` | `principle`, `chars[]` = `{hanzi, pinyin, meaning, image}` | N chữ Hán CÙNG minh hoạ 1 nguyên tắc viết nét, xếp thẻ ngang (ảnh GIF nét + nhãn) dưới 1 dòng nguyên tắc chung — tránh lặp nguyên tắc giống hệt nhau nhiều slide (vd 一/二/三 đều "nét ngang, trái→phải") |
| `info_grid` | `cards[]` = `{label, image?, py?, caption?}` | N thẻ (ảnh + label CJK đậm + pinyin + caption Việt) xếp LƯỚI trong 1 slide (≤4 thẻ → 1 hàng, >4 → 4 cột nhiều hàng) — dùng khi 1 slide cần NHIỀU ảnh cùng lúc (vd hồ sơ 1 quốc gia: cờ+biểu tượng+thủ đô+ngôn ngữ+tiền tệ), khác mọi type khác chỉ hỗ trợ 1 ảnh/slide |

Ghi chú:
- **`dialogue`**: speaker xuất hiện **đầu tiên** căn trái, các speaker khác căn phải.
- **`table.cjk_cols`**: mảng chỉ số cột (0-based) dùng font CJK. Mặc định (khi bỏ trống/KHÔNG có field): cột 0 là nhãn tiếng Việt, các cột còn lại là CJK. ⚠️ `cjk_cols: []` (mảng RỖNG) khác với bỏ hẳn field — `[]` ép TOÀN BỘ cột về non-CJK, kể cả cột chứa câu Hán thuần. Hậu quả: renderer ước lượng độ rộng chữ theo font Latin (hẹp hơn CJK) → tính thiếu số dòng cần wrap → chữ tràn ô ("rớt dòng"). Bảng có cột chứa câu/từ tiếng Trung PHẢI khai đúng index cột đó vào `cjk_cols` (vd `[0, 1]`), không để `[]` nếu có cột CJK.
- **`image`**: đường dẫn ảnh **tương đối theo thư mục chứa file JSON**. Thiếu file → renderer vẽ khung xám placeholder (không lỗi). Cần `Pillow` để giữ đúng tỉ lệ ảnh (đã có sẵn). Hỗ trợ ở `title/vocab/grammar/dialogue/bullets/exercise/table/image` (không có ở `reading`).
- **`word_bank`** (`exercise`/`answers`/`bullets`, 2026-08-14): mảng `{hz, py}` render thành 1 dải "Từ cần dùng: ..." full-width ngay dưới header, TRƯỚC nội dung chính. Dùng cho bài tập đục lỗ (`[___]`) không có slide `vocab`/`wordcard` nào đứng ngay trước để giới thiệu từ — nếu không học viên không biết chính xác 5 (hay N) từ mục tiêu cần điền là từ nào (từng bị hỏi "từ cần điền đâu?" khi thiếu). Nên xáo trộn thứ tự `word_bank` so với thứ tự xuất hiện trong câu (ở tầng soạn JSON) để vẫn cần suy luận theo nghĩa, không chỉ điền theo thứ tự.
- **`footer_note`** (mọi type): chú thích nhỏ ở đáy slide (vd đối chiếu giáo
  trình khác, hoặc mẹo chiết tự từ vựng — xem dưới) — thay cho việc phải làm 1
  slide `bullets` đứng riêng. Nhận **string** (1 dòng, layout gốc) hoặc **list
  string** (2026-08-19: nhiều dòng, mỗi phần tử 1 dòng riêng — dùng khi 1 slide
  có nhiều từ cần mẹo riêng, vd `word_pair`/`vocab` 2 từ/slide). Renderer tự
  giãn chiều cao dải footer theo số dòng thực tế (không cần tính tay) — nhưng
  với `vocab`/`word_pair` (2 loại duy nhất có thể có >1 từ/slide), nơi gọi PHẢI
  cộng thêm `self._footer_lines_extra(s)` vào `_content_area_h()` để trừ đúng
  chỗ, nếu không nội dung chính sẽ tràn xuống đè lên dải footer nhiều dòng.
  **Mẹo chiết tự từ vựng (dùng `footer_note` cho mục đích này):** tra
  `.claude/skills/vocab-study/data/hanzi.json` lấy bộ thủ + pinyin + nghĩa
  từng phần làm nguồn — không tự bịa cách chiết tự khi không có nguồn/không
  chắc (thà để trống còn hơn ghi sai). Tuyệt đối không dùng thuật ngữ ngôn ngữ
  học ("mượn âm", "biểu âm", "hình thanh", "phiên thiết") — người đọc không có
  nền Hán Việt sẽ không hiểu; nếu 1 bộ phận chỉ biểu âm (không mang nghĩa),
  DROP hẳn khỏi lời giải thích, chỉ giữ bộ phận có nghĩa/hình ảnh thật. Với từ
  vay mượn phiên âm nước ngoài (vd T恤, 台风) — nói thẳng đó là phiên âm, không
  gán nghĩa giả cho chữ Hán dùng để ghi âm.
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

**⚠️ Cổng duyệt bắt buộc (2026-08-04, user nhắc lại 2 lần trong 1 session; TÁI DIỄN
2026-08-12 Buổi 15 — lần thứ 3):** KHÔNG chạy `slide_audio.py` cho tới khi user đã
duyệt **TOÀN BỘ** nội dung JSON sẽ build (mọi slide, không chỉ phần vừa sửa). Duyệt
1 slide/1 phần nhỏ qua chat KHÔNG đồng nghĩa "sẵn sàng sinh audio cả deck" — đặc biệt
vì chèn/xoá/reorder 1 slide bắt buộc audio TOÀN BỘ phải sinh lại (xem cảnh báo vị trí
bên dưới), nên "duyệt cục bộ" rồi chạy audio cho cả deck sẽ tốn công sinh lại nếu còn
slide khác chưa chốt. Không chắc → hỏi thẳng "nội dung đã chốt hết chưa, sinh audio
bản cuối được chưa?" trước khi chạy, đừng tự suy diễn từ 1 lời duyệt cục bộ.
**Cụ thể tái diễn ở Buổi 15:** user chỉ trả lời 2 câu hỏi trắc nghiệm hẹp (giữ/bỏ
danh sách từ mở rộng, có/không thêm 1 slide) — KHÔNG phải trình bày rồi hỏi "chốt
chưa" — nhưng bị hiểu lầm là đã duyệt xong cả deck, build luôn pptx+audio. Trả lời
1-2 câu hỏi lựa chọn hẹp KHÔNG đồng nghĩa duyệt toàn văn; phải trình đủ text mọi
slide (title + mọi item/ví dụ) rồi hỏi thẳng mới được sinh audio.

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
  **⚠️ `zh-CN-YunxiaNeural` là giọng NAM** (2026-08-10, xác nhận qua
  `edge_tts --list-voices`: `Male, Cartoon, Cute`) — dù mô tả nghe "trẻ con"
  chung chung dễ tưởng trung tính, gán cho nhân vật NỮ trẻ em sẽ đọc sai giới
  tính. Toàn bộ giọng `zh-CN-*` cơ bản (không kể phương ngữ) chỉ có:
  Nữ = `XiaoxiaoNeural` (Warm), `XiaoyiNeural` (Lively/Cartoon); Nam =
  `YunyangNeural` (Professional), `YunjianNeural` (Passion), `YunxiNeural`
  (Lively/Sunshine), `YunxiaNeural` (Cute/trẻ em, CHỈ nam). **Không có giọng
  nữ trẻ em riêng** — nếu cần nhân vật nữ trẻ em, dùng tạm `XiaoyiNeural`
  (gần "cartoon" nhất trong 2 giọng nữ) và chấp nhận không phân biệt hẳn với
  giọng nữ người lớn. **Hội thoại ≥3 người CÙNG giới tính bắt buộc phải share
  giọng** (vd 3 nhân vật nữ chỉ có 2 giọng nữ để chia) — ưu tiên để 2 nhân vật
  không nói liên tiếp nhau dùng chung 1 giọng, người còn lại (vd giáo viên/vai
  trung tâm) giữ giọng riêng để dễ phân biệt nhất trong hội thoại đó.
- `--rate=...` (CLI) override cho CẢ HAI loại cùng lúc nếu cần đồng nhất (vd
  buổi ngữ âm nhập môn muốn chậm hơn hẳn, `--rate=-30%`).

Text được đọc tự trích theo `type` của slide. **Trừ khi slide có field
`audio_text`** (chuỗi tuỳ ý) — khi đó đọc ĐÚNG chuỗi này, bỏ qua mọi rule theo
`type` bên dưới. Dùng cho slide mà nội dung hiển thị không tự trích được câu
để đọc, điển hình nhất là `exercise` đục lỗ (`[___]` không phải chữ Hán nên
không tự trích ra được câu liền mạch) — gắn `audio_text` = câu GỐC chưa che,
để vẫn có audio đọc câu đầy đủ (học viên coi như 1 dạng nghe kiểm tra sau khi
điền, không nghe không sao vì phần nhìn vẫn đục lỗ bình thường).

Không có `audio_text` → trích theo `type`:
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

> ⚠️ **Tự sinh pinyin hàng loạt cho câu văn tự soạn (không phải từ đơn) bằng
> `pypinyin` hay sai đa âm tự mặc định (2026-08-14, phát hiện khi soạn ~38 câu
> ví dụ ôn tập HSK2 Phần 2)** — `pypinyin.pinyin(..., heteronym=False)` chọn âm
> theo từ điển nội bộ, không hiểu ngữ pháp câu, nên các trợ từ/động từ đa âm
> sau hay bị đọc SAI nếu không ép tay theo từng vị trí xuất hiện:
> - **得** — LUÔN là "de" (nhẹ) trong mọi câu ở buổi này (bổ ngữ trình độ
>   V+得+tính từ, hoặc các cụm cố định 记得/懂得/舍得/值得): pypinyin hay trả về
>   "dé" (nặng, nghĩa "đạt được" như 得到/得意) — ép "de" TOÀN CỤC an toàn trừ
>   khi câu thật sự dùng nghĩa "đạt được".
> - **着** — LUÔN "zhe" (trợ từ tiếp diễn V+着) trong ngữ cảnh thông thường —
>   ép TOÀN CỤC an toàn.
> - **地** — CHỈ "de" khi làm trạng ngữ (tính từ/động từ + 地 + động từ, vd
>   "高兴地画"); còn lại (vd 地方/地址 — "nơi chốn/địa chỉ") giữ nguyên "dì" mặc
>   định của pypinyin. KHÔNG được ép toàn cục — phải chỉ định đúng VỊ TRÍ xuất
>   hiện (0-based occurrence index trong câu) cần ép, còn lại giữ mặc định.
> - **过** — "guo" (nhẹ, trợ từ kinh nghiệm "đã từng", vd "来过") khác "guò"
>   (nặng, động từ "đi qua/trải qua", vd "过去", "过得非常美好") — phải ép theo
>   từng vị trí xuất hiện cụ thể, không ép toàn cục.
> - **长** — "cháng" (dài, thời lượng/độ dài) khác "zhǎng" (lớn lên/đứng đầu) —
>   pypinyin hay mặc định nhầm sang "zhǎng"; câu chỉ nói về ĐỘ DÀI/THỜI GIAN
>   thì ép "cháng" theo vị trí xuất hiện.
> - **教** — "jiāo" (động từ "dạy", vd "教我们") khác "jiào" (danh từ/cụm cố
>   định như 教室/教育) — pypinyin hay mặc định "jiào"; câu dùng làm ĐỘNG TỪ
>   thì ép "jiāo" theo vị trí xuất hiện.
>
> Cách làm an toàn: viết wrapper quanh `pypinyin.pinyin()` trả về list 1-1
> theo từng KÝ TỰ (không phải theo từ), ép cứng 得/着 toàn cục, và nhận thêm
> tham số override dạng `{group_index: (vị_trí_xuất_hiện_0_based, ...)}` cho
> 地/过/长/教 (và bất kỳ đa âm tự nào khác gặp phải) để chỉ ép đúng lần xuất
> hiện cần thiết, không đụng các lần khác cùng ký tự trong cùng câu. ⚠️ Coi
> chừng dấu câu ghép nhiều ký tự (vd "——" 2 dấu gạch ngang liền) — pypinyin có
> thể gộp thành 1 token duy nhất, làm lệch alignment ký tự↔token cho MỌI ký tự
> phía sau trong câu đó; luôn `assert len(tokens) == len(text)` để bắt lỗi này
> sớm, hoặc tránh hẳn các dấu câu ghép khi soạn câu ví dụ.

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

**Đừng quên gắn ảnh cho `vocab` chủ đề thực dụng (2026-08-12, Buổi 15):** khác
`wordcard`/`word_pair` (vốn ép có ảnh theo thiết kế), `image` ở `vocab` chỉ là field
tùy chọn nên dễ bị bỏ sót hoàn toàn nếu không tự nhắc — buổi 15 đã soạn xong 12 slide
`vocab` không có ảnh nào, phải đợi user nhắc mới bổ sung. Mặc định: nếu từ vựng có vật/
cảnh thực tế minh hoạ được (đồ vật, địa danh, hoạt động — không phải hư từ/khái niệm
ngữ pháp), chủ động gen ảnh trước khi trình user duyệt, trừ khi có quyết định rõ ràng
bỏ ảnh cho buổi đó (vd buổi quá dày chữ, muốn gọn).

**Known issues chờ điều tra kỹ hơn (2026-08-07, phát hiện khi làm Buổi 9):**
- **Bong bóng hội thoại (`_slide_dialogue`) quá khổ**: chiều rộng/chiều cao bubble hiện
  rộng rãi hơn cần thiết so với nội dung thật — user phải tự canh lại tay. Cần xem lại
  công thức `_bubble_w`/`_lines_at` để bubble ôm sát nội dung hơn, không chỉ tránh tràn.
- ✅ **Header (`_band_header`) tràn khi kicker dài — đã sửa (2026-08-11, Buổi 14):**
  nguyên nhân thật là tab kicker có bề rộng CỐ ĐỊNH `Inches(1.5)` bất kể độ dài chữ —
  kicker ngắn (`"语法 1/4"`) vừa khít, nhưng kicker dài (`"语法 3/4 · 拓展"`) bị wrap 2
  dòng và tràn khỏi khung (auto-shrink cũ chỉ áp dụng cho TITLE, không áp dụng cho tab
  kicker). Đã sửa: bề rộng tab co giãn theo `_text_width_pt(kicker, ...)` ước lượng
  (floor 1.5in, trần 3.6in), vượt trần mới co cỡ chữ kicker xuống tối thiểu 11pt.
- ✅ **Header tràn khi TITLE dài (khác nguyên nhân với kicker ở trên) — đã sửa
  (2026-08-10):** dù đã auto-shrink cỡ chữ theo bề rộng ước lượng, `_text_width_pt`
  vẫn chỉ là công thức gần đúng — title dài (mix Hán+Việt, hoặc ghép 2 vế bằng
  "—") có thể vẫn wrap xuống 2 dòng thật trong PowerPoint dù ước lượng nói vừa 1
  dòng, và band/khung tiêu đề trước đây LUÔN cố định 1 dòng (`BAND_H`) nên 2 dòng
  đó tràn xuống đè nội dung. Đã sửa: đo lại SỐ DÒNG THỰC bằng `_wrap_lines` (cùng
  công cụ dùng cho mọi nội dung khác) ở cỡ chữ đã co, rồi NỚI RỘNG cả `band` và
  khung tiêu đề đủ chỗ cho đúng số dòng đó. `_content_top()` giờ đọc theo
  `self._band_h` (lưu per-slide trong `_new_slide`/`_band_header`), không còn
  hằng số `BAND_H` cố định cho mọi slide.
- **`highlight` (tô đỏ từ ngữ pháp chính) mới chỉ có ở `type: grammar`** — slide
  `table` dùng để so sánh nhiều quy tắc (vd 时量补语 "Tân ngữ đứng ở đâu") chưa hỗ trợ
  tô đỏ từ khoá trong cột Ví dụ. Cân nhắc mở rộng `_set_run_highlighted` sang
  `_fill_cell`/`_slide_table` ở phiên sau.
- ✅ **`vocab` chế độ thẻ — cột từ dọc hẹp cố định tràn/wrap khi ≥4-5 thẻ từ
  dài — đã sửa (2026-08-14, ôn tập HSK2 Phần 2):** `_slide_vocab_cards` (nhánh
  có `example` cấp slide) từng LUÔN xếp thẻ từ CHỒNG DỌC trong 1 cột hẹp cố
  định (~19% content width khi không ảnh, ~32% khi có ảnh) — với từ 4 chữ (vd
  不好意思) và ≥4-5 thẻ/slide, cột hẹp này làm chữ wrap 2 dòng rồi tràn khỏi
  khung (thấy rõ khi mở bằng PowerPoint thật, khác preview trong 1 số app xem
  nhanh). Đã sửa: thêm `_slide_vocab_cards_row` — câu ví dụ full-width (hoặc
  chia sẻ với cột ảnh nếu có `image`) ở TRÊN, thẻ từ xếp thành 1 HÀNG NGANG
  ngay dưới (mỗi thẻ tự co theo bề rộng khả dụng/số từ, cỡ chữ 汉字 tự giảm
  theo độ dài từ: ≤2 chữ giữ cỡ gốc, 3-4 chữ giảm nhẹ, ≥5 chữ giảm thêm). Áp
  dụng cho MỌI slide `vocab` có `example`, kể cả khi có `image` (ảnh chiếm 1
  cột dọc riêng trái/phải qua `image_side`, phần còn lại mới chia trên/dưới
  như thường).

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
(Hán tự đậm, pinyin XUỐNG DÒNG RIÊNG ngay dưới — đổi lại 2026-08-11, review
Buổi 14: để cùng dòng làm hàng quá dài/khó đọc khi câu ví dụ dài — nghĩa Việt
tiếp tục xuống dòng của nó, giãn cách rộng)" đã ổn định
sẵn — không cần code mới, tránh trùng khẩu ngữ với 生词/语法 đã dạy trong buổi.

⚠️ **Bảng `vocab` (hz/py/nghĩa) rớt dòng cột 汉字 khi item là CẢ CÂU (2026-08-06):**
cột 汉字 mặc định chỉ 26% bề rộng — đủ cho 1-2 từ nhưng câu dài (vd lời chúc
"祝您福如东海，寿比南山！") wrap quá nhiều dòng so với chiều cao hàng chia đều
`height/nrow`, chữ Hán bị tràn đáy ô. Đã sửa: cột 汉字 lên 40% + chiều cao mỗi
hàng tính theo số dòng 汉字 THẬT cần wrap (dùng `_wrap_lines`), Pinyin/Nghĩa
được PHÉP hẹp/rớt dòng trước (ưu tiên 汉字 không bao giờ mất chữ).

⚠️ **`vocab` chế độ THẺ (`_slide_vocab_cards`) — cột ví dụ rớt dòng khi không có
`image` (2026-08-12, Buổi 15 HSK2):** cột thẻ từ (bên phải, chỉ chứa 1-2 chữ Hán
to + pinyin + nghĩa) trước đây LUÔN chiếm cố định `min(3.8in, 32%)` bất kể có
ảnh hay không — khi slide chỉ có `example` (không `image`), cột ví dụ bên trái
bị ép hẹp lại theo phần còn dư, ví dụ dài (2 dòng 汉字 + pinyin + nghĩa Việt)
tính `natural_h` vượt `ex_h` nhưng `sz()` có floor cứng (16/11/11pt) chặn không
co xuống được nữa → chữ tràn xuống dưới khung, mất dòng cuối. Đã sửa: thêm
nhánh riêng khi KHÔNG có `image` — cột thẻ từ hẹp lại `min(2.4in, 19%)` (vẫn đủ
rộng cho từ 3 âm tiết như 登机牌/登机口 không bị tách đôi), nhường phần dư cho
cột ví dụ (từ ~66% lên ~77% content width).

⚠️ **Hội thoại ≥3 người (`_dialogue_script`, swimlane nhiều cột) — bug lệch
khoảng cách giữa các thẻ cùng cột (2026-08-10, KHÁC với việc đánh số thứ tự
"1./2./3." đã làm ở Buổi 14 — đánh số chỉ giúp đọc đúng thứ tự, không sửa bug
này):** code cũ dùng 1 biến `y` DÙNG CHUNG cho mọi cột, cộng dồn theo đúng thứ
tự lượt thoại trong mảng `turns` bất kể lượt đó thuộc cột nào — nghĩa là lượt
của cột B cũng đẩy con trỏ `y` xuống, để lại khoảng trống "ma" trong cột A
đúng bằng chiều cao lượt cột B đó (user báo "card cùng cột cách nhau xa gần
không đều"). Đã sửa: mỗi cột (người nói) có timeline riêng (`y_col` dict theo
cột), `natural`/scale tính theo cột CAO NHẤT thay vì tổng tất cả lượt.
**TODO chưa giải quyết gốc rễ:** layout cột độc lập (dù đã đánh số) vẫn khó
đọc trực quan hơn hội thoại 2 người dạng bong bóng trái/phải, đặc biệt hội
thoại kiểu gọi điện xen giữa 2 nơi. User muốn thiết kế lại layout này ở 1
session riêng sau.

⚠️ **Bullet "•/◦" trơ trọi xuất hiện ở đoạn văn thứ 2+ trong textbox tự do
(2026-08-10):** mọi `_slide_*` tạo nhiều đoạn văn qua `tf.add_paragraph()`
(vd dòng pinyin/nghĩa dưới câu ví dụ 生词) — PowerPoint THẬT vẫn áp list style
mặc định của theme (`otherStyle` trong `txStyles`) cho các đoạn không khai báo
rõ, dù shape là textbox tự do (không phải placeholder) lẽ ra không nên có
bullet. Hiện ra như 1 dấu chấm tròn trơ trọi ở đầu dòng. Đã sửa TOÀN CỤC (áp
dụng mọi slide, không riêng 1 chỗ): `_set_run` giờ gọi `_no_bullet(run)` trước
khi gán text — chèn tường minh `<a:buNone/>` vào `pPr` của đoạn chứa run đó
(idempotent, không chèn trùng nếu đoạn đã xử lý).

⚠️ **Xóa slide khỏi file `.pptx` đã build KHÔNG được chỉ gỡ khỏi `sldIdLst`
(2026-08-11, Buổi 12 HSK2):** cách làm nhanh `xml_slides = prs.slides._sldIdLst;
xml_slides.remove(...)` (recipe phổ biến trên mạng) chỉ bỏ slide khỏi thứ tự
hiển thị — **không xóa relationship** tương ứng trong `presentation.xml.rels`,
để lại 1 quan hệ "mồ côi" vẫn trỏ tới đúng file `slideN.xml` đang được slide
khác dùng chung tên. Hậu quả xuất hiện ở lần `prs.save()` KẾ TIẾP (không phải
ngay lúc xóa): python-pptx tự tính lại partname cho mọi part, đếm nhầm số
lượng do quan hệ mồ côi này → 2 slide khác nhau bị gán cùng tên file trong zip
(vd `slide13.xml` xuất hiện 2 lần với nội dung khác nhau) → PowerPoint/
python-pptx đọc lại chỉ thấy 1 trong 2 (thường là bản sai), nội dung slide còn
lại coi như mất. Xảy ra 2 lần liên tiếp trong 1 session (lần đầu khi xóa+thêm
slide cùng lúc, lần hai chỉ vì sửa 1 chữ rồi save lại) — phải vá tay ở tầng
zip/XML (gỡ trùng tên, xóa hẳn relationship mồ côi) mới ổn định.
**Quy tắc:** khi cần xóa slide khỏi 1 file `.pptx` đã build (đặc biệt file đã
có ảnh/audio dán tay, không rebuild được từ JSON):
1. Xóa CẢ HAI: entry trong `sldIdLst` **và** relationship tương ứng trong
   `presentation.xml.rels` (regex xóa nguyên `<Relationship Id="rIdX".*?/>`).
2. Sau khi xóa, KHÔNG gọi thêm `add_slide()`/sửa run text nào trong CÙNG 1 lần
   `Presentation()...save()` — mở lại file, kiểm tra `zipfile.namelist()` không
   có tên trùng, rồi mới làm bước tiếp theo (add/edit) ở 1 lần mở file MỚI.
3. Sau MỌI lần `save()` trên file đã qua thao tác này, luôn tự kiểm tra lại
   bằng `collections.Counter(ZipFile(path).namelist())` tìm entry có count > 1
   trước khi báo user là xong — im lặng không kiểm tra dễ báo "xong" nhưng thực
   ra đã mất nội dung.

⚠️ **生词 tách hoàn toàn khỏi 课文 gốc → cần hoạt động nhận diện, không bắt
production (2026-08-11, Buổi 12 HSK2):** khi user muốn đổi nhóm 生词 sang chủ đề
khác (vd từ thời tiết cơ bản sang thời tiết mạnh/thiên tai) nhưng **giữ nguyên
课文** gốc sách (không viết lại hội thoại), 生词 mới sẽ không xuất hiện trong bất
kỳ câu 课文 nào của buổi — đặc biệt rủi ro nếu từ mới khó/trừu tượng hơn hẳn cấp
học (vd HSK2 học từ thiên tai như 火山爆发/山体滑坡). Bắt học viên tự đặt câu
比较句 với những từ này ngay là quá tải. Giải pháp đã áp dụng: thêm 1-2 hoạt động
CHỈ nhận diện (ghép tranh-từ kiểu 热身 gốc sách, hoặc đoạn đọc ngắn tự viết sẵn
câu hoàn chỉnh + hỏi đúng/sai) ngay sau phần 生词, trước khi vào 课文 — học viên
chỉ cần HIỂU câu có sẵn, không phải tự sản sinh câu với từ khó. Tránh dùng
flashcard đơn thuần (liệt kê từ không có hoạt động) khi rơi vào tình huống này.

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

**Thêm 1 slide MỚI vào file đã bị sửa tay, không rebuild toàn bộ** (2026-08-10,
buổi 13 HSK2: user tự thêm ảnh tay + lưu vào 5 slide, sau đó muốn thêm slide 口语
2/2 — rebuild từ JSON lúc này sẽ xoá sạch ảnh tay). Cách làm: dùng lại đúng
class `DeckBuilder` (cùng style/renderer với các slide khác) nhưng gắn `.prs`
của nó vào file ĐANG có thay vì để nó tự tạo Presentation() rỗng, rồi gọi thẳng
method `_slide_<type>` cho MỖI slide mới cần thêm:
```python
import sys, json
sys.path.insert(0, ".claude/skills/teaching-coach/pptx")
import build_deck as bd
from pptx import Presentation

path = "output/hskN/buoiX_.../slide/Buoi-X-....pptx"
spec = json.loads(open("output/hskN/buoiX_.../slide/buoiX.json", encoding="utf-8").read())
spec.setdefault("_base", "output/hskN/buoiX_.../slide")   # để resolve path ảnh

builder = bd.DeckBuilder(spec)
builder.prs = Presentation(path)              # nạp file HIỆN CÓ, không tạo mới
builder.blank = builder.prs.slide_layouts[6]  # lấy lại layout blank từ chính file đó

new_slide_spec = spec["slides"][-1]           # slide mới, đã thêm vào cuối JSON
builder._slide_grammar(new_slide_spec)        # gọi đúng handler theo "type"
builder.prs.save(path)
```
Muốn đổi 1 kicker/text có sẵn (vd đổi "口语" thành "口语 1/2" khi tách thêm
slide 2/2) thì sửa trực tiếp run text qua `slide.shapes` (đối chiếu
`shape.text_frame.text` để tìm đúng shape) TRƯỚC khi gọi `_slide_<type>` thêm
slide mới, cùng 1 lần mở file — không cần `build_deck.py`.

⚠️ **Sau khi thêm slide mới, user tự DỜI VỊ TRÍ slide đó trong PowerPoint —
phải đánh số lại TOÀN BỘ kicker theo đúng thứ tự VẬT LÝ mới, không phải thứ tự
lúc thêm** (2026-08-11, Buổi 14 HSK2: thêm slide `语法 5/5` ở cuối, user dời nó
lên nằm cạnh `语法 2/5` trong PowerPoint). Quy trình:
1. Quét lại text từng slide hiện tại (`shape.text_frame.text`) để biết đúng
   thứ tự VẬT LÝ mới — đừng tin lại thứ tự lúc build.
2. Đánh số lại kicker theo thứ tự đó bằng **rename 2-pass qua nhãn tạm**
   (`"语法 3/5" -> "__TMP__0__" -> "语法 4/5"`, vv.) — bắt buộc 2 pass vì nhiều
   kicker đổi số CHÉO nhau cùng lúc (vd slide cũ 3→4 và 4→5), rename thẳng 1
   pass sẽ ghi đè nhầm giá trị đã đổi của slide khác.
3. **Đồng bộ lại thứ tự phần tử trong `buoiX.json` cho khớp** (di chuyển phần
   tử trong mảng `slides`, không chỉ sửa text kicker) — bỏ qua bước này để lại
   sai lệch thứ tự JSON ≠ thứ tự pptx thật, tái diễn đúng lớp lỗi audio bị lệch
   nội dung đã ghi ở mục "Đồng bộ audio" phía trên (`slide_audio.py` đặt tên
   file mp3 theo thứ tự JSON, không phải thứ tự pptx).

✅ **Đánh số lượt thoại ≥3 người — đã tự động hoá trong renderer (2026-08-11,
Buổi 14):** `_dialogue_script` (swimlane, kích hoạt khi >2 speaker) giờ tự in
số thứ tự `"1. "/"2. "/...` trước mỗi lượt thoại khi build từ JSON — không cần
sửa tay `p.runs[0].text` như trước nữa (thứ tự đọc trước/sau giữa các cột dễ bị
mất khi chỉ nhìn vị trí, xem review Buổi 14: "hội thoại 3 người chưa đánh số").
Kỹ thuật sửa tay ở trên chỉ còn cần khi thao tác trên file ĐÃ QUA CHỈNH TAY
(không rebuild từ JSON sạch).

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
