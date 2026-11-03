# template/hskk-answer — video HSKK 高级 回答问题 (câu 5, câu 6 mỗi chủ đề Talk series)

Khuôn rút từ `output/Gen ảnh_video/talk02-hskk-c5/` (Chủ đề 1 · 快乐会传染 · câu 5; thư mục dự án lỡ đặt tên talk02 — thực chứa chủ đề 1). 1 video / câu hỏi, 2 bản EN + VI (chỉ khác phụ đề dịch).

## Luồng
1. **Nguồn nội dung:** `onluyen/bai-mau-cau5-6.md` (bài mẫu + Flow + cụm đắt giá) — user đã làm sẵn, KHÔNG tự soạn. Câu hỏi: `HSKK_LESSONS[n].p3` trong `on-luyen.html`.
2. **Cổng nội dung** (chưa tốn gì): bảng ~30 dòng phụ đề (ngắt ở dấu phẩy, ≤ 15 chữ Hán/dòng) + dịch VI/EN, mindmap (mở bài → thân 1 → thân 2 → kết), 5-6 cụm KHÓ & ngắn (pinyin chỉ khi khó), storyboard ~14 cảnh (≥ 1 hoạt động mới mỗi ~5s). User duyệt.
3. **Giọng:** `voice_edge.py --voice zh-CN-YunxiaNeural --rate +8% --pitch +4Hz` (user chê Yunxi -5% "mệt mệt hơi xuống") → `read.wav` + `timing.json`; `tts_intro.py` → câu hỏi, 现在开始, từng cụm. Hoặc user tự thu.
4. **Khung tĩnh = vẽ NGUYÊN CẢNH bằng model ảnh** (cách chốt từ chủ đề 2, 2026-11-03 — nét đẹp, tự nhiên hơn ghép): `src/scenes.json` (`style` + `yh` mô tả 越黄 + nhóm trang phục `uniform`/`home`/`friends` + mô tả từng cảnh `["nhóm", …, "mô tả"]`) → `python gen_scenes.py K1 K5` → `out/gen/<id>.png` (3:2). Gen 2 mẫu cho user duyệt trước rồi mới gen hàng loạt. Soát TỪNG ảnh: 2 越黄 trong 1 hình, tay thừa ở tiền cảnh, 越黄 to hơn bạn, thiếu món đỏ, đồng hồ sai tay/quá to → gen lại cảnh đó. Đạt → chép sang `assets/keyframes/`. (Cách cũ ghép `src/Keyframes.tsx` từ nhân vật tách nền vẫn dùng được khi cần giữ đúng 1 tấm nhân vật.)
5. **Không cắt/lót clip dọc từ video khác** vào khung ngang (user chê mờ, nhỏ) — cảnh nào cũng vẽ khung mới.
6. **Clip:** `src/motion.json` (prompt từng clip) → `gen_motion.py K1 K2 …` (tự bỏ tiếng; `.env` thiếu VIDEOGEN_* thì truyền qua biến môi trường — xem gotchas). Tối đa 2 luồng song song. Soát từng clip bằng `ffmpeg -vf "fps=1,scale=420:-1,tile=5x2"` — clip hay lệch sau ~5s (đổi màu tóc, mọc người lạ) → chỉ dùng phần đầu qua `USE` trong Full.tsx; lỗi 502 → chạy lại riêng clip đó.
7. **Ghép:** `src/Full.tsx` (S1 câu hỏi → S2 mindmap → S3 cụm → 现在开始 → S4 clip + phụ đề → kết follow) + `src/lines.json` (mốc đầu mỗi dòng phụ đề, dịch VI/EN) + `CLIPS` ánh xạ dòng → clip. `bash chunk_render.sh FullVI video/<slug>-vi.mp4` rồi `FullEN` (render chia đoạn, chống "No frame found"; không chạy 2 bản render song song). Nhạc nền SUỐT video, tự hạ khi có giọng.

Nội dung riêng chủ đề 1 (`PH`/`TOPIC`/`Q` trong `Frames.tsx`, `data.json`, `lines.json`, `timing.json`, `intro.json`) giữ làm mẫu — thay khi dựng chủ đề mới. Cần thêm `public/` (audio, img, motion, sfx, `bg.mp3`, `jx_avatar.png`, `yh_front.png`) như project gốc.
