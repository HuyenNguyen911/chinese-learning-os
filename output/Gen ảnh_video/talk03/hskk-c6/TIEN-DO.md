# talk03/hskk-c6 — XONG (2026-11-05)

Video HSKK 高级 · Chủ đề 3 《活人图书馆》 · câu 6 · nhân vật 瑾玄. User đã chốt cả 2 bản:
- `video/talk03-hskk-c6-vi.mp4`, `video/talk03-hskk-c6-en.mp4` (~2:03).

## Ghi chú cho lần sửa sau
- Dịch VI/EN trong `src/lines.json` đã rà lại từng dòng (2026-11-05): giữ 怎样 (dòng 5-8), 潜力, 停下来 = dừng lại, 一帆风顺 = thuận buồm xuôi gió / plain sailing (khớp thẻ cụm).
- **K10, K12 là chuyển động GIẢ** (`fake_motion.py`) vì muse-video chết (9router báo `muse.ai session rejected (HTTP 401); cookies are no longer valid`):
  - K10: khung `assets/keyframes/K10.png` (dù chĩa ra trước chắn gió) + đẩy máy + nhún bước + mưa xiên vẽ bằng code + nắng sáng dần.
  - K12: đoạn muse cũ (`out/old_motion/K12_v1.mp4`, đang nói) tới dòng 28 → cắt sang cận cảnh tay đặt lên ngực (`out/gen/K12h1.png`).
  - Muse sống lại muốn có chuyển động thật: `python gen_motion.py K10 K12` (prompt mới đã có trong `src/motion.json`) → `python make_frames.py` → `rm -rf out/ch-FullVI out/ch-FullEN` → `bash chunk_render.sh FullVI …` + `FullEN …`.
- `chunk_render.sh` GIỮ đoạn đã render → sửa nội dung xong PHẢI xoá `out/ch-<Comp>/` trước khi render lại.
