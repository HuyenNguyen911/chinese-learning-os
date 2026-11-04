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
  template/hskk-answer/         # video HSKK 回答问题 (câu 5/6 mỗi chủ đề; phân cảnh minh hoạ muse-video) — xem mục "Video HSKK 回答问题"
  template/read-along/          # video 朗读 9:16 (bài đọc chạy theo giọng + thẻ từ EN/VI) — xem mục "Video 朗读"
  .venv/                        # Python riêng của skill (edge-tts 7.3.1; rembg tuỳ chọn) — KHÔNG dùng Python chung cho edge-tts
output/Gen ảnh_video/<slug>/    # mỗi video 1 project tự chứa; thành phẩm ở video/<slug>.mp4
output/Gen ảnh_video/talkNN/<loại>/  # video Talk series gom theo chủ đề: talk01/{contagious,langdu,hskk-c5,hskk-c6}, talk02/{langdu,tranhluan,hskk-c5}…
                                     #   tạo mới: new_project.py talkNN/<loại> (vd talk03/langdu); <loại> = langdu | tranhluan | hskk-c5 | hskk-c6 | <tên clip kể chuyện>
```

Biến trong `scripts/imagegen/.env`: `IMAGEGEN_URL` (`…/v1/images/generations`), `IMAGEGEN_KEY`, `IMAGEGEN_MODEL`
(**`ag/gemini-3.1-flash-image`** — thiếu tiền tố `ag/` là rơi vào gói Gemini free hết lượt, lỗi 429), `VIDEOGEN_URL`
(`…/v1/videos/generations`), `VIDEOGEN_MODEL` (`muse-web/muse-video`, dùng chung `IMAGEGEN_KEY`),
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
Ví dụ đã chạy: `output/Gen ảnh_video/talk01/contagious/`. Cảnh khai báo trong `src/story.json`; ĐỌC `reference/design-rules.md` §9 trước khi dựng.
- **Cảnh:** `id`, `text` (phụ đề, ở đầu khung), `actors[]`, tuỳ chọn `bubble`, `cards` (`han`/`py`/`en` — nghĩa tiếng Anh), `glow`, `door`.
- **Giọng:** 1 file/câu `public/audio/<voice>.m4a|wav`; nhiều cảnh dùng chung 1 câu bằng `"voice": "c2"` (thời lượng chia theo số chữ Hán). `python make_durations.py` → `durations.json` + `envelope.json`. Chưa có giọng: chạy im lặng, mỗi chữ ~0.24s.
- **Cảnh không thoại:** `"silent": true, "sec": 3.2, "text": ""` (không cần file giọng).
- **Actor:** `img,x,feet,h,z`; `from`/`fromSec`/`walk` (bước vào), `enter:{x,feet,h,sec}` (thu/phóng từ vị trí cảnh trước), `swap:{img,at}` (đổi tư thế), `bob` (`voice`/`laugh`/`none`), `still` (ảnh đứng yên), `lean` (nghiêng người, độ).
- **Khuôn mặt sống:** bảng `FACE` trong `Story.tsx` (toạ độ **dò từ pixel**, xem gotchas) cho `mouth`/`eyes`/`chat`; actor bật `talk` (nhép theo giọng/chữ), `mime` (nhép không thoại), `chat` (2 người nói xen kẽ trên cùng ảnh), `neutral` (miệng khép, chưa cười). Chớp mắt tự động nếu ảnh có `eyes`.
- Render: `npm install` → `npm run render` → `video/<slug>.mp4`. Kiểm tra bằng `npx remotion still` + ảnh phóng to vùng mặt.
- **Âm nền:** `python make_bed.py` (sau `make_durations.py`) → `public/audio/bed.wav` = nhạc nền tự hạ khi có giọng + hiệu ứng theo mốc cảnh. Âm thật từ Mixkit/Freesound CC0 vào `public/sfx/` (design-rules §10, gotchas).
- **Nền & hiệu ứng có sẵn (talk02):** `bg` = `home` | `school` (bảng đen) | `road` (đường tới trường) | `floor` (sàn nhìn từ trên xuống) | `duo` (1 màu, cảnh 2 người) | `versus`; `split` + `clock`; `spark` (tia sét SVG); `who` (`jx`|`yh`|`both`) + `story.json "tags"` = nhãn phe theo nhân vật; `video`/`vstart` = đoạn cử động thật (mục dưới). `FACE.draw` = vẽ miệng mở đè lên ảnh miệng khép.
- **Đoạn kết + chống copy** đã gắn sẵn trong `Story.tsx` (`Outro.tsx`, `outro.json` = giây của `public/audio/outro.wav` giọng 瑾玄) — design-rules §11.

## Cử động thật bằng muse-video (ảnh → video, dùng trong `story-clip`)
Ví dụ đã chạy: `output/Gen ảnh_video/talk02/tranhluan/` (11 đoạn, user duyệt 2026-11-01). Ảnh tĩnh + Remotion trượt/nhún bị chê
"giống mấy ảnh tĩnh ghép lại" → mỗi cảnh 1 đoạn cử động thật, giữ đúng nhân vật đã duyệt.
1. Dựng bố cục cảnh bằng ảnh tĩnh như thường (story.json `actors`, nền `bg`) → xuất **khung sạch** (không chữ/logo — AI làm méo chữ):
   `npx remotion still src/index.ts Story assets/keyframes/<id>.png --frame=N --props='{"clean":true}'`
2. Mô tả chuyển động trong `src/motion.json` (`common` + `clips.<id>`): **ghi rõ AI nói, ai "mouth stays CLOSED"** (design-rules §9).
3. `python gen_motion.py [id…]` (venv của skill) → `assets/motion/<id>.mp4` (10s, giữ tỉ lệ khung mẫu). **Gen lần lượt từng đoạn** —
   3 yêu cầu song song bị máy chủ ngắt / 502. Mỗi đoạn ~1,5–4 phút.
4. Soát cận mặt mỗi 0,5–1s (`ffmpeg -vf "fps=1,crop=…,tile=5x2"`): mặt giữ đúng chưa, người nghe có ngậm miệng không → chọn khúc đẹp.
5. Chép sang `public/motion/`, gắn vào cảnh: `"video": "<id>", "vstart": <giây bắt đầu cắt>` (cảnh liền sau cùng video tự phát tiếp).
   `Story.tsx` dựng **lớp video riêng**: 1 trình phát / đoạn, chồng mờ 10 khung giữa 2 đoạn, `premountFor` — hết nháy/giật.
   Phụ đề, nhãn, tia sét, chống copy vẫn do Remotion vẽ chồng lên. Âm gốc của video tắt. Miệng AI không khớp từng chữ (giới hạn).
6. Trước khi gọi muse-video lần đầu trong session → hỏi user (tốn lượt, ~4 phút/lần).

## Video 朗读 (khuôn `template/read-along/`, dùng cho Talk series clip ②)
Ví dụ đã chạy: `output/Gen ảnh_video/talk01/langdu/` (bài 1 快乐会传染, nhân vật 越黄). ĐỌC `reference/design-rules.md` §11–12 trước khi dựng.
1. **Cổng nội dung:** bài đọc (`p2Text` trong `onluyen/on-luyen.html`, nguyên văn), tên bài, bảng ~14 từ khoá (汉字 · pinyin · EN · VI) → user duyệt → ghi `src/data.json` (`title, topic, channel, character, gender, text, words`).
   **Trước khi đưa bảng:** grep từng từ trong `output/Gen ảnh_video/talk*/*/src/*.{json,tsx}` — từ đã làm thẻ ở video khác (langdu `words`, HSKK cụm đáng học) → thay từ khác trong bài
   (2026-11-03 phải dừng render giữa chừng vì 不可否认 trùng talk02/hskk-c5). Nhân vật luân phiên: 01 越黄 · 02 瑾玄 · 03 越黄 (tấm chuẩn `talk01/langdu/public/img/yh_front_v1.png`, không gen lại);
   giọng 越黄 = `--voice zh-CN-YunxiaNeural --rate +8%`. Nhanh nhất: chép code + `public/` từ project langdu gần nhất rồi thay `data.json`/`sizes.json`.
2. **Cổng ảnh:** nhân vật mặc đồng phục trường phù thuỷ, nhìn thẳng, cầm sách, nền mint → `python cutout_mint.py <tên>`; xem khung tĩnh `npx remotion still src/index.ts Read out/preview-en.png --frame=N` (+ `ReadVI`).
3. **Giọng:** `.claude/skills/genimagevideo/.venv/Scripts/python.exe voice_edge.py` → `public/audio/read.wav` + `src/timing.json` (mốc từng chữ từ WordBoundary). User tự thu thì bỏ `read.m4a` vào `public/audio/` rồi `python align.py` (dò chỗ ngắt hơi ↔ dấu câu).
4. Nhạc nền `public/audio/bg.mp3` (rất nhỏ, `loop`); đoạn kết `public/audio/outro.wav` (giọng 瑾玄, câu 收听) + `src/outro.json`.
5. Render **bản VI trước**: `npx remotion render src/index.ts ReadVI video/<slug>-vi.mp4` (~8 phút) → mở cho user → **chờ chốt** → mới render EN `Read … -en.mp4` (render liền 2 bản thì mỗi lần sửa phải render lại cả 2 — user nhắc 2026-11-03).
   **Bàn giao = đủ cả 2 bản `-en` + `-vi`** — liệt kê `video/` trước khi báo xong (user từng tự phát hiện thiếu EN).
6. Có sẵn trong khuôn (talk02): 15s chuẩn bị đếm trong ô thẻ + tiếng `public/sfx/ting.wav` (chép từ `talk02/langdu`), cụm từ đọc sát
   nhau khai `data.json "groups": [["欠佳","不得已","另辟蹊径"]]` — xem design-rules §12. **Chỉ khai `groups` sau khi đo `timing.json`** thấy các từ cách nhau 0,5–1s;
   không chép `groups` từ tập trước (talk03 chép nhầm 3 cụm cách nhau 1,4–3,1s → user hỏi "sao 1 thẻ 2 từ", phải bỏ gộp + render lại).

## Video HSKK 回答问题 (khuôn `template/hskk-answer/`, câu 5 & 6 mỗi chủ đề Talk series)
Ví dụ đã chạy: `output/Gen ảnh_video/talk01/hskk-c5/` (Chủ đề 1 · câu 5). 1 video/câu × 2 bản EN/VI, ~2-3 phút. ĐỌC `template/hskk-answer/README.md` (luồng 7 bước) + `reference/design-rules.md` §13 trước khi dựng.
- Tạo project: `python .claude/skills/genimagevideo/scripts/new_project.py talkNN/hskk-cN --template hskk-answer` (**phải có `--template`**, mặc định là poster-highlight). Nếu có project HSKK mới hơn khuôn thì chép `src/` + script của project đó (bản mới nhất: `talk03/hskk-c5` — có dòng 0/dòng ảo, hồi tưởng sepia, phụ đề tự thu chữ) rồi thay nội dung.
- Nguồn = `onluyen/bai-mau-cau5-6.md` của user (không tự soạn). Cổng nội dung (phụ đề + dịch + mindmap + cụm khó + storyboard ~14 cảnh) → giọng → khung tĩnh K1…Kn → clip muse-video (tự bỏ tiếng) → ghép `Full.tsx` → render FullVI/FullEN (**bàn giao đủ cả 2 bản**, liệt kê `video/` trước khi báo xong; video có clip muse-video → render bằng `bash chunk_render.sh FullEN video/<slug>-en.mp4`, xem gotchas). Nhạc nền suốt video. Làm lần lượt chủ đề 1 c5, c6 → chủ đề 2 c5, c6…

## Ảnh bìa bài đăng (Talk series)
Ví dụ: `output/Gen ảnh_video/talk01/contagious/src/Cover.tsx` → `cover/talk01-cover.png`.
- **1 khung 3:4 (1080×1440) dùng chung mọi nền tảng** (RedNote/IG/FB/HelloTalk/TikTok ảnh) — user chọn, đỡ phải nhớ bản nào đăng đâu; bìa video TikTok lấy từ chính clip.
- **Ghép từ ảnh nhân vật đã duyệt** trong `public/img/` của project clip, KHÔNG gen lại (gen lại → nhân vật xê dịch, lệch clip; không tốn lượt gen).
- Thêm composition `Cover` (durationInFrames 1) vào `Root.tsx`, render: `npx remotion still src/index.ts Cover cover/<slug>-cover.png --frame=0` → Read ảnh tự soát rồi mở cho user.
- Tiêu đề font thật ~104px (132px bị chê to); tiêu đề + mặt nhân vật dồn vùng giữa vì HelloTalk/FB cắt ảnh xem trước gần vuông.
- **Chưa có project clip** (vd tập 03): vẽ NGUYÊN CẢNH bằng `gen_image.py --size 1536x1024` (mô tả 瑾玄/越黄 theo `nhan-vat/README.md`) → sửa chi tiết bằng Pillow
  → ghép chữ bằng `cover.html` + Chrome headless (mẫu + lệnh: `talk03/cover/README.md`). Gen 2 phương án/lượt, soát từng tấm trước khi đưa user.
- **Bài học cảnh bìa (2026-11-03):** phải thể hiện đúng KHÁI NIỆM bài, nhìn là hiểu không cần chữ (活人图书馆 = phòng đọc nhiều "cuốn sách người"
  đeo thẻ quyển sách, 1 ghế trống chờ được mượn); 2 người ngồi đối diện = bị đọc thành "hẹn hò"; cảnh **tối giản** (ít bàn, tường trơn, ít cây — bị chê "nhiều hoạ tiết");
  người nghe là người lớn, không trẻ con; bìa trơn bị chê "thiếu hiệu ứng" → thêm tia sáng toả mờ dần (giống tập 01) + vài ✨ (không đè mặt) + bong bóng thoại ngắn nói ý chủ đề.

## Nhân vật chibi (Talk series + video)
- Ảnh chụp thật làm mẫu: `raw/nhan-vat/<tên>/` — **gitignored**, không lên GitHub. User tự bỏ ảnh vào; nhân vật đã có thì dùng lại, không xin lại ảnh.
- Bản chibi + hồ sơ: `output/Gen ảnh_video/nhan-vat/<tên>/avatar.png` + `nhan-vat/README.md` (dấu hiệu nhận diện từng người — ĐỌC trước khi vẽ).
- Phong cách chung: chibi đầu to, nét mảnh, tô phẳng pastel, nền mint trơn (để tách nền), không chữ/logo.
- **Model ảnh của 9router KHÔNG sửa được ảnh theo ảnh mẫu** (xem gotchas) → mỗi lần vẽ lại, nhân vật xê dịch. (Muốn nhân vật **cử động** mà giữ đúng mặt → dùng muse-video ảnh→video, mục "Cử động thật".)
  Chỉnh chi tiết nhỏ (thêm đồng hồ, đổi tay) → **lật ảnh / vẽ đè bằng Pillow** trên tấm đã duyệt, không vẽ lại cả nhân vật.
- Người thật khác (bạn bè, bố mẹ): chỉ vẽ theo ảnh khi user tự gửi; nhắc user hỏi ý người đó trước khi đăng công khai.

## Không làm
- Không để AI vẽ chữ Hán/pinyin trong ảnh — chữ do Remotion vẽ bằng font thật.
- Không gửi key tới endpoint tự đoán; không in key ra terminal; không commit `.env`.
- Không thêm hiệu ứng thứ hai "cho sinh động" (xem design-rules.md §1).
- Không render toàn bộ khi chưa qua lint + still check.
