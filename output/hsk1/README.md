# HSK1 — Bộ giáo trình 12 buổi (syllabus · source of truth)

Thứ tự **dạy** hợp lý cho bộ HSK1. Số buổi = vị trí syllabus = prefix folder (`buoi01`…`buoi12`).
Chi tiết thiết kế: `docs/superpowers/specs/2026-07-19-hsk1-full-course-design.md`.
Checklist phủ 150 từ: `docs/superpowers/plans/hsk1-150-checklist.md`.

## Syllabus

| # | Buổi | Folder | Nguồn | Ngữ pháp trọng tâm | Bài đọc HSK SC1 | Hán ngữ Q1 | TT |
|---|---|---|---|---|---|---|---|
| 1 | Ngữ âm: pinyin · thanh điệu · thanh/vận mẫu | `buoi01_nguam/` | MỚI · nền tảng | hệ thống ngữ âm, thanh điệu, 变调 | — | Bài 1–5 (ngữ âm) | ⏳ |
| 2 | Đại từ · chào hỏi · làm quen | `buoi02_daitu_chaohoi/` | MỚI · nền tảng | 是 · 吗 · 呢 · 叫…名字 · 很高兴认识你 | L1 你好 · L2 谢谢你 · L3 你叫什么名字 | Bài 1,3,5 | ⏳ |
| 3 | Số đếm · thời gian · ngày tháng · địa điểm · phương hướng | `buoi03_so_thoigian_diadiem/` | MỚI · nền tảng | 几点 · 号/月/星期 · 这儿/那儿/哪儿 · 在 | L7 今天几号 · L11 现在几点 | Bài 8 | ⏳ |
| 4 | Gia đình & tuổi | `buoi04_giadinh/` | MỚI | 有/没有 · 几口人 · 和 · 都 · 多大/几岁 | L5 她女儿今年二十岁 | Q1 Hạ (gia đình) | ⏳ |
| 5 | Nghề nghiệp · quốc tịch · ngôn ngữ | `buoi05_nghe_quoctich/` | MỚI | 是 (X是Y) · 说+ngôn ngữ · 哪国人 | L4 她是我的汉语老师 · L6 我会说汉语 · L9 你儿子在哪儿工作 | Bài 6,11,12 | ⏳ |
| 6 | 会/想/能 — Hoạt động & giao thông | `buoi06_nangnguyen_phuongtien/` | ĐÃ CÓ | 会/想/能/要/可以 | L6 我会说汉语 · L10 我能坐这儿吗 | Bài 10 | ✅ |
| 7 | Ăn uống | `buoi07_anuong/` | MỚI | 想/要+V · 吃饭了吗 · 好吃/好喝 | L8 我想喝茶 | Bài 7 | ⏳ |
| 8 | Nhà · đồ vật · vị trí 在…里/上 | `buoi08_nha_vitri/` | MỚI | 在 (tồn tại) · …里/…上 · 前面/后面 | L9 你儿子在哪儿工作 | Bài 10,12 | ⏳ |
| 9 | Sở thích & động từ | `buoi09_sothich/` | MỚI | 喜欢+V · 爱 · (ôn 会/想) | L13 他在学做中国菜 | Q1 Hạ (sở thích) | ⏳ |
| 10 | Lượng từ + 一点儿 · Màu sắc | `buoi10_luongtu_mausac/` | ĐÃ CÓ | 量词 · 一点儿/有点儿 | L14 她买了不少东西 | Bài 14 | ✅ |
| 11 | Mua sắm · tiền · tính từ mô tả | `buoi11_muasam_tinhtu/` | MỚI | 多少钱 · 太…了 · 买 · 很+Adj · 不 · số lớn | L14 她买了不少东西 · L15 我在这儿买的 | Bài 8,9,15 | ⏳ |
| 12 | 了/没/过/快…了 — Thời tiết | `buoi12_le_thoitiet/` | ĐÃ CÓ | 了/没/过/快…了 | L12 明天天气怎么样 | Q1 Hạ (thời tiết) | ✅ |
| Ôn 1 | Ngữ pháp · động từ · cấu trúc câu | `on1_nguphap_dongtu/` | ĐÃ CÓ | — | — | — | ✅ |
| Ôn 2 | Từ vựng theo cụm chủ đề | `on2_tuvung_chude/` | ĐÃ CÓ | — | — | — | ✅ |

TT: ✅ đã có / ⏳ chưa soạn. **9 buổi cần soạn** = vị trí 1,2,3,4,5,7,8,9,11.

## Cấu trúc mỗi buổi

```
buoiXX_<slug>/
  slide/   buoiXX.json + Buoi-XX-*.pptx + assets/ (ảnh, GIF, audio/slideNN.mp3)
  baitap/  baitap-buoiXX.json + hocsinh/{worksheet.docx, audio/} + dapan/dapan.docx
  doc/     bai-doc-hsksc1.md (课文 HSK SC1: hán+pinyin+dịch) + *.mp3 (edge-tts)
```

Thứ tự block slide: `title → ôn buổi trước → mục tiêu → 生词 → ngữ pháp → 10 câu khẩu ngữ → hội thoại/课文 → bài đọc → footer Hán ngữ Q1 → lỗi người Việt → preview bài tập`. (Buổi 1 ngữ âm: không có "10 câu khẩu ngữ", thay bằng luyện âm.)

## Ghi chú kỹ thuật

- **GIF phát âm (buổi nền tảng):** đã xác nhận GIF động **nhúng thẳng trong `.pptx` PHÁT ĐỘNG** khi trình chiếu PowerPoint desktop (Task 0.2, user verified). Chốt phương án embed (không dùng fallback sprite). Sinh GIF: `scripts/hsk1/gen_tone_gif.py` (thanh điệu), `scripts/hsk1/gen_stroke_gif.py` (thứ tự nét, nguồn Make Me a Hanzi).
- **Đổi tên:** buổi 1/2/3 cũ đã đổi → 06/10/12 (git mv per-file do dir bị Windows lock). Nội dung dạy giữ nguyên, chỉ đổi số + nhãn.
- **Trang từ vựng HSK1 theo buổi** (`output/study/hsk1/buoiXX/tu-vung.html`, kiểu Quizlet) — làm ở phase cuối, plan riêng (spec §14).
- Chỉ nghe được audio nhúng khi mở bằng **PowerPoint thật** (Drive/Google Slides không phát).
