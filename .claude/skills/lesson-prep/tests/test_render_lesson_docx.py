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
