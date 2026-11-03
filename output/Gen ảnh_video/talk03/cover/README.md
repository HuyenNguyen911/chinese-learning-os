# talk03/cover — Ảnh bìa bài đăng tập 03 《活人图书馆》

Thành phẩm: `talk03-cover.png` (1080×1440, 3:4, dùng chung mọi kênh). User duyệt 2026-11-03.

- Cảnh vẽ nguyên bằng model ảnh (`gen_image.py --size 1536x1024`) → chọn `gen/D2.png`
  (phòng đọc tối giản, 3 bàn, 越黄 ngồi một mình chờ được "mượn"; 瑾玄 cầm thẻ mượn).
  Đã sửa bằng Pillow → `scene.png`: xoá vòng đỏ thừa ở tay phải 越黄, thêm vòng đỏ cạnh đồng hồ tay trái, mặt đồng hồ trắng → đen.
- Các bản không chọn trong `gen/`: A (giống hẹn hò), B (chưa ra ý thư viện), C/C2 (kệ sách người), D (người nghe là trẻ con), D3 (越黄 thiếu thẻ sách).
- Khung chữ + hiệu ứng: `cover.html` (nhãn 每周一个话题 · 03, tiêu đề 104px, tia sáng mờ dần, ✨, bong bóng 来借我吧～).
  Không dùng Remotion (tập này chưa có project clip). Render lại:

```bash
cd "output/Gen ảnh_video/talk03/cover"
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1080,1440 \
  --screenshot="$(cygpath -w "$PWD")\\talk03-cover.png" "file:///$(cygpath -m "$PWD")/cover.html"
```
