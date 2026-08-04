# Session Log

_Append mỗi session. Skill Name = "HSK6 Examiner" hoặc "Speaking Coach"._

_Ví dụ Writing:_
_## 2026-06-11 | Writing | HSK6 Examiner_
_- Topic: 科技与隐私_
_- Score: 185-195 / 300 (phần Writing ~55/100)_
_- Notes: 逻辑性 ổn, cần thêm 关联词_
_- Words used: 信誉, 隐私权_
_- Status: PENDING UPDATE_

_Ví dụ Speaking:_
_## 2026-06-11 | Speaking | Speaking Coach_
_- Topic: Áp lực công việc_
_- Assessment: Phản xạ tốt, tonal errors on 4th tone_
_- Notes: Cần luyện thêm 转折句_
_- Words used: 辜负, 信誉_
_- Status: PENDING UPDATE_

---

## 2026-06-30 | Writing | HSK6 Examiner
- Topic: 我们究竟为什么而活 (ý nghĩa cuộc sống)
- Score: phần Writing ~57–58/60 (sau tinh chỉnh)
- Notes: Bản gốc đã rất tốt (语法 sạch, ẩn dụ 大海里的一朵小浪花 đắt). Tinh chỉnh 3 hướng: (1) cắm ví dụ cá nhân thật (妈妈), (2) phân tầng 向外/向内, (3) thêm 4 discourse marker cá nhân hóa. Gap đã đóng: thiếu ví dụ thật + 2 đoạn giữa song song cùng tầng.
- Words used: 随波逐流, 患得患失, 与其…不如…, 据我观察, 于我而言, 在我心里, 说到底, 固然…却…
- Status: PENDING UPDATE

## 2026-07-10 · Exercise Generator · HSK1 Buổi 1 (会/想/能)
- Blocks: noi, dien_cho_trong, doc_hieu, sap_xep, dich_dat_cau, nghe, noi_hskk×2 (đủ 听/读/书写 + HSKK)
- Độ khó: ~70% HSK1 + điểm xuyết HSK2 (感冒了, 一点儿); kho đề chưa seed → toàn bộ [phỏng theo 真题]
- Output: output/hsk1/baitap/buoi1/{worksheet,dapan}.docx (audio MP3 chờ confirm)
  - Audio: đã sinh 6 MP3 (edge-tts, zh-CN-XiaoxiaoNeural) → buoi1/audio/ (3 nghe + 3 听后重复)

## 2026-07-12 · Exercise Generator · HSK1 Buổi 2 (Lượng từ + 一点儿/有点儿 · Màu sắc)
- Blocks: noi, dien_cho_trong, doc_hieu, sap_xep, dich_dat_cau, nghe, noi_hskk×2 — rút gọn 27 mục (không câu trùng; phủ 8/16 lượng từ + 6/10 màu)
- Output: buoi2_luongtu_mausac/baitap/ → hocsinh/{worksheet.docx + audio 6 MP3} + dapan/dapan.docx
- Audio: zh-CN-XiaoxiaoNeural (3 nghe + 3 听后重复); toàn bộ [phỏng theo 真题]

## 2026-07-12 · Exercise Generator · HSK1 Buổi 3 (了/没/快…了/过 · Thời tiết)
- Blocks: noi, dien_cho_trong, doc_hieu, sap_xep, dich_dat_cau, nghe, noi_hskk×2 — 27 mục (không câu trùng; phủ 8/8 thời tiết + 6/7 mùa + 4/4 ngữ pháp)
- Output: buoi3_le_thoitiet/baitap/ → hocsinh/{worksheet.docx + audio 6 MP3} + dapan/dapan.docx
- Audio: zh-CN-XiaoxiaoNeural (3 nghe + 3 听后重复); toàn bộ [phỏng theo 真题]

## 2026-07-15 · Exercise Generator · Chấm bài học viên · HSK1 Buổi 1 (会/想/能)
- Nguồn: raw/BT chủ đề năng nguyện.docx (bài học viên làm) đối chiếu baitap-buoi1.json
- Kết quả: 24/26 câu khách quan đúng — §1 6/6, §2 5/6, §3 3/3, §4 4/4, §5 3/4, §6 3/3, §7 2/3, §8 tốt
- Lỗi/sửa: §2.3 phân vân 会/想 (đáp án 想); §5.2 nối động từ nên dùng 、 thay 和; §8 viết lẫn phồn thể 騎 (→骑)
- Còn trống: §5.3 (这儿能打电话吗？), §7.3 (我们走路去公园吧。)
- §8 (trả lời tự do): mạnh nhất — dùng được, có 离…很远/送我/睡觉以前; đã gợi ý bản hay hơn giữ 90% câu gốc (nối 也/因为/这样, bỏ lặp)
- Output: buoi1_nangnguyen_phuongtien/baitap/nhanxet.docx (nhận xét bôi đỏ)
- Điểm mạnh cần theo dõi: nền 会/想/能 vững, output tự nhiên; cần nhắc viết giản thể nhất quán + hoàn thành đủ ô

## 2026-08-01 · Exercise Generator · HSK2 Buổi 1 (她请我们吃了北京烤鸭)
- Blocks: noi, dien_cho_trong, doc_hieu (tin nhắn tự soạn), sap_xep, dich_dat_cau, nghe, noi_hskk×2, writing_prompt (lời nhắn 60-100 chữ) — 28 mục (không câu trùng; phủ 12/12 từ vựng + đủ 3 điểm ngữ pháp 吧(2)/是……的/兼语句)
- Output: buoi01_moian_vitquay/baitap/ → hocsinh/{worksheet.docx + audio 8 MP3} + dapan/dapan.docx
- Audio: zh-CN-XiaoxiaoNeural (3 nghe rate -25% + 5 noi_hskk rate -18%); toàn bộ [phỏng theo 真题] (kho hsk2.md chưa seed)

## 2026-08-04 · Exercise Generator · HSK2 Buổi 2 (还是打车去北大吧)
- Blocks: noi (8, có bổ sung 十字路口), dien_cho_trong (6, có bổ sung 一直走), doc_hieu (đường đến thư viện, tự soạn), sap_xep, dich_dat_cau, nghe, noi_hskk×2 (bỏ writing_prompt theo yêu cầu user) — 30 mục (hơi dài so chuẩn 29 nhưng không câu trùng; đã cập nhật phủ thêm nhóm từ 问路 mở rộng — 怎么走/一直走/拐/十字路口/红绿灯/附近 — mới thêm vào slide sau khi draft đầu; câu tránh trùng slide theo yêu cầu user, chỉ giữ chung từ vựng)
- Output: buoi02_giaothong/baitap/ → hocsinh/{worksheet.docx + audio 8 MP3} + dapan/dapan.docx
- Audio: zh-CN-XiaoxiaoNeural (3 nghe rate -25% + 5 noi_hskk rate -18%); toàn bộ [phỏng theo 真题] (kho hsk2.md chưa seed)
