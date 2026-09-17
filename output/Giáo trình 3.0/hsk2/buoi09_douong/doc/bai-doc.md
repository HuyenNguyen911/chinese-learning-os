# Buổi 9 — 我去买杯奶茶 (Tớ đi mua một cốc trà sữa)

> Trích nguyên văn từ `raw/New HSK Course 2.pdf`, **Bài 9, trang in sách 073-082**
> (PDF index 89-98, `doc/_tmp/p89.png`→`p98.png`, đã xoá sau khi bóc xong). Đọc trực
> tiếp bằng ảnh trang (pinyin in sách đủ dấu thanh, giữ nguyên). Nhân vật: 王一雪 (vợ),
> 刘明 (chồng) — cùng cặp đôi xuyên suốt Bài 6-9. **4 课文** nối tiếp trong 1 buổi đi mua
> sắm: mua quần cho con trai → rủ đi uống (cà phê/trà sữa, dùng 离) → đi bộ về nhà (thời
> lượng, 时量补语) → 课文4 王一雪 viết nhật ký tường thuật lại cả buổi.

## ⚠️ Sửa lại biên trang so với ghi chú cũ trong README (2026-08-06→nay)

`output/hsk2/README.md` (ghi chú "verify Bài 8/9/10 bằng ảnh") từng chốt **"Bài 9 thật =
trang 088-098"**. Đối chiếu trực tiếp ảnh trang lần này (đúng quy trình PyMuPDF render +
đọc vision, không dùng text extract thô) cho kết quả **khác**: trang bìa "Lesson 9 我去买
杯奶茶" nằm ở **PDF index 89, footer in "073"** — không phải 088. Toàn bộ nội dung Bài 9
(4 课文 + 3 điểm ngữ pháp + 综合练习 + 课堂活动 + 彩蛋 + 学习小结 7~9) nằm gọn trong
**PDF index 89-98 = trang in sách 073-082**. Trang PDF 88 (footer 072) vẫn là 课堂活动 +
彩蛋 **cuối Bài 8** (chủ đề nhà hàng/hỏi giá, khớp `buoi08_trinho_sosanh`), không phải mở
đầu Bài 9. Ghi chú cũ trong README bị lệch — cần sửa lại thành **073-082** khi đóng
session này (xem việc cần làm ở cuối file).

Nội dung 3 điểm ngữ pháp + 13 từ vựng thì **README ghi đúng từ trước** (比较句(3)[没有] ·
动词"离" · 时量补语(1); 13 từ khớp checklist), chỉ riêng số trang bị sai.

## 目标 Objectives (trang 073, nguyên văn sách)

1. 能听懂并使用"没有"描述事物之间的差别。(nghe hiểu + dùng "没有" mô tả khác biệt giữa sự vật)
2. 掌握动词"离"的用法，能表达处所或时间的距离。(dùng động từ "离" diễn đạt khoảng cách nơi chốn/thời gian)
3. 掌握时量补语（1）的用法，能描述动作持续的时间。(dùng thời lượng bổ ngữ (1) diễn đạt thời gian kéo dài của hành động)

## 热身 Warm-up (trang 073)
- Nối từ với tranh: 个子 gèzi · 走路 zǒulù · 咖啡 kāfēi · 门口 ménkǒu (4/13 từ mới xuất hiện
  ngay từ khởi động — tận dụng làm slide mở đầu/ôn nhanh).
- Bảng điền theo thực tế: 气温 (nhiệt độ hôm nay/hôm qua) · 价格 (giá cà phê/trà sữa) ·
  味道 (bao tử/sủi cảo ngon không) · 偏好 (thích xem TV/phim không) — tham khảo cho
  exercise-generator (câu hỏi cá nhân hoá).

---

## 课文1 — Trong cửa hàng, 王一雪 và 刘明 đang xem quần

王一雪：儿子的裤子坏了，我们给他买条新的吧。
Wáng Yīxuě: Érzi de kùzi huài le, wǒmen gěi tā mǎi tiáo xīn de ba.
*Quần của con trai hỏng rồi, mình mua cho nó một cái mới đi.*

刘明：好啊。
Liú Míng: Hǎo a.
*Được đó.*

王一雪：你看这条黑色的怎么样？
Wáng Yīxuě: Nǐ kàn zhè tiáo hēisè de zěnmeyàng?
*Cậu xem cái màu đen này thế nào?*

刘明：没有你上次买的那条好看。
Liú Míng: Méiyǒu nǐ shàng cì mǎi de nà tiáo hǎokàn.
*Không đẹp bằng cái lần trước cậu mua.*

王一雪：旁边那个男孩儿就穿了这样的裤子，我觉得很好看啊！
Wáng Yīxuě: Pángbiān nàge nánháir jiù chuānle zhèyàng de kùzi, wǒ juéde hěn hǎokàn a!
*Cậu bé đứng bên cạnh đang mặc đúng kiểu quần này, tớ thấy đẹp lắm đó!*

刘明：儿子的个子没有他那么高，穿上就不会太好看。
Liú Míng: Érzi de gèzi méiyǒu tā nàme gāo, chuānshang jiù bú huì tài hǎokàn.
*Con mình vóc dáng không cao bằng cậu bé đó, mặc vào sẽ không đẹp lắm đâu.*

王一雪：好吧，我们再去那边看看。
Wáng Yīxuě: Hǎo ba, wǒmen zài qù nàbiān kànkan.
*Được rồi, mình qua bên kia xem thêm.*

> 小语的提示: "会" ở đây nghĩa là "có thể/khả năng" (không phải "biết").

**生词 New Words:** 坏 huài (hỏng, xấu, adj.) · 旁边 pángbiān (bên cạnh, n.) ·
男孩儿 nánháir (bé trai, n.) · 这样 zhèyàng (như thế này, pron.) · 个子 gèzi (vóc dáng,
n.) · 那么 nàme (như thế đó, pron.) · 高 gāo (cao, adj. — ⚠️ TRÙNG HSK1)

---

## 课文2 — Ở cửa cửa hàng, 王一雪 và 刘明 đang đi ra

王一雪：门口有家奶茶店。你想喝杯奶茶吗？
Wáng Yīxuě: Ménkǒu yǒu jiā nǎichádiàn. Nǐ xiǎng hē bēi nǎichá ma?
*Ở cửa ra vào có một tiệm trà sữa. Cậu có muốn uống một cốc trà sữa không?*

刘明：我想喝咖啡，还是去咖啡店吧。
Liú Míng: Wǒ xiǎng hē kāfēi, háishi qù kāfēidiàn ba.
*Tớ muốn uống cà phê, hay là đi tiệm cà phê đi.*

王一雪：咖啡店离这儿有点儿远。
Wáng Yīxuě: Kāfēidiàn lí zhèr yǒudiǎnr yuǎn.
*Tiệm cà phê cách đây hơi xa.*

刘明：没关系，那家店的咖啡很好喝。
Liú Míng: Méi guānxi, nà jiā diàn de kāfēi hěn hǎohē.
*Không sao, cà phê tiệm đó rất ngon.*

王一雪：那你等一下，我去买杯奶茶。
Wáng Yīxuě: Nà nǐ děng yíxià, wǒ qù mǎi bēi nǎichá.
*Vậy cậu đợi chút, tớ đi mua một cốc trà sữa.*

刘明：你不想喝咖啡吗？
Liú Míng: Nǐ bù xiǎng hē kāfēi ma?
*Cậu không muốn uống cà phê à?*

王一雪：喝了咖啡，晚上就别想睡觉了。
Wáng Yīxuě: Hēle kāfēi, wǎnshang jiù bié xiǎng shuìjiào le.
*Uống cà phê vào là tối nay đừng hòng ngủ được.*

**生词 New Words:** 门口 ménkǒu (cửa ra vào, n.) · 咖啡 kāfēi (cà phê, n. — ⚠️ TRÙNG HSK1)
· 离 lí (cách, khoảng cách, v./prep.)

---

## 课文3 — Ở cửa tiệm cà phê, 王一雪 và 刘明 đang trò chuyện

刘明：我们打车回去吧。
Liú Míng: Wǒmen dǎchē huíqù ba.
*Mình bắt taxi về đi.*

王一雪：这里离家很近，还是走路吧。
Wáng Yīxuě: Zhèlǐ lí jiā hěn jìn, háishi zǒulù ba.
*Chỗ này cách nhà gần lắm, hay là đi bộ đi.*

刘明：要走多长时间？
Liú Míng: Yào zǒu duō cháng shíjiān?
*Phải đi bộ bao lâu?*

王一雪：走半个多小时就到了。
Wáng Yīxuě: Zǒu bàn gè duō xiǎoshí jiù dào le.
*Đi bộ hơn nửa tiếng là tới.*

刘明：好的。每天上下班都坐车，今天运动运动吧。
Liú Míng: Hǎo de. Měi tiān shàng xià bān dōu zuò chē, jīntiān yùndòng yùndòng ba.
*Được. Ngày nào đi làm về cũng ngồi xe, hôm nay vận động chút đi.*

**生词 New Words:** 近 jìn (gần, adj.) · 走路 zǒulù (đi bộ, v. — ⚠️ TRÙNG HSK1)

---

## 课文4 — 王一雪 viết nhật ký (đoạn văn tự sự, không hội thoại)

这周刘明休息，我下班后跟他去了一家商店。商店里边的衣服没有大商场里的好看。我们没有买到
喜欢的衣服，从商店出来就到咖啡店坐了坐。因为想运动运动，所以喝完东西，我们就走回家了。
Zhè zhōu Liú Míng xiūxi, wǒ xiàbān hòu gēn tā qùle yì jiā shāngdiàn. Shāngdiàn lǐbian de
yīfu méiyǒu dà shāngchǎng lǐ de hǎokàn. Wǒmen méiyǒu mǎidào xǐhuan de yīfu, cóng shāngdiàn
chūlái jiù dào kāfēidiàn zuòle zuò. Yīnwèi xiǎng yùndòng yùndòng, suǒyǐ hēwán dōngxi,
wǒmen jiù zǒuhuí jiā le.
*Tuần này Lưu Minh nghỉ, tan làm tớ với anh ấy đi đến một cửa hàng. Quần áo trong cửa hàng
không đẹp bằng ở trung tâm thương mại lớn. Bọn tớ không mua được bộ nào ưng ý, ra khỏi
cửa hàng liền ghé quán cà phê ngồi một lát. Vì muốn vận động chút nên uống xong đồ, bọn
tớ đi bộ về nhà.*

> 小语助力: "动词+到" (vd 买到) diễn đạt hành động đã đạt được mục đích — "买到" = mua được
> (thành công), khác "买" (chỉ hành động mua, chưa chắc có được).

**生词 New Words:** 周 zhōu (tuần, n.)

---

## 小语讲堂 — 3 điểm ngữ pháp Bài 9 (trang 075, 077, 078-079)

1. **比较句(3) Comparative Sentence (3) — "没有" (trang 075)** — dùng "没有" biểu thị so
   sánh, nghĩa "không bằng/không đạt tới". Cấu trúc: **A + 没有 + B + tính từ (cụm tính
   từ)**, tính từ có thể thêm "这么"/"那么" phía trước để nhấn mạnh mức độ của B. VD:
   儿子的个子没有他那么高。· 昨天没有今天这么冷。· 这块手表没有那块好看。
   Dạng khẳng định "有" của "没有" thường dùng trong câu hỏi so sánh: 妹妹有姐姐高吗？·
   那件衣服有这件好看吗？

2. **动词"离" Verb "离" (trang 077)** — biểu thị khoảng cách nơi chốn hoặc thời gian.
   Cấu trúc: **A + 离 + B + …**. VD: 咖啡店离这儿有点儿远。· 学校离医院不远。·
   现在离我的生日还有三天。

3. **时量补语(1) Complement of Duration (1) (trang 078-079)** — từ ngữ chỉ khoảng thời
   gian đứng sau động từ tạo thành bổ ngữ thời lượng, nói rõ hành động/trạng thái kéo dài
   bao lâu. Cấu trúc cơ bản: **Chủ ngữ + Động từ + Bổ ngữ thời lượng**. VD: 走半个多小时
   就到了。· 他们学了两年。· 我们休息十分钟。
   - Tân ngữ là **danh từ sự vật** → đứng **sau** bổ ngữ thời lượng: 我看了一个晚上电视。
   - Tân ngữ là **đại từ/xưng hô** → đứng **trước** bổ ngữ thời lượng: 李文等了她一个小时。·
     我找了陈天中二十多分钟。
   - Có tân ngữ → có thể **lặp lại động từ** rồi mới thêm bổ ngữ: 他们学中文学了两年。·
     李文等她等了一个小时。
   - Động từ ly hợp (离合词) → **bắt buộc lặp** ngữ tố động từ rồi thêm bổ ngữ: 安妮游泳游了
     一个下午。· 陈天中跑步跑了两个小时。
   - Có "了" sau động từ **và** "了" cuối câu → hành động **vẫn đang tiếp diễn**: 他写了半个
     小时汉字了。(现在还在写汉字) · 陈天中跑步跑了两个小时了。(还在跑步)

## 综合练习 (trang 081) — dạng bài (tham khảo cho exercise-generator)
- 选词填空 5 câu, ngân hàng từ: 旁边/走路/那么/个子/这样.
- Mô tả 4 tranh dùng 离/没有: bàn học cách cửa lớp (离) · siêu thị cách đây (离) · so sánh
  2 áo (没有) · so sánh chiều cao 2 bé trai (没有).

## 课堂活动 (trang 082) — Pair Work
2 người 1 nhóm: bàn cách đi du lịch, so sánh ưu nhược điểm các phương tiện — dùng
生词 + ngữ pháp bài này (mẫu: A: 你想怎么去上海? B: 我们都会开车，开车去吧。…)

## 小语的彩蛋 (trang 082) — Văn hoá: 新中式茶饮 (New Chinese Tea Drink)
Video ngắn giới thiệu trà sữa/trà trái cây kiểu Trung Quốc mới — khớp trực tiếp chủ đề
课文2 (mua trà sữa/cà phê) của bài này.

---

## Đối chiếu 生词 với checklist (`docs/superpowers/plans/hsk2-vocab-grammar-checklist.md`, Bài 9)

Checklist dự kiến 13 từ: 坏·个子·近·咖啡·离·门口·那么·男孩儿·旁边·这样·周·走路·高.

Bóc được từ sách (4 khối 生词): 坏·旁边·男孩儿·这样·个子·那么·高 (课文1, 7 từ) ·
门口·咖啡·离 (课文2, 3 từ) · 近·走路 (课文3, 2 từ) · 周 (课文4, 1 từ).

**Khớp 100% — không thiếu, không dư.** ⚠️ TRÙNG HSK1: 高 (cao — cùng nghĩa, ôn lại) ·
咖啡 (cà phê — cùng nghĩa, ôn lại) · 走路 (đi bộ — cùng nghĩa, ôn lại).

---

## Việc cần làm khi đóng session (sửa README)

`output/hsk2/README.md` dòng Bài 9 hiện ghi biên trang sai (theo ghi chú
"verify Bài 8/9/10 bằng ảnh" cũ: 088-098) — cần sửa lại thành **073-082** kèm dẫn chiếu
file này, giống cách Buổi 7/8 đã tự sửa ghi chú sai của phiên trước.
