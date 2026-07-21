# HSK1 3.0 — Đề xuất tái thiết kế theo chủ đề (proposal, chưa sản xuất)

**Ngày:** 2026-07-21
**Trạng thái:** DRAFT — proposal nghiên cứu, chờ user duyệt trước khi viết implementation plan
**Thay thế cho:** `docs/superpowers/specs/2026-07-19-hsk1-full-course-design.md` (bản 12 buổi / 150 từ / HSK Standard Course — bản 2.0 cũ)

---

## 0. Tóm tắt cho người duyệt nhanh

- Xác nhận **HSK 3.0 Level 1 = 500 từ** là đúng với **bản dự thảo 2021** (GF 0025-2021, Bộ Giáo dục TQ công bố 31/3/2021, hiệu lực 1/7/2021). NHƯNG có một phát hiện quan trọng cần user quyết định — xem **§1.2 cảnh báo**: có dấu hiệu một **bản "final" 2025** đã rút Level 1 xuống còn **300 từ**, và giáo trình chính **New HSK Course 1** (ISBN 9787521367744) hiện đang bám theo **300 từ / 40 điểm ngữ pháp** đó, không phải 500.
- Đã dựng danh sách ~500 từ (thực tế 506 sau khi bổ sung 6 từ phát hiện thiếu qua đối chiếu — xem §1.3), chia 26 nhóm chủ đề (§2).
- Đã lấy được 15 课文 New HSK Course 1 (tên + chủ đề), map vào cụm chủ đề (§3).
- Đề xuất **26 buổi** (buổi 1 ngữ âm giữ nguyên + 25 buổi chủ đề) (§4).
- Review buổi 06/10/12 cũ: **buổi06 REUSE tốt, buổi10 REWORK một phần (màu sắc gần như ngoài phạm vi), buổi12 REUSE phần ngữ pháp nhưng REWORK phần từ vựng thời tiết/mùa (phần lớn ngoài phạm vi 500 từ)** — chi tiết §5.

---

## 1. Nguồn & số liệu

### 1.1 Số liệu 500 từ — xác nhận nguồn

| Nguồn | Số từ nói | Ghi chú |
|---|---|---|
| [HSK Tracker — New HSK 3.0 Level 1 vocabulary list](https://www.hsktracker.com/en/new-hsk-vocabulary-list-level-1/) | **500** ("500 Total Vocabulary items — 206 Total Single Words + 294 Total Compound Words") | Nguồn chính dùng để dựng danh sách §2 |
| [Everyday Chinese — NEW(3.0) HSK 1 Vocabulary](https://www.everydaychinese.com/youtube-lessons/new-hsk-1.html) | 500 ("Learn your first 500 Chinese vocabulary words in New Standard level 1") | Xác nhận chéo con số 500, không lấy được list chi tiết (phải đăng ký email) |
| [Mandarin Bean — New HSK Vocabulary](https://mandarinbean.com/new-hsk-vocabulary/) | Trước đây 500 (2021), hiện trang đã cập nhật xuống 300 (2026) | Xem §1.2 — chính trang này là bằng chứng có bản sửa đổi |
| [Khanji School — New HSK 3.0 2026](https://khanjischool.com/blog/chinese/new-hsk-30-2026-vocabulary-levels-exams-and-official-textbooks) | "HSK 3.0 (2021): 500 từ Level 1" vs "HSK 3.0 (2026): 300 từ Level 1" | Nguồn giải thích rõ nhất về 2 phiên bản |
| [HSK Story — Complete HSK 3.0 Vocabulary Guide](https://hskstory.com/guides/hsk-30-vocabulary-complete) | HSK1 = 300 (bản "2025 final standard"), cảnh báo "2021 draft had significant differences... 36-60% turnover ở level 1-4" | Nguồn cảnh báo rõ nhất |

**Kết luận:** con số **500 mà user chốt là đúng với bản dự thảo 2021 (GF 0025-2021)** — đây là bản đã được nhiều giáo trình/app tham chiếu suốt 2021-2025 và đúng như user đã quyết định dùng làm baseline "full coverage". Cross-check ≥ 2 nguồn độc lập (HSK Tracker + Everyday Chinese) đều xác nhận 500.

### 1.2 ⚠️ Cảnh báo cần user quyết định: có bản sửa đổi 2025 rút xuống 300 từ

Đây là phát hiện quan trọng nhất của vòng nghiên cứu này, nằm ngoài phạm vi "đã quyết" nhưng ảnh hưởng trực tiếp đến việc chọn nguồn 课文:

- Theo Khanji School và HSK Story, cuối 2025 (Hội nghị Global HSK Partners tại Bắc Kinh) đã công bố **"新版HSK考试大纲" (2025 final standard)** rút Level 1 từ 500 → **300 từ**. Pilot exam dự kiến 31/1/2026, triển khai đại trà nửa cuối 2026.
- **New HSK Course 1** (chính là giáo trình user chọn làm textbook chính, ISBN 9787521367744) — theo mô tả trên newhskcourse.com — **bám sát 300 từ + 40 điểm ngữ pháp** của bản 2025, KHÔNG PHẢI 500. Điều này có nghĩa: giáo trình sẽ không có 课文 phủ khoảng 200 từ "500-only" (từ chỉ có trong bản dự thảo 2021, đã bị bản 2025 loại bỏ).
- Đối chiếu tay giữa danh sách 500 (hsktracker, bản 2021) và danh sách 300 (mandarinbean, bản đã cập nhật 2025) trong quá trình dựng §2, phát hiện **~200/500 từ không xuất hiện trong danh sách 300** — khớp với cảnh báo "36-60% turnover" ở trên. Một vài ví dụ tiêu biểu KHÔNG có trong bản 300 (chỉ có trong 500): 差、动作、告诉、教、开会、开玩笑、考试、课本、课文、记得、见面、老人、身体、准备、认真、试、知识、重要、走路...
- **Không tự quyết thay** — nêu 2 hướng để user chọn ở lần review:
  1. **Giữ nguyên quyết định cũ (500 từ, bản 2021)** — coi đây là "phiên bản đầy đủ hơn", 300 từ 2025 chỉ là tập con. Ưu điểm: học rộng hơn, không lãng phí công nếu bản 2025 lại đổi tiếp. Nhược điểm: ~40% nội dung không khớp giáo trình chính thức 300-từ mà New HSK Course 1 nhắm tới; nếu học viên thi theo chuẩn 2025 sẽ học dư ~200 từ không cần.
  2. **Chuyển sang bám 300 từ (bản 2025 final)** — khớp đúng New HSK Course 1 + đề thi thực tế 2026. Nhược điểm: phải dựng lại toàn bộ §2/§4 của proposal này theo danh sách 300.
- Đề xuất **giữ hướng 500 như user đã chốt** cho proposal này (không re-litigate theo yêu cầu), nhưng gắn cờ rõ trong syllabus rằng ~200 từ là "mở rộng ngoài core 300" để sau này nếu cần thu hẹp thì có thể cắt nhanh (xem đánh dấu ở §2).

### 1.3 Chất lượng danh sách 500 từ — giới hạn cần biết

Danh sách §2 được dựng bằng cách fetch trang hsktracker.com 3 lần (đoạn 1–200, 200–350, 350–500) qua công cụ tóm tắt tự động — **không phải trích xuất máy móc 100% chính xác từ dữ liệu gốc**. Trong lúc đối chiếu chéo với danh sách 300 (mandarinbean), phát hiện **6 từ cơ bản bị thiếu sót** trong lần trích đầu (rất có thể do lỗi tóm tắt của công cụ fetch, không phải do các từ này thực sự không thuộc HSK1): **你好, 可以, 卖, 女士, 怎么样, 千**. Đã bổ sung thủ công 6 từ này vào §2 (đánh dấu *[bổ sung]*), nâng tổng từ đã liệt kê lên **506**.

**Khuyến nghị trước khi dùng danh sách này làm checklist sản xuất chính thức:** chạy một lượt đối chiếu tự động (không qua tool tóm tắt) với nguồn dữ liệu có cấu trúc, ví dụ repo GitHub [`drkameleon/complete-hsk-vocabulary`](https://github.com/drkameleon/complete-hsk-vocabulary) (file `wordlists/inclusive/new/1.json`) — repo này có JSON đầy đủ nhưng do file lớn nên trong phiên nghiên cứu này chỉ fetch được ~100-130 dòng đầu mỗi lần (giới hạn của công cụ fetch), không đủ để dùng làm nguồn chính, nhưng dùng để **diff xác nhận lại lần cuối** thì rất đáng làm (ví dụ tải file về máy và so sánh trực tiếp, không qua model tóm tắt).

---

## 2. Danh sách ~500 từ HSK 3.0 Level 1 theo nhóm chủ đề

Chú thích cột "Phạm vi": không đánh dấu = có trong cả bản 500 (2021) và bản lõi 300 (2025 final); **⚠️500-only** = chỉ có trong bản 500, không có trong bản lõi 300 (tham khảo §1.2 khi cần thu hẹp).

### C1 — Đại từ nhân xưng & câu trần thuật cơ bản (22 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 我 | wǒ | tôi |
| 你 | nǐ | bạn |
| 他 | tā | anh ấy |
| 她 | tā | cô ấy |
| 我们 | wǒmen | chúng tôi |
| 你们 | nǐmen | các bạn |
| 他们 | tāmen | họ (nam) |
| 她们 | tāmen | họ (nữ) |
| 您 | nín | ngài, bác (kính ngữ) |
| 们 | men | trợ từ số nhiều |
| 是 | shì | là |
| 不 | bù | không |
| 有 | yǒu | có |
| 没 | méi | không (có) |
| 没有 | méiyǒu | không có |
| 也 | yě | cũng |
| 都 | dōu | đều |
| 很 | hěn | rất |
| 太 | tài | quá |
| 非常 | fēicháng | rất, vô cùng |
| 真 | zhēn | thật là |
| 在 | zài | ở, đang |

### C2 — Chào hỏi, lịch sự, làm quen (19 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 你好 | nǐ hǎo | *[bổ sung]* xin chào |
| 谢谢 | xièxie | cảm ơn |
| 不客气 | bú kèqi | không có gì |
| 对不起 | duìbuqǐ | xin lỗi |
| 没关系 | méi guānxi | không sao |
| 没什么 | méi shénme | không có gì |
| 没事儿 | méi shìr | không sao |
| 再见 | zàijiàn | tạm biệt |
| 请 | qǐng | mời, xin |
| 请进 | qǐng jìn | mời vào |
| 请问 | qǐngwèn | xin hỏi |
| 请坐 | qǐng zuò | mời ngồi |
| 叫 | jiào | gọi, tên là |
| 名字 | míngzi | tên |
| 介绍 | jièshào | ⚠️500-only giới thiệu |
| 别 | bié | đừng |
| 别的 | biéde | cái khác |
| 别人 | biérén | người khác |
| 行 | xíng | được, ổn |

### C3 — Chỉ định & nghi vấn (22 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 这 | zhè | này |
| 这个 | zhège | ⚠️500-only cái này |
| 这里 | zhèlǐ | chỗ này |
| 这儿 | zhèr | đây |
| 这些 | zhèxiē | những cái này |
| 那 | nà | đó, kia |
| 那个 | nàge | ⚠️500-only cái đó |
| 那里 | nàlǐ | chỗ đó |
| 那儿 | nàr | đó |
| 那些 | nàxiē | những cái đó |
| 谁 | shéi | ai |
| 什么 | shénme | gì |
| 哪 | nǎ | nào |
| 哪个 | nǎge | ⚠️500-only cái nào |
| 哪里 | nǎlǐ | đâu |
| 哪儿 | nǎr | đâu |
| 哪些 | nǎxiē | những cái nào |
| 怎么 | zěnme | thế nào, sao |
| 怎么样 | zěnmeyàng | *[bổ sung]* thế nào |
| 多少 | duōshao | bao nhiêu |
| 吗 | ma | trợ từ nghi vấn |
| 呢 | ne | trợ từ nghi vấn/tiếp diễn |
| 吧 | ba | trợ từ đề nghị/phỏng đoán |

### C4a — Số đếm 0–1000 & lượng từ cơ bản (24 từ) — buổi 05
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 一 | yī | một |
| 二 | èr | hai |
| 三 | sān | ba |
| 四 | sì | bốn |
| 五 | wǔ | năm |
| 六 | liù | sáu |
| 七 | qī | bảy |
| 八 | bā | tám |
| 九 | jiǔ | chín |
| 十 | shí | mười |
| 百 | bǎi | trăm |
| 千 | qiān | *[bổ sung]* nghìn |
| 零 | líng | số không |
| 两 | liǎng | hai (trước lượng từ) |
| 第 | dì | thứ (số thứ tự) |
| 个 | gè | cái (lượng từ vạn năng) |
| 口 | kǒu | người (đếm người nhà) |
| 本 | běn | quyển (lượng từ) |
| 件 | jiàn | bộ, việc (lượng từ) |
| 张 | zhāng | tấm, cái phẳng (lượng từ) |
| 杯 | bēi | cốc (lượng từ) |
| 次 | cì | lần (lượng từ) |
| 些 | xiē | vài, một số |
| 岁 | suì | tuổi |

### C4b — Lượng từ mở rộng, tiền tệ, 一点儿/有点儿 (14 từ) — buổi 06
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 块 | kuài | đồng (tiền), cục |
| 毛 | máo | hào (đơn vị tiền) |
| 元 | yuán | đồng (tiền) |
| 半 | bàn | nửa |
| 半年 | bànnián | ⚠️500-only nửa năm |
| 半天 | bàntiān | ⚠️500-only nửa ngày, rất lâu |
| 一半 | yíbàn | một nửa |
| 一下 / 一下儿 | yíxià / yíxiàr | một chút, thử xem |
| 一点儿 | yìdiǎnr | một chút |
| 有点儿 | yǒudiǎnr | hơi (chê) |
| 一些 | yìxiē | một số, vài |
| 有些 | yǒuxiē | có một số |
| 有（一）些 | yǒu (yì) xiē | ⚠️500-only có một số |

### C5 — Gia đình & bạn bè (18 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 爸爸 | bàba | bố |
| 妈妈 | māma | mẹ |
| 爷爷 | yéye | ⚠️500-only ông nội |
| 奶奶 | nǎinai | ⚠️500-only bà nội |
| 儿子 | érzi | con trai |
| 女儿 | nǚ'ér | con gái |
| 哥哥 | gēge | anh trai |
| 姐姐 | jiějie | chị gái |
| 弟弟 | dìdi | em trai |
| 妹妹 | mèimei | em gái |
| 孩子 | háizi | con cái, trẻ em |
| 家 | jiā | nhà |
| 家里 | jiālǐ | ⚠️500-only trong nhà |
| 家人 | jiārén | người nhà |
| 朋友 | péngyou | bạn bè |
| 男朋友 | nánpéngyou | bạn trai |
| 女朋友 | nǚpéngyou | bạn gái |
| 同学 | tóngxué | bạn học |

### C6 — Con người: giới tính, tuổi tác, sức khỏe (25 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 男 | nán | nam |
| 女 | nǚ | nữ |
| 男人 | nánrén | ⚠️500-only đàn ông |
| 女人 | nǚrén | ⚠️500-only phụ nữ |
| 男孩儿 | nánháir | ⚠️500-only con trai (bé) |
| 女孩儿 | nǚháir | ⚠️500-only con gái (bé) |
| 男生 | nánshēng | ⚠️500-only nam sinh |
| 女生 | nǚshēng | ⚠️500-only nữ sinh |
| 先生 | xiānsheng | ông, quý ông |
| 小姐 | xiǎojiě | ⚠️500-only cô (xưng hô) |
| 女士 | nǚshì | *[bổ sung]* quý bà |
| 老 | lǎo | ⚠️500-only già |
| 老人 | lǎorén | ⚠️500-only người già |
| 小孩儿 | xiǎoháir | ⚠️500-only trẻ con |
| 小朋友 | xiǎopéngyou | bạn nhỏ |
| 人 | rén | người |
| 身体 | shēntǐ | ⚠️500-only cơ thể, sức khỏe |
| 身上 | shēnshàng | ⚠️500-only trên người |
| 病 | bìng | bệnh |
| 病人 | bìngrén | ⚠️500-only bệnh nhân |
| 看病 | kànbìng | khám bệnh |
| 生病 | shēngbìng | bị bệnh |
| 生气 | shēngqì | ⚠️500-only giận |
| 累 | lèi | ⚠️500-only mệt |
| 医院 | yīyuàn | bệnh viện |

### C7+C8 — Quốc gia/ngôn ngữ & nghề nghiệp/công việc (25 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 中国 | Zhōngguó | Trung Quốc |
| 国 | guó | nước |
| 国家 | guójiā | ⚠️500-only quốc gia |
| 国外 | guówài | ⚠️500-only nước ngoài |
| 外国 | wàiguó | ⚠️500-only nước ngoài |
| 北京 | Běijīng | ⚠️500-only Bắc Kinh |
| 汉语 | Hànyǔ | tiếng Trung |
| 汉字 | Hànzì | chữ Hán |
| 中文 | Zhōngwén | tiếng Trung (văn) |
| 外语 | wàiyǔ | ⚠️500-only ngoại ngữ |
| 工作 | gōngzuò | công việc, làm việc |
| 工人 | gōngrén | ⚠️500-only công nhân |
| 医生 | yīshēng | bác sĩ |
| 上班 | shàngbān | đi làm |
| 下班 | xiàbān | tan làm |
| 忙 | máng | bận |
| 休息 | xiūxi | nghỉ ngơi |
| 请假 | qǐngjià | ⚠️500-only xin nghỉ phép |
| 放假 | fàngjià | ⚠️500-only nghỉ lễ |
| 开会 | kāihuì | ⚠️500-only họp |

### C9 — Trường học & học tập (17 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 学校 | xuéxiào | trường học |
| 学生 | xuésheng | học sinh |
| 大学 | dàxué | đại học |
| 大学生 | dàxuéshēng | sinh viên đại học |
| 中学 | zhōngxué | trung học |
| 中学生 | zhōngxuéshēng | học sinh trung học |
| 小学 | xiǎoxué | tiểu học |
| 小学生 | xiǎoxuéshēng | học sinh tiểu học |
| 学院 | xuéyuàn | ⚠️500-only học viện |
| 学 | xué | học |
| 学习 | xuéxí | học tập |
| 读 | dú | đọc |
| 读书 | dúshū | đọc sách, đi học |
| 教 | jiāo | ⚠️500-only dạy |
| 老师 | lǎoshī | giáo viên |
| 上学 | shàngxué | đi học |
| 教学楼 | jiàoxuélóu | ⚠️500-only tòa nhà giảng đường |

### C10 — Lớp học, thi cử, chữ viết (13 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 课 | kè | tiết học, bài học |
| 课本 | kèběn | ⚠️500-only sách giáo khoa |
| 课文 | kèwén | ⚠️500-only bài khóa |
| 上课 | shàngkè | lên lớp, học |
| 下课 | xiàkè | tan học |
| 听写 | tīngxiě | ⚠️500-only chính tả |
| 考 | kǎo | ⚠️500-only thi |
| 考试 | kǎoshì | ⚠️500-only kỳ thi |
| 试 | shì | ⚠️500-only thử |
| 写 | xiě | viết |
| 字 | zì | chữ |
| 知识 | zhīshi | ⚠️500-only kiến thức |
| 准备 | zhǔnbèi | ⚠️500-only chuẩn bị |

### C11 — Thời gian: ngày/tháng/năm (18 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 年 | nián | năm |
| 月 | yuè | tháng |
| 日 | rì | ngày |
| 号 | hào | số, ngày (trong tháng) |
| 星期 | xīngqī | tuần |
| 星期日 | xīngqīrì | chủ nhật |
| 星期天 | xīngqītiān | chủ nhật |
| 今年 | jīnnián | năm nay |
| 明年 | míngnián | năm sau |
| 去年 | qùnián | năm ngoái |
| 今天 | jīntiān | hôm nay |
| 明天 | míngtiān | ngày mai |
| 昨天 | zuótiān | hôm qua |
| 前天 | qiántiān | ⚠️500-only hôm kia |
| 后天 | hòutiān | ⚠️500-only ngày kia |
| 新年 | xīnnián | ⚠️500-only năm mới |
| 生日 | shēngrì | sinh nhật |
| 天 | tiān | ngày |

### C12 — Thời gian: buổi trong ngày & giờ giấc (18 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 上午 | shàngwǔ | buổi sáng |
| 中午 | zhōngwǔ | buổi trưa |
| 下午 | xiàwǔ | buổi chiều |
| 晚上 | wǎnshang | buổi tối |
| 早上 | zǎoshang | buổi sáng sớm |
| 白天 | báitiān | ban ngày |
| 晚 | wǎn | ⚠️500-only muộn |
| 早 | zǎo | ⚠️500-only sớm |
| 点 | diǎn | giờ |
| 分 | fēn | phút |
| 时候 | shíhou | lúc, thời điểm |
| 时间 | shíjiān | thời gian |
| 小时 | xiǎoshí | giờ (thời lượng) |
| 现在 | xiànzài | bây giờ |
| 先 | xiān | ⚠️500-only trước tiên |
| 一会儿 | yíhuìr | ⚠️500-only một lát |
| 马上 | mǎshàng | ⚠️500-only ngay lập tức |

### C13+C14 — 了/过/正在/着 (thể/thời) + Thời tiết (22 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 了 | le | trợ từ hoàn thành/thay đổi |
| 过 | guò | trợ từ kinh nghiệm "đã từng" |
| 正 | zhèng | ⚠️500-only đúng lúc |
| 正在 | zhèngzài | đang |
| 着 | zhe | ⚠️500-only trợ từ tiếp diễn |
| 还 | hái | vẫn, còn |
| 再 | zài | lại, nữa |
| 常 | cháng | ⚠️500-only thường |
| 常常 | chángcháng | ⚠️500-only thường xuyên |
| 就 | jiù | ⚠️500-only thì, liền |
| 快 | kuài | ⚠️500-only nhanh, sắp |
| 最 | zuì | ⚠️500-only nhất |
| 最好 | zuìhǎo | ⚠️500-only tốt nhất |
| 最后 | zuìhòu | ⚠️500-only cuối cùng |
| 天气 | tiānqì | thời tiết |
| 下雨 | xiàyǔ | mưa |
| 雨 | yǔ | mưa (danh từ) |
| 下雪 | xiàxuě | ⚠️500-only có tuyết |
| 雪 | xuě | ⚠️500-only tuyết |
| 冷 | lěng | lạnh |
| 热 | rè | nóng |
| 风 | fēng | ⚠️500-only gió |

> **Lưu ý quan trọng:** HSK 3.0 Level 1 (500 từ) **KHÔNG có từ vựng mùa** (không có 春天/夏天/秋天/冬天) và **không có** 晴天/阴天/刮风/暖和/凉快/度 — những từ này thuộc HSK2 trở lên. Buổi 12 cũ (2.0) dùng toàn bộ nhóm này → xem cảnh báo REWORK ở §5.3.

### C15 — Ăn uống (23 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 吃 | chī | ăn |
| 吃饭 | chīfàn | ăn cơm |
| 喝 | hē | uống |
| 菜 | cài | món ăn, rau |
| 茶 | chá | trà |
| 米饭 | mǐfàn | cơm (gạo) |
| 面包 | miànbāo | bánh mì |
| 面条儿 | miàntiáor | mì sợi |
| 包子 | bāozi | bánh bao |
| 饺子 | jiǎozi | sủi cảo |
| 鸡蛋 | jīdàn | trứng gà |
| 水 | shuǐ | nước |
| 水果 | shuǐguǒ | hoa quả |
| 牛奶 | niúnǎi | sữa bò |
| 早饭 | zǎofàn | cơm sáng |
| 午饭 | wǔfàn | cơm trưa |
| 晚饭 | wǎnfàn | cơm tối |
| 饭 | fàn | cơm |
| 饭店 | fàndiàn | nhà hàng |
| 饿 | è | ⚠️500-only đói |
| 渴 | kě | ⚠️500-only khát |
| 做饭 | zuò fàn | nấu cơm |
| 好吃 | hǎochī | ngon |

### C16 — Mua sắm & tiền bạc (15 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 买 | mǎi | mua |
| 卖 | mài | *[bổ sung]* bán |
| 钱 | qián | tiền |
| 钱包 | qiánbāo | ⚠️500-only ví tiền |
| 贵 | guì | đắt |
| 便宜 | piányi | rẻ |
| 商店 | shāngdiàn | cửa hàng |
| 商场 | shāngchǎng | ⚠️500-only trung tâm thương mại |
| 东西 | dōngxi | đồ vật |
| 衣服 | yīfu | quần áo |
| 穿 | chuān | mặc |
| 漂亮 | piàoliang | đẹp |
| 好看 | hǎokàn | đẹp, dễ nhìn |
| 好听 | hǎotīng | ⚠️500-only hay (nghe) |
| 好玩儿 | hǎowánr | vui, thú vị |

### C17 — Nhà ở & đồ vật (18 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 房子 | fángzi | ⚠️500-only nhà (căn nhà) |
| 房间 | fángjiān | phòng |
| 床 | chuáng | ⚠️500-only giường |
| 桌子 | zhuōzi | cái bàn |
| 椅子 | yǐzi | ghế |
| 门 | mén | ⚠️500-only cửa |
| 门口 | ménkǒu | ⚠️500-only cửa ra vào |
| 门票 | ménpiào | ⚠️500-only vé vào cửa |
| 杯子 | bēizi | cái cốc |
| 本子 | běnzi | ⚠️500-only quyển vở |
| 书 | shū | sách |
| 书包 | shūbāo | ⚠️500-only cặp sách |
| 书店 | shūdiàn | hiệu sách |
| 图书馆 | túshūguǎn | ⚠️500-only thư viện |
| 洗手间 | xǐshǒujiān | ⚠️500-only nhà vệ sinh |
| 住 | zhù | ở, sống |
| 页 | yè | ⚠️500-only trang (giấy) |
| 间 | jiān | ⚠️500-only gian, phòng (lượng từ) |

### C18 — Phương hướng & vị trí cơ bản (17 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 上 | shàng | trên |
| 下 | xià | dưới |
| 前 | qián | trước |
| 后 | hòu | sau |
| 里 | lǐ | trong |
| 外 | wài | ⚠️500-only ngoài |
| 东 | dōng | ⚠️500-only đông (hướng) |
| 西 | xī | ⚠️500-only tây |
| 南 | nán | ⚠️500-only nam (hướng) |
| 北 | běi | ⚠️500-only bắc |
| 中 | zhōng | ⚠️500-only giữa |
| 中间 | zhōngjiān | ⚠️500-only ở giữa |
| 旁边 | pángbiān | ⚠️500-only bên cạnh |
| 左 | zuǒ | ⚠️500-only trái (bên) |
| 右 | yòu | ⚠️500-only phải (bên) |
| 地方 | dìfang | ⚠️500-only nơi chốn |
| 地点 | dìdiǎn | ⚠️500-only địa điểm |

### C19 — Phương hướng ghép & vị trí mở rộng (15 từ) — ⚠️toàn bộ 500-only
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 上边 | shàngbiān | phía trên |
| 下边 | xiàbiān | phía dưới |
| 前边 | qiánbiān | phía trước |
| 后边 | hòubiān | phía sau |
| 里边 | lǐbiān | bên trong |
| 外边 | wàibiān | bên ngoài |
| 东边 | dōngbiān | phía đông |
| 西边 | xībiān | phía tây |
| 南边 | nánbiān | phía nam |
| 北边 | běibiān | phía bắc |
| 左边 | zuǒbian | bên trái |
| 右边 | yòubian | bên phải |
| 这边 | zhèbiān | bên này |
| 那边 | nàbiān | đằng kia |
| 地上 | dì shàng | trên mặt đất |

### C20 — Giao thông: phương tiện & nơi chốn (16 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 车 | chē | xe |
| 汽车 | qìchē | ⚠️500-only ô tô |
| 火车 | huǒchē | tàu hỏa |
| 飞机 | fēijī | máy bay |
| 机场 | jīchǎng | ⚠️500-only sân bay |
| 机票 | jīpiào | ⚠️500-only vé máy bay |
| 车票 | chēpiào | ⚠️500-only vé xe |
| 车站 | chēzhàn | ⚠️500-only bến xe |
| 站 | zhàn | ⚠️500-only trạm, đứng |
| 出租车 | chūzūchē | taxi |
| 打车 | dǎchē | ⚠️500-only bắt taxi |
| 开车 | kāichē | lái xe |
| 路 | lù | ⚠️500-only đường |
| 路口 | lùkǒu | ⚠️500-only ngã tư |
| 路上 | lùshàng | ⚠️500-only trên đường |
| 马路 | mǎlù | ⚠️500-only đường phố |

### C21 — Động từ di chuyển: ra/vào/đến/đi/về (21 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 去 | qù | đi |
| 来 | lái | đến |
| 来到 | láidào | ⚠️500-only đến, tới nơi |
| 回 | huí | trở về |
| 回家 | huíjiā | ⚠️500-only về nhà |
| 回来 | huílái | ⚠️500-only về, quay lại |
| 回去 | huíqù | ⚠️500-only đi về |
| 进 | jìn | ⚠️500-only vào |
| 进来 | jìnlái | ⚠️500-only đi vào |
| 进去 | jìnqù | ⚠️500-only đi vào |
| 出 | chū | ⚠️500-only ra |
| 出来 | chūlái | ⚠️500-only ra (đi ra) |
| 出去 | chūqù | ⚠️500-only đi ra ngoài |
| 上车 | shàngchē | ⚠️500-only lên xe |
| 下车 | xiàchē | ⚠️500-only xuống xe |
| 坐 | zuò | ngồi, đi (xe) |
| 坐下 | zuòxià | ⚠️500-only ngồi xuống |
| 走 | zǒu | ⚠️500-only đi, đi bộ |
| 走路 | zǒulù | ⚠️500-only đi bộ |
| 到 | dào | đến |
| 得到 | dédào | ⚠️500-only nhận được |

### C22 — Sở thích, giải trí & công nghệ (18 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 爱好 | àihào | ⚠️500-only sở thích |
| 唱 | chàng | hát |
| 唱歌 | chànggē | ⚠️500-only hát |
| 歌 | gē | bài hát |
| 电视 | diànshì | tivi |
| 电视机 | diànshìjī | ⚠️500-only máy thu hình |
| 电影 | diànyǐng | phim |
| 电影院 | diànyǐngyuàn | rạp chiếu phim |
| 电脑 | diànnǎo | máy tính |
| 电话 | diànhuà | điện thoại |
| 手机 | shǒujī | điện thoại di động |
| 上网 | shàngwǎng | ⚠️500-only lên mạng |
| 网上 | wǎngshàng | ⚠️500-only trên mạng |
| 网友 | wǎngyǒu | ⚠️500-only bạn qua mạng |
| 玩儿 | wánr | chơi |
| 好听 | — | *(đã đưa vào C16, không lặp)* |
| 球 | qiú | ⚠️500-only quả bóng |
| 打球 | dǎqiú | ⚠️500-only chơi bóng |
| 跑 | pǎo | ⚠️500-only chạy |

### C23 — Sinh hoạt cá nhân hằng ngày (18 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 起床 | qǐchuáng | ngủ dậy |
| 起 | qǐ | ⚠️500-only dậy, bắt đầu |
| 起来 | qǐlái | ⚠️500-only dậy, lên |
| 睡 | shuì | ngủ |
| 睡觉 | shuìjiào | ngủ |
| 洗 | xǐ | ⚠️500-only rửa, tắm |
| 打电话 | dǎ diànhuà | gọi điện thoại |
| 打 | dǎ | ⚠️500-only đánh, gọi |
| 打开 | dǎkāi | ⚠️500-only mở ra |
| 关 | guān | ⚠️500-only đóng, tắt |
| 关上 | guānshàng | ⚠️500-only đóng lại |
| 拿 | ná | ⚠️500-only cầm, lấy |
| 放 | fàng | ⚠️500-only đặt, để |
| 放学 | fàngxué | ⚠️500-only tan học |
| 开 | kāi | mở |
| 做 | zuò | làm |
| 干 | gàn | ⚠️500-only làm |
| 送 | sòng | ⚠️500-only tặng, đưa |

### C24 — Động từ tri giác, tư duy, giao tiếp & động từ năng nguyện (30 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 会 | huì | biết (kỹ năng) |
| 想 | xiǎng | muốn, nghĩ |
| 能 | néng | có thể |
| 要 | yào | muốn, sẽ |
| 可以 | kěyǐ | *[bổ sung]* có thể, được phép |
| 看 | kàn | xem, nhìn |
| 看到 | kàndào | ⚠️500-only nhìn thấy |
| 看见 | kànjiàn | nhìn thấy |
| 听 | tīng | nghe |
| 听到 | tīngdào | ⚠️500-only nghe thấy |
| 听见 | tīngjiàn | nghe thấy |
| 说 | shuō | nói |
| 说话 | shuōhuà | nói chuyện |
| 问 | wèn | hỏi |
| 回答 | huídá | ⚠️500-only trả lời |
| 见 | jiàn | gặp |
| 见面 | jiànmiàn | ⚠️500-only gặp mặt |
| 觉得 | juéde | cảm thấy |
| 知道 | zhīdào | biết |
| 记 | jì | ⚠️500-only nhớ, ghi |
| 记得 | jìdé | ⚠️500-only nhớ |
| 记住 | jìzhù | ⚠️500-only ghi nhớ |
| 忘 | wàng | ⚠️500-only quên |
| 忘记 | wàngjì | ⚠️500-only quên |
| 明白 | míngbai | ⚠️500-only hiểu, rõ |
| 喜欢 | xǐhuan | thích |
| 认识 | rènshi | quen biết |
| 告诉 | gàosu | ⚠️500-only nói cho biết |
| 找 | zhǎo | ⚠️500-only tìm |
| 找到 | zhǎodào | ⚠️500-only tìm thấy |
| 笑 | xiào | ⚠️500-only cười |

### C25 — Tính từ mô tả & so sánh (20 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 大 | dà | to, lớn |
| 小 | xiǎo | nhỏ |
| 多 | duō | nhiều |
| 少 | shǎo | ít |
| 好 | hǎo | tốt, được |
| 坏 | huài | ⚠️500-only hỏng, xấu |
| 新 | xīn | mới |
| 干净 | gānjìng | ⚠️500-only sạch sẽ |
| 难 | nán | ⚠️500-only khó |
| 远 | yuǎn | ⚠️500-only xa |
| 慢 | màn | ⚠️500-only chậm |
| 重 | zhòng | ⚠️500-only nặng |
| 重要 | zhòngyào | ⚠️500-only quan trọng |
| 错 | cuò | ⚠️500-only sai |
| 对 | duì | đúng |
| 不对 | bú duì | ⚠️500-only sai, không đúng |
| 不大 | bú dà | ⚠️500-only không lớn lắm |
| 一样 | yíyàng | ⚠️500-only giống nhau |
| 差 | chà | ⚠️500-only kém, thiếu |
| 有名 | yǒumíng | ⚠️500-only nổi tiếng |

### C26 — Hư từ ngữ pháp, liên kết câu & còn lại (21 từ)
| 汉字 | Pinyin | Nghĩa |
|---|---|---|
| 的 | de | trợ từ sở hữu |
| 地 | de | trợ từ trạng ngữ |
| 得到 | — | *(đã đưa vào C21)* |
| 还是 | háishi | ⚠️500-only hay là |
| 还有 | hái yǒu | ⚠️500-only còn có |
| 从 | cóng | ⚠️500-only từ |
| 跟 | gēn | ⚠️500-only cùng, với |
| 给 | gěi | cho, đưa |
| 和 | hé | và |
| 比 | bǐ | ⚠️500-only so với |
| 等 | děng | ⚠️500-only chờ, đợi |
| 一起 | yìqǐ | ⚠️500-only cùng nhau |
| 一块儿 | yíkuàir | ⚠️500-only cùng nhau |
| 一边 | yìbiān | ⚠️500-only một bên; vừa...vừa |
| 用 | yòng | ⚠️500-only dùng |
| 有用 | yǒuyòng | ⚠️500-only có ích |
| 有的 | yǒude | có cái |
| 有时候 / 有时 | yǒushíhou / yǒushí | ⚠️500-only đôi khi |
| 是不是 | shì bú shì | ⚠️500-only có phải không |
| 真的 | zhēnde | ⚠️500-only thật đấy |
| 子 | zi | hậu tố danh từ (không nghĩa riêng) |

**Tổng cộng:** 26 nhóm, ~506 mục từ (đã bổ sung 6 từ theo §1.3). Một vài dòng "*(đã đưa vào C..)*" dùng để tránh đếm trùng khi một từ có logic thuộc 2 nhóm — không tính lặp vào tổng.

---

## 3. 15 课文 New HSK Course 1 (新HSK教程1)

Nguồn: [newhskcourse.com — Level 1](https://newhskcourse.com/new-hsk-course-volume-1/), [newhskcourse.com — Textbook](https://newhskcourse.com/new-hsk-course-volume-1-textbook/), [aprendechinohoy.com](https://www.aprendechinohoy.com/en/textbooks-adults/2757-new-hsk-course-1-hsk-30-2026-beginner-level-1-textbook-9787521367744.html). Các trang công khai không liệt kê chi tiết 40 điểm ngữ pháp/bài — cột "Ngữ pháp chính" dưới đây là **suy luận từ tên bài + chủ đề** (không phải trích nguyên văn mục lục).

| # | Tên 课文 (Hán) | Chủ đề | Ngữ pháp chính (suy luận) | Cụm chủ đề (§2) khớp |
|---|---|---|---|---|
| 1 | AI小语，你好！ | Chào hỏi, làm quen với AI | 你好, 是, 吗 | C2, C1 |
| 2 | 我叫李文 | Xưng tên | 叫, 什么名字, đại từ | C2, C3 |
| 3 | 我是中国人 | Quốc tịch | 是 + quốc tịch, 中国人 | C7 |
| 4 | 我有两个孩子 | Gia đình | 有, số + lượng từ + danh từ | C5, C4a |
| 5 | 今天我休息 | Nghỉ làm, lịch trình | 休息, 今天, phủ định | C8 (trong C7+C8), C11 |
| 6 | 你的手机号是多少？ | Số điện thoại | 多少, số đếm dài | C4a, C22 |
| 7 | 我晚上六点半下班 | Giờ giấc, tan làm | 点/半 giờ giấc, 下班 | C12, C8 |
| 8 | 我爸爸也在医院工作 | Nghề nghiệp gia đình | 在 + nơi + 工作, 也 | C7+C8, C5 |
| 9 | 我明天上午在学校学习 | Trường học, thời gian tương lai | 在 + trường + 学习, 上午 | C9, C12 |
| 10 | 这儿的苹果真便宜！ | Mua sắm, tính từ | 真 + tính từ, 的 định ngữ | C16, C25 |
| 11 | 我读大学呢 | Đại học, tiếp diễn | 呢 tiếp diễn, 读大学 | C9 |
| 12 | 昨天下雪了 | Thời tiết, quá khứ | 了 thay đổi/hoàn thành, thời tiết | C13+C14, C11 |
| 13 | 请给我一杯茶 | Gọi đồ uống | 请给我 + lượng từ + danh từ | C15, C4a |
| 14 | 我看了一个电影 | Giải trí, đã làm | 了 hoàn thành, 一个 | C22, C13+C14 |
| 15 | 大兴机场见！ | Du lịch, chia tay | 见, địa danh, hẹn gặp | C20, C2 |

Ghi chú: 8/15 课文 map vào đúng 1 cụm chủ đề chính + 1 cụm phụ (ngữ pháp thời gian/年紀 thường lặp lại xuyên suốt). Không có 课文 nào rơi vào nhóm phương hướng thuần túy (C18/C19) hoặc tính từ/hư từ thuần túy (C25/C26) — hợp lý vì đây là các nhóm "công cụ ngữ pháp" bổ trợ, ít khi làm chủ đề riêng một bài khóa.

---

## 4. Đề xuất chia buổi theo chủ đề (26 buổi, buổi 1 giữ nguyên)

Buổi 01 (ngữ âm) giữ nguyên như hiện có — không tính vào 500 từ. Các buổi 02–26 dưới đây map 1:1 (hoặc 1:2 khi cụm quá lớn) vào 26 cụm chủ đề của §2.

| # | Tên buổi | Từ lõi (12–18, xem đủ ở §2) | Ngữ pháp trọng tâm | 课文 NHK Course 1 lồng vào | Giáo trình Hán ngữ Q1 (ước lượng, cần rà lại) |
|---|---|---|---|---|---|
| 01 | Ngữ âm | — (giữ nguyên, đã có) | Pinyin, thanh điệu, 变调 | — | Bài 1–5 |
| 02 | Đại từ & câu trần thuật cơ bản | 我/你/他/她/我们/你们/是/不/有/也/都/很 (C1) | 是 câu, 吗 nghi vấn, phủ định 不/没 | L1 AI小语你好 | Bài 1 你好 |
| 03 | Chào hỏi, lịch sự & làm quen | 你好/谢谢/不客气/对不起/没关系/请/请问/叫/名字/介绍/别 (C2) | 叫…名字, 请 + động từ | L2 我叫李文 | Bài 2 汉语不太难, Bài 3 明天见 |
| 04 | Chỉ định & câu hỏi cơ bản | 这/那/这儿/那儿/谁/什么/哪/哪儿/怎么/怎么样/多少/呢/吗/吧 (C3) | Câu hỏi 什么/谁/哪, 呢 rút gọn | — | Bài 4 你去哪儿 |
| 05 | Số đếm & lượng từ cơ bản | 一~十/百/千/两/个/口/本/件/张/杯/次/岁 (C4a) | 数+量+名, 二 vs 两 | L6 你的手机号是多少 | (số đếm, chưa xác định bài cụ thể) |
| 06 | Lượng từ mở rộng & 一点儿/有点儿 | 块/毛/元/半/一点儿/有点儿/一些/有些 (C4b) | 一点儿 vs 有点儿, 一下 | — | (mua bán, chưa xác định) |
| 07 | Gia đình & bạn bè | 爸爸/妈妈/儿子/女儿/哥哥/姐姐/弟弟/妹妹/孩子/家/朋友/同学 (C5) | 有 (我有两个孩子), lượng từ 口 | L4 我有两个孩子 | Bài 5 这是王老师 |
| 08 | Con người: giới tính, tuổi tác, sức khỏe | 男/女/先生/小姐/老人/小孩儿/岁/身体/病/生病/累 (C6) | 多大/几岁 hỏi tuổi, 有点儿 + sức khỏe | — | (chưa xác định) |
| 09 | Quốc gia, ngôn ngữ & nghề nghiệp | 中国/汉语/汉字/中文/工作/医生/上班/下班/忙/休息 (C7+C8) | 是 + quốc tịch, 在+nơi+工作, 也 | L3 我是中国人, L8 我爸爸也在医院工作 | Bài 6, 8 (nghề nghiệp) |
| 10 | Trường học & học tập | 学校/学生/大学/大学生/学/学习/读/读书/老师/上学 (C9) | 在+trường+学习(呢) | L9 我明天上午在学校学习, L11 我读大学呢 | (chưa xác định) |
| 11 | Lớp học, thi cử, chữ viết | 课/上课/下课/考/考试/写/字/准备 (C10) | 上课/下课 cụm cố định | — | (chưa xác định) |
| 12 | Thời gian: ngày/tháng/năm | 年/月/日/号/星期/今年/明年/去年/今天/明天/昨天/生日 (C11) | Cách nói ngày tháng năm | — | Bài 7 (thời gian, ước lượng) |
| 13 | Thời gian: buổi & giờ giấc | 上午/中午/下午/晚上/早上/点/分/时候/时间/现在 (C12) | Đọc giờ 点/分, từ chỉ buổi | L7 我晚上六点半下班, L9 (phần 上午) | Bài 11 现在几点 (ước lượng) |
| 14 | 了/过/正在 (thể/thời) & Thời tiết | 了/过/正在/还/再/常常/快/天气/下雨/雨/冷/热 (C13+C14) | 了 hoàn thành/thay đổi, 过 kinh nghiệm, 正在 đang | L12 昨天下雪了, L14 我看了一个电影 | Bài 12 明天天气怎么样 (ước lượng) |
| 15 | Ăn uống | 吃/吃饭/喝/菜/茶/米饭/水/水果/饭/饿/好吃 (C15) | 想/要 + động từ ăn uống, 好吃/好喝 | L13 请给我一杯茶 | Bài 8 (ăn uống, ước lượng) |
| 16 | Mua sắm & tiền bạc | 买/钱/贵/便宜/商店/东西/衣服/穿/漂亮/好看 (C16) | 多少钱, 太…了, 的 định ngữ | L10 这儿的苹果真便宜 | Bài 9, 14 (mua sắm, ước lượng) |
| 17 | Nhà ở & đồ vật | 房子/房间/床/桌子/椅子/门/杯子/书/书店/图书馆 (C17) | 在 + đồ vật, lượng từ đồ vật | — | Bài 10 (chưa xác định chính xác) |
| 18 | Phương hướng & vị trí cơ bản | 上/下/前/后/里/外/东/西/南/北/左/右/地方 (C18) | 在…上/里, cấu trúc chỉ phương hướng | — | Bài 8 (vị trí, ước lượng) |
| 19 | Phương hướng ghép & vị trí mở rộng | 上边/下边/前边/后边/里边/外边/旁边/中间/这边/那边 (C19) | X + 边 = phía X, 在…边 | — | (chưa xác định) |
| 20 | Giao thông: phương tiện & nơi chốn | 车/汽车/火车/飞机/机场/车站/出租车/打车/开车/路 (C20) | 坐/骑 + phương tiện + 去 | L15 大兴机场见 | (chưa xác định) |
| 21 | Động từ di chuyển: ra/vào/đến/đi/về | 去/来/回/回家/进/出/上车/下车/坐/到 (C21) | Bổ ngữ xu hướng đơn giản 回来/出去/进去 | — | Bài 10–12 (đi lại, ước lượng — trùng vùng nội dung buổi06 2.0 cũ) |
| 22 | Sở thích, giải trí & công nghệ | 爱好/唱歌/电视/电影/电脑/手机/上网/玩儿/球/打球 (C22) | 喜欢 + động từ, tân ngữ kép | L14 我看了一个电影 | (chưa xác định) |
| 23 | Sinh hoạt cá nhân hằng ngày | 起床/睡觉/洗/打电话/打开/关/拿/放/开/做 (C23) | Trình tự động từ trong ngày (连动句) | — | (chưa xác định) |
| 24 | Động từ năng nguyện, tri giác & giao tiếp | 会/想/能/要/可以/看/听/说/问/知道/喜欢/认识 (C24) | 会/想/能/要/可以 phân biệt, 看见/听见 | — | Bài 6, 10 (会/能, trùng vùng buổi06 2.0 cũ) |
| 25 | Tính từ mô tả & so sánh | 大/小/多/少/好/新/干净/难/远/慢/重要/对 (C25) | 很/太/非常 + tính từ, so sánh 比 sơ giản | L10 这儿的苹果真便宜 (tính từ 便宜) | Bài 15 (ước lượng) |
| 26 | Hư từ ngữ pháp & liên kết câu (tổng ôn) | 的/还是/还有/从/跟/给/和/一起/一边/用 | Liên từ cơ bản, giới từ 从/跟/给 | — | (ôn tập tổng, không gắn bài cụ thể) |

**Ghi chú về "Giáo trình Hán ngữ Q1":** cột này chỉ mang tính **ước lượng thô** dựa trên tên bài công khai tìm được (Bài 1 你好, Bài 2 汉语不太难, Bài 3 明天见, Bài 4 你去哪儿, Bài 5 这是王老师) và các range đã dùng trong buổi06/10/12 cũ (Bài 8-15). Không tìm được mục lục đầy đủ 30 bài (cả 上/下) trong phiên nghiên cứu này — **cần rà lại bản sách giấy thật của user** trước khi chốt cột này vào production (giống cách buổi06/10/12 2.0 đã làm — "chỉ list tên bài, user tự đối chiếu").

---

## 5. Review 3 buổi cũ (2.0) — REUSE hay REWORK?

### 5.1 Buổi 06 — 会/想/能 · Hoạt động & giao thông → **REUSE** (khuyến nghị chính), gợi ý nhập vào buổi 21+24 mới

**Từ vựng hiện có và đối chiếu HSK 3.0 L1 (500 từ):**

| Từ trong buổi06 cũ | Có trong 500? |
|---|---|
| 起床, 吃饭, 上课, 做作业(⚠️不在500), 看电视, 打电话, 睡觉 | Có (trừ 做作业 — không thấy trong 500) |
| 上学, 坐(车), 公共汽车(⚠️不在500), 地铁(⚠️不在500), 出租车, 骑(⚠️不在500/自行车⚠️不在500), 走路 | 上学/坐/出租车/走路 có; 公共汽车/地铁/骑/自行车 KHÔNG có trong 500 |
| 会, 想, 能, 要, 可以 | Có cả 5 (要/可以 là 2 trong 6 từ phải bổ sung ở §1.3) |

**Nhận xét:** phần ngữ pháp (会/想/能/要/可以) là lõi rất chuẩn, khớp 100% cụm C24 mới. Phần từ vựng "hoạt động trong ngày" khớp tốt với C23 (sinh hoạt cá nhân). Phần "giao thông" có vấn đề: **公共汽车 (xe buýt), 地铁 (tàu điện ngầm), 骑/自行车 (đi xe đạp) đều KHÔNG có trong danh sách 500 từ HSK 3.0 L1** — đây là 3/7 từ (~43%) của riêng nhóm giao thông nằm ngoài phạm vi, phải chuyển sang HSK2 hoặc bỏ khỏi buổi.

**Verdict: REUSE có tinh chỉnh nhỏ.** Tách nội dung buổi06 cũ thành 2 phần theo cấu trúc mới:
- Ngữ pháp 会/想/能/要/可以 + phần "hoạt động trong ngày" (起床/吃饭/上课/看电视/打电话/睡觉) → nhập vào **buổi 24** (Động từ năng nguyện, tri giác & giao tiếp) + **buổi 23** (Sinh hoạt cá nhân).
- Phần giao thông: giữ 上学/坐/出租车/骑(nếu chấp nhận vượt phạm vi nhẹ)/走路 → nhập vào **buổi 20-21** (Giao thông); nhưng phải **bỏ hoặc đánh dấu ngoài phạm vi** 公共汽车/地铁/自行车 (đưa xuống HSK2 hoặc giữ như "từ mở rộng có thể học thêm" ngoài checklist 500).
- Hội thoại mẫu + câu giao tiếp hiện có dùng được gần như nguyên vẹn (đã khớp văn phong khẩu ngữ yêu cầu).

### 5.2 Buổi 10 — Lượng từ + 一点儿/有点儿 · Màu sắc → **REWORK một phần** (phần màu sắc)

**Đối chiếu:**

| Từ trong buổi10 cũ | Có trong 500? |
|---|---|
| 颜色(⚠️不在500), 红色/橙色/黄色/绿色/蓝色/紫色/粉色/黑色/灰色 — **TẤT CẢ đều KHÔNG có trong 500** | Không — ngoại trừ 白 (trắng, đứng một mình, không phải 白色) |
| 铅笔(⚠️不在500), 本子, 书包, 尺子(⚠️不在500), 橡皮(⚠️不在500), 杯子, 筷子(⚠️不在500) | Chỉ 本子/书包/杯子 có trong 500; 铅笔/尺子/橡皮/筷子 KHÔNG có |
| 数+量+名, 个/口/件/张, 一点儿/有点儿 | Khớp hoàn toàn với C4a/C4b mới |

**Nhận xét: đây là phát hiện quan trọng nhất của §5.** Toàn bộ mảng "颜色 màu sắc" (9/9 từ màu cụ thể) và phần lớn "học cụ" (4/7 từ) của buổi10 cũ **nằm ngoài phạm vi HSK 3.0 Level 1**. Có khả năng những từ này thuộc HSK2 (bản 2.0 cũ gộp chung phạm vi rộng hơn 150 từ HSK1 2.0). Phần ngữ pháp lượng từ + 一点儿/有点儿 thì rất chuẩn, khớp gần 100% với cụm C4a/C4b.

**Verdict: REUSE phần ngữ pháp (lượng từ, 一点儿/有点儿) → nhập thẳng vào buổi 05-06 mới; REWORK/loại bỏ phần từ vựng màu sắc và phần lớn học cụ** — thay bằng từ vựng thực sự nằm trong C4a/C4b/C16 (ví dụ dùng bối cảnh mua sắm quần áo 衣服/漂亮/贵/便宜 vốn đã có sẵn từ trong 500, thay vì màu sắc). Nếu muốn giữ màu sắc vì lý do sư phạm (dễ dạy, trực quan), có thể để như một "buổi mở rộng ngoài 500 từ chính thức" — cần user quyết.

### 5.3 Buổi 12 — 了/没/过/快…了 · Thời tiết → **REUSE phần ngữ pháp, REWORK phần thời tiết/mùa**

**Đối chiếu:**

| Từ trong buổi12 cũ | Có trong 500? |
|---|---|
| 天气, 晴天(⚠️不在500), 阴天(⚠️不在500), 下雨, 下雪, 刮风(⚠️不在500 — chỉ có 风 đơn, không có cụm 刮风), 冷, 热 | Chỉ 天气/下雨/下雪/冷/热 có; 晴天/阴天/刮风 KHÔNG có (风 đơn có nhưng 刮风 thì không) |
| 春天/夏天/秋天/冬天/暖和/凉快/度 — **TẤT CẢ 7 từ đều KHÔNG có trong 500** | Không — mùa và 暖和/凉快/độ đều thuộc HSK2 |
| 了 (thay đổi + hoàn thành), 没, 快…了, 过 | Khớp hoàn toàn với C13 mới |

**Nhận xét:** giống buổi10, phần ngữ pháp là lõi chuẩn và tái dùng tốt. Nhưng phần từ vựng "mùa" (春夏秋冬) và "nhiệt độ định tính" (暖和/凉快/度) **hoàn toàn nằm ngoài HSK 3.0 Level 1** — đây rõ ràng là nội dung HSK2. Ngay cả trong nhóm "thời tiết cơ bản", 3/8 từ (晴天/阴天/刮风) cũng không có.

**Verdict: REUSE phần ngữ pháp (了/没/过/快…了) → nhập vào buổi 14 mới; REWORK mạnh phần từ vựng thời tiết** — chỉ giữ 天气/下雨/雨/下雪/雪/冷/热/风 (8 từ hợp lệ, khớp C13+C14 mới), bỏ hẳn 晴天/阴天/刮风/mùa/暖和/凉快/độ (đẩy sang HSK2 nếu vẫn muốn dạy).

### 5.4 Tổng kết bảng verdict

| Buổi cũ | Verdict | Lý do chính |
|---|---|---|
| 06 — 会/想/能 | **REUSE** (tách nhập buổi 20/21/23/24 mới) | Ngữ pháp + phần lớn từ vựng khớp; chỉ 3 từ giao thông (公共汽车/地铁/骑自行车) ngoài phạm vi |
| 10 — Lượng từ + màu sắc | **REUSE ngữ pháp / REWORK từ vựng màu** (nhập buổi 05/06 mới) | Toàn bộ 9 từ màu sắc + 4/7 học cụ ngoài phạm vi 500 |
| 12 — 了/过 + thời tiết | **REUSE ngữ pháp / REWORK từ vựng mùa** (nhập buổi 14 mới) | Toàn bộ nhóm mùa (4 từ) + 暖和/凉快/度 (3 từ) + 晴天/阴天/刮风 (3 từ) ngoài phạm vi 500 |

---

## 6. Chênh lệch, ghi chú & việc cần user quyết

1. **Quyết định lớn nhất (§1.2):** giữ bám 500 từ (bản 2021) như đã chốt, hay chuyển sang bám 300 từ (bản 2025 final) để khớp đúng New HSK Course 1 + kỳ thi thực tế nửa cuối 2026? Đề xuất giữ 500 cho proposal này nhưng cần quyết trước khi implementation.
2. **Chất lượng danh sách 500 từ (§1.3):** đã phát hiện và vá 6 lỗ hổng qua đối chiếu chéo (你好, 可以, 卖, 女士, 怎么样, 千). Khuyến nghị chạy một lượt diff tự động với file JSON gốc (GitHub `drkameleon/complete-hsk-vocabulary`) trước khi dùng danh sách này làm checklist production chính thức — rủi ro còn sót 1-2 từ khác là có thật dù đã cross-check.
3. **Màu sắc & học cụ chi tiết, mùa & nhiệt độ định tính:** hoàn toàn ngoài phạm vi 500 từ (đều là nội dung HSK2). Đây là phần nội dung "được lòng học viên" (trực quan, dễ dạy) nhưng không thuộc HSK1 3.0 — cần quyết: bỏ hẳn, hay giữ như một "buổi bonus ngoài chuẩn" không tính vào 26 buổi chính?
4. **Hư từ/ngữ pháp dày ở một số buổi:** buổi 02 (C1, 22 từ), buổi 12/13 (C11/C12, 17-18 từ), buổi 24 (C24, ~30 từ nếu tính cả modal verbs) vượt mức 12-18 từ khuyến nghị. Vì đây đều là từ chức năng tần suất cực cao (đại từ, hư từ, động từ năng nguyện), đề xuất giữ nguyên (đúng lưu ý "hư từ có thể dày hơn" trong đề bài), nhưng buổi 24 nên cân nhắc tách thành 24a (modal 会/想/能/要/可以) + 24b (tri giác/giao tiếp: 看/听/说/知道…) nếu thấy quá tải khi thực dạy.
5. **Giáo trình Hán ngữ Quyển 1 — cột đối chiếu chưa đầy đủ:** chỉ xác nhận được tên 5/15 bài đầu (上册) qua web search; nhiều buổi trong bảng §4 để trống hoặc "(chưa xác định)". Cần user (có sách giấy) đối chiếu lại toàn bộ 30 bài (上+下) khi vào implementation — giữ đúng tinh thần "chỉ list tên bài, user tự đối chiếu" như bản 2.0 cũ.
6. **15 课文 New HSK Course 1 — thiếu chi tiết ngữ pháp/từ khóa chính thức:** các trang công khai (newhskcourse.com) không liệt kê 40 điểm ngữ pháp hay từ vựng riêng từng bài; cột "Ngữ pháp chính" ở §3 là suy luận từ tên bài, cần verify lại nguyên văn 课文 (mua sách/PDF) trước khi trích dẫn làm bài đọc — giống gate "không bịa nội dung 课文" đã áp dụng ở bản 2.0.
7. **Buổi không có 课文 lồng ghép:** buổi 04 (chỉ định/nghi vấn), 06 (lượng từ mở rộng), 08 (con người), 11 (lớp học/thi cử), 17-19 (nhà ở/phương hướng), 22-23 (giải trí/sinh hoạt), 25-26 (tính từ/hư từ) — không có 课文 nào trong 15 bài khớp trực tiếp. Hợp lý vì 15 课文 chỉ đủ phủ ~9/26 chủ đề; các buổi còn lại cần dựng hội thoại/bài đọc riêng (theo đúng tinh thần "textbook 15 bài chỉ là reading material lồng vào, không quyết định cấu trúc buổi").
8. **Tổng số buổi (26) ở cận trên của range 20-28** được giao — do chọn chia nhỏ các cụm lớn (C4, C18/19, C13/14) thành 2 buổi riêng để giữ nhịp 12-18 từ/buổi. Có thể gộp bớt nếu muốn rút xuống ~22-24 buổi (ví dụ gộp buổi 18+19 phương hướng thành 1 buổi ~25 từ, gộp buổi 05+06 số đếm thành 1 buổi ~35 từ) — đánh đổi nhịp độ dạy vs. số buổi.

---

## Nguồn tổng hợp

- [HSK Tracker — New HSK Vocabulary List Level 1](https://www.hsktracker.com/en/new-hsk-vocabulary-list-level-1/)
- [Everyday Chinese — NEW(3.0) HSK 1 Vocabulary](https://www.everydaychinese.com/youtube-lessons/new-hsk-1.html)
- [Mandarin Bean — New HSK 1 Word List](https://mandarinbean.com/new-hsk-1-word-list/)
- [Khanji School — New HSK 3.0 2026: differences vs HSK 2.0 and 2021](https://khanjischool.com/blog/chinese/new-hsk-30-2026-vocabulary-levels-exams-and-official-textbooks)
- [HSK Story — Complete HSK 3.0 Vocabulary List Guide](https://hskstory.com/guides/hsk-30-vocabulary-complete)
- [New HSK Course — Level 1](https://newhskcourse.com/new-hsk-course-volume-1/), [Textbook page](https://newhskcourse.com/new-hsk-course-volume-1-textbook/)
- [Aprende Chino Hoy — New HSK Course 1 textbook listing (ISBN 9787521367744)](https://www.aprendechinohoy.com/en/textbooks-adults/2757-new-hsk-course-1-hsk-30-2026-beginner-level-1-textbook-9787521367744.html)
- [GitHub — drkameleon/complete-hsk-vocabulary](https://github.com/drkameleon/complete-hsk-vocabulary) (đề xuất dùng để verify lần cuối, xem §1.3)
- Nội dung buổi06/10/12 cũ: `output/hsk1/buoi06_nangnguyen_phuongtien/slide/buoi06.json`, `output/hsk1/buoi10_luongtu_mausac/slide/buoi10.json`, `output/hsk1/buoi12_le_thoitiet/slide/buoi12.json`
