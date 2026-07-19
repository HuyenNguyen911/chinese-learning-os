# _inbox — Hộp nạp từ vựng

Thả file export từ Google Sheet vào đây, rồi gõ **"sync backlog"** trong chat.

## Cách làm
1. Google Sheet → **File → Download → Comma-separated values (.csv)**
2. Bỏ file `.csv` vào chính folder này (`knowledge/vocabulary/_inbox/`)
3. Gõ: **sync backlog**

## Cột Sheet nên có (tối thiểu 2 cột đầu)
| Cột | Bắt buộc | Ghi chú |
|---|---|---|
| 词 / Từ (Hán) | ✅ | Khóa dedup — bắt buộc |
| Nghĩa | ✅ | Tiếng Việt |
| Pinyin | tùy | Nếu trống, hệ thống tự điền |
| Ngày thêm | tùy | |
| Buổi / Nguồn | tùy | |

Thứ tự cột không quan trọng — miễn có header. Strategist tự map.

## An toàn khi lặp
Dedup theo **chữ Hán** trên CẢ 2 nơi: `master-backlog.md` (kho 1316 từ) **và** tier-a/b/c.md.
Cứ export **cả bảng** mỗi lần — hệ thống chỉ thêm từ chưa có, không tạo bản trùng.
Không cần nhớ "lần trước sync tới đâu".

## Kiến trúc 2 tầng
- **master-backlog.md** = KHO (toàn bộ corpus, gom theo bài) — chỉ để tra + dedup, KHÔNG học dàn trải.
- **tier-a/b/c.md** = ACTIVE (từ đang thực sự học, ~40 từ Tier A) — học qua 3-nhịp, leo D→C→B→A.
- Từ mới sync vào → mặc định nằm ở master. Strategist mới kéo lên tier khi tới lượt học.

## Sau khi sync
- Từ mới được phân tier (A/B/C) + ghi vào `knowledge/vocabulary/tier-*.md`
- `state/activation.md` cập nhật số đếm
- File `.csv` đã xử lý được đổi tên `<tên>.processed.csv` (giữ lại để đối chiếu)
