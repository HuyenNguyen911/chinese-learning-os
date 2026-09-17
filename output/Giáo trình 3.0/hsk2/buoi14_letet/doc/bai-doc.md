# Buổi 14 — 一个人过年多没意思啊 (Ăn Tết một mình chán quá)

> Trích từ `raw/New HSK Course 2.pdf`. **Bài 14 = PDF trang 137-145** (9 trang, khớp độ
> dài trung bình các bài khác). Xác định biên bằng cách tìm điểm bắt đầu Lesson 15
> ("我想再去一次中国") — xuất hiện rõ ràng ở **PDF trang 146** (`目标objectives` + tên bài,
> dòng "Lesson / 我想再去一次中国" tại `raw/New HSK Course 2.pdf.txt` dòng 4598-4601) →
> Bài 14 kết thúc đúng trang 145, không lấn sang 146.

## ⚠️ Sai khác quy trình lần này — CHƯA verify bằng ảnh trang
Mọi buổi trước (Bài 3, 5-10) đều verify biên trang bằng cách render ảnh PDF (PyMuPDF) rồi
đọc trực tiếp, vì text-layer của sách này từng gây lệch bài liên tiếp. Lần này `pip
install pymupdf` bị chặn ở tầng permission trong session (không cài được), user đã đồng ý
dùng tạm text-layer sẵn có (`raw/New HSK Course 2.pdf.txt`, trích bằng pypdf) + đối chiếu
kỹ với checklist từ vựng/ngữ pháp thay vì ảnh. Chữ Hán trong text-layer đọc mạch lạc,
không bị xáo trộn cột (khác lo ngại ban đầu) — chỉ phần pinyin in kèm bị mất dấu thanh
(vấn đề đã biết toàn sách, luôn tự sinh lại bằng pypinyin) và một số khối 生词 dạng bảng bị
OCR lẫn ký tự rác. **Khuyến nghị: nếu có dịp cài được pymupdf, nên render lại ảnh trang
137-145 để đối chiếu 1 lần cho chắc trước khi khoá buổi này**, nhưng nội dung dưới đây đã
đối chiếu chéo 100% với checklist nên đủ tin cậy để bắt đầu build.

## 目标 Objectives (trang 137, nguyên văn sách) — **3 điểm, không phải 2 như bảng README/TOC cũ**
1. 能听懂并描述某处存在某人或某物。(nghe hiểu + miêu tả có ai/vật gì tồn tại ở một nơi) → **存现句(2)**
2. 能听懂并使用复合趋向补语表达动作的方向。(nghe hiểu + dùng bổ ngữ xu hướng phức hợp diễn đạt hướng của động tác) → **复合趋向补语**
3. 掌握程度副词"多"的用法，能表达程度很高的意思。(nắm phó từ mức độ "多" diễn đạt mức độ rất cao) → **程度副词"多"**

> README (`output/hsk2/README.md` dòng Bài 14) và TOC spec chỉ ghi "存现句 · 复合趋向补语"
> — thiếu điểm thứ 3 **程度副词"多"**. Cần sửa cả 2 file khi đóng session.
> Ghi chú thêm: 复合趋向补语 đã được "đưa sớm" một phần ở Buổi 5 (theo ghi chú kỹ thuật
> README) nên học viên đã quen dạng đơn giản — Bài 14 dạy dạng **phức hợp** (上/下/进/出/
> 回/过 + 来/去, và 起来) là nội dung mới thật sự, không phải ôn lại thuần tuý.

## 热身 Warm-up (trang 137)
Nối từ với tranh: 包 bāo · 女孩儿 nǚháir · 跳舞 tiàowǔ · 眼睛 yǎnjing (4/11 từ mới xuất
hiện ngay từ khởi động).

---

## 课文1 — Trên đường về nhà, 李文 và 王一飞 vừa đi vừa chuyện trò

李文：王老师，你家楼下站着一个人。
Lǐ Wén: Wáng lǎoshī, nǐ jiā lóuxià zhànzhe yí ge rén.
*Cô Vương, dưới nhà cô có một người đang đứng đó.*

王一飞：我家楼下？我看看。
Wáng Yīfēi: Wǒ jiā lóuxià? Wǒ kànkan.
*Dưới nhà tôi á? Để tôi xem.*

李文：那个人穿着黑色的裤子，手里还拿着一个黑色的包。
Lǐ Wén: Nàge rén chuānzhe hēisè de kùzi, shǒulǐ hái názhe yí ge hēisè de bāo.
*Người đó mặc quần đen, tay còn cầm một cái túi màu đen.*

王一飞：我看见那个人了，他是我男朋友。
Wáng Yīfēi: Wǒ kànjiàn nàge rén le, tā shì wǒ nánpéngyou.
*Tôi thấy người đó rồi, đó là bạn trai tôi.*

李文：那我们快过去吧。
Lǐ Wén: Nà wǒmen kuài guòqù ba.
*Vậy mình mau qua đó đi.*

> Ngữ pháp minh hoạ ngay ở câu mở đầu: "楼下站着一个人" = 存现句(2) (处所 + động từ + 着 +
> người/vật phiếm chỉ).

**生词 New Words:** 包 bāo (cái túi; gói, n./v.)

---

## 课文2 — Dưới nhà, 王一飞 gặp 杨同乐 (bạn trai)

王一飞：同乐，真是你啊！上次打电话，你说有时间过来看我，没想到这么快就来了！
Wáng Yīfēi: Tóngle, zhēnshi nǐ a! Shàng cì dǎ diànhuà, nǐ shuō yǒu shíjiān guòlái kàn wǒ,
méi xiǎngdào zhème kuài jiù lái le!
*Đồng Nhạc, đúng là anh rồi! Lần trước gọi điện anh bảo có thời gian sẽ qua thăm em,
không ngờ anh đến nhanh vậy!*

杨同乐：就要过年了，你一个人在这儿多没意思啊，所以我就早早过来了。
Yáng Tónglè: Jiù yào guònián le, nǐ yí ge rén zài zhèr duō méiyìsi a, suǒyǐ wǒ jiù zǎozǎo
guòlái le.
*Sắp Tết rồi, em một mình ở đây chán biết bao, nên anh đến sớm luôn.*

王一飞：你能来，我太高兴了！
Wáng Yīfēi: Nǐ néng lái, wǒ tài gāoxìng le!
*Anh đến được là em vui lắm rồi!*

杨同乐：一飞，你旁边这位是？
Yáng Tónglè: Yīfēi, nǐ pángbiān zhè wèi shì?
*Nhất Phi, người đứng cạnh em đây là ai vậy?*

王一飞：同乐，这是李文，他在我们学校学医。李文，这是我男朋友杨同乐。
Wáng Yīfēi: Tóngle, zhè shì Lǐ Wén, tā zài wǒmen xuéxiào xué yī. Lǐ Wén, zhè shì wǒ
nánpéngyou Yáng Tónglè.
*Đồng Nhạc, đây là Lý Văn, cậu ấy học y ở trường em. Lý Văn, đây là bạn trai chị, Dương
Đồng Nhạc.*

杨同乐：李文，很高兴认识你！
Yáng Tónglè: Lǐ Wén, hěn gāoxìng rènshi nǐ!
*Lý Văn, rất vui được quen em!*

李文：认识你我也很高兴！我家就在前面那个楼，有时间来玩。
Lǐ Wén: Rènshi nǐ wǒ yě hěn gāoxìng! Wǒ jiā jiù zài qiánmiàn nàge lóu, yǒu shíjiān lái wán.
*Em cũng rất vui được quen anh! Nhà em ở ngay toà nhà phía trước kia, lúc nào rảnh ghé
chơi.*

> Ngữ pháp: "多没意思啊" = 程度副词"多" trong câu cảm thán, biểu thị mức độ cao.

**生词 New Words:** 过年 guònián (ăn Tết, đón năm mới, v.) · 没意思 méiyìsi (chán, vô vị,
adj.) · 位 wèi (lượng từ chỉ người, lịch sự, m.) · 前面 qiánmiàn (phía trước, n.)

---

## 课文3 — Ở nhà 王一飞, 杨同乐 và 王一飞 ngồi phòng khách chuyện trò

杨同乐：一飞，你住的房子真不错，很大，离学校也不远。
Yáng Tónglè: Yīfēi, nǐ zhù de fángzi zhēn búcuò, hěn dà, lí xuéxiào yě bù yuǎn.
*Nhất Phi, căn nhà em ở thật tốt, rộng, mà cách trường cũng không xa.*

王一飞：是啊！我楼下还住着一家中国人，他们人很好。
Wáng Yīfēi: Shì a! Wǒ lóuxià hái zhùzhe yì jiā Zhōngguó rén, tāmen rén hěn hǎo.
*Đúng vậy! Dưới nhà em còn có một gia đình người Trung Quốc ở, họ tốt bụng lắm.*

杨同乐：这样你有事情就可以找他们帮忙。
Yáng Tónglè: Zhèyàng nǐ yǒu shìqing jiù kěyǐ zhǎo tāmen bāngmáng.
*Vậy nếu có việc gì em có thể nhờ họ giúp.*

王一飞：对，我也帮他们家的小孩儿学中文。
Wáng Yīfēi: Duì, wǒ yě bāng tāmen jiā de xiǎoháir xué Zhōngwén.
*Đúng vậy, em cũng giúp con nhỏ nhà họ học tiếng Trung.*

杨同乐：我记得你跟我说过，是个女孩儿，学得也很好。
Yáng Tónglè: Wǒ jìde nǐ gēn wǒ shuōguo, shì ge nǚháir, xué de yě hěn hǎo.
*Anh nhớ em từng kể, là một bé gái, học cũng giỏi lắm.*

王一飞：没错，她经常跑上来找我玩。
Wáng Yīfēi: Méi cuò, tā jīngcháng pǎo shànglái zhǎo wǒ wán.
*Đúng vậy, bé ấy hay chạy lên tìm em chơi.*

杨同乐：你问问他们什么时候有时间，我请他们吃个饭。
Yáng Tónglè: Nǐ wènwen tāmen shénme shíhou yǒu shíjiān, wǒ qǐng tāmen chī ge fàn.
*Em hỏi họ khi nào rảnh, anh mời họ ăn cơm.*

> Ngữ pháp: "跑上来" = 复合趋向补语 (跑 + 上来, động tác + hướng lên trên + về phía người nói).

**生词 New Words:** 房子 fángzi (căn nhà, n.) · 小孩儿 xiǎoháir (trẻ con, n.) · 女孩儿
nǚháir (bé gái, n.)

---

## 课文4 — 王一飞 viết nhật ký (tự sự, không hội thoại)

我男朋友姓杨，叫杨同乐。他高个子、大眼睛，唱歌唱得很好，跳舞跳得也不错。他和我姐姐一起
工作，是姐姐介绍我们认识的。他告诉我，从见到我的第一天开始，他就喜欢上我了。
Wǒ nánpéngyou xìng Yáng, jiào Yáng Tónglè. Tā gāo gèzi, dà yǎnjing, chàng gē chàng de hěn
hǎo, tiàowǔ tiào de yě búcuò. Tā hé wǒ jiějie yìqǐ gōngzuò, shì jiějie jièshào wǒmen rènshi
de. Tā gàosu wǒ, cóng jiàndào wǒ de dì-yī tiān kāishǐ, tā jiù xǐhuan shàng wǒ le.
*Bạn trai tôi họ Dương, tên Dương Đồng Nhạc. Anh ấy cao, mắt to, hát hay, nhảy cũng đẹp.
Anh ấy làm cùng chỗ chị gái tôi, chính chị giới thiệu chúng tôi quen nhau. Anh ấy kể với
tôi, từ ngày đầu gặp tôi là đã thích tôi rồi.*

> 小语的提示 (nguyên văn sách): "喜欢上" 表示开始喜欢，并一直喜欢下去 — "上" trong "喜欢上"
> là dùng mở rộng nghĩa của bổ ngữ xu hướng (bắt đầu một trạng thái và duy trì), không phải
> nghĩa hướng "lên" gốc — ví dụ hay để nối 课文4 với điểm ngữ pháp 复合趋向补语 chính của bài.

**生词 New Words:** 姓 xìng (họ; mang họ, n./v.) · 跳舞 tiàowǔ (nhảy múa, v. — đã xuất hiện
ở 热身) · 眼睛 yǎnjing (con mắt, n. — đã xuất hiện ở 热身)

## 综合练习 (trang 144) — chọn từ điền câu, tham khảo cho exercise-generator
Ngân hàng từ: 位·过年·跳舞·姓·眼睛. 5 câu mẫu: tả mắt to đẹp của con · mấy năm không về nước,
năm nay muốn về ăn Tết · từ nhỏ học nhảy với thầy, học hơn 10 năm · tự giới thiệu "tôi họ
Lý..." · hỏi "chỉ mình anh thôi ạ?" — "còn một người bạn nữa, anh ấy đến là gọi món luôn".

## 课堂活动 (trang 145) — Pair Work
2 người 1 nhóm: mô phỏng giúp bạn xem nhà thuê, nói ưu/nhược điểm căn nhà (bám 房子/离/
小孩儿 và 复合趋向补语).

---

## Đối chiếu 生词 với checklist (`docs/superpowers/plans/hsk2-vocab-grammar-checklist.md`, Bài 14)

Checklist dự kiến 11 từ: 包·房子·过年·没意思·女孩儿·前面·跳舞·位·小孩儿·姓·眼睛.

Bóc được từ sách (4 khối 生词): 包 (课文1, 1 từ) · 过年·没意思·位·前面 (课文2, 4 từ) ·
房子·小孩儿·女孩儿 (课文3, 3 từ) · 姓·跳舞·眼睛 (课文4, 3 từ — 跳舞/眼睛 lặp lại từ 热身).

**Khớp 100% — không thiếu, không dư.** Không có từ nào trùng HSK1 trong bài này (khác các
buổi trước luôn có 1-3 từ trùng).

---

## Chủ đề thật của buổi (rộng hơn tên "lễ Tết" trong README)
Không chỉ "过年/lễ Tết" — mạch chính là **王一飞 giới thiệu bạn trai** (杨同乐) đến thăm dịp
Tết vì sợ cô ở một mình buồn, xen giữa là **tả nhà thuê** (房子, hàng xóm) và **trẻ con
hàng xóm** (小孩儿/女孩儿 cô dạy tiếng Trung). Đề xuất chủ đề slide: "Tết + giới thiệu người
yêu/bạn trai" thay vì chỉ thuần "lễ Tết, cảm xúc" — bám sát nội dung 4 课文 hơn.

## Cập nhật sau khi trao đổi nội dung slide (chốt trước khi build)

1. **复合趋向补语 KHÔNG dạy lại ở Buổi 14** — kiểm tra lại phát hiện điểm này đã được dạy
   khá đầy đủ ở **Buổi 5** (kể cả quy tắc đặt tân ngữ địa điểm/sự vật), nên slide Buổi 14
   bỏ hẳn slide ngữ pháp riêng cho điểm này (dù sách chính thức đặt nó ở Bài 14) — chỉ còn
   xuất hiện tự nhiên qua 课文3 gốc sách ("跑上来") như ôn nhận diện, không dạy lại từ đầu.
2. **Thay bằng 2 điểm mở rộng thật (không trùng bài nào khác)**:
   - **动词+"上" (nghĩa mở rộng: bắt đầu+duy trì trạng thái)** — nguồn 小语的提示 trang 144
     (课文4: "喜欢上"), có callback "爱上" từ tên bài Buổi 13.
   - **已经 + khoảng thời gian + 没 + động từ + 了** — nguồn nguyên văn 综合练习 Bài 14
     ("他已经几年没回国了，今年想回国过年"), chưa từng dạy ở buổi nào khác.
   - Đã cân nhắc và loại 2 phương án khác trước khi chốt: "动词+认识" (giới thiệu quen
     nhau, ứng dụng 结果补语 Bài 3) và "动态助词着 cơ bản" (lấp lỗ hổng Buổi 11 chưa build) —
     cả 2 đều bị từ chối, giữ lại làm tham khảo nếu cần dùng ở buổi khác.
3. **Từ vựng mở rộng dùng ĐỦ 21/21 từ** user cung cấp (không chỉ chọn lọc 8 từ như bản
   nháp đầu) — xem `slide/buoi14.json` 生词 1/13 → 13/13. Nhóm theo sơ đồ cây 3 nhánh:
   loại nhà (公寓/别墅/宿舍/平房) · phòng (客厅/卧室/厨房/卫生间/阳台) · việc nhà (打扫/收拾/
   擦窗户/拖地/倒垃圾/洗衣服/晒衣服/烹饪/洗碗/搬家/浇花/修东西).
4. **Bài tập (exercise-generator) khi làm sau này**: chỉ kiểm tra 4 điểm ngữ pháp thật sự
   dạy ở slide (存现句(2) · 程度副词"多" · 已经…没…了 · 动词+上), KHÔNG đưa 复合趋向补语 vào
   bài tập như một điểm "mới học ở buổi này".

## Việc cần làm khi đóng session (sửa README + TOC)
1. `output/hsk2/README.md` dòng Bài 14: sửa ngữ pháp thành "存现句(2) · 复合趋向补语 ·
   程度副词"多"" (thêm điểm thứ 3), sửa cột chủ đề nếu chốt theo đề xuất trên.
2. `docs/superpowers/specs/hsk2-new-hsk-course-2-toc.md` dòng Bài 14: cập nhật trang
   "~121" → "137-145 (verify text-layer, khuyến nghị verify lại bằng ảnh nếu cài được
   pymupdf)", cập nhật cột ngữ pháp thêm 程度副词"多".
