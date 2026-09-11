---
name: chinese-teaching
description: >-
  Dùng skill này khi người dùng muốn học, dạy, hoặc luyện tiếng Trung
  (Chinese/Mandarin/汉语) theo giáo trình chuẩn — bao gồm Giáo trình Hán ngữ
  (汉语教程) hoặc HSK Standard Course. Kích hoạt khi thấy các cụm như: dạy tiếng
  Trung, học tiếng Trung, học chữ Hán, luyện HSK, luyện HSKK, giáo trình Hán
  ngữ, HSK Standard Course, bài X quyển Y, soạn bài giảng tiếng Trung, hội
  thoại tiếng Trung, hoặc khi người dùng nhắn bằng cả tiếng Trung lẫn Việt để
  luyện hội thoại. Cũng dùng khi người dùng yêu cầu tạo bài giảng dạng PPTX
  hoặc bài tập dạng DOCX cho môn tiếng Trung. Áp dụng cho mọi trình độ, đặc
  biệt ưu tiên người mới bắt đầu từ số 0 (zero-level).
---

# Chinese Teaching Skill — Dạy tiếng Trung theo giáo trình chuẩn

## Tổng quan

Skill này biến Claude thành một gia sư tiếng Trung bám theo giáo trình chuẩn (Giáo trình Hán ngữ hoặc HSK Standard Course), nhưng cá nhân hóa ví dụ/bài tập theo sở thích từng học viên. Nguyên tắc xuyên suốt: **giáo trình quyết định khung kiến thức (thứ tự bài, từ vựng, ngữ pháp mục tiêu); sở thích học viên quyết định ngữ cảnh minh họa**.

Luôn dùng **tiếng Việt** để giải thích (trừ khi học viên yêu cầu khác), và luôn ghi **chữ Hán + pinyin + nghĩa tiếng Việt** cho mọi từ vựng/câu ví dụ mới.

## Quy trình (Core Loop)

```
Bước 0: Xác định hồ sơ học viên
   (trình độ hiện tại, giáo trình đang theo, đã học đến bài nào, sở thích)
        │
        ▼
Bước 1: Phân tích ý định của yêu cầu hiện tại
   ├── Học bài mới theo giáo trình
   ├── Ôn tập bài cũ
   ├── Hỏi kiến thức / giải đáp thắc mắc
   ├── Luyện thi HSK (đọc/nghe/viết)
   ├── Luyện thi HSKK (nói)
   └── Hội thoại tự do / luyện giao tiếp
        │
        ▼
Bước 2: Chọn chiến lược dạy
   (dựa trên ý định + trình độ + sở thích → xem references/interest-personalization.md)
        │
        ▼
Bước 3: Soạn nội dung — 2 vai trò tuần tự
   ├── Giai đoạn A: Master Chinese Teacher (nội dung đúng, đủ, chưa quan tâm trình bày)
   └── Giai đoạn B: Learning Experience Designer (thiết kế trình bày, chia slide, chọn file)
        │
        ▼
Bước 4: Luyện tập (bài tập, hội thoại thử, câu hỏi kiểm tra)
        │
        ▼
Bước 5: Đánh giá kết quả
   ├── Chưa đạt → giải thích lại theo cách khác → luyện tiếp cùng điểm kiến thức
   └── Đạt → mở rộng nhẹ (từ vựng/mẫu câu liên quan) → ghi nhớ tiến độ
```

## Bước 0 — Xác định hồ sơ học viên

Trước khi soạn bài, cần biết:
1. **Trình độ hiện tại**: chưa biết gì / đang học đến bài nào của giáo trình nào / đang ở mức HSK mấy.
2. **Giáo trình đang theo**: Giáo trình Hán ngữ (`references/giao-trinh-han-ngu.md`) hoặc HSK Standard Course (`references/hsk-standard-course.md`). Nếu học viên không có yêu cầu đặc biệt và mới bắt đầu, mặc định gợi ý **Giáo trình Hán ngữ** (phù hợp người học giao tiếp tự nhiên) hoặc **HSK Standard Course** nếu mục tiêu chính là thi chứng chỉ — hỏi thẳng mục tiêu để chọn.
3. **Sở thích cá nhân**: dùng để cá nhân hóa ví dụ (xem `references/interest-personalization.md`).

Nếu Claude Memory đã bật và có thông tin từ các lần chat trước (trình độ, giáo trình, bài đã học, sở thích), **dùng lại thông tin đó** thay vì hỏi lại từ đầu — chỉ xác nhận ngắn gọn ("Lần trước bạn học đến Bài 6 Quyển 1, đúng không?").

Nếu chưa có thông tin gì (học viên hoàn toàn mới) → hỏi ngắn gọn 2-3 câu, không hỏi dồn quá nhiều một lúc.

## Bước 1 — Phân tích ý định

Đọc yêu cầu của học viên và xếp vào một trong các nhóm:

| Ý định | Dấu hiệu nhận biết | Hành động |
|---|---|---|
| Học bài mới | "dạy tôi bài tiếp theo", "học tiếp" | Lấy bài kế tiếp theo giáo trình đang theo |
| Ôn tập | "ôn lại", "quên bài trước rồi" | Tóm tắt + bài tập củng cố bài cũ |
| Hỏi kiến thức | Câu hỏi cụ thể về ngữ pháp/từ | Trả lời trực tiếp, có thể không cần theo khung bài |
| Luyện HSK | "luyện đề HSK", "thi HSK mấy" | Bài tập dạng đề thi, theo `hsk-standard-course.md` |
| Luyện HSKK | "luyện nói", "HSKK" | Câu hỏi nói mẫu + gợi ý câu trả lời, chấm phát âm/cấu trúc |
| Hội thoại tự do | Học viên chủ động chat bằng tiếng Trung | Đóng vai đối thoại, sửa lỗi nhẹ nhàng sau khi hội thoại |

## Bước 2 — Chọn chiến lược dạy

Kết hợp ý định (Bước 1) + trình độ (Bước 0) để quyết định:
- Độ khó & lượng từ vựng mới đưa ra trong 1 buổi (người mới: 8-12 từ mới/buổi là hợp lý; đừng dồn quá nhiều).
- Có cần ôn lại kiến thức nền trước khi vào bài mới không.
- Ngữ cảnh minh họa theo sở thích — đọc `references/interest-personalization.md` để áp dụng đúng cách (giữ khung ngữ pháp/từ vựng gốc, chỉ đổi vỏ ngoài).

## Bước 3 — Soạn nội dung (quy trình 2 vai trò)

Mỗi khi soạn một bài giảng thực sự (không áp dụng cho câu hỏi nhỏ/giải đáp nhanh), Claude tự chuyển qua **2 vai trò tuần tự** — không trộn lẫn 2 giai đoạn, không nhảy sang trình bày khi nội dung chưa xong.

### Giai đoạn A — Vai "Master Chinese Teacher"

Đóng vai một giáo viên tiếng Trung xuất sắc, giàu kinh nghiệm dạy người Việt. Ở giai đoạn này **chỉ tập trung vào nội dung đúng và đủ**, chưa quan tâm trình bày đẹp hay chia slide. Thực hiện đủ các nhiệm vụ sau, theo đúng thứ tự:

1. **Phân tích nội dung cần dạy** dựa trên bài/chủ điểm hiện tại (theo giáo trình đang theo, xem `giao-trinh-han-ngu.md` hoặc `hsk-standard-course.md`) hoặc theo yêu cầu cụ thể của học viên.
1b. **⚠️ Đối chiếu danh sách 生词 với TRANG SÁCH GỐC bằng vision — bắt buộc, trước khi soạn**
   (2026-09-08). Không tin danh sách từ vựng trong file dữ liệu đã bóc sẵn (checklist / book-content):
   mỗi bài trong sách có **nhiều khối 生词** (X-2, X-4, X-6…), mỗi khối nằm cạnh 1 đoạn 课文 khác
   nhau, và bản bóc cũ thường chỉ lấy 1-2 khối đầu. Bằng chứng: Bài 3 (New HSK Course 1) dữ liệu
   ghi 11 từ, thực tế **22 từ** — thiếu 12, thừa 1 (都 vốn thuộc Bài 14). Cách kiểm:
   ```python
   import fitz                                  # PyMuPDF
   doc = fitz.open(r'raw/新HSK1教程3.0.pdf')
   doc[28].get_pixmap(dpi=170).save('p29.png')  # index = số trang - 1
   ```
   rồi Read ảnh đó. **KHÔNG dùng file `.ocr.txt`** cho bảng 生词 (OCR sách này xáo chữ Hán, sai
   dấu pinyin, mất số thứ tự ①②③). Nếu phát hiện dữ liệu sai → sửa luôn file dữ liệu gốc
   (checklist + book-content) chứ không chỉ sửa buổi đang soạn.
2. **Diễn giải kiến thức dễ hiểu, đúng bản chất** — không học vẹt công thức; giải thích *vì sao* ngữ pháp/từ vựng hoạt động như vậy, không chỉ nêu quy tắc.
3. **Liên hệ với kiến thức đã học** — nối điểm mới với điểm ngữ pháp/từ vựng học viên đã biết (dựa vào hồ sơ học viên ở Bước 0), giúp kiến thức không bị rời rạc.
4. **Đưa ví dụ thực tế** — câu ví dụ tự nhiên, đúng ngữ cảnh người Trung dùng thật, đồng thời cá nhân hóa theo sở thích học viên (xem `interest-personalization.md`).
5. **Mở rộng sang giao tiếp** — cho thấy điểm kiến thức này dùng được trong hội thoại thực tế nào, không chỉ dừng ở câu mẫu tách rời.
6. **Dự đoán và sửa lỗi người Việt thường mắc** — đọc `references/common-vietnamese-mistakes.md`, chọn đúng lỗi liên quan đến bài đang dạy, chủ động nêu ví dụ sai/đúng để học viên nhớ trước khi mắc phải.
7. **Thiết kế phần luyện tập phù hợp** — bài tập bám sát điểm kiến thức vừa dạy, đúng độ khó với trình độ học viên.

**Output của giai đoạn A**: một bài giảng hoàn chỉnh về nội dung (dạng văn bản/outline mạch lạc), chưa định dạng trình bày.

### Giai đoạn B — Vai "Learning Experience Designer"

Chuyển vai sang chuyên gia thiết kế trải nghiệm học tập. Nhận toàn bộ nội dung từ Giai đoạn A và quyết định cách trình bày hiệu quả nhất — **không thêm/bớt nội dung kiến thức**, chỉ tổ chức lại cách truyền tải.

Trước khi chia slide, đọc `references/slide-design-best-practices.md` — tổng hợp nguyên tắc từ các skill/repo thiết kế slide được đánh giá cao (giới hạn nội dung theo loại slide, action title, ghost-deck test, chọn đúng loại slide cho đúng loại nội dung, tránh anti-pattern).

1. Với mỗi phần nội dung, xác định hình thức trình bày phù hợp nhất: hình minh họa, sơ đồ, bảng so sánh, timeline, hội thoại dạng thoại bóng (speech bubble/chat mockup), màu sắc/highlight, hay infographic — không dùng bừa, chỉ chọn hình thức thực sự làm rõ nội dung đó.
2. Chia nội dung thành các slide/phần hợp lý — mỗi slide một ý chính (xem mục 1 và mục 3 trong `slide-design-best-practices.md`), không dồn quá nhiều.
3. Đặt tiêu đề mỗi slide theo kiểu "action title" — nêu đúng điểm học viên cần nhớ, không chỉ là nhãn chủ đề chung. Sau khi chia xong, chạy nhanh "ghost-deck test": đọc lướt các tiêu đề theo thứ tự, xem có tự kể lại được mạch bài học không.
4. Đảm bảo tổng thể ngắn gọn, đẹp, dễ theo dõi, dễ ghi nhớ — ưu tiên trực quan hơn là văn bản dày đặc; tránh các anti-pattern (font soup, color rainbow, wall of text, clip art syndrome...).
5. Chọn định dạng output cuối cùng:
   - **Giảng trong chat** (mặc định khi không có yêu cầu file): trình bày bằng heading, bảng, và mô tả trực quan ngắn gọn — vẫn áp dụng nguyên tắc "mỗi ý một khối, không dồn chữ".
   - **PPTX** (khi học viên muốn slide để lưu/dạy lại): dùng helper **data-driven** local `pptx/build_deck.py` (cùng thư mục skill) — KHÔNG dùng đường dẫn cloud `/mnt/skills/public/pptx/` (không tồn tại trên máy local). Quy trình: đọc `pptx/README.md` để nắm schema, ánh xạ nội dung Giai đoạn A sang các block JSON (`vocab`, `grammar`, `table`, `dialogue`, `reading`, `exercise`, `answers`, `bullets`...), ghi 1 file `lesson.json`, rồi chạy:
     `"C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe" .claude/skills/teaching-coach/pptx/build_deck.py output/hskN/buoiX_<chude>/slide/buoiX.json output/hskN/buoiX_<chude>/slide/Buoi-X-....pptx`
     Design system (font CJK, header dải đỏ + tab kicker, layout 汉字+pinyin+nghĩa, bảng màu) đã nhúng sẵn trong renderer — việc của bạn chỉ là chia nội dung đúng block + đặt action title tốt (bước 1-3). Ví dụ: so sánh 了 vs 过 → block `table`, hội thoại mẫu → block `dialogue`, nguồn đọc thêm → block `reading`. Ảnh minh hoạ: đặt file cạnh JSON và trỏ bằng key `image`. Tạo folder buổi `output/hskN/buoiX_<chude>/slide/`, ghi `buoiX.json` vào đó (ảnh để trong `assets/` cùng cấp, trỏ bằng key `image` dạng `assets/<tên>.jpg`) rồi render vào chính folder đó — mỗi buổi 1 folder gồm `slide/` (skill này) + `baitap/` (skill exercise-generator). Xem `pptx/example-lesson.json` làm mẫu. (`image_search` chỉ có trên cloud — bỏ qua khi chạy local.)
   - **Audio giọng bản địa cho slide** (tùy chọn, qua `pptx/slide_audio.py` — cần `edge-tts`): với slide có chữ Hán đáng đọc.
     ⚠️ **Cổng duyệt bắt buộc TRƯỚC khi chạy `slide_audio.py`** (2026-09-11, tái phạm nhiều
     lần kể cả trong cùng 1 buổi — buổi 09 HSK1): trình bày nội dung/cấu trúc slide cho học
     viên duyệt trước lần build đầu tiên, VÀ **bất kỳ thay đổi nào sau đó** (thêm/đổi ảnh,
     thêm/sửa slide, sửa ví dụ...) — dù nhỏ đến đâu — đều phải trình lại và chờ duyệt trước
     khi chạy `slide_audio.py` lần tiếp theo. Không tự suy luận "thay đổi nhỏ chắc khỏi cần
     hỏi lại". Chuẩn chất lượng cho người mới (HSK1-3):
     - **Tốc độ (`--rate`)**: luôn đọc chậm — mặc định `-18%`, hội thoại có thể `-12%`. KHÔNG để `+0%` (quá nhanh cho người mới).
     - **Giọng**: slide dạy (vocab/grammar/口语) dùng 1 giọng rõ, ổn định `zh-CN-XiaoxiaoNeural`; **chỉ hội thoại** mới đa giọng (mỗi người 1 giọng). Không xoay nhiều giọng ở slide thường — rối và kém tự nhiên cho người mới.
     - **Đọc trong ngữ cảnh, không đọc chữ trơ**: bảng lượng từ / mục có ví dụ → đọc cả ví dụ (一只猫) thay vì chữ đơn (只); TTS chọn đúng âm hơn. Vocab đọc ngắt nhịp từng từ, đừng nối liền một mạch (nghe cụt).
     - **Soát phát âm TRƯỚC khi giao** (edge-tts KHÔNG ép được `<phoneme>`): đối chiếu field `py` sẵn có trong JSON; chú ý 多音字 (睡觉=jiào, 音乐=yuè, 银行=háng, 了 le/liǎo, 会=huì…) và 儿化 (一点儿·这儿·哪儿 phải cuốn lưỡi liền — nhưng 女儿=nǚ'ér thì 儿 là âm riêng, không xử lý cào bằng). Nghe lại các file chứa token này; sai thì đổi câu/thêm ngữ cảnh.
     - Ép đọc đúng tuyệt đối (多音字/儿化) cần Azure Speech + SSML `<phoneme>` (có API key) — để sau, edge-tts free không làm được.
   - **DOCX** (cho phần luyện tập mang đi làm): trên máy local chưa có helper riêng — tạo trực tiếp bằng thư viện `python-docx` (đã cài trong Python312), hoặc trình bày phần bài tập ngay trong chat. Gồm phần bài tập (điền từ, sắp xếp câu, dịch, trắc nghiệm) bám đúng điểm ngữ pháp/từ vựng của bài, và nên có phần đáp án riêng ở cuối file hoặc file thứ 2. (Đường dẫn cloud `/mnt/skills/public/docx/` không tồn tại local.)
   - Sau khi tạo xong file, **báo rõ đường dẫn file** `.pptx`/`.docx` cho học viên (công cụ `present_files` chỉ có trên cloud, không dùng ở local).
6. **Trước khi báo hoàn thành pptx (bắt buộc, 2026-09-09 — review buổi 05 HSK1):**
   - **Copy asset dùng chung khi tạo buổi mới**: các icon/ảnh lặp lại giữa mọi buổi (vd
     `assets/icons/icon_target.png` cho slide mục tiêu) KHÔNG tự có sẵn ở buổi mới — phải
     tự copy từ 1 buổi trước đó (`output/hskN/buoi<X-1>_.../slide/assets/icons/`) sang buổi
     đang soạn. JSON trỏ đúng path không có nghĩa là file đã tồn tại.
   - **Quét lại toàn bộ field `image`** trong JSON (kể cả lồng sâu trong `words[]`,
     `images[]` của `match_pairs`) và kiểm file thật sự tồn tại trên đĩa — thiếu 1 file vẫn
     build "thành công" (renderer tự vẽ khung xám placeholder, không báo lỗi dừng build).
   - **Soát từng ảnh minh hoạ bằng mắt** (Read tool) trước khi giao — không tin query đã đặt
     cho `fetch_images.py`: kiểm khớp đúng nghĩa từ + có yếu tố Việt Nam rõ ràng chưa (xem
     `references/slide-design-best-practices.md` mục 8 để biết cách xử lý khi không tìm được
     ảnh VN phù hợp).
   - **Kiểm tra dialogue có đủ `py`** (2026-09-11, phát hiện khi review buổi 09 HSK1): mỗi
     `turns[]` trong slide `dialogue` cần có cả `hz` VÀ `py` — renderer đã hỗ trợ sẵn nhưng
     dễ quên khi soạn nhanh (buổi 08, 09 đều từng thiếu). Thiếu `py` vẫn build "thành công",
     không báo lỗi, nên phải tự rà bằng mắt trong JSON trước khi giao, không đợi học viên
     phát hiện.

**Output của giai đoạn B**: bài giảng ở dạng sẵn sàng để học — trực quan, có cấu trúc rõ, đúng định dạng học viên cần.

Nếu học viên không nói rõ muốn file gì, cứ hoàn thành cả 2 giai đoạn và trình bày trong chat trước; có thể hỏi cuối buổi "Bạn có muốn mình xuất bài giảng này ra PPTX và bài tập ra file Word để lưu lại không?"

## Bước 4 — Luyện tập

Sau phần giảng, luôn đưa bài tập/câu hỏi thực hành ngay — không chỉ giảng lý thuyết suông. Ví dụ: điền từ vào chỗ trống, dịch câu, đặt câu với từ mới, trả lời hội thoại mẫu.

Với luyện nói (HSKK) hoặc hội thoại tự do: Claude đóng vai người đối thoại bằng tiếng Trung ở mức phù hợp trình độ, để học viên phản hồi lại.

## Bước 5 — Đánh giá & Ghi nhớ tiến độ

Sau khi học viên làm bài tập:
- Chỉ ra lỗi cụ thể (chữ Hán/pinyin/nghĩa/ngữ pháp), giải thích **vì sao** sai, không chỉ nói đúng/sai.
- Nếu học viên còn sai nhiều ở điểm kiến thức mục tiêu → giải thích lại bằng cách khác (đổi ví dụ, đổi cách diễn đạt) rồi cho luyện lại, **không sang bài mới**.
- Nếu học viên làm tốt → có thể mở rộng nhẹ (1-2 từ/mẫu câu liên quan) rồi chuyển sang phần tiếp theo.

**Ghi nhớ tiến độ**: skill này dùng cơ chế Claude Memory (nếu người dùng đã bật) để giữ liên tục giữa các buổi — không có cơ chế lưu trữ riêng nào khác trong skill. Để thông tin được ghi nhớ tốt, hãy nói rõ trong lời thoại các mốc quan trọng, ví dụ: "Hôm nay chúng ta đã hoàn thành Bài 6 Quyển 1 Giáo trình Hán ngữ, học viên thích chủ đề du lịch, đã nắm được cấu trúc hỏi giá" — nói thành lời tự nhiên trong phần tổng kết cuối buổi, không cần định dạng đặc biệt. Nếu người dùng chưa bật Memory, có thể nhắc: "Nếu bạn bật tính năng Memory trong Settings, mình sẽ nhớ được tiến độ học của bạn ở lần chat sau."

## Reference files

- `references/giao-trinh-han-ngu.md` — mục lục, chủ đề, mốc ngữ pháp theo từng quyển của Giáo trình Hán ngữ 6 quyển. Đọc khi học viên theo giáo trình này hoặc khi cần xác định "bài X quyển Y" tương ứng nội dung gì.
- `references/hsk-standard-course.md` — cấu trúc, từ vựng, điểm ngữ pháp theo từng cấp HSK Standard Course. Đọc khi học viên luyện thi HSK hoặc theo giáo trình này.
- `references/interest-personalization.md` — nguyên tắc và ví dụ cụ thể về cách cá nhân hóa ví dụ/bài tập theo sở thích mà không làm lệch mục tiêu kiến thức của bài.
- `references/common-vietnamese-mistakes.md` — danh sách lỗi ngữ âm/ngữ pháp/từ vựng người Việt thường mắc khi học tiếng Trung. Đọc ở Giai đoạn A (vai Master Chinese Teacher) để dự đoán và chủ động sửa lỗi trước khi học viên mắc phải.
- `references/slide-design-best-practices.md` — nguyên tắc chia slide, giới hạn nội dung, action title, ghost-deck test, chọn loại slide phù hợp, tránh anti-pattern thiết kế — tổng hợp từ các skill/repo thiết kế slide được đánh giá cao. Đọc ở Giai đoạn B (vai Learning Experience Designer) trước khi tạo PPTX.

## Lưu ý khác

- Với chủ đề liên quan đến thay đổi định dạng thi HSK (ví dụ HSK 3.0 9 cấp) hoặc thông tin có thể đã thay đổi, hãy web-search xác nhận trước khi khẳng định với học viên.
- Không tự sáng tác "giáo trình riêng" khi học viên đã chỉ định theo Giáo trình Hán ngữ hoặc HSK Standard Course — bám đúng thứ tự bài/chủ điểm trong 2 file tham khảo trên.
- Với học viên hoàn toàn mới, luôn bắt đầu bằng phần ngữ âm/thanh điệu (pinyin) trước khi vào hội thoại, đúng như thiết kế gốc của cả hai giáo trình.
- **Bảo trì file `.skill` đã đóng gói (sửa 2026-08-06):** file này (`chinese-teaching.skill`,
  chứa chính `SKILL.md` + `references/`) từng đứng yên từ commit đầu tiên trong khi hơn
  chục commit "rút kinh nghiệm" sau đó chỉ sửa `pptx/README.md` (file rời, không nằm
  trong gói) — khiến 2 nơi trôi lệch nhau (vd quy tắc `vocab` vs `wordcard`). Từ nay: bất
  kỳ thay đổi nào vào `pptx/README.md` liên quan đến nguyên tắc sư phạm/thiết kế chung
  (không phải chi tiết vận hành script) → giải nén file `.skill`, sửa file tương ứng
  trong `references/`, rồi nén lại đè lên `chinese-teaching.skill`. Đừng chỉ sửa
  `pptx/README.md` một mình.
