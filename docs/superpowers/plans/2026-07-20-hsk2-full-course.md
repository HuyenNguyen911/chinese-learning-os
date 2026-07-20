# HSK2 (chuẩn 3.0) Full Course Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây bộ HSK2 chuẩn **3.0** — 16 buổi nội dung + 2 ôn, trọn gói slide/audio/bài tập(có Viết 3.0)/bài đọc, bám sách chính **New HSK Course 2**, tham khảo **Hán ngữ Q2**, không trùng từ HSK1.

**Architecture:** Pipeline nội dung dựa trên tooling có sẵn của vault (teaching-coach, exercise-generator, edge-tts). Mỗi buổi = 1 folder `output/hsk2/buoiXX_<slug>/` với `slide/` · `baitap/` · `doc/`. Quy trình mỗi buổi giống nhau (Procedure P) — chỉ khác dữ liệu. Làm 2 pilot trước (buổi 02 比 · buổi 05 得) để chốt khuôn, rồi nhân bản theo lô.

**Tech Stack:** Python 3.12 (python-pptx, Pillow, pypinyin, python-docx), edge-tts, build_deck.py / slide_audio.py / fetch_images.py (teaching-coach), build_worksheet.py / check_baitap.py (exercise-generator), gen_stroke_gif.py (tuỳ chọn, tái dùng HSK1).

**Spec:** `docs/superpowers/specs/2026-07-20-hsk2-full-course-design.md` — nguồn chân lý về chuẩn 3.0 (§2), syllabus 16 buổi (§4), vocab lõi (§5), cấu trúc slide (§6), nguồn 課文 (§7), Hán ngữ Q2 (§8), pipeline (§9), đặt tên (§10).

## Global Constraints

- **Python:** `PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"`. Chạy mọi lệnh **từ gốc repo** `c:/Tài liệu/ai-vault/CHINESE`.
- **Chuẩn 3.0:** vocab/ngữ pháp bám **词汇表/语法表 3.0 + New HSK Course 2**. Số vận hành: ~200 từ mới + mở rộng, 45 điểm ngữ pháp.
- **Đánh số:** tất cả buổi prefix 2 chữ số `buoiXX` (§10 spec). Ôn: `on1_nguphap_1-8`, `on2_nguphap_9-16`.
- **CHỐNG TRÙNG HSK1 (ràng buộc cứng):** mọi 生词 phải KHÔNG nằm trong 150 từ HSK1 (đối chiếu Task 0.1). Từ trùng chỉ dùng lại trong câu ví dụ, không tính là từ mới.
- **Mọi từ/câu tiếng Trung mới** phải có đủ **汉字 + pinyin + nghĩa Việt**.
- **Lượng từ mới:** ~12–15 từ/buổi (nhịp HSK2, học viên đã qua HSK1).
- **Thứ tự block slide (§6 spec):** `title → ôn buổi trước → mục tiêu → 生词 → ngữ pháp → 10 câu khẩu ngữ → hội thoại/課文 → bài đọc → footer Hán ngữ Q2 → lỗi người Việt → preview bài tập`. KHÔNG có block ngữ âm.
- **Bài tập đủ 4 phần 3.0:** 听 (nghe) · 读 (đọc) · **书写/Viết** (sắp câu, điền chữ, viết câu ngắn) · HSKK (nói). Phần Viết là điểm mới bắt buộc.
- **Audio đọc chậm:** slide `slide_audio.py --rate=-18%`; baitap `nghe` `--rate=-22%` (nhanh hơn HSK1 chút vì trình độ cao hơn), `noi_hskk` `--rate=-18%`. Giọng chính `zh-CN-XiaoxiaoNeural`.
- **Cổng duyệt bắt buộc:** (a) text 課文 web-search đối chiếu New HSK Course 2 (hoặc tự soạn có ghi chú) trước khi dùng; (b) script 听力/HSKK trình user trước khi sinh MP3; (c) đáp án bài tập `check_baitap.py` + rà AI trước khi giao; (d) soát 多音字/儿化 mọi audio.
- **Console Windows:** khi in 中文 debug, đặt `PYTHONIOENCODING=utf-8`.
- **Git:** commit sau mỗi task, message tiếng Việt + trailer `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

---

## File Structure

```
output/hsk2/
  README.md                          # [Task 0.3] bảng syllabus 16 buổi + 2 ôn (source of truth, ghi rõ chuẩn 3.0)
  buoiXX_<slug>/                      # mỗi buổi:
    slide/
      buoiXX.json                     # JSON teaching-coach
      buoiXX-images.json              # manifest fetch ảnh
      Buoi-XX-<Ten>.pptx              # render
      assets/                         # *.jpg (fetch), *.gif (nét, tuỳ chọn), audio/slideNN.mp3
    baitap/
      baitap-buoiXX.json              # JSON exercise-generator (có phần Viết 3.0)
      hocsinh/worksheet.docx + audio/*.mp3
      dapan/dapan.docx
    doc/
      bai-doc.md                      # 課文: hán+pinyin+dịch (nguyên văn New HSK Course 2 hoặc tự soạn có ghi chú)
      bai-doc.NN.mp3                  # audio edge-tts
docs/superpowers/plans/hsk2-vocab-grammar-checklist.md   # [Task 0.1] checklist phủ từ 3.0 + chống trùng HSK1
```

Vocab-study phase (§13 spec) **tách plan riêng** — xem "Out of scope / follow-up".

---

## PHASE 0 — Infrastructure

### Task 0.1: Checklist vocab 3.0 + chống trùng HSK1

**Files:**
- Create: `docs/superpowers/plans/hsk2-vocab-grammar-checklist.md`

**Interfaces:**
- Produces: (1) bảng từ HSK2 3.0 ↔ buổi phụ trách; (2) danh sách 150 từ HSK1 để đối chiếu loại trùng; (3) bảng 45 điểm ngữ pháp ↔ buổi.

- [ ] **Step 1: Lấy danh sách từ + ngữ pháp HSK2 3.0**

WebSearch/WebFetch **词汇表 3.0 cấp 2** + mục lục **New HSK Course 2** (200 từ mới + mở rộng) + **语法表 3.0 cấp 2** (45 điểm). Đối chiếu ≥2 nguồn (fltrp/newhskcourse.com, mandarinbean new-hsk-2, hskstory syllabus). Nếu user có PDF sách → bóc bằng doc-analyzer (chính xác hơn).

- [ ] **Step 2: Trích 150 từ HSK1 để loại trùng**

```bash
grep -ho '"hz": *"[^"]*"' output/hsk1/*/slide/*.json | sort -u
```
Expected: tập 汉字 HSK1 đã dạy → dùng làm bộ lọc chống trùng.

- [ ] **Step 3: Viết checklist**

Bảng vocab: `汉字 | pinyin | nghĩa | buổi phụ trách (§4/§5) | trùng HSK1? | trạng thái`. Từ trùng HSK1 → đánh dấu, loại khỏi 生词 (chỉ dùng ôn trong câu). Bảng ngữ pháp: `điểm ngữ pháp | buổi phụ trách | nhóm (1 trong 6 nhóm mới)`.

- [ ] **Step 4: Verify — phủ đủ, không trùng HSK1, không trùng giữa buổi**

Mọi từ 3.0 có buổi phụ trách; không từ nào trùng 150 HSK1 lọt vào cột 生词; 45 điểm ngữ pháp đều có buổi. Lệch → chỉnh phân bổ trong plan + ghi chú.

- [ ] **Step 5: Commit**
```bash
git add docs/superpowers/plans/hsk2-vocab-grammar-checklist.md
git commit -m "docs(hsk2): checklist vocab 3.0 + chống trùng HSK1 + map 45 ngữ pháp"
```

### Task 0.2: Đánh giá schema Viết (书写) 3.0 trong exercise-generator

**Files:**
- Read: `.claude/skills/exercise-generator/worksheet/schema.md`, `build_worksheet.py`

**Interfaces:**
- Produces: kết luận exercise-generator có hỗ trợ dạng mục "Viết câu / sắp xếp câu / điền chữ Hán" chưa; nếu chưa → phương án (dùng dạng mục gần nhất vs mở rộng schema).

- [ ] **Step 1: Rà schema hiện có**

Đọc schema exercise-generator — liệt kê các dạng mục hỗ trợ (听/读/书写/HSKK). Xác định dạng nào dùng được cho Viết 3.0 (sắp xếp câu 连词成句, điền chữ Hán, viết câu theo mẫu/tranh).

- [ ] **Step 2: Kết luận + quyết định**

- Nếu schema đã đủ (có dạng sắp xếp câu/điền) → ghi mapping dạng mục → phần Viết. KHÔNG sửa skill.
- Nếu thiếu → **cổng duyệt user**: đề xuất bổ sung dạng mục (qua close-session hoặc chỉnh schema exercise-generator có duyệt). Ghi quyết định vào README kỹ thuật.

- [ ] **Step 3: Commit (nếu có ghi chú)**
```bash
git add output/hsk2/README.md
git commit -m "docs(hsk2): kết luận schema Viết 3.0 cho exercise-generator"
```

### Task 0.3: README syllabus (source of truth)

**Files:**
- Create: `output/hsk2/README.md`

- [ ] **Step 1: Viết bảng syllabus 16 buổi + 2 ôn**

Copy bảng §4 spec: cột `# | Buổi | Folder | Ngữ pháp | Chủ đề 3.0 | New HSK Course 2 (bài) | Hán ngữ Q2`. Header ghi rõ: **chuẩn 3.0**, sách chính New HSK Course 2, tham khảo Hán ngữ Q2. Mục "Ghi chú kỹ thuật" (kết luận schema Viết Task 0.2, quyết định GIF nét). Buổi chưa làm đánh dấu "⏳".

- [ ] **Step 2: Verify** — mỗi dòng buổi trỏ folder đúng convention; ôn 1 sau buổi 8, ôn 2 sau buổi 16.

- [ ] **Step 3: Commit**
```bash
git add output/hsk2/README.md
git commit -m "docs(hsk2): README syllabus 16 buổi + 2 ôn (source of truth, chuẩn 3.0)"
```

---

## PROCEDURE P — Quy trình sản xuất 1 buổi (dùng lại cho mọi task buổi)

> Mỗi task buổi cung cấp **Param** rồi chạy P1–P9. Lệnh giống nhau, chỉ khác đường dẫn theo `SLUG`/`XX`.

**Param mỗi buổi:** `XX` (số 2 chữ số); `SLUG`; `DIR=output/hsk2/buoiXX_SLUG`; danh sách **生词** (§5, đã lọc trùng HSK1) + nhóm; **điểm ngữ pháp** (§4); **課文** New HSK Course 2 bài tương ứng; **dòng Hán ngữ Q2**; ghi chú lỗi người Việt.

**P1 — Master Teacher (nội dung):** Đóng vai Master Chinese Teacher (teaching-coach Giai đoạn A). Soạn: giải thích ngữ pháp đúng bản chất; ~12–15 生词 (đủ 汉字/pinyin/nghĩa, **đã đối chiếu checklist Task 0.1 — không trùng HSK1, không lấn buổi khác**); ví dụ khẩu ngữ đời thường; **10 câu khẩu ngữ thông dụng** dùng-ngay; hội thoại mẫu; 2–3 lỗi người Việt (đọc `.claude/skills/teaching-coach/references/common-vietnamese-mistakes.md`).

**P2 — Nguồn 課文 (cổng duyệt a):** WebSearch/WebFetch text 課文 New HSK Course 2 bài được giao. ≥1 nguồn tin cậy → dùng nguyên văn, ghi nguồn. Không tìm được → **tự soạn** đoạn đọc/hội thoại bám 生词+ngữ pháp, **đánh dấu rõ "tự soạn, không phải nguyên văn sách"**. **Trình user duyệt text** trước khi ghi `DIR/doc/bai-doc.md` (汉字+pinyin+dịch).

**P3 — Experience Designer (JSON slide):** Map P1+P2 → `DIR/slide/buoiXX.json` theo schema teaching-coach (`.claude/skills/teaching-coach/pptx/README.md`) và **đúng thứ tự block** (Global Constraints). "10 câu khẩu ngữ" dùng `vocab`/`dialogue`/`bullets`; footer Hán ngữ Q2 dùng `bullets`/`reading`; lỗi người Việt dùng `table` (Sai|Đúng|Vì sao). Đặt **action title** + chạy ghost-deck test.

**P4 — Ảnh minh hoạ:** `DIR/slide/buoiXX-images.json` = `{"out_dir":"DIR/slide/assets","images":[...]}`. Chạy `fetch_images.py`. Expected: `DONE: N/N images`.

**P5 — GIF nét (TUỲ CHỌN):** Chỉ nếu buổi có chữ mới khó → `gen_stroke_gif.py <hz> DIR/slide/assets/xx.gif` (tái dùng HSK1). Không bắt buộc.

**P6 — Render slide + audio:**
```bash
"$PY" .claude/skills/teaching-coach/pptx/build_deck.py DIR/slide/buoiXX.json DIR/slide/Buoi-XX-<Ten>.pptx
"$PY" .claude/skills/teaching-coach/pptx/slide_audio.py DIR/slide/buoiXX.json --rate=-18%
```
**Soát phát âm (cổng d):** nghe lại file chứa 多音字/儿化 (得/着/行/为/教/还…), sai thì đổi câu/thêm ngữ cảnh rồi `--force`.

**P7 — Audio bài đọc 課文:** edge-tts đọc chậm `--rate=-18%` → `DIR/doc/bai-doc.NN.mp3`. Soát như P6.

**P8 — Bài tập (exercise-generator):** Soạn `DIR/baitap/baitap-buoiXX.json` (~25–30 mục), **đủ 4 phần: 听/读/书写(Viết 3.0)/HSKK**, không trùng câu, phủ rộng vốn từ, đáp án 2 cấp cho tự luận. **Cổng b:** trình script 听力/HSKK cho user duyệt trước khi sinh MP3. `check_baitap.py` (không báo trùng). Sinh audio sau duyệt (`nghe --rate=-22%`, `noi_hskk --rate=-18%`). Render `build_worksheet.py`. **Cổng c:** rà đáp án AI. Append 1 dòng `state/session-log.md`.

**P9 — Cập nhật README + commit:** Đổi trạng thái buổi trong `output/hsk2/README.md` "⏳"→"✅". Commit:
```bash
git add output/hsk2/buoiXX_SLUG output/hsk2/README.md state/session-log.md
git commit -m "feat(hsk2): buổi XX <chủ đề> — trọn gói (slide+audio+bài tập+bài đọc)"
```

**Verify hoàn thành buổi:** pptx mở được; số 生词 ~12–15 & khớp checklist & KHÔNG trùng HSK1; có block 10 câu khẩu ngữ; `doc/` có 課文 đã duyệt + audio; bài tập có **đủ phần Viết 3.0**; worksheet.docx KHÔNG chứa đáp án; dapan.docx có đáp án + 听力文本; audio đã soát 多音字/儿化.

---

## PHASE 1 — Pilot buổi 02 (比 · ngoại hình & trang phục)

### Task 1: buoi02_ngoaihinh_trangphuc

**Param:** `XX=02`, `SLUG=ngoaihinh_trangphuc`, `DIR=output/hsk2/buoi02_ngoaihinh_trangphuc`.
- 生词 (§5 B2): 衣服, 穿, 帽子, 眼睛, 长, 短, 高, 白, 黑, 觉得, 比, 一样 (lọc trùng HSK1).
- Ngữ pháp: **比 (so sánh 1: A比B+adj, KHÔNG dùng 很/非常)** · 跟…一样 · 觉得 · vị ngữ tính từ.
- 課文: New HSK Course 2 bài ngoại hình/trang phục (P2 web-search/tự soạn).
- Hán ngữ Q2: ⏳ (map khi có mục lục).
- Lỗi người Việt: 他比我很高 (thừa 很), lẫn 长 (cháng/zhǎng), thiếu 觉得.

- [ ] **Step 1:** P1 — nội dung + 10 câu khẩu ngữ mô tả người/đồ.
- [ ] **Step 2:** P2 — 課文 (duyệt text).
- [ ] **Step 3:** P3 — `buoi02.json` đủ block đúng thứ tự.
- [ ] **Step 4:** P4 (ảnh) + P5 (GIF nét tuỳ chọn).
- [ ] **Step 5:** P6 (render+audio, soát) + P7 (audio 課文).
- [ ] **Step 6:** P8 — bài tập trọn gói **có phần Viết 3.0** (sắp câu 比, điền chữ).
- [ ] **Step 7:** Verify hoàn thành buổi.
- [ ] **Step 8:** P9 — README ✅ + commit.

## PHASE 2 — Pilot buổi 05 (得 · thể thao)

### Task 2: buoi05_thethao

**Param:** `XX=05`, `SLUG=thethao`, `DIR=output/hsk2/buoi05_thethao`.
- 生词 (§5 B5): 运动, 篮球, 足球, 游泳, 跑步, 踢, 打, 得, 累, 身体 (lọc trùng HSK1).
- Ngữ pháp: **得 (bổ ngữ trình độ: 踢得很好/跑得很快)** · 正在…呢 (đang làm).
- 課文: New HSK Course 2 bài thể thao/vận động.
- Lỗi người Việt: quên 得 (他打篮球好→打得很好), lẫn 踢/打 (踢足球 vs 打篮球), vị trí 正在.

- [ ] **Step 1:** P1. **Step 2:** P2. **Step 3:** P3. **Step 4:** P4(+P5). **Step 5:** P6+P7. **Step 6:** P8 (Viết: sắp câu có 得). **Step 7:** Verify. **Step 8:** P9.

> **REVIEW GATE (bắt buộc):** Sau Task 1 + Task 2, **trình user 2 pilot** (pptx + worksheet + bài đọc). User duyệt khuôn (bố cục, chất lượng, phần Viết 3.0, độ khó) → mới sản xuất phần còn lại. Chỉnh khuôn nếu user yêu cầu.

---

## PHASE 3 — Sản xuất 14 buổi còn lại + 2 ôn (sau khi duyệt pilot)

> Mỗi task chạy đúng **Procedure P** với Param của buổi. Thứ tự: 01 → 03 → 04 → 06 → 07 → 08 → **[Ôn 1]** → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → **[Ôn 2]**. Giao theo lô + review giữa các lô.

### Task 3: buoi01_thoiquen
**Param:** `XX=01`, `SLUG=thoiquen`. 生词 (B1): 起床, 睡觉, 上班, 事情, 分钟, 小时, 时候, 以前, 以后, 一起, 正在. Ngữ pháp: 每 · thời lượng (V了+时间) · 从…到 (thời gian). 課文: routine. Lỗi VN: vị trí thời lượng, 以前/以后.
- [ ] P1→P9 (không GIF bắt buộc).

### Task 4: buoi03_anuong
**Param:** `XX=03`, `SLUG=anuong`. 生词 (B3, mở rộng, loại trùng HSK1): 鸡蛋, 羊肉, 鱼, 牛奶, 咖啡, 西瓜, 服务员, 餐厅, 完, 饱. Ngữ pháp: 了 (đổi trạng thái) · 太…了 · bổ ngữ kết quả 完 (吃完了). 課文: dietary habits. Lỗi VN: 了 lạm dụng, 完 vị trí.
- [ ] P1→P9.

### Task 5: buoi04_sothich_giaitri
**Param:** `XX=04`, `SLUG=sothich_giaitri`. 生词 (B4): 爱好, 唱歌, 跳舞, 音乐, 玩(儿), 游戏, 有意思, 一边. Ngữ pháp: 喜欢/爱+V nâng cao · 一边…一边 · 会…的. 課文: hobbies & entertainment. Lỗi VN: 一边…一边 thiếu vế, 有意思/有意义.
- [ ] P1→P9.

### Task 6: buoi06_dongvat_thucung
**Param:** `XX=06`, `SLUG=dongvat_thucung`. 生词 (B6): 猫, 狗, 鸟, 可爱, 养, 只, 大, 小, 比. Ngữ pháp: tồn tại 有/是 nâng cao · **比 (so sánh 2)** · tính từ mô tả. 課文: animals & pets. Lỗi VN: lượng từ 只, 比 thừa 很.
- [ ] P1→P9. *(chủ đề mới user yêu cầu — chú ý vốn từ động vật thuộc 3.0, đối chiếu checklist)*

### Task 7: buoi07_thoitiet
**Param:** `XX=07`, `SLUG=thoitiet`. 生词 (B7, mở rộng, loại trùng HSK1): 晴, 阴, 雪, 春, 夏, 秋, 冬, 冷, 热, 最, 更. Ngữ pháp: **比 (so sánh 3, sâu: 比…更/一点儿/得多)** · 要…了 (sắp) · 最/更. 課文: weather & seasons. Lỗi VN: 比 + mức độ, 要…了.
- [ ] P1→P9.

### Task 8: buoi08_giaothong
**Param:** `XX=08`, `SLUG=giaothong`. 生词 (B8): 火车, 出租车, 公共汽车, 飞机, 机场, 站, 路, 走, 离, 远, 近, 到. Ngữ pháp: 从…到 · 离 (khoảng cách) · bổ ngữ kết quả 到 (到 nơi). 課文: transport. Lỗi VN: 离 vs 从, 到 vị trí.
- [ ] P1→P9.

### Task 9: Ôn 1 (`on1_nguphap_1-8`)
Ôn ngữ pháp buổi 1–8 (每/thời lượng, **比**, 了/太…了/完, 一边…一边/会…的, **得**/正在, 有/是, 要…了, 从…到/离/到). Slide ôn + bài tập tổng hợp (đủ 听/读/书写/HSKK). Không 生词 mới.
- [ ] P1(ôn)→P3→P6→P8→P9.

### Task 10: buoi09_dulich
**Param:** `XX=09`, `SLUG=dulich`. 生词 (B9): 旅游, 照片, 地方, 过, 次, 回, 来, 去. Ngữ pháp: **过 (trải nghiệm)** · 了 (hoàn thành) · bổ ngữ xu hướng 来/去. 課文: travel experiences. Lỗi VN: 过 vs 了, 次/回.
- [ ] P1→P9.

### Task 11: buoi10_hoctap
**Param:** `XX=10`, `SLUG=hoctap`. 生词 (B10): 课, 考试, 问题, 意思, 复习, 因为, 所以, 虽然, 但是, 懂. Ngữ pháp: **因为…所以** · **虽然…但是**. 課文: study experiences. Lỗi VN: dùng lẻ 1 vế liên từ.
- [ ] P1→P9.

### Task 12: buoi11_congviec_giaotiep
**Param:** `XX=11`, `SLUG=congviec_giaotiep`. 生词 (B11): 公司, 帮, 帮助, 告诉, 介绍, 让, 给, 对, 回答, 打电话. Ngữ pháp: 给 sb V · 对 sb · 让 (khiến, cơ bản) · 帮. 課文: work & communication. Lỗi VN: vị trí 给/对, 让 cấu trúc.
- [ ] P1→P9.

### Task 13: buoi12_muasam
**Param:** `XX=12`, `SLUG=muasam`. 生词 (B12, mở rộng, loại trùng HSK1): 卖, 贵, 便宜, 送, 千, 元, 又. Ngữ pháp: 多少钱 nâng cao · 千/元 · 又…又 · 有点儿 vs (一)点儿. 課文: shopping. Lỗi VN: 有点儿(chê)/一点儿, số lớn.
- [ ] P1→P9.

### Task 14: buoi13_suckhoe
**Param:** `XX=13`, `SLUG=suckhoe`. 生词 (B13): 医院, 药, 生病, 休息, 累, 应该, 别, 疼(check). Ngữ pháp: 别 (khuyên/cấm) · 应该 · 快…了. 課文: health. Lỗi VN: 别 vs 不要, 应该 vị trí.
- [ ] P1→P9.

### Task 15: buoi14_camxuc
**Param:** `XX=14`, `SLUG=camxuc`. 生词 (B14): 高兴, 快乐, 忙, 舒服, 聪明, 认真, 更, 非常, 还是. Ngữ pháp: 觉得 · 得 (ôn) · 更/最/非常 · 还是/或者 (lựa chọn). 課文: feelings & describing people. Lỗi VN: 还是 vs 或者.
- [ ] P1→P9.

### Task 16: buoi15_kehoach
**Param:** `XX=15`, `SLUG=kehoach`. 生词 (B15): 打算, 希望, 准备, 第, 就, 才, 时间. Ngữ pháp: 打算 · 就/才 · 第 (thứ tự) · 会…的. 課文: plans & future. Lỗi VN: 就/才 sắc thái, 第 + 量词.
- [ ] P1→P9.

### Task 17: buoi16_capstone
**Param:** `XX=16`, `SLUG=capstone`. Không 生词 mới lớn — hội thoại dài tổng hợp toàn khoá (mua sắm + du lịch + so sánh + trải nghiệm). Ngữ pháp: ôn tổng hợp. 課文: bài đọc dài tổng hợp. Bài tập mô phỏng đề HSK2 3.0 (đủ 听/读/书写/HSKK).
- [ ] P1→P9.

### Task 18: Ôn 2 (`on2_nguphap_9-16`)
Ôn ngữ pháp buổi 9–16 (过, 因果/nhượng bộ, 给/对/让, 又…又/有点儿, 别/应该/快…了, 还是/或者, 就/才/第) + từ vựng theo cụm chủ đề. Slide ôn + bài tập tổng hợp.
- [ ] P1(ôn)→P3→P6→P8→P9.

> **FINAL GATE:** Sau tất cả buổi + 2 ôn, chạy verify tổng: `hsk2-vocab-grammar-checklist.md` mọi từ "✅ có buổi + đã soạn + không trùng HSK1"; 45 điểm ngữ pháp đã dạy; `output/hsk2/README.md` mọi buổi ✅; đối chiếu số từ ≈ mục tiêu sách chính. Trình user bàn giao.

---

## Out of scope / follow-up

**Phase từ vựng HSK2 theo buổi (§13 spec)** — trang `output/study/hsk2/buoiXX/tu-vung.html` kiểu Quizlet, bỏ neo Activation vault, Leitner box 1. **Tách plan riêng**, viết **sau khi vocab 16 buổi đã chốt** (nguồn = 生词 trong các `buoiXX.json`). Cần điều chỉnh tooling vocab-study (hardcode `hsk6`, đọc `raw/Từ vựng.xlsx`, đọc Activation) → quyết định adapter vs biến thể renderer khi tới nơi. Backlog, không chặn Phase 0–3.

**Rebuild HSK1 lên 3.0** — việc riêng của user (đã nêu). Không thuộc plan này.

**Seed kho đề `knowledge/hsk-exam-bank/hsk2.md`** — tách việc, không thuộc bộ giáo trình này.

## Self-review notes
- Spec §2 chuẩn 3.0 → Global Constraints + Task 0.1. §4 syllabus → Task 0.3 README + mọi task buổi. §5 vocab → Param từng task + Task 0.1 checklist (chống trùng HSK1). §6 block → Global Constraints + P3 (bỏ ngữ âm). §7 課文 → P2 (web-search→fallback tự soạn có ghi chú). §8 Hán ngữ Q2 → P3 footer + Param (⏳ chờ mục lục). §9 pipeline → Procedure P. §10 đặt tên → Global Constraints + tên folder từng task. §12 verify → "Verify hoàn thành buổi" + FINAL GATE. §13 vocab-study → follow-up. §14 rủi ro → Task 0.2 (schema Viết), P2 (課文 fallback), gap HSK1 đã giải quyết (user rebuild).
- Điểm mới 3.0 so với plan HSK1: (a) phần Viết 3.0 bắt buộc trong P8/bài tập — cần Task 0.2 xác nhận schema; (b) chống trùng HSK1 thành ràng buộc cứng có checklist; (c) không có buổi/GIF ngữ âm; (d) 課文 sách mới → nhiều khả năng tự soạn có ghi chú.
- Điểm cần user cấp: mục lục Hán ngữ Q2 (§8, ⏳); xác nhận có PDF New HSK Course 2 để bóc doc-analyzer (tăng độ chính xác vocab + 課文).
