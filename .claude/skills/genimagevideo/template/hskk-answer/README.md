# template/hskk-answer — video HSKK 高级 回答问题 (câu 5, câu 6 mỗi chủ đề Talk series)

Khuôn rút từ `output/Gen ảnh_video/talk01/hskk-c5/` (Chủ đề 1 · 快乐会传染 · câu 5). 1 video / câu hỏi, 2 bản EN + VI (chỉ khác phụ đề dịch).

## Luồng
1. **Nguồn nội dung:** `onluyen/bai-mau-cau5-6.md` (bài mẫu + Flow + cụm đắt giá) — user đã làm sẵn, KHÔNG tự soạn. Câu hỏi: `HSKK_LESSONS[n].p3` trong `on-luyen.html`.
2. **Cổng nội dung** (chưa tốn gì): bảng ~30 dòng phụ đề (ngắt ở dấu phẩy, ≤ 15 chữ Hán/dòng) + dịch VI/EN, mindmap (mở bài → thân 1 → thân 2 → kết), 5-6 cụm KHÓ & ngắn (pinyin chỉ khi khó), storyboard ~14 cảnh (≥ 1 hoạt động mới mỗi ~5s). User duyệt.
   **Soát storyboard trước khi đưa (talk03 c6, 2026-11-04):** có cảnh **chuyển ý** ở chỗ bắt đầu kể / đổi tâm trạng (vd sách mở ra phát sáng → hồi tưởng; hít sâu, nắm tay trước khi dám nói);
   bài là đối thoại 2 người thì người đối diện phải **tương tác** (khoảng lặng ~1,5s người kia nhép miệng hỏi, không giọng — `plan.json gapLine/gap` của `talk03/hskk-c6`);
   cảnh nào cũng rõ "đang làm gì" (user hỏi "cảnh này là gì?" khi chỉ ghi "giơ cuốn sách có bìa…"). **Dịch VI theo kiểu nói tự nhiên**, không bám chữ (bản bám chữ bị chê "chưa hay").
   Cụm đáng học: đủ trên **1 màn** (8 cụm: thẻ cao 158, cách 178 — `talk03/hskk-c6/src/Full.tsx`).
3. **Giọng:** `voice_edge.py --voice zh-CN-YunxiaNeural --rate +8% --pitch +4Hz` (user chê Yunxi -5% "mệt mệt hơi xuống") → `read.wav` + `timing.json`; `tts_intro.py` → câu hỏi, 现在开始, từng cụm. Hoặc user tự thu. Nhân vật nữ (瑾玄): `--voice zh-CN-XiaoxiaoNeural --rate +0%` (user: "đừng cố ép quá"). **Giọng KẾT (outro, câu "谢谢大家的观看～…关注我哦！") = giọng thật Huyền Babe** (`nhan-vat/README.md`) — chép `public/audio/outro.wav` + `src/outro.json` từ project trước cùng câu, KHÔNG gen TTS (Edge đọc 哦 cuối câu quá nhẹ, nghe như mất). Edge lỗi 403 → user tự `python -m pip install -U edge-tts` (gotchas).
4. **Khung tĩnh = vẽ NGUYÊN CẢNH bằng model ảnh** (cách chốt từ chủ đề 2, 2026-11-03 — nét đẹp, tự nhiên hơn ghép): `src/scenes.json` (`style` + `yh` mô tả 越黄 + nhóm trang phục `uniform`/`home`/`friends` + mô tả từng cảnh `["nhóm", …, "mô tả"]`) → `python gen_scenes.py K1 K5` → `out/gen/<id>.png` (3:2). Gen 2 mẫu cho user duyệt trước rồi mới gen hàng loạt. Soát TỪNG ảnh: 2 越黄 trong 1 hình, tay thừa ở tiền cảnh, 越黄 to hơn bạn, thiếu món đỏ, đồng hồ sai tay/quá to → gen lại cảnh đó. Đạt → chép sang `assets/keyframes/`.
   **Cảnh cùng 1 nơi (lớp học, thư viện…) phải đồng nhất nền:** dùng CHUNG 1 ảnh khởi đầu, phần khác nhau giữa 2 cảnh để muse làm (đổi nét mặt, cô giáo quay lại hỏi) hoặc vẽ thêm bằng PIL (giọt mồ hôi) — gen riêng từng cảnh thì nền lệch, user bắt.
   Học sinh phải **quay về phía bảng** + bàn **cách xa bảng** (ghi "desks grouped in the LEFT half, board on far RIGHT wall, wide empty floor between"). Cảnh trò chuyện giữ nguyên tư thế ngồi giữa các cảnh (không nhảy ngồi ↔ đứng).
   **Chữ Hán trong cảnh** (bảng, biển quán — user muốn có để biết là quán/lớp Trung): thêm khối `EXCEPTION to the no-text rule … exactly these characters '老王包子'` và bỏ tag `nobody_text` ở cảnh đó → model ag/gemini vẽ đúng chữ ngắn; soát TỪNG chữ.
   Muse hay tự cắt/zoom giữa đoạn (K5, K13 talk03 c6) hoặc cho nhân vật đi ra tiền cảnh → ghi "stays STANDING STILL, does NOT walk"; cắt bằng `use`. (Cách cũ ghép `src/Keyframes.tsx` từ nhân vật tách nền vẫn dùng được khi cần giữ đúng 1 tấm nhân vật.)
5. **Không cắt/lót clip dọc từ video khác** vào khung ngang (user chê mờ, nhỏ) — cảnh nào cũng vẽ khung mới.
6. **Clip:** `src/motion.json` (prompt từng clip) → `gen_motion.py K1 K2 …` (tự bỏ tiếng; `.env` thiếu VIDEOGEN_* thì truyền qua biến môi trường — xem gotchas). Tối đa 2 luồng song song. Soát từng clip bằng `ffmpeg -vf "fps=1,scale=420:-1,tile=5x2"` — clip hay lệch sau ~5s (đổi màu tóc, mọc người lạ) → chỉ dùng phần đầu qua `USE` trong Full.tsx; lỗi 502 → chạy lại riêng clip đó.
7. **Ghép:** `src/Full.tsx` (S1 câu hỏi → S2 mindmap → S3 cụm → 现在开始 → S4 clip + phụ đề → kết follow) + `src/lines.json` (mốc đầu mỗi dòng phụ đề, dịch VI/EN) + `CLIPS` ánh xạ dòng → clip. **Trước khi render: `python make_frames.py`** (CLIPS/USE trong đó phải khớp Full.tsx) → cắt + đổi tốc độ từng đoạn clip cho khớp lời đọc, tách JPG từng khung vào `public/frames/` (gitignored, máy khác phải chạy lại); Full.tsx hiện ảnh thay vì phát mp4 → hết lỗi "No frame found", render 3 luồng ~7 phút. Phụ đề mỗi dòng ≤ 15 chữ Hán (dòng dài tự thu chữ nhưng vẫn nên tách). `bash chunk_render.sh FullVI video/<slug>-vi.mp4` rồi `FullEN` (render chia đoạn, chống "No frame found"; không chạy 2 bản render song song). Nhạc nền SUỐT video, tự hạ khi có giọng.

Nội dung mẫu hiện tại = **Chủ đề 2 · câu 6 (在家上学)**, đồng bộ từ `talk02/hskk-c6` ngày 2026-11-03 (`PH`/`TOPIC`/`Q` trong `Frames.tsx`, câu hỏi + mindmap + `CLIPS`/`USE`/`PHRASE_AT` trong `Full.tsx`, `data.json`, `lines.json`, `timing.json`, `intro.json`, `scenes.json`, `motion.json`) — thay hết khi dựng chủ đề mới. Tạo bằng `new_project.py talkNN/hskk-cN --template hskk-answer`.

**Khung tĩnh vẽ nguyên cảnh:** `src/scenes.json` = `style` + khối mô tả theo tag (`jx`, `yh`, `son`, `jx_home`…) + `scenes.<id> = [tag…, mô tả]` → `python gen_scenes.py [id…]` → `out/gen/<id>.png` → soát → chép `assets/keyframes/`.
**Cắt clip:** `make_frames.py` có `USE = { id: giây dùng }` (phải khớp `USE` trong `Full.tsx`) và `START = { id: giây bỏ đầu }` (đoạn đầu clip bị đổi nền / giật khung). Cần thêm `public/` (audio, img, motion, sfx, `bg.mp3`, `jx_avatar.png`, `yh_front.png`) như project gốc.

**Thứ tự VI/EN:** render VI trước, user xem + chốt rồi mới render EN (`FullEN`) theo bản VI đã chốt — không chạy liền cả hai.

**Bản mới nhất để chép = `talk03/hskk-c5` (2026-11-04)** — khuôn này vẫn là bản talk02; chép `src/` + `make_frames.py` từ talk03 sẽ có sẵn:
- `CLIPS` nhận **dòng 0** (`lineT(0)` = lúc 现在开始, cảnh mở màn trước khi đọc) và **dòng ảo** sau câu cuối (`VIRT = [0, 3.0, 7.5]` → cảnh kết không lời, `OUT0 = ANS_END + HOLD`). `make_frames.py` phải có cùng `CLIPS`/`VIRT`/`USE`/`START`.
- Tốc độ clip ≤ 1.0 (không tua nhanh); hồi tưởng: `FLASH` = các cảnh phủ sepia + viền tối, loé trắng ở đầu cảnh hồi tưởng đầu và cảnh hiện tại kế tiếp; cảnh dẫn vào hồi tưởng đẩy cận (`zoom`, `transformOrigin`).
- Phụ đề: dòng dịch tự thu chữ `min(36, 1000 / (0.52 × số ký tự))` — câu dịch dài từng bị cắt mép khung.
- `ITEMS` trong `tts_intro.py` (`p0…p5`) phải **cùng thứ tự** với `S3_LIST` trong `Full.tsx` — lệch thì thẻ 挑 hiện mà giọng đọc 真诚 (user tưởng "gen từ danh sách cũ").
- Đổi câu chữ bài đọc → chỉ cần chạy lại `voice_edge.py` + sửa `lines.json`/`PHRASE_AT`/`CLIPS` theo số dòng mới; clip không phải gen lại.
