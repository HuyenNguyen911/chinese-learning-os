# HSK1 — Bộ giáo trình 12 buổi (design spec)

**Ngày:** 2026-07-19
**Trạng thái:** Đã duyệt thiết kế — chờ viết implementation plan
**Chủ sở hữu output:** Teaching Coach (`slide/`), Exercise Generator (`baitap/`)

## 1. Mục tiêu

Hoàn thiện **bộ HSK1 đủ 12 buổi** chất lượng cao, mạch lạc, khẩu ngữ, thông dụng — đủ 150 từ vựng HSK1 + trọn bộ điểm ngữ pháp HSK1, đa dạng chủ đề, dễ hiểu cho người mới bắt đầu từ số 0.

Bắc Kinh của thiết kế (theo yêu cầu user):
- Đủ lượng từ vựng + ngữ pháp, dễ hiểu, đa dạng chủ đề.
- Ví dụ **khẩu ngữ, đời thường, thông dụng** — tránh câu sách vở sáo rỗng.
- 3 buổi nền tảng làm **kỹ**, có **GIF phát âm**.
- Mỗi buổi có **bài đọc trích từ HSK Standard Course 1** (user không có sẵn sách/audio → hệ thống cấp text + audio tự tạo).
- Mỗi buổi có dòng **đối chiếu Giáo trình Hán ngữ Quyển 1** (chỉ list tên bài — user có sẵn sách + audio, dùng để hướng dẫn học viên mở ra đọc/nghe).

## 2. Phạm vi

### Trong phạm vi
- **9 buổi tôi làm** = 3 buổi nền tảng (dựng mới, có GIF) + 6 buổi chủ đề mới.
- Mỗi buổi giao **trọn gói**: slide `.pptx` (+ audio) · bài tập worksheet + audio + đáp án · bài đọc HSK SC1 (text + audio) · dòng đối chiếu Hán ngữ Q1.
- **Trang từ vựng HSK1 theo buổi** (vocab-study-style, kiểu Quizlet) — mỗi buổi 1 trang `output/study/hsk1/buoiXX/tu-vung.html`. Làm ở **phase cuối** (mục 14).
- 1 file syllabus tổng `output/hsk1/README.md` (bảng thứ tự dạy, source of truth).

### Ngoài phạm vi (không tái soạn nội dung)
- **Nội dung dạy** của buổi 1/2/3 hiện có — giữ nguyên. Chỉ **đổi tên folder + nhãn số** theo syllabus (mục 11), không viết lại bài giảng.
- Ôn 1 (`on1_nguphap_dongtu`), Ôn 2 (`on2_tuvung_chude`) — giữ nguyên.
- 3 file raw `.pptx` (`NHẬP MÔN`, `CHỦ ĐỀ 1`, `CHỦ ĐỀ 2`) — chỉ đọc tham khảo để tránh trùng, KHÔNG sửa. (Các buổi nền tảng mới dựng lại nội dung này ở định dạng vault, có GIF, không phụ thuộc file raw.)

## 3. Reconcile "12 buổi"

**12 buổi content = 9 (tôi làm) + 3 (đã có).** Ngoài ra 2 buổi ôn (đã có) là checkpoint. Tổng tài liệu = 12 content + 2 ôn.

- 9 tôi làm: vị trí syllabus **1, 2, 3, 4, 5, 7, 8, 9, 11**.
- 3 đã có (đổi tên theo syllabus): `buoi06` (会/想/能), `buoi10` (lượng từ/màu), `buoi12` (thời tiết).

## 4. Master syllabus (thứ tự dạy hợp lý)

Tiến trình sư phạm: nền tảng → nhận diện người/danh tính → động từ năng nguyện → đời sống hằng ngày → lượng từ/màu → mua sắm → thể/thời (khó nhất để cuối).

| # | Buổi | Nguồn | Ngữ pháp trọng tâm | Bài đọc HSK SC1 | Đối chiếu Hán ngữ Q1 |
|---|---|---|---|---|---|
| 1 | Ngữ âm: pinyin · thanh điệu · thanh/vận mẫu | MỚI · nền tảng | hệ thống ngữ âm, thanh điệu, 变调 (三声/一/不) | — | Bài 1–5 (ngữ âm) |
| 2 | Đại từ · chào hỏi · làm quen | MỚI · nền tảng | 是 · 吗 · 呢 · 叫…名字 · 很高兴认识你 | L1 你好 · L2 谢谢你 · L3 你叫什么名字 | Bài 1, 3, 5 |
| 3 | Số đếm · thời gian · ngày tháng · địa điểm · phương hướng | MỚI · nền tảng | 几点 · 号/月/星期 · 这儿/那儿/哪儿 · 在 | L7 今天几号 · L11 现在几点 | Bài 8 |
| 4 | Gia đình & tuổi | MỚI | 有/没有 · 几口人 · 和 · 都 · 多大/几岁 | L5 她女儿今年二十岁 | Q1 Hạ (gia đình) |
| 5 | Nghề nghiệp · quốc tịch · ngôn ngữ | MỚI | 是 (X是Y) · 说+ngôn ngữ · 哪国人 | L4 她是我的汉语老师 · L6 我会说汉语 · L9 你儿子在哪儿工作 | Bài 6, 11, 12 |
| 6 | 会/想/能 — Hoạt động & giao thông | ĐÃ CÓ (buoi06) | 会/想/能/要/可以 | L6 我会说汉语 · L10 我能坐这儿吗 | Bài 10 |
| 7 | Ăn uống | MỚI | 想/要+V · 吃饭了吗 · 好吃/好喝 | L8 我想喝茶 | Bài 7 |
| 8 | Nhà · đồ vật · vị trí 在…里/上 | MỚI | 在 (tồn tại) · …里/…上 · 前面/后面 | L9 你儿子在哪儿工作 | Bài 10, 12 |
| 9 | Sở thích & động từ | MỚI | 喜欢+V · 爱 · (ôn 会/想) | L13 他在学做中国菜 | Q1 Hạ (sở thích) |
| 10 | Lượng từ + 一点儿 · Màu sắc | ĐÃ CÓ (buoi10) | 量词 · 一点儿/有点儿 | L14 她买了不少东西 | Bài 14 |
| 11 | Mua sắm · tiền · tính từ mô tả | MỚI | 多少钱 · 太…了 · 买 · 很+Adj · 不 · số lớn | L14 她买了不少东西 · L15 我在这儿买的 | Bài 8, 9, 15 |
| 12 | 了/没/过/快…了 — Thời tiết | ĐÃ CÓ (buoi12) | 了/没/过/快…了 | L12 明天天气怎么样 | Q1 Hạ (thời tiết) |
| Ôn 1 | Ngữ pháp · động từ · cấu trúc câu | ĐÃ CÓ | — | — | — |
| Ôn 2 | Từ vựng theo cụm chủ đề | ĐÃ CÓ | — | — | — |

**Ghi chú phủ từ vựng:** Nền tảng (buổi 1–3) phủ đại từ/chào hỏi/số/thời gian/địa điểm; buổi 4–5 phủ người/danh tính; buổi 7–9 phủ đời sống; buổi 11 phủ mua sắm/tính từ. Cùng existing buoi1/2/3 (năng nguyện/lượng từ-màu/thể-thời tiết) → đủ 150 từ HSK1. Danh sách 150 từ chính thức sẽ được đối chiếu chi tiết ở bước implementation để đảm bảo không sót/không trùng.

## 5. Chi tiết 9 buổi mới (từ vựng lõi + ngữ pháp)

Mỗi buổi 8–12 từ mới (đúng nhịp người mới). Danh sách dưới là **lõi**; bước implementation chốt chính xác theo danh sách 150 từ HSK1.

- **Buổi 1 — Ngữ âm:** 声母/韵母/声调, 拼音 quy tắc, 变调 (三声连读, 一/不 biến điệu), 轻声, 儿化. Không tính từ vựng HSK. GIF: đường cong 5 mức thanh điệu, khẩu hình âm khó (zh/ch/sh/r, j/q/x, ü, e), thứ tự nét vài chữ cơ bản (一二三人口).
- **Buổi 2 — Đại từ, chào hỏi, làm quen:** 你好, 谢谢, 不客气, 再见, 对不起, 没关系, 我/你/他/她, 们, 是, 叫, 名字, 什么, 认识, 高兴, 请, 老师, 学生, 吗, 呢. GIF: thứ tự nét 你好我是.
- **Buổi 3 — Số/thời gian/địa điểm:** 一~十, 零, 百, 几, 点, 分, 号, 月, 星期, 年, 今天, 明天, 昨天, 现在, 上午, 下午, 中午, 这儿, 那儿, 哪儿, 在. GIF: thứ tự nét chữ số.
- **Buổi 4 — Gia đình & tuổi:** 家, 爸爸, 妈妈, 儿子, 女儿, 口, 有, 没有, 和, 都, 岁, 多大.
- **Buổi 5 — Nghề/quốc tịch/ngôn ngữ:** 中国, 中国人, 医生, 工作, 学习, 说, 汉语, 字, 人, 哪, 是, 谁.
- **Buổi 7 — Ăn uống:** 吃, 喝, 饭, 米饭, 菜, 水, 茶, 水果, 苹果, 东西, 好吃.
- **Buổi 8 — Nhà/đồ vật/vị trí:** 桌子, 椅子, 电视, 电脑, 书, 在, 里, 上, 家, 前面, 后面.
- **Buổi 9 — Sở thích & động từ:** 喜欢, 看, 书, 电影, 听, 读, 写, 爱, 学习, 唱歌.
- **Buổi 11 — Mua sắm/tiền/tính từ:** 买, 钱, 块, 多少, 太, 大, 小, 多, 少, 好, 漂亮, 很, 不, 商店. Capstone hội thoại tổng hợp.

## 6. Cấu trúc deliverable mỗi buổi

```
output/hsk1/buoiXX_<slug>/
  slide/
    buoiXX.json            # teaching-coach schema
    Buoi-XX-....pptx        # render từ build_deck.py
    buoiXX-images.json      # query fetch ảnh (nếu dùng)
    assets/                 # ảnh, GIF, audio slide
  baitap/
    baitap-buoiXX.json      # exercise-generator
    hocsinh/
      worksheet.docx
      audio/                # nghe-*.mp3, hskk-*.mp3
    dapan/
      dapan.docx
  doc/
    bai-doc-hsksc1.md       # 课文 HSK SC1: hán + pinyin + dịch + link audio
    bai-doc-hsksc1.<n>.mp3  # audio tự tạo (edge-tts)
```

Khối JSON slide theo thứ tự:
`title` → `ôn buổi trước` (bullets) → `muctieu` (bullets) → `生词` (vocab, chia nhóm) → `ngữ pháp` (grammar/table) → **`10 câu khẩu ngữ thông dụng`** (10 câu dùng-được-ngay, khẩu ngữ đời thường; hán + pinyin + dịch) → `hội thoại / 课文` (dialogue) → `bài đọc` (reading HSK SC1) → **footer đối chiếu Hán ngữ Q1** → **slide lỗi người Việt hay mắc** (từ `common-vietnamese-mistakes.md`) → preview bài tập (exercise) → Done.

Foundation thêm slide **GIF** (image key trỏ `.gif` trong `assets/`). Riêng buổi 1 (ngữ âm) không có block "10 câu khẩu ngữ" — thay bằng luyện âm; các buổi còn lại đều có.

## 7. GIF phát âm (buổi nền tảng)

- **Định dạng:** GIF động **nhúng thẳng trong pptx** (PowerPoint phát khi trình chiếu). Không làm trang HTML riêng.
- **Nguồn:**
  - Thanh điệu (đường cong 5 mức) — **tự sinh** (matplotlib/PIL → GIF).
  - Thứ tự nét chữ Hán — **tự sinh** từ dữ liệu nét mở (vd Make Me a Hanzi / hanzi-writer stroke data).
  - Khẩu hình (môi/lưỡi) âm khó — **web-search GIF** + **cổng duyệt bản quyền/nguồn** trước khi nhúng; nếu không có nguồn dùng được → fallback sơ đồ tĩnh + audio.
- **Kiểm tra:** GIF nhúng phải phát được khi mở slideshow trên máy user (verify ở pilot buổi 1).

## 8. Bài đọc HSK Standard Course 1

- Mỗi buổi trích **課文** HSK SC1 tương ứng (bảng mục 4). Nhiều bài đọc/buổi khi cùng chủ điểm.
- Định dạng: chữ Hán + pinyin + dịch Việt.
- **Audio:** tự tạo bằng edge-tts (đọc chậm `-18%`, hội thoại đa giọng), soát 多音字/儿化 trước khi giao.
- **Sourcing gate:** web-search đối chiếu bản gốc HSK SC1 trước khi chốt text (giáo trình xuất bản — phải đúng nguyên văn). Không bịa nội dung 课文.

## 9. Đối chiếu Giáo trình Hán ngữ Quyển 1

- Chỉ **list tên bài** (số + tên Hán + nghĩa) ở footer slide + trong `README.md`. User có sách + audio Hán ngữ → tự hướng dẫn học viên mở đọc/nghe.
- Nguồn mapping: `references/giao-trinh-han-ngu.md` (Tập 1 Quyển Thượng 15 bài).

## 10. Pipeline sản xuất mỗi buổi (có cổng duyệt)

1. **Master Teacher** (teaching-coach Giai đoạn A): nội dung đúng-đủ — từ vựng, ngữ pháp giải thích bản chất, ví dụ khẩu ngữ đời thường, dự đoán lỗi người Việt.
2. **Nguồn 课文 HSK SC1**: web-search đối chiếu → **cổng duyệt text**.
3. **Experience Designer** (Giai đoạn B): map nội dung → `buoiXX.json` (chia block, action title, ghost-deck test).
4. **Assets**: fetch ảnh · sinh/tìm GIF · edge-tts audio → **soát phát âm 多音字/儿化 trước khi giao**.
5. **Render pptx**: `build_deck.py`.
6. **Bài tập**: exercise-generator (worksheet + audio + đáp án) → **cổng kiểm tra đáp án AI**; audio qua cổng xác nhận.

> **Không nạp `tier-a.md` / vocab-study.** `tier-a.md` là vocabulary activation **cá nhân của user (HSK6)** do Learning Strategist/Lesson Prep quản lý — không phải kho từ HSK1 dạy học viên. `vocab-study` là luồng HSK6 (đọc `raw/Từ vựng.xlsx`, neo Activation vault của user) — không áp cho tài liệu HSK1. Từ vựng HSK1 của mỗi buổi đã nằm trong slide `生词` + bài tập; không cần đường nạp riêng.

## 11. Đặt tên & syllabus index

- **Tất cả 12 buổi đánh số 2 chữ số theo vị trí syllabus** — đồng nhất `buoi01` … `buoi12`.
- Folder mới: `buoi01_nguam`, `buoi02_daitu_chaohoi`, `buoi03_so_thoigian_diadiem`, `buoi04_giadinh`, `buoi05_nghe_quoctich`, `buoi07_anuong`, `buoi08_nha_vitri`, `buoi09_sothich`, `buoi11_muasam_tinhtu`.
- **Existing đổi tên** (git mv) theo vị trí syllabus:
  - `buoi1_nangnguyen_phuongtien` → `buoi06_nangnguyen_phuongtien`
  - `buoi2_luongtu_mausac` → `buoi10_luongtu_mausac`
  - `buoi3_le_thoitiet` → `buoi12_le_thoitiet`
- Khi đổi tên existing: cũng đổi tên file `buoiX.json`/`.pptx` bên trong + cập nhật nhãn `meta.lesson` ("HSK1 · Buổi 6/10/12") cho khớp. **Không tái soạn nội dung dạy** (block "ôn buổi trước" cũ có thể lệch mạch — chấp nhận như artifact, không viết lại). Grep toàn repo tìm tham chiếu đường dẫn cũ (state, memory, docs) và cập nhật.
- Ôn 1/Ôn 2 (`on1_nguphap_dongtu`, `on2_tuvung_chude`) giữ nguyên tên, nằm sau buổi 12.
- `output/hsk1/README.md` = bảng syllabus 12 buổi + 2 ôn, map vị trí ↔ folder, là source of truth về thứ tự dạy. Trong `meta.lesson` của các JSON mới ghi đúng vị trí syllabus (vd "HSK1 · Buổi 4").

## 12. Chiến lược giao (de-risk)

- **2 pilot trước (theo yêu cầu user):**
  - `buoi01_nguam` (ngữ âm + GIF) — chốt khuôn nền tảng + verify GIF phát trong pptx.
  - `buoi02_daitu_chaohoi` (đại từ · chào hỏi · làm quen) — chốt khuôn buổi có 生词/hội thoại/课文/10 câu khẩu ngữ/bài tập (trọn gói).
- User duyệt 2 pilot → sản xuất 7 buổi còn lại theo khuôn, **giao theo lô + review**.
- Thứ tự sản xuất còn lại: theo syllabus (3 → 4 → 5 → 7 → 8 → 9 → 11).
- Việc **đổi tên existing** buoi1/2/3 (mục 11) làm 1 lần ở đầu (trước hoặc cùng lô pilot) để `README.md` syllabus khớp ngay.
- **Phase cuối:** sinh trang từ vựng theo buổi (mục 14) sau khi vocab tất cả các buổi đã chốt.

## 13. Tiêu chí hoàn thành (verification)

- [ ] 9 buổi đủ deliverable (slide pptx + audio, baitap 3 phần, bài đọc HSK SC1 + audio, footer Hán ngữ Q1).
- [ ] Mỗi buổi (trừ buổi ngữ âm) có block **10 câu khẩu ngữ thông dụng**.
- [ ] Existing buoi1/2/3 đã đổi tên `buoi06/buoi10/buoi12` (folder + file + nhãn), grep tham chiếu cũ đã cập nhật.
- [ ] Tổng từ vựng 9 buổi mới + 3 existing = phủ đủ 150 từ HSK1 (đối chiếu danh sách chính thức), không trùng lặp giữa các buổi.
- [ ] Mỗi pptx render thành công, mở được, GIF phát trong slideshow (buổi nền tảng).
- [ ] Audio soát 多音字/儿化, đọc chậm đúng chuẩn HSK1-3.
- [ ] 课文 HSK SC1 đối chiếu đúng bản gốc (web-search verified).
- [ ] Bài tập qua cổng kiểm tra đáp án AI.
- [ ] `README.md` syllabus đầy đủ, khớp folder.
- [ ] Trang từ vựng theo buổi `output/study/hsk1/buoiXX/tu-vung.html` sinh đủ, flashcard + 🔊 chạy được (không phụ thuộc Activation vault).

## 14. Trang từ vựng HSK1 theo buổi (vocab-study-style)

- **Phạm vi:** mỗi buổi (có 生词) 1 trang `output/study/hsk1/buoiXX/tu-vung.html` tự chứa, kiểu Quizlet — giống bản HSK6 nhưng cho từ vựng buổi đó.
- **Tái dùng** engine của vocab-study: bảng 生词 (+ 生词拓展 nếu có), flashcard active-recall + Leitner, chiết tự + mẹo nhớ tiếng Việt, phát âm 🔊.
- **Khác bản HSK6:** **bỏ phần neo Activation từ vault** (`knowledge/vocabulary` là dữ liệu HSK6 cá nhân của user, không áp cho từ HSK1 dạy học viên) → Leitner khởi động trung tính (box 1). KHÔNG đọc `raw/Từ vựng.xlsx` — nguồn từ vựng là `生词` của buổi (đã chốt trong `buoiXX.json`).
- **Thời điểm:** **phase cuối**, sau khi vocab các buổi đã chốt (tránh làm lại nếu vocab đổi trong lúc sản xuất). Sinh loạt cho tất cả các buổi (kể cả buổi existing 06/10/12 nếu muốn đồng bộ — xác nhận ở plan).

## 15. Rủi ro & mở

- **GIF khẩu hình bản quyền**: nếu không tìm được nguồn dùng được → fallback sơ đồ tĩnh + audio (không chặn tiến độ).
- **Nguyên văn 课文 HSK SC1**: phải verify; nếu web-search không cho bản đáng tin → xác nhận với user cách xử lý (paraphrase có ghi chú vs. bỏ bài đọc buổi đó).
- **Danh sách 150 từ HSK1**: chốt ở đầu implementation, dùng làm checklist phủ từ.
