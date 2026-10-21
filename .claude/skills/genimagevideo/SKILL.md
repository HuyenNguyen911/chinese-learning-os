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
output/Gen ảnh_video/<slug>/    # mỗi video 1 project tự chứa; thành phẩm ở video/<slug>.mp4
```

Biến trong `scripts/imagegen/.env`: `IMAGEGEN_URL`, `IMAGEGEN_KEY`, `IMAGEGEN_MODEL`,
`TTS_PROVIDER`, `VIVIBE_API_KEY`, `LUCYLAB_VOICE_ID`, `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`,
`ELEVENLABS_MODEL_ID`. Thiếu file `.env` → hỏi user key, **không** đoán endpoint để gửi key thử.

Cần sẵn trên máy: Python 3 (Pillow, numpy), Node ≥ 18, ffmpeg/ffprobe, Chrome hoặc Edge.

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

## Không làm
- Không để AI vẽ chữ Hán/pinyin trong ảnh — chữ do Remotion vẽ bằng font thật.
- Không gửi key tới endpoint tự đoán; không in key ra terminal; không commit `.env`.
- Không thêm hiệu ứng thứ hai "cho sinh động" (xem design-rules.md §1).
- Không render toàn bộ khi chưa qua lint + still check.
