# Quy tắc thiết kế — rút từ 5 vòng góp ý của user (bản demo bộ phận cơ thể, 2026-10-21)

Mỗi quy tắc kèm lỗi thật đã bị chê, để hiểu *vì sao*, không chỉ *cái gì*.

## 1. MỘT hiệu ứng highlight duy nhất cho mỗi từ
- v1–v3 chồng nhiều thứ cùng lúc (thẻ phóng to + khung phóng to giữa + mũi tên + vòng tròn +
  dòng chữ đỏ) → user: "rối", "chọn 1 phương án thôi".
- Chốt (v5): **vòng đỏ khoanh đúng chỗ trên nhân vật**. Thẻ đứng yên; chỉ chữ của thẻ đang đọc
  ngả đỏ + hiện nghĩa tiếng Việt, các thẻ khác mờ ~45%. Đổi màu chữ không tính là hiệu ứng thứ
  hai vì nó không chuyển động.

## 2. Chỉ thứ đang được nói mới chuyển động
- v2 có zoom camera, thẻ lơ lửng/nghiêng, nhân vật lắc/thở → "chóng mặt".
- Được phép: intro (tiêu đề + thẻ bật lên lần lượt, một lần), vòng đỏ đập nhẹ ±5%.
- Mọi animation qua `useCurrentFrame()` + `interpolate`/`spring` (Remotion không render CSS transition).
  Vào/ra bằng easing mềm (`Easing.bezier(0.45,0,0.55,1)`), không bật/tắt cứng.

## 3. Ảnh minh hoạ: không nền, không khung, mỗi thẻ một ảnh riêng
- v3–v4 cắt ảnh từ một chân dung rồi đặt trong khung tròn/viền trắng → "cục cục dày dày",
  "bị giới hạn khung nên nhìn không rõ", mờ khi phóng (nguồn chỉ 1024px).
- Chốt: mỗi bộ phận sinh **một ảnh riêng trên nền xanh lá #00FF00 → tách nền theo màu (PNG trong
  suốt)**, đặt thẳng lên nền poster, không viền/bóng. Nền trắng cũ để lại khung nhạt vuông ở 额头.
- Mảng da (trán, má) dễ thành "khối vuông": prompt thêm "soft rounded edges".

## 4. Không lặp hình giữa các thẻ
- v1: 头, 脸, 额头 đều là "một khuôn mặt" → "trùng lặp".
- Prompt phải làm khác biệt rõ: 头 = đầu có tóc; 脸 = khuôn mặt **trọc, không tóc, không tai**;
  额头 = mảng trán có chân tóc + lông mày. Soát contact sheet trước khi đưa user.
- Style chung KHÔNG chứa đặc điểm nhân vật ("curly hair") → nếu có, AI vẽ tóc lên mũi/tai/tay.

## 5. Bố cục thoáng như poster gốc
- v2–v3: 5 thẻ/cột sát nhau + dòng nghĩa trên mọi thẻ → "chật", "ngột ngạt hơn hình gốc".
- Chốt: 4 thẻ hàng trên / 3 trái + 3 phải nhân vật / 4 hàng dưới (cho ~14 từ), khe dọc ≥ 80px.
  Thẻ chỉ có ảnh + 汉字 + pinyin; nghĩa tiếng Việt chỉ hiện khi đang đọc.
- Không thêm thanh caption/phụ đề lặp lại thông tin đã có trên thẻ (v2 bị chê "dư thừa").
- `lint_layout.py` phải OK trước khi render.

## 6. Nhân vật trung tâm phải có việc làm
- v4 bỏ mũi tên → user hỏi "nhân vật chính giữa dùng để làm gì?". Nếu nhân vật chỉ để trang trí
  thì bỏ đi; ở template này nó là **nơi highlight** (quy tắc 1).

## 7. Chữ
- 汉字 54px đậm, pinyin 28px, nghĩa 24px; font hệ thống (Microsoft YaHei) — không để AI vẽ chữ.
- Tiêu đề 2 dòng (cam / xanh) có viền trắng, lấy từ `layout.json → title`.
- Câu mẫu/giọng đọc: khẩu ngữ, tự nhiên (xem memory feedback-sample-answer-style-colloquial).

## 8. Giọng
- TTS ViVibe giọng `cLZi…` bị user chê "dở thiệt" → ưu tiên user tự thu âm (đúng thanh điệu).
- Giọng clone từ mẫu tiếng Việt dễ đọc tiếng Trung sai thanh — báo user trước khi dùng.

## 9. Clip kể chuyện (story-clip) — rút từ góp ý của user 2026-10-27/28 (clip talk01/contagious)
- **Bảng cảnh trước, dựng sau:** liệt kê từng cảnh (đoạn phụ đề, ai ở đâu, làm gì) cho user duyệt trước khi render; user từng chê "không giống bối cảnh đã bàn".
- **Nhân vật không che nhau, không xếp 3 người ngang hàng** (chật). Chia lớp trước/sau (người ở gần camera lớn, người ở xa nhỏ vào góc) hoặc đứng 2 bên; cảnh chuyển thì thu/phóng nhân vật (`enter`) thay vì để chồng.
- **Câu dài tách theo ý:** mỗi đoạn phụ đề ≤ ~12 chữ Hán, tách ở dấu phẩy; thời lượng chia theo số chữ Hán trong 1 file giọng (`voice`).
- **Đúng cảm xúc theo tình tiết:** nhân vật chưa biết chuyện thì chưa cười (che miệng cười bằng miệng khép — `neutral`), cười sau.
- **Người đang nói chuyện/cười phải có miệng nói xen kẽ** (`chat`/`mime`), không chỉ cười + nhún. Ảnh sofa 2 người: giữ ảnh liền khối, đứng yên — tách đôi ảnh để lắc riêng làm ghế "lung lay".
- **Cảnh không thoại** (`silent` + `sec`): cho phản ứng giữa các nhân vật (nhìn nhau, nhép miệng), không cần file giọng, không phụ đề.
- Muốn tay/đầu cử động thật cần **tấm tư thế riêng do user cung cấp** rồi luân phiên (`swap`) — xem gotchas.


- **Lời thoại khớp nhân vật:** chỉ người đang có lời mới mấp máy miệng; người nghe **ngậm miệng** (user sửa 4 lần, talk02). Một đoạn video chung cho 2 lượt thoại thì không khớp được → tách đoạn theo lượt nói.
- **Khung 0 = ảnh xem trước:** cảnh đầu không mờ dần, phải thấy đủ nhân vật + chủ đề (vd nhãn phe 🏫 去学校 / 🏠 在家上学). Khung trắng/nhân vật bị cắt → người ta lướt qua.
- **Nhún theo giọng rất nhẹ** (~4px): 16px bị chê "nhảy nhảy, nhức mắt".
- **Góc nhìn nhất quán:** ảnh nhìn từ trên xuống (giường top-down) đặt trên nền sàn top-down, không đặt lên tường nhìn ngang ("giường dựng đứng").
- **Cảnh 2 người cần chữ/biểu tượng ở tâm** (VS, tia sét) → nền **1 màu**; nền chia 2 màu trong video AI bị xê dịch làm mọi thứ trông lệch. Tia sét vẽ SVG (emoji lệch tâm).
- Nhãn phe đi theo nhân vật đang có mặt (`scene.who`, chữ trong `story.json "tags"`); 2 nhãn đối xứng, VS nằm trong khe giữa, không đè lên nhãn.

## 10. Âm thanh clip (rút từ góp ý 2026-10-28, clip talk01/contagious)
- **Nhạc nền nhẹ + hiệu ứng theo ngữ cảnh** (chỉ giọng thì "đơn điệu"): `make_bed.py` dựng 1 file `bed.wav` = nhạc (tự hạ còn ~50% khi có giọng, fade vào/ra) + hiệu ứng đặt theo mốc cảnh. Giọng vẫn là `<Audio>` riêng.
- **Hiệu ứng phải là âm thật** (Mixkit / Freesound CC0 — xem gotchas), không tổng hợp bằng code.
- **Tiếng cười nữ trẻ: kiểu khúc khích, líu lo** (Freesound 218308 "Girl, female, laughing, giggling", cắt từng tràng ngắn). Cười to/kéo dài kiểu "hilarious/cheerful" bị chê "đáng sợ".
- **Bỏ âm "đáng sợ"**: cửa cọt kẹt, tra chìa khoá, tiếng đường phố mở đầu → chỉ giữ bước chân đi trong nhà cho cảnh về nhà.
- Nhạc nền: đưa **3–5 đoạn ứng viên 25s** cho user nghe chọn, đừng đoán nhiều lần. Đã chốt: clip kể chuyện "Happy Home" (Mixkit 801), video 朗读 "A Happy Child" (Mixkit 532). Piano chậm / "Smile" bị chê buồn hoặc "không ăn nhập".

- **Giọng mẫu TTS cho clip 2 nhân vật** (khi chưa thu giọng thật): 瑾玄 = Edge `zh-CN-XiaoyiNeural`, 越黄 = `zh-CN-YunxiaNeural`, giữ nguyên tông — nâng `--pitch` cho "trẻ hơn" bị chê "ép, không tự nhiên". Từ khó nghe rõ thì thêm dấu phẩy trước + đọc chậm câu đó (-5%) (孤单 talk02).

## 11. Thương hiệu, chống copy, đoạn kết — MỌI video Talk series
- **Chống copy:** nhãn đỏ nền trắng `禁止搬运` (góc trên phải) + tên kênh `@瑾玄在练嘴` + 1 dấu chìm nhỏ mờ đổi chỗ mỗi 6s ở mép dưới (không đè phụ đề/tên kênh). **Không** dùng watermark chéo phủ kín màn hình (user: "gây rối").
- **Đoạn kết** = `Outro.tsx` (template/shared): thẻ hồ sơ (avatar 瑾玄 + tên kênh) → bàn tay chạm nút đỏ **"Follow"** → xám **"✓ Followed"** + tiếng tick → tim bật lên + pop. Câu thoại **luôn bằng giọng 瑾玄** (LucyLab "Huyền Babe", xem `nhan-vat/README.md`): `谢谢大家的观看～喜欢的话，记得点赞、关注我哦！` (video đọc: 收听).
- **Chữ nhiều dòng rớt dòng theo ý** (sau ～。！？), mỗi dòng `nowrap` — "cùng câu mà rớt 1 chữ nó kỳ". Cỡ chữ câu kết ~46px (60 bị chê to).
- **Chỉ giữ 1 bản final** mỗi video: render đè đúng tên `video/<slug>.mp4`; xoá bản nháp, ảnh nhân vật không chọn, giọng/nhạc thử trước khi commit (user: "không cần lưu nhiều rối").

## 12. Video 朗读 (template/read-along) — bố cục user chốt 2026-10-28 (talk01/langdu)
- Bài đọc = `p2Text` của bài trong `onluyen/on-luyen.html`, **giữ nguyên chữ + dấu câu** (chỉ đổi `"` → `“ ”` cho vừa ô). Tiêu đề = **tên bài 口语** (vd 快乐会传染), không ghi nguồn sách.
- **1 dòng tiêu đề** `朗读 | <tên bài>` (朗读 đen có vệt xanh, tên bài xanh lá); bài đọc ngay dưới, căn trái, 21 chữ/dòng, dấu câu không đứng đầu dòng.
- **Nền kem trơn** — không kẻ ô, không dòng kẻ mờ dưới chữ ("khó coi"). Chỉ có **vạch xanh tiến độ mảnh 3px** chạy dưới phần đã đọc.
- Từ khoá tô đỏ = từ H6 trong `raw/Từ vựng.xlsx` + thành ngữ hay (~14 mục); thẻ góc phải dưới "重点词": 汉字 + pinyin + nghĩa. **Xuất 2 bản: EN và VI** (`Read` / `ReadVI`). Nghĩa phải theo ngữ cảnh câu, không thay bằng tục ngữ tiếng Anh na ná.
- Chữ ký `—— @瑾玄在练嘴` ngay dưới dòng cuối bài; thẻ từ ngay dưới chữ ký.
- **Nhân vật** (luân phiên theo bài — bài 1: 越黄) mặc đồng phục kiểu trường phù thuỷ (áo choàng đen lót đỏ, cà vạt sọc — không huy hiệu/logo thật), **nhìn thẳng**, cầm sách ngang hông, **to (~670px)** góc trái dưới, không đè chữ.
- **Giọng:** Edge TTS theo giới tính nhân vật — nam `zh-CN-YunxiNeural`, nữ `zh-CN-XiaoxiaoNeural` (giọng thanh thiếu niên). Giọng clone "Huyền Babe" bị chê "lơ lớ, chưa tròn âm" cho bài đọc dài. **Đọc từng câu** (tách ở 。！？；：), tốc độ **-5%**, nghỉ thêm 0.2s sau 。 / 0.08s sau ；：. Đọc liền cả bài → đoạn đầu nhanh, nối chữ; tách vụn ở —— / trích dẫn → câu đầu chậm, đứt nhịp; -30% → quá chậm.
- **15s chuẩn bị** trước khi đọc (user chốt 2026-11-01, talk02): bài đọc + nhân vật hiện sẵn; ô thẻ 重点词 (lúc đầu trống) hiện `准备时间` + số xanh **15→4** + thanh thời gian, rồi **3·2·1 đỏ** kèm 3 tiếng *ting* (không đọc số, không làm mờ bài đọc) → bắt đầu đọc. Không cần cảnh mở đầu AI.
- Nhạc nền 0.09 lúc chuẩn bị/đoạn kết, **hạ còn ~1/3 trong lúc đọc**.
- Từ khoá đọc sát nhau (cách < 1s, thẻ chớp qua không kịp nhìn): khai `data.json "groups"` → cả cụm hiện sớm 1,5s thành danh sách, **Focus** từ đang đọc (to + rõ), từ khác nhỏ + mờ. Chỉ áp cho cụm khai báo; từ đơn lẻ giữ thẻ to theo giọng.
- Nhân vật mặc đồng phục kiểu Harry Potter **không cần kính râm** (user bỏ, talk02).

## 13. Video HSKK 高级 回答问题 (template/hskk-answer) — chốt với user 2026-11-02 (talk01 · 快乐会传染 · câu 5)
- **Bố cục 4 cảnh:** (1) câu hỏi giữa khung, KHÔNG ghi "câu 5/6", tên chủ đề nhỏ chân trang mọi cảnh; (2) mindmap CHỈ tiếng Trung (mở bài → thân 1 → thân 2 → kết: luận điểm + ví dụ), không dịch; (3) cụm đáng học: chỉ cụm khó + ngắn, pinyin chỉ khi khó đọc; (4) clip minh hoạ + phụ đề kiểu phim (≤ 2 câu, Hán trên/dịch dưới, mỗi câu 1 dòng, ngắt ở dấu phẩy, KHÔNG thẻ mở/thân/kết) + thẻ 重点词 bật đúng lúc. Rồi 现在开始 → đọc → kết follow.
- **Nguồn nội dung:** `onluyen/bai-mau-cau5-6.md` của user, không tự soạn bài mẫu. Thứ tự làm: chủ đề 1 (c5, c6) → chủ đề 2 (c5, c6) → … để user kiểm soát tiến độ.
- **Âm thanh:** nhạc nền chạy SUỐT toàn video (nhỏ, hạ khi có giọng); TẮT hẳn âm gốc clip muse-video (user không cần tiếng cười nói); giọng Edge `zh-CN-YunxiaNeural` +8% +4Hz (Yunxi -5% bị chê "mệt, hơi xuống").
- **Phân cảnh:** user chê "ít cảnh, lặp, chán" → ≥ 1 hoạt động/cảnh MỚI mỗi ~5 giây (nói chuyện, học miệt mài hết đề này tới đề khác, đi bộ cùng nhau, ăn lẩu, động viên bạn…), ~14 cảnh cho 74s giọng. Đổi bối cảnh + trang phục so với các video trước ("gen lại thấy chán"). Nền tối giản (user chê nhà "quá nhiều chi tiết"), cửa phải nằm trên tường hợp lý.
- **Hành động tự nhiên:** đã ở trong nhà thì chỉ ĐI BỘ tới (tay buông đánh nhẹ), tới sát mới giơ tay ôm — không chạy, không giơ tay sẵn từ xa; hướng đi phải quay về phía người nhận (soát bằng khung tĩnh); cả nhà cười nói rôm rả ngồi thẳng, KHÔNG nghiêng qua nghiêng lại; mỗi người đúng 1 ly; nhân vật chính (越黄) cùng cỡ thân với người khác, đứng giữa nhóm khi cụng ly; nét "ngơ ngác" = mắt mở to, chân mày nhướn, gãi đầu — nhắm mắt/méo miệng bị đọc thành giận; cảnh ôm kết bằng push-in từ từ tới cận cảnh (ôm sát che nhau, khó giữ rõ hình).
- **Khung tĩnh (chốt 2026-11-03, chủ đề 2):** vẽ nguyên cảnh bằng model ảnh, KHÔNG cắt/lót clip dọc từ video khác vào khung ngang (user chê "mờ, nhỏ"). 越黄 CÙNG CỠ với các bạn (user bắt sửa), chỉ 1 越黄/hình. Đồ ở nhà phải mới mẻ, vẫn có món đỏ (áo thun đỏ + quần short be bị chê "nhàm chán"). Bàn ghế lớp học xếp thẳng hàng. Cảnh lập trình: MacBook bạc + thêm 1 màn hình rời cho "chuyên nghiệp".
- **Checklist soát khung/clip TRƯỚC khi đưa user duyệt** (user bắt lại 2026-11-03, "đã sửa nhiều lần ở các video khác"): (a) viết/vẽ → bút ở **tay phải** suốt clip (khung: "RIGHT hand holds the marker, LEFT hand with the watch hangs relaxed"; motion: "the marker NEVER changes hands"); (b) 越黄 không to hơn bạn, không chiếm gần hết khung khi cảnh cần thấy bối cảnh (cổng trường…) — đặt mô tả CẢNH trước mô tả nhân vật trong prompt thì model chịu vẽ nhỏ; (c) đồ vật đúng chỗ, không dính người/lơ lửng (tập nằm trên bàn), không trùng (mũ tốt nghiệp đội trên đầu thì tay trống, 1 người 1 mũ); (d) cảnh di chuyển phải thấy rõ ĐÍCH (đi học → cổng trường + cờ + bạn đang vào, nhà ở phía sau); (e) cảnh giảng hoà kết vui rõ ràng (ôm nhau, người xung quanh giơ like); (f) khung 0 có câu hỏi + nhân vật (S1 không fade-in).
- **Trang phục/nhân vật:** nhà ấm theo mùa; mẹ trang nhã (không lòe loẹt), ba KHÔNG lố, mặt bố mẹ phải HIỀN (bản đầu "hơi ác"). Xem `nhan-vat/README.md`.
- **Chốt thêm 2026-11-03 (talk01 · câu 6 · 分享快乐, nhân vật 瑾玄):** khung ghép bằng code (nhân vật tách nền dán lên nền khối màu) bị chê "kỳ kỳ, không linh hoạt", nhà như cái hộp → luôn vẽ NGUYÊN CẢNH bằng model ảnh `--size 1536x1024`, soát từng ảnh trước khi gen clip.
- **Màu:** tông sáng, nhẹ (trắng ngà, xanh sage, xanh trời nhạt, gỗ sáng); tông thu cam-nâu bị chê "hơi nóng". **Ngôi sao/lấp lánh** (thay trái tim): tối đa 1-2 sao nhỏ mỗi cảnh, 3-4 ở cảnh cao trào; prompt muse-video ghi rõ KHÔNG thêm sao/lấp lánh/chói (bản nhiều sao bị chê, clip tự tung sao che mặt).
- **Hợp bối cảnh:** ở công ty không reo to — ôm điện thoại rón rén ra ngoài gọi; người gọi về nhà → ba mẹ đang nấu ăn trong bếp thì điện thoại reo; tin lan họ hàng = bong bóng tin nhắn bay tới avatar cô chú; khoe con = khung ảnh NHỎ treo tường, ba mẹ cười híp mắt, ba khoác vai mẹ (KHÔNG cầm khung ảnh to — trông như ảnh thờ); ăn mừng bàn ăn = mọi người ngồi GHẾ phía sau bàn (không ai ngồi lên bàn, không mất chân); đăng bài = tối ngồi trên giường, đồng nghiệp bình luận hiện quanh điện thoại.
- **Khung chữ:** khung ĐẦU TIÊN phải có câu hỏi (không fade-in từ trắng — ảnh bìa trắng bị lướt qua); không đầu người ló ở mép khung video S4; phụ đề ≤ 15 chữ Hán/dòng.
- **Chốt thêm 2026-11-03 (talk02 · câu 6 · 在家上学, bố mẹ 瑾玄 + 越黄 + con trai ~7t):**
  - **Đưa / nhờ vật** (con đưa bài tập cho mẹ…): người đưa phải QUAY CẢ MẶT LẪN THÂN về phía người nhận. Ghi trong prompt ảnh lẫn prompt clip là "his whole body and face turned TOWARD HER (side view, facing her, not facing the viewer)", rồi soát bằng khung tĩnh. Nếu người đưa quay ra phía người xem, user sẽ bắt sửa.
  - **Cảnh "nhiều việc cùng lúc":** tách khu vực rõ ràng (bàn làm việc RIÊNG ↔ bếp, KHÔNG đặt laptop sát bếp), và chia 2 clip cho 2 dòng phụ đề liền nhau. Clip 1: ngồi họp, nồi phía sau bắt đầu trào. Clip 2: chạy ra đeo găng nhấc nồi sôi trào, laptop vẫn đang họp, điện thoại reo. Người làm phiền (con) bám theo suốt. Mặt nhân vật phải nhăn, lo lắng; prompt ghi rõ "NOT smiling", vì model hay vẽ cười.
  - Cảnh 2 vợ chồng đọc chung tài liệu, xem chung điện thoại → nhân vật "cùng cặp", không để 瑾玄 một mình (user: "cô đơn").
- **Đồ vật thật:** laptop của 瑾玄 = MacBook Pro bạc (logo táo nhỏ ở lưng nắp, màn hình quay về phía cô); model hay vẽ màn hình quay ra người xem → ghi rõ "back lid facing the viewer, screen toward her".
- **Quy trình VI/EN (user chỉnh 2026-11-03):** làm xong HẲN bản VI → user xem + chốt → MỚI render EN theo bản VI đã chốt (không chạy chuỗi VI rồi EN tự động). Bản EN cũ còn trên đĩa là bản cũ, phải làm lại sau khi VI chốt.
- **Phụ đề cụm đáng học đồng nhất:** hoặc mọi cụm đều có pinyin hoặc không cụm nào (user chê "chỗ có chỗ không") — mặc định thêm pinyin cho cả danh sách.
- **Hành động hợp ngữ cảnh:** cảnh công sở (nhận email thăng chức) → vui THẦM (mắt long lanh, nụ cười nhỏ, thân người đứng yên), không cười lớn/nhún/giơ nắm đấm; gọi điện → đứng yên, điện thoại áp tai, gật đầu + 1 cử chỉ tay, không nhảy/nhún (điện thoại dính tai mà nhảy là vô lý).
- **Chốt thêm 2026-11-04 (talk03 · câu 5 · 活人图书馆, 越黄 + chàng trai xăm tay cựu lính cứu hoả):**
  - **CHỐT HƯỚNG DI CHUYỂN** (user bắt lỗi sai hướng ở gần như mọi clip: đi chéo ra người xem, bà cụ đi ngược chiều xe đẩy, 2 người bưng đồ đứng đối mặt): prompt khung tĩnh VÀ prompt muse-video của cảnh có người đi/đẩy/bưng phải mở đầu bằng `DIRECTION: everyone … move toward the LEFT/RIGHT`, ghi thân + mặt từng người quay đâu ("strict side profile facing LEFT"), người đi trước muốn nhìn người sau thì "turns only her HEAD back". Soát mục HƯỚNG riêng ở khung tĩnh và clip trước khi đưa user.
  - **Cảnh có diễn biến tách 2 khung/clip** (chờ thang máy → cửa mở thấy người lạ → vẫy tay không đi): 1 clip không tự diễn đủ các nhịp. Cảnh "chờ" có thể chiếu lúc 现在开始 (dòng 0 trong `CLIPS`).
  - **Nhân vật phụ = 1 khối FACE cố định** (tóc, mày, hàm, không râu…) dùng cho MỌI cảnh kể cả hồi tưởng/đổi trang phục — tả riêng từng cảnh thì mặt/tóc đổi, user không nhận ra người lính cứu hoả chính là chàng trai → mất cú lật. Model vẽ vết sẹo/hình xăm sai tay → lật ngang cả ảnh (Pillow) thay vì vẽ đè.
  - **Video phải có ý nghĩa, không minh hoạ rời từng câu:** kể 1 mạch truyện (định kiến → gặp → nghe chuyện thật → thay đổi), cảnh đầu và cảnh kết đối xứng; mỗi cảnh ≥ ~3s (dòng quá ngắn thì gộp dòng, bỏ cảnh phụ); KHÔNG tua nhanh clip (tốc độ ≤ 1.0 — tua 1.6× bị chê vội, mất cảm xúc). Hồi tưởng phải nhận ra được: đẩy cận vật nối (hình xăm) → loé trắng → sepia + viền tối; ra khỏi hồi tưởng loé trắng lần nữa. Cảnh "kết quả" (giúp bà cụ đẩy xe hàng, bưng đồ giúp người lạ) chiếu KHÔNG lời sau khi đọc xong (dòng ảo `VIRT`).
  - Nhân vật chính không được trông "hèn": định kiến thể hiện bằng cử chỉ nhỏ (liếc, khựng lại, lịch sự từ chối), không co rúm/nép tường.
