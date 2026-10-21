# Lỗi kỹ thuật đã gặp (Windows, 2026-10-21)

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| `remotion still/render` lỗi `spawn EFTYPE` | Chromium headless Remotion tự tải về không chạy được | `remotion.config.ts` trong template tự chọn Chrome/Edge có sẵn (`Config.setBrowserExecutable`) |
| Bundling lỗi `typescript.sys` undefined | TypeScript bản mới nhất (7.x) không tương thích esbuild-loader của Remotion 4.0.x | Ghim `typescript@5.6.3` (đã có trong package-lock của template) |
| `tsc` báo `moduleResolution=node10 removed` | tsconfig cũ | Dùng `"moduleResolution": "bundler"` |
| Python in tiếng Việt lỗi `UnicodeEncodeError cp1252` | Console Windows | Đầu mọi script: `sys.stdout.reconfigure(encoding="utf-8")` |
| Gọi `api.lucylab.io` từ Python → 403 (curl thì được) | Cloudflare chặn User-Agent `Python-urllib` | Luôn gửi header `User-Agent: curl/8.4.0` |
| LucyLab: "You already have an export in progress" | Tài khoản chỉ 1 job cùng lúc; job kẹt chặn job sau | TTS tuần tự; job lỗi tự `failed` sau ~1–2 phút. Không bắn song song |
| LucyLab job `failed: No audio files to merge` | Giọng chỉ hỗ trợ tiếng Việt (vd "Huyền Bây Bê") nhận chữ Hán | Đổi giọng; kiểm `--list` |
| edge-tts 7.2.8 → 403 | Microsoft đổi token; cần bản mới hơn | User đã từ chối nâng cấp pip toàn cục → không dùng edge-tts |
| API ảnh bỏ qua `size: 2048x2048` | Model trả tối đa 1024×1024 | Không phóng ảnh nhỏ lên quá ~1.5× (mờ) — dùng ảnh riêng từng bộ phận |
| Video có tiếng nhưng user không nghe | Trình xem mp4 trong VS Code không phát tiếng | Mở bằng app Windows: `cmd.exe //c start "" file.mp4` |
| Bash heredoc dài chứa `'` lỗi "unexpected EOF" | Quoting trong Git Bash | Ghi file bằng tool Write thay vì heredoc |
| Tách nền để lại khung nhạt hình chữ nhật (额头) | `cutout.py` flood-fill pixel gần trắng từ viền; viền nhạt của ảnh không đủ trắng | Sinh lại ảnh, hoặc hạ ngưỡng `TH` trong cutout.py |
| `git mv` báo "not under version control" | Thư mục vừa `mv` thường, chưa `git add` | Dùng `mv` rồi `git add -A <path>` |
