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

## 2026-08-05 · Exercise Generator · HSK2 Buổi 4 (你穿红色的很好看)
- Blocks: noi (7: 尺码/打折/试衣间/配饰/经典/百搭/合适), dien_cho_trong (5: 更/过去/因为/所以/条), doc_hieu (tin nhắn mua sắm tự soạn), sap_xep (把字句/过), dich_dat_cau (因为…所以…/过/把), nghe, noi_hskk×2 — 29 mục, không câu trùng. Trước khi duyệt đã rà lại toàn bộ câu theo đúng từ vựng đã dạy buổi 1-4 (đối chiếu corpus 汉字 toàn bộ slide, không chỉ danh sách 生词) — phát hiện & thay 8 từ ngoài phạm vi (陪/顾客/购买/藏青色/商品/将/如需/耐脏/冷/暖和/平时/而且/看起来/不一样/国外/少见), viết lại đoạn đọc hiểu bằng từ đã học.
- Output: buoi04_trangphuc_mausac/baitap/ → hocsinh/{worksheet.docx + audio 8 MP3} + dapan/dapan.docx
- Audio: zh-CN-XiaoxiaoNeural (3 nghe rate -25% + 5 noi_hskk rate -18%); toàn bộ [phỏng theo 真题] (kho hsk2.md chưa seed)

## 2026-08-06 · Exercise Generator · HSK2 Buổi 5 (第一次去中国朋友家)
- Blocks: noi (5: 爷爷/奶奶/礼物/酒店/奶茶), dien_cho_trong (5: 快/等/跟/一会儿/走), doc_hieu (tin nhắn hẹn giờ đến nhà bạn tự soạn), sap_xep (简单趋向补语/都……了), dich_dat_cau, nghe, noi_hskk×2 (听后重复 + 回答问题) — 28 mục, không câu trùng. Bám 18 từ gốc sách + 3 điểm ngữ pháp chính (简单趋向补语(1)(2), 都……了), không dùng 20 từ nâng cao mở rộng của slide. 听后重复 lần đầu soạn bị trùng câu 課文/khẩu ngữ — user phát hiện, đã đổi 3 câu khác dùng cùng từ vựng nhưng cách diễn đạt mới.
- Output: buoi05_thamnha/baitap/ → hocsinh/{worksheet.docx + audio 8 MP3} + dapan/dapan.docx
- Audio: zh-CN-XiaoxiaoNeural (3 nghe rate -25% + 5 noi_hskk rate -18%)

## 2026-08-06 · Exercise Generator · HSK2 Buổi 6 (小雪，生日快乐！)
- Blocks: noi (7: 蜡烛/打开/蛋糕/画笔/快乐/舒服/惊喜), dien_cho_trong (4: 的/地/得), doc_hieu (tiệc sinh nhật bất ngờ, tự soạn), sap_xep (状态补语 得, gồm dạng lặp động từ có tân ngữ + phủ định), dich_dat_cau, nghe, noi_hskk×2 (听后重复 + 回答问题) — 28 mục, không câu trùng. Lần soạn đầu bị 5 câu trùng nguyên văn + nhiều câu gần trùng với slide (user phát hiện, đối chiếu bằng script so khớp câu) — đã viết lại toàn bộ câu trùng bằng tình huống/cách diễn đạt mới, chỉ giữ chung từ vựng + điểm ngữ pháp.
- **Phần 回答问题 (mọi buổi 1-6):** bổ sung dàn bài chuẩn HSKK 初级 vào `instructions` (hiện ngay trên worksheet, không chỉ đáp án): (1) trả lời thẳng 1 câu ngắn, (2) thêm 1 câu mô tả/giải thích, (3) không bắt buộc — 1 câu cảm nghĩ/mở rộng để đạt điểm cao. Đã rebuild lại worksheet+dapan buổi 1-4 để đồng bộ (buổi 5 chưa render nên chỉ cập nhật JSON).
- Output: buoi06_sinhnhat/baitap/ → hocsinh/{worksheet.docx + audio 8 MP3} + dapan/dapan.docx
- Audio: zh-CN-XiaoxiaoNeural (3 nghe rate -25% + 5 noi_hskk rate -18%); toàn bộ [phỏng theo 真题] (kho hsk2.md chưa seed)

## 2026-08-06 · Exercise Generator · HSK2 Buổi 8 (虽然你忘了，但是我记得)
- Blocks: noi (7: 手表/记得/有意思/虽然/花/错/一定), dien_cho_trong (4: 比/虽然/但是/一点儿), doc_hieu (mua tặng mẹ đồng hồ nhân sinh nhật, tự soạn), sap_xep (比较句 一点儿/số lượng cụ thể + 虽然…但是), dich_dat_cau (3), nghe (3: hỏi giá/xin lỗi/so sánh sách), noi_hskk 听后重复 (3), noi_hskk 回答问题 (2, dàn bài mở-thân-kết theo yêu cầu riêng của user thay vì dàn bài 3-câu mặc định) — 29 mục, không câu trùng (đã đối chiếu cả nội bộ lẫn với toàn bộ slide buổi 8).
- **回答问题 buổi 8 dùng dàn bài khác 2 kiểu trước (mặc định 1-2-3 câu ngắn):** user yêu cầu kiểu gợi ý mở bài/thân bài/kết bài (câu hỏi gợi mở từng phần) thay vì 3 câu mẫu ngắn — áp dụng riêng cho buổi này, chưa đổi mặc định của skill.
- Output: buoi08_trinho_sosanh/baitap/ → hocsinh/{worksheet.docx + audio 8 MP3} + dapan/dapan.docx
- Audio: zh-CN-XiaoxiaoNeural (3 nghe rate -25% + 5 noi_hskk rate -18%); toàn bộ tự soạn (kho hsk2.md chưa seed)

## 2026-08-06 · Exercise Generator · HSK2 Buổi 7 (他篮球打得很好)
- Blocks: noi (7: 从/往/跑步/游泳/爱好/开始/运动), dien_cho_trong (4, điền 得 ôn 状态补语), doc_hieu (刘明 thích thể thao, tự soạn), sap_xep (3, 得 + 一…就…), dich_dat_cau (3), nghe (3), noi_hskk 听后重复 (3), noi_hskk 回答问题 tách 2 block riêng theo 2 câu hỏi (mỗi câu 1 dàn bài 开头/主体/结尾 riêng, bám sát nội dung câu đó — theo mẫu user cung cấp) — 28 mục, không trùng nội bộ/slide (đã check_baitap.py + đối chiếu thủ công).
- **Bỏ block `writing_prompt`** theo yêu cầu user (không muốn phần Viết nhật ký ở buổi này).
- **回答问题 tách thành 2 block riêng (không dùng 1 block chung 2 câu)** — vì mỗi câu cần dàn bài 开头/主体/结尾 khác nhau bám đúng nội dung câu đó (không phải 1 dàn bài chung cho cả 2 câu). Khớp pattern đã dùng ở Buổi 8 (đổi từ dàn bài 3-câu mặc định sang mở-thân-kết), nhưng buổi 7 đi xa hơn: tách block + dàn bài riêng từng câu.
- Output: buoi07_thethao/baitap/ → hocsinh/{worksheet.docx + audio 8 MP3} + dapan/dapan.docx
- Audio: zh-CN-XiaoxiaoNeural (3 nghe rate -25% + 5 noi_hskk rate -18%); toàn bộ tự soạn (kho hsk2.md chưa seed)
