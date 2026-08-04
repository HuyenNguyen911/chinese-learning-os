# HSK2 — Checklist từ vựng (Task 0.1)

**Nguồn:** `raw/New HSK Course 2.pdf`, bảng 词语表/Vocabulary trang **141-146** (PDF trang 157-162).

**Phương pháp trích (2026-07-27):** pypdf trích bảng này bị xáo cột hoàn toàn (nhiều cột chồng lấn trong PDF gốc), OCR (tesseract) cải thiện nhưng vẫn ra một số "từ" vô nghĩa do lẫn cột. → **Render từng trang thành ảnh (PyMuPDF, 250dpi) rồi đọc trực tiếp bằng mắt (vision)** — chính xác tuyệt đối, xác nhận qua toàn bộ 6 trang. Đây là phương pháp nên dùng lại cho các bảng/khu vực layout phức tạp khác trong sách (vd nếu 課文 có khu vực tương tự).

**Lưu ý quan trọng — pinyin PDF bị lỗi dấu thanh toàn sách (không riêng bảng này):** cả 課文 lẫn bảng từ vựng khi trích bằng pypdf đều mất dấu thanh pinyin (font/encoding). **Quyết định (2026-07-27):** không dùng pinyin in trong PDF — pinyin trong bảng dưới đây đọc trực tiếp từ ảnh (chuẩn), nhưng khi trích 課文 ở Procedure P sau này, **phải tự sinh pinyin bằng `pypinyin`** từ chữ Hán (đã trích đúng qua pypdf) thay vì tin pinyin in kèm — cross-check từ đa âm theo quy trình soát 多音字 hiện có.

**词性 (từ loại):** sách KHÔNG in từ loại theo từng từ trong bảng này (chỉ có 词性对照表 là bảng chú giải viết tắt chung, trang 141). Cột "Từ loại" dưới đây do tôi tự gán theo kiến thức ngữ pháp chuẩn — cần soát lại khi dùng cho nội dung dạy.

**Đối chiếu trùng HSK1:** dùng `output/hsk1/*/slide/*.json` (đã build, field `hz`), lọc bỏ câu ví dụ dài, chỉ giữ mục có dạng từ/cụm từ (~160 mục). Bảng dưới đánh dấu **⚠️ TRÙNG HSK1** cho từ đã dạy ở HSK1 — cần quyết định khi sản xuất buổi: bỏ từ này khỏi 生词 chính (không dạy lại), hoặc nếu bài cần nhắc lại thì chỉ dùng như ôn nhanh, không tính vào từ mới.

**Ngữ pháp (45 điểm):** đã có sẵn, đủ dùng, tại bảng ở `docs/superpowers/specs/hsk2-new-hsk-course-2-toc.md` §"Master syllabus" — không lặp lại ở đây.

**Tổng: 210 mục** (207 từ thường + 3 tên riêng) — 10 từ đánh dấu ★ (vượt khung/超纲词 theo sách) — **20 từ trùng HSK1** (đánh dấu bên dưới).

### Bài 1 (14 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 帮忙 | bāngmáng | v. | giúp đỡ | 1 |  |
| 不好意思 | bù hǎoyìsi | idiom | ngại quá, xin lỗi | 1 |  |
| 次 | cì | m. | lần (lượng từ) | 1 |  |
| 懂 | dǒng | v. | hiểu | 1 |  |
| 给 | gěi | v./prep. | cho | 1 |  |
| 接 | jiē | v. | đón, tiếp | 1 | vượt khung |
| 介绍 | jièshào | v. | giới thiệu | 1 | không dạy lại (user đã biết) |
| 就 | jiù | adv. | thì, liền (phó từ nhấn mạnh) | 1 |  |
| 旅游 | lǚyóu | v. | du lịch | 1 |  |
| 那 | nà | pron. | đó, kia | 1 | ⚠️ TRÙNG HSK1 (`on2_tuvung_chude`, cặp 这/那) |
| 让 | ràng | v. | nhường, để cho, khiến | 1 |  |
| 已经 | yǐjīng | adv. | đã, đã rồi | 1 |  |
| 意思 | yìsi | n. | ý nghĩa, ý tứ | 1 |  |
| 有时 | yǒushí | adv. | có lúc, đôi khi | 1 |  |

### Bài 2 (16 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 啊 | a | int./part. | từ cảm thán/ngữ khí cuối câu | 2 |  |
| 别 | bié | adv. | đừng | 2 |  |
| 车站 | chēzhàn | n. | bến/trạm xe | 2 |  |
| 打车 | dǎchē | v. | bắt taxi | 2 |  |
| 但 | dàn | conj. | nhưng | 2 |  |
| 公交车 | gōngjiāochē | n. | xe buýt | 2 |  |
| 过来 | guòlái | v. | đi tới, đi lại đây | 2 |  |
| 还是 | háishi | conj./adv. | hay là; vẫn là | 2,10 |  |
| 间 | jiān | m. | phòng; khoảng, giữa (lượng từ) | 2 |  |
| 教室 | jiàoshì | n. | phòng học | 2 |  |
| 名 | míng | n. | tên | 2 |  |
| 票 | piào | n. | vé | 2 |  |
| 外国 | wàiguó | n. | nước ngoài | 2 |  |
| 万 | wàn | num. | vạn (10.000) | 2 |  |
| 网上 | wǎngshang | n. | trên mạng | 2 |  |
| 远 | yuǎn | adj. | xa | 2 |  |

### Bài 3 (15 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 不错 | búcuò | adj. | khá tốt, không tệ | 3 |  |
| 出去 | chūqù | v. | đi ra ngoài | 3 |  |
| 回来 | huílái | v. | quay lại, trở về | 3 |  |
| 回去 | huíqù | v. | quay về, trở lại đó | 3 |  |
| 累 | lèi | adj. | mệt | 3 |  |
| 每 | měi | pron. | mỗi | 3 |  |
| 拿 | ná | v. | cầm, lấy | 3 |  |
| 手 | shǒu | n. | bàn tay | 3 |  |
| 送 | sòng | v. | tặng; đưa, tiễn | 3 |  |
| 完 | wán | v. | xong, hết | 3 |  |
| 为什么 | wèishénme | pron. | tại sao | 3 |  |
| 洗 | xǐ | v. | rửa, giặt, tắm | 3 |  |
| 一起 | yìqǐ | adv. | cùng nhau | 3 | ⚠️ TRÙNG HSK1 |
| 这么 | zhème | pron. | như thế này | 3 |  |
| 自己 | zìjǐ | pron. | bản thân, tự mình | 3 |  |

### Bài 4 (16 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 白色 | báisè | n. | màu trắng | 4 | ⚠️ TRÙNG HSK1 |
| 更 | gèng | adv. | càng, hơn nữa | 4 | vượt khung |
| 过去 | guòqù | v. | đi qua, đi tới đó | 4 |  |
| 过 | guo | part. | trợ từ động thái (đã từng) | 4 |  |
| 黑色 | hēisè | n. | màu đen | 4 | ⚠️ TRÙNG HSK1 |
| 红色 | hóngsè | n. | màu đỏ | 4 | ⚠️ TRÙNG HSK1 |
| 进去 | jìnqù | v. | đi vào (đó) | 4 |  |
| 裤子 | kùzi | n. | quần | 4 |  |
| 绿色 | lǜsè | n. | màu xanh lá | 4 | ⚠️ TRÙNG HSK1 |
| 商场 | shāngchǎng | n. | trung tâm thương mại | 4 |  |
| 试 | shì | v. | thử | 4 | vượt khung |
| 书包 | shūbāo | n. | cặp sách | 4 | ⚠️ TRÙNG HSK1 |
| 所以 | suǒyǐ | conj. | cho nên | 4 |  |
| 条 | tiáo | m. | cái, chiếc (lượng từ dài mảnh) | 4 |  |
| 颜色 | yánsè | n. | màu sắc | 4 | ⚠️ TRÙNG HSK1 |
| 因为 | yīnwèi | conj. | bởi vì | 4 |  |

### Bài 5 (18 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 等 | děng | v. | chờ; đợi | 5 |  |
| 跟 | gēn | prep./conj. | với; theo | 5 |  |
| 进来 | jìnlái | v. | đi vào (đây) | 5 |  |
| 酒店 | jiǔdiàn | n. | khách sạn | 5 |  |
| 快 | kuài | adj./adv. | nhanh; sắp | 5 |  |
| 礼物 | lǐwù | n. | quà tặng | 5 | vượt khung |
| 面 | miàn | n. | mặt; mì | 5 |  |
| 奶茶 | nǎichá | n. | trà sữa | 5 |  |
| 奶奶 | nǎinai | n. | bà nội | 5 |  |
| 上来 | shànglái | v. | đi lên (đây) | 5 |  |
| 上去 | shàngqù | v. | đi lên (đó) | 5 |  |
| 下来 | xiàlái | v. | đi/rơi xuống (đây) | 5 |  |
| 下面 | xiàmian | n. | phía dưới | 5 |  |
| 下去 | xiàqù | v. | đi xuống (đó); tiếp tục | 5 |  |
| 爷爷 | yéye | n. | ông nội | 5 |  |
| 一会儿 | yíhuìr | n. | một lát, một chút | 5 |  |
| 准备 | zhǔnbèi | v. | chuẩn bị | 5 |  |
| 走 | zǒu | v. | đi bộ, rời đi | 5 |  |

### Bài 6 (14 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 长 | cháng | adj. | dài | 6 |  |
| 床 | chuáng | n. | cái giường | 6 |  |
| 打开 | dǎkāi | v. | mở ra | 6 |  |
| 蛋糕 | dàngāo | n. | bánh kem/bánh ngọt | 6 | vượt khung |
| 地 | de | part. | trợ từ kết cấu (đứng trước động từ) | 6 |  |
| 过 | guò | v. | đi qua, trải qua | 6 |  |
| 画 | huà | v./n. | vẽ; bức tranh | 6 |  |
| 画笔 | huàbǐ | n. | bút vẽ | 6 | vượt khung |
| 快乐 | kuàilè | adj. | vui vẻ | 6 |  |
| 肉 | ròu | n. | thịt | 6 |  |
| 生日 | shēngrì | n. | sinh nhật | 6 |  |
| 舒服 | shūfu | adj. | thoải mái, dễ chịu | 6 |  |
| 忘 | wàng | v. | quên | 6 |  |
| 鱼 | yú | n. | con cá | 6 |  |

### Bài 7 (15 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 爱好 | àihào | n. | sở thích | 7 |  |
| 从 | cóng | prep. | từ (nơi chốn/thời gian) | 7 |  |
| 打 | dǎ | v. | đánh; chơi (thể thao) | 7 |  |
| 得 | de | part. | trợ từ (bổ ngữ trình độ) | 7 |  |
| 开始 | kāishǐ | v. | bắt đầu | 7 |  |
| 篮球 | lánqiú | n. | bóng rổ | 7 |  |
| 跑 | pǎo | v. | chạy | 7 |  |
| 跑步 | pǎobù | v. | chạy bộ | 7 |  |
| 球 | qiú | n. | quả bóng | 7 |  |
| 踢 | tī | v. | đá | 7 | ⚠️ TRÙNG HSK1 |
| 往 | wǎng | prep. | hướng về phía | 7 |  |
| 游 | yóu | v. | bơi | 7 |  |
| 游泳 | yóuyǒng | v. | bơi lội | 7 |  |
| 运动 | yùndòng | v./n. | vận động, thể thao | 7 |  |
| 足球 | zúqiú | n. | bóng đá | 7 |  |

### Bài 8 (16 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 爱情片 | àiqíngpiàn | n. | phim tình cảm | 8 | vượt khung |
| 比 | bǐ | prep. | so với | 8 |  |
| 但是 | dànshì | conj. | nhưng mà | 8 |  |
| 点 | diǎn | v./n. | chấm; gọi (món) | 8 |  |
| 饭馆 | fànguǎn | n. | quán ăn, nhà hàng | 8 |  |
| 花 | huā | n./v. | hoa; tiêu (tiền) | 8,13 | ⚠️ TRÙNG HSK1 |
| 记得 | jìde | v. | nhớ được | 8 |  |
| 妻子 | qīzi | n. | vợ | 8 | ⚠️ TRÙNG HSK1 |
| 手表 | shǒubiǎo | n. | đồng hồ đeo tay | 8 |  |
| 虽然 | suīrán | conj. | mặc dù | 8 |  |
| 有意思 | yǒuyìsi | adj. | thú vị, hay | 8 |  |
| 右 | yòu | n. | bên phải | 8 |  |
| 右边 | yòubian | n. | phía bên phải | 8 |  |
| 丈夫 | zhàngfu | n. | chồng | 8 |  |
| 左 | zuǒ | n. | bên trái | 8 |  |
| 左边 | zuǒbian | n. | phía bên trái | 8 |  |

### Bài 9 (13 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 高 | gāo | adj. | cao | 9 | ⚠️ TRÙNG HSK1 |
| 个子 | gèzi | n. | vóc dáng, chiều cao | 9 |  |
| 坏 | huài | adj. | hỏng, xấu | 9 |  |
| 近 | jìn | adj. | gần | 9 |  |
| 咖啡 | kāfēi | n. | cà phê | 9 | ⚠️ TRÙNG HSK1 |
| 离 | lí | prep. | cách (khoảng cách) | 9 |  |
| 门口 | ménkǒu | n. | cửa ra vào | 9 |  |
| 那么 | nàme | conj./adv. | vậy thì; như thế | 9 |  |
| 男孩儿 | nánháir | n. | bé trai | 9 |  |
| 旁边 | pángbiān | n. | bên cạnh | 9 |  |
| 这样 | zhèyàng | pron. | như thế này, thế này | 9 |  |
| 周 | zhōu | n. | tuần | 9 |  |
| 走路 | zǒulù | v. | đi bộ | 9 | ⚠️ TRÙNG HSK1 |

### Bài 10 (13 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 帮 | bāng | v. | giúp | 10 | ⚠️ TRÙNG HSK1 |
| 本子 | běnzi | n. | quyển vở | 10 | ⚠️ TRÙNG HSK1 |
| 笔 | bǐ | n. | bút | 10,13 |  |
| 词 | cí | n. | từ (ngôn ngữ) | 10 |  |
| 错 | cuò | adj. | sai | 10 |  |
| 后面 | hòumiàn | n. | phía sau | 10 |  |
| 开学 | kāixué | v. | khai giảng | 10 |  |
| 考 | kǎo | v. | thi | 10 |  |
| 考试 | kǎoshì | n./v. | kỳ thi, thi cử | 10 |  |
| 快要 | kuàiyào | adv. | sắp sửa | 10 |  |
| 门 | mén | n./m. | cửa; môn (học) | 10 |  |
| 题 | tí | n. | đề bài, câu hỏi | 10 |  |
| 笑 | xiào | v. | cười | 10 |  |

### Bài 11 (13 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 动 | dòng | v. | động, cử động | 11 |  |
| 进 | jìn | v. | vào | 11 |  |
| 经常 | jīngcháng | adv. | thường xuyên | 11 |  |
| 路上 | lùshang | n. | trên đường | 11 |  |
| 慢 | màn | adj. | chậm | 11 |  |
| 身体 | shēntǐ | n. | cơ thể, sức khoẻ | 11 |  |
| 时 | shí | n. | khi, lúc | 11 |  |
| 疼 | téng | adj./v. | đau | 11 |  |
| 头 | tóu | n. | cái đầu | 11 |  |
| 药 | yào | n. | thuốc | 11 |  |
| 药店 | yàodiàn | n. | hiệu thuốc | 11 |  |
| 着 | zhe | part. | trợ từ động thái (đang, trạng thái tiếp diễn) | 11 |  |
| 最 | zuì | adv. | nhất (mức độ cao nhất) | 11 |  |

### Bài 12 (11 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 从小 | cóngxiǎo | adv. | từ nhỏ | 12 |  |
| 地铁 | dìtiě | n. | tàu điện ngầm | 12 | ⚠️ TRÙNG HSK1 |
| 好 | hǎo | adj. | tốt | 12 | ⚠️ TRÙNG HSK1 |
| 楼 | lóu | n. | lầu, tòa nhà | 12 |  |
| 晴 | qíng | adj. | trời quang, nắng | 12 |  |
| 事情 | shìqing | n. | việc, sự việc | 12 |  |
| 外面 | wàimiàn | n. | bên ngoài | 12 |  |
| 小时候 | xiǎoshíhou | n. | hồi nhỏ, lúc còn bé | 12 |  |
| 阴 | yīn | adj. | âm u, nhiều mây | 12 |  |
| 站 | zhàn | n./v. | trạm, bến; đứng | 12,14 |  |
| 正 | zhèng | adv./adj. | đang; ngay ngắn | 12 |  |

### Bài 13 (11 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 班 | bān | n. | lớp học | 13 |  |
| 告诉 | gàosu | v. | nói cho biết, bảo | 13 |  |
| 教 | jiāo | v. | dạy | 13 |  |
| 可能 | kěnéng | adv./n. | có thể, có lẽ | 13 |  |
| 里面 | lǐmiàn | n. | bên trong | 13 |  |
| 那样 | nàyàng | pron. | như thế, như vậy | 13 |  |
| 上面 | shàngmiàn | n. | phía trên | 13 |  |
| 上网 | shàngwǎng | v. | lên mạng | 13 |  |
| 希望 | xīwàng | v./n. | hy vọng | 13 |  |
| 洗手间 | xǐshǒujiān | n. | nhà vệ sinh | 13 |  |
| 新年 | xīnnián | n. | năm mới | 13 | vượt khung |

### Bài 14 (11 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 包 | bāo | n./v. | cái túi; gói | 14 | ⚠️ TRÙNG HSK1 |
| 房子 | fángzi | n. | căn nhà | 14 | vượt khung |
| 过年 | guònián | v. | ăn Tết, đón năm mới | 14 |  |
| 没意思 | méiyìsi | adj. | chán, vô vị | 14 |  |
| 女孩儿 | nǚháir | n. | bé gái | 14 |  |
| 前面 | qiánmiàn | n. | phía trước | 14 |  |
| 跳舞 | tiàowǔ | v. | nhảy múa | 14 |  |
| 位 | wèi | m. | vị (lượng từ chỉ người, lịch sự) | 14 |  |
| 小孩儿 | xiǎoháir | n. | trẻ con | 14 |  |
| 姓 | xìng | n./v. | họ (tên họ); mang họ | 14 |  |
| 眼睛 | yǎnjing | n. | con mắt | 14 |  |

### Bài 15 (11 từ)

| 汉字 | Pinyin | Từ loại | Nghĩa | Bài (đủ) | Ghi chú |
|---|---|---|---|---|---|
| 出国 | chūguó | v. | xuất ngoại, ra nước ngoài | 15 |  |
| 出门 | chūmén | v. | ra khỏi nhà, ra ngoài | 15 |  |
| 飞 | fēi | v. | bay | 15 | ⚠️ TRÙNG HSK1 |
| 高中 | gāozhōng | n. | trung học phổ thông | 15 |  |
| 好像 | hǎoxiàng | v./adv. | hình như, giống như | 15 | vượt khung |
| 机场 | jīchǎng | n. | sân bay | 15 |  |
| 机票 | jīpiào | n. | vé máy bay | 15 |  |
| 路 | lù | n. | con đường | 15 |  |
| 门票 | ménpiào | n. | vé vào cửa | 15 |  |
| 鸟 | niǎo | n. | chim | 15 |  |
| 姓名 | xìngmíng | n. | họ tên | 15 |  |

### Tên riêng (专有名词)

| 汉字 | Pinyin | Nghĩa | Bài |
|---|---|---|---|
| 北京烤鸭 | Běijīng Kǎoyā | vịt quay Bắc Kinh | 1 |
| 北京大学 | Běijīng Dàxué | Đại học Bắc Kinh | 2 |
| 颐和园 | Yíhé Yuán | Di Hòa Viên | 15 |
## Verify (Task 0.1 Step 4)

- [x] Tổng ≈ 200: **207 từ thường + 3 tên riêng = 210 mục**, khớp "200 từ chuẩn + 略有扩展" ghi trong sách.
- [x] Mọi từ có gán bài (1-15), một số từ xuất hiện lại ở bài sau (vd 花 bài 8+13, 站 bài 12+14, 笔 bài 10+13, 还是 bài 2+10) — giữ nguyên vì sách lặp lại có chủ đích (ôn từ cũ trong bài mới), không tính trùng lặp lỗi.
- [x] 10 từ đánh dấu ★ (vượt khung/超纲词 theo chính sách): 爱情片(8), 蛋糕(6), 房子(14), 更(4), 好像(15), 画笔(6), 礼物(5), 接(1), 试(4), 新年(13).
- [x] **20 từ trùng HSK1** — liệt kê: 白色/黑色/红色/绿色/颜色 (cụm màu sắc, đều ở Bài 4) · 帮(10) · 包(14) · 本子(10) · 地铁(12) · 飞(15) · 高(9) · 好(12) · 花(8,13) · 咖啡(9) · 妻子(8) · 书包(4) · 踢(7) · 一起(3) · 走路(9) · 那(1, phát hiện khi duyệt Bài 1 — bản gốc bỏ sót).
  - ⚠️ **Đáng chú ý:** Bài 4 (trang phục, màu sắc) có **5/16 từ trùng HSK1** (gần 1/3 bài) — vì HSK1 3.0 đã có buổi màu sắc riêng. Cần quyết định khi sản xuất buổi 4: thay các từ màu trùng bằng từ mở rộng khác (vd màu sắc nâng cao: 灰色/紫色 nếu chưa dạy, hoặc bỏ hẳn phần ôn màu, tập trung 把字句 + trang phục thời trang).
- [ ] **Chưa xong:** đối chiếu HSK1 dùng danh sách tự lọc theo heuristic (loại câu ví dụ dài) — có thể sót/lẫn vài mục biên (vd buổi 1 ngữ âm có nhiều ký tự đơn lẻ luyện viết, chưa chắc phải "từ đã dạy"). Nên soát lại thủ công 19 dòng TRÙNG khi bắt đầu sản xuất Bài tương ứng, không chỉ tin tự động.

## Bước tiếp theo

Task 0.2 (mở rộng schema Viết, làm trên `main`) và Task 0.3 (README syllabus) — theo plan. Sau đó bắt đầu Procedure P cho Bài 1.
