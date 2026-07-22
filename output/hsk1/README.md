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
| 03 | Quốc tịch & bản thân | `buoi03_quoctich/` | L3 我是中国人 | "是"字句 · 的 · X是Y · 哪国人 | ⏳ chưa soạn |
| 04 | Gia đình | `buoi04_giadinh/` | L4 我有两个孩子 | "有"字句 · 几口人 · 和 · 都 · 两 vs 二 | ⏳ chưa soạn |
| 05 | Số đếm & số điện thoại | `buoi05_sodem_sodt/` | L6 手机号是多少 | 多少 vs 几 · số lớn · 连动句(1) | ⏳ chưa soạn |
| 06 | Ngày tháng & nghỉ làm | `buoi06_ngaythang/` | L5 今天我休息 | 时间的表达(1) · 名词谓语句 · 能愿动词"会" | ⏳ chưa soạn |
| 07 | Giờ giấc & công việc | `buoi07_giogiac_congviec/` | L7 六点半下班 | 时间的表达(2): 点/分 · 语气助词"吧"(1) | ⏳ chưa soạn |
| 08 | Nghề & nơi làm · 在 | `buoi08_nghe_vitri/` | L8 在医院工作 | 方位词 · 介词"在" · 能愿动词"能" | ⏳ chưa soạn |
| 09 | Nơi chốn & đồ vật · vị trí | `buoi09_noichon_dovat/` | L9 在学校学习 | 存现句(1) · thời gian+nơi chốn làm trạng ngữ · 第 | ⏳ chưa soạn |
| 10 | Mua sắm & giá tiền | `buoi10_muasam/` | L10 苹果真便宜 | 钱数的表达 · 形容词谓语句 · 怎么样 | ⏳ chưa soạn |
| 11 | Ăn uống & gọi món | `buoi11_anuong/` | L13 请给我一杯茶 | 能愿动词"可以" · 动词+一下 · 双宾语句(1) | ⏳ chưa soạn |
| 12 | Sở thích & phim · 了 | `buoi12_sothich_phim/` | L14 看了一个电影 | 动态助词"了(2)" · 离合词(1) · 范围副词"都" | ⏳ chưa soạn |
| 13 | Đại học & đang làm · 呢 | `buoi13_daihoc/` | L11 我读大学呢 | 正反问 · 时间副词"在/正在" · 能愿动词"要" | ⏳ chưa soạn |
| 14 | Thời tiết & sức khỏe | `buoi14_thoitiet_suckhoe/` | L12 昨天下雪了 | 非主谓句 · 语气助词"了(1)" · "太……了" | ⏳ chưa soạn |
| 15 | Đi lại & du lịch · hẹn gặp | `buoi15_dulai_dulich/` | L15 大兴机场见 | 并列复句"……，还/也……" | ⏳ chưa soạn |
| 16 | Ôn tập tổng hợp | `buoi16_ontap/` | — (ôn ~243–300 từ đã học) | Đủ 15 điểm ngữ pháp trọng tâm của 15 bài sách 3.0 (không phải on1/on2 2.0 cũ) | ✅ slide + audio + ảnh xong (chưa có baitap/) |

**15 buổi cần soạn** = vị trí 02–16 (buổi 01 ngữ âm đã xong). Trạng thái vocab: xem checklist
`hsk1-3.0-checklist.md` — 243 từ distinct remap từ 15 课 sách (per-buổi 11–26 từ/buổi), 2 buổi
(08, 11) có block 生词 flag OCR sót cần đối chiếu `raw/新HSK1教程3.0.pdf` khi build.

## Buổi cũ (2.0) tái dùng — không phải buổi mới, chỉ là nguồn nguyên liệu

`buoi06_nangnguyen_phuongtien/`, `buoi10_luongtu_mausac/`, `buoi12_le_thoitiet/` là 3 folder
**đã sản xuất theo syllabus 2.0** (12 buổi, sách HSK Standard Course) — **số buổi của chúng
KHÔNG khớp vị trí 06/10/12 trong bảng 3.0 ở trên**. Theo spec 3.0 §5, đây là nguồn tái dùng có
chọn lọc:
- `buoi06_nangnguyen_phuongtien` (会/想/能, giao thông): fold từ 会/想/能 + giao thông
  (坐/飞机/开车) vào buổi 3.0 mới **08/13/15**.
- `buoi10_luongtu_mausac` (lượng từ, màu sắc): reuse lượng từ **个/本/块** vào buổi 3.0 mới
  **04/10**. Màu sắc (红/蓝…) phần lớn NGOÀI phạm vi 300 từ 3.0 → để "mở rộng", không dạy như
  生词 chính (xem checklist §"Đối chiếu tận dụng buổi cũ").
- `buoi12_le_thoitiet` (了/过, thời tiết): reuse ngữ pháp **了** + thời tiết cơ bản
  (天气/下雨/下雪/冷/热) vào buổi 3.0 mới **14**. Mùa/暖和/凉快/度/晴天/阴天 NGOÀI 300 → "mở rộng".

Nội dung 3 folder cũ KHÔNG bị xoá. Khi build buổi 3.0 tương ứng, copy phần hợp lệ sang folder
mới (`buoi04_giadinh/`, `buoi08_nghe_vitri/`, `buoi10_muasam/`, `buoi13_daihoc/`,
`buoi14_thoitiet_suckhoe/`, `buoi15_dulai_dulich/`) + đánh dấu rõ phần nào là "mở rộng" ngoài
scope 300 từ. `on1_nguphap_dongtu/`, `on2_tuvung_chude/` (2.0) tham khảo khi build buổi 16 ôn
tập, không map 1-1.

## Cấu trúc mỗi buổi

```
buoiXX_<slug>/
  slide/   buoiXX.json + Buoi-XX-*.pptx + assets/ (ảnh, GIF, audio/slideNN.mp3)
  baitap/  baitap-buoiXX.json + hocsinh/{worksheet.docx, audio/} + dapan/dapan.docx
  doc/     课文 sách (bóc từ newhsk1-book-content.md): 汉字+pinyin+dịch + audio edge-tts + footer đối chiếu Hán ngữ Q1
```

Thứ tự block slide: `title → ôn buổi trước → mục tiêu → 生词 → ngữ pháp → 10 câu khẩu ngữ →
hội thoại/课文 → bài đọc → footer Hán ngữ Q1 → lỗi người Việt → preview bài tập`. (Buổi 01 ngữ
âm: không có "10 câu khẩu ngữ", thay bằng luyện âm.)

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
