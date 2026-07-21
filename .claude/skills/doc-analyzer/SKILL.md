---
name: doc-analyzer
version: "1.3.0"
description: >
  Skill trích xuất tri thức từ tài liệu (PDF, DOCX, XLSX, CSV, MD, TXT, HTML) — ví dụ giáo trình, tài liệu học.
  PDF luôn được quy về text (pypdf); PDF scan tự động OCR fallback (Tesseract vie+eng+chi_sim).
  Two-phase: Structure Scan → Targeted Extraction.
  Output: in-context YAML compact blocks. Không sinh file knowledge.
  Knowledge > Text — token efficiency là ưu tiên.
author: Chinese Learning OS
modes:
  standalone:
    trigger: "User gọi /doc-analyzer {file_path}"
    description: "Phân tích 1 file, output YAML block trong context"
---

# doc-analyzer Skill

> Trích xuất tri thức từ tài liệu thô với token usage tối thiểu.
> **Không sinh file output.** Output là YAML block trong conversation context.
> **Knowledge > Text.** Không copy nguyên văn — chỉ chuẩn hóa và nén.

---

## Bước 0 — Xác định file đầu vào

User gọi trực tiếp với file path:
```
/doc-analyzer raw/HSK6-textbook.pdf
```
→ Dùng file path user truyền vào.

Nếu user chỉ gọi `/doc-analyzer` không kèm path:
```
Scan raw/ → lấy tất cả files có extension: .pdf .docx .xlsx .csv .txt .html
```
- Nếu có 1 file → dùng file đó
- Nếu nhiều file → chọn file **mới nhất** (modified date) tự động. Thông báo: `[doc-analyzer] Auto-selected: {filename} (most recent)`
- Nếu không có file nào → thông báo "raw/ trống hoặc không có file được hỗ trợ" → dừng

---

## Bước 1 — Layer 1: File Detection & Conversion

Kiểm tra extension của file đầu vào:

| Extension | Action |
|-----------|--------|
| `.pdf` | **Quy về text bằng script `pdf_to_text.py`** (text-PDF: pypdf; scan-PDF: OCR). Xem bên dưới. **KHÔNG** dùng Read tool cho `.pdf` (render ảnh → tốn token + cần poppler) |
| `.md` `.txt` `.csv` `.html` | Đọc trực tiếp bằng Read tool |
| `.docx` | Convert bằng pandoc (xem bên dưới) |
| `.xlsx` | Convert bằng Python pandas (xem bên dưới) |
| `.pptx` | **Convert bằng `pptx_to_text.py`** (python-pptx). In `PPTX <out.txt> <slides>` → đọc file `<out.txt>`. |

### Convert PDF → Text (text-PDF hoặc scan-PDF/OCR)

**Nguyên tắc:** PDF luôn được quy về **file text** trước khi vào Structure Scan.
- **Text-PDF** (có text trích được): dùng `pypdf` → rẻ, nhanh, không cần poppler.
- **Scan-PDF** (ảnh, ~0 text): tự động **OCR fallback** — PyMuPDF render 200 DPI → Tesseract `vie+eng+chi_sim`.

Chạy script (tự phát hiện text vs scan, tự cache):
```bash
python "{skill_dir}/pdf_to_text.py" "{file_path}"
```
Script in ra 1 dòng kết quả:
- `TEXT_PDF <out.txt> <pages>` → PDF text thường → đọc file `<out.txt>`
- `SCAN_PDF <out.ocr.txt> <pages>` → PDF scan đã OCR → đọc file `<out.ocr.txt>`
- `CACHED <path> <pages>` → dùng lại kết quả OCR đã cache (bỏ qua OCR)

Output text được ghi cạnh file gốc: `{file_path}.txt` (text-PDF) hoặc `{file_path}.ocr.txt` (scan-PDF), phân trang bằng marker `===== PAGE n =====`.

**Cache:** nếu `{file_path}.ocr.txt` đã tồn tại và mới hơn PDF → script trả `CACHED`, không OCR lại.

**Ngưỡng phát hiện scan:** trung bình < 25 ký tự/trang → coi là scan.
**Số trang lớn:** scan > 100 trang → script cảnh báo `[doc-analyzer] Scan {N} trang, OCR có thể mất vài phút…` rồi vẫn chạy.
**DPI:** mặc định 200. Nếu OCR ra chữ sai nhiều (chữ nhỏ/mờ) → chạy lại với `--dpi 300`.
**OCR có target (`--pages`):** sách/PDF scan lớn (vài trăm trang) mà chỉ cần 1 chương → dùng `--pages START-END` (1-based, inclusive) để **chỉ OCR dải trang đó**, tránh OCR mù cả file:
```bash
python "{skill_dir}/pdf_to_text.py" "{file_path}" --pages 10-48
```
Output ghi ra tên có hậu tố dải trang, vd `{file_path}.p10-48.ocr.txt` (không đè cache OCR toàn bộ). Sai cú pháp → `ERROR BADPAGES`. Quy trình gợi ý: structure-scan (OCR vài trang mục lục) tìm dải trang cần → OCR target đúng dải đó.

Nội dung file `pdf_to_text.py` (đặt trong thư mục skill — trích yếu; bản chạy có thêm hàm `parse_pages()` xử lý `--pages`):
```python
import sys, os, subprocess, tempfile, argparse, shutil

ap = argparse.ArgumentParser()
ap.add_argument("pdf")
ap.add_argument("--dpi", type=int, default=200)
ap.add_argument("--lang", default="vie+eng+chi_sim")
ap.add_argument("--scan-threshold", type=int, default=25)  # avg chars/page
ap.add_argument("--pages", default=None)  # "5-48" (1-based, inclusive) → chỉ xử lý dải trang
a = ap.parse_args()

PDF = a.pdf
if not os.path.exists(PDF):
    print("ERROR NOFILE " + PDF); sys.exit(2)

def page_marker(i, t):
    return "\n===== PAGE %d =====\n%s" % (i + 1, (t or "").strip())

# ---- 1) Try text extraction (pypdf) ----
try:
    from pypdf import PdfReader
except ImportError:
    print("ERROR NOPYPDF"); sys.exit(3)

reader = PdfReader(PDF)
n = len(reader.pages)
texts = [(p.extract_text() or "") for p in reader.pages]
total = sum(len(t) for t in texts)
avg = total / max(n, 1)

if avg >= a.scan_threshold:
    out = PDF + ".txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(page_marker(i, t) for i, t in enumerate(texts)))
    print("TEXT_PDF %s %d" % (out, n)); sys.exit(0)

# ---- 2) Scan-PDF → OCR ----
out = PDF + ".ocr.txt"
if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(PDF):
    print("CACHED %s %d" % (out, n)); sys.exit(0)

if n > 100:
    sys.stderr.write("[doc-analyzer] Scan %d trang, OCR có thể mất vài phút…\n" % n)

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR NOPYMUPDF"); sys.exit(4)

# locate tesseract
TESS = shutil.which("tesseract")
for c in [r"C:\Program Files\Tesseract-OCR\tesseract.exe",
          os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe")]:
    if not TESS and os.path.exists(c):
        TESS = c
if not TESS:
    print("ERROR NOTESSERACT"); sys.exit(5)

doc = fitz.open(PDF)
parts = []
with tempfile.TemporaryDirectory() as tmp:
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(dpi=a.dpi)
        ip = os.path.join(tmp, "p.png")
        pix.save(ip)
        r = subprocess.run([TESS, ip, "stdout", "-l", a.lang, "--psm", "3"],
                           capture_output=True, text=True, encoding="utf-8")
        parts.append(page_marker(i, r.stdout))
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(parts))
print("SCAN_PDF %s %d" % (out, n))
```

### Convert DOCX → Markdown
```bash
pandoc "{file_path}" -t markdown --wrap=none -o "{file_path}.converted.md"
```
Sau khi chạy xong → đọc file `{file_path}.converted.md` bằng Read tool.

### Convert XLSX → CSV (mỗi sheet thành 1 file CSV)
```bash
python -c "
import pandas as pd, sys
f = sys.argv[1]
xl = pd.ExcelFile(f)
for s in xl.sheet_names:
    out = f + '.' + s.replace(' ','_') + '.csv'
    xl.parse(s).to_csv(out, index=False)
    print('Converted:', out)
" "{file_path}"
```
Sau khi chạy → đọc tất cả file `.csv` được tạo ra.

### Xử lý lỗi
- `pandoc` chưa cài: Báo `[ERROR] pandoc chưa cài. Cài bằng: winget install pandoc` → dừng
- `python` / `pandas` chưa cài: Báo `[ERROR] Cần Python + pandas. Cài: pip install pandas openpyxl` → dừng
- File không tồn tại: Báo `[ERROR] Không tìm thấy file: {file_path}` → dừng

### Xử lý lỗi công cụ PDF/OCR (khi `pdf_to_text.py` in ra `ERROR <code>`)

Chính sách: **thử tự cài trước → nếu thất bại (không mạng/không quyền) thì báo lỗi + hướng dẫn → dừng.**
Sau khi tự cài thành công, **chạy lại** `pdf_to_text.py` một lần.

| Code script in ra | Tự cài (thử) | Nếu thất bại → báo |
|---|---|---|
| `ERROR NOPYPDF` | `python -m pip install pypdf` | `[ERROR] Cần pypdf. Cài: pip install pypdf` |
| `ERROR NOPYMUPDF` | `python -m pip install pymupdf` | `[ERROR] Cần PyMuPDF. Cài: pip install pymupdf` |
| `ERROR NOTESSERACT` | `winget install --id UB-Mannheim.TesseractOCR -e --silent --accept-source-agreements --accept-package-agreements` | `[ERROR] Cần Tesseract OCR. Cài: winget install UB-Mannheim.TesseractOCR` |
| `ERROR NOPPTX` | `python -m pip install python-pptx` | `[ERROR] Cần python-pptx. Cài: pip install python-pptx` |
| `ERROR NOFILE` | — | `[ERROR] Không tìm thấy file: {file_path}` → dừng |

**Thiếu language data OCR** (Tesseract có nhưng thiếu `chi_sim`/`vie`): tải `.traineddata` vào `<tessdata>`:
```bash
# <tessdata> thường: %LOCALAPPDATA%\Programs\Tesseract-OCR\tessdata hoặc C:\Program Files\Tesseract-OCR\tessdata
for L in chi_sim vie; do
  curl -L -o "<tessdata>/$L.traineddata" \
    "https://github.com/tesseract-ocr/tessdata_fast/raw/main/$L.traineddata"
done
```
Kiểm tra: `tesseract --list-langs` phải có `chi_sim`, `vie`, `eng`. Nếu winget/tải fail (không mạng/không quyền) → báo lỗi + hướng dẫn cài tay → dừng.

**Lưu ý PowerShell:** trên Windows, gọi Python bằng đường dẫn tuyệt đối nếu `python` trong PATH là stub Microsoft Store (thường ở `%LOCALAPPDATA%\Programs\Python\Python3xx\python.exe`).

---

## Bước 2 — Layer 2: Structure Scan (Phase 1)

**Mục tiêu:** Build extraction map — tìm ra sections chứa business knowledge, bỏ boilerplate.

### Quy tắc đọc
- Document ≤ 300 dòng: đọc toàn bộ
- Document > 300 dòng: đọc **tối đa 200 dòng đầu**
- Document > 500 dòng VÀ có TOC rõ ràng: đọc 100 dòng đầu mỗi major section (header `#` hoặc dấu phân cách `---`)
- **KHÔNG BAO GIỜ** đọc > 300 dòng trong 1 lần Read call

Nếu không tìm thấy TOC → cảnh báo: `[doc-analyzer] Không tìm thấy TOC. Scan 200 dòng đầu.`

### Keywords INCLUDE — sections cần đọc sâu
```
quy trình | workflow | flow | luồng | process | nghiệp vụ
điều kiện | condition | rule | quy tắc | ràng buộc | áp dụng khi
tính toán | công thức | formula | calculation | phí | lãi suất | tính phí
validate | kiểm tra | validation | hợp lệ | bắt buộc | không được để trống
mapping | ánh xạ | field | trường | cấu trúc dữ liệu | data
```

### Keywords SKIP — sections bỏ qua
```
lịch sử | revision history | history | changelog | phiên bản
bìa | cover | trang bìa | tiêu đề
mục lục | table of contents | toc | danh sách
chữ ký | signature | phê duyệt | approval | sign off
phụ lục | appendix | reference | tài liệu tham chiếu | glossary
```

### Output Phase 1
Thông báo extraction map ngắn gọn:
```
[doc-analyzer] Extraction map: §2.1 Quy trình đăng ký, §3 Điều kiện áp dụng, §4.2 Công thức phí
```
Nếu không tìm thấy section nào liên quan:
```
[doc-analyzer] Không tìm thấy section nghiệp vụ rõ ràng. Phân tích toàn bộ nội dung.
```

---

## Bước 3 — Layer 3: Targeted Extraction (Phase 2)

Đọc **chỉ các sections** trong extraction map từ Phase 1. Nếu Phase 1 không identify được → đọc toàn bộ (với giới hạn 300 dòng/lần).

### Business Rules
**Nhận dạng:** câu có "phải", "cần", "không được", "điều kiện:", "trường hợp:", "áp dụng khi"
**Format:** `condition → consequence` viết ngắn gọn 1 dòng
**ID:** BR-01, BR-02…

### Workflow
**Nhận dạng:** bước đánh số, actor được đề cập rõ, trình tự hành động
**Format:** `step + actor + action + trigger + next`
**Không bao gồm:** chi tiết UI (button label, màu sắc, vị trí element)

### Validation Rules
**Nhận dạng:** "nếu … thì báo lỗi", range check, "bắt buộc", "không hợp lệ nếu"
**Format:** `field + condition + error message`
**Fallback:** Nếu không có error message trong tài liệu → `error: "[TBD]"`

### Calculation Formula
**Nhận dạng:** công thức toán học, ký hiệu %, ×, ÷, "bằng cách", "tính theo", "áp dụng công thức"
**Format:** `tên + công thức rút gọn + định nghĩa biến`
**Chuẩn hóa:** dùng ký hiệu toán học thuần (`*`, `/`, `+`, `-`) thay chữ dài

### Data Mapping
**Nhận dạng:** bảng ánh xạ field, "tương ứng với", "lấy từ", "map sang", "đổ vào"
**Format:** `source → target + transform`

### Dependencies
**Nhận dạng:** "phụ thuộc vào", "cần có X mới được Y", "sau khi", "yêu cầu trước", "prerequisite", điều kiện tiên quyết giữa 2 bước/module
**Format:** `X phụ thuộc vào Y (loại: data|sequence|rule)`
**ID:** DEP-01, DEP-02…

### Open Questions
**Nhận dạng:** "TBD", "cần xác nhận", "chờ quyết định", "chưa rõ", "TODO", mâu thuẫn giữa 2 đoạn trong tài liệu
**Format:** câu hỏi ngắn + context (section tham chiếu). Ghi cả 2 phát biểu nếu phát hiện mâu thuẫn.
**ID:** OQ-01, OQ-02…

### Compression Rules (BẮT BUỘC với mọi knowledge type)
1. Không copy nguyên văn đoạn văn từ tài liệu gốc
2. Rút gọn về dạng ngắn nhất còn đủ ý
3. Ghi `source_ref`: số section (`§3.2`), hoặc trang (`p.12`)
4. **Omit key hoàn toàn** nếu knowledge type không tìm thấy — KHÔNG để array `[]` rỗng

---

## Bước 4 — Output YAML Block

In YAML block sau vào conversation context (không ghi ra file):

```yaml
# @extracted_knowledge | source: "{filename}" | doc_type: {LESSON|REFERENCE|DATA|OTHER}
business_rules:
  - id: BR-01
    rule: "..."
    source_ref: "§x.y"
workflow:
  - step: 1
    actor: "..."
    action: "..."
    trigger: "..."
    next: 2
    source_ref: "§x.y"
validation_rules:
  - field: "..."
    condition: "..."
    error: "..."
    source_ref: "§x.y"
calculation_formulas:
  - name: "..."
    formula: "..."
    variables:
      var_name: "định nghĩa"
data_mapping:
  - source: "field_a"
    target: "field_b"
    transform: "direct | formula | lookup"
dependencies:
  - id: DEP-01
    subject: "X"
    depends_on: "Y"
    type: "data|sequence|rule"
    source_ref: "§x.y"
open_questions:
  - id: OQ-01
    question: "..."
    context: "§x.y"
# /@extracted_knowledge
```

### doc_type detection (tự suy luận)
| Tên file chứa | doc_type |
|---------------|----------|
| giáo trình, bài học, lesson, textbook, HSK | `LESSON` |
| từ vựng, ngữ pháp, reference, cheat sheet, tra cứu | `REFERENCE` |
| bảng, list, csv, data, dữ liệu | `DATA` |
| Khác | `OTHER` |

### Extraction priorities by doc_type

| doc_type | Tập trung nhiều | Bỏ qua tương đối |
|----------|-----------------|-----------------|
| `LESSON` | workflow (trình tự bài), business_rules (quy tắc dùng), open_questions | data_mapping |
| `REFERENCE` | business_rules (quy tắc/ngữ pháp), validation_rules | workflow |
| `DATA` | data_mapping | business_rules (trừ khi explicit) |
| `OTHER` | tất cả đều nhau | — |

### Summary line (in sau YAML block)
```
[doc-analyzer] Extracted: {N} BR, {M} workflow steps, {K} VR, {J} formulas, {L} mappings, {P} deps, {Q} OQs from "{filename}" [{doc_type}]
```
