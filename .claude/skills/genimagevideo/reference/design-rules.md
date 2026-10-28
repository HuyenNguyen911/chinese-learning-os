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

## 9. Clip kể chuyện (story-clip) — rút từ góp ý của user 2026-10-27/28 (clip talk01-contagious)
- **Bảng cảnh trước, dựng sau:** liệt kê từng cảnh (đoạn phụ đề, ai ở đâu, làm gì) cho user duyệt trước khi render; user từng chê "không giống bối cảnh đã bàn".
- **Nhân vật không che nhau, không xếp 3 người ngang hàng** (chật). Chia lớp trước/sau (người ở gần camera lớn, người ở xa nhỏ vào góc) hoặc đứng 2 bên; cảnh chuyển thì thu/phóng nhân vật (`enter`) thay vì để chồng.
- **Câu dài tách theo ý:** mỗi đoạn phụ đề ≤ ~12 chữ Hán, tách ở dấu phẩy; thời lượng chia theo số chữ Hán trong 1 file giọng (`voice`).
- **Đúng cảm xúc theo tình tiết:** nhân vật chưa biết chuyện thì chưa cười (che miệng cười bằng miệng khép — `neutral`), cười sau.
- **Người đang nói chuyện/cười phải có miệng nói xen kẽ** (`chat`/`mime`), không chỉ cười + nhún. Ảnh sofa 2 người: giữ ảnh liền khối, đứng yên — tách đôi ảnh để lắc riêng làm ghế "lung lay".
- **Cảnh không thoại** (`silent` + `sec`): cho phản ứng giữa các nhân vật (nhìn nhau, nhép miệng), không cần file giọng, không phụ đề.
- Muốn tay/đầu cử động thật cần **tấm tư thế riêng do user cung cấp** rồi luân phiên (`swap`) — xem gotchas.

