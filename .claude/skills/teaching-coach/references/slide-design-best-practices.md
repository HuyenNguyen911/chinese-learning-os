# Nguyên tắc thiết kế slide bài giảng (tổng hợp từ các repo uy tín)

File này bổ sung cho quy tắc thiết kế đã có trong `/mnt/skills/public/pptx/SKILL.md` (bảng màu, font an toàn, QA...). Dùng ở **Giai đoạn B (Learning Experience Designer)** khi quyết định cách chia slide và trình bày. Các nguyên tắc dưới đây được tổng hợp và điều chỉnh cho ngữ cảnh dạy ngôn ngữ từ các skill/repo thiết kế slide được đánh giá cao: `proyecto26/slides-ai-plugin`, `Gabberflast/academic-pptx-skill`, `zarazhangrui/frontend-slides`, `MiniMax-AI/skills` (pptx-generator).

## 1. Một slide — một ý (One idea per slide)
Mỗi slide chỉ truyền tải **một** đơn vị kiến thức: một điểm ngữ pháp, một nhóm từ vựng, một đoạn hội thoại, một bài tập. Không dồn "từ vựng + ngữ pháp + ví dụ" vào cùng 1 slide nếu chúng đủ lớn để tách riêng.

## 2. Tiêu đề slide phải là "action title", không phải nhãn chủ đề
Thay vì tiêu đề chung như "Ngữ pháp" hay "Từ vựng bài 6", hãy đặt tiêu đề nêu rõ **điểm chính học viên cần nhớ**:
- Yếu: "Ngữ pháp: 了"
- Tốt: "了 đánh dấu hành động đã hoàn thành — không phải thời quá khứ"

**Ghost-deck test**: đọc lướt qua tất cả tiêu đề slide theo thứ tự (bỏ qua phần nội dung bên dưới) — nếu chuỗi tiêu đề đó tự kể lại được toàn bộ mạch bài học, tiêu đề đã đạt. Nếu không, tiêu đề đang quá chung.

## 3. Giới hạn nội dung theo loại slide (Content Density Limits)
Không nhồi chữ — vượt giới hạn thì tách slide, không giảm cỡ chữ để nhồi thêm (chữ chính tối thiểu ~18pt trên slide chiếu, theo `proyecto26/slides-ai-plugin`).

| Loại slide (áp dụng cho bài giảng tiếng Trung) | Giới hạn nội dung tối đa |
|---|---|
| Tiêu đề bài học | 1 heading + 1 subtitle (số bài/chủ đề) |
| Từ vựng mới | Tối đa 6-8 từ/slide (chữ Hán + pinyin + nghĩa); nhiều hơn → chia "Từ vựng 1/2" |
| Bài khóa/hội thoại mẫu | 1 đoạn hội thoại ngắn (≤ 6-8 lượt lời), trình bày dạng khung chat, không dán nguyên trang sách |
| Điểm ngữ pháp | 1 cấu trúc + 2-3 ví dụ minh họa, không nhồi nhiều điểm ngữ pháp khác nhau cùng slide |
| Bảng so sánh (ví dụ 了 vs 过) | 1 heading + 2 cột, mỗi cột 3-4 dòng |
| Lỗi thường gặp | 1 lỗi/slide: câu sai → câu đúng → giải thích ngắn |
| Timeline mốc ngữ pháp/lộ trình | Tối đa 5 mốc |
| Bài tập luyện tập | 1 dạng bài tập/slide (không trộn điền từ + trắc nghiệm cùng slide) |
| Tổng kết cuối buổi | 3-5 gạch đầu dòng "hôm nay đã học" |

## 3b. Sắp xếp 生词 theo NHÓM NGHĨA, không cứng theo thứ tự khối trong sách (2026-09-09)

Sách thường liệt kê 生词 theo thứ tự khối xuất hiện trong 课文 (X-2, X-4, X-6…) — đúng
với mạch đọc hiểu bài khóa, nhưng KHÔNG phải thứ tự tối ưu để dạy/ôn từ vựng. Trước khi
soạn slide từ vựng, thử nhóm lại các từ theo chủ đề/chức năng ngữ dụng (vd: cụm xưng hô
đi chung, cụm chào hỏi đi chung, cụm cảm ơn-đáp lễ đi chung, cụm xin lỗi-đáp lễ đi
chung…) — giúp học viên thấy được các từ liên quan nhau ngay khi học, dễ nhớ theo nhóm
hơn là nhớ rời rạc theo thứ tự xuất hiện trong sách. Khi đổi thứ tự, vẫn giữ đủ 课文
nguyên văn theo đúng trình tự gốc của sách (chỉ đổi thứ tự phần 生词, không đổi 课文).

## 4. Cấu trúc mạch bài học như một lập luận (không phải tập hợp slide rời rạc)
Vận dụng ý tưởng "situation → complication → resolution" (từ `academic-pptx-skill`) vào bài giảng ngôn ngữ: **tình huống có thật (hội thoại/nhu cầu giao tiếp) → vướng mắc (điểm ngữ pháp/từ vựng chưa biết cách diễn đạt) → giải quyết (dạy cấu trúc mới) → áp dụng lại vào tình huống ban đầu**. Tránh liệt kê ngữ pháp khô khan không có bối cảnh dẫn nhập.

## 5. Chọn đúng "loại slide" cho đúng loại nội dung
Tham khảo bảng loại slide chuẩn (điều chỉnh cho bài giảng ngôn ngữ):

| Nội dung cần trình bày | Loại slide phù hợp |
|---|---|
| Từ vựng mới có hình ảnh minh họa được (danh từ cụ thể) | Slide hình ảnh + chữ Hán/pinyin/nghĩa |
| Hội thoại mẫu | Khung chat/speech-bubble, không phải bullet list |
| So sánh 2 cấu trúc ngữ pháp dễ nhầm | Bảng so sánh 2 cột |
| Trình tự các mốc ngữ pháp/bài học đã qua | Timeline |
| Quy tắc ngữ pháp trừu tượng (thứ tự từ trong câu) | Sơ đồ khối câu (S + trạng ngữ + V + O) hơn là chữ thuần |
| Lỗi sai thường gặp | Slide 2 phần: ❌ câu sai — ✅ câu đúng, có highlight màu ở phần khác biệt |
| Tổng kết/mở rộng | Feature-grid (thẻ nhỏ, tối đa 6 thẻ) |

**Điểm ngữ pháp có ≥3 quy tắc con khác nhau (2026-08-07, rút ra khi làm 时量补语 HSK2
Buổi 9):** đừng nhồi hết vào 1 slide `grammar` + 1 `note` dài — chữ tự co nhỏ, khó đọc,
học viên không tách được quy tắc nào ứng với ví dụ nào. Tách thành: 1 slide `grammar`
cho cấu trúc chính + 1 slide `table` riêng liệt kê từng trường hợp con (cột "Trường hợp"
| cột "Ví dụ") — nhìn vào bảng là thấy ngay có mấy trường hợp, không cần đọc hết văn
xuôi mới hiểu.

## 5b. Đừng chỉ chọn giữa "bảng" và "chữ" — cân nhắc cả minigame (2026-09)

Ngoài các loại slide tĩnh (bảng, thẻ, ảnh+chữ), renderer có 2 loại slide
**minigame** (mỗi block JSON tự sinh 2 slide: đố → đáp án) giúp bài giảng đỡ
đơn điệu khi lặp lại nhiều buổi:

| Nội dung | Minigame phù hợp | Vì sao |
|---|---|---|
| Từ vựng cụ thể có ảnh minh hoạ rõ (đồ vật, hoạt động) | `guess` — đoán từ qua ảnh | Buộc học viên chủ động nhớ lại trước khi được cho đáp án, thay vì chỉ nhìn ảnh+chữ cùng lúc như `wordcard` |
| Ôn tập 1 nhóm từ đã dạy (đầu buổi sau hoặc cuối buổi) | `match` — ghép cặp xáo trộn | Liệt kê bằng `bullets` là hình thức ôn tập yếu nhất (chỉ đọc lại thụ động); ghép cặp buộc nhớ lại chủ động (active recall) |
| Ôn tập có ảnh, GV tự chấm/hỏi đáp trực tiếp trên lớp | `match_pairs` — nối ảnh-số với từ, 1 slide, KHÔNG tự sinh đáp án | `guess`/`match` luôn tự sinh thêm 1 slide đáp án — thừa và không cần thiết khi GV đã kiểm tra miệng ngay tại lớp |

Không dùng 2 minigame `guess`/`match` cho từ trừu tượng/hư từ (không có ảnh minh hoạ
được, và ghép cặp với khái niệm ngữ pháp dễ gây nhầm lẫn hơn là giúp nhớ) — giữ
`vocab`/`grammar`/`table` cho các trường hợp đó. Xem schema đầy đủ (`items`,
`seed`, giới hạn số cặp) trong `pptx/README.md`.

## 6. Chế độ mật độ nội dung: chọn "low-density / speaker-led" cho bài giảng trực tiếp
Theo phân loại của `zarazhangrui/frontend-slides`: bài giảng dùng để **Claude giảng trực tiếp cùng học viên** (không phải tài liệu tự đọc async) nên ưu tiên **low-density / speaker-led** — heading lớn, cụm từ ngắn, nhiều khoảng trắng, để Claude giải thích thêm bằng lời trong chat/slide notes. Chỉ chuyển sang **high-density / reading-first** (bảng chi tiết, chú thích đầy đủ) khi học viên xin tài liệu tự ôn tập không có người giảng kèm.

## 7. Tránh các lỗi thiết kế phổ biến (Anti-patterns)
- **Font soup**: quá 2 font (1 heading + 1 body) — xem danh sách font an toàn trong `/mnt/skills/public/pptx/SKILL.md`.
- **Color rainbow**: quá 3 màu — áp dụng quy tắc 60-30-10 (màu chủ đạo 60-70%, phụ 1-2 tông, nhấn 1 tông).
- **Wall of text**: không dán nguyên đoạn văn từ giáo trình — chắt lọc thành từ khóa/cụm ngắn.
- **Clip art syndrome**: mỗi hình ảnh phải có lý do rõ ràng (minh họa từ vựng cụ thể, không trang trí vô nghĩa).
- **AI slop aesthetics**: tránh gradient tím mặc định, font Inter/Roboto ở mọi nơi, layout card rập khuôn — mỗi bài giảng nên có màu sắc phù hợp chủ đề bài học đó (ví dụ bài về ẩm thực dùng tông màu ấm, bài về thời tiết dùng tông xanh...).
- **Transition carnival**: nếu dùng animation/transition, chỉ 1 kiểu xuyên suốt, không đổi liên tục.

## 8. Kiểm tra trước khi hoàn thiện (rút gọn từ quy trình QA trong pptx skill)
Sau khi tạo file, đọc lại toàn bộ tiêu đề slide theo thứ tự (ghost-deck test ở mục 2), kiểm tra không có slide nào vượt giới hạn nội dung ở mục 3, và không slide nào chỉ có chữ không có yếu tố trực quan nào.

**Tự soát bằng ảnh (bắt buộc khi có PowerPoint):** xuất từng slide ra PNG (PowerPoint COM `Slide.Export`) rồi ghép contact-sheet để nhìn tổng thể trước khi giao — bắt lỗi bố cục/canh lề/ảnh sai mà đọc XML không thấy.

## 9. Nguyên tắc trình bày (bổ sung từ phản hồi dạy thực tế)

Đây là các quy tắc rút ra sau khi dùng slide thật trên lớp. `build_deck.py` đã enforce sẵn phần cấu trúc; phần biên tập (giọng văn, tiêu đề, chọn câu) do người soạn JSON tuân thủ.

- **Giọng văn thân thiện nhưng KHÔNG "sến"**: hạn chế dấu chấm than và câu cảm thán kiểu "Cùng khoe nhé!", "做得好!". Ưu tiên câu ngắn, khích lệ nhẹ nhàng, tự nhiên ("Mục tiêu hôm nay", "Nhắc lại buổi trước").
- **Tiêu đề slide chỉ 1 ngôn ngữ**: KHÔNG trộn tiếng Trung + tiếng Việt trong cùng dòng tiêu đề. Slide dạy 1 chữ/điểm tiếng Trung → tiêu đề là chữ đó (kèm pinyin), nghĩa tiếng Việt đưa xuống phần `point`/nội dung. Nhãn phân loại ở tab (kicker) dùng chữ Hán (生词/语法/对比/会话/阅读/应用/作业) — nằm ở tab riêng nên không tính là trộn.
- **Từ vựng — chọn `vocab` (bảng) hay `wordcard`/`word_pair` (1-2 từ/slide) (sửa 2026-08-06):**
  quy tắc gốc ở đây từng chỉ nói dùng `vocab` (bảng 3 cột 汉字|Pinyin|Nghĩa) — viết ra
  TRƯỚC KHI `wordcard`/`word_pair` tồn tại trong renderer, chưa từng đối chiếu lại sau đó.
  Thực tế sản xuất (Buổi 8, 9) chốt dùng `wordcard` (1 từ/slide, đào sâu + ảnh + ví dụ
  riêng) hoặc `word_pair` (2 từ liên quan/slide, khi cần nén gọn số lượng lớn) cho **生词
  dạy mới trong 1 buổi** — không dùng bảng dồn nhiều từ nữa. `vocab` (bảng) vẫn hợp lệ,
  chỉ dùng cho liệt kê nhanh không cần ảnh/ví dụ riêng (bảng tổng kết, bảng đối chiếu).
  **Thêm chế độ THẺ cho `vocab` (2026-08-07, Buổi 10):** khi 2-3 từ ghép chung
  được 1 câu ví dụ tự nhiên (khác `word_pair` — mỗi từ ảnh/ví dụ RIÊNG, không hợp
  khi 2 từ không liên quan nhau), gắn `image`/`example` **cấp SLIDE** vào `vocab`
  → renderer tự chuyển sang layout thẻ: ảnh to 1 bên + câu ví dụ nổi bật (tự tô đỏ
  đúng các từ trong `items[].hz` xuất hiện trong câu, không cần khai `highlight`
  tay) + danh sách thẻ từ (không bảng) canh giữa bên còn lại. Gọn hơn hẳn bảng cũ
  khi chỉ có 1-3 từ, không tốn diện tích như bảng full-width.
- **`passage` (课文 tự sự) ưu tiên 1 cột full-width (2026-08-07):** layout chia cột
  trái/phải cũ (ảnh 1 bên, câu văn cột hẹp bên kia) khiến câu dài phải wrap nhiều
  dòng trong cột hẹp, nhìn như bị xé thành nhiều cột — ảnh (nếu có) nên đặt dải
  TRÊN full-width, câu văn xuống 1 cột rộng full-width bên dưới, đánh số ①②③ đầu
  mỗi câu để tách bạch.
- **口语 (khẩu ngữ tự nhiên, cuối buổi) dùng `type: "grammar"` thay vì `table`:**
  tái dùng đúng layout "ảnh 1 bên + danh sách cụm câu (Hán tự đậm + pinyin cùng
  dòng, nghĩa xuống dòng, giãn cách rộng)" đã ổn định — không cần `point`, chỉ cần
  `image` + `examples[]` là các câu khẩu ngữ, tránh trùng nội dung đã dạy ở 生词/语法.
- **Giọng trẻ con (dialogue audio):** 4 giọng nam/nữ hay dùng mặc định
  (Xiaoxiao/Xiaoyi/Yunxi/Yunyang/Yunjian) đều là giọng NGƯỜI LỚN — dùng riêng
  `zh-CN-YunxiaNeural` ("Cartoon, Cute", có trên edge-tts) cho nhân vật trẻ em.
  Nhân vật lặp lại ở nhiều 课文 trong cùng 1 buổi phải liệt kê hết TRƯỚC khi gán
  giọng, tránh 2 nhân vật khác nhau vô tình trùng giọng.
- **Thứ tự khối trong 1 buổi (chốt theo Buổi 8):** Title → 目标 → toàn bộ 生词 (chính rồi
  đến mở rộng, theo thứ tự xuất hiện trong 课文) → 课文/hội thoại (đúng thứ tự sách) →
  语法 (đúng thứ tự sách) → luyện tập. Dạy hết từ mới TRƯỚC khi học viên gặp trong bài,
  không xen kẽ theo đúng thứ tự sách gốc (bài học rút ra khi làm Buổi 9: xen kẽ theo thứ
  tự sách gốc bị coi là sai).
- **汉字 và pinyin canh thẳng hàng**: trong khung hội thoại/thẻ, chữ Hán và pinyin cùng canh trái, không lệch nhau.
- **Lấp đầy slide, tránh dồn chữ 1 góc**: nội dung canh giữa theo chiều dọc, cỡ chữ đủ lớn, bảng trải đều chiều cao — không để nửa dưới trống trơn.
- **Câu giao tiếp**: (a) ưu tiên câu bám sát nội dung bài hôm đó; (b) KHÔNG hiển thị cột mã ID cho học viên — ID chỉ dùng nội bộ để tracking (file conversation-bank).
- **Thêm mẹo ghi nhớ**: ở điểm ngữ pháp/dễ nhầm, thêm key `tip` (render "🔑 Mẹo ghi nhớ: …") giúp học viên liên tưởng, nhớ có hệ thống.
- **Bài tập về nhà**: làm bằng công cụ/skill riêng; trong slide bài giảng chỉ để 1 slide `blank` có placeholder.

### Ảnh minh hoạ
- Dùng `fetch_images.py` để tải ảnh Creative Commons (Openverse) theo nội dung; ghi nguồn ở `credits.json`.
- **Ưu tiên ảnh mô tả đúng nội dung** (vd 我会说汉语 → ảnh người đang đọc/nói tiếng Trung), **hạn chế emoji**.
- Tránh ảnh mang sắc thái tiêu cực (vd học sinh mệt mỏi ôm đầu) — chọn ảnh tích cực, đúng tinh thần khích lệ.
