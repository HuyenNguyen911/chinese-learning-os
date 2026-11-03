# talk02-hskk-c5-zaijia — Video HSKK 高级 · Chủ đề 2 《在家上学》 · Câu 5

Khuôn `template/hskk-answer`. Nguồn: `onluyen/bai-mau-cau5-6.md` (Bài 2, Câu 5).

## Tiến độ (2026-11-03)
- [x] Cổng nội dung: 38 dòng phụ đề + dịch VI/EN (`src/lines.json`), mindmap + 6 cụm (`src/Frames.tsx`), user duyệt
- [x] Giọng Yunxia +8% +4Hz: `public/audio/read.wav` (84s) + `src/timing.json`; intro (`tts_intro.py`)
- [x] 24 khung tĩnh vẽ nguyên cảnh bằng model ảnh (`gen_scenes.py` + `src/scenes.json`) → `assets/keyframes/`, user duyệt
- [x] 24 clip muse-video (`gen_motion.py` + `src/motion.json`) → `assets/motion/` (gốc) + `public/motion/` (mã hoá lại 30fps)
- [x] Ghép `src/Full.tsx`: K4 = ô ghép 5 sở thích (K4a…K4e); cụm tách (发挥…潜力) tô đỏ từng mảnh
- [ ] Render bản VI → user duyệt (máy nhà: render 4 luồng thẳng bị lỗi; nhường máy cho render câu 6 chủ đề 1 đang chạy song song — KHÔNG chạy 2 render cùng lúc)
- [ ] Render bản EN
- [ ] Commit video/

## Làm tiếp ở máy khác
```bash
cd "output/Gen ảnh_video/talk02-hskk-c5-zaijia"
npm ci
bash chunk_render.sh FullVI video/talk02-hskk-c5-vi.mp4   # render chia đoạn (chống "No frame found"); chạy lại = làm tiếp
bash chunk_render.sh FullEN video/talk02-hskk-c5-en.mp4
```

## Ghi chú kỹ thuật
- Clip lỗi phải cắt dùng phần đầu (`USE` trong Full.tsx): K2a 5s (sau 6s tóc đổi màu), K8 7,5s (clip gốc 7,6s), K6 4,5s (sau 5s mọc thêm bạn tóc vàng).
- Clip cuối (K21) chạy tới hết đoạn kết → tốc độ tính trên ANS+2,5s, nếu không Remotion báo "No frame found at position".
- Ảnh 越黄: đồng hồ NHỎ dây mảnh, tay trái; cùng cỡ với bạn; chỉ 1 越黄/hình (đã ghi trong `src/scenes.json` → `yh`, `friends`).
- Đồ ở nhà: hoodie xám nhạt túi + dây rút đỏ, jogger navy. Đồng phục: sơ mi trắng, cà vạt đỏ (bạn: cà vạt navy).
- Cảnh mindmap vẫn dùng `public/img/yh_w_wave.png` (áo len đỏ của chủ đề 1) — muốn đổi sang đồng phục cần tách nền (cần numpy; venv skill máy nhà thiếu numpy).
- Máy nhà: venv skill hỏng numpy → `voice_edge.py` bản project đã bỏ numpy.
