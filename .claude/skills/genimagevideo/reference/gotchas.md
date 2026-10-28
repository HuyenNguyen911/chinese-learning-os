# Lỗi kỹ thuật đã gặp (Windows, 2026-10-21)

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| `remotion still/render` lỗi `spawn EFTYPE` | Chromium headless Remotion tự tải về không chạy được | `remotion.config.ts` trong template tự chọn Chrome/Edge có sẵn (`Config.setBrowserExecutable`) |
| Bundling lỗi `typescript.sys` undefined | TypeScript bản mới nhất (7.x) không tương thích esbuild-loader của Remotion 4.0.x | Ghim `typescript@5.6.3` (đã có trong package-lock của template) |
| `tsc` báo `moduleResolution=node10 removed` | tsconfig cũ | Dùng `"moduleResolution": "bundler"` |
| `gen_image.py -n 2` chỉ ra 1 ảnh (2026-10-22) | Model qua 9router bỏ qua `n` | Cần nhiều phương án → gọi nhiều lần, mỗi lần 1 prompt |
| Xin `--size 1536x1024` nhận về 1264×848 (2026-10-22) | Model chỉ có vài khung cố định (ngang ≈ 3:2) | Nhận 3:2 rồi tự cắt bằng Pillow (vd 5:4 bìa RedNote); chủ thể lệch → cắt lệch theo chủ thể |
| Python in tiếng Việt lỗi `UnicodeEncodeError cp1252` | Console Windows | Đầu mọi script: `sys.stdout.reconfigure(encoding="utf-8")` |
| Gọi `api.lucylab.io` từ Python → 403 (curl thì được) | Cloudflare chặn User-Agent `Python-urllib` | Luôn gửi header `User-Agent: curl/8.4.0` |
| LucyLab: "You already have an export in progress" | Tài khoản chỉ 1 job cùng lúc; job kẹt chặn job sau | TTS tuần tự; job lỗi tự `failed` sau ~1–2 phút. Không bắn song song |
| LucyLab job `failed: No audio files to merge` | Giọng chỉ hỗ trợ tiếng Việt (vd "Huyền Bây Bê") nhận chữ Hán | Đổi giọng; kiểm `--list` |
| edge-tts 7.2.8 → 403 | Microsoft đổi token; cần bản mới hơn | User đã từ chối nâng cấp pip toàn cục → không dùng edge-tts |
| API ảnh bỏ qua `size: 2048x2048` | Model trả tối đa 1024×1024 | Không phóng ảnh nhỏ lên quá ~1.5× (mờ) — dùng ảnh riêng từng bộ phận |
| Video có tiếng nhưng user không nghe | Trình xem mp4 trong VS Code không phát tiếng | Mở bằng app Windows: `cmd.exe //c start "" file.mp4` |
| Bash heredoc dài chứa `'` lỗi "unexpected EOF" | Quoting trong Git Bash | Ghi file bằng tool Write thay vì heredoc |
| Tách nền để lại khung nhạt hình chữ nhật (额头) | Flood-fill pixel gần trắng từ viền; ảnh nền trắng có viền nhạt không đủ trắng | **Sinh ảnh trên nền xanh #00FF00** → cutout tự dùng chroma key. Đã sửa được 额头 (viền tóc bo tròn tự nhiên) |
| rembg làm hỏng ảnh bộ phận rời (thử 2026-10-21, 8 ảnh) | Model AI đoán "chủ thể" — với mảnh rời (trán, đôi mắt, mớ tóc) nó đoán sai | `isnet-anime`: mất cả đôi mắt, gần hết trán, nửa mớ tóc. `birefnet-general-lite`: xoá da trán, cắt lệch miệng, ~50s/ảnh CPU. → không dùng mặc định |
| Model mặc định của rembg (`bria-rmbg`) | ~1GB, cần license thương mại | Luôn chỉ định `--model` khác nếu dùng rembg |
| `git mv` báo "not under version control" | Thư mục vừa `mv` thường, chưa `git add` | Dùng `mv` rồi `git add -A <path>` |
| `/v1/images/edits` trả HTTP 500; gửi `image` kèm `/images/generations` thì bị bỏ qua, ra nhân vật khác hẳn (2026-10-23) | 9router không hỗ trợ sửa ảnh theo ảnh mẫu | Chỉnh chi tiết bằng lật ảnh / vẽ đè Pillow; muốn giữ nhân vật thì dùng lại đúng tấm đã duyệt |
| `/v1/models` không có model video nào (2026-10-23; danh sách cũng không đầy đủ — thiếu cả model ảnh đang dùng) | Router chỉ có model chat + ảnh ẩn | Chuyển động làm bằng Remotion (lật tấm, nhép miệng theo âm lượng), không đoán tên model video |
| `OSError: [Errno 22] Invalid argument` khi lưu ảnh (2026-10-23) | File đích đang mở trong trình xem ảnh Windows (bị khoá) | Lưu sang tên mới, đổi tên sau khi user đóng trình xem |
| Nhép miệng/chớp mắt bằng cách vẽ đè: viền miệng gốc lòi ra, vùng nền da lệch (2026-10-28) | Toạ độ miệng/mắt ước lượng bằng mắt từ ảnh đã thu nhỏ lệch 5–6px; vùng cắt sát quá cắt cụt mép miệng | **Dò từ pixel file ảnh gốc**: bản đồ ký tự theo màu (đỏ hồng `r>200,g<125` = lòng miệng, nâu `r<150,g<100` = viền) → bbox, tâm, nửa trục; lấy màu da = **trung vị** các điểm trên vòng quanh bộ phận (k≈1.5–2×). Elip cắt lớn hơn bbox ~10–20%. Kiểm bằng ảnh phóng to 3–6× ở nhiều nhịp mở/khép |
| Cắt tay/đầu từ ảnh phẳng rồi xoay → hiện 2 bàn tay (bóng đôi), tách đôi ảnh 2 người để lắc riêng → ghế bị "chia đôi lung lay" (2026-10-28) | Ảnh phẳng không có lớp riêng cho từng chi; phần ảnh gốc dưới chi bị xoay vẫn còn | Không làm. Cử động tay/đầu thật = user cung cấp tấm tư thế (tay giơ/hạ…) cùng khung → luân phiên bằng `swap`. Tạm thời chỉ dùng: thở/nhún nhẹ, chớp mắt, nhép miệng, nghiêng người (`lean`) |

