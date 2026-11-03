# talk02/hskk-c5 — Video HSKK 高级 · Chủ đề 2 《在家上学》 · Câu 5

Khuôn `template/hskk-answer`. Nguồn: `onluyen/bai-mau-cau5-6.md` (Bài 2, Câu 5).

## Tiến độ (2026-11-03)
- [x] Cổng nội dung: 38 dòng phụ đề + dịch VI/EN (`src/lines.json`), mindmap + 6 cụm (`src/Frames.tsx`), user duyệt
- [x] Giọng Yunxia +8% +4Hz: `public/audio/read.wav` (84s) + `src/timing.json`; intro (`tts_intro.py`)
- [x] 24 khung tĩnh vẽ nguyên cảnh bằng model ảnh (`gen_scenes.py` + `src/scenes.json`) → `assets/keyframes/`, user duyệt
- [x] 24 clip muse-video (`gen_motion.py` + `src/motion.json`) → `assets/motion/` (gốc) + `public/motion/` (mã hoá lại 30fps)
- [x] Ghép `src/Full.tsx`: K4 = ô ghép 5 sở thích (K4a…K4e); cụm tách (发挥…潜力) tô đỏ từng mảnh
- [x] Render bản VI → user góp ý 8 điểm (2026-11-03) → sửa: khung 0 không fade-in; mindmap 越黄 đồng phục (`yh_uni_wave.png`); vẽ lại + gen lại K1 (đích đến rõ), K3 (bút tay phải), K5 (越黄 nhỏ), K12 (tập trên bàn), K19 (ôm nhau + like), K21 (mũ trên đầu) → user duyệt
- [x] Render bản EN
- [x] Commit video/

## Làm tiếp ở máy khác
```bash
cd "output/Gen ảnh_video/talk02/hskk-c5"
npm ci
bash chunk_render.sh FullVI video/talk02-hskk-c5-vi.mp4   # render chia đoạn (chống "No frame found"); chạy lại = làm tiếp
bash chunk_render.sh FullEN video/talk02-hskk-c5-en.mp4
```

## Ghi chú kỹ thuật
- Clip lỗi phải cắt dùng phần đầu (`USE` trong Full.tsx): K2a 5s (sau 6s tóc đổi màu), K8 7,5s (clip gốc 7,6s), K6 4,5s (sau 5s mọc thêm bạn tóc vàng).
- Clip cuối (K21) chạy tới hết đoạn kết → tốc độ tính trên ANS+2,5s, nếu không Remotion báo "No frame found at position".
- Ảnh 越黄: đồng hồ NHỎ dây mảnh, tay trái; cùng cỡ với bạn; chỉ 1 越黄/hình (đã ghi trong `src/scenes.json` → `yh`, `friends`).
- Đồ ở nhà: hoodie xám nhạt túi + dây rút đỏ, jogger navy. Đồng phục: sơ mi trắng, cà vạt đỏ (bạn: cà vạt navy).
- Cảnh mindmap dùng `public/img/yh_uni_wave.png` (đồng phục, tách nền bằng `cutout_mint.py`).
- K5 bản mới chỉ 7,08s → `USE.K5 = 6.3` (tính cả 0,3s chuyển cảnh mỗi đầu, không được vượt độ dài clip).
- 2026-11-03: `public/motion/K8.mp4` bị commit HỎNG (786 KB, "moov atom not found" — commit lúc đang mã hoá dở) → render đứng ở đoạn 3 (khung 2247). Đã gen lại K8 bằng muse-video từ `K8.png` + mã hoá lại 30fps. Trước khi commit clip: `ffprobe` từng file.
- Máy nhà: venv skill hỏng numpy → `voice_edge.py` bản project đã bỏ numpy.
