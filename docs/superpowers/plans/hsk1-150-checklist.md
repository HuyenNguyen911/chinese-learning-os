# HSK1 — Checklist phủ 150 từ (source of truth)

**Ngày tạo:** 2026-07-20
**Task:** 0.1 (hạ tầng cho `feat/hsk1-full-course`)
**Mục đích:** mọi buổi sau khi build phải đối chiếu bảng này để đảm bảo phủ đủ 150 từ HSK1 chính thức, không sót, không trùng.

## Nguồn đối chiếu (≥2 nguồn, khớp 100%)

1. https://www.hsk.academy/en/hsk_1 (HSK Academy — danh sách 150 từ HSK1, định dạng HSK cũ/2.0)
2. https://mandarinbean.com/hsk-1-vocabulary-list/ (Mandarin Bean — danh sách 150 từ, thứ tự & nội dung **trùng khớp 100%** với nguồn 1)
3. Đối chiếu bổ sung: https://www.hanzistroke.com/hsk/level-1 xác nhận tổng "150 vocabulary (82 characters + 68 words)" cho HSK Level 1 (2.0/cũ) → khớp tổng số 150.

Hai nguồn 1 và 2 cho **danh sách giống hệt nhau từng từ, từng thứ tự** (150/150) — dùng làm danh sách chuẩn chính thức trong file này. (Một nguồn thứ 4, digmandarin.com, hiển thị dạng phân nhóm chủ đề có lẫn thêm vài biến thể — 你们/他们/她们/零/日/火车站/说话 — không khớp 2 nguồn kia nên **không dùng**; các từ này không được tính vào 150 chuẩn.)

## Mapping vị trí syllabus ↔ folder hiện tại

| Vị trí syllabus | Chủ đề | Folder hiện tại (chưa đổi tên — Task 0.3) |
|---|---|---|
| Buổi 2 | Đại từ · chào hỏi · làm quen | MỚI |
| Buổi 3 | Số/thời gian/địa điểm | MỚI |
| Buổi 4 | Gia đình & tuổi | MỚI |
| Buổi 5 | Nghề/quốc tịch/ngôn ngữ | MỚI |
| Buổi 6 | 会/想/能 — Hoạt động & giao thông | `output/hsk1/buoi1_nangnguyen_phuongtien/` (ĐÃ CÓ) |
| Buổi 7 | Ăn uống | MỚI |
| Buổi 8 | Nhà/đồ vật/vị trí | MỚI |
| Buổi 9 | Sở thích & động từ | MỚI |
| Buổi 10 | Lượng từ + màu sắc | `output/hsk1/buoi2_luongtu_mausac/` (ĐÃ CÓ) |
| Buổi 11 | Mua sắm/tiền/tính từ | MỚI |
| Buổi 12 | 了/没/过/快…了 — Thời tiết | `output/hsk1/buoi3_le_thoitiet/` (ĐÃ CÓ) |

Buổi 1 (Ngữ âm) không có 生词 HSK — không nằm trong bảng 150 từ.

## Tổng số từ theo buổi (summary)

| Buổi | Số từ mới (150-chuẩn) | Trạng thái |
|---|---|---|
| Buổi 2 | 29 | ⏳ chưa soạn |
| Buổi 3 | 36 | ⏳ chưa soạn |
| Buổi 4 | 10 | ⏳ chưa soạn |
| Buổi 5 | 8 | ⏳ chưa soạn |
| Buổi 6 | 11 | ✅ đã có |
| Buổi 7 | 8 | ⏳ chưa soạn |
| Buổi 8 | 9 | ⏳ chưa soạn |
| Buổi 9 | 15 | ⏳ chưa soạn |
| Buổi 10 | 6 | ✅ đã có |
| Buổi 11 | 13 | ⏳ chưa soạn |
| Buổi 12 | 5 | ✅ đã có |
| **Tổng** | **150** | |

Ghi chú "ôn ở buổi X" trong cột **buổi phụ trách** = từ đã dạy chính thức ở buổi này, được **dùng lại/ôn tập** (không phải dạy lại) ở buổi X sau đó theo mạch ngữ pháp của spec §4. Không tính trùng vào tổng 150.

---

## Buổi 2 — Đại từ · chào hỏi · làm quen (29 từ) — ⏳ chưa soạn

| 汉字 | pinyin | nghĩa Việt | buổi phụ trách | trạng thái |
|---|---|---|---|---|
| 我 | wǒ | tôi, mình | Buổi 2 | ⏳ chưa soạn |
| 我们 | wǒmen | chúng tôi, chúng ta | Buổi 2 | ⏳ chưa soạn |
| 你 | nǐ | bạn, anh, chị | Buổi 2 | ⏳ chưa soạn |
| 他 | tā | anh ấy, nó | Buổi 2 | ⏳ chưa soạn |
| 她 | tā | chị ấy, cô ấy | Buổi 2 | ⏳ chưa soạn |
| 谁 | shéi | ai | Buổi 2 (ôn ở buổi 5) | ⏳ chưa soạn |
| 什么 | shénme | gì, cái gì | Buổi 2 | ⏳ chưa soạn |
| 的 | de | (trợ từ sở hữu) "của" | Buổi 2 | ⏳ chưa soạn |
| 吗 | ma | (trợ từ nghi vấn) | Buổi 2 | ⏳ chưa soạn |
| 呢 | ne | (trợ từ) "còn... thì sao" | Buổi 2 | ⏳ chưa soạn |
| 喂 | wèi | alô | Buổi 2 | ⏳ chưa soạn |
| 老师 | lǎoshī | giáo viên | Buổi 2 | ⏳ chưa soạn |
| 学生 | xuéshēng | học sinh | Buổi 2 | ⏳ chưa soạn |
| 同学 | tóngxué | bạn học | Buổi 2 | ⏳ chưa soạn |
| 朋友 | péngyǒu | bạn bè | Buổi 2 | ⏳ chưa soạn |
| 先生 | xiānsheng | ông, quý ông | Buổi 2 | ⏳ chưa soạn |
| 小姐 | xiǎojiě | cô, quý cô | Buổi 2 | ⏳ chưa soạn |
| 名字 | míngzi | tên | Buổi 2 | ⏳ chưa soạn |
| 谢谢 | xièxie | cảm ơn | Buổi 2 | ⏳ chưa soạn |
| 不客气 | búkèqi | không có gì | Buổi 2 | ⏳ chưa soạn |
| 再见 | zàijiàn | tạm biệt | Buổi 2 | ⏳ chưa soạn |
| 请 | qǐng | xin mời | Buổi 2 | ⏳ chưa soạn |
| 对不起 | duìbùqǐ | xin lỗi | Buổi 2 | ⏳ chưa soạn |
| 没关系 | méiguānxi | không sao | Buổi 2 | ⏳ chưa soạn |
| 是 | shì | là | Buổi 2 (ôn ở buổi 5) | ⏳ chưa soạn |
| 叫 | jiào | gọi, tên là | Buổi 2 | ⏳ chưa soạn |
| 认识 | rènshi | quen biết | Buổi 2 | ⏳ chưa soạn |
| 好 | hǎo | tốt, khỏe | Buổi 2 (ôn ở buổi 7, 11) | ⏳ chưa soạn |
| 高兴 | gāoxìng | vui, vui mừng | Buổi 2 | ⏳ chưa soạn |

## Buổi 3 — Số/thời gian/địa điểm (36 từ) — ⏳ chưa soạn

| 汉字 | pinyin | nghĩa Việt | buổi phụ trách | trạng thái |
|---|---|---|---|---|
| 这 | zhè | này, cái này | Buổi 3 | ⏳ chưa soạn |
| 那 | nà | kia, đó | Buổi 3 | ⏳ chưa soạn |
| 哪 | nǎ | nào | Buổi 3 (ôn ở buổi 5) | ⏳ chưa soạn |
| 哪儿 | nǎr | đâu, ở đâu | Buổi 3 | ⏳ chưa soạn |
| 几 | jǐ | mấy | Buổi 3 | ⏳ chưa soạn |
| 怎么 | zěnme | làm sao, thế nào | Buổi 3 | ⏳ chưa soạn |
| 怎么样 | zěnmeyàng | thế nào (nhận xét) | Buổi 3 | ⏳ chưa soạn |
| 一 | yī | một | Buổi 3 | ⏳ chưa soạn |
| 二 | èr | hai | Buổi 3 | ⏳ chưa soạn |
| 三 | sān | ba | Buổi 3 | ⏳ chưa soạn |
| 四 | sì | bốn | Buổi 3 | ⏳ chưa soạn |
| 五 | wǔ | năm | Buổi 3 | ⏳ chưa soạn |
| 六 | liù | sáu | Buổi 3 | ⏳ chưa soạn |
| 七 | qī | bảy | Buổi 3 | ⏳ chưa soạn |
| 八 | bā | tám | Buổi 3 | ⏳ chưa soạn |
| 九 | jiǔ | chín | Buổi 3 | ⏳ chưa soạn |
| 十 | shí | mười | Buổi 3 | ⏳ chưa soạn |
| 在 | zài | ở, tại; đang | Buổi 3 (ôn ở buổi 8) | ⏳ chưa soạn |
| 学校 | xuéxiào | trường học | Buổi 3 | ⏳ chưa soạn |
| 饭店 | fàndiàn | nhà hàng, khách sạn | Buổi 3 | ⏳ chưa soạn |
| 医院 | yīyuàn | bệnh viện | Buổi 3 | ⏳ chưa soạn |
| 北京 | Běijīng | Bắc Kinh | Buổi 3 | ⏳ chưa soạn |
| 今天 | jīntiān | hôm nay | Buổi 3 | ⏳ chưa soạn |
| 明天 | míngtiān | ngày mai | Buổi 3 | ⏳ chưa soạn |
| 昨天 | zuótiān | hôm qua | Buổi 3 | ⏳ chưa soạn |
| 上午 | shàngwǔ | buổi sáng | Buổi 3 | ⏳ chưa soạn |
| 中午 | zhōngwǔ | buổi trưa | Buổi 3 | ⏳ chưa soạn |
| 下午 | xiàwǔ | buổi chiều | Buổi 3 | ⏳ chưa soạn |
| 年 | nián | năm (thời gian) | Buổi 3 | ⏳ chưa soạn |
| 月 | yuè | tháng | Buổi 3 | ⏳ chưa soạn |
| 号 | hào | ngày, mùng (số) | Buổi 3 | ⏳ chưa soạn |
| 星期 | xīngqī | tuần, thứ | Buổi 3 | ⏳ chưa soạn |
| 点 | diǎn | giờ, điểm | Buổi 3 | ⏳ chưa soạn |
| 分钟 | fēnzhōng | phút | Buổi 3 | ⏳ chưa soạn |
| 现在 | xiànzài | bây giờ | Buổi 3 | ⏳ chưa soạn |
| 时候 | shíhou | lúc, thời điểm | Buổi 3 | ⏳ chưa soạn |

## Buổi 4 — Gia đình & tuổi (10 từ) — ⏳ chưa soạn

| 汉字 | pinyin | nghĩa Việt | buổi phụ trách | trạng thái |
|---|---|---|---|---|
| 岁 | suì | tuổi | Buổi 4 | ⏳ chưa soạn |
| 没 | méi | không, chưa (có) | Buổi 4 (ôn ở buổi 12) | ⏳ chưa soạn |
| 都 | dōu | đều | Buổi 4 | ⏳ chưa soạn |
| 和 | hé | và | Buổi 4 | ⏳ chưa soạn |
| 家 | jiā | nhà, gia đình | Buổi 4 | ⏳ chưa soạn |
| 爸爸 | bàba | bố | Buổi 4 | ⏳ chưa soạn |
| 妈妈 | māma | mẹ | Buổi 4 | ⏳ chưa soạn |
| 儿子 | érzi | con trai | Buổi 4 | ⏳ chưa soạn |
| 女儿 | nǚ'ér | con gái | Buổi 4 | ⏳ chưa soạn |
| 有 | yǒu | có | Buổi 4 | ⏳ chưa soạn |

## Buổi 5 — Nghề nghiệp · quốc tịch · ngôn ngữ (8 từ) — ⏳ chưa soạn

| 汉字 | pinyin | nghĩa Việt | buổi phụ trách | trạng thái |
|---|---|---|---|---|
| 中国 | Zhōngguó | Trung Quốc | Buổi 5 | ⏳ chưa soạn |
| 医生 | yīshēng | bác sĩ | Buổi 5 | ⏳ chưa soạn |
| 人 | rén | người | Buổi 5 | ⏳ chưa soạn |
| 汉语 | hànyǔ | tiếng Hán, tiếng Trung | Buổi 5 | ⏳ chưa soạn |
| 字 | zì | chữ | Buổi 5 | ⏳ chưa soạn |
| 说 | shuō | nói | Buổi 5 | ⏳ chưa soạn |
| 学习 | xuéxí | học, học tập | Buổi 5 (ôn ở buổi 9) | ⏳ chưa soạn |
| 工作 | gōngzuò | làm việc, công việc | Buổi 5 | ⏳ chưa soạn |

## Buổi 6 — 会/想/能 · Hoạt động & giao thông (11 từ) — ✅ đã có

| 汉字 | pinyin | nghĩa Việt | buổi phụ trách | trạng thái |
|---|---|---|---|---|
| 飞机 | fēijī | máy bay | Buổi 6 | ✅ đã có |
| 出租车 | chūzūchē | taxi | Buổi 6 | ✅ đã có |
| 电视 | diànshì | tivi | Buổi 6 (ôn ở buổi 8) | ✅ đã có |
| 看 | kàn | xem, nhìn | Buổi 6 (ôn ở buổi 9) | ✅ đã có |
| 吃 | chī | ăn | Buổi 6 (ôn ở buổi 7) | ✅ đã có |
| 睡觉 | shuìjiào | ngủ | Buổi 6 | ✅ đã có |
| 打电话 | dǎ diànhuà | gọi điện thoại | Buổi 6 | ✅ đã có |
| 坐 | zuò | ngồi | Buổi 6 | ✅ đã có |
| 想 | xiǎng | muốn, nghĩ | Buổi 6 (ôn ở buổi 9) | ✅ đã có |
| 会 | huì | biết (kỹ năng) | Buổi 6 (ôn ở buổi 9) | ✅ đã có |
| 能 | néng | có thể | Buổi 6 | ✅ đã có |

## Buổi 7 — Ăn uống (8 từ) — ⏳ chưa soạn

| 汉字 | pinyin | nghĩa Việt | buổi phụ trách | trạng thái |
|---|---|---|---|---|
| 水 | shuǐ | nước | Buổi 7 | ⏳ chưa soạn |
| 菜 | cài | món ăn, rau | Buổi 7 | ⏳ chưa soạn |
| 米饭 | mǐfàn | cơm | Buổi 7 | ⏳ chưa soạn |
| 水果 | shuǐguǒ | hoa quả | Buổi 7 | ⏳ chưa soạn |
| 苹果 | píngguǒ | táo | Buổi 7 | ⏳ chưa soạn |
| 茶 | chá | trà | Buổi 7 | ⏳ chưa soạn |
| 东西 | dōngxi | đồ vật, thứ | Buổi 7 | ⏳ chưa soạn |
| 喝 | hē | uống | Buổi 7 | ⏳ chưa soạn |

## Buổi 8 — Nhà · đồ vật · vị trí (9 từ) — ⏳ chưa soạn

| 汉字 | pinyin | nghĩa Việt | buổi phụ trách | trạng thái |
|---|---|---|---|---|
| 上 | shàng | trên, lên | Buổi 8 | ⏳ chưa soạn |
| 下 | xià | dưới, xuống | Buổi 8 | ⏳ chưa soạn |
| 前面 | qiánmiàn | phía trước | Buổi 8 | ⏳ chưa soạn |
| 后面 | hòumiàn | phía sau | Buổi 8 | ⏳ chưa soạn |
| 里面 | lǐmiàn | bên trong | Buổi 8 | ⏳ chưa soạn |
| 电脑 | diànnǎo | máy tính | Buổi 8 | ⏳ chưa soạn |
| 书 | shū | sách | Buổi 8 (ôn ở buổi 9) | ⏳ chưa soạn |
| 桌子 | zhuōzi | cái bàn | Buổi 8 | ⏳ chưa soạn |
| 椅子 | yǐzi | cái ghế | Buổi 8 | ⏳ chưa soạn |

## Buổi 9 — Sở thích & động từ (15 từ) — ⏳ chưa soạn

| 汉字 | pinyin | nghĩa Việt | buổi phụ trách | trạng thái |
|---|---|---|---|---|
| 电影 | diànyǐng | phim | Buổi 9 | ⏳ chưa soạn |
| 猫 | māo | mèo | Buổi 9 | ⏳ chưa soạn |
| 狗 | gǒu | chó | Buổi 9 | ⏳ chưa soạn |
| 听 | tīng | nghe | Buổi 9 | ⏳ chưa soạn |
| 读 | dú | đọc | Buổi 9 | ⏳ chưa soạn |
| 写 | xiě | viết | Buổi 9 | ⏳ chưa soạn |
| 看见 | kànjiàn | nhìn thấy | Buổi 9 | ⏳ chưa soạn |
| 来 | lái | đến | Buổi 9 | ⏳ chưa soạn |
| 回 | huí | về, quay lại | Buổi 9 | ⏳ chưa soạn |
| 去 | qù | đi | Buổi 9 | ⏳ chưa soạn |
| 做 | zuò | làm | Buổi 9 | ⏳ chưa soạn |
| 开 | kāi | mở, lái (xe) | Buổi 9 | ⏳ chưa soạn |
| 住 | zhù | ở, sống | Buổi 9 | ⏳ chưa soạn |
| 爱 | ài | yêu | Buổi 9 | ⏳ chưa soạn |
| 喜欢 | xǐhuan | thích | Buổi 9 | ⏳ chưa soạn |

## Buổi 10 — Lượng từ + 一点儿 · Màu sắc (6 từ) — ✅ đã có

| 汉字 | pinyin | nghĩa Việt | buổi phụ trách | trạng thái |
|---|---|---|---|---|
| 个 | gè | cái (lượng từ chung) | Buổi 10 | ✅ đã có |
| 本 | běn | quyển (lượng từ sách) | Buổi 10 | ✅ đã có |
| 些 | xiē | vài, một số | Buổi 10 | ✅ đã có |
| 块 | kuài | đồng (tiền), miếng | Buổi 10 (ôn ở buổi 11) | ✅ đã có |
| 一点儿 | yìdiǎnr | một chút | Buổi 10 | ✅ đã có |
| 杯子 | bēizi | cái cốc | Buổi 10 | ✅ đã có |

## Buổi 11 — Mua sắm · tiền · tính từ mô tả (13 từ) — ⏳ chưa soạn

| 汉字 | pinyin | nghĩa Việt | buổi phụ trách | trạng thái |
|---|---|---|---|---|
| 多少 | duōshǎo | bao nhiêu | Buổi 11 | ⏳ chưa soạn |
| 不 | bù | không | Buổi 11 | ⏳ chưa soạn |
| 很 | hěn | rất | Buổi 11 | ⏳ chưa soạn |
| 太 | tài | quá | Buổi 11 | ⏳ chưa soạn |
| 商店 | shāngdiàn | cửa hàng | Buổi 11 | ⏳ chưa soạn |
| 衣服 | yīfu | quần áo | Buổi 11 | ⏳ chưa soạn |
| 钱 | qián | tiền | Buổi 11 | ⏳ chưa soạn |
| 买 | mǎi | mua | Buổi 11 | ⏳ chưa soạn |
| 大 | dà | to, lớn | Buổi 11 | ⏳ chưa soạn |
| 小 | xiǎo | nhỏ | Buổi 11 | ⏳ chưa soạn |
| 多 | duō | nhiều | Buổi 11 | ⏳ chưa soạn |
| 少 | shǎo | ít | Buổi 11 | ⏳ chưa soạn |
| 漂亮 | piàoliang | đẹp | Buổi 11 | ⏳ chưa soạn |

## Buổi 12 — 了/没/过/快…了 — Thời tiết (5 từ) — ✅ đã có

| 汉字 | pinyin | nghĩa Việt | buổi phụ trách | trạng thái |
|---|---|---|---|---|
| 了 | le | (trợ từ hoàn thành/biến đổi) "rồi" | Buổi 12 | ✅ đã có |
| 天气 | tiānqì | thời tiết | Buổi 12 | ✅ đã có |
| 下雨 | xiàyǔ | trời mưa | Buổi 12 | ✅ đã có |
| 冷 | lěng | lạnh | Buổi 12 | ✅ đã có |
| 热 | rè | nóng | Buổi 12 | ✅ đã có |

---

## Chênh lệch & đề xuất

Tổng vocab lõi §5 (spec) + existing (buổi 6/10/12) **không** khớp thẳng 150 nếu lấy nguyên văn danh sách gợi ý trong spec — có 2 loại lệch, cả hai đã được xử lý để bảng trên đạt đúng 150/150 không trùng:

### 1. Từ chính thức (150) bị thiếu trong danh sách lõi §5 → đã bổ sung thủ công (14 từ)

Spec §5 chỉ liệt kê vocab **lõi gợi ý**, không đủ 150 khi đối chiếu danh sách chuẩn. 14 từ HSK1 chính thức sau **không nằm trong bất kỳ danh sách lõi §5 nào** — đã tự bổ sung vào buổi phù hợp nhất theo chủ đề (đã phản ánh trong bảng trên), cần **user/Teaching Coach xác nhận lại** khi build buổi tương ứng:

| 汉字 | nghĩa | Đề xuất buổi | Lý do |
|---|---|---|---|
| 的 | của | Buổi 2 | trợ từ cơ bản, đi cùng 是/吗/呢 |
| 喂 | alô | Buổi 2 | chào hỏi qua điện thoại |
| 同学 | bạn học | Buổi 2 | cùng nhóm 朋友/老师/学生 |
| 朋友 | bạn bè | Buổi 2 | làm quen |
| 先生 | ông, quý ông | Buổi 2 | xưng hô lịch sự |
| 小姐 | cô, quý cô | Buổi 2 | xưng hô lịch sự |
| 学校 | trường học | Buổi 3 | địa điểm |
| 饭店 | nhà hàng/khách sạn | Buổi 3 | địa điểm |
| 医院 | bệnh viện | Buổi 3 | địa điểm |
| 北京 | Bắc Kinh | Buổi 3 | địa điểm/địa danh |
| 飞机 | máy bay | Buổi 6 | giao thông |
| 猫 | mèo | Buổi 9 | sở thích ("你喜欢猫还是狗?") |
| 狗 | chó | Buổi 9 | sở thích |
| 衣服 | quần áo | Buổi 11 | mua sắm (đã xuất hiện trong ví dụ buổi 10 hiện có: "这件衣服...") |

### 2. Từ trong danh sách lõi §5 nhưng KHÔNG thuộc 150 chính thức

- **唱歌 (buổi 9)** — brief đã lường trước case này. `唱歌` không có trong danh sách 150 HSK1 chuẩn (là từ HSK2/mở rộng). **Đề xuất:** bỏ khỏi 生词 chính thức của buổi 9; buổi 9 đã có đủ 15 từ chính thức (bao gồm nhóm động từ chung 来/回/去/做/开/住/看见 dùng để bù đủ 150 — xem mục 1) nên không cần từ thay thế, `唱歌` có thể giữ lại như **câu ví dụ/mở rộng** (không tính vào 生词 chính) nếu muốn.
- **零, 百 (buổi 3, §5 liệt kê "一~十, 零, 百")** — không thuộc 150 (HSK2+). Có thể vẫn dạy như mở rộng đếm số (không tính vào 150), không cần thay thế vì buổi 3 đã đủ 36 từ chính thức.
- **要, 可以 (buổi 6 hiện có)** — không thuộc 150. Giữ nguyên vì buổi 6 là nội dung đã có (out of scope, không tái soạn theo spec §2).
- **过, 快…了 (buổi 12 hiện có)** — không thuộc 150 (aspect marker HSK2). Giữ nguyên, out of scope.
- **口 (buổi 4, §5 liệt kê)** — không thuộc 150 chuẩn (chỉ có 岁/个/本/些/块 là lượng từ chính thức HSK1). Có thể vẫn dạy 口 như mở rộng lượng từ đếm người trong nhà (không tính vào 150).

### 3. Từ ngoài 150 trong nội dung buổi 6/10/12 hiện có (out of scope — chỉ liệt kê để tham khảo, KHÔNG sửa)

- Buổi 6: 起床, 上课, 做作业, 上学, 公共汽车, 地铁, 骑 (自行车), 走路, 要, 可以
- Buổi 10: 颜色, 红色, 橙色, 黄色, 绿色, 蓝色, 紫色, 粉色, 白色, 黑色, 灰色 (toàn bộ nhóm màu sắc — **không có màu nào** nằm trong 150 từ HSK1 chuẩn), 铅笔, 本子, 书包, 尺子, 橡皮, 筷子, và các lượng từ mở rộng 位/口/只/条/支/双/把/件/张/辆/杯/瓶
- Buổi 12: 晴天, 阴天, 下雪, 刮风, 春天, 夏天, 秋天, 冬天, 暖和, 凉快, 度, 过, 快…了

Theo spec §2/§11, nội dung 3 buổi này **không tái soạn** — các từ trên là nội dung mở rộng có giá trị (không sai), chỉ đơn giản không thuộc phạm vi đếm 150 từ checklist này.

### 4. Trường hợp "ôn" (từ dùng lại có chủ đích, không tính trùng)

是, 谁, 哪 (buổi 2/3 → ôn ở buổi 5) · 在 (buổi 3 → ôn ở buổi 8) · 电视, 看, 会, 想 (buổi 6 → ôn ở buổi 8/9) · 吃 (buổi 6 → ôn ở buổi 7) · 书, 学习 (buổi 8/5 → ôn ở buổi 9) · 好 (buổi 2 → ôn ở buổi 7, 11) · 没 (buổi 4 → ôn ở buổi 12) · 块 (buổi 10 → ôn ở buổi 11). Tất cả đã ghi chú trong bảng, chỉ tính 1 lần vào tổng 150.

## Verify

- Tổng số dòng trong 11 bảng buổi (2–12): 29+36+10+8+11+8+9+15+6+13+5 = **150** ✓
- Không từ nào xuất hiện ở 2 dòng khác nhau (đã rà tay theo index 1–150 của danh sách chuẩn, không trùng) ✓
- Mọi từ có đủ 汉字 + pinyin + nghĩa Việt ✓
- Mọi từ có đúng 1 buổi phụ trách (ghi chú "ôn ở buổi X" không phải gán buổi thứ 2) ✓
