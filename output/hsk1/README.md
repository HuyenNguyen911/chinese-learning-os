# HSK1 — Bộ giáo trình 16 buổi (chuẩn HSK 3.0 · syllabus · source of truth)

Thứ tự **dạy** hợp lý cho bộ HSK1, bám **New HSK Course 1 3.0** (新HSK1教程 3.0, 15 课, ~300 từ
chuẩn 2026 final). Số buổi = vị trí syllabus = prefix folder (`buoi01`…`buoi16`).

Chi tiết thiết kế: `docs/superpowers/specs/2026-07-21-hsk1-3.0-full-course-design.md`
(thay cho bản 2.0 `2026-07-19-hsk1-full-course-design.md` — SUPERSEDED, giữ tham chiếu lịch sử).
Nguồn 生词 gốc theo 课: `docs/superpowers/specs/newhsk1-book-content.md`.
Checklist phủ ~300 từ theo buổi: `docs/superpowers/plans/hsk1-3.0-checklist.md`
(thay cho `hsk1-150-checklist.md` bản 2.0 — SUPERSEDED).

## Syllabus

| # | Buổi | Folder | 课文 sách | Ngữ pháp trọng tâm | Trạng thái |
|---|---|---|---|---|---|
| 01 | Ngữ âm: pinyin · thanh điệu · thanh/vận mẫu · 变调 | `buoi01_nguam/` | — | hệ thống ngữ âm, thanh điệu, 变调 | ✅ đã có |
| 02 | Chào hỏi & làm quen | `buoi02_chaohoi_lamquen/` | L1 你好 · L2 我叫李文 | 是 · 吗 · 呢 · 叫…名字 | ⏳ chưa soạn |
| 03 | Quốc tịch & bản thân | `buoi03_quoctich/` | L3 我是中国人 (3 课文) | "是"字句 · 结构助词"的" · 用"吗"的是非问句 | ✅ XONG (38 slide + audio; không làm baitap — thực hành ngay trên lớp) |
| 04 | Gia đình | `buoi04_giadinh/` | L4 我有两个孩子 | "有"字句 · 几口人 · 和 · 都 · 两 vs 二 | ⏳ chưa soạn |
| 05 | Số đếm & số điện thoại | `buoi05_sodem_sodt/` | L6 手机号是多少 | 多少 vs 几 · số lớn · 连动句(1) | ✅ slide XONG (28 slide + 20 audio; 22 生词 bám sách — bỏ 西安饭店 khỏi thẻ từ vựng riêng vì chỉ là tên riêng 1 lần dùng, vẫn giữ trong 课文/ví dụ; 3 课文 hội thoại dạng 1-cột tuần tự [`layout: "column"`, thêm 2026-09-09]; 语法 想/连动句/怎么 + mở rộng 几vs多少/đọc số điện thoại; 1 slide 练习 选词填空 nguyên đề sách); baitap CHƯA làm — chưa quyết định |
| 06 | Ngày tháng & nghỉ làm | `buoi06_ngaythang/` | L5 今天我休息 | 时间的表达(1) · 名词谓语句 · 能愿动词"会" | ⏳ chưa soạn |
| 07 | Giờ giấc & công việc | `buoi07_giogiac_congviec/` | L7 六点半下班 | 时间的表达(2): 点/分 · 语气助词"吧"(1) | ⏳ chưa soạn |
| 08 | Nghề & nơi làm · 在 | `buoi08_nghe_vitri/` | L8 在医院工作 | 方位词 · 介词"在" · 能愿动词"能" | ✅ XONG 2026-09-10 (23 từ audit lại bằng vision — checklist cũ thiếu 学校/书店/病人; 27 slide + audio + ảnh Pexels, có tách nền rembg cho ảnh chân dung nghề nghiệp; 语法 mở rộng có bảng so sánh 会/想/能 lấy từ buổi06 2.0 cũ — xem mục "Buổi cũ (2.0) tái dùng" bên dưới; KHÔNG có baitap/ riêng — bài tập đã nhúng trong slide) |
| 09 | Nơi chốn & đồ vật · vị trí | `buoi09_noichon_dovat/` | L9 在学校学习 | 存现句(1) · thời gian+nơi chốn làm trạng ngữ · 第 | ⏳ chưa soạn |
| 10 | Mua sắm & giá tiền | `buoi10_muasam/` | L10 苹果真便宜 | 钱数的表达 · 形容词谓语句 · 怎么样 | ⏳ chưa soạn |
| 11 | Ăn uống & gọi món | `buoi11_anuong/` | L13 请给我一杯茶 | 能愿动词"可以" · 动词+一下 · 双宾语句(1) | ⏳ chưa soạn |
| 12 | Sở thích & phim · 了 | `buoi12_sothich_phim/` | L14 看了一个电影 | 动态助词"了(2)" · 离合词(1) · 范围副词"都" | ⏳ chưa soạn |
| 13 | Đại học & đang làm · 呢 | `buoi13_daihoc/` | L11 我读大学呢 | 正反问 · 时间副词"在/正在" · 能愿动词"要" | ⏳ chưa soạn |
| 14 | Thời tiết & sức khỏe | `buoi14_thoitiet_suckhoe/` | L12 昨天下雪了 | 非主谓句 · 语气助词"了(1)" · "太……了" | ⏳ chưa soạn |
| 15 | Đi lại & du lịch · hẹn gặp | `buoi15_dulai_dulich/` | L15 大兴机场见 | 并列复句"……，还/也……" | ⏳ chưa soạn |
| 16 | Ôn tập tổng hợp | `buoi16_ontap/` | — (ôn ~243–300 từ đã học) | Phần 1: đủ 15 điểm ngữ pháp trọng tâm của 15 bài sách 3.0. Phần 2: 243 từ vựng theo chủ đề | ✅ phần 1 (`slide/`) + phần 2 (`slide2_tuvung/`) xong slide + audio + ảnh (chưa có baitap/) |

**15 buổi cần soạn** = vị trí 02–16 (buổi 01 ngữ âm đã xong; buổi 03 đã xong 2026-09-08).

> ⚠️ **Số từ trong checklist KHÔNG đáng tin — phải đối chiếu sách trước khi soạn mỗi buổi.**
> Phát hiện khi làm buổi 03 (2026-09-08): mỗi bài trong sách có NHIỀU khối 生词 (X-2, X-4, X-6…),
> mỗi khối cạnh 1 đoạn 课文 khác nhau; bản bóc cũ chỉ lấy 1-2 khối đầu. Bài 3 thực tế **22 từ**
> nhưng checklist ghi 11 (thiếu 12, thừa 1 — 都 vốn thuộc Bài 14). Các bài khác rất có thể cũng
> thiếu tương tự. Cách kiểm đúng: render trang PDF ra ảnh rồi ĐỌC BẰNG VISION
> (`fitz` → `get_pixmap(dpi=170)`), KHÔNG dùng `raw/新HSK1教程3.0.pdf.ocr.txt` cho bảng 生词
> (OCR sách này xáo chữ Hán, sai dấu pinyin, mất số thứ tự).

## Buổi cũ (2.0) tái dùng — không phải buổi mới, chỉ là nguồn nguyên liệu

`buoi06_nangnguyen_phuongtien/`, `buoi10_luongtu_mausac/`, `buoi12_le_thoitiet/` là 3 folder
**đã sản xuất theo syllabus 2.0** (12 buổi, sách HSK Standard Course) — **số buổi của chúng
KHÔNG khớp vị trí 06/10/12 trong bảng 3.0 ở trên**. Theo spec 3.0 §5, đây là nguồn tái dùng có
chọn lọc:
- `buoi06_nangnguyen_phuongtien` (会/想/能, giao thông) — **QUYẾT ĐỊNH CHỐT 2026-09-10**
  (đơn giản hoá so với dự kiến ban đầu "fold vào 08/13/15"): xé làm 2, KHÔNG dùng buổi 13.
  - Phần **ngữ pháp** 会/想/能 → ✅ ĐÃ vào buổi 3.0 mới **08** (`buoi08_nghe_vitri/`, bảng so
    sánh "Đừng nhầm 3 từ 'có thể'", xong 2026-09-10).
  - Phần **chủ đề giao thông** (坐/飞机/开车/公共汽车/地铁/出租车...) → ⏳ CHƯA dùng, để dành cho
    buổi 3.0 mới **15** (`buoi15_dulai_dulich/`, chưa soạn).
- `buoi10_luongtu_mausac` (lượng từ, màu sắc): reuse lượng từ **个/本/块** vào buổi 3.0 mới
  **04/10**. 个/本 đã đủ ở buổi 04 (`buoi04_giadinh/`, xong, có 生词拓展·量词 riêng) — buổi 04
  KHÔNG cần lấy gì thêm từ folder này nữa. Buổi **10** (Mua sắm & giá tiền, `buoi10_muasam/`)
  vẫn ⏳ CHƯA soạn — khi soạn, lấy lượng từ liên quan mua sắm (块 tiền, cái, chiếc...) từ folder
  này. Màu sắc (红/蓝…) phần lớn NGOÀI phạm vi 300 từ 3.0 → để "mở rộng", không dạy như 生词
  chính (xem checklist §"Đối chiếu tận dụng buổi cũ").
- `buoi12_le_thoitiet` (了/过, thời tiết): reuse ngữ pháp **了** + thời tiết cơ bản
  (天气/下雨/下雪/冷/热) vào buổi 3.0 mới **14** (`buoi14_thoitiet_suckhoe/`, ⏳ CHƯA soạn).
  Mùa/暖和/凉快/度/晴天/阴天 NGOÀI 300 → "mở rộng".

Nội dung 3 folder cũ KHÔNG bị xoá — `buoi10_luongtu_mausac/` và `buoi12_le_thoitiet/` vẫn còn
nguyên vẹn để tái dùng cho buổi 10/14 sau này; `buoi06_nangnguyen_phuongtien/` vẫn giữ phần
giao thông chưa dùng, chờ buổi 15.

`on1_nguphap_dongtu/` (2.0) đã xoá — thay bằng `buoi16_ontap/slide/` (phần 1, đúng 15 điểm
ngữ pháp sách 3.0). `on2_tuvung_chude/` (2.0) đã được dựng lại thành `buoi16_ontap/slide2_tuvung/`
(phần 2, 243 từ theo checklist 3.0, nhóm theo 14 chủ đề buổi 02–15, có ảnh minh hoạ + audio).

## Cấu trúc mỗi buổi

```
buoiXX_<slug>/
  slide/   buoiXX.json + Buoi-XX-*.pptx + assets/ (ảnh, GIF, audio/slideNN.mp3)
  baitap/  baitap-buoiXX.json + hocsinh/{worksheet.docx, audio/} + dapan/dapan.docx
  doc/     课文 sách (bóc từ newhsk1-book-content.md): 汉字+pinyin+dịch + audio edge-tts + footer đối chiếu Hán ngữ Q1
```

**Buổi 16 (ôn tập) là ngoại lệ 2 phần** — không có 课文/doc riêng, gồm 2 slide deck độc lập:
```
buoi16_ontap/
  slide/            phần 1 — 15 điểm ngữ pháp trọng tâm (buoi16.json + Buoi-16-Ontap.pptx + assets/)
  slide2_tuvung/    phần 2 — 243 từ vựng theo 14 chủ đề buổi 02-15 (buoi16-p2.json +
                    Buoi-16-P2-Tuvung.pptx + assets/)
```

**Thứ tự block slide — mô hình 2 PHẦN (chốt ở buổi 03, 2026-09-08):**

```
title → 目标 (mục tiêu)
── 第一部分 · 课本生词 (slide `section`) ──
   生词 bám sách (wordcard 1 từ / word_pair 2 từ, mỗi từ 2 ví dụ)
   → 课文 nguyên văn của sách (đủ các đoạn, mỗi đoạn 1 slide dialogue)
   → 语法 (dùng `grammar.groups`: mỗi điểm ngữ pháp kèm ví dụ riêng, 2 cột)
   → 自我介绍 (3 bước: chào mở đầu → thông tin cá nhân → lời kết)
── 第二部分 · 生词拓展 (slide `section`) ──
   từ mở rộng ngoài sách (tên nước khác, cấp học…)
   → 配对游戏 (slide `match_pairs`, tối đa 5 cặp/slide, chia đều)
```

Khác bản 2.0 cũ (`title → ôn buổi trước → mục tiêu → 生词 → ngữ pháp → 10 câu khẩu ngữ →
hội thoại → bài đọc → footer Hán ngữ → lỗi người Việt → preview bài tập`): **bỏ** slide ôn buổi
trước, bảng 10 câu khẩu ngữ, bảng lỗi người Việt và slide preview bài tập; **tách** từ bám sách
với từ mở rộng thành 2 phần có slide phân mục; **thêm** minigame nối ảnh-từ cuối buổi.
Buổi 01 (ngữ âm) là ngoại lệ: không có 生词/课文, thay bằng các block luyện âm.

## Ghi chú kỹ thuật

- **GIF phát âm (buổi 01 ngữ âm):** đã xác nhận GIF động **nhúng thẳng trong `.pptx` PHÁT ĐỘNG**
  khi trình chiếu PowerPoint desktop (Task 0.2, user verified). Chốt phương án embed (không dùng
  fallback sprite). Sinh GIF: `scripts/hsk1/gen_tone_gif.py` (thanh điệu), `scripts/hsk1/gen_stroke_gif.py`
  (thứ tự nét, nguồn Make Me a Hanzi). Buổi 01 đã sản xuất xong (commit `3791086`), giữ nguyên.
- **Pivot 2.0 → 3.0 (2026-07-21):** cấu trúc buổi đổi từ 12 buổi (sách HSK Standard Course) sang
  16 buổi thematic bám New HSK Course 1 3.0 (~300 từ chuẩn 2026 final). 9 buổi mới của 2.0 (vị
  trí 1,2,3,4,5,7,8,9,11 cũ) **không còn khớp** với vị trí 3.0 — coi như phải soạn lại theo bảng
  syllabus mới ở trên; 3 buổi 2.0 đã sản xuất (06/10/12 cũ) giữ làm nguồn tái dùng (xem mục trên),
  KHÔNG đổi tên/xoá.
- **Trang từ vựng HSK1 theo buổi** (`output/study/hsk1/buoiXX/tu-vung.html`, kiểu Quizlet) — làm
  ở phase cuối sau khi vocab 3.0 chốt (spec §10).
- Chỉ nghe được audio nhúng khi mở bằng **PowerPoint thật** (Drive/Google Slides không phát).
