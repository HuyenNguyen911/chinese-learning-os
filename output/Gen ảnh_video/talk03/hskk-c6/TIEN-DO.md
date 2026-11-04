# talk03/hskk-c6 — TIẾN ĐỘ (dừng 2026-11-04 chiều, chưa render)

Video HSKK 高级 · Chủ đề 3 《活人图书馆》 · câu 6「如果你是活人图书馆的一本"书"，你会是一本什么样的"书"？」 · nhân vật 瑾玄.

## ĐÃ XONG (user duyệt)
- **Nội dung:** `src/data.json` (nguyên văn bài mẫu `onluyen/bai-mau-cau5-6.md` Bài 3 câu 6), `src/lines.json` = 31 dòng + dịch **VI đã duyệt (bản dịch lại kiểu nói)**. `en` còn để trống → điền trước khi render bản EN.
- **Giọng:** `public/audio/read.wav` + `src/timing.json` (Xiaoxiao +0%, 67.7s), `intro_*.wav` + `src/intro.json` (câu hỏi, 现在开始, 8 cụm).
- **8 cụm đáng học** (`PH` trong `src/Frames.tsx`), hiện CHUNG 1 màn: 犯错, 不只是…, 只有…才…, 哪怕…也…, 一帆风顺, 迷茫, 重要的不是…而是…, 追梦.
- **17 khung tĩnh** (`assets/keyframes/`, user duyệt từng khung): K1 K2 K3b K4 K5 K6 K6b K7a K7b K8 K8b K9 K10 K11 K12 K13 K14.
  - K5 = K6 dùng CHUNG 1 ảnh lớp (`out/gen/K5x.png`; K6 = K5x + giọt mồ hôi vẽ bằng PIL) — user đòi nền lớp đồng nhất, bàn cách xa bảng, học sinh quay về bảng.
  - Bảng lớp có chữ thật 第三课 我的爱好 / 我喜欢看书。/ 你喜欢什么？; quầy có biển 老王包子 (AI vẽ đúng chữ).
- **17 đoạn muse-video** `assets/motion/K*.mp4` — đã soát 1,25–2 khung/giây, đều dùng được:
  - K5: từ ~4s tự nhảy cận cảnh → `plan.json use.K5 = 3.8`.
  - K6: tự đẩy cận vào mặt lo lắng (giữ, hợp cảm xúc). Bản cô giáo đi ra tiền cảnh đã bỏ (`out/old_motion/`).
  - K10 chỉ 4.2s (giãn 0.8×). K13 ~5s cắt sang cận cảnh người đọc rực sáng (giữ).
- **Dựng:** `src/Full.tsx` viết mới (dựa câu 5), `src/plan.json` = lịch clip dùng CHUNG với `make_frames.py`:
  - Khoảng lặng 1.6s trước dòng 19 (`gapLine`): giọng đọc tách 2 đoạn, K8b người đọc nhép miệng hỏi (không giọng, không phụ đề).
  - Hồi tưởng (`mem`: K4–K7b, K9, K10) phủ sepia + viền tối, loé trắng lúc vào/ra.
  - Dòng 20 có 2 cụm (追梦 + 一帆风顺) → 2 thẻ cạnh nhau.

## CÒN LẠI (làm tiếp theo thứ tự)
1. `python make_frames.py` (lệnh cuối bị dừng giữa chừng — chạy lại từ đầu, nó tự xoá `public/frames/<id>` cũ).
2. Soát khung tĩnh: `npx remotion still src/index.ts FullVI out/v<N>.png --frame=<N>` (S1 câu hỏi, S2 mindmap, S3 8 cụm có vừa 1 màn không, S4 vài cảnh + chỗ khoảng lặng K8b, thẻ đôi dòng 20).
   `Full.tsx` CHƯA từng render thử → có thể có lỗi cú pháp/TS.
3. Render VI: `bash chunk_render.sh FullVI video/talk03-hskk-c6-vi.mp4` → mở cho user (`cmd.exe //c start ""`) → chờ chốt.
4. Sau khi user chốt VI: dịch EN vào `lines.json.en` → `bash chunk_render.sh FullEN video/talk03-hskk-c6-en.mp4`.
5. Commit vào `main` (không kèm `out/`, `node_modules/`, `public/frames/`).

## Lưu ý
- Peeker ở màn câu hỏi dùng `img/jx3_smile.png` (đồ talk02) — chưa có tấm 瑾玄 đồ chủ đề 3 tách nền.
- `src/scenes.json` = prompt từng khung; `src/motion.json` = prompt muse (ai mở miệng).
