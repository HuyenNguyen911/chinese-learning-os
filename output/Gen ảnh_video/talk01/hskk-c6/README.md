# template/hskk-answer — video HSKK 高级 回答问题 (câu 5, câu 6 mỗi chủ đề Talk series)

Khuôn rút từ `output/Gen ảnh_video/talk02-hskk-c5/` (Chủ đề 1 · 快乐会传染 · câu 5; thư mục dự án lỡ đặt tên talk02 — thực chứa chủ đề 1). 1 video / câu hỏi, 2 bản EN + VI (chỉ khác phụ đề dịch).

## Luồng
1. **Nguồn nội dung:** `onluyen/bai-mau-cau5-6.md` (bài mẫu + Flow + cụm đắt giá) — user đã làm sẵn, KHÔNG tự soạn. Câu hỏi: `HSKK_LESSONS[n].p3` trong `on-luyen.html`.
2. **Cổng nội dung** (chưa tốn gì): bảng ~30 dòng phụ đề (ngắt ở dấu phẩy, ≤ 15 chữ Hán/dòng) + dịch VI/EN, mindmap (mở bài → thân 1 → thân 2 → kết), 5-6 cụm KHÓ & ngắn (pinyin chỉ khi khó), storyboard ~14 cảnh (≥ 1 hoạt động mới mỗi ~5s). User duyệt.
3. **Giọng:** `voice_edge.py --voice zh-CN-YunxiaNeural --rate +8% --pitch +4Hz` (user chê Yunxi -5% "mệt mệt hơi xuống") → `read.wav` + `timing.json`; `tts_intro.py` → câu hỏi, 现在开始, từng cụm. Hoặc user tự thu.
4. **Nhân vật/nền** theo `reference/design-rules.md` §13 + `nhan-vat/README.md`; nền tối giản (ít chi tiết), nhân vật gen chung 1 ảnh theo nhóm, vật cầm do AI vẽ trong tay.
5. **Khung tĩnh:** `src/Keyframes.tsx` (K1…Kn, 1280×720, KHÔNG chữ) → `npx remotion still src/index.ts K1 assets/keyframes/K1.png`.
6. **Clip:** `src/motion.json` (prompt từng clip) → `gen_motion.py K1 K2 …` (tự bỏ tiếng; `.env` thiếu VIDEOGEN_* thì truyền qua biến môi trường — xem gotchas). Tối đa 2 luồng song song. Soát từng clip bằng `ffmpeg -vf "fps=1,scale=420:-1,tile=5x2"`.
7. **Ghép:** `src/Full.tsx` (S1 câu hỏi → S2 mindmap → S3 cụm → 现在开始 → S4 clip + phụ đề → kết follow) + `src/lines.json` (mốc đầu mỗi dòng phụ đề, dịch VI/EN) + `CLIPS` ánh xạ dòng → clip. `npx remotion render src/index.ts FullVI video/<slug>-vi.mp4 --concurrency=4` rồi `FullEN`. Nhạc nền SUỐT video, tự hạ khi có giọng.

Nội dung riêng chủ đề 1 (`PH`/`TOPIC`/`Q` trong `Frames.tsx`, `data.json`, `lines.json`, `timing.json`, `intro.json`) giữ làm mẫu — thay khi dựng chủ đề mới. Cần thêm `public/` (audio, img, motion, sfx, `bg.mp3`, `jx_avatar.png`, `yh_front.png`) như project gốc.
