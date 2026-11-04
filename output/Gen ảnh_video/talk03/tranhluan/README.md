# talk03/tranhluan — clip 活人图书馆 (越黄 hỏi, 瑾玄 hiểu nhầm thành "thư viện hay đi")

Thành phẩm: `video/talk03-tranhluan.mp4` (~35s, 9:16). User duyệt 2026-11-04.

Luồng đã chạy (mỗi câu thoại = 1 đoạn muse-video riêng, chỉ người nói mở miệng):
1. `assets/bg_park.png` = nền công viên trống (gen 1024x1536). Cặp nhân vật vẽ trên nền mint: `python gen_pairs.py <tư thế>` → `python cutout_mint.py <tư thế>`.
2. Ghép khung: `python compose_key.py <tư thế> m_<tư thế> 0.40 0.75` (nhân vật cao 40% khung, chân ở 75%) → `assets/keyframes/m_*.png`.
   Model ảnh KHÔNG nghe lệnh "nhân vật nhỏ" khi vẽ nguyên cảnh dọc → phải ghép như vậy mới chỉnh được cỡ/vị trí.
3. `src/motion.json` → `python gen_motion.py m_walk m_ask …` (tuần tự) → `assets/motion/m_*.mp4`.
4. Giọng Edge: 越黄 `zh-CN-YunxiaNeural +8% +4Hz`, 瑾玄 `zh-CN-XiaoyiNeural +5%` (giống talk02/tranhluan) → `public/audio/l*.mp3` + `src/durations.json`.
5. `python make_frames.py` (public/frames/, gitignored) → `npx remotion render src/index.ts Clip video/talk03-tranhluan.mp4`.

Bố cục `src/Clip.tsx`: phủ kín 9:16, phụ đề chữ trắng viền nâu ở trên, KHÔNG thẻ tên/thẻ từ; khung 0 có nhân vật + tiêu đề "活人图书馆？"; nhạc nền chạy suốt kể cả đoạn kết follow.
