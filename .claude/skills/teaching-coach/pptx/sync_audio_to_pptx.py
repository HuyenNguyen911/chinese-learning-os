#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_audio_to_pptx.py — Ghep/dong bo audio vao 1 file .pptx DA BI SUA TAY, khong
rebuild tu JSON (rebuild se xoa sach chinh sua tay ve layout/anh).

Dieu kien dung duoc script nay (khong can doi chieu tung dong):
  - Thu tu + noi dung text cua tung slide trong .pptx HIEN TAI van khop 1:1 voi
    cac slide trong JSON goc (user chi sua layout/anh/format, KHONG xoa/tach/
    doi cho slide). Neu nghi ngo, dump text tung slide (Presentation(path) roi
    doc shape.text_frame.text) doi chieu bang tay voi JSON truoc khi chay.
  - JSON da co key "audio" o slide can doc (chay slide_audio.py truoc buoc nay).

Neu slide da bi TACH/GOP/DOI CHO trong luc sua tay, KHONG dung script nay —
lam theo quy trinh doi chieu NGUYEN VAN trong README.md ("Dong bo audio vao
file .pptx da bi sua tay").

Chay:
    python sync_audio_to_pptx.py <lesson.json> <deck.pptx>

Se ghi de len chinh <deck.pptx> — tu backup file truoc khi chay neu can.
"""
import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Inches

SLIDE_W = Inches(13.333)
MARGIN = Inches(0.6)

# Vá lỗi python-pptx khi file .pptx có relationship MEDIA/VIDEO mồ côi (từ
# audio đã bị xoá thủ công trước đó) — _find_by_sha1 gốc giả định mọi phần tử
# trong _MediaParts đều có .sha1, crash AttributeError nếu gặp Part thường.
import pptx.package as _pptx_package


def _safe_find_by_sha1(self, sha1):
    for media_part in self:
        if getattr(media_part, "sha1", None) == sha1:
            return media_part
    return None


_pptx_package._MediaParts._find_by_sha1 = _safe_find_by_sha1


def remove_old_audio(slide):
    for shape in list(slide.shapes):
        if shape.shape_type == MSO_SHAPE_TYPE.MEDIA:
            shape._element.getparent().remove(shape._element)


def place_audio(slide, base_dir, rel_path, speaker_icon):
    path = base_dir / rel_path
    if not path.exists():
        print(f"  SKIP (missing mp3): {rel_path}")
        return False
    remove_old_audio(slide)
    sz = Inches(0.62)
    left = SLIDE_W - MARGIN - sz
    top = Inches(0.35)
    poster = str(speaker_icon) if speaker_icon.exists() else None
    mv = slide.shapes.add_movie(str(path), left, top, sz, sz,
                                 poster_frame_image=poster,
                                 mime_type="audio/mpeg")
    mv.line.fill.background()
    return True


def main(argv):
    if len(argv) != 3:
        print("Usage: python sync_audio_to_pptx.py <lesson.json> <deck.pptx>",
              file=sys.stderr)
        return 2
    json_path = Path(argv[1])
    pptx_path = Path(argv[2])
    speaker_icon = Path(__file__).with_name("speaker.png")

    spec = json.loads(json_path.read_text(encoding="utf-8"))
    slides_spec = spec["slides"]

    prs = Presentation(str(pptx_path))
    n_pptx = len(prs.slides._sldIdLst)
    if n_pptx != len(slides_spec):
        print(f"MISMATCH so luong slide: pptx={n_pptx} json={len(slides_spec)} "
              "— DUNG LAI, doi chieu tung slide truoc khi ghep audio (co the "
              "slide da bi tach/xoa khi sua tay).")
        return 1

    done = 0
    for i, (slide, s) in enumerate(zip(prs.slides, slides_spec), start=1):
        rel = s.get("audio")
        if not rel:
            continue
        if place_audio(slide, json_path.parent, rel, speaker_icon):
            done += 1
            print(f"OK slide {i:02d} <- {rel}")

    prs.save(str(pptx_path))
    print(f"DONE: da ghep {done} audio vao {pptx_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
