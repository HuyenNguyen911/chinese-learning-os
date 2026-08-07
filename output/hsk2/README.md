# HSK2 (chuẩn 3.0) — Syllabus tổng

**Chuẩn:** 国际中文教育中文水平等级标准 3.0 (công bố ~11/2025).
**Sách chính:** *New HSK Course 2* (新HSK教程2, 主编 郭风岚, 外语教学与研究出版社/FLTRP) — 15 bài, ~200 từ mới + mở rộng, 45 điểm ngữ pháp (小语讲堂).
**Sách tham khảo (đối chiếu, không phải nguồn dạy):** 《汉语教程》第一册·下 (杨寄洲, BLCU) — bài 16-30, footer mỗi buổi.
**Đầu vào:** học viên đã qua HSK1 (chuẩn 3.0, ~300 từ).
**Nguồn thiết kế:** `docs/superpowers/specs/2026-07-20-hsk2-full-course-design.md` (spec) + `docs/superpowers/plans/2026-07-20-hsk2-full-course.md` (plan) + `docs/superpowers/specs/hsk2-new-hsk-course-2-toc.md` (mục lục thật) + `docs/superpowers/plans/hsk2-vocab-grammar-checklist.md` (210 từ vựng).

**Sản xuất tuần tự** — mỗi buổi 1 cổng duyệt riêng trước khi mở buổi kế tiếp (không làm pilot rồi hàng loạt).

## Syllabus 15 buổi + 2 ôn

| # | Buổi (folder) | 课文 | Chủ đề | Ngữ pháp (小语讲堂) | Hán ngữ 第一册·下 | Trạng thái |
|---|---|---|---|---|---|---|
| 1 | `buoi01_moian_vitquay` | 她请我们吃了北京烤鸭 | mời ăn, món BK, nhờ vả | 语气助词"吧"(2) · "是…的"句 · 兼语句 (请/让/叫) | — | ✅ |
| 2 | `buoi02_giaothong` | 还是打车去北大吧 | giao thông, đề nghị **+ hỏi đường 怎么走** | 还是…吧 · 多(概数) · cụm làm định ngữ | L16 · L17 | ✅ |
| 3 | `buoi03_dulich_xian` | 我想去西安旅游 | du lịch (Tây An) **+ đặt khách sạn**⚠️ | 结果补语 · 动词重叠(1)(2) | L29 · L19 · L27 | ⏳ |
| 4 | `buoi04_trangphuc_mausac` | 你穿红色的很好看 | trang phục, màu sắc | 动态助词"过" · 因为…所以 · 的字短语 · **把字句 (bổ sung)** | L19 | ⏳ |
| 5 | `buoi05_thamnha` | 第一次去中国朋友家 | thăm nhà bạn TQ **+ động vật/thú cưng + giới thiệu bản thân/gia đình sâu** | 简单趋向补语(1)(2) · 都…了 | — | ✅ |
| 6 | `buoi06_sinhnhat` | 小雪，生日快乐！ | sinh nhật, chúc mừng | ~~形容词重叠 · "什么的" · "地"~~ → đã build 状态补语(1)(2)[得] (lệch, xem ghi chú "Sửa 2026-08-06 (khi bóc Bài 7)") | L25 | ✅ |
| 7 | `buoi07_thethao` | 他篮球打得很好 | thể thao (bóng rổ) | 状态补语(1)(2) [得] (ôn lại, đã dạy ở Buổi 6) · 紧缩复句"一…就…" | L25 | ⏳ |
| 8 | `buoi08_trinho_sosanh` | 虽然你忘了，但是我记得 | mua sắm (đồng hồ/xem phim/đặt món), sinh nhật, trí nhớ, so sánh **+ hỏi giá/so sánh giá**⚠️ **+ nhận lỗi/xin lỗi/hứa sửa**⚠️ | 比较句(1)(2)[比] tách 6 dạng (cơ bản/一点儿/số lượng/还-更/phủ định/nghi vấn) · 虽然…但是 | L28 · L23 | ✅ |
| — | `on1_bai1-8` | **Ôn 1** (giữa khoá) | ôn bài 1-8 + bảng hệ thống bổ ngữ (kết quả/xu hướng/得) + bảng 比较句(1)(2)(3) — chỉ ôn tập | — | — | ⏳ |
| 9 | `buoi09_douong` | 我去买杯奶茶 | mua sắm (quần áo) + đồ uống (cà phê/trà sữa) + so sánh khoảng cách, đi bộ | 比较句(3) [没有] · 动词"离" · 时量补语(1) | L30 · L16 | ⏳ |
| 10 | `buoi10_thicu` | 就要考试了 | thi cử, học tập **+ đặt lịch hẹn**⚠️ | 要/快/快要/就要…了 · 着(1)(2) (⚠️ trang 099 目标 chỉ liệt kê 主谓谓语句·选择问句·要/快/快要/就要…了, KHÔNG thấy 着 — nghi 着(1)(2) cũng bị lệch bài, chưa verify hết Bài 10 nên giữ tạm, cần đối chiếu ảnh đầy đủ trước khi sản xuất buổi 10) | — | ⏳ |
| 11 | `buoi11_monan_yeuthich` | 我最喜欢吃中国菜 | ăn uống, sở thích | 程度副词"最" · **被字句 (bổ sung)** | — | ⏳ |
| 12 | `buoi12_thoitiet` | 这里比北京冷多了 | thời tiết, so sánh | 比较句(4)(5)(6) · **连…都/也 (bổ sung)** | — | ⏳ |
| 13 | `buoi13_hoctiengtrung` | 我们爱上中文课 | học tiếng Trung | 双宾语句(2) · 比较句(7)(8) | L17 | ⏳ |
| 14 | `buoi14_letet` | 一个人过年多没意思啊 | lễ Tết, cảm xúc | 存现句 · 复合趋向补语 | L23 | ⏳ |
| 15 | `buoi15_kehoach` | 我想再去一次中国 | kế hoạch, quay lại TQ | 动量补语(1)(2) · 有字句(2) | — | ⏳ |
| — | `on2_bai9-15` | **Ôn 2** (cuối khoá) | ôn bài 9-15 + bảng hệ thống bổ ngữ đầy đủ 6 loại + bảng 比较句(1)-(8) đầy đủ + capstone roleplay (hỏi đường/khách sạn/giới thiệu bản thân/hỏi giá/đặt lịch hẹn — chỉ ứng dụng lại) | — | — | ⏳ |

⚠️ = ngoài phạm vi chuẩn thi chính thức HSK2 (đã đối chiếu HSK 二级考试大纲 chính thức), giữ lại theo yêu cầu thực dụng cá nhân — xem spec §16b.

**Sửa 2026-08-04 (khi bóc Bài 3):** cột ngữ pháp Bài 3/4 bị lệch 1 bài so với sách
thật (TOC gốc gán nhầm, cùng lỗi dạng đã sửa ở Bài 1/2 với 兼语句) — đã đối chiếu trực
tiếp PDF trang 019-036 và sửa lại: Bài 3 chỉ có 结果补语+动词重叠(1)(2); 过 và 因为…
所以 thực ra thuộc Bài 4. Xem `output/hsk2/buoi03_dulich_xian/doc/bai-doc.md` để biết
chi tiết đối chiếu.

**Sửa 2026-08-05/06 (khi bóc Bài 5):** đã xác minh lại 4 điểm cũ còn hedge ở trên —
**KHÔNG thuộc Bài 5**, đúng là bị lệch tiếp: 形容词重叠 · 固定短语"什么的" · 结构助词
"地" thực ra thuộc **Bài 6** (objectives trang 062 xác nhận), 紧缩复句"一…就…" thuộc
**Bài 7** (objectives trang 072 xác nhận). Bài 5 CHỈ có 简单趋向补语(1)(2) + 都…了
(đã sửa lại bảng syllabus ở trên). Khi sản xuất Bài 6/7 nhớ đối chiếu lại các điểm này
đã đúng vị trí trong TOC hiện tại chưa trước khi bóc.

**Sửa 2026-08-06 (khi bóc Bài 7) — phát hiện Buổi 6 đã build SAI ngữ pháp:** dòng
bảng Bài 6/7 ở trên KHI ĐÓ vẫn còn nội dung cũ (chưa đồng bộ theo note ngay trên), nên
lúc build slide Buổi 6 đã lấy nhầm "状态补语(1)(2)[得]" (ngữ pháp thật của **Bài 7**)
thay vì "形容词重叠 · 什么的 · 地" (ngữ pháp thật của Bài 6) — trong khi chủ đề/课文/生词
Buổi 6 (sinh nhật) vẫn đúng sách. Đối chiếu trực tiếp ảnh trang 072-088: Bài 7 thật =
状态补语(1)(2)[得] + 紧缩复句"一…就…" (KHÔNG có 比较句); 比较句(1)(2)[比] thực ra thuộc
**Bài 8** (thay cho 比较句(3)+动词"离" cũ — điểm đó nghi thuộc Bài 9, **chưa verify bằng
ảnh**, xem `output/hsk2/buoi07_thethao/doc/bai-doc.md` phần cảnh báo cuối). **Quyết định
của user (2026-08-06): KHÔNG sửa lại Buổi 6 đã duyệt/push — chấp nhận lệch.** Buổi 7 dạy
đúng theo sách thật (状态补语 ôn lại + 一…就… mới), học viên sẽ ôn 状态补语 lần 2 một cách
tự nhiên qua chủ đề thể thao. **Bài 9 cần verify lại bằng ảnh trước khi sản xuất** (không
chặn Buổi 7).

**Sửa 2026-08-06 (verify Bài 8/9/10 bằng ảnh, trước khi bóc Bài 8):** đối chiếu trực tiếp
ảnh PDF trang 079-099 (`output/hsk2/buoi08_trinho_sosanh/doc/_tmp/p79-88.png` +
`output/hsk2/buoi09_douong/doc/_tmp/p88-99.png`) — bảng ở trên vẫn còn SAI cả biên trang
và ngữ pháp:
- **Bài 8** thật = trang **079-087** (không phải 080-088): trang 079 là 目标, đúng
  2 điểm **比较句(1)(2)[比]** (trang 081, 083) + **虽然…但是** (trang 084-085) — đã sửa
  thứ tự cột ngữ pháp cho khớp trình tự sách (trước đó ghi 虽然…但是 trước 比较句 là sai
  thứ tự). Không có điểm thứ 3 nào lẫn vào cuối Bài 8 — 比较句(3)/动词"离" hoàn toàn không
  xuất hiện ở Bài 8.
- **Bài 9** thật = trang **088-098** (không phải trang 089-095 như gợi ý cũ dựa text
  extract thô) — ⚠️ **sửa lại 2026-08-06 (khi bóc Bài 9):** con số này lệch 1, giống lỗi
  đã xảy ra với Bài 8 ở mục ngay trên (079-087 lệch 1 so với 080-088 xác nhận sau này).
  Đối chiếu trực tiếp ảnh trang (`output/hsk2/buoi09_douong/doc/bai-doc.md`): trang bìa
  "Lesson 9 我去买杯奶茶" là **PDF index 89 = trang in sách 073**; toàn bộ nội dung Bài 9
  nằm ở **PDF index 89-98 = trang in sách 073-082** (PDF index 88/trang 072 vẫn là 课堂
  活动 cuối Bài 8). Tên bài 我去买杯奶茶 ĐÚNG như README đã ghi, ngữ pháp 3 điểm là
  **比较句(3)[没有]** (trang 090-091) + **动词"离"** (trang 092) + **时量补语(1)** (trang
  093-094) — HOÀN TOÀN KHÔNG có 主谓谓语句/选择问句 (2 điểm đó thuộc **Bài 10**, xác nhận ở
  trang 099 目标). 生词 đối chiếu checklist 13 từ (`hsk2-vocab-grammar-checklist.md` mục
  Bài 9): 坏·个子·近·咖啡·离·门口·那么·男孩儿·旁边·这样·周·走路·高 — **khớp 100%**, tất cả xuất
  hiện đúng trong 4 khối 生词 của Bài 9 (课文1: 坏·旁边·男孩儿·这样·个子·那么·高; 课文2: 门口·
  咖啡·离; 课文3: 近·走路; 课文4: 周). Chủ đề thật: **mua sắm (quần quần áo cho con) + mua đồ
  uống (cà phê/trà sữa) + so sánh khoảng cách/đi bộ về nhà** — không phải thuần "đồ uống"
  như dòng cũ, nhưng 课文2 vẫn có mua trà sữa/cà phê nên tên bài + phần "đồ uống" trong chủ
  đề vẫn đúng, chỉ thiếu phần so sánh khoảng cách (đã bổ sung vào cột chủ đề).
- **Bài 10** thật bắt đầu trang **099** (`我去买杯奶茶` kết thúc đúng trang 098 bằng
  trang 学习小结 tổng kết 7-9), tên bài 就要考试了 + chủ đề thi cử ĐÚNG như README đã ghi.
  目标 trang 099 chỉ liệt kê 3 điểm 主谓谓语句·选择问句·要/快/快要/就要…了 — KHÔNG thấy
  "着(1)(2)" trong 目标 này, nghi ngữ pháp 着(1)(2) hiện gán cho Bài 10 cũng bị lệch, nhưng
  **CHƯA verify hết nội dung Bài 10** (nhiệm vụ này chỉ yêu cầu xác định biên, không bóc
  đầy đủ) — để hedge trong bảng, cần verify lại bằng ảnh trước khi sản xuất Buổi 10.
- **Cân nhắc "hỏi giá/so sánh giá" (mở rộng cá nhân hoá đang gắn ở Bài 9):** sau khi verify,
  Bài 9 KHÔNG có đoạn hỏi giá/số tiền nào trong 课文. Ngược lại **Bài 8 课文1** có hẳn đoạn
  hỏi giá đồng hồ ("你看看要多少钱！" → "八千八！") gắn liền với 比较句. Đề xuất: dời phần mở
  rộng "hỏi giá/so sánh giá" từ Bài 9 sang Bài 8 (khớp nội dung sách hơn) — **cần user xác
  nhận trước khi đổi**, hiện bảng trên đã tạm bỏ ghi chú "hỏi giá" khỏi cả 2 dòng Bài 8/9
  chờ quyết định.

## Ghi chú kỹ thuật

- **Ngữ pháp bổ sung ngoài 45 điểm sách** (把 Bài 4, 被 Bài 11, 连…都/也 Bài 12, 复合趋向补语 Bài 5 — đưa sớm từ Bài 14 vì học viên đã nắm chắc 简单趋向补语): đánh dấu rõ trong slide buổi tương ứng "ngữ pháp mở rộng ngoài sách chính".
- **Buổi 5 nâng độ khó từ vựng** (2026-08-06, theo yêu cầu user — học viên đã vượt xa mức 18 từ gốc sách): 生词 slide đổi hẳn sang 20 từ động từ nâng cao (拿/带/搬/寄/扔/摆/放/挂/抬/抱/提/借/还/卖/爬/跳/倒/退/躲/传) để luyện 简单/复合趋向补语, không dùng 18 từ gốc sách nữa (18 từ gốc vẫn xuất hiện tự nhiên qua 課文). Bài tập (`baitap-buoi05.json`) vẫn bám 18 từ gốc + 3 điểm ngữ pháp chính theo đúng chuẩn Bài 5. Cân nhắc áp dụng tương tự (khảo sát trình độ trước khi bám 100% sách) cho các buổi sau nếu học viên tiếp tục vượt tiến độ.
- **Viết 3.0:** mỗi buổi bài tập có sắp câu/điền chữ/câu ngắn + luân phiên đoạn 60-100 chữ / điền form (`dien_bieu_mau`) / lời nhắn / nhật ký (`writing_prompt` với `kind` + `target_length`) — schema đã mở rộng ở exercise-generator (`main`, commit `021493e`).
- **Đọc thực tế:** mỗi buổi bài tập phần 读 có ≥1 văn bản tự soạn theo chủ đề (tin nhắn/biển báo/thực đơn/quảng cáo), không lấy từ sách.
- **Từ vựng:** 210 mục (207 từ + 3 tên riêng), 19 từ trùng HSK1 cần xử lý khi sản xuất buổi tương ứng (đáng chú ý: Bài 4 trùng 5/16 từ — cụm màu sắc) — xem `hsk2-vocab-grammar-checklist.md`.
- **Pinyin:** PDF gốc lỗi mất dấu thanh toàn sách → luôn tự sinh bằng `pypinyin` từ chữ Hán, không tin pinyin in kèm.
- **GIF thứ tự nét:** tuỳ chọn cho chữ mới khó, tái dùng `gen_stroke_gif.py` của HSK1 — không bắt buộc mỗi buổi.
- **Trang từ vựng** (`output/study/hsk2/buoiXX/tu-vung.html`): làm ở phase cuối, sau khi cả 15 buổi + 2 ôn chốt xong vocab.

## Trạng thái build

Buổi 1 ✅ (slide + bài tập, đã duyệt 2026-08-02). Buổi 2 ✅ (slide + bài tập, đã duyệt
2026-08-04 — có bổ sung nhóm từ 问路 ngoài 45 điểm sách, xem ghi chú kỹ thuật). Buổi 5 ✅
(slide + bài tập, đã duyệt 2026-08-06 — 生词 slide đổi sang 20 từ nâng cao + mở rộng
复合趋向补语, xem ghi chú kỹ thuật). Buổi 8 ✅ (slide + bài tập, đã duyệt
2026-08-06 — 生词 gộp chung 1 khối đầu bài (13 chính + 6 mở rộng nhận lỗi/xin
lỗi), 課文 1-4 gộp liền nhau, 比较句 tách 6 slide riêng theo dạng câu, mở rộng
hỏi giá dời từ Bài 9 sang; đã sửa 2 lỗi audio ở tool dùng chung — xem
`state/session-log.md`). Buổi 3-4, 6-7, 9-15 (trừ 8) + Ôn 1 + Ôn 2 xem trạng
thái ở bảng trên (⚠️ dòng này có thể chưa đồng bộ hết với bảng — bảng trên là
nguồn chân lý).
