# HSK2 (chuẩn 3.0) — Bộ giáo trình 15 buổi (design spec)

**Ngày:** 2026-07-20
**Trạng thái:** Đã duyệt thiết kế (user chốt 2026-07-20; HSK1 sẽ build lại 3.0 riêng) — implementation plan: xem `docs/superpowers/plans/2026-07-20-hsk2-full-course.md`
**Chủ sở hữu output:** Teaching Coach (`slide/`), Exercise Generator (`baitap/`), Vocab Study (trang từ vựng, phase cuối)

## 1. Mục tiêu

Xây **bộ HSK2 theo chuẩn mới HSK 3.0** (国际中文教育中文水平等级标准, công bố 11/2025, kỳ thi chuyển đổi từ 2026) — **15 buổi (bám sát 15 bài New HSK Course 2) + 2 ôn**, chất lượng cao, khẩu ngữ, đa dạng chủ đề, dành cho học viên **đã qua HSK1** và chuẩn bị thi HSK2 (cấp 2 hệ 3 bậc 9 cấp).

Yêu cầu cốt lõi (theo phỏng vấn user):
- Build theo **chuẩn 3.0**, KHÔNG phải 2.0.
- **Sách chính** = giáo trình chuẩn 3.0 = **New HSK Course 2** (新HSK教程2, 主编 **郭风岚** — GS ĐH Ngôn ngữ Bắc Kinh, chủ biên trọn bộ 新HSK教程 1–6; NXB FLTRP/外研社, HSK官方认证教材; user xác nhận bìa). Xác minh nguồn chính chủ (中国高校教材图书网): **15 课 · 200 từ mới + mở rộng · 45 điểm ngữ pháp**, đối tượng đã học ~30–36 tiết / ~300 từ. **Sách tham khảo** = **Giáo trình Hán ngữ** (user cấp `raw/Hán ngữ 2.pdf` = 《汉语教程》第一册·下 修订本, 主编 杨寄洲, BLCU, 2007 — **bài 16–30**, nối tiếp Quyển Thượng bài 1–15; là giáo trình Hán ngữ tổng hợp cũ, KHÔNG phải sách chuẩn HSK 3.0 → chỉ đóng vai footer đối chiếu). Footer list tên bài.
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
- **15 buổi nội dung** (buổi = 1 bài New HSK Course 2) + **2 buổi ôn** (checkpoint sau bài 8 và sau bài 15).
- Mỗi buổi giao **trọn gói**: slide `.pptx` (+ audio) · bài tập worksheet + audio + đáp án (đủ 听/读/书写 + **书写/Viết** 3.0 + HSKK; phần 读 có thêm **≥1 văn bản thực tế tự soạn theo chủ đề buổi** — tin nhắn/biển báo/thực đơn/quảng cáo, KHÔNG trích từ sách) · bài đọc 課文 (text + audio) · footer đối chiếu Hán ngữ Q2.
- **Trang từ vựng HSK2 theo buổi** (vocab-study-style, Quizlet) — `output/study/hsk2/buoiXX/tu-vung.html`. Làm ở **phase cuối** (§14).
- 1 file syllabus tổng `output/hsk2/README.md` (source of truth thứ tự dạy).

### Ngoài phạm vi
- **Không đụng bộ HSK1** (2.0) đã build. HSK2 là cây độc lập trong `output/hsk2/`.
- **Không tái chuẩn hoá HSK1 lên 3.0** (xem rủi ro §15 — gap đầu vào).
- Không seed kho đề `knowledge/hsk-exam-bank/hsk2.md` trong bộ này (tách việc).

## 4. Master syllabus 15 buổi + 2 ôn — BÁM SÁT New HSK Course 2

**Quyết định (user 2026-07-20):** syllabus **bám đúng 15 bài sách chính**; **buổi = bài**. Nguồn chân lý = mục lục thật `docs/superpowers/specs/hsk2-new-hsk-course-2-toc.md` (đã trích từ `raw/New HSK Course 2.pdf`). Ngữ pháp = cột 小语讲堂 của sách; 生词 = 词汇表 sách (trang 141) + 生词 từng bài (khoá ở Task 0.1). **Ôn:** 2 buổi ôn (sau bài 8 giữa khoá, sau bài 15 cuối khoá); ngoài ra sách có 学习小结 mỗi 3 bài → dùng làm ôn nhanh trong buổi.

Cột "Hán ngữ" = bài trong 《汉语教程》第一册·下 (bài 16–30, §8) khớp **một phần** (điểm nâng cao như 比较句/趋向补语/着/动量补语 nằm ở 第二册 → đánh dấu). Footer để học viên tự mở đọc/nghe.

| # | Bài (课文 tiêu đề) | Ngữ pháp (小语讲堂) | Chủ đề | Hán ngữ 第一册·下 |
|---|---|---|---|---|
| 1 | 她请我们吃了北京烤鸭 | 语气助词"吧"(2) · "是…的"句 · 请/让/叫 (nhờ) | mời ăn, món BK, nhờ vả | L22 请… |
| 2 | 还是打车去北大吧 | 兼语句 · 还是…吧 · 多 (概数) · cụm làm định ngữ | giao thông, đề nghị ⟨**+ hỏi đường 怎么走**⟩ | L16 还是/或者 · L17 兼语 |
| 3 | 我想去西安旅游 | 结果补语 · 动词重叠(1)(2) · 动态助词"过" · 因为…所以 | du lịch (Tây An) ⟨**+ đặt khách sạn**⟩ | L29 结果补语 · L19 动词重叠 · L27 因为…所以 |
| 4 | 你穿红色的很好看 | "的"字短语 · 简单趋向补语(1)(2) · 都…了 · **把字句 (cơ bản, bổ sung)** | trang phục, màu sắc | L19 便宜一点儿 · (趋向补语→第二册) |
| 5 | 第一次去中国朋友家 | 形容词重叠 · 什么的 · 结构助词"地" · 一…就… | thăm nhà bạn ⟨**lồng động vật/thú cưng + giới thiệu bản thân/gia đình sâu**⟩ | — |
| 6 | 小雪，生日快乐！ | 状态补语(1)(2) [bổ ngữ trình độ **得**] | sinh nhật, chúc mừng | **L25 状态补语 得** |
| 7 | 他篮球打得很好 | 比较句(1)(2) [**比**] | **thể thao** (bóng rổ) | L25 得 · (比较句→第二册) |
| 8 | 虽然你忘了，但是我记得 | 虽然…但是 · 比较句(3) · 动词"离" | trí nhớ, so sánh | **L28 虽然…但是** · **L23 离** |
| — | **Ôn 1** (giữa khoá) | ôn bài 1–8 + **bảng hệ thống bổ ngữ (kết quả/xu hướng/得) + bảng so sánh 比较句(1)(2)(3)** (chỉ ôn tập, không dạy mới) | — | — |
| 9 | 我去买杯奶茶 | 时量补语(1) · 主谓谓语句 · 选择问句 | đồ uống, mua sắm ⟨**+ hỏi giá, so sánh giá**⟩ | **L30 时量补语** · L16 选择问 |
| 10 | 就要考试了 | 要/快/快要/就要…了 · 动态助词"着"(1)(2) | thi cử, học tập ⟨**+ đặt lịch hẹn**⟩ | (快…了; 着→第二册) |
| 11 | 我最喜欢吃中国菜 | 程度副词"最" · **被字句 (đơn giản, bổ sung)** | ăn uống, sở thích | L?? (最) |
| 12 | 这里比北京冷多了 | 比较句(4)(5)(6) · **连…都/也 (bổ sung)** | thời tiết, so sánh | (比较句→第二册) |
| 13 | 我们爱上中文课 | 双宾语句(2) · 比较句(7)(8) | học tiếng Trung | **L17 双宾语句** |
| 14 | 一个人过年多没意思啊 | 存现句 · 复合趋向补语 | lễ Tết, cảm xúc | L23 存在的表达 · (复合趋向→第二册) |
| 15 | 我想再去一次中国 | 动量补语(1)(2) · "有"字句(2) | kế hoạch, quay lại TQ | (动量补语→第二册) |
| — | **Ôn 2** (cuối khoá) | ôn bài 9–15 + **bảng hệ thống bổ ngữ đầy đủ 6 loại (nối Ôn 1) + bảng so sánh 比较句(1)-(8) đầy đủ** + capstone hội thoại tổng hợp (chỉ ôn tập, không dạy mới) | — | — |

**Phủ ngữ pháp:** 45 điểm 小语讲堂 trải đều 15 bài (một số bài 2–3 điểm; bài nhiều nhất là các bài có nhiều 比较句). Danh sách 45 điểm đầy đủ ở file TOC.

> **Động vật & thú cưng (user muốn, sách không có bài riêng):** theo quyết định → **lồng từ mở rộng vào Bài 5** (第一次去中国朋友家 — tự nhiên có "nhà bạn nuôi mèo/chó"), đánh dấu "từ mở rộng ngoài 200 từ sách". Có thể rải thêm ở Bài 3 (du lịch thấy động vật). KHÔNG thêm buổi riêng.

**Ràng buộc chống trùng HSK1 (cứng):** 生词 mỗi bài loại mọi từ đã có trong HSK1 (đối chiếu checklist Task 0.1). Từ mở rộng (pets) cũng chọn từ ngoài HSK1.

> **Ngữ pháp bổ sung ngoài sách (vá theo tiêu chuẩn đầu ra — 把/被/连…都/也 KHÔNG có trong 45 điểm 小语讲堂 của New HSK Course 2), lồng vào buổi có sẵn — KHÔNG dạy ở 2 buổi Ôn (Ôn chỉ ôn tập, không học nội dung mới):**
> - **把字句 (mức cơ bản)** — lồng vào **Bài 4** (trang phục), ghép tự nhiên với 简单趋向补语 vốn có sẵn: "把+O+V+bổ ngữ xu hướng/kết quả" (vd 把衣服穿上, 把衣服脱下来).
> - **被字句 (đơn giản)** — lồng vào **Bài 11** (món ăn yêu thích): vd 这道菜太好吃了，都被吃光了.
> - **连…都/也** — lồng vào **Bài 12** (thời tiết, so sánh), nhấn mạnh mức độ cực đoan tự nhiên đi cùng 比较句: vd 这儿冷得连水都能结冰.
> - Đánh dấu rõ trong slide buổi tương ứng: "ngữ pháp mở rộng ngoài 45 điểm sách chính, bổ sung theo yêu cầu đầu ra".

> **Bổ sung giao tiếp còn thiếu, lồng vào buổi có sẵn — KHÔNG dồn vào Ôn.** Đã đối chiếu nguồn chính thống (HSK 二级考试大纲, chinesetest.cn — xem §16b) trước khi chốt vị trí:
> - **Hỏi đường (问路指路)** → lồng **Bài 2** (giao thông). ✅ Có trong 10 language task chính thức của HSK2.
> - **Hỏi giá, so sánh giá (đổi tên từ "mặc cả" 2026-07-27 — bám đúng khung chính thức "讨论价格/质量/差异", không dạy hẳn kỹ năng trả giá kiểu chợ)** → lồng **Bài 9** (mua trà sữa/đồ uống). ✅ Khớp task chính thức "Shopping: discuss price/quality/differences".
> - **Giới thiệu bản thân/gia đình sâu (2-3 phút, dùng ngữ pháp mới)** → lồng **Bài 5** (thăm nhà bạn TQ). ✅ Khớp topic chính thức "Family".
> - **Đặt khách sạn** → lồng **Bài 3** (du lịch Tây An). ⚠️ **NGOÀI phạm vi chính thức HSK2** — không có trong 10 task/17 task đã tra được; giữ lại vì đây là mong muốn thực dụng cá nhân của user (không phải yêu cầu thi), đánh dấu rõ trong slide "kỹ năng thực tế bổ sung, ngoài chuẩn thi".
> - **Đặt lịch hẹn (2026-07-27, dời từ Bài 6 → Bài 10)** → lồng **Bài 10** (thi cử, học tập), ghép tự nhiên với ngữ pháp 要/快/快要/就要…了 (vd 我跟老师约好了，下午两点就要见面了). ⚠️ **NGOÀI phạm vi chính thức HSK2** tương tự — lý do dời khỏi Bài 6: ghép với ngữ pháp "sắp diễn ra" hợp lý hơn hẳn so với bối cảnh sinh nhật (vốn khá gượng), đồng thời giữ Bài 6 gọn nhẹ (chỉ 1 điểm ngữ pháp 得).
> - Ôn 2 vẫn giữ **capstone hội thoại** đã có trong thiết kế gốc, nhưng chỉ để **ôn tập/ứng dụng lại** các kỹ năng giao tiếp trên (đã dạy rải rác ở buổi 2/3/5/9/10), không dạy từ/ngữ pháp/tình huống mới.

> **Bảng hệ thống hoá trong 2 buổi Ôn (2026-07-27, theo góp ý user — KHÔNG gom lại thành buổi riêng vì phá vỡ "buổi=bài" và tăng nguy cơ nhiễu giữa các loại bổ ngữ; thay vào đó hệ thống hoá bằng bảng so sánh thuần ôn tập):**
> - **Ôn 1 — bảng bổ ngữ (1/2):** đối chiếu 结果补语 (B3) · 简单趋向补语 (B4) · 状态补语/得 (B6) — cấu trúc, ý nghĩa, ví dụ đặt cạnh nhau.
> - **Ôn 1 — bảng 比较句 (1/2):** 比较句(1)(2) (B7) + 比较句(3) (B8) — liệt kê cả 4 mẫu câu (A比B+adj, A比B+adj+bổ ngữ, A有/没有B, A比B+động từ+得+比+adj).
> - **Ôn 2 — bảng bổ ngữ (2/2, nối Ôn 1 thành bảng tổng 6 loại):** + 时量补语 (B9) · 复合趋向补语 (B14) · 动量补语 (B15).
> - **Ôn 2 — bảng 比较句 (2/2, nối thành bảng tổng 1-8):** + 比较句(4)(5)(6) (B12) + 比较句(7)(8) (B13).
> - Cả 4 bảng đều là **tổng hợp lại nội dung đã dạy**, không giới thiệu cấu trúc/ví dụ mới chưa xuất hiện ở buổi trước đó.

## 5. Nguồn vocab mỗi bài (từ sách chính, không tự nghĩ)

**Không liệt kê vocab tự soạn.** 生词 mỗi bài = trích trực tiếp từ **`raw/New HSK Course 2.pdf`**:
- **词汇表 tổng (trang 141)** = 200 từ chuẩn + 略有扩展 → nguồn chân lý.
- **生词 từng bài** (đầu mỗi bài trong sách) → phân bổ ~12–15 từ/bài.

Ở **Task 0.1** (implementation) sẽ bóc `New HSK Course 2.pdf` (có text layer — pypdf, không cần OCR) ra bảng `汉字 | pinyin | 词性 | nghĩa | bài | trùng HSK1?`, rồi:
1. **Loại/đánh dấu từ trùng HSK1** (ràng buộc cứng §4).
2. **Từ mở rộng động vật/thú cưng** cho Bài 5 (猫/狗/鸟/可爱/养/只… — chọn ngoài HSK1, đánh dấu "mở rộng ngoài 200 từ").
3. Verify tổng ≈ 200 (+扩展), khớp 词汇表 sách.

45 điểm ngữ pháp: theo cột 小语讲堂 (đã liệt kê §4 + file TOC), bóc giải thích + ví dụ từ mục 小语讲堂 mỗi bài.

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
- Bài tập **thêm phần Viết (书写) 3.0**: sắp xếp câu · điền chữ Hán · viết câu ngắn theo mẫu · **viết đoạn ngắn 60–100 chữ theo chủ đề buổi · điền biểu mẫu đơn giản (form) · viết lời nhắn (note) · viết nhật ký ngắn** (4 dạng bổ sung, vá theo tiêu chuẩn đầu ra; luân phiên qua các buổi — không bắt buộc đủ cả 4 dạng mỗi buổi) (tách khỏi HSKK nói).

## 7. Nguồn bài đọc 課文 (LẤY THẲNG TỪ SÁCH — đã có PDF)

**ĐÃ GIẢI QUYẾT:** có `raw/New HSK Course 2.pdf` (**có text layer**) → 課文 **trích trực tiếp từ sách**, KHÔNG cần web-search / tự soạn / fallback nữa.
- Mỗi bài sách có **4 課文** (3 hội thoại + 1 tự sự). Chọn 課文 phù hợp buổi (thường lấy bài đối thoại chính + bài tự sự làm bài đọc).
- Bóc bằng pypdf (text layer sạch). Giữ **nguyên văn sách** → độ chính xác tuyệt đối, không lo bịa.
- Định dạng: 汉字 (nguyên văn) + pinyin + dịch Việt. Audio edge-tts đọc chậm (`-18%`, hội thoại đa giọng), soát 多音字/儿化. (Sách có audio gốc — nếu user cấp file MP3 sách thì ưu tiên; mặc định tự sinh edge-tts.)

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
2. **Nguồn 課文 (cổng a):** trích nguyên văn từ `raw/New HSK Course 2.pdf` (text layer) → cổng duyệt text đã trích.
3. **Experience Designer:** map → `buoiXX.json` (đúng thứ tự block, action title, ghost-deck test).
4. **Assets:** fetch ảnh · (GIF nét tuỳ chọn) · edge-tts audio → soát 多音字/儿化.
5. **Render pptx:** `build_deck.py`.
6. **Bài tập (cổng b/c):** exercise-generator — đủ 听/读/书写 + **Viết 3.0** + HSKK; cổng duyệt script audio; `check_baitap.py`; **cổng kiểm tra đáp án AI**.

## 10. Đặt tên & syllabus index

- Tất cả buổi đánh số 2 chữ số theo bài sách: `buoi01_moian_vitquay`, `buoi02_giaothong`, `buoi03_dulich_xian`, `buoi04_trangphuc_mausac`, `buoi05_thamnha` (lồng động vật/thú cưng), `buoi06_sinhnhat`, `buoi07_thethao`, `buoi08_trinho_sosanh`, `buoi09_douong`, `buoi10_thicu`, `buoi11_monan_yeuthich`, `buoi12_thoitiet`, `buoi13_hoctiengtrung`, `buoi14_letet`, `buoi15_kehoach`; ôn: `on1_bai1-8`, `on2_bai9-15`.
- `output/hsk2/README.md` = bảng syllabus 15 buổi + 2 ôn, map bài sách ↔ folder, ghi rõ chuẩn **3.0** + sách chính (New HSK Course 2)/tham khảo (Hán ngữ 第一册·下). Source of truth.
- `meta.lesson` mỗi JSON: `"HSK2 · Buổi X"`.

## 11. Chiến lược giao (de-risk)

- **Sản xuất tuần tự, KHÔNG làm 2 pilot rồi hàng loạt (quyết định 2026-07-27, theo user):** dù buổi nào user cũng phải review + điều chỉnh, nên đi từng buổi đúng thứ tự sách, **mỗi buổi có 1 cổng duyệt trọn gói riêng** (pptx + worksheet + bài đọc) trước khi bắt đầu buổi kế tiếp. Không có khái niệm "pilot" hay "sản xuất hàng loạt sau khi duyệt khuôn".
- Thứ tự sản xuất: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → [Ôn 1] → 09 → 10 → 11 → 12 → 13 → 14 → 15 → [Ôn 2].
- **Phase cuối:** trang từ vựng theo buổi (§14) sau khi vocab đã chốt.

## 12. Tiêu chí hoàn thành (verification)

- [ ] 15 buổi + 2 ôn đủ deliverable (slide pptx + audio, baitap 4 phần **có Viết 3.0**, bài đọc + audio, footer Hán ngữ 第一册·下).
- [ ] Mỗi buổi có block **10 câu khẩu ngữ thông dụng**.
- [ ] **Không từ nào trùng 150 từ HSK1** trong danh sách 生词 (đối chiếu checklist).
- [ ] Tổng vocab khớp 词汇表 sách (~200 + mở rộng), + động vật/thú cưng lồng ở Bài 5, không trùng giữa các buổi.
- [ ] 45 điểm ngữ pháp (小语讲堂) đều có buổi phụ trách (đối chiếu mục lục sách).
- [ ] Mỗi pptx render + mở được.
- [ ] Audio soát 多音字/儿化, đọc chậm.
- [ ] 課文: nguyên văn trích từ `raw/New HSK Course 2.pdf` (text layer), đúng bài.
- [ ] Bài tập qua cổng kiểm tra đáp án AI.
- [ ] `README.md` syllabus đầy đủ, ghi rõ chuẩn 3.0.
- [ ] Trang từ vựng `output/study/hsk2/buoiXX/tu-vung.html` sinh đủ, flashcard + 🔊 chạy (Leitner trung tính, không neo Activation vault).
- [ ] Bài 4 có dạy **把字句 cơ bản**; Bài 11 có **被字句 đơn giản**; Bài 12 có **连…都/也** (ngữ pháp bổ sung ngoài sách, đánh dấu rõ trong slide buổi tương ứng — KHÔNG ở 2 buổi Ôn).
- [ ] Bài 2 (hỏi đường), Bài 3 (khách sạn — ngoài chuẩn), Bài 5 (giới thiệu bản thân/gia đình sâu), Bài 9 (hỏi giá/so sánh giá), Bài 10 (đặt lịch hẹn — ngoài chuẩn) có lồng đủ nội dung giao tiếp bổ sung; 2 mục ngoài chuẩn đánh dấu rõ trong slide.
- [ ] Bài tập Viết luân phiên đủ 4 dạng bổ sung (đoạn 60–100 chữ, điền form, lời nhắn, nhật ký) qua các buổi — không chỉ dừng ở câu ngắn.
- [ ] Mỗi buổi bài tập phần 读 có ≥1 văn bản thực tế (tin nhắn/biển báo/thực đơn/quảng cáo) tự soạn theo chủ đề, không lấy từ sách.
- [ ] 2 buổi Ôn chỉ ôn tập nội dung đã học (kể cả capstone Ôn 2) — không xuất hiện từ/ngữ pháp/tình huống mới chưa dạy ở buổi trước đó.

## 13. Trang từ vựng HSK2 theo buổi (vocab-study-style)

- Như HSK1 §14: mỗi buổi 1 trang Quizlet `output/study/hsk2/buoiXX/tu-vung.html`, tái dùng engine vocab-study (bảng 生词 + flashcard active-recall + Leitner + chiết tự + mẹo nhớ Việt + 🔊).
- **Bỏ neo Activation vault** (dữ liệu Activation là HSK6 cá nhân user) → Leitner khởi động box 1. Nguồn từ = 生词 trong `buoiXX.json`. KHÔNG đọc `raw/Từ vựng.xlsx`.
- **Phase cuối**, sau khi vocab 15 buổi chốt.

## 14. Rủi ro & mở

- **Gap đầu vào HSK1→HSK2 — ĐÃ GIẢI QUYẾT:** user sẽ **build lại HSK1 theo chuẩn 3.0** (việc riêng, sau). Do đó HSK2 3.0 cứ giả định đầu vào HSK1 3.0 (~300 từ) như sách chính, **không cần buổi cầu nối**. Buổi 1 là chủ đề HSK2 đầy đủ.
- **Nguyên văn 課文 — ĐÃ GIẢI QUYẾT:** có `raw/New HSK Course 2.pdf` (text layer) → trích thẳng, không cần web-search/tự soạn (§7).
- **Con số 3.0:** chốt bằng 词汇表 sách (trang 141) + 小语讲堂 ở Task 0.1. (200 từ + mở rộng, 45 ngữ pháp — đã xác minh nguồn chính chủ.)
- **Audio gốc sách:** New HSK Course 2 có audio chính thức. Mặc định tự sinh edge-tts; nếu user cấp MP3 gốc → ưu tiên dùng.
- **Phần Viết (书写) 3.0 — ĐÃ QUYẾT (2026-07-27):** ngoài sắp câu/điền chữ/viết câu ngắn, bổ sung 4 dạng mới — đoạn 60–100 chữ, điền form, lời nhắn, nhật ký — theo tiêu chuẩn đầu ra. Task 0.2 chuyển từ "đánh giá" sang "mở rộng schema exercise-generator" nếu chưa hỗ trợ.
- **Ngữ pháp bổ sung ngoài sách — ĐÃ QUYẾT (2026-07-27, sửa lại):** 把 lồng Bài 4, 被 lồng Bài 11, 连…都/也 lồng Bài 12 — không có trong 45 điểm sách chính nhưng nằm trong tiêu chuẩn đầu ra user yêu cầu. **Không dạy ở Ôn** (Ôn chỉ ôn tập, không học mới — user chỉnh 2026-07-27).
- **Giao tiếp thiếu (hẹn/hỏi đường/mặc cả/khách sạn/giới thiệu bản thân sâu) — ĐÃ QUYẾT (2026-07-27, sửa lại), ĐÃ ĐỐI CHIẾU NGUỒN CHÍNH THỐNG (2026-07-27, xem §16b):** lồng vào buổi 2/3/5/9/10 tương ứng, không thêm buổi, không dồn vào Ôn. 3/5 mục có trong chuẩn thi chính thức (hỏi đường, hỏi giá/so sánh giá, giới thiệu gia đình); 2/5 mục (khách sạn, đặt lịch hẹn) NGOÀI chuẩn thi — giữ lại theo yêu cầu thực dụng cá nhân của user, đánh dấu rõ trong slide.
- **Đọc thực tế (tin nhắn/biển báo/thực đơn/quảng cáo) — ĐÃ QUYẾT (2026-07-27):** thêm ≥1 mục/buổi trong phần 读 của bài tập, tự soạn theo chủ đề (khác 課文 nguyên văn sách).
- **Hán ngữ mapping — ĐÃ CÓ:** user cấp `raw/Hán ngữ 2.pdf` (=《汉语教程》第一册·下, L16–30); mục lục đã OCR + map vào §4/§8. Còn thiếu điểm **比** (khả năng ở 第二册) → nếu cần, user cấp thêm 第二册; nếu không, footer buổi 2/6/7 ghi rõ 比 ngoài phạm vi sách này.

## 15. Bước tiếp theo

Sau khi user **duyệt spec này** → viết **implementation plan** (mô phỏng `2026-07-19-hsk1-full-course.md`): Phase 0 (checklist phủ từ 3.0 + chống trùng HSK1, README syllabus, đánh giá schema Viết) → Procedure P → sản xuất tuần tự từng buổi (mỗi buổi 1 cổng duyệt, xem §11) → phase trang từ vựng.

## 16b. Nguồn chính thống đối chiếu cho phần "bổ sung giao tiếp" (2026-07-27)

Trước khi chốt vị trí lồng ghép ở §4, đã tra cứu để tránh tự bịa phạm vi:

- **官方 HSK 二级考试大纲** (chinesetest.cn, tải và bóc trực tiếp bằng pypdf) — trang 3 xác nhận: *"HSK（二级）...涉及职业工作、文化、体验感悟等 6 大话题，涵盖**问路指路**、描述商品信息、**点菜**等 10 个语言任务"* → **问路指路 (hỏi đường) là 1 trong 10 task chính thức, có căn cứ vững**. Tài liệu này là bản đại cương chung (300 từ, khớp chuẩn 2.0 cũ hơn là 3.0 500 từ) — chỉ nêu tên 3/10 task, chưa chắc là bản 3.0 mới nhất.
- **Nguồn phụ (passhsk.app, bên thứ 3, CHƯA verify với bản gốc 3.0):** liệt kê 17 task HSK2 3.0 — có "Travel: give/ask directions" và "Shopping: discuss price/quality/differences" (khớp hỏi giá/so sánh giá) và "Family: discuss relationships" (khớp giới thiệu gia đình); **không có** mục đặt khách sạn hay đặt lịch hẹn dịch vụ nào.
- **Kết luận:** hỏi đường / hỏi giá-so sánh giá / giới thiệu gia đình sâu = có căn cứ chính thống. Đặt khách sạn / đặt lịch hẹn = ngoài phạm vi chuẩn thi, giữ lại vì mục tiêu "dùng được" thực dụng của user (không phải yêu cầu thi), đã đánh dấu rõ ở §4.

## 16c. Xác minh 3 điểm ngữ pháp bị nghi thiếu — 一边…一边/越来越/又…又 (2026-07-27)

Có ý kiến review cho rằng HSK2 "thiếu" 3 điểm ngữ pháp phổ biến này. Đã tải trực tiếp **văn bản gốc chính thức** để kiểm chứng thay vì suy đoán:

- **Nguồn:** `新版HSK考试大纲（词汇、汉字、语法）.pdf` (中外语言交流合作中心/汉考国际 phát hành, host tại `hsk.cn-bj.ufileos.com/3.0/`, Last-Modified 2025-12-25 — đúng là **bản 3.0 chính thức**, 330 trang, bóc bằng pypdf).
- **Kết quả:** cả 3 điểm đều nằm trong mục **"HSK（三级）语法"** (trang 316-318 của PDF — ngay sau khi mục "HSK（二级）语法" kết thúc ở trang 315), cụ thể:
  - `越来越` — 固定短语, mục **HSK 三级**.
  - `一边……，一边……` và `又……，又……` — 复句 (并列复句), mục **HSK 三级**.
- **Kết luận: KHÔNG phải gap của HSK2 — đây là ngữ pháp cấp 3, HSK2 đúng khi không dạy.** Ý kiến review trước đó không chính xác; không cần vá thêm gì cho 3 điểm này.
- **Lợi ích phụ:** đã đối chiếu toàn bộ mục "HSK（二级）语法" chính thức (trang 313-315) với 45 điểm của New HSK Course 2 — khớp tốt (还是…吧, 都…了, 兼语句, 双宾语句, 虽然…但是, 因为…所以, 一…就…, 着, 过, 比较句 nhóm 1, 是…的句, 有字句, 存现句... đều xuất hiện đúng cấp). Không phát hiện gap chính thức nào khác ngoài 4 điểm đã vá (把/被/连 + phần giao tiếp).

## 16. Nguồn tra cứu (3.0)

- New HSK Course / HSK 3.0 launch (FLTRP, 11/2025): [fltrp.com](https://www.fltrp.com/c/2025-11-20/540070.shtml) · [newhskcourse.com](https://newhskcourse.com/)
- HSK 3.0 vs 2.0, số từ cấp 2: [hanzistroke.com/blog/new-hsk-3-guide](https://www.hanzistroke.com/blog/new-hsk-3-guide) · [khanjischool.com](https://khanjischool.com/blog/chinese/new-hsk-30-2026-vocabulary-levels-exams-and-official-textbooks)
- HSK2 3.0 yêu cầu/đề cương + phần Viết: [passhsk.app/hsk-2-requirements-2026](https://www.passhsk.app/hsk-2-requirements-2026) · [mandarinzone.com](https://www.mandarinzone.com/hsk-level-2-all-you-need-to-know-about-hsk-2/)
- Ngữ pháp 3.0 cấp 2: [mandarinbean.com/new-hsk-grammar](https://mandarinbean.com/new-hsk-grammar/) · [hskstory.com/guides/hsk-30-syllabus](https://hskstory.com/guides/hsk-30-syllabus)
- New HSK Course 2 (15 bài, ~200 từ, 45 ngữ pháp): kết quả tìm kiếm FLTRP/purpleculture (2026)
- HSK Standard Course 2 (2.0, đối chứng): [hskstandardcourse.com](https://www.hskstandardcourse.com/hsk-standard-course-level-2/hsk-standard-course-2-textbook/)
