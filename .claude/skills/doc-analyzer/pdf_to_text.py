import sys, os, subprocess, tempfile, argparse, shutil

ap = argparse.ArgumentParser()
ap.add_argument("pdf")
ap.add_argument("--dpi", type=int, default=200)
ap.add_argument("--lang", default="vie+eng+chi_sim")
ap.add_argument("--scan-threshold", type=int, default=25)  # avg chars/page
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

# ---- 2) Scan-PDF -> OCR ----
out = PDF + ".ocr.txt"
if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(PDF):
    print("CACHED %s %d" % (out, n)); sys.exit(0)

if n > 100:
    sys.stderr.write("[doc-analyzer] Scan %d trang, OCR co the mat vai phut...\n" % n)

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
