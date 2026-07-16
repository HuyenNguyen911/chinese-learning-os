# Thiết kế: Skill `exercise-generator`

**Ngày:** 2026-07-10
**Trạng thái:** Đã duyệt thiết kế, chờ viết plan
**Liên quan:** teaching-coach (2 giai đoạn, `build_deck.py`), doc-analyzer (bóc đề), learning-strategist

---

## 1. Mục tiêu & Phạm vi

Sinh **bài tập số** cho học viên **HSK1–3** mà mình đang dạy, bám theo từng buổi học
(会/想/能 · lượng từ+一点儿 · 了...). Học viên **làm trực tiếp trên file** (Word/PPTX mở
trên máy hoặc điện thoại), **không in giấy**.

**Trong phạm vi (V1):**
- Skill độc lập `exercise-generator`, anh em với teaching-coach (kiến trúc 2 giai đoạn).
- Đủ 4 kỹ năng theo format thi **HSK** (听/读/书写) và **HSKK** (nói).
- 4 loại bài tập cốt lõi: điền chỗ trống, nối/trắc nghiệm, sắp xếp câu, dịch/đặt câu.
- Ưu tiên rút câu từ **kho đề** (真题/đề mẫu chính thức); thiếu thì sinh theo phong cách 真题 có nhãn.
- Độ khó: đúng cấp + cao hơn 1 bậc (HSK1 → thêm HSK2).
- Output: `.docx` (tương tác chính) + `.pdf` + `.pptx` (tùy chọn) + file đáp án riêng.
- Nghe/nói: sinh **script text trước**; MP3 (edge-tts) **chỉ sau khi user confirm**.
- Cá nhân hóa theo sở thích học viên (tái dùng `interest-personalization.md`).

**Ngoài phạm vi (V1):**
- Thu âm/chấm phát âm học viên tự động.
- Ngân hàng đề lớn tự cào hàng loạt; chấm điểm tự động online.
- Anki/flashcard export (có thể V2).
- HSK4–6 (chỉ khi mở rộng sau).

---

## 2. Kiến trúc

Skill 2 giai đoạn, giống teaching-coach:

- **Giai đoạn A — Soạn bài tập** (vai Master Teacher):
  đọc `buoiX.json` (nội dung buổi do teaching-coach tạo) → ưu tiên rút câu từ
  `knowledge/hsk-exam-bank/` → chỗ thiếu sinh theo phong cách 真题 (gắn nhãn) →
  ra `baitap-buoiX.json` + **script nghe/nói dạng text**.
- **Cổng xác nhận:** trình script nghe/nói cho user duyệt → chờ confirm → mới sinh MP3.
- **Giai đoạn B — Render:** `build_worksheet.py` (JSON → `.docx`) + tái dùng
  `build_deck.py` (→ `.pptx`) + xuất PDF từ docx + file đáp án riêng.

### Cây thư mục

```
.claude/skills/exercise-generator/
  SKILL.md                    # persona + quy trình 2 giai đoạn + format HSK/HSKK
  references/
    hsk-exam-format.md        # cấu trúc từng phần thi HSK1-3 + HSKK 初级
    exercise-types.md         # 4 loại BT + cách chấm + thang điểm
  worksheet/
    build_worksheet.py        # JSON → .docx (renderer mới)
    schema.md                 # schema JSON bài tập
    example-baitap.json       # test fixture, phủ cả 7 block

knowledge/hsk-exam-bank/       # kho đề (seed 1 lần từ nguồn uy tín, lớn dần)
  hsk1.md  hsk2.md  hsk3.md
  sources.md                  # nguồn + ngày tải, truy vết được

output/hskN/baitap/            # .docx / .pdf / .pptx + đáp án + audio/
```

### Routing (thêm vào CLAUDE.md §3)
- Hard route: `/exercise-generator`
- Soft route: "tạo bài tập buổi X" / "bài tập" / "làm đề" / "worksheet" → `exercise-generator`

---

## 3. Loại bài tập & Ánh xạ kỹ năng HSK/HSKK

Mỗi buổi = một worksheet gồm nhiều **block**, phủ đủ 4 kỹ năng.

**读 (Đọc):**
| Block            | Loại BT              | Format thi tương ứng                     |
|------------------|----------------------|------------------------------------------|
| `noi`            | Nối/trắc nghiệm      | HSK 匹配 (chữ–pinyin–nghĩa / câu–ảnh)    |
| `dien_cho_trong` | Điền chỗ trống       | HSK 选词填空 (có word bank)              |
| `doc_hieu`       | Trắc nghiệm          | HSK 阅读理解 (đoạn ngắn + câu hỏi A/B/C) |

**书写 (Viết, HSK3+):**
| Block           | Loại BT        | Format thi                              |
|-----------------|----------------|-----------------------------------------|
| `sap_xep`       | Sắp xếp câu    | HSK 完成句子 (排序)                     |
| `dich_dat_cau`  | Dịch/đặt câu   | Việt→Trung, dùng từ cho trước (hoạt hóa)|

**听 (Nghe):** `nghe` — script text trước → (confirm) → MP3 + QR/nút phát.
Format 听力 HSK cấp đó: 看图/判断对错, 对话选đáp án.

**说 (HSKK 初级):** `noi_hskk` — in câu hỏi + gợi ý; audio mẫu chờ confirm.
听后重复 (nghe & nhắc lại), 回答问题 (trả lời câu hỏi).

**Quy tắc độ khó:** mỗi block ~**70% đúng cấp + 30% cao hơn 1 bậc**; ưu tiên kho đề,
thiếu thì sinh theo phong cách 真题 (nhãn "phỏng theo真题").

**Cá nhân hóa:** tái dùng `interest-personalization.md` của teaching-coach — ví dụ/câu
bám sở thích học viên, tránh câu sáo rỗng.

---

## 4. Luồng dữ liệu

```
buoiX.json (teaching-coach)  ─┐
knowledge/hsk-exam-bank/*.md ─┼─► [A] ─► baitap-buoiX.json + script nghe/nói (text)
memory/interest-personalization ─┘              │
                                    [Cổng confirm] ──┤
                                                     ▼
                        [B] build_worksheet.py
                           ├─► worksheet.docx  (học viên gõ trực tiếp)
                           ├─► worksheet.pdf   (xuất từ docx)
                           ├─► deck.pptx       (build_deck.py, chiếu lớp — tùy chọn)
                           ├─► dapan.docx      (đáp án + 听力文本 + thang điểm)
                           └─► audio/*.mp3     (chỉ sau confirm; QR/nút phát nhúng vào file)
```

---

## 5. Renderer `build_worksheet.py`

Data-driven như `build_deck.py`.
- **Input:** `baitap-buoiX.json` → **output** `.docx` bằng `python-docx` (đã cài sẵn).
- **Design system:** font CJK; ô trống gạch chân/bảng để gõ; khung word-bank; đánh số câu;
  tiêu đề block song ngữ (Trung + Việt).
- **Block types:** `noi`, `dien_cho_trong`, `doc_hieu`, `sap_xep`, `dich_dat_cau`, `nghe`, `noi_hskk`.
- **PDF:** xuất từ docx — docx2pdf (nếu có MS Word) → LibreOffice → fallback báo đường dẫn
  docx để user tự "Save as PDF".
- **Đáp án tách file** `dapan.docx`: đáp án đúng + 听力文本 + gợi ý chấm HSKK + thang điểm.

**Python:** dùng path `C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe`
(nhất quán với build_deck.py).

---

## 6. Audio (sau cổng confirm)

- `edge-tts` → MP3 giọng chuẩn zh-CN. Nhúng link/QR vào docx, nút phát vào pptx.
- Nếu chưa cài edge-tts → skill **dừng**, hướng dẫn cài, **không tự ý** cài.
- Chỉ chạy **sau khi user duyệt script nghe/nói**.

---

## 7. Kho đề & Seed (task 1 lần, có review gate)

Vì user không có sẵn đề: skill có bước **gây dựng kho đề** từ nguồn uy tín.

- **Nguồn ưu tiên (đáng tin, miễn phí/hợp pháp):**
  - `chinesetest.cn` (CTI 官方) — đề mẫu/样卷 chính thức.
  - Đề mẫu Hanban / Viện Khổng Tử công bố công khai.
  - Bộ **HSK Standard Course** (giáo trình đã dùng) — bài tập theo format thi.
- **Không** lấy 真题 sách bản quyền (NXB ĐH Ngôn ngữ Bắc Kinh) từ nguồn lậu.
- **Quy trình:** WebSearch/WebFetch → doc-analyzer bóc → ghi `knowledge/hsk-exam-bank/hskN.md`
  + `sources.md` (nguồn + ngày tải). **Trình user duyệt trước khi lưu.**
- Kho **lớn dần** theo thời gian; câu sinh mới hợp cách cũng có thể được thêm vào (gắn nhãn).

---

## 8. State / Memory

- Skill chỉ **đọc** memory (theo CLAUDE.md §4). User là người duy nhất ghi memory.
- Output ghi vào `output/hskN/baitap/`.
- Ghi 1 dòng log vào `state/session-log.md` (buổi, block, cấp độ) — nhất quán các skill khác.
- Cập nhật CLAUDE.md: §3 routing, §6 state ownership (thêm dòng exercise-generator),
  §7 skill catalog.

---

## 9. Kiểm thử

- `example-baitap.json` phủ **cả 7 block** → chạy `build_worksheet.py` phải ra `.docx`
  mở được, **không lỗi font CJK**.
- File đáp án render đúng, tách biệt worksheet.
- Kho đề seed xong: kiểm ngẫu nhiên vài câu khớp `sources.md`.
- Audio (khi bật): MP3 phát được, QR/link trong docx trỏ đúng file.
- PDF: xuất được hoặc fallback báo đúng đường dẫn docx.

---

## 10. Rủi ro & Quyết định mở

- **PDF trên Windows:** phụ thuộc MS Word/LibreOffice; fallback docx là chấp nhận được V1.
- **Bản quyền đề:** chỉ dùng đề mẫu chính thức + giáo trình; ghi nguồn minh bạch.
- **"Đã từng ra thi":** không đảm bảo 100% là 真题 gốc; nhãn "đề mẫu chính thức" /
  "phỏng theo真题" để minh bạch, không nói dối nguồn.
- **Độ khó cao hơn 1 bậc:** cần `hsk-exam-format.md` mô tả rõ ranh giới cấp để trộn 70/30 đúng.
