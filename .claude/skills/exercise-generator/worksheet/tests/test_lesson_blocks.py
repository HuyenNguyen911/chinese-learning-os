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
