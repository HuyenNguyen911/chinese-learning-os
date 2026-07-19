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
