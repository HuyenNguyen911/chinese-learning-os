# lesson-prep Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây skill `lesson-prep` bóc tách file `.pptx` bài khóa HSK6 → nạp từ vựng vào tier-a + trang học vocab-study, và xuất bài tập/bài viết ra 1 file `.docx`.

**Architecture:** doc-analyzer thêm bước convert pptx→text (Tầng 1). lesson-prep (Claude điều phối trong SKILL.md) đọc text, phân loại slide, xuất 2 JSON trung gian (`vocab_payload.json`, `exercise_payload.json`), rồi gọi trực tiếp các script Python để: (a) append tier-a.md + xlsx → chạy pipeline vocab-study, (b) render 1 `.docx` gộp bằng renderer đã mở rộng của exercise-generator.

**Tech Stack:** Python 3.12, `python-pptx` (1.0.2), `python-docx`, `openpyxl`, `pypinyin`, pytest 9.1.1.

## Global Constraints

- Python interpreter: `C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe` (gọi tắt `$PY`). Chạy mọi lệnh **từ gốc repo** `c:/Tài liệu/ai-vault/CHINESE`.
- Mọi script Python phải `stdout/stderr.reconfigure(encoding="utf-8")` ở đầu `main()` (console Windows mặc định cp1252, in tiếng Việt/Trung sẽ crash).
- Ghi file `.md`/`.txt` luôn `encoding="utf-8"`.
- Từ vựng chuẩn hoá đúng cột sheet 'Từ vựng': `Bài, 生词, Pinyin, 描述(释义 TQ đơn giản), 意义(nghĩa Việt), 例如(ví dụ), 复习, 检查`.
- Từ mới vào tier-a.md dùng `Activation: D` (mức thấp nhất "chưa dùng được" — không có giá trị 0/⚪ trong file).
- Ghi tier-a.md **append-only, dedup theo 生词** trên cả tier-a/b/c; KHÔNG sửa entry cũ.
- Phong cách đáp án AI: tự nhiên, khẩu ngữ, đơn giản nhưng điểm cao.
- **One Request = One Skill:** lesson-prep gọi *script* của skill khác, KHÔNG invoke skill khác.
- Không sinh audio.

---

### Task 1: doc-analyzer — convert pptx → text

**Files:**
- Create: `.claude/skills/doc-analyzer/pptx_to_text.py`
- Create: `.claude/skills/doc-analyzer/tests/test_pptx_to_text.py`
- Modify: `.claude/skills/doc-analyzer/SKILL.md` (thêm dòng `.pptx` vào bảng conversion + đoạn mô tả script)

**Interfaces:**
- Produces: CLI `python pptx_to_text.py <file.pptx>` → ghi `<file.pptx>.txt`, in 1 dòng `PPTX <out> <slides>` khi OK; `ERROR NOPPTX` nếu thiếu lib; `ERROR NOFILE <path>` nếu không có file. Hàm lõi `slide_to_text(slide, idx) -> str`.

- [ ] **Step 1: Write the failing test**

Tạo `.claude/skills/doc-analyzer/tests/test_pptx_to_text.py`:

```python
# -*- coding: utf-8 -*-
import os, sys, subprocess
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "pptx_to_text.py"
PY = sys.executable

def _make_pptx(path):
    prs = Presentation()
    # Slide 1: title + body
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = "生词"
    s.placeholders[1].text = "尴尬 gāngà bối rối"
    s.notes_slide.notes_text_frame.text = "ghi chú của cô"
    # Slide 2: table
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    tbl = s2.shapes.add_table(2, 2, Inches(1), Inches(1), Inches(4), Inches(1)).table
    tbl.cell(0, 0).text = "词"; tbl.cell(0, 1).text = "拼音"
    tbl.cell(1, 0).text = "尴尬"; tbl.cell(1, 1).text = "gāngà"
    prs.save(str(path))

def test_pptx_to_text(tmp_path):
    pptx = tmp_path / "bai.pptx"
    _make_pptx(pptx)
    r = subprocess.run([PY, str(SCRIPT), str(pptx)], capture_output=True,
                       text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("PPTX ")
    out = pptx.with_suffix(".pptx.txt")
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "===== SLIDE 1 =====" in text
    assert "[TITLE] 生词" in text
    assert "尴尬" in text
    assert "[NOTES] ghi chú của cô" in text
    assert "===== SLIDE 2 =====" in text
    assert "[TABLE]" in text

def test_pptx_to_text_nofile(tmp_path):
    r = subprocess.run([PY, str(SCRIPT), str(tmp_path / "missing.pptx")],
                       capture_output=True, text=True, encoding="utf-8")
    assert "ERROR NOFILE" in r.stdout
```

- [ ] **Step 2: Run test to verify it fails**

Run: `$PY -m pytest .claude/skills/doc-analyzer/tests/test_pptx_to_text.py -v`
Expected: FAIL (script chưa tồn tại → lỗi import/no such file).

- [ ] **Step 3: Write minimal implementation**

Tạo `.claude/skills/doc-analyzer/pptx_to_text.py`:

```python
# -*- coding: utf-8 -*-
"""pptx_to_text.py — convert 1 file .pptx thành text có cấu trúc cho lesson-prep.

Mỗi slide 1 khối, giữ [TITLE]/[BODY]/[TABLE]/[NOTES]. Ghi cạnh file gốc:
{file}.pptx.txt. In 1 dòng: PPTX <out> <slides>.

Chạy:  python pptx_to_text.py <file.pptx>
Cần: python-pptx.
"""
import sys, os

try:
    from pptx import Presentation
except ImportError:
    print("ERROR NOPPTX"); sys.exit(3)


def slide_to_text(slide, idx):
    lines = ["===== SLIDE %d =====" % idx]
    title, title_id = None, None
    try:
        t = slide.shapes.title
        if t is not None and (t.text or "").strip():
            title = t.text.strip(); title_id = t.shape_id
    except Exception:
        title = None
    if title:
        lines.append("[TITLE] " + title)
    for shape in slide.shapes:
        if title_id is not None and getattr(shape, "shape_id", None) == title_id:
            continue
        if getattr(shape, "has_table", False) and shape.has_table:
            rows = []
            for row in shape.table.rows:
                rows.append(" | ".join((c.text or "").strip() for c in row.cells))
            if rows:
                lines.append("[TABLE] " + rows[0])
                lines.extend("        " + r for r in rows[1:])
        elif getattr(shape, "has_text_frame", False) and shape.has_text_frame:
            txt = (shape.text_frame.text or "").strip()
            if txt:
                lines.append("[BODY] " + txt.replace("\n", " / "))
    try:
        if slide.has_notes_slide:
            notes = (slide.notes_slide.notes_text_frame.text or "").strip()
            if notes:
                lines.append("[NOTES] " + notes)
    except Exception:
        pass
    return "\n".join(lines)


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    if len(argv) != 2:
        print("Usage: python pptx_to_text.py <file.pptx>", file=sys.stderr); return 2
    path = argv[1]
    if not os.path.exists(path):
        print("ERROR NOFILE " + path); return 2
    prs = Presentation(path)
    blocks = [slide_to_text(s, i) for i, s in enumerate(prs.slides, start=1)]
    out = path + ".txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n\n".join(blocks))
    print("PPTX %s %d" % (out, len(blocks)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `$PY -m pytest .claude/skills/doc-analyzer/tests/test_pptx_to_text.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Update doc-analyzer SKILL.md**

Trong bảng conversion (Bước 1), thêm dòng:

```
| `.pptx` | **Convert bằng `pptx_to_text.py`** (python-pptx). In `PPTX <out.txt> <slides>` → đọc file `<out.txt>`. |
```

Trong "Xử lý lỗi công cụ" thêm dòng bảng:

```
| `ERROR NOPPTX` | `python -m pip install python-pptx` | `[ERROR] Cần python-pptx. Cài: pip install python-pptx` |
```

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/doc-analyzer/pptx_to_text.py .claude/skills/doc-analyzer/tests/test_pptx_to_text.py .claude/skills/doc-analyzer/SKILL.md
git commit -m "feat(doc-analyzer): add pptx to text conversion"
```

---

### Task 2: exercise-generator — mở rộng renderer (answer_alts, grammar_note, writing_prompt, render_study)

**Files:**
- Modify: `.claude/skills/exercise-generator/worksheet/build_worksheet.py`
- Create: `.claude/skills/exercise-generator/worksheet/tests/test_lesson_blocks.py`
- Modify: `.claude/skills/exercise-generator/worksheet/schema.md` (tài liệu 2 block mới + `answer_alts`)

**Interfaces:**
- Consumes: lớp `WorksheetBuilder(spec)` sẵn có.
- Produces:
  - `WorksheetBuilder.render_study(header_text="...") -> Document` — 1 doc gộp, hiện đáp án (mode "answers"), dùng cho lesson-prep.
  - Block type mới: `grammar_note` `{type,title,instructions?,points:[{pattern,explain?,example?}]}`; `writing_prompt` `{type,title,instructions?,items:[{prompt,kind?,outline?:[str]}]}`.
  - `dich_dat_cau`/`sap_xep` item hỗ trợ thêm `answer_alts:[str]` (in dưới nhãn "Phương án khác").

- [ ] **Step 1: Write the failing test**

Tạo `.claude/skills/exercise-generator/worksheet/tests/test_lesson_blocks.py`:

```python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from docx import Document

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from build_worksheet import WorksheetBuilder  # noqa: E402


def _text(doc):
    return "\n".join(p.text for p in doc.paragraphs)


def test_render_study_grammar_and_writing():
    spec = {
        "meta": {"lesson": "Buổi 5: tính cách"},
        "blocks": [
            {"type": "grammar_note", "title": "Ngữ pháp 固然",
             "points": [{"pattern": "固然…但是…",
                         "explain": "thừa nhận A nhấn mạnh B",
                         "example": "他固然聪明，但是不努力。"}]},
            {"type": "dich_dat_cau", "title": "Đặt câu",
             "items": [{"prompt": "Đặt câu với 尴尬",
                        "answer": "那个场面很尴尬。",
                        "answer_plus": "当时的气氛特别尴尬，大家都不说话。",
                        "answer_alts": ["我觉得有点尴尬。", "他尴尬地笑了笑。"],
                        "src": "AI"}]},
            {"type": "writing_prompt", "title": "Bài viết",
             "items": [{"prompt": "Tả một người bạn", "kind": "viết",
                        "outline": ["Mở: giới thiệu", "Thân: tính cách", "Kết: cảm nghĩ"]}]},
        ],
    }
    doc = WorksheetBuilder(spec).render_study("BÀI TẬP CHUẨN BỊ — Buổi 5")
    t = _text(doc)
    assert "BÀI TẬP CHUẨN BỊ — Buổi 5" in t
    assert "固然…但是…" in t
    assert "他固然聪明，但是不努力。" in t
    assert "那个场面很尴尬。" in t            # đáp án chuẩn
    assert "当时的气氛特别尴尬" in t           # nâng cao
    assert "他尴尬地笑了笑。" in t             # answer_alts
    assert "[AI]" in t                        # nhãn nguồn
    assert "Tả một người bạn" in t
    assert "Thân: tính cách" in t             # dàn ý
```

- [ ] **Step 2: Run test to verify it fails**

Run: `$PY -m pytest .claude/skills/exercise-generator/worksheet/tests/test_lesson_blocks.py -v`
Expected: FAIL (`render_study` / `_ans_grammar_note` chưa có → AttributeError/ValueError).

- [ ] **Step 3: Write minimal implementation**

Trong `build_worksheet.py`, sửa `_two_level_answer` để nhận `alts` và in thêm; cập nhật 2 caller; thêm `grammar_note`/`writing_prompt`/`render_study`.

3a. Đổi chữ ký + thân `_two_level_answer` (thêm tham số `alts=None` và khối in cuối):

```python
    def _two_level_answer(self, doc, n, standard, advanced=None, src=None,
                          alts=None, std_label="Chuẩn (đủ điểm)",
                          adv_label="Nâng cao (điểm cao)"):
        """Đáp án tự luận 2 cấp + (tùy chọn) các phương án khác (alts)."""
        p = doc.add_paragraph()
        self._run(p, "%d) " % n, 12, color="accent", bold=True)
        self._run(p, std_label + ": ", 11, color="muted", bold=True)
        self._run(p, standard, 14, cjk=True)
        if src:
            self._run(p, "  [%s]" % src, 10, color="muted", italic=True)
        if advanced:
            ap = doc.add_paragraph()
            ap.paragraph_format.left_indent = Pt(18)
            self._run(ap, adv_label + ": ", 11, color="accent", bold=True)
            self._run(ap, advanced, 13, cjk=True)
        for alt in (alts or []):
            altp = doc.add_paragraph()
            altp.paragraph_format.left_indent = Pt(18)
            self._run(altp, "Phương án khác: ", 11, color="muted", bold=True)
            self._run(altp, alt, 13, cjk=True)
```

3b. Trong `_ans_sap_xep` và `_ans_dich_dat_cau`, truyền `alts=it.get("answer_alts")`:

```python
    def _ans_sap_xep(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Sắp xếp câu"))
        for n, it in enumerate(block.get("items", []), start=1):
            self._two_level_answer(doc, n, it.get("answer", ""),
                                   it.get("answer_plus"), it.get("src"),
                                   alts=it.get("answer_alts"))

    def _ans_dich_dat_cau(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Dịch / Đặt câu"))
        for n, it in enumerate(block.get("items", []), start=1):
            self._two_level_answer(doc, n, it.get("answer", ""),
                                   it.get("answer_plus"), it.get("src"),
                                   alts=it.get("answer_alts"))
```

3c. Thêm 2 block mới + `render_study` (đặt trong lớp `WorksheetBuilder`, ví dụ ngay trước `def docx_to_pdf` — tức cuối phần method của lớp):

```python
    # -- grammar_note (giải thích ngữ pháp) -------------------------------
    def _grammar_note(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Ngữ pháp"),
                           block.get("instructions"))
        for pt in block.get("points", []):
            p = doc.add_paragraph()
            self._run(p, "• ", 12, color="accent", bold=True)
            self._run(p, pt.get("pattern", ""), 13, color="ink", bold=True,
                      cjk=True)
            if pt.get("explain"):
                ep = doc.add_paragraph()
                ep.paragraph_format.left_indent = Pt(18)
                self._run(ep, pt["explain"], 12, color="ink")
            if pt.get("example"):
                xp = doc.add_paragraph()
                xp.paragraph_format.left_indent = Pt(18)
                self._run(xp, "Vd: ", 11, color="muted", bold=True)
                self._run(xp, pt["example"], 12, cjk=True)

    _ws_grammar_note = _grammar_note
    _ans_grammar_note = _grammar_note

    # -- writing_prompt (đề viết/HSKK + dàn ý) ----------------------------
    def _writing_prompt(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Bài viết / HSKK"),
                           block.get("instructions"))
        for n, it in enumerate(block.get("items", []), start=1):
            p = doc.add_paragraph()
            self._run(p, "%d) " % n, 12, color="accent", bold=True)
            if it.get("kind"):
                self._run(p, "[%s] " % it["kind"], 11, color="muted", bold=True)
            self._run(p, it.get("prompt", ""), 13, cjk=True)
            for step in it.get("outline", []):
                sp = doc.add_paragraph()
                sp.paragraph_format.left_indent = Pt(18)
                self._run(sp, "– ", 12, color="muted")
                self._run(sp, step, 12, cjk=True)

    _ws_writing_prompt = _writing_prompt
    _ans_writing_prompt = _writing_prompt

    # -- render_study: 1 doc gộp có đáp án (cho lesson-prep) ---------------
    def render_study(self, header_text="BÀI TẬP CHUẨN BỊ"):
        doc = Document()
        p = doc.add_paragraph()
        self._run(p, header_text, 13, color="muted", bold=True)
        return self._render(doc, "answers")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `$PY -m pytest .claude/skills/exercise-generator/worksheet/tests/ -v`
Expected: PASS (test cũ + `test_lesson_blocks.py` đều xanh — không phá regression).

- [ ] **Step 5: Update schema.md**

Thêm vào `worksheet/schema.md`, mục "Các block":

```
- `grammar_note`: `{ "type":"grammar_note", "title", "instructions"?,
  "points":[{"pattern","explain"?,"example"?}] }` — hộp giải thích ngữ pháp (chỉ hiển thị).
- `writing_prompt`: `{ "type":"writing_prompt", "title", "instructions"?,
  "items":[{"prompt","kind"?:"viết|HSKK","outline"?:[str]}] }` — đề viết/HSKK + dàn ý.
```

Và bổ sung dòng vào mục "Đáp án 2 cấp": `dich_dat_cau`/`sap_xep` có thêm field tùy chọn `answer_alts:[str]` — in dưới nhãn "Phương án khác" (dùng cho lesson-prep khi muốn ~3 phương án). Ghi chú: `render_study()` xuất 1 doc gộp (đề + đáp án), khác luồng worksheet/dapan của exercise-generator.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/exercise-generator/worksheet/build_worksheet.py .claude/skills/exercise-generator/worksheet/tests/test_lesson_blocks.py .claude/skills/exercise-generator/worksheet/schema.md
git commit -m "feat(exercise-generator): grammar_note, writing_prompt, answer_alts, render_study"
```

---

### Task 3: lesson-prep — append_tier_a.py

**Files:**
- Create: `.claude/skills/lesson-prep/scripts/append_tier_a.py`
- Create: `.claude/skills/lesson-prep/tests/conftest.py`
- Create: `.claude/skills/lesson-prep/tests/test_append_tier_a.py`

**Interfaces:**
- Produces:
  - `append_words(payload: dict, vocab_dir: str|Path) -> int` — append từ mới vào `<vocab_dir>/tier-a.md`, dedup theo 生词 trên tier-a/b/c.md, trả số từ đã thêm.
  - CLI `python append_tier_a.py <vocab_payload.json>` (chạy từ gốc repo; dùng `knowledge/vocabulary`).
- Consumes: `vocab_payload.json` `{ "bai": int, "words":[{"w","pinyin","desc","vi","ex"}] }`.

- [ ] **Step 1: Write conftest + failing test**

Tạo `.claude/skills/lesson-prep/tests/conftest.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
```

Tạo `.claude/skills/lesson-prep/tests/test_append_tier_a.py`:

```python
# -*- coding: utf-8 -*-
from pathlib import Path
from append_tier_a import append_words

TIER_A_SEED = """# Tier A

## 固然
- Pinyin: gùrán
- Nghĩa: cố nhiên
- Activation: D

---

_Thêm từ mới theo format trên._
"""


def _setup(tmp_path):
    d = tmp_path / "vocabulary"
    d.mkdir()
    (d / "tier-a.md").write_text(TIER_A_SEED, encoding="utf-8")
    return d


def test_append_new_word(tmp_path):
    d = _setup(tmp_path)
    payload = {"bai": 5, "words": [
        {"w": "尴尬", "pinyin": "gāngà", "vi": "bối rối", "desc": "", "ex": ""}]}
    n = append_words(payload, d)
    assert n == 1
    text = (d / "tier-a.md").read_text(encoding="utf-8")
    assert "## 尴尬" in text
    assert "Activation: D" in text.split("## 尴尬")[1]
    # entry chèn TRƯỚC footer
    assert text.index("## 尴尬") < text.index("_Thêm từ mới")


def test_dedup_existing(tmp_path):
    d = _setup(tmp_path)
    payload = {"bai": 5, "words": [
        {"w": "固然", "pinyin": "gùrán", "vi": "x", "desc": "", "ex": ""},
        {"w": "尴尬", "pinyin": "gāngà", "vi": "bối rối", "desc": "", "ex": ""}]}
    n = append_words(payload, d)
    assert n == 1  # 固然 bị bỏ vì đã có
    assert (d / "tier-a.md").read_text(encoding="utf-8").count("## 固然") == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `$PY -m pytest .claude/skills/lesson-prep/tests/test_append_tier_a.py -v`
Expected: FAIL (`No module named append_tier_a`).

- [ ] **Step 3: Write minimal implementation**

Tạo `.claude/skills/lesson-prep/scripts/append_tier_a.py`:

```python
# -*- coding: utf-8 -*-
"""append_tier_a.py — append từ mới (Activation: D) vào knowledge/vocabulary/tier-a.md.

Append-only, dedup theo 生词 trên tier-a/b/c.md. Không sửa entry cũ.
Chạy từ gốc repo:  python append_tier_a.py <vocab_payload.json>
"""
import sys, json, re
from pathlib import Path

TIER_FILES = ["tier-a.md", "tier-b.md", "tier-c.md"]
FOOTER_PREFIX = "_Thêm từ mới"

ENTRY = """## {w}
- Pinyin: {pinyin}
- Nghĩa: {vi}
- Usage:
  - Seen: 0
  - Speaking: 0
  - Writing: 0
- Confidence: 0%
- Activation: D
- Last Studied: —

---

"""


def existing_words(vocab_dir):
    vocab_dir = Path(vocab_dir)
    words = set()
    for fn in TIER_FILES:
        p = vocab_dir / fn
        if p.exists():
            for m in re.finditer(r"^##\s+(.+?)\s*$",
                                 p.read_text(encoding="utf-8"), re.M):
                words.add(m.group(1).strip())
    return words


def append_words(payload, vocab_dir):
    vocab_dir = Path(vocab_dir)
    have = existing_words(vocab_dir)
    seen, entries = set(), []
    for it in payload.get("words", []):
        w = (it.get("w") or "").strip()
        if not w or w in have or w in seen:
            continue
        seen.add(w)
        entries.append(ENTRY.format(w=w, pinyin=it.get("pinyin", ""),
                                    vi=it.get("vi", "")))
    if not entries:
        return 0
    tier_a = vocab_dir / "tier-a.md"
    text = tier_a.read_text(encoding="utf-8")
    block = "".join(entries)
    lines = text.splitlines(keepends=True)
    idx = next((i for i, ln in enumerate(lines)
                if ln.lstrip().startswith(FOOTER_PREFIX)), None)
    if idx is not None:
        new_text = "".join(lines[:idx]) + block + "".join(lines[idx:])
    else:
        sep = "" if text.endswith("\n") else "\n"
        new_text = text + sep + block
    tier_a.write_text(new_text, encoding="utf-8")
    return len(entries)


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    if len(argv) != 2:
        print("Usage: python append_tier_a.py <vocab_payload.json>",
              file=sys.stderr); return 2
    payload = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    n = append_words(payload, Path("knowledge") / "vocabulary")
    print("append_tier_a: +%d từ mới -> tier-a.md" % n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `$PY -m pytest .claude/skills/lesson-prep/tests/test_append_tier_a.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/lesson-prep/scripts/append_tier_a.py .claude/skills/lesson-prep/tests/conftest.py .claude/skills/lesson-prep/tests/test_append_tier_a.py
git commit -m "feat(lesson-prep): append new words to tier-a.md (dedup, Activation D)"
```

---

### Task 4: lesson-prep — append_xlsx.py

**Files:**
- Create: `.claude/skills/lesson-prep/scripts/append_xlsx.py`
- Create: `.claude/skills/lesson-prep/tests/test_append_xlsx.py`

**Interfaces:**
- Produces:
  - `append_rows(payload: dict, xlsx_path: str|Path) -> int` — append từ mới vào sheet 'Từ vựng', dedup theo 生词, trả số dòng thêm.
  - CLI `python append_xlsx.py <vocab_payload.json> [xlsx]` (mặc định `raw/Từ vựng.xlsx`).
- Consumes: cùng `vocab_payload.json` như Task 3. Cột ghi: `[Bài N, w, pinyin, desc, vi, ex, "", ""]`.

- [ ] **Step 1: Write the failing test**

Tạo `.claude/skills/lesson-prep/tests/test_append_xlsx.py`:

```python
# -*- coding: utf-8 -*-
import openpyxl
from append_xlsx import append_rows

HEADER = ["Bài", "生词", "Pinyin", "描述", "意义", "例如", "复习", "检查"]


def _make_xlsx(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Từ vựng"
    ws.append(HEADER)
    ws.append(["Bài 1", "已经", "yǐjīng", "", "đã", "我已经吃了。", "", ""])
    wb.save(str(path))


def test_append_new_row(tmp_path):
    xlsx = tmp_path / "tv.xlsx"
    _make_xlsx(xlsx)
    payload = {"bai": 5, "words": [
        {"w": "尴尬", "pinyin": "gāngà", "desc": "不好意思", "vi": "bối rối",
         "ex": "很尴尬。"}]}
    n = append_rows(payload, xlsx)
    assert n == 1
    wb = openpyxl.load_workbook(str(xlsx))
    ws = wb["Từ vựng"]
    rows = list(ws.iter_rows(values_only=True))
    last = rows[-1]
    assert last[0] == "Bài 5" and last[1] == "尴尬" and last[2] == "gāngà"
    assert last[4] == "bối rối"


def test_dedup_existing(tmp_path):
    xlsx = tmp_path / "tv.xlsx"
    _make_xlsx(xlsx)
    payload = {"bai": 2, "words": [
        {"w": "已经", "pinyin": "yǐjīng", "desc": "", "vi": "đã", "ex": ""}]}
    n = append_rows(payload, xlsx)
    assert n == 0  # 已经 đã có
```

- [ ] **Step 2: Run test to verify it fails**

Run: `$PY -m pytest .claude/skills/lesson-prep/tests/test_append_xlsx.py -v`
Expected: FAIL (`No module named append_xlsx`).

- [ ] **Step 3: Write minimal implementation**

Tạo `.claude/skills/lesson-prep/scripts/append_xlsx.py`:

```python
# -*- coding: utf-8 -*-
"""append_xlsx.py — append từ mới vào raw/Từ vựng.xlsx (sheet 'Từ vựng').

Dedup theo 生词. Cột: Bài, 生词, Pinyin, 描述, 意义, 例如, 复习, 检查.
Chạy:  python append_xlsx.py <vocab_payload.json> [xlsx]
"""
import sys, json
from pathlib import Path
import openpyxl


def _sheet(wb, name):
    for s in wb.sheetnames:
        if s.strip().lower() == name.lower():
            return wb[s]
    return wb[wb.sheetnames[0]]


def append_rows(payload, xlsx_path):
    xlsx_path = str(xlsx_path)
    wb = openpyxl.load_workbook(xlsx_path)
    ws = _sheet(wb, "Từ vựng")
    have = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        if len(row) > 1 and row[1]:
            have.add(str(row[1]).strip())
    bai = payload.get("bai")
    added = 0
    for it in payload.get("words", []):
        w = (it.get("w") or "").strip()
        if not w or w in have:
            continue
        have.add(w)
        ws.append(["Bài %s" % bai if bai is not None else "",
                   w, it.get("pinyin", ""), it.get("desc", ""),
                   it.get("vi", ""), it.get("ex", ""), "", ""])
        added += 1
    if added:
        wb.save(xlsx_path)
    return added


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    if len(argv) < 2:
        print("Usage: python append_xlsx.py <vocab_payload.json> [xlsx]",
              file=sys.stderr); return 2
    payload = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    xlsx = argv[2] if len(argv) > 2 else "raw/Từ vựng.xlsx"
    n = append_rows(payload, xlsx)
    print("append_xlsx: +%d từ -> %s (sheet 'Từ vựng')" % (n, xlsx))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `$PY -m pytest .claude/skills/lesson-prep/tests/test_append_xlsx.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/lesson-prep/scripts/append_xlsx.py .claude/skills/lesson-prep/tests/test_append_xlsx.py
git commit -m "feat(lesson-prep): append new words to Từ vựng.xlsx (dedup)"
```

---

### Task 5: lesson-prep — render_lesson_docx.py (driver mỏng)

**Files:**
- Create: `.claude/skills/lesson-prep/scripts/render_lesson_docx.py`
- Create: `.claude/skills/lesson-prep/tests/test_render_lesson_docx.py`

**Interfaces:**
- Consumes: `WorksheetBuilder.render_study` (Task 2); `exercise_payload.json` theo schema baitap (có 2 block mới).
- Produces: CLI `python render_lesson_docx.py <exercise_payload.json> <out.docx>` → 1 file `.docx` gộp (đề + đáp án + ngữ pháp + đề viết/dàn ý). In `OK: lesson docx -> <path> (<n> block)`.

- [ ] **Step 1: Write the failing test**

Tạo `.claude/skills/lesson-prep/tests/test_render_lesson_docx.py`:

```python
# -*- coding: utf-8 -*-
import json, sys, subprocess
from pathlib import Path
from docx import Document

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "render_lesson_docx.py"
PY = sys.executable


def test_render_lesson_docx(tmp_path):
    spec = {
        "meta": {"lesson": "Buổi 5: tính cách"},
        "blocks": [
            {"type": "dien_cho_trong", "title": "Điền", "word_bank": ["尴尬"],
             "items": [{"q": "那个场面很{}。", "answer": "尴尬", "src": "slide"}]},
            {"type": "grammar_note", "title": "Ngữ pháp",
             "points": [{"pattern": "固然…但是…", "explain": "nhượng bộ"}]},
            {"type": "writing_prompt", "title": "Viết",
             "items": [{"prompt": "Tả bạn thân", "kind": "viết",
                        "outline": ["Mở bài", "Thân bài"]}]},
        ],
    }
    src = tmp_path / "exercise_payload.json"
    src.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "baitap.docx"
    r = subprocess.run([PY, str(SCRIPT), str(src), str(out)],
                       capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    assert out.exists()
    t = "\n".join(p.text for p in Document(str(out)).paragraphs)
    assert "Buổi 5: tính cách" in t
    assert "尴尬" in t and "[slide]" in t
    assert "固然…但是…" in t
    assert "Tả bạn thân" in t and "Thân bài" in t
```

- [ ] **Step 2: Run test to verify it fails**

Run: `$PY -m pytest .claude/skills/lesson-prep/tests/test_render_lesson_docx.py -v`
Expected: FAIL (script chưa tồn tại).

- [ ] **Step 3: Write minimal implementation**

Tạo `.claude/skills/lesson-prep/scripts/render_lesson_docx.py`:

```python
# -*- coding: utf-8 -*-
"""render_lesson_docx.py — render exercise_payload.json thành 1 .docx gộp (đề+đáp án).

Tái dùng WorksheetBuilder của exercise-generator (render_study).
Chạy:  python render_lesson_docx.py <exercise_payload.json> <out.docx>
"""
import sys, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EG = HERE.parent.parent / "exercise-generator" / "worksheet"
sys.path.insert(0, str(EG))
from build_worksheet import WorksheetBuilder  # noqa: E402


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    if len(argv) != 3:
        print("Usage: python render_lesson_docx.py <exercise_payload.json> <out.docx>",
              file=sys.stderr); return 2
    spec = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    header = spec.get("meta", {}).get("lesson", "BÀI TẬP CHUẨN BỊ")
    out = Path(argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    WorksheetBuilder(spec).render_study(header).save(str(out))
    print("OK: lesson docx -> %s (%d block)" % (out, len(spec.get("blocks", []))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

- [ ] **Step 4: Run full lesson-prep test suite**

Run: `$PY -m pytest .claude/skills/lesson-prep/tests/ -v`
Expected: PASS (append_tier_a + append_xlsx + render_lesson_docx đều xanh).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/lesson-prep/scripts/render_lesson_docx.py .claude/skills/lesson-prep/tests/test_render_lesson_docx.py
git commit -m "feat(lesson-prep): render combined study docx via exercise-generator builder"
```

---

### Task 6: lesson-prep — SKILL.md (bộ não điều phối)

**Files:**
- Create: `.claude/skills/lesson-prep/SKILL.md`

**Interfaces:**
- Consumes: mọi script Task 1–5.
- Produces: tài liệu hướng dẫn Claude chạy luồng ①–④. Không có unit test (là instruction doc) — verify bằng checklist ở Step 2.

- [ ] **Step 1: Write SKILL.md**

Tạo `.claude/skills/lesson-prep/SKILL.md` với nội dung:

````markdown
---
name: lesson-prep
description: >
  Bóc tách file .pptx bài khóa HSK6 của cô → (1) nạp từ vựng vào tier-a + trang học
  vocab-study, (2) xuất bài tập + bài viết/HSKK ra 1 file .docx để copy sang Google Docs.
  Use when user muốn "chuẩn bị bài", "bóc bài khóa", "lesson-prep", "chuẩn bị buổi X".
author: Chinese Learning OS
---

# lesson-prep — Chuẩn bị bài khóa từ pptx

> Chuẩn bị cho việc HỌC HSK6 của user. KHÔNG phải soạn bài cho học viên HSK1-3
> (đó là exercise-generator/teaching-coach). Gọi trực tiếp script của skill khác,
> KHÔNG invoke skill khác (One Request = One Skill).

## Input
File `.pptx` bài khóa của cô (mặc định tìm trong `raw/`, chọn file mới nhất nếu nhiều).

## Biến môi trường
```
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
DA=".claude/skills/doc-analyzer"
VS=".claude/skills/vocab-study/scripts"
LP=".claude/skills/lesson-prep/scripts"
```

## Luồng

### ① Convert pptx → text
```
"$PY" "$DA/pptx_to_text.py" "raw/<file>.pptx"
```
→ đọc `raw/<file>.pptx.txt` (mỗi slide 1 khối [TITLE]/[BODY]/[TABLE]/[NOTES]).

### ② Hiểu & phân loại (Claude tự đọc file .txt)
Xác định `buoiX_<chude>` (suy từ tên file/tiêu đề slide; không rõ → hỏi user 1 câu).
Tạo `output/hsk6/buoiX_<chude>/lesson-prep/`.

Phân loại từng slide:
- **Slide "từ vựng"** = từ có 释义 + ví dụ đi kèm → nhặt vào `vocab_payload.json`.
  KHÔNG đào từ trong đoạn bài đọc; chỉ lấy từ ở slide có giải thích + ví dụ.
- **Slide "bài tập/bài đọc"** (đục lỗ, đặt câu, sắp xếp, đoạn đọc dùng lại từ mới)
  → `exercise_payload.json`. Từ mới ở đây chỉ là ngữ liệu, KHÔNG nhặt làm vocab.
- **Slide "bài viết/HSKK"** → block `writing_prompt` trong `exercise_payload.json`.

**`vocab_payload.json`:** `{ "bai": <N>, "words":[{"w","pinyin","desc","vi","ex"}] }`
- `desc` = 释义 tiếng Trung ĐƠN GIẢN (học sinh tiểu học hiểu, KHÔNG đồng nghĩa).
- `pinyin` ưu tiên lấy từ slide; `ex` ưu tiên câu ví dụ từ slide (tự nhiên).

**`exercise_payload.json`:** theo `.claude/skills/exercise-generator/worksheet/schema.md`
(gồm block mới `grammar_note`, `writing_prompt`; item tự luận có thể thêm `answer_alts`).
- Trích đề từ slide → block phù hợp (`dien_cho_trong`, `sap_xep`, `dich_dat_cau`, `doc_hieu`).
- Slide đã có đáp án → giữ, gắn `src:"slide"`. Đáp án AI tự giải → `src:"AI"`.
- Câu hoàn thành/đặt câu → cung cấp ~3 phương án (`answer` + `answer_plus` + `answer_alts`).
- Kèm `grammar_note` giải thích điểm ngữ pháp trọng tâm.
- Phong cách đáp án: tự nhiên, khẩu ngữ, đơn giản nhưng điểm cao.

### ③ Kiểm tra đúng đắn (BẮT BUỘC trước khi ghi/render)
Rà lại từng đáp án `src:"AI"`: đúng ngữ pháp, đúng nghĩa, pinyin chuẩn. Sửa nếu sai.
(Nâng cao tùy chọn: nếu user bật orchestration, dùng workflow adversarial verify.)

### ④ Xuất
Vocab:
```
"$PY" "$LP/append_tier_a.py" "output/hsk6/buoiX_<chude>/lesson-prep/vocab_payload.json"
"$PY" "$LP/append_xlsx.py"   "output/hsk6/buoiX_<chude>/lesson-prep/vocab_payload.json"
# rồi chạy pipeline vocab-study (tối thiểu 1→3→5; thêm 2/4 nếu có chữ/từ mới):
"$PY" "$VS/extract_xlsx.py"
"$PY" "$VS/build_md.py"
"$PY" "$VS/render_html.py"
```
→ `output/study/hsk6/tu-vung.html` (từ mới hiện trạng thái D vì đọc tier-a).

Bài tập/viết:
```
"$PY" "$LP/render_lesson_docx.py" \
  "output/hsk6/buoiX_<chude>/lesson-prep/exercise_payload.json" \
  "output/hsk6/buoiX_<chude>/lesson-prep/baitap.docx"
```

## Báo kết quả
Báo user: số từ mới thêm (tier-a + xlsx), đường dẫn `tu-vung.html` và `baitap.docx`.

## Nguyên tắc
- Chỉ đọc `memory/*`. Ghi tier-a.md **append-only** (dedup, Activation D) — không sửa entry cũ.
- Không sinh audio. Không tự promote/demote tier (việc của learning-strategist).
- Chỉ xử lý pptx trong V1.

## Phụ thuộc
`python-pptx`, `python-docx`, `openpyxl`, `pypinyin` (đều đã có).
````

- [ ] **Step 2: Verify SKILL.md (checklist thủ công)**

Đọc lại và xác nhận:
- Có frontmatter `name: lesson-prep` + `description` chứa trigger ("chuẩn bị bài", "bóc bài khóa", "lesson-prep").
- Mọi đường dẫn script khớp Task 1–5 (`pptx_to_text.py`, `append_tier_a.py`, `append_xlsx.py`, `render_lesson_docx.py`).
- Không có placeholder TBD/TODO.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/lesson-prep/SKILL.md
git commit -m "feat(lesson-prep): add SKILL.md orchestration doc"
```

---

### Task 7: Governance — cập nhật CLAUDE.md

**Files:**
- Modify: `CLAUDE.md` (§3 routing, §6 ownership, §7 catalog)

**Interfaces:**
- Consumes: —. Produces: routing + ownership cho lesson-prep. Verify bằng đọc lại.

- [ ] **Step 1: §3 — thêm hard route**

Trong "Hard Route", thêm dòng:
```
- `/lesson-prep` → invoke Skill("lesson-prep")
```

- [ ] **Step 2: §3 — thêm soft route**

Thêm rule (sau 4d):
```
4e. "chuẩn bị bài" / "bóc bài khóa" / "lesson-prep" / "chuẩn bị buổi X" / "bài khóa của cô" → lesson-prep
```

- [ ] **Step 3: §6 — thêm ownership**

Thêm các dòng vào bảng §6 State Ownership:
```
| knowledge/vocabulary/tier-a.md | User / Learning Strategist / Lesson Prep (append-only, chỉ thêm từ mới ⚪→Activation D) |
| raw/Từ vựng.xlsx | User / Lesson Prep (append dòng vocab mới) |
| output/hsk6/**/lesson-prep/ | Lesson Prep (vocab_payload.json, exercise_payload.json, baitap.docx) |
```
Ghi chú blockquote: lesson-prep chỉ **thêm** entry tier-a mới (dedup theo 生词), không sửa entry learning-strategist đang quản.

- [ ] **Step 4: §7 — cập nhật catalog**

Sửa dòng lesson-prep trong §7 (bỏ "(CHƯA làm)"):
```
- **lesson-prep** — Bóc tách pptx bài khóa HSK6: convert (doc-analyzer) → phân loại → nạp từ vựng (tier-a + vocab-study) + xuất bài tập/bài viết ra .docx. Kiểm tra đáp án AI trước khi xuất.
```

- [ ] **Step 5: Verify**

Đọc lại CLAUDE.md: §3 có hard+soft route lesson-prep; §6 có 3 dòng ownership mới; §7 mô tả cập nhật. Không mâu thuẫn quy tắc "memory/* User only" (lesson-prep KHÔNG ghi memory).

- [ ] **Step 6: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(CLAUDE): register lesson-prep routing + ownership"
```

---

### Task 8: End-to-end smoke test

**Files:**
- Create (tạm, xoá sau): `scratchpad` pptx mẫu — dùng thư mục scratchpad, KHÔNG commit.

**Interfaces:** Consumes toàn bộ luồng. Produces: xác nhận chạy thật ra `tu-vung.html` + `baitap.docx`.

- [ ] **Step 1: Tạo pptx mẫu**

```bash
$PY - <<'EOF'
from pptx import Presentation
from pptx.util import Inches
p = Presentation()
s = p.slides.add_slide(p.slide_layouts[1])
s.shapes.title.text = "生词"
s.placeholders[1].text = "尴尬 gāngà 释义：不好意思的感觉。例：那个场面很尴尬。"
s2 = p.slides.add_slide(p.slide_layouts[1])
s2.shapes.title.text = "练习：填空"
s2.placeholders[1].text = "那个场面很____。"
import os
os.makedirs("scratchpad", exist_ok=True)
p.save("scratchpad/mau.pptx")
print("saved scratchpad/mau.pptx")
EOF
```
(Chạy trong thư mục scratchpad của session; đường dẫn tuyệt đối theo môi trường.)

- [ ] **Step 2: Chạy convert + kiểm tra text**

Run: `$PY .claude/skills/doc-analyzer/pptx_to_text.py <scratchpad>/mau.pptx`
Expected: in `PPTX <...>.txt 2`; file .txt chứa `[TITLE] 生词` và `[TITLE] 练习：填空`.

- [ ] **Step 3: Dựng payload mẫu + chạy render**

Tạo `vocab_payload.json` `{"bai":99,"words":[{"w":"尴尬","pinyin":"gāngà","desc":"不好意思的感觉","vi":"bối rối","ex":"那个场面很尴尬。"}]}` và `exercise_payload.json` (1 block `dien_cho_trong` + 1 `grammar_note`) trong scratchpad, rồi:

Run:
```
$PY .claude/skills/lesson-prep/scripts/render_lesson_docx.py <scratchpad>/exercise_payload.json <scratchpad>/baitap.docx
```
Expected: `OK: lesson docx -> ... (2 block)`; mở `baitap.docx` thấy đề + đáp án + ngữ pháp.

- [ ] **Step 4: Kiểm tra append (dùng bản sao, KHÔNG đụng file thật)**

Copy `raw/Từ vựng.xlsx` → `<scratchpad>/tv.xlsx`; copy `knowledge/vocabulary/tier-a.md` → `<scratchpad>/vocabulary/tier-a.md`. Chạy `append_rows`/`append_words` trỏ vào bản sao (qua `python -c`), xác nhận +1 từ, dedup lần 2 = 0.

- [ ] **Step 5: Dọn scratchpad + báo cáo**

Xoá file tạm trong scratchpad. Báo user: luồng chạy thông, không commit file smoke.

---

## Self-Review

**1. Spec coverage:**
- §3 convert pptx → **Task 1** ✓
- §4 hiểu/phân loại (vocab/bài tập/viết), 2 payload → **Task 6 SKILL.md** (Claude) ✓; schema block mới → **Task 2** ✓
- §5 vocab: append tier-a (Activation D, dedup) → **Task 3** ✓; append xlsx → **Task 4** ✓; pipeline vocab-study → **Task 6** (gọi script có sẵn) ✓
- §6 render .docx gộp, 2 block mới, answer_alts, src → **Task 2 + Task 5** ✓
- §7 kiểm tra đáp án → **Task 6 ③** ✓
- §8 governance CLAUDE.md → **Task 7** ✓
- Xác định buoiX_<chude> → **Task 6 ②** ✓

**2. Placeholder scan:** không có TBD/TODO/"handle edge cases"; mọi step code có code thật. ✓

**3. Type consistency:** `vocab_payload` `{bai, words:[{w,pinyin,desc,vi,ex}]}` dùng nhất quán Task 3/4/6. `render_study(header_text)` định nghĩa Task 2, gọi Task 5. Block `grammar_note.points[].{pattern,explain,example}`, `writing_prompt.items[].{prompt,kind,outline}`, `answer_alts:[str]` khớp giữa Task 2 (định nghĩa/test) và Task 5/6 (dùng). `append_words`/`append_rows` tên khớp test. ✓
