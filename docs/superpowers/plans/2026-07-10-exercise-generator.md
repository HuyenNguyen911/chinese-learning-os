# Exercise Generator Skill — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `exercise-generator` skill that turns a lesson's content into interactive HSK1-3 exercise worksheets (`.docx` + answer key), covering reading/writing/listening/speaking, rendered by a new data-driven Python renderer.

**Architecture:** A two-phase skill mirroring `teaching-coach`. Phase A (prose in `SKILL.md`) composes exercises into a `baitap-buoiX.json` file, drawing from an HSK exam bank. Phase B is a Python renderer `build_worksheet.py` that reads that JSON and emits a student `worksheet.docx` and a separate `dapan.docx` (answer key + listening scripts). Listening/speaking audio (`edge-tts`) is deferred behind a user confirm-gate. The renderer copies `build_deck.py`'s CJK-font technique and per-type dispatch style.

**Tech Stack:** Python 3.12, `python-docx` (renderer), `qrcode` (optional listening links), `pytest` (tests). `edge-tts` installed only when the user opts into audio. `python-pptx`/`Pillow` already present (reused for optional projection deck via existing `build_deck.py`).

## Global Constraints

- Python interpreter (all commands): `C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe`
- CJK font: `Microsoft YaHei`, applied to Chinese runs via `w:eastAsia` (mirror `build_deck.py._set_run`).
- Theme colors reuse `build_deck.py` `DEFAULT_THEME` values (accent `C0392B`, ink `1F2933`, muted `6B7683`, band `F4F5F7`, accent_soft `F7E4E1`, bg `FFFFFF`).
- **`worksheet.docx` MUST NEVER contain answers or 听力文本 (listening scripts).** Answers and scripts live only in `dapan.docx`.
- Every non-真题 (model-generated) exercise item is labeled `[phỏng theo 真题]`; items pulled from the exam bank cite their source tag.
- Difficulty mix per skill block: ~70% at the lesson's HSK level, ~30% one level higher.
- Skill only **reads** `memory/*` (per CLAUDE.md §4). It writes outputs under `output/hskN/baitap/` and appends one line to `state/session-log.md`.
- Audio (`edge-tts`) is generated ONLY after the user confirms the listening/speaking script. The skill never auto-installs `edge-tts` nor auto-synthesizes MP3.
- All JSON/text files are UTF-8. Console debug prints of Chinese require `PYTHONIOENCODING=utf-8`.
- Renderer CLI: `python build_worksheet.py <baitap.json> <out_dir>` → writes `<out_dir>/worksheet.docx` and `<out_dir>/dapan.docx`.

---

## File Structure

```
.claude/skills/exercise-generator/
  SKILL.md                         # Task 14 — persona + 2-phase process + routing + seed/audio gates
  references/
    hsk-exam-format.md             # Task 15 — HSK1-3 + HSKK 初级 section structure & level boundaries
    exercise-types.md              # Task 15 — the 7 blocks, how to compose & grade
  worksheet/
    build_worksheet.py             # Tasks 2-12 — JSON → worksheet.docx + dapan.docx
    schema.md                      # Task 15 — baitap JSON schema
    example-baitap.json            # Task 13 — fixture covering all 7 blocks
    tests/
      test_build_worksheet.py      # Tasks 2-13 — pytest suite
knowledge/hsk-exam-bank/
  hsk1.md hsk2.md hsk3.md          # Task 16 — exam-bank scaffold (seeded later, gated)
  sources.md                       # Task 16 — source + date provenance template
CLAUDE.md                          # Task 16 — routing §3, state §6, catalog §7 updates
```

**One-block-one-renderer-pair.** Each exercise block type has a `_ws_<type>` (student) and `_ans_<type>` (answer-key) method. This keeps each block independently testable and reviewable.

---

## Task 1: Environment & skill scaffold

**Files:**
- Create: `.claude/skills/exercise-generator/worksheet/tests/` (dir)
- Create: `.claude/skills/exercise-generator/worksheet/tests/conftest.py`

**Interfaces:**
- Produces: an importable `build_worksheet` module location on `sys.path` for tests; installed `docx`, `qrcode`, `pytest`.

- [ ] **Step 1: Install dependencies**

Run:
```bash
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
"$PY" -m pip install python-docx qrcode pytest
```
Expected: ends with `Successfully installed ... python-docx-... qrcode-... pytest-...` (or "already satisfied").

- [ ] **Step 2: Verify imports**

Run:
```bash
"$PY" -c "import docx, qrcode, pytest; print('deps OK')"
```
Expected: `deps OK`

- [ ] **Step 3: Create the test conftest that puts the renderer on the path**

Create `.claude/skills/exercise-generator/worksheet/tests/conftest.py`:
```python
import sys
import pathlib

# Make build_worksheet.py importable from the tests without packaging.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/exercise-generator/worksheet/tests/conftest.py
git commit -m "chore(exercise-generator): scaffold + test path (python-docx, qrcode, pytest)"
```

---

## Task 2: Renderer core — spec loading, document shell, CJK run helper, dispatch

**Files:**
- Create: `.claude/skills/exercise-generator/worksheet/build_worksheet.py`
- Test: `.claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py`

**Interfaces:**
- Produces:
  - `class WorksheetBuilder(spec: dict)` with attrs `.meta` (`spec["meta"]`), `.theme` (DEFAULT_THEME merged with `spec.get("theme")`).
  - `WorksheetBuilder._rgb(key: str) -> RGBColor`
  - `WorksheetBuilder._run(p, text, size=12, color="ink", bold=False, italic=False, cjk=False) -> Run` — adds a run to paragraph `p`, sets size/color/bold/italic/font, and sets `w:eastAsia` to the CJK font when `cjk=True`.
  - `WorksheetBuilder._title_block(doc, text)` — H1-style lesson title paragraph (cjk).
  - `WorksheetBuilder._block_header(doc, idx, title, instructions=None)` — numbered block heading + optional italic instruction line.
  - `WorksheetBuilder.render_worksheet() -> docx.document.Document`
  - `WorksheetBuilder.render_answers() -> docx.document.Document`
  - Both iterate `spec["blocks"]` and dispatch to `_ws_<type>` / `_ans_<type>`; unknown type raises `ValueError`.

- [ ] **Step 1: Write the failing test**

Create `.claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py`:
```python
from docx.oxml.ns import qn
from build_worksheet import WorksheetBuilder


def _run_has_cjk_font(run, font="Microsoft YaHei"):
    rPr = run._element.rPr
    if rPr is None or rPr.rFonts is None:
        return False
    return rPr.rFonts.get(qn("w:eastAsia")) == font


def _all_text(doc):
    parts = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                parts.append(cell.text)
    return "\n".join(parts)


def test_core_renders_lesson_title_with_cjk():
    spec = {"meta": {"lesson": "Buổi 1: 会/想/能", "hsk": 1}, "blocks": []}
    doc = WorksheetBuilder(spec).render_worksheet()
    assert "Buổi 1" in _all_text(doc)
    # The title run carrying Chinese must declare the East-Asian font.
    title_runs = [r for p in doc.paragraphs for r in p.runs if "会" in r.text]
    assert title_runs and _run_has_cjk_font(title_runs[0])


def test_core_unknown_block_type_raises():
    spec = {"meta": {"lesson": "x", "hsk": 1}, "blocks": [{"type": "nope"}]}
    try:
        WorksheetBuilder(spec).render_worksheet()
    except ValueError as e:
        assert "nope" in str(e)
    else:
        raise AssertionError("expected ValueError for unknown block type")
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'build_worksheet'`.

- [ ] **Step 3: Write the minimal implementation**

Create `.claude/skills/exercise-generator/worksheet/build_worksheet.py`:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_worksheet.py — Data-driven renderer: baitap JSON -> worksheet.docx + dapan.docx.

Dùng bởi skill exercise-generator (Giai đoạn B). Nhận 1 file JSON mô tả bài tập
(danh sách block: noi / dien_cho_trong / doc_hieu / sap_xep / dich_dat_cau /
nghe / noi_hskk) và render ra:
  - worksheet.docx : bản cho học viên (KHÔNG có đáp án, KHÔNG có 听力文本)
  - dapan.docx     : đáp án + 听力文本 + gợi ý chấm

Chạy:
    python build_worksheet.py <baitap.json> <out_dir>

Cần: python-docx. Không cần internet lúc render.
"""

import json
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

DEFAULT_THEME = {
    "accent": "C0392B",
    "ink": "1F2933",
    "muted": "6B7683",
    "band": "F4F5F7",
    "accent_soft": "F7E4E1",
    "bg": "FFFFFF",
    "cjk_font": "Microsoft YaHei",
    "text_font": "Calibri",
}

BLANK = "＿＿＿＿"  # ô trống để học viên gõ (full-width để dễ thấy)


class WorksheetBuilder:
    def __init__(self, spec):
        self.spec = spec
        self.meta = spec.get("meta", {})
        self.theme = {**DEFAULT_THEME, **spec.get("theme", {})}

    # -- helpers -----------------------------------------------------------
    def _rgb(self, key):
        return RGBColor.from_string(self.theme[key])

    def _run(self, p, text, size=12, color="ink", bold=False, italic=False,
             cjk=False):
        run = p.add_run(text)
        f = run.font
        f.size = Pt(size)
        f.bold = bold
        f.italic = italic
        f.color.rgb = self._rgb(color)
        f.name = self.theme["cjk_font"] if cjk else self.theme["text_font"]
        if cjk:
            run._element.rPr.rFonts.set(qn("w:eastAsia"), self.theme["cjk_font"])
        return run

    def _title_block(self, doc, text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        self._run(p, text, 20, color="accent", bold=True, cjk=True)

    def _block_header(self, doc, idx, title, instructions=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        self._run(p, "%d. " % idx, 15, color="accent", bold=True)
        self._run(p, title, 15, color="ink", bold=True, cjk=True)
        if instructions:
            ip = doc.add_paragraph()
            self._run(ip, instructions, 11, color="muted", italic=True, cjk=True)

    # -- dispatch ----------------------------------------------------------
    def _render(self, doc, mode):
        prefix = "_ws_" if mode == "worksheet" else "_ans_"
        self._title_block(doc, self.meta.get("lesson", "Bài tập"))
        for i, block in enumerate(self.spec.get("blocks", []), start=1):
            btype = block.get("type", "")
            handler = getattr(self, prefix + btype, None)
            if handler is None:
                raise ValueError(
                    "Block #%d: type '%s' không hỗ trợ." % (i, btype))
            handler(doc, block, i)
        return doc

    def render_worksheet(self):
        return self._render(Document(), "worksheet")

    def render_answers(self):
        doc = Document()
        p = doc.add_paragraph()
        self._run(p, "ĐÁP ÁN — ", 13, color="muted", bold=True)
        self._run(p, "chỉ dành cho giáo viên", 13, color="muted", italic=True)
        return self._render(doc, "answers")


def main(argv):
    if len(argv) != 3:
        print("Usage: python build_worksheet.py <baitap.json> <out_dir>",
              file=sys.stderr)
        return 2
    src = Path(argv[1])
    out_dir = Path(argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    spec = json.loads(src.read_text(encoding="utf-8"))
    b = WorksheetBuilder(spec)
    b.render_worksheet().save(str(out_dir / "worksheet.docx"))
    b.render_answers().save(str(out_dir / "dapan.docx"))
    n = len(spec.get("blocks", []))
    print("OK: %d block -> %s/{worksheet,dapan}.docx" % (n, out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/exercise-generator/worksheet/build_worksheet.py .claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py
git commit -m "feat(exercise-generator): renderer core — doc shell, CJK run, dispatch"
```

---

## Task 3: `noi` block — matching (读, HSK 匹配)

**Files:**
- Modify: `.claude/skills/exercise-generator/worksheet/build_worksheet.py`
- Test: `.claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py`

**Block shape:** `{"type":"noi","title":str,"instructions":str,"pairs":[{"left":str,"right":str}, ...]}`
Worksheet shows a 2-column table: left column = shuffled Chinese items, right column = shuffled meanings with letters (A, B, C…); student writes the letter. Answer key shows the correct left→letter mapping.

**Interfaces:**
- Consumes: `WorksheetBuilder._run`, `_block_header`, `_rgb` (Task 2).
- Produces: `_ws_noi(doc, block, idx)`, `_ans_noi(doc, block, idx)`.

- [ ] **Step 1: Write the failing test**

Append to `test_build_worksheet.py`:
```python
NOI_BLOCK = {
    "type": "noi",
    "title": "Nối chữ với nghĩa",
    "instructions": "Viết chữ cái đúng vào ô.",
    "pairs": [
        {"left": "会", "right": "biết (kỹ năng)"},
        {"left": "想", "right": "muốn"},
        {"left": "能", "right": "có thể"},
    ],
}


def _spec(*blocks):
    return {"meta": {"lesson": "Buổi 1", "hsk": 1}, "blocks": list(blocks)}


def test_noi_worksheet_lists_all_left_items_and_no_direct_answer_pairing():
    doc = WorksheetBuilder(_spec(NOI_BLOCK)).render_worksheet()
    text = _all_text(doc)
    for hz in ("会", "想", "能"):
        assert hz in text
    # meanings are present (as a shuffled lettered bank), instruction shown
    assert "muốn" in text
    assert "Viết chữ cái đúng" in text


def test_noi_answer_key_shows_mapping():
    doc = WorksheetBuilder(_spec(NOI_BLOCK)).render_answers()
    text = _all_text(doc)
    # answer key pairs each character with its meaning
    assert "会" in text and "biết (kỹ năng)" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k noi -v
```
Expected: FAIL — `AttributeError`/`ValueError` (no `_ws_noi`).

- [ ] **Step 3: Write the implementation**

Add these methods to `WorksheetBuilder` (before `main`), plus a deterministic shuffle helper. Insert after `_block_header`:
```python
    def _fill_cell(self, cell, text, size=12, color="ink", bold=False,
                   cjk=False, italic=False):
        p = cell.paragraphs[0]
        self._run(p, text, size, color=color, bold=bold, italic=italic, cjk=cjk)

    @staticmethod
    def _rotate(seq, by):
        # Deterministic reorder so worksheet order != source order, no RNG.
        by = by % len(seq) if seq else 0
        return seq[by:] + seq[:by]
```

Add the block methods:
```python
    # -- noi (matching) ----------------------------------------------------
    def _ws_noi(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Nối"),
                           block.get("instructions"))
        pairs = block.get("pairs", [])
        rights = self._rotate(list(range(len(pairs))), 1)
        letters = [chr(ord("A") + i) for i in range(len(pairs))]
        table = doc.add_table(rows=len(pairs) + 1, cols=3)
        table.style = "Table Grid"
        hdr = table.rows[0].cells
        self._fill_cell(hdr[0], "汉字", 12, color="accent", bold=True, cjk=True)
        self._fill_cell(hdr[1], "Trả lời", 12, color="accent", bold=True)
        self._fill_cell(hdr[2], "Nghĩa", 12, color="accent", bold=True)
        for r, pair in enumerate(pairs, start=1):
            cells = table.rows[r].cells
            self._fill_cell(cells[0], pair.get("left", ""), 16, bold=True,
                            cjk=True)
            self._fill_cell(cells[1], BLANK, 12, color="muted")
            j = rights[r - 1]
            self._fill_cell(cells[2],
                            "%s. %s" % (letters[r - 1], pairs[j].get("right", "")),
                            12, cjk=True)

    def _ans_noi(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Nối"))
        pairs = block.get("pairs", [])
        rights = self._rotate(list(range(len(pairs))), 1)
        letters = [chr(ord("A") + i) for i in range(len(pairs))]
        pos = {j: letters[k] for k, j in enumerate(rights)}
        for i, pair in enumerate(pairs):
            p = doc.add_paragraph()
            self._run(p, pair.get("left", ""), 14, bold=True, cjk=True)
            self._run(p, "  → %s. " % pos[i], 12, color="accent", bold=True)
            self._run(p, pair.get("right", ""), 12, cjk=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k noi -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add -A .claude/skills/exercise-generator/worksheet
git commit -m "feat(exercise-generator): noi (matching) block renderer"
```

---

## Task 4: `dien_cho_trong` block — fill in the blank (读, HSK 选词填空)

**Files:**
- Modify: `.claude/skills/exercise-generator/worksheet/build_worksheet.py`
- Test: same test file.

**Block shape:** `{"type":"dien_cho_trong","title":str,"instructions":str,"word_bank":[str,...],"items":[{"q":str,"answer":str,"src":str?}, ...]}`
Each `q` contains a `{}` placeholder marking the blank. Worksheet renders the bank once, then each sentence with the blank replaced by `BLANK` — **never the answer**. Answer key renders each sentence with the answer filled and shown in accent.

**Interfaces:**
- Consumes: `_run`, `_block_header` (Task 2).
- Produces: `_ws_dien_cho_trong`, `_ans_dien_cho_trong`.

- [ ] **Step 1: Write the failing test**

Append:
```python
FILL_BLOCK = {
    "type": "dien_cho_trong",
    "title": "Điền từ",
    "instructions": "Chọn từ trong khung.",
    "word_bank": ["会", "想", "能"],
    "items": [
        {"q": "我{}说一点儿汉语。", "answer": "会"},
        {"q": "今天我不{}去。", "answer": "能", "src": "phỏng theo 真题"},
    ],
}


def test_fill_worksheet_shows_blanks_and_bank_but_no_answers():
    doc = WorksheetBuilder(_spec(FILL_BLOCK)).render_worksheet()
    text = _all_text(doc)
    assert "会" in text and "想" in text  # bank present
    assert BLANK in text                   # blanks rendered
    # The full answered sentence "我会说一点儿汉语。" must NOT appear.
    assert "我会说一点儿汉语。" not in text


def test_fill_answer_key_fills_and_labels_generated():
    doc = WorksheetBuilder(_spec(FILL_BLOCK)).render_answers()
    text = _all_text(doc)
    assert "我会说一点儿汉语。" in text
    assert "phỏng theo 真题" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k fill -v
```
Expected: FAIL — no `_ws_dien_cho_trong`.

- [ ] **Step 3: Write the implementation**

Add to `WorksheetBuilder`:
```python
    # -- dien_cho_trong (fill blank) --------------------------------------
    def _word_bank(self, doc, words):
        p = doc.add_paragraph()
        self._run(p, "[ ", 12, color="muted", bold=True)
        for i, w in enumerate(words):
            if i:
                self._run(p, " / ", 12, color="muted")
            self._run(p, w, 13, color="accent", bold=True, cjk=True)
        self._run(p, " ]", 12, color="muted", bold=True)

    def _ws_dien_cho_trong(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Điền vào chỗ trống"),
                           block.get("instructions"))
        self._word_bank(doc, block.get("word_bank", []))
        for n, it in enumerate(block.get("items", []), start=1):
            p = doc.add_paragraph()
            self._run(p, "%d) " % n, 12, color="accent", bold=True)
            self._run(p, it.get("q", "").replace("{}", BLANK), 14, cjk=True)

    def _ans_dien_cho_trong(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Điền vào chỗ trống"))
        for n, it in enumerate(block.get("items", []), start=1):
            p = doc.add_paragraph()
            self._run(p, "%d) " % n, 12, color="accent", bold=True)
            self._run(p, it.get("q", "").replace("{}", it.get("answer", "")),
                      14, cjk=True)
            if it.get("src"):
                self._run(p, "  [%s]" % it["src"], 10, color="muted",
                          italic=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k fill -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add -A .claude/skills/exercise-generator/worksheet
git commit -m "feat(exercise-generator): dien_cho_trong (fill-blank) block renderer"
```

---

## Task 5: `doc_hieu` block — reading comprehension MCQ (读, HSK 阅读理解)

**Files:**
- Modify: `build_worksheet.py`; Test: same file.

**Block shape:** `{"type":"doc_hieu","title":str,"instructions":str,"passage":str,"questions":[{"q":str,"options":[str,str,str],"answer":"A|B|C","src":str?}, ...]}`
Worksheet shows the passage, then each question with lettered options and a blank for the choice — **no answer marked**. Answer key repeats each question and marks the correct letter.

**Interfaces:**
- Consumes: `_run`, `_block_header`.
- Produces: `_ws_doc_hieu`, `_ans_doc_hieu`.

- [ ] **Step 1: Write the failing test**

Append:
```python
READ_BLOCK = {
    "type": "doc_hieu",
    "title": "Đọc hiểu",
    "passage": "小明会说汉语，也会说英语。",
    "questions": [
        {"q": "小明会说什么？", "options": ["汉语和英语", "只有汉语", "日语"],
         "answer": "A"},
    ],
}


def test_read_worksheet_shows_passage_options_no_marked_answer():
    doc = WorksheetBuilder(_spec(READ_BLOCK)).render_worksheet()
    text = _all_text(doc)
    assert "小明会说汉语" in text
    assert "A." in text and "汉语和英语" in text
    assert "✔" not in text  # no answer marker on the worksheet


def test_read_answer_key_marks_correct_letter():
    doc = WorksheetBuilder(_spec(READ_BLOCK)).render_answers()
    text = _all_text(doc)
    assert "✔ A" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k read -v
```
Expected: FAIL — no `_ws_doc_hieu`.

- [ ] **Step 3: Write the implementation**

Add to `WorksheetBuilder`:
```python
    # -- doc_hieu (reading MCQ) -------------------------------------------
    def _mcq_questions(self, doc, questions, mark_answer):
        letters = ["A", "B", "C", "D"]
        for n, q in enumerate(questions, start=1):
            p = doc.add_paragraph()
            self._run(p, "%d) " % n, 12, color="accent", bold=True)
            self._run(p, q.get("q", ""), 13, cjk=True)
            if not mark_answer:
                self._run(p, "   " + BLANK, 12, color="muted")
            for li, opt in enumerate(q.get("options", [])):
                op = doc.add_paragraph()
                op.paragraph_format.left_indent = Pt(18)
                letter = letters[li]
                is_ans = mark_answer and q.get("answer") == letter
                self._run(op, ("✔ " if is_ans else "") + "%s. " % letter,
                          12, color=("accent" if is_ans else "ink"),
                          bold=is_ans)
                self._run(op, opt, 12, cjk=True, bold=is_ans)
            if mark_answer and q.get("src"):
                sp = doc.add_paragraph()
                self._run(sp, "[%s]" % q["src"], 10, color="muted", italic=True)

    def _ws_doc_hieu(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Đọc hiểu"),
                           block.get("instructions"))
        pp = doc.add_paragraph()
        self._run(pp, block.get("passage", ""), 13, cjk=True)
        self._mcq_questions(doc, block.get("questions", []), mark_answer=False)

    def _ans_doc_hieu(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Đọc hiểu"))
        self._mcq_questions(doc, block.get("questions", []), mark_answer=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k read -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add -A .claude/skills/exercise-generator/worksheet
git commit -m "feat(exercise-generator): doc_hieu (reading MCQ) block renderer"
```

---

## Task 6: `sap_xep` block — sentence ordering (书写, HSK 完成句子)

**Files:**
- Modify: `build_worksheet.py`; Test: same file.

**Block shape:** `{"type":"sap_xep","title":str,"instructions":str,"items":[{"words":[str,...],"answer":str,"src":str?}, ...]}`
Worksheet shows the scrambled word chips (deterministically reordered, joined by " / ") and a blank line to write the sentence. Answer key shows the correct sentence.

**Interfaces:**
- Consumes: `_run`, `_block_header`, `_rotate`.
- Produces: `_ws_sap_xep`, `_ans_sap_xep`.

- [ ] **Step 1: Write the failing test**

Append:
```python
ORDER_BLOCK = {
    "type": "sap_xep",
    "title": "Sắp xếp câu",
    "items": [{"words": ["我", "会", "说", "汉语"], "answer": "我会说汉语。"}],
}


def test_order_worksheet_shows_chips_not_answer():
    doc = WorksheetBuilder(_spec(ORDER_BLOCK)).render_worksheet()
    text = _all_text(doc)
    assert "会" in text and "汉语" in text
    assert "我会说汉语。" not in text  # answer hidden


def test_order_answer_key_shows_sentence():
    doc = WorksheetBuilder(_spec(ORDER_BLOCK)).render_answers()
    assert "我会说汉语。" in _all_text(doc)
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k order -v
```
Expected: FAIL — no `_ws_sap_xep`.

- [ ] **Step 3: Write the implementation**

Add to `WorksheetBuilder`:
```python
    # -- sap_xep (sentence ordering) --------------------------------------
    def _ws_sap_xep(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Sắp xếp câu"),
                           block.get("instructions"))
        for n, it in enumerate(block.get("items", []), start=1):
            chips = self._rotate(list(it.get("words", [])), 2)
            p = doc.add_paragraph()
            self._run(p, "%d) " % n, 12, color="accent", bold=True)
            self._run(p, " / ".join(chips), 14, cjk=True)
            ans = doc.add_paragraph()
            self._run(ans, "→ " + BLANK * 3, 12, color="muted")

    def _ans_sap_xep(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Sắp xếp câu"))
        for n, it in enumerate(block.get("items", []), start=1):
            p = doc.add_paragraph()
            self._run(p, "%d) " % n, 12, color="accent", bold=True)
            self._run(p, it.get("answer", ""), 14, cjk=True)
            if it.get("src"):
                self._run(p, "  [%s]" % it["src"], 10, color="muted",
                          italic=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k order -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add -A .claude/skills/exercise-generator/worksheet
git commit -m "feat(exercise-generator): sap_xep (sentence ordering) block renderer"
```

---

## Task 7: `dich_dat_cau` block — translate / compose (书写, hoạt hóa)

**Files:**
- Modify: `build_worksheet.py`; Test: same file.

**Block shape:** `{"type":"dich_dat_cau","title":str,"instructions":str,"items":[{"prompt":str,"given":[str,...],"answer":str,"src":str?}, ...]}`
`prompt` is the Vietnamese to translate (or a compose instruction); `given` are required words. Worksheet shows prompt + given words + blank; answer key shows the model sentence.

**Interfaces:**
- Consumes: `_run`, `_block_header`.
- Produces: `_ws_dich_dat_cau`, `_ans_dich_dat_cau`.

- [ ] **Step 1: Write the failing test**

Append:
```python
TRANS_BLOCK = {
    "type": "dich_dat_cau",
    "title": "Dịch câu",
    "items": [{"prompt": "Tôi muốn học tiếng Trung.", "given": ["想", "学"],
               "answer": "我想学汉语。"}],
}


def test_trans_worksheet_shows_prompt_and_given_not_answer():
    doc = WorksheetBuilder(_spec(TRANS_BLOCK)).render_worksheet()
    text = _all_text(doc)
    assert "Tôi muốn học tiếng Trung." in text
    assert "想" in text and "学" in text
    assert "我想学汉语。" not in text


def test_trans_answer_key_shows_model_sentence():
    doc = WorksheetBuilder(_spec(TRANS_BLOCK)).render_answers()
    assert "我想学汉语。" in _all_text(doc)
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k trans -v
```
Expected: FAIL — no `_ws_dich_dat_cau`.

- [ ] **Step 3: Write the implementation**

Add to `WorksheetBuilder`:
```python
    # -- dich_dat_cau (translate / compose) -------------------------------
    def _ws_dich_dat_cau(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Dịch / Đặt câu"),
                           block.get("instructions"))
        for n, it in enumerate(block.get("items", []), start=1):
            p = doc.add_paragraph()
            self._run(p, "%d) " % n, 12, color="accent", bold=True)
            self._run(p, it.get("prompt", ""), 13)
            if it.get("given"):
                self._run(p, "  (dùng: %s)" % " / ".join(it["given"]), 12,
                          color="muted", cjk=True)
            ans = doc.add_paragraph()
            self._run(ans, "→ " + BLANK * 3, 12, color="muted")

    def _ans_dich_dat_cau(self, doc, block, idx):
        self._block_header(doc, idx, block.get("title", "Dịch / Đặt câu"))
        for n, it in enumerate(block.get("items", []), start=1):
            p = doc.add_paragraph()
            self._run(p, "%d) " % n, 12, color="accent", bold=True)
            self._run(p, it.get("answer", ""), 14, cjk=True)
            if it.get("src"):
                self._run(p, "  [%s]" % it["src"], 10, color="muted",
                          italic=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k trans -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add -A .claude/skills/exercise-generator/worksheet
git commit -m "feat(exercise-generator): dich_dat_cau (translate/compose) block renderer"
```

---

## Task 8: `nghe` block — listening (听力) with script-only-in-answer-key

**Files:**
- Modify: `build_worksheet.py`; Test: same file.

**Block shape:** `{"type":"nghe","title":str,"instructions":str,"items":[{"script":str,"q":str,"options":[str,...],"answer":"A|B|C","audio":str?,"audio_url":str?,"src":str?}, ...]}`
CRITICAL: `script` (听力文本) MUST appear **only** in the answer key. Worksheet shows a listening icon + the question + options + blank, plus an audio hyperlink if `audio`/`audio_url` present (audio files themselves are produced later, gated). Answer key shows script + correct letter.

**Interfaces:**
- Consumes: `_run`, `_block_header` (Task 2). Note: `_ws_nghe` renders its own
  lettered options (it also needs the audio link + answer blank), so it does NOT
  reuse `_mcq_questions`.
- Produces: `_ws_nghe`, `_ans_nghe`.

- [ ] **Step 1: Write the failing test**

Append:
```python
LISTEN_BLOCK = {
    "type": "nghe",
    "title": "Nghe và chọn",
    "instructions": "Nghe rồi chọn đáp án đúng.",
    "items": [
        {"script": "你会游泳吗？", "q": "对话问什么？",
         "options": ["会不会游泳", "会不会开车", "想不想吃饭"], "answer": "A",
         "audio": "audio/nghe-1.mp3"},
    ],
}


def test_listen_worksheet_hides_script_shows_question():
    doc = WorksheetBuilder(_spec(LISTEN_BLOCK)).render_worksheet()
    text = _all_text(doc)
    assert "你会游泳吗？" not in text          # script hidden on worksheet
    assert "对话问什么？" in text               # question shown
    assert "会不会游泳" in text                 # options shown
    assert "audio/nghe-1.mp3" in text          # audio link shown


def test_listen_answer_key_reveals_script_and_answer():
    doc = WorksheetBuilder(_spec(LISTEN_BLOCK)).render_answers()
    text = _all_text(doc)
    assert "你会游泳吗？" in text               # 听力文本 revealed
    assert "✔ A" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k listen -v
```
Expected: FAIL — no `_ws_nghe`.

- [ ] **Step 3: Write the implementation**

Add to `WorksheetBuilder`:
```python
    # -- nghe (listening) -------------------------------------------------
    def _ws_nghe(self, doc, block, idx):
        self._block_header(doc, idx, "🔊 " + block.get("title", "Nghe"),
                           block.get("instructions"))
        letters = ["A", "B", "C", "D"]
        for n, it in enumerate(block.get("items", []), start=1):
            link = it.get("audio_url") or it.get("audio")
            if link:
                lp = doc.add_paragraph()
                self._run(lp, "🔊 Nghe câu %d: %s" % (n, link), 11,
                          color="accent", italic=True)
            qp = doc.add_paragraph()
            self._run(qp, "%d) " % n, 12, color="accent", bold=True)
            self._run(qp, it.get("q", ""), 13, cjk=True)
            self._run(qp, "   " + BLANK, 12, color="muted")
            for li, opt in enumerate(it.get("options", [])):
                op = doc.add_paragraph()
                op.paragraph_format.left_indent = Pt(18)
                self._run(op, "%s. " % letters[li], 12)
                self._run(op, opt, 12, cjk=True)

    def _ans_nghe(self, doc, block, idx):
        self._block_header(doc, idx, "🔊 " + block.get("title", "Nghe"))
        for n, it in enumerate(block.get("items", []), start=1):
            sp = doc.add_paragraph()
            self._run(sp, "%d) 听力文本: " % n, 12, color="muted", bold=True)
            self._run(sp, it.get("script", ""), 13, cjk=True)
            ap = doc.add_paragraph()
            self._run(ap, "✔ %s" % it.get("answer", ""), 12, color="accent",
                      bold=True)
            if it.get("src"):
                self._run(ap, "  [%s]" % it["src"], 10, color="muted",
                          italic=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k listen -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add -A .claude/skills/exercise-generator/worksheet
git commit -m "feat(exercise-generator): nghe (listening) block — script only in answer key"
```

---

## Task 9: `noi_hskk` block — speaking prompts (HSKK 初级)

**Files:**
- Modify: `build_worksheet.py`; Test: same file.

**Block shape:** `{"type":"noi_hskk","title":str,"part":"听后重复|回答问题",​"instructions":str,"items":[{"script":str,"hint":str,"audio":str?}, ...]}`
Worksheet shows the part name + prompts. For `回答问题` the student sees the question text; for `听后重复` the target sentence is a listening item, so its `script` is hidden on the worksheet (shown only in answer key) and only an audio link/instruction appears. Answer key always shows script + suggested answer (`hint`).

**Interfaces:**
- Consumes: `_run`, `_block_header`.
- Produces: `_ws_noi_hskk`, `_ans_noi_hskk`.

- [ ] **Step 1: Write the failing test**

Append:
```python
SPEAK_REPEAT = {
    "type": "noi_hskk", "title": "Nghe và nhắc lại", "part": "听后重复",
    "items": [{"script": "我会说一点儿汉语。", "audio": "audio/hskk-1.mp3"}],
}
SPEAK_ANSWER = {
    "type": "noi_hskk", "title": "Trả lời câu hỏi", "part": "回答问题",
    "items": [{"script": "你会做饭吗？", "hint": "我会做饭。/ 我不会做饭。"}],
}


def test_speak_repeat_hides_target_on_worksheet():
    doc = WorksheetBuilder(_spec(SPEAK_REPEAT)).render_worksheet()
    text = _all_text(doc)
    assert "听后重复" in text
    assert "我会说一点儿汉语。" not in text  # target hidden for repeat drill
    assert "audio/hskk-1.mp3" in text


def test_speak_answer_shows_question_on_worksheet_hint_in_key():
    ws = _all_text(WorksheetBuilder(_spec(SPEAK_ANSWER)).render_worksheet())
    ans = _all_text(WorksheetBuilder(_spec(SPEAK_ANSWER)).render_answers())
    assert "你会做饭吗？" in ws           # question is shown for 回答问题
    assert "我会做饭。" not in ws          # suggested answer hidden on worksheet
    assert "我会做饭。" in ans             # suggested answer in the key
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k speak -v
```
Expected: FAIL — no `_ws_noi_hskk`.

- [ ] **Step 3: Write the implementation**

Add to `WorksheetBuilder`:
```python
    # -- noi_hskk (speaking) ----------------------------------------------
    def _ws_noi_hskk(self, doc, block, idx):
        part = block.get("part", "")
        title = block.get("title", "Nói")
        self._block_header(doc, idx, "🗣 %s (%s)" % (title, part),
                           block.get("instructions"))
        repeat = part == "听后重复"
        for n, it in enumerate(block.get("items", []), start=1):
            p = doc.add_paragraph()
            self._run(p, "%d) " % n, 12, color="accent", bold=True)
            if it.get("audio"):
                self._run(p, "🔊 %s   " % it["audio"], 11, color="accent",
                          italic=True)
            if repeat:
                # target sentence is the listening stimulus -> hide it
                self._run(p, "(nghe audio rồi nhắc lại)", 12, color="muted",
                          italic=True)
            else:
                self._run(p, it.get("script", ""), 13, cjk=True)

    def _ans_noi_hskk(self, doc, block, idx):
        part = block.get("part", "")
        self._block_header(doc, idx,
                           "🗣 %s (%s)" % (block.get("title", "Nói"), part))
        for n, it in enumerate(block.get("items", []), start=1):
            p = doc.add_paragraph()
            self._run(p, "%d) " % n, 12, color="accent", bold=True)
            self._run(p, it.get("script", ""), 13, cjk=True)
            if it.get("hint"):
                hp = doc.add_paragraph()
                self._run(hp, "   Gợi ý: ", 11, color="muted", bold=True)
                self._run(hp, it["hint"], 12, cjk=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k speak -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add -A .claude/skills/exercise-generator/worksheet
git commit -m "feat(exercise-generator): noi_hskk (speaking) block renderer"
```

---

## Task 10: Audio manifest helper (gated TTS job list + optional QR)

**Files:**
- Create: `.claude/skills/exercise-generator/worksheet/audio_manifest.py`
- Test: same test file.

**Purpose:** Produce the list of TTS jobs the skill would synthesize (text → filename → voice) from a baitap spec, WITHOUT calling the network. Actual MP3 synthesis (`edge-tts`) is a separate, user-gated runtime step documented in SKILL.md. This task builds only the deterministic, testable planning half.

**Interfaces:**
- Produces: `build_audio_manifest(spec: dict, voice: str = "zh-CN-XiaoxiaoNeural") -> list[dict]` where each dict is `{"text": str, "file": str, "voice": str}`. It collects every `audio` path in `nghe` and `noi_hskk` items, pairing it with the item's `script`. Items without an `audio` key are skipped.

- [ ] **Step 1: Write the failing test**

Append to `test_build_worksheet.py`:
```python
from audio_manifest import build_audio_manifest


def test_audio_manifest_collects_listening_and_speaking_jobs():
    spec = _spec(LISTEN_BLOCK, SPEAK_REPEAT, TRANS_BLOCK)
    jobs = build_audio_manifest(spec)
    files = {j["file"] for j in jobs}
    assert files == {"audio/nghe-1.mp3", "audio/hskk-1.mp3"}
    nghe = next(j for j in jobs if j["file"] == "audio/nghe-1.mp3")
    assert nghe["text"] == "你会游泳吗？"
    assert nghe["voice"] == "zh-CN-XiaoxiaoNeural"
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k manifest -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'audio_manifest'`.

- [ ] **Step 3: Write the implementation**

Create `.claude/skills/exercise-generator/worksheet/audio_manifest.py`:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audio_manifest.py — Liệt kê các job TTS (text -> file -> voice) từ baitap spec.

KHÔNG gọi mạng. Việc sinh MP3 thật (edge-tts) là bước riêng, có cổng xác nhận
của user (xem SKILL.md). Đây chỉ là phần lập kế hoạch, kiểm thử được.
"""

DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"


def build_audio_manifest(spec, voice=DEFAULT_VOICE):
    jobs = []
    for block in spec.get("blocks", []):
        if block.get("type") not in ("nghe", "noi_hskk"):
            continue
        for it in block.get("items", []):
            path = it.get("audio")
            if not path:
                continue
            jobs.append({"text": it.get("script", ""), "file": path,
                         "voice": voice})
    return jobs
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k manifest -v
```
Expected: 1 passed.

- [ ] **Step 5: Commit**

```bash
git add -A .claude/skills/exercise-generator/worksheet
git commit -m "feat(exercise-generator): audio manifest planner (gated TTS jobs)"
```

---

## Task 11: PDF export — best-effort with explicit fallback

**Files:**
- Modify: `build_worksheet.py`; Test: same file.

**Purpose:** Convert a rendered `.docx` to `.pdf` when a converter exists (LibreOffice `soffice`), else return a clear fallback signal so the skill can tell the user to "Save as PDF" manually. Must NOT crash when no converter is present.

**Interfaces:**
- Produces: `docx_to_pdf(docx_path: str) -> str | None` — returns the output `.pdf` path on success, or `None` when no converter is available (never raises for the missing-converter case).
- Modify `main` to attempt PDF export for both docs and print which ones converted.

- [ ] **Step 1: Write the failing test**

Append:
```python
import shutil
from build_worksheet import docx_to_pdf


def test_pdf_fallback_returns_none_when_no_converter(tmp_path, monkeypatch):
    # Simulate no LibreOffice on PATH.
    monkeypatch.setattr(shutil, "which", lambda name: None)
    fake = tmp_path / "worksheet.docx"
    fake.write_bytes(b"not a real docx")
    assert docx_to_pdf(str(fake)) is None
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k pdf -v
```
Expected: FAIL — cannot import `docx_to_pdf`.

- [ ] **Step 3: Write the implementation**

Add near the top of `build_worksheet.py` (after imports):
```python
import shutil
import subprocess
```

Add before `main`:
```python
def docx_to_pdf(docx_path):
    """Convert .docx -> .pdf via LibreOffice if available; else return None."""
    soffice = shutil.which("soffice") or shutil.which("soffice.exe")
    if not soffice:
        return None
    src = Path(docx_path)
    out_dir = src.parent
    try:
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf", "--outdir",
             str(out_dir), str(src)],
            check=True, capture_output=True, timeout=120)
    except (subprocess.SubprocessError, OSError):
        return None
    pdf = src.with_suffix(".pdf")
    return str(pdf) if pdf.exists() else None
```

Update `main` — replace its final `print(...)`/`return 0` tail with:
```python
    made = []
    for name in ("worksheet.docx", "dapan.docx"):
        pdf = docx_to_pdf(str(out_dir / name))
        if pdf:
            made.append(Path(pdf).name)
    n = len(spec.get("blocks", []))
    print("OK: %d block -> %s/{worksheet,dapan}.docx" % (n, out_dir))
    if made:
        print("PDF: " + ", ".join(made))
    else:
        print("PDF: chưa xuất (không thấy LibreOffice). "
              "Mở .docx và 'Save as PDF' nếu cần.")
    return 0
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k pdf -v
```
Expected: 1 passed.

- [ ] **Step 5: Commit**

```bash
git add -A .claude/skills/exercise-generator/worksheet
git commit -m "feat(exercise-generator): best-effort docx->pdf with fallback"
```

---

## Task 12: Full-suite guard — worksheet-vs-key leakage check

**Files:**
- Test: same test file (no source change expected; this is the safety net for the Global Constraint).

**Interfaces:**
- Consumes: all block renderers + `_spec`, `_all_text`.

- [ ] **Step 1: Write the failing test**

Append:
```python
ALL_BLOCKS = [NOI_BLOCK, FILL_BLOCK, READ_BLOCK, ORDER_BLOCK, TRANS_BLOCK,
              LISTEN_BLOCK, SPEAK_REPEAT, SPEAK_ANSWER]


def test_no_listening_script_leaks_into_worksheet():
    spec = {"meta": {"lesson": "Buổi 1: 会/想/能", "hsk": 1},
            "blocks": ALL_BLOCKS}
    ws = _all_text(WorksheetBuilder(spec).render_worksheet())
    # Every listening / repeat script must be absent from the worksheet.
    for hidden in ("你会游泳吗？", "我会说一点儿汉语。"):
        assert hidden not in ws
    # But the answer key must contain them.
    key = _all_text(WorksheetBuilder(spec).render_answers())
    assert "你会游泳吗？" in key and "我会说一点儿汉语。" in key
```

- [ ] **Step 2: Run test — expect PASS (renderers already enforce this)**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k leak -v
```
Expected: PASS. If it FAILS, the offending block renderer is leaking an answer/script into the worksheet — fix that renderer (the worksheet method must not emit `script`/`answer` text) before continuing.

- [ ] **Step 3: Commit**

```bash
git add -A .claude/skills/exercise-generator/worksheet
git commit -m "test(exercise-generator): guard against answer/script leakage into worksheet"
```

---

## Task 13: Integration fixture — example-baitap.json + end-to-end render

**Files:**
- Create: `.claude/skills/exercise-generator/worksheet/example-baitap.json`
- Test: same test file.

**Interfaces:**
- Consumes: `main` (CLI), all block renderers.

- [ ] **Step 1: Create the fixture covering all 7 block types**

Create `.claude/skills/exercise-generator/worksheet/example-baitap.json`:
```json
{
  "meta": {"lesson": "Buổi 1: 会 / 想 / 能", "hsk": 1, "student": "demo"},
  "blocks": [
    {"type": "noi", "title": "Nối chữ với nghĩa",
     "instructions": "Viết chữ cái đúng vào ô.",
     "pairs": [
       {"left": "会", "right": "biết (kỹ năng đã học)"},
       {"left": "想", "right": "muốn"},
       {"left": "能", "right": "có thể (điều kiện)"}
     ]},
    {"type": "dien_cho_trong", "title": "Điền từ vào chỗ trống",
     "instructions": "Chọn từ trong khung.",
     "word_bank": ["会", "想", "能"],
     "items": [
       {"q": "我{}说一点儿汉语。", "answer": "会"},
       {"q": "今天下雨，我不{}去公园。", "answer": "能",
        "src": "phỏng theo 真题"},
       {"q": "我{}喝一杯咖啡。", "answer": "想"}
     ]},
    {"type": "doc_hieu", "title": "Đọc hiểu",
     "passage": "小明会说汉语，也会说一点儿英语。他很想去中国。",
     "questions": [
       {"q": "小明会说什么？",
        "options": ["汉语和一点儿英语", "只有英语", "日语"], "answer": "A"},
       {"q": "小明想去哪儿？", "options": ["中国", "美国", "日本"],
        "answer": "A", "src": "phỏng theo 真题"}
     ]},
    {"type": "sap_xep", "title": "Sắp xếp thành câu đúng",
     "items": [
       {"words": ["我", "会", "说", "汉语"], "answer": "我会说汉语。"},
       {"words": ["他", "想", "去", "中国"], "answer": "他想去中国。"}
     ]},
    {"type": "dich_dat_cau", "title": "Dịch sang tiếng Trung",
     "items": [
       {"prompt": "Tôi muốn học tiếng Trung.", "given": ["想", "学"],
        "answer": "我想学汉语。"},
       {"prompt": "Hôm nay tôi không thể đi.", "given": ["能"],
        "answer": "今天我不能去。"}
     ]},
    {"type": "nghe", "title": "Nghe và chọn đáp án",
     "instructions": "Nghe rồi chọn đáp án đúng.",
     "items": [
       {"script": "你会游泳吗？", "q": "问的是什么？",
        "options": ["会不会游泳", "会不会开车", "想不想吃饭"], "answer": "A",
        "audio": "audio/nghe-1.mp3"}
     ]},
    {"type": "noi_hskk", "title": "Nghe và nhắc lại", "part": "听后重复",
     "items": [
       {"script": "我会说一点儿汉语。", "audio": "audio/hskk-1.mp3"}
     ]},
    {"type": "noi_hskk", "title": "Trả lời câu hỏi", "part": "回答问题",
     "items": [
       {"script": "你会做饭吗？", "hint": "我会做饭。/ 我不会做饭。"}
     ]}
  ]
}
```

- [ ] **Step 2: Write the failing end-to-end test**

Append to `test_build_worksheet.py`:
```python
import json
import pathlib
from build_worksheet import main

FIXTURE = pathlib.Path(__file__).resolve().parent.parent / "example-baitap.json"


def test_example_fixture_has_all_seven_block_types():
    spec = json.loads(FIXTURE.read_text(encoding="utf-8"))
    types = {b["type"] for b in spec["blocks"]}
    assert types == {"noi", "dien_cho_trong", "doc_hieu", "sap_xep",
                     "dich_dat_cau", "nghe", "noi_hskk"}


def test_end_to_end_cli_writes_both_docs(tmp_path):
    rc = main(["build_worksheet.py", str(FIXTURE), str(tmp_path)])
    assert rc == 0
    assert (tmp_path / "worksheet.docx").exists()
    assert (tmp_path / "dapan.docx").exists()
    # reopen worksheet and confirm CJK + no listening-script leak
    from docx import Document
    ws = _all_text(Document(str(tmp_path / "worksheet.docx")))
    assert "会" in ws
    assert "你会游泳吗？" not in ws
```

- [ ] **Step 3: Run test to verify it fails, then passes**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/test_build_worksheet.py" -k "fixture or end_to_end" -v
```
Expected: PASS (fixture + renderers already exist). If the fixture path/type set is wrong, fix the JSON.

- [ ] **Step 4: Run the FULL suite**

Run:
```bash
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/" -v
```
Expected: all tests pass.

- [ ] **Step 5: Manual smoke — open the generated files**

Run:
```bash
"$PY" .claude/skills/exercise-generator/worksheet/build_worksheet.py \
  .claude/skills/exercise-generator/worksheet/example-baitap.json \
  output/hsk1/baitap/demo
```
Expected: prints `OK: 8 block -> .../demo/{worksheet,dapan}.docx` and a `PDF:` line. Open `worksheet.docx` and `dapan.docx`; confirm Chinese renders (not tofu boxes), answers/scripts appear only in `dapan.docx`.

- [ ] **Step 6: Commit**

```bash
git add -A .claude/skills/exercise-generator/worksheet
git commit -m "test(exercise-generator): example fixture + end-to-end CLI render"
```

---

## Task 14: SKILL.md — persona, two-phase process, routing, gates

**Files:**
- Create: `.claude/skills/exercise-generator/SKILL.md`

**Interfaces:**
- Consumes: the renderer CLI and JSON schema (documented in later task) — reference exact paths.

- [ ] **Step 1: Write SKILL.md**

Create `.claude/skills/exercise-generator/SKILL.md`:
```markdown
---
name: exercise-generator
description: Sinh bài tập tiếng Trung HSK1-3 cho học viên (đủ 听/读/书写 + HSKK), bám theo từng buổi dạy, ưu tiên câu từ kho đề真题/đề mẫu, render ra .docx tương tác + file đáp án riêng. Use when user muốn "tạo bài tập", "làm đề", "worksheet", "bài tập buổi X".
---

# Exercise Generator — Bài tập HSK1-3

## Vai trò
Master Chinese Teacher soạn bài tập cho học viên đang học HSK1-3. Bài tập bám
theo nội dung từng buổi (会/想/能 · lượng từ · 了...), phủ đủ 4 kỹ năng theo đúng
format thi HSK và HSKK 初级.

## Nguyên tắc nội dung
- **Ưu tiên kho đề:** rút/biến tấu câu từ `knowledge/hsk-exam-bank/hskN.md` trước.
  Chỗ kho thiếu mới tự sinh, gắn nhãn `[phỏng theo 真题]`.
- **Độ khó:** ~70% đúng cấp của buổi + ~30% cao hơn 1 bậc (HSK1 → điểm xuyết HSK2).
- **Cá nhân hóa:** dùng `.claude/skills/teaching-coach/references/interest-personalization.md`
  để ví dụ bám sở thích học viên, tránh câu sáo rỗng.
- Chỉ **đọc** `memory/*`. Không tự sửa memory (CLAUDE.md §4).

## Giai đoạn A — Soạn bài tập
1. Đọc nội dung buổi: `output/hskN/buoiX.json` (do teaching-coach tạo) để lấy
   từ vựng + điểm ngữ pháp trọng tâm.
2. Chọn các block phù hợp (xem `references/exercise-types.md`) — thường đủ 7 loại:
   `noi`, `dien_cho_trong`, `doc_hieu`, `sap_xep`, `dich_dat_cau`, `nghe`,
   `noi_hskk`.
3. Ghi file `output/hskN/baitap/baitap-buoiX.json` theo `worksheet/schema.md`.
4. **Với block `nghe` / `noi_hskk`:** trình 听力文本 / câu hỏi nói dạng text cho
   user duyệt. **KHÔNG sinh MP3 ngay.**

## Cổng xác nhận audio (bắt buộc)
- Chỉ sau khi user duyệt script, mới sinh MP3:
  - Kiểm tra `edge-tts`: `python -c "import edge_tts"`. Nếu thiếu → **dừng**,
    hướng dẫn `python -m pip install edge-tts`, KHÔNG tự cài.
  - Lấy job list: `audio_manifest.build_audio_manifest(spec)`.
  - Sinh từng file: `python -m edge_tts --voice zh-CN-XiaoxiaoNeural
    --text "<script>" --write-media output/hskN/baitap/<file>`.
- Đường dẫn `audio` trong JSON phải khớp file sinh ra để link trong .docx trỏ đúng.

## Giai đoạn B — Render
```bash
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
"$PY" .claude/skills/exercise-generator/worksheet/build_worksheet.py \
  output/hskN/baitap/baitap-buoiX.json output/hskN/baitap/buoiX
```
→ `worksheet.docx` (cho học viên) + `dapan.docx` (đáp án + 听力文本). PDF tự xuất
nếu có LibreOffice, không thì báo user "Save as PDF".

- **worksheet.docx KHÔNG BAO GIỜ chứa đáp án hay 听力文本** (renderer đã tách).
- Chiếu lớp (tùy chọn): có thể tái dùng `teaching-coach/pptx/build_deck.py` với
  một deck riêng — không bắt buộc trong luồng bài tập.

## Gây dựng kho đề (1 lần, có review gate)
Khi kho `knowledge/hsk-exam-bank/hskN.md` còn trống:
1. WebSearch/WebFetch nguồn uy tín: chinesetest.cn (CTI 官方), đề mẫu Hanban/Viện
   Khổng Tử, bài tập bộ HSK Standard Course.
2. Dùng skill `doc-analyzer` bóc câu hỏi.
3. **Trình user duyệt** danh sách câu + nguồn trước khi ghi vào `hskN.md` +
   `sources.md` (nguồn + ngày). Không lấy 真题 sách bản quyền từ nguồn lậu.

## Ghi log
Sau khi render, append 1 dòng vào `state/session-log.md`: buổi, các block, cấp độ.

## Báo kết quả
Báo user đường dẫn `worksheet.docx` / `dapan.docx` (+ PDF nếu có).
```

- [ ] **Step 2: Verify frontmatter parses (name/description present)**

Run:
```bash
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
"$PY" - <<'EOF'
import re, pathlib
t = pathlib.Path(".claude/skills/exercise-generator/SKILL.md").read_text(encoding="utf-8")
m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
assert m, "missing frontmatter"
assert "name: exercise-generator" in m.group(1)
assert "description:" in m.group(1)
print("SKILL.md frontmatter OK")
EOF
```
Expected: `SKILL.md frontmatter OK`

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/exercise-generator/SKILL.md
git commit -m "docs(exercise-generator): SKILL.md — 2-phase process, audio + seed gates"
```

---

## Task 15: Reference docs — exam format, exercise types, JSON schema

**Files:**
- Create: `.claude/skills/exercise-generator/references/hsk-exam-format.md`
- Create: `.claude/skills/exercise-generator/references/exercise-types.md`
- Create: `.claude/skills/exercise-generator/worksheet/schema.md`

- [ ] **Step 1: Write `hsk-exam-format.md`**

Create `.claude/skills/exercise-generator/references/hsk-exam-format.md`:
```markdown
# Cấu trúc đề HSK1-3 + HSKK 初级 (để soạn bài tập đúng format & độ khó)

## Ranh giới cấp độ (dùng cho quy tắc 70/30)
- **HSK1:** ~150 từ. Câu đơn, chủ đề: chào hỏi, số, thời gian, gia đình, ăn uống.
  Ngữ pháp: 是, 有, 会/想/能 cơ bản, 吗, 几, 现在.
- **HSK2:** ~300 từ. Thêm: 了 (hoàn thành), 过, 比, 一点儿/有点儿, lượng từ,
  正在, 因为…所以.
- **HSK3:** ~600 từ. Đoạn ngắn, 把, 被, 得 (bổ ngữ trình độ), 一边…一边, 越来越.

## HSK 听力 (Nghe)
- HSK1: 看图判断对错; 对话选图; 问答匹配.
- HSK2: 判断对错; 对话选图; 对话理解(选答案).
- HSK3: 对话/短文 → chọn đáp án A/B/C.
→ Map sang block `nghe` (script ẩn khỏi worksheet, chỉ ở đáp án).

## HSK 阅读 (Đọc)
- 匹配 (câu–ảnh / câu–câu) → block `noi`.
- 选词填空 (có word bank) → block `dien_cho_trong`.
- 阅读理解 (đoạn + câu hỏi) → block `doc_hieu`.

## HSK 书写 (Viết, HSK3+)
- 完成句子 / 排序 → block `sap_xep`.
- (mở rộng) dịch/đặt câu để hoạt hóa → block `dich_dat_cau`.

## HSKK 初级 (Nói)
- 第一部分 听后重复 (nghe & nhắc lại) → block `noi_hskk` part `听后重复`
  (target ẩn khỏi worksheet, có audio).
- 第三部分 回答问题 (trả lời câu hỏi) → block `noi_hskk` part `回答问题`
  (câu hỏi hiện, gợi ý trả lời chỉ ở đáp án).
```

- [ ] **Step 2: Write `exercise-types.md`**

Create `.claude/skills/exercise-generator/references/exercise-types.md`:
```markdown
# 7 loại block bài tập — cách soạn & chấm

| type | Kỹ năng | Worksheet hiện gì | Đáp án hiện gì |
|---|---|---|---|
| `noi` | Đọc | Bảng 汉字 / ô trả lời / nghĩa (đã xáo, đánh A,B,C) | chữ → chữ cái đúng |
| `dien_cho_trong` | Đọc | Word bank + câu có ＿＿＿ | câu điền đầy đủ |
| `doc_hieu` | Đọc | Đoạn văn + câu hỏi + options + ô trống | ✔ chữ cái đúng |
| `sap_xep` | Viết | Các chip từ (đã xáo) + dòng trống | câu đúng |
| `dich_dat_cau` | Viết | Câu Việt + từ cho trước + dòng trống | câu mẫu tiếng Trung |
| `nghe` | Nghe | 🔊 link + câu hỏi + options (KHÔNG script) | 听力文本 + ✔ đáp án |
| `noi_hskk` | Nói | part `听后重复`: chỉ audio; `回答问题`: câu hỏi | script + gợi ý trả lời |

## Quy tắc chấm gợi ý (ghi trong dapan.docx nếu cần)
- Đọc/Nghe: đúng/sai theo đáp án.
- Viết (`sap_xep`,`dich_dat_cau`): đúng trật tự + đúng chữ; chấp nhận biến thể hợp lệ.
- Nói (`noi_hskk`): chấm theo phát âm + đúng ý; gợi ý là 1 mẫu, không phải đáp án duy nhất.

## Nhắc
- Mỗi item tự sinh (không từ kho đề) → thêm `"src": "phỏng theo 真题"`.
- Item lấy từ kho → `"src"` ghi nguồn ngắn (vd `"HSK2 đề mẫu CTI 2023"`).
```

- [ ] **Step 3: Write `schema.md`**

Create `.claude/skills/exercise-generator/worksheet/schema.md`:
```markdown
# Schema JSON bài tập (`baitap-buoiX.json`)

```jsonc
{
  "meta": { "lesson": "Buổi 1: 会/想/能", "hsk": 1, "student": "tên (tùy chọn)" },
  "theme": { /* tùy chọn, override DEFAULT_THEME của build_worksheet.py */ },
  "blocks": [ /* danh sách block, mỗi block 1 "type" bên dưới */ ]
}
```

## Các block
- `noi`: `{ "type":"noi", "title", "instructions"?, "pairs":[{"left","right"}] }`
- `dien_cho_trong`: `{ "type":"dien_cho_trong", "title", "instructions"?,
  "word_bank":[str], "items":[{"q" (có "{}" đánh dấu chỗ trống), "answer", "src"?}] }`
- `doc_hieu`: `{ "type":"doc_hieu", "title", "instructions"?, "passage",
  "questions":[{"q","options":[str,str,str],"answer":"A|B|C","src"?}] }`
- `sap_xep`: `{ "type":"sap_xep", "title", "instructions"?,
  "items":[{"words":[str],"answer","src"?}] }`
- `dich_dat_cau`: `{ "type":"dich_dat_cau", "title", "instructions"?,
  "items":[{"prompt","given":[str]?,"answer","src"?}] }`
- `nghe`: `{ "type":"nghe", "title", "instructions"?,
  "items":[{"script" (chỉ vào đáp án), "q", "options":[str], "answer":"A|B|C",
  "audio"?, "audio_url"?, "src"?}] }`
- `noi_hskk`: `{ "type":"noi_hskk", "title", "part":"听后重复|回答问题",
  "instructions"?, "items":[{"script","hint"?,"audio"?}] }`

Xem ví dụ đầy đủ: `worksheet/example-baitap.json`.
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/exercise-generator/references .claude/skills/exercise-generator/worksheet/schema.md
git commit -m "docs(exercise-generator): exam-format, exercise-types, JSON schema refs"
```

---

## Task 16: Wire into the OS — exam-bank scaffold + CLAUDE.md updates

**Files:**
- Create: `knowledge/hsk-exam-bank/hsk1.md`, `hsk2.md`, `hsk3.md`, `sources.md`
- Modify: `CLAUDE.md` (§3 routing, §6 state, §7 catalog)

- [ ] **Step 1: Create the exam-bank scaffold**

Create `knowledge/hsk-exam-bank/sources.md`:
```markdown
# Nguồn kho đề HSK

Ghi lại nguồn từng đợt seed (nguồn + ngày tải) để truy vết.
Chỉ dùng đề mẫu/样卷 công khai hợp pháp (CTI/Hanban) + bài tập giáo trình.
KHÔNG lấy 真题 sách bản quyền từ nguồn lậu.

| Ngày | Cấp | Nguồn | Ghi chú |
|---|---|---|---|
| _(chưa seed)_ | | | |
```

Create `knowledge/hsk-exam-bank/hsk1.md`:
```markdown
# Kho đề HSK1

> Chưa seed. Skill exercise-generator sẽ điền câu hỏi (có review gate) từ nguồn
> trong `sources.md`. Mỗi mục ghi: dạng (匹配/选词填空/听力...), nội dung, đáp án,
> nguồn.
```

Create `knowledge/hsk-exam-bank/hsk2.md`:
```markdown
# Kho đề HSK2

> Chưa seed. Xem `sources.md` + hsk1.md để biết định dạng mục.
```

Create `knowledge/hsk-exam-bank/hsk3.md`:
```markdown
# Kho đề HSK3

> Chưa seed. Xem `sources.md` + hsk1.md để biết định dạng mục.
```

- [ ] **Step 2: Update CLAUDE.md — routing (§3)**

In `CLAUDE.md`, under `### Hard Route`, add after the `/speaking-coach` line:
```markdown
- `/exercise-generator` → invoke Skill("exercise-generator")
```

Under `### Soft Route`, add as a new rule before the `Ambiguous` line (renumbering not required — insert as rule 4.5 / adjust numbers if desired):
```markdown
4b. "tạo bài tập" / "bài tập" / "làm đề" / "worksheet" / "bài tập buổi X" → exercise-generator
```

- [ ] **Step 3: Update CLAUDE.md — state ownership (§6)**

In the §6 table, add these rows:
```markdown
| output/hskN/baitap/ | Exercise Generator (tạo baitap + worksheet + đáp án) |
| knowledge/hsk-exam-bank/ | Exercise Generator (seed có review gate) |
```
And append `Exercise Generator` to the writers of `state/session-log.md`:
```markdown
| state/session-log.md | HSK6 Examiner, Speaking Coach, Exercise Generator (append) |
```

- [ ] **Step 4: Update CLAUDE.md — skill catalog (§7)**

Add to the `## 7. Skill Catalog` list:
```markdown
- **exercise-generator** — Sinh bài tập HSK1-3 cho học viên (đủ 听/读/书写 + HSKK), bám buổi dạy, ưu tiên kho đề真题, render .docx tương tác + file đáp án; audio nghe/nói qua cổng xác nhận
```

- [ ] **Step 5: Update the Memory Ownership table (§4) read column**

In §4 table, add a row so the skill's read access to memory is documented:
```markdown
| memory/user-profile.md | Learning Strategist, HSK6 Examiner, Speaking Coach, Exercise Generator |
```
(Adjust the existing `user-profile.md` row rather than duplicating if present.)

- [ ] **Step 6: Verify CLAUDE.md still lists all skills consistently**

Run:
```bash
grep -n "exercise-generator" CLAUDE.md
```
Expected: matches in §3 (hard + soft route), §4, §6, §7.

- [ ] **Step 7: Final full-suite run**

Run:
```bash
PY="C:/Users/huyennhm/AppData/Local/Programs/Python/Python312/python.exe"
"$PY" -m pytest ".claude/skills/exercise-generator/worksheet/tests/" -v
```
Expected: all tests pass.

- [ ] **Step 8: Commit**

```bash
git add knowledge/hsk-exam-bank CLAUDE.md
git commit -m "feat(exercise-generator): wire into OS — exam-bank scaffold + CLAUDE.md routing/state/catalog"
```

---

## Done criteria

- `pytest` suite green (all block renderers + leakage guard + end-to-end CLI).
- `build_worksheet.py` produces a `worksheet.docx` (no answers/scripts) and `dapan.docx` (answers + 听力文本) with correct CJK rendering.
- `exercise-generator` skill discoverable and routed via CLAUDE.md.
- Exam bank scaffolded with provenance file; seeding deferred to a gated skill run.
- Audio synthesis fully gated behind user confirm; `edge-tts` never auto-installed.
