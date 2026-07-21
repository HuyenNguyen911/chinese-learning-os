# HSK2 (chuẩn 3.0) — Bộ giáo trình 16 buổi (design spec)

**Ngày:** 2026-07-20
**Trạng thái:** Đã duyệt thiết kế (user chốt 2026-07-20; HSK1 sẽ build lại 3.0 riêng) — implementation plan: xem `docs/superpowers/plans/2026-07-20-hsk2-full-course.md`
**Chủ sở hữu output:** Teaching Coach (`slide/`), Exercise Generator (`baitap/`), Vocab Study (trang từ vựng, phase cuối)

## 1. Mục tiêu

Xây **bộ HSK2 theo chuẩn mới HSK 3.0** (国际中文教育中文水平等级标准, công bố 11/2025, kỳ thi chuyển đổi từ 2026) — trọn 16 buổi + 2 ôn, chất lượng cao, khẩu ngữ, đa dạng chủ đề, dành cho học viên **đã qua HSK1** và chuẩn bị thi HSK2 (cấp 2 hệ 3 bậc 9 cấp).

Yêu cầu cốt lõi (theo phỏng vấn user):
- Build theo **chuẩn 3.0**, KHÔNG phải 2.0.
- **Sách chính** = giáo trình chuẩn 3.0 = **New HSK Course 2** (新HSK教程2, 主编 郭凤岚, NXB FLTRP/外研社, HSK官方认证教材 — user đã xác nhận bìa). **Sách tham khảo** = **Giáo trình Hán ngữ** (user cấp `raw/Hán ngữ 2.pdf` = 《汉语教程》第一册·下 修订本, 主编 杨寄洲, BLCU — **bài 16–30**, nối tiếp Quyển Thượng bài 1–15). Footer đối chiếu, list tên bài.
- **Thêm chủ đề** Giải trí · Thể thao · Sở thích · Động vật · Thú cưng (3.0 có sẵn vốn từ các nhóm này — không phải "bổ sung ngoài chuẩn").
- **Tránh trùng lặp với HSK1** để không gây chán — mỗi buổi chỉ dạy **từ MỚI**; chủ đề tái xuất thì **đào sâu bằng từ mới + ngữ pháp mới**, không lặp lại.
- Deliverable mỗi buổi **trọn gói như HSK1**.

## 2. Bối cảnh chuẩn 3.0 (nguồn đã tra — §16)

| | HSK2 2.0 (cũ) | **HSK2 3.0 (bộ này)** |
|---|---|---|
| Từ mới | 150 | **~200 từ mới + mở rộng** (New HSK Course 2); tích luỹ theo hệ 3.0 |
| Ngữ pháp | ~12 cụm | **45 điểm ngữ pháp** (theo sách chính); đề cương chính thức liệt kê 60+ điểm cấp 2 |
| Kỹ năng | Nghe + Đọc | Nghe + Đọc **+ phần Viết (书写)** mới ở cấp 2 |
| Sách chính | HSK Standard Course 2 (姜丽萍, BLCU) | **New HSK Course 2 (FLTRP, 15 bài)** |
| Chữ Hán | nhận đọc | 3.0 bắt đầu yêu cầu **nhận diện chữ** rõ hơn |

**Con số chính xác chốt ở implementation** (Task checklist) — đối chiếu **词汇表/语法表 chính thức 3.0** + mục lục New HSK Course 2. Lý do: các nguồn thứ cấp đếm lệch nhau (词 vs 字, danh sách thi vs sách). Số vận hành của spec = **theo sách chính New HSK Course 2** (~200 từ mới, 45 điểm ngữ pháp, 15 bài).

## 3. Phạm vi

### Trong phạm vi
- **16 buổi nội dung** (dựng mới hoàn toàn) + **2 buổi ôn** (checkpoint sau buổi 8 và sau buổi 16).
- Mỗi buổi giao **trọn gói**: slide `.pptx` (+ audio) · bài tập worksheet + audio + đáp án (đủ 听/读/书写 + **书写/Viết** 3.0 + HSKK) · bài đọc 課文 (text + audio) · footer đối chiếu Hán ngữ Q2.
- **Trang từ vựng HSK2 theo buổi** (vocab-study-style, Quizlet) — `output/study/hsk2/buoiXX/tu-vung.html`. Làm ở **phase cuối** (§14).
- 1 file syllabus tổng `output/hsk2/README.md` (source of truth thứ tự dạy).

### Ngoài phạm vi
- **Không đụng bộ HSK1** (2.0) đã build. HSK2 là cây độc lập trong `output/hsk2/`.
- **Không tái chuẩn hoá HSK1 lên 3.0** (xem rủi ro §15 — gap đầu vào).
- Không seed kho đề `knowledge/hsk-exam-bank/hsk2.md` trong bộ này (tách việc).

## 4. Master syllabus 16 buổi + 2 ôn (thứ tự dạy)

Nguyên tắc: **1 buổi = 1 chủ đề 3.0 + 3–4 điểm ngữ pháp + ~12–15 từ mới**, bám sát 15 bài New HSK Course 2 (buổi ≈ bài; buổi 16 là capstone tổng hợp). Chủ đề trùng tên với HSK1 (ăn uống, thời tiết, mua sắm...) **chỉ tái xuất ở tầng sâu hơn** với vốn từ + ngữ pháp mới.

Cột "Hán ngữ" trỏ bài trong 《汉语教程》第一册·下 (bài 16–30, §8). Ngữ pháp HSK2 3.0 **khớp rất tốt** với ngữ pháp các bài này → footer để học viên tự mở đọc/nghe đúng bài.

| # | Buổi (chủ đề) | Ngữ pháp trọng tâm | Chủ đề 3.0 | Hán ngữ (第一册·下) |
|---|---|---|---|---|
| 1 | Ngày mới & thói quen | 每 · thời lượng (V了+时间) · 从…到 (thời gian) | daily routine, time mở rộng | L21 我的一天 · L30 时量补语 · L22 以前/以后 |
| 2 | Ngoại hình & trang phục | **比 (so sánh 1)** · 觉得 · vị ngữ tính từ nâng cao | appearance & clothing | L19 便宜一点儿 (⚠️ 比 có thể ở 第二册 — kiểm tra) |
| 3 | Ăn uống & thói quen ăn | 了 (đổi trạng thái) · 太…了 · bổ ngữ kết quả 完 | dietary habits | L26 语气助词了 · L29 结果补语(完) |
| 4 | **Sở thích & giải trí** | 喜欢/爱+V nâng cao · 一边…一边 · 会…的 | hobbies & entertainment | L16 晚上你常做什么 |
| 5 | **Thể thao** | **得 (bổ ngữ trình độ)** · 正在…呢 | sports | **L25 她学得很好 (状态补语)** · L17 动作的进行 |
| 6 | **Động vật & thú cưng** | tồn tại 有/是 nâng cao · **比 (so sánh 2)** · tính từ mô tả | animals & pets | L20 属狗 (con giáp) · L23 存在的表达 |
| 7 | Thời tiết & mùa | **比 (so sánh 3, sâu)** · 要…了 (sắp) · 最/更 | weather & seasons | L28 阳光 (⚠️ 比/mùa có thể bổ sung ngoài) |
| 8 | Đi lại & giao thông | 从…到 · 离 (khoảng cách) · bổ ngữ kết quả 到 | transport | **L23 从这儿到博物馆有多远/方位词** · L18 去上海参观 |
| — | **Ôn 1** | ngữ pháp buổi 1–8 | — | — |
| 9 | Du lịch & trải nghiệm | **过 (trải nghiệm)** · 了 (hoàn thành) · bổ ngữ xu hướng 来/去 | travel experiences | L27 动作的完成:动词+了 · L18 参观 |
| 10 | Học tập & kinh nghiệm | **因为…所以** · **虽然…但是** | study experiences | **L27 因为…所以** · **L28 虽然…但是** |
| 11 | Công việc & giao tiếp | 给 sb V · 对 sb · 让 (khiến, cơ bản) · 帮 | work & communication | **L17 双宾语句** · L22 请老师教我书法 |
| 12 | Mua sắm nâng cao | 多少钱 nâng cao · 千/元 · 又…又 · 有点儿 vs (一)点儿 | shopping | **L19 便宜一点儿/人民币单位/多一点儿·有一点儿** |
| 13 | Sức khoẻ & khám bệnh | 别 (khuyên/cấm) · 应该 · 快…了 | health | L27 你怎么了/玛丽病了 · L24 能愿动词(应该) |
| 14 | Cảm xúc & mô tả người | 觉得 · 得 (ôn) · 更/最/非常 · 还是/或者 (lựa chọn) | feelings, describing people | **L16 还是/或者** |
| 15 | Kế hoạch & tương lai | 打算 · 就/才 · 第 (thứ tự) · 会…的 | plans, future | **L28 就/才 · 要是…就** · L20 毕业/生日 |
| 16 | **Capstone hội thoại** | ôn tổng hợp toàn khoá | trộn chủ đề | tổng hợp L16–30 |
| — | **Ôn 2** | ngữ pháp buổi 9–16 + từ vựng cụm | — | — |

**Phủ ngữ pháp:** ~3 điểm/buổi × 16 ≈ 48 điểm ⊇ 45 điểm sách chính. "6 nhóm ngữ pháp mới của cấp 2" (so sánh 比, liên từ nhân quả/nhượng bộ, bổ ngữ trình độ/kết quả, thể quá khứ/tiếp diễn, giới từ, mô tả mức độ) đều có buổi phụ trách.

> ⚠️ **Điểm cần kiểm tra ở impl:** 汉语教程 第一册·下 (L16–30) **thiếu điểm 比 (so sánh)** và có thể thiếu mùa/thời tiết đầy đủ — các điểm này có thể nằm ở **第二册**. Buổi 2/6/7 (dùng 比 nhiều) sẽ đối chiếu 第二册 nếu user có, hoặc footer ghi "比 — bổ sung ngoài Hán ngữ 第一册·下". New HSK Course 2 (sách chính) mới là nguồn chuẩn cho 比.

**Ràng buộc chống trùng HSK1 (cứng):** danh sách 生词 mỗi buổi phải **loại mọi từ đã có trong 150 từ HSK1** (đối chiếu checklist §Task impl). Chủ đề tái xuất (buổi 3 ăn uống / 7 thời tiết / 12 mua sắm) framing "mở rộng", vocab hoàn toàn mới.

## 5. Chi tiết vocab lõi + ngữ pháp mỗi buổi

Danh sách chốt ở implementation theo **词汇表 3.0 + mục lục New HSK Course 2**. Lõi định hướng (đã loại từ HSK1):

- **B1 Thói quen:** 起床, 睡觉, 上班, 事情, 分钟, 小时, 时候, 以前, 以后, 一起, 正在.
- **B2 Ngoại hình/trang phục:** 衣服, 穿, 帽子, 眼睛, 长, 短, 高, 白, 黑, 觉得, 比, 一样.
- **B3 Ăn uống mở rộng:** 鸡蛋, 羊肉, 鱼, 牛奶, 咖啡, 西瓜, 服务员, 餐厅, 好吃(≠HSK1?→check), 完, 饱.
- **B4 Sở thích/giải trí:** 爱好, 唱歌, 跳舞, 音乐, 玩(儿), 电影, 游戏, 一边…一边, 有意思.
- **B5 Thể thao:** 运动, 篮球, 足球, 游泳, 跑步, 踢, 打, 得, 累, 身体.
- **B6 Động vật/thú cưng:** 猫, 狗, 鸟, 鱼, 可爱, 养, 只(lượng từ), 大/小(mô tả), 比.
- **B7 Thời tiết/mùa:** 晴, 阴, 雪, 春, 夏, 秋, 冬, 冷, 热, 最, 更, 要…了.
- **B8 Giao thông:** 火车, 出租车, 公共汽车, 飞机, 机场, 站, 路, 走, 离, 远, 近, 到.
- **B9 Du lịch/trải nghiệm:** 旅游, 玩儿, 照片, 地方, 过, 次, 回, 来, 去, 一起.
- **B10 Học tập/kinh nghiệm:** 课, 考试, 问题, 意思, 复习, 因为, 所以, 虽然, 但是, 懂.
- **B11 Công việc/giao tiếp:** 公司, 帮, 帮助, 告诉, 介绍, 让, 给, 对, 回答, 打电话.
- **B12 Mua sắm:** 卖, 贵, 便宜, 送, 千, 元, 块, 又…又, 一点儿, 有点儿, 商店.
- **B13 Sức khoẻ:** 医院, 药, 生病, 休息, 累, 应该, 别, 快…了, 疼(check level).
- **B14 Cảm xúc/mô tả người:** 高兴, 快乐, 忙, 舒服, 漂亮, 聪明, 认真, 更, 非常, 还是.
- **B15 Kế hoạch/tương lai:** 打算, 希望, 准备, 第, 就, 才, 会…的, 时间.

> Từ nghi trùng HSK1 (好吃, 电影, 一起, 块, 商店...) sẽ bị gạt khỏi 生词 nếu đã dạy ở HSK1; giữ lại chỉ để **ôn nhanh trong câu ví dụ**, không tính là từ mới của buổi.

## 6. Cấu trúc deliverable mỗi buổi

```
output/hsk2/buoiXX_<slug>/
  slide/
    buoiXX.json            # teaching-coach schema
    Buoi-XX-....pptx
    buoiXX-images.json
    assets/                # ảnh, (GIF nét chữ nếu dùng), audio slide
  baitap/
    baitap-buoiXX.json     # exercise-generator (đủ 听/读/书写 + Viết 3.0 + HSKK)
    hocsinh/worksheet.docx + audio/
    dapan/dapan.docx
  doc/
    bai-doc.md             # 課文: hán + pinyin + dịch + link audio
    bai-doc.NN.mp3
```

Thứ tự block slide (giống HSK1, bỏ block ngữ âm):
`title → ôn buổi trước → mục tiêu → 生词 (chia nhóm) → ngữ pháp (giải thích bản chất + bảng) → 10 câu khẩu ngữ thông dụng → hội thoại/課文 → bài đọc → footer đối chiếu Hán ngữ Q2 → slide lỗi người Việt hay mắc → preview bài tập → Done.`

Khác HSK1:
- **Không có buổi ngữ âm/GIF phát âm** (học viên đã qua HSK1). GIF **thứ tự nét** chỉ dùng **tuỳ chọn** cho vài chữ mới khó (tái dùng `gen_stroke_gif.py` của HSK1), không bắt buộc.
- Bài tập **thêm phần Viết (书写) 3.0**: sắp xếp câu, điền chữ Hán, viết câu ngắn theo mẫu (tách khỏi HSKK nói).

## 7. Nguồn bài đọc 課文 (sách chính New HSK Course 2)

- Quyết định user: **web-search thử** text New HSK Course 2 → bài nào không có bản đáng tin thì **tự soạn theo chủ đề** (fallback).
- Sách New HSK Course 2 mới ra 11/2025 → nhiều bài có thể **chưa có bản gốc online**. Quy trình mỗi buổi:
  1. WebSearch/WebFetch text 課文 bài tương ứng → nếu tìm được bản đáng tin (≥1 nguồn) → dùng nguyên văn, ghi nguồn.
  2. Không tìm được → **tự soạn** đoạn đọc/hội thoại bám 生词 + ngữ pháp buổi, **đánh dấu rõ "tự soạn, không phải nguyên văn sách"**.
- Định dạng: 汉字 + pinyin + dịch Việt. Audio edge-tts đọc chậm (`-18%`, hội thoại đa giọng), soát 多音字/儿化.

## 8. Đối chiếu Giáo trình Hán ngữ (《汉语教程》第一册·下)

- **Sách:** `raw/Hán ngữ 2.pdf` = 《汉语教程》第一册·下 修订本 (主编 杨寄洲, BLCU) — **bài 16–30**, nối tiếp Quyển Thượng (bài 1–15) mà HSK1 dùng. File là **PDF scan** → bóc mục lục bằng doc-analyzer/OCR chi_sim (đã làm; số trang trong ngoặc).
- Footer slide + `README.md`: **list tên bài Hán ngữ** tương ứng chủ đề buổi (mapping ở bảng §4). User có sách + audio → tự hướng dẫn học viên mở đọc/nghe.

**Mục lục 《汉语教程》第一册·下 (đã OCR):**

| Bài | 课文 | Ngữ pháp chính | Trang |
|---|---|---|---|
| L16 | 你常去图书馆吗 / 晚上你常做什么 | 时间词语作状语 · 还是/或者 | 1 |
| L17 | 他在做什么呢 / 谁教你们语法 | 动作的进行 · 双宾语句 · 怎么+动词 | 14 |
| L18 | 我去邮局寄包裹 / 外贸代表团明天去上海参观 | (语音: 逻辑重音) | 28 |
| L19 | 可以试试吗 / 便宜一点儿吧 | 动词重叠 · 多一点儿/有一点儿 · 人民币单位 | 40 |
| L20 | 你哪一年大学毕业 / 祝你生日快乐 | 年月日 · 疑问语调 · 属狗 | 54 |
| L21 | 我的一天 / 明天早上七点一刻出发 | 时间的表达 | 68 |
| L22 | 请老师教我书法 | 以前/以后 · 京剧 | 82 |
| L23 | 学校里边有邮局吗 / 从这儿到博物馆有多远 | 方位词 · 存在的表达 · 离…有多远 | ~96 |
| L24 | 我想学太极拳 / 您能不能再说一遍 | 能愿动词 · 询问原因 | 114 |
| L25 | 她学得很好 / 她每天都起得很早 | **状态补语 (bổ ngữ trình độ 得)** | 129 |
| L26 | 田芳去哪儿了 / 他又来电话了 | 语气助词"了"(1) | 144 |
| L27 | 你怎么了 / 玛丽病了 | 动作的完成:动词+了 · 因为…所以 | 160 |
| L28 | (房子/阳光) / 我还是想要上下午都有阳光的 | 就/才 · 要是…就 · 虽然…但是 | 177 |
| L29 | 我都做对了 / 看完电影再做作业 | 结果补语 (上/成/到) · 主谓词组作定语 | 192 |
| L30 | 我来了两个多月了 / 我每天都练一个小时 | 时量补语 · 概数 · 离合动词 | 208 |

- ⚠️ Sách **thiếu điểm 比 (so sánh)** — nhiều khả năng ở 第二册. Buổi 2/6/7 (HSK2 3.0 dùng 比) sẽ đối chiếu 第二册 nếu user cấp, hoặc footer ghi rõ "比 — ngoài phạm vi Hán ngữ 第一册·下, xem sách chính New HSK Course 2".

## 9. Pipeline sản xuất mỗi buổi (có cổng duyệt) — Procedure P

Giống HSK1 (P1–P9), điều chỉnh cho 3.0:
1. **Master Teacher:** nội dung đúng-đủ — 生词 (đủ 汉字/pinyin/nghĩa, đã loại trùng HSK1), ngữ pháp giải thích bản chất, ví dụ khẩu ngữ đời thường, 10 câu khẩu ngữ dùng-ngay, 2–3 lỗi người Việt.
2. **Nguồn 課文 (cổng a):** web-search New HSK Course 2 → cổng duyệt text (nguyên văn hoặc tự soạn có ghi chú).
3. **Experience Designer:** map → `buoiXX.json` (đúng thứ tự block, action title, ghost-deck test).
4. **Assets:** fetch ảnh · (GIF nét tuỳ chọn) · edge-tts audio → soát 多音字/儿化.
5. **Render pptx:** `build_deck.py`.
6. **Bài tập (cổng b/c):** exercise-generator — đủ 听/读/书写 + **Viết 3.0** + HSKK; cổng duyệt script audio; `check_baitap.py`; **cổng kiểm tra đáp án AI**.

## 10. Đặt tên & syllabus index

- Tất cả buổi đánh số 2 chữ số theo vị trí: `buoi01_thoiquen`, `buoi02_ngoaihinh_trangphuc`, `buoi03_anuong`, `buoi04_sothich_giaitri`, `buoi05_thethao`, `buoi06_dongvat_thucung`, `buoi07_thoitiet`, `buoi08_giaothong`, `buoi09_dulich`, `buoi10_hoctap`, `buoi11_congviec_giaotiep`, `buoi12_muasam`, `buoi13_suckhoe`, `buoi14_camxuc`, `buoi15_kehoach`, `buoi16_capstone`; ôn: `on1_nguphap_1-8`, `on2_nguphap_9-16`.
- `output/hsk2/README.md` = bảng syllabus 16 buổi + 2 ôn, map vị trí ↔ folder, ghi rõ chuẩn **3.0** + sách chính/tham khảo. Source of truth.
- `meta.lesson` mỗi JSON: `"HSK2 · Buổi X"`.

## 11. Chiến lược giao (de-risk)

- **2 pilot trước:**
  - `buoi02_ngoaihinh_trangphuc` — chốt khuôn buổi có **比 (so sánh)**, block đầy đủ, phần Viết 3.0 trong bài tập.
  - `buoi05_thethao` — chốt khuôn **得 (bổ ngữ trình độ)** + chủ đề mới (thể thao) user yêu cầu.
- User duyệt 2 pilot → sản xuất phần còn lại theo lô + review.
- Thứ tự sản xuất còn lại: theo syllabus (01 → 03 → 04 → 06 → 07 → 08 → [Ôn 1] → 09 → … → 16 → [Ôn 2]).
- **Phase cuối:** trang từ vựng theo buổi (§14) sau khi vocab đã chốt.

## 12. Tiêu chí hoàn thành (verification)

- [ ] 16 buổi + 2 ôn đủ deliverable (slide pptx + audio, baitap 4 phần **có Viết 3.0**, bài đọc + audio, footer Hán ngữ Q2).
- [ ] Mỗi buổi có block **10 câu khẩu ngữ thông dụng**.
- [ ] **Không từ nào trùng 150 từ HSK1** trong danh sách 生词 (đối chiếu checklist).
- [ ] Tổng vocab ≈ mục tiêu sách chính (~200 từ mới + mở rộng), phủ đủ nhóm chủ đề (gồm giải trí/thể thao/sở thích/động vật/thú cưng), không trùng giữa các buổi.
- [ ] 45 điểm ngữ pháp 3.0 đều có buổi phụ trách (đối chiếu 语法表 3.0).
- [ ] Mỗi pptx render + mở được.
- [ ] Audio soát 多音字/儿化, đọc chậm.
- [ ] 課文: nguyên văn New HSK Course 2 (web-search verified) HOẶC tự soạn có ghi chú rõ.
- [ ] Bài tập qua cổng kiểm tra đáp án AI.
- [ ] `README.md` syllabus đầy đủ, ghi rõ chuẩn 3.0.
- [ ] Trang từ vựng `output/study/hsk2/buoiXX/tu-vung.html` sinh đủ, flashcard + 🔊 chạy (Leitner trung tính, không neo Activation vault).

## 13. Trang từ vựng HSK2 theo buổi (vocab-study-style)

- Như HSK1 §14: mỗi buổi 1 trang Quizlet `output/study/hsk2/buoiXX/tu-vung.html`, tái dùng engine vocab-study (bảng 生词 + flashcard active-recall + Leitner + chiết tự + mẹo nhớ Việt + 🔊).
- **Bỏ neo Activation vault** (dữ liệu Activation là HSK6 cá nhân user) → Leitner khởi động box 1. Nguồn từ = 生词 trong `buoiXX.json`. KHÔNG đọc `raw/Từ vựng.xlsx`.
- **Phase cuối**, sau khi vocab 16 buổi chốt.

## 14. Rủi ro & mở

- **Gap đầu vào HSK1→HSK2 — ĐÃ GIẢI QUYẾT:** user sẽ **build lại HSK1 theo chuẩn 3.0** (việc riêng, sau). Do đó HSK2 3.0 cứ giả định đầu vào HSK1 3.0 (~300 từ) như sách chính, **không cần buổi cầu nối**. Buổi 1 là chủ đề HSK2 đầy đủ.
- **Nguyên văn 課文 New HSK Course 2:** sách mới (11/2025) → có thể thiếu bản online. Fallback: tự soạn có ghi chú (đã thống nhất §7). Nếu user có sách/PDF → chuyển sang bóc bằng doc-analyzer (chính xác hơn).
- **Con số 3.0 lệch giữa nguồn:** chốt bằng 词汇表/语法表 chính thức + sách chính ở implementation.
- **Phần Viết (书写) 3.0:** cần xác nhận exercise-generator hỗ trợ dạng câu Viết; nếu chưa, bổ sung dạng mục trong schema (đánh giá ở đầu implementation).
- **Hán ngữ mapping — ĐÃ CÓ:** user cấp `raw/Hán ngữ 2.pdf` (=《汉语教程》第一册·下, L16–30); mục lục đã OCR + map vào §4/§8. Còn thiếu điểm **比** (khả năng ở 第二册) → nếu cần, user cấp thêm 第二册; nếu không, footer buổi 2/6/7 ghi rõ 比 ngoài phạm vi sách này.

## 15. Bước tiếp theo

Sau khi user **duyệt spec này** → viết **implementation plan** (mô phỏng `2026-07-19-hsk1-full-course.md`): Phase 0 (checklist phủ từ 3.0 + chống trùng HSK1, README syllabus, đánh giá schema Viết) → Procedure P → 2 pilot → sản xuất lô → phase trang từ vựng.

## 16. Nguồn tra cứu (3.0)

- New HSK Course / HSK 3.0 launch (FLTRP, 11/2025): [fltrp.com](https://www.fltrp.com/c/2025-11-20/540070.shtml) · [newhskcourse.com](https://newhskcourse.com/)
- HSK 3.0 vs 2.0, số từ cấp 2: [hanzistroke.com/blog/new-hsk-3-guide](https://www.hanzistroke.com/blog/new-hsk-3-guide) · [khanjischool.com](https://khanjischool.com/blog/chinese/new-hsk-30-2026-vocabulary-levels-exams-and-official-textbooks)
- HSK2 3.0 yêu cầu/đề cương + phần Viết: [passhsk.app/hsk-2-requirements-2026](https://www.passhsk.app/hsk-2-requirements-2026) · [mandarinzone.com](https://www.mandarinzone.com/hsk-level-2-all-you-need-to-know-about-hsk-2/)
- Ngữ pháp 3.0 cấp 2: [mandarinbean.com/new-hsk-grammar](https://mandarinbean.com/new-hsk-grammar/) · [hskstory.com/guides/hsk-30-syllabus](https://hskstory.com/guides/hsk-30-syllabus)
- New HSK Course 2 (15 bài, ~200 từ, 45 ngữ pháp): kết quả tìm kiếm FLTRP/purpleculture (2026)
- HSK Standard Course 2 (2.0, đối chứng): [hskstandardcourse.com](https://www.hskstandardcourse.com/hsk-standard-course-level-2/hsk-standard-course-2-textbook/)
