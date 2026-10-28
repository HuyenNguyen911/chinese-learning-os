---
name: genimagevideo
description: Sinh ảnh minh hoạ (AI, tách nền) + giọng đọc + video dạy từ vựng tiếng Trung dạng "poster highlight" (9:16, Remotion) — đọc từ nào thì chỗ đó trên nhân vật được khoanh đỏ. Output ở output/Gen ảnh_video/<slug>/. Use when user nói "gen ảnh", "tạo ảnh minh hoạ", "tạo video từ vựng", "làm video TikTok dạy từ", "video bộ phận cơ thể/màu sắc/...", "remotion", "/genimagevideo", hoặc muốn sinh giọng đọc (TTS ViVibe/ElevenLabs) cho video.
---

# Gen ảnh & video dạy từ vựng

Dựng video ngắn dạy từ vựng theo kiểu **poster**: tiêu đề, một nhân vật ở giữa, các thẻ từ
(ảnh + 汉字 + pinyin) xung quanh. Giọng đọc lần lượt từng từ; **từ đang đọc → chỗ tương ứng
trên nhân vật được khoanh đỏ**, chữ của thẻ ngả đỏ, các thẻ khác mờ nhẹ.

Ví dụ hoàn chỉnh đã được user duyệt: `output/Gen ảnh_video/bo-phan-co-the/` (14 từ bộ phận cơ thể).

## Cấu trúc

```
.claude/skills/genimagevideo/
  SKILL.md
  reference/design-rules.md     # quy tắc thiết kế — rút từ 5 vòng góp ý của user. ĐỌC TRƯỚC KHI DỰNG.
  reference/gotchas.md          # lỗi kỹ thuật đã gặp + cách xử lý
  scripts/imagegen/gen_image.py # gọi API sinh ảnh (OpenAI-compatible, 9router)
  scripts/imagegen/.env         # KEY — gitignored, không bao giờ in/commit
  scripts/voicegen/tts.py       # TTS: --provider lucylab (ViVibe) | elevenlabs
  scripts/new_project.py        # tạo project mới từ template
  template/poster-highlight/    # code Remotion + script sinh ảnh/giọng (copy vào mỗi project)
  template/story-clip/          # clip kể chuyện 9:16 nhiều cảnh (Talk series) — xem mục "Clip kể chuyện"
output/Gen ảnh_video/<slug>/    # mỗi video 1 project tự chứa; thành phẩm ở video/<slug>.mp4
```

Biến trong `scripts/imagegen/.env`: `IMAGEGEN_URL`, `IMAGEGEN_KEY`, `IMAGEGEN_MODEL`,
`TTS_PROVIDER`, `VIVIBE_API_KEY`, `LUCYLAB_VOICE_ID`, `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`,
`ELEVENLABS_MODEL_ID`. Thiếu file `.env` → hỏi user key, **không** đoán endpoint để gửi key thử.

Cần sẵn trên máy: Python 3 (Pillow, numpy), Node ≥ 18, ffmpeg/ffprobe, Chrome hoặc Edge.

Tuỳ chọn — rembg (tách nền bằng AI) trong venv RIÊNG của skill, không đụng Python chung
(user không muốn nâng cấp pip toàn cục):
```
python -m venv .claude/skills/genimagevideo/.venv
.claude/skills/genimagevideo/.venv/Scripts/python.exe -m pip install "rembg[cpu]"
```
Chỉ dùng khi tách nền theo màu thất bại — xem gotchas.md (rembg làm hỏng ảnh bộ phận rời).

## Quy trình (có cổng duyệt — không gộp bước)

### Bước 0 — Chốt yêu cầu
Chủ đề, danh sách từ, đối tượng (HSK1 = học sinh tiểu học → hình dễ thương, không thuật ngữ).
Thiếu thông tin → hỏi **1 câu**. Đọc `reference/design-rules.md`.

### Bước 1 — CỔNG 1: duyệt nội dung (chưa sinh gì)
Trình user bảng: `id | 汉字 | pinyin | nghĩa | ảnh sẽ vẽ gì | chỗ khoanh trên nhân vật`
+ mô tả nhân vật + bố cục (bao nhiêu thẻ hàng trên / hai bên / hàng dưới). Pinyin tự sinh
(pypinyin) rồi soát thanh nhẹ (头发 tóu fa, 眼睛 yǎn jing). **Chờ OK** rồi mới sang bước 2.

### Bước 2 — Tạo project
```
python .claude/skills/genimagevideo/scripts/new_project.py <slug>
```
Sửa `words.json` (id, han, pinyin, vi, prompt) và `layout.json` (title, style, characterPrompt,
slots: x/y/iw/ih + `hl` = các elip `[cx, cy, rx, ry]` theo pixel ảnh nhân vật 640×628).

### Bước 3 — CỔNG 2: ảnh
```
python gen_assets.py          # chỉ sinh ảnh chưa có;  python gen_assets.py lian etou  = sinh lại id đó
python cutout.py              # tách nền -> assets/*.png + public/img + assets/contact.jpg
```
Ảnh được sinh trên **nền xanh lá #00FF00** (đã ghi trong `layout.json → style`) rồi `cutout.py`
tách đúng màu đó (chroma key + khử viền xanh) — chính xác, không đoán. Nếu chủ thể CÓ màu xanh lá
(vd chủ đề màu sắc 绿色, lá cây) → đổi riêng prompt ảnh đó sang nền trắng; cutout tự nhận ra và
dùng flood-fill.
**Read `assets/contact.jpg`** và tự soát trước khi đưa user: ảnh trùng nhau? thừa chi tiết (tóc mọc
trên mũi)? có chữ? phong cách lệch? Sinh lại đúng id lỗi. Rồi cho user xem contact sheet, chờ OK.

### Bước 4 — Bố cục + điểm khoanh
1. `python lint_layout.py` phải **OK** (không chồng, không tràn, cách ≥ 20px). Fail → sửa layout.json, không bỏ qua.
2. Read ảnh `public/img/character.png` để đặt toạ độ `hl` cho từng từ (bộ phận đôi → 2 elip: tai, tay, chân).
3. `npm run still` (hoặc `npx remotion still src/index.ts Poster out/x.png --frame=N`) ở 3–4 khung
   rơi giữa các từ khác nhau → **Read từng ảnh**, kiểm vòng đỏ nằm đúng bộ phận.

### Bước 5 — Giọng đọc
Ưu tiên theo thứ tự (hỏi user nếu chưa rõ):
1. **User tự thu âm** — đúng thanh điệu nhất. Bỏ file `<id>.mp3|m4a|wav...` vào `public/audio/`.
2. TTS ViVibe/LucyLab (`TTS_PROVIDER=lucylab`) hoặc ElevenLabs.
```
python gen_voice.py            # có file thu âm -> đổi wav + cắt lặng; không có -> TTS
python gen_voice.py --no-tts   # chỉ dùng thu âm, báo id còn thiếu
```
Sinh ra `src/durations.json`; thời lượng mỗi từ = audio + 1.1s (tối thiểu 1.8s).

### Bước 6 — Render + kiểm tra
```
npm run render                 # -> video/<slug>.mp4
```
Kiểm bằng máy (tôi không xem/nghe được video): `ffprobe` có cả stream video + audio;
`ffmpeg -af silencedetect=n=-35dB:d=0.25` → thời điểm có tiếng phải khớp lịch
`(INTRO + START[i] + 8)/30` giây (lệch ≤ ~0.1s). Ghi rõ với user phần nào **chưa kiểm được**
(độ mượt chuyển động, chất lượng giọng).

### Bước 7 — Bàn giao
Mở video cho user bằng ứng dụng Windows: `cmd.exe //c start "" "video/<slug>.mp4"`
(**trình xem trong VS Code phát hình nhưng không ra tiếng** — đã xác nhận với user).
Commit vào `main` theo luật Git Hygiene (CLAUDE.md §5.5); không push nếu user chưa bảo.

## Clip kể chuyện (khuôn `template/story-clip/`, dùng cho Talk series)
Ví dụ đã chạy: `output/Gen ảnh_video/talk01-contagious/`. Cảnh khai báo trong `src/story.json`; ĐỌC `reference/design-rules.md` §9 trước khi dựng.
- **Cảnh:** `id`, `text` (phụ đề, ở đầu khung), `actors[]`, tuỳ chọn `bubble`, `cards` (`han`/`py`/`en` — nghĩa tiếng Anh), `glow`, `door`.
- **Giọng:** 1 file/câu `public/audio/<voice>.m4a|wav`; nhiều cảnh dùng chung 1 câu bằng `"voice": "c2"` (thời lượng chia theo số chữ Hán). `python make_durations.py` → `durations.json` + `envelope.json`. Chưa có giọng: chạy im lặng, mỗi chữ ~0.24s.
- **Cảnh không thoại:** `"silent": true, "sec": 3.2, "text": ""` (không cần file giọng).
- **Actor:** `img,x,feet,h,z`; `from`/`fromSec`/`walk` (bước vào), `enter:{x,feet,h,sec}` (thu/phóng từ vị trí cảnh trước), `swap:{img,at}` (đổi tư thế), `bob` (`voice`/`laugh`/`none`), `still` (ảnh đứng yên), `lean` (nghiêng người, độ).
- **Khuôn mặt sống:** bảng `FACE` trong `Story.tsx` (toạ độ **dò từ pixel**, xem gotchas) cho `mouth`/`eyes`/`chat`; actor bật `talk` (nhép theo giọng/chữ), `mime` (nhép không thoại), `chat` (2 người nói xen kẽ trên cùng ảnh), `neutral` (miệng khép, chưa cười). Chớp mắt tự động nếu ảnh có `eyes`.
- Render: `npm install` → `npm run render` → `video/<slug>.mp4`. Kiểm tra bằng `npx remotion still` + ảnh phóng to vùng mặt.

## Ảnh bìa bài đăng (Talk series)
Ví dụ: `output/Gen ảnh_video/talk01-contagious/src/Cover.tsx` → `cover/talk01-cover.png`.
- **1 khung 3:4 (1080×1440) dùng chung mọi nền tảng** (RedNote/IG/FB/HelloTalk/TikTok ảnh) — user chọn, đỡ phải nhớ bản nào đăng đâu; bìa video TikTok lấy từ chính clip.
- **Ghép từ ảnh nhân vật đã duyệt** trong `public/img/` của project clip, KHÔNG gen lại (gen lại → nhân vật xê dịch, lệch clip; không tốn lượt gen).
- Thêm composition `Cover` (durationInFrames 1) vào `Root.tsx`, render: `npx remotion still src/index.ts Cover cover/<slug>-cover.png --frame=0` → Read ảnh tự soát rồi mở cho user.
- Tiêu đề font thật ~104px (132px bị chê to); tiêu đề + mặt nhân vật dồn vùng giữa vì HelloTalk/FB cắt ảnh xem trước gần vuông.

## Nhân vật chibi (Talk series + video)
- Ảnh chụp thật làm mẫu: `raw/nhan-vat/<tên>/` — **gitignored**, không lên GitHub. User tự bỏ ảnh vào; nhân vật đã có thì dùng lại, không xin lại ảnh.
- Bản chibi + hồ sơ: `output/Gen ảnh_video/nhan-vat/<tên>/avatar.png` + `nhan-vat/README.md` (dấu hiệu nhận diện từng người — ĐỌC trước khi vẽ).
- Phong cách chung: chibi đầu to, nét mảnh, tô phẳng pastel, nền mint trơn (để tách nền), không chữ/logo.
- **Máy chủ 9router KHÔNG sửa được ảnh theo ảnh mẫu và KHÔNG có model video** (xem gotchas) → mỗi lần vẽ lại, nhân vật xê dịch.
  Chỉnh chi tiết nhỏ (thêm đồng hồ, đổi tay) → **lật ảnh / vẽ đè bằng Pillow** trên tấm đã duyệt, không vẽ lại cả nhân vật.
- Người thật khác (bạn bè, bố mẹ): chỉ vẽ theo ảnh khi user tự gửi; nhắc user hỏi ý người đó trước khi đăng công khai.

## Không làm
- Không để AI vẽ chữ Hán/pinyin trong ảnh — chữ do Remotion vẽ bằng font thật.
- Không gửi key tới endpoint tự đoán; không in key ra terminal; không commit `.env`.
- Không thêm hiệu ứng thứ hai "cho sinh động" (xem design-rules.md §1).
- Không render toàn bộ khi chưa qua lint + still check.
