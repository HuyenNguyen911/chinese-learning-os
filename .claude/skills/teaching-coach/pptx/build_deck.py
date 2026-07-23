#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_deck.py — Data-driven renderer cho bài giảng tiếng Trung -> PPTX.

Dùng bởi skill teaching-coach. Nhận 1 file JSON mô tả bài giảng (danh sách block:
title/section/vocab/grammar/table/dialogue/reading/bullets/exercise/answers/blank)
và render ra .pptx với design system cố định:
  - Header dải đỏ full-width + tab CJK (kicker) + tiêu đề (1 ngôn ngữ)
  - Vocab dạng BẢNG cân cột: 汉字 | Pinyin | Nghĩa
  - Nội dung canh giữa theo chiều dọc (không dồn 1 góc, không thừa chỗ)
  - Hỗ trợ ảnh minh hoạ (key "image") + mẹo ghi nhớ (key "tip")

Chạy:
    python build_deck.py <lesson.json> <output.pptx>

Cần: python-pptx, Pillow. Không cần internet lúc render.
"""

import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

try:
    from PIL import Image
    _HAS_PIL = True
except Exception:
    _HAS_PIL = False

DEFAULT_THEME = {
    "accent": "8E2B20",
    "accent_dark": "5F160D",
    "accent_soft": "F7E4E1",
    "ink": "1F2933",
    "muted": "6B7683",
    "bg": "FFFFFF",
    "band": "F4F5F7",
    "cjk_font": "Microsoft YaHei",
    "text_font": "Calibri",
}

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN = Inches(0.6)
BAND_H = Inches(1.32)


class DeckBuilder:
    def __init__(self, spec):
        self.spec = spec
        self.meta = spec.get("meta", {})
        self.theme = {**DEFAULT_THEME, **spec.get("theme", {})}
        self.base = Path(spec.get("_base", "."))
        self.prs = Presentation()
        self.prs.slide_width = SLIDE_W
        self.prs.slide_height = SLIDE_H
        self.blank = self.prs.slide_layouts[6]

    # -- helpers -----------------------------------------------------------
    def _rgb(self, key):
        return RGBColor.from_string(self.theme[key])

    def _new_slide(self, bg=None):
        slide = self.prs.slides.add_slide(self.blank)
        rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
        rect.fill.solid()
        rect.fill.fore_color.rgb = self._rgb(bg or "bg")
        rect.line.fill.background()
        rect.shadow.inherit = False
        rect._element.addprevious(rect._element)
        return slide

    def _textbox(self, slide, left, top, width, height, anchor=None):
        box = slide.shapes.add_textbox(left, top, width, height)
        tf = box.text_frame
        tf.word_wrap = True
        if anchor is not None:
            tf.vertical_anchor = anchor
        return box, tf

    def _set_run(self, run, text, size, color="ink", bold=False,
                 font=None, italic=False, cjk=False):
        run.text = text
        f = run.font
        f.size = Pt(size)
        f.bold = bold
        f.italic = italic
        # Đồng nhất font: chữ Latin/Việt LUÔN dùng text_font (hoặc override).
        # Chữ Hán trong cùng run tự dùng cjk_font qua thuộc tính east-asian /
        # complex-script — nên không còn cảnh chữ Việt bị nhảy sang YaHei.
        f.name = font or self.theme["text_font"]
        f.color.rgb = self._rgb(color)
        rPr = run._r.get_or_add_rPr()
        for tag in ("a:ea", "a:cs"):
            rPr.append(rPr.makeelement(qn(tag), {"typeface": self.theme["cjk_font"]}))

    def _band_header(self, slide, title, kicker=None):
        band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, BAND_H)
        band.fill.solid()
        band.fill.fore_color.rgb = self._rgb("accent")
        band.line.fill.background()
        band.shadow.inherit = False
        if kicker:
            tab = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, MARGIN, Inches(0.16),
                Inches(1.5), Inches(0.42))
            tab.fill.solid()
            tab.fill.fore_color.rgb = self._rgb("accent_dark")
            tab.line.fill.background()
            tab.shadow.inherit = False
            tf = tab.text_frame
            tf.word_wrap = True
            tf.margin_top = Pt(2); tf.margin_bottom = Pt(2)
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            self._set_run(p.add_run(), kicker, 16, color="bg", bold=True, cjk=True)
            title_top = Inches(0.62)
        else:
            title_top = Inches(0.30)
        box, tf = self._textbox(slide, MARGIN, title_top,
                                SLIDE_W - 2 * MARGIN, Inches(0.62),
                                anchor=MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]
        self._set_run(p.add_run(), title, 27, color="bg", bold=True, cjk=True)

    def _place_audio(self, slide, rel_path):
        """Nhúng audio (mp3) làm nút 🔊 ở góc phải dải header. PowerPoint nhận
        là đối tượng Sound (MediaType=Sound), bấm/di chuột để phát giọng bản địa.
        Chỉ chạy trong PowerPoint thật (desktop/app) — trình xem Drive không phát."""
        path = self.base / rel_path
        if not path.exists():
            return
        icon = Path(__file__).with_name("speaker.png")
        sz = Inches(0.62)
        left = SLIDE_W - MARGIN - sz
        top = Inches(0.35)
        poster = str(icon) if icon.exists() else None
        mv = slide.shapes.add_movie(str(path), left, top, sz, sz,
                                    poster_frame_image=poster,
                                    mime_type="audio/mpeg")
        mv.line.fill.background()

    def _content_top(self):
        return BAND_H + Inches(0.30)

    def _content_area_h(self):
        return SLIDE_H - self._content_top() - Inches(0.4)

    def _place_image(self, slide, rel_path, left, top, box_w, box_h):
        path = self.base / rel_path
        if not path.exists():
            ph = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                        left, top, box_w, box_h)
            ph.fill.solid(); ph.fill.fore_color.rgb = self._rgb("band")
            ph.line.color.rgb = self._rgb("muted"); ph.line.width = Pt(0.5)
            ph.shadow.inherit = False
            tf = ph.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            self._set_run(p.add_run(), "[hình: %s]" % rel_path, 11, color="muted",
                          italic=True)
            return
        if _HAS_PIL:
            with Image.open(str(path)) as im:
                iw, ih = im.size
        else:
            iw, ih = 4, 3
        scale = min(box_w / iw, box_h / ih)
        w = int(iw * scale); h = int(ih * scale)
        l = int(left + (box_w - w) / 2)
        t = int(top + (box_h - h) / 2)
        slide.shapes.add_picture(str(path), Emu(l), Emu(t), Emu(w), Emu(h))

    def _split_image_col(self, s, img_w, default_side="right", gap=Inches(0.4)):
        """Chia slide thành cột chữ + cột ảnh. `image_side` = 'left'|'right'
        (tùy chọn trong JSON) để đổi bên cho đa dạng. Không có ảnh → chữ full."""
        if not s.get("image"):
            return MARGIN, SLIDE_W - 2 * MARGIN, None, img_w
        side = s.get("image_side", default_side)
        if side == "left":
            img_left = MARGIN
            txt_left = MARGIN + img_w + gap
            txt_w = SLIDE_W - MARGIN - txt_left
        else:
            txt_left = MARGIN
            img_left = SLIDE_W - MARGIN - img_w
            txt_w = img_left - gap - txt_left
        return txt_left, txt_w, img_left, img_w

    def _fill_cell(self, cell, text, size, color="ink", bold=False,
                   cjk=False, italic=False, align=PP_ALIGN.LEFT):
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = Pt(10); cell.margin_right = Pt(8)
        cell.margin_top = Pt(3); cell.margin_bottom = Pt(3)
        tf = cell.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.alignment = align
        self._set_run(p.add_run(), text, size, color=color, bold=bold,
                      italic=italic, cjk=cjk)

    def _tip_paragraph(self, tf, first, text):
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        p.space_before = Pt(14)
        self._set_run(p.add_run(), "🔑 Mẹo ghi nhớ: ", 15, color="accent", bold=True)
        self._set_run(p.add_run(), text, 15, color="ink", bold=False, cjk=True)

    # -- auto-fit cho các slide dạng textbox (grammar/bullets/reading) -----
    # Trước đây các slide này neo MSO_ANCHOR.MIDDLE với chiều cao cố định:
    # ít nội dung thì chữ dồn giữa trang, nhiều nội dung thì tràn lên đè cả
    # header. Dùng lại đúng ý tưởng đã chứng minh hiệu quả ở _slide_dialogue
    # (ước lượng chiều cao "tự nhiên" rồi co font/spacing nếu vượt khung) +
    # neo TOP để nội dung luôn bắt đầu ngay dưới header, nhất quán dù ít/nhiều.
    def _line_h(self, pt):
        return int(Pt(pt) * 1.28)

    def _wrap_lines(self, text, width_emu, pt, cjk=False):
        if not text:
            return 1
        avg_char_w = Pt(pt) * (1.0 if cjk else 0.52)
        per_line = max(1, int(width_emu / avg_char_w))
        return max(1, -(-len(str(text)) // per_line))

    def _fit_scale(self, natural_h, avail_h):
        return min(1.0, avail_h / natural_h) if natural_h else 1.0

    # -- render dispatch ---------------------------------------------------
    def render(self):
        for i, s in enumerate(self.spec.get("slides", [])):
            stype = s.get("type", "bullets")
            handler = getattr(self, f"_slide_{stype}", None)
            if handler is None:
                raise ValueError("Slide #%d: type '%s' không hỗ trợ." % (i, stype))
            handler(s)
            if s.get("audio"):
                self._place_audio(slide=self.prs.slides[-1], rel_path=s["audio"])
        return self.prs

    def _slide_title(self, s):
        slide = self._new_slide(bg="accent")
        has_img = bool(s.get("image"))
        txt_w = (SLIDE_W - 2 * MARGIN) if not has_img else Inches(7.3)
        align = PP_ALIGN.CENTER if not has_img else PP_ALIGN.LEFT
        box, tf = self._textbox(slide, MARGIN, Inches(2.1), txt_w, Inches(3.3),
                                anchor=MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]; p.alignment = align
        self._set_run(p.add_run(), s.get("title", ""), 44, color="bg", bold=True,
                      cjk=True)
        if s.get("subtitle"):
            p = tf.add_paragraph(); p.alignment = align; p.space_before = Pt(10)
            self._set_run(p.add_run(), s["subtitle"], 20, color="accent_soft")
        # Vắng key "footer" -> mặc định lấy meta.lesson; đặt "" -> ẩn hẳn.
        footer = s.get("footer", self.meta.get("lesson"))
        if footer:
            p = tf.add_paragraph(); p.alignment = align; p.space_before = Pt(6)
            self._set_run(p.add_run(), footer, 14, color="accent_soft")
        if has_img:
            self._place_image(slide, s["image"], SLIDE_W - MARGIN - Inches(4.9),
                              Inches(1.6), Inches(4.9), Inches(4.3))

    def _slide_section(self, s):
        slide = self._new_slide(bg="band")
        box, tf = self._textbox(slide, MARGIN, Inches(2.6),
                                SLIDE_W - 2 * MARGIN, Inches(2.3),
                                anchor=MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        self._set_run(p.add_run(), s.get("title", ""), 36, color="accent",
                      bold=True, cjk=True)
        if s.get("subtitle"):
            p = tf.add_paragraph(); p.alignment = PP_ALIGN.CENTER; p.space_before = Pt(10)
            self._set_run(p.add_run(), s["subtitle"], 18, color="muted", cjk=True)

    # -- vocab: BẢNG cân cột 汉字 | Pinyin | Nghĩa ------------------------
    def _slide_vocab(self, s):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", "Từ vựng mới"), s.get("kicker"))
        items = s.get("items", [])
        top = self._content_top()
        area_h = self._content_area_h()
        tleft, tw, img_left, img_w = self._split_image_col(
            s, Inches(4.2), default_side="left")
        example = s.get("example")
        has_img = bool(s.get("image"))
        table_h = area_h
        if example and not has_img:
            ex_h = Inches(0.85)
            table_h = area_h - ex_h - Inches(0.14)
        self._vocab_table(slide, items, tleft, top, tw, table_h)
        if has_img:
            img_h = self._image_fit_height(
                s["image"], img_w,
                int(area_h * 0.62) if example else area_h)
            self._place_image(slide, s["image"], img_left, top, img_w, img_h)
            if example:
                ex_top = top + img_h + Inches(0.22)
                ex_h = (top + area_h) - ex_top
                if ex_h > Inches(0.35):
                    self._vocab_example(slide, example, img_left, ex_top,
                                        img_w, ex_h)
        elif example:
            ex_top = top + table_h + Inches(0.14)
            self._vocab_example(slide, example, tleft, ex_top, tw, ex_h)

    def _image_fit_height(self, rel_path, box_w, max_h):
        """Chiều cao hiển thị THẬT của ảnh khi ép vừa bề rộng box_w (giữ tỉ lệ),
        giới hạn tối đa max_h — để không kéo giãn ảnh lấp đầy hết cột dọc."""
        path = self.base / rel_path
        if not (path.exists() and _HAS_PIL):
            return max_h
        try:
            with Image.open(str(path)) as im:
                iw, ih = im.size
        except Exception:
            return max_h
        h = int(box_w * ih / iw)
        return min(h, max_h)

    def _vocab_example(self, slide, example, left, top, width, height):
        # Chữ thường, KHÔNG khung/nền — tránh lệch form khi cột ảnh hẹp hơn bảng.
        box, tf = self._textbox(slide, left, top, width, height)
        p = tf.paragraphs[0]
        self._set_run(p.add_run(), "例句  ", 12, color="accent", bold=True)
        self._set_run(p.add_run(), example.get("hz", ""), 15, color="ink",
                      bold=True, cjk=True)
        if example.get("py"):
            p2 = tf.add_paragraph(); p2.space_before = Pt(3)
            self._set_run(p2.add_run(), example["py"], 11, color="accent",
                          italic=True)
        if example.get("vn"):
            p3 = tf.add_paragraph(); p3.space_before = Pt(3)
            self._set_run(p3.add_run(), example["vn"], 12, color="muted")

    def _vocab_table(self, slide, items, left, top, width, height):
        # Nếu item có key "color" (hex) -> chèn cột "ô màu thật" (swatch) cho
        # bài dạy màu sắc: từ Hán ↔ màu trực quan.
        has_sw = any(it.get("color") for it in items)
        if has_sw:
            widths = [0.22, 0.12, 0.28, 0.38]
            headers = ["汉字", "Màu", "Pinyin", "Nghĩa"]
        else:
            widths = [0.26, 0.36, 0.38]
            headers = ["汉字", "Pinyin", "Nghĩa"]
        ncol = len(headers)
        nrow = len(items) + 1
        gfx = slide.shapes.add_table(nrow, ncol, left, top, width, height)
        table = gfx.table
        for i, w in enumerate(widths):
            table.columns[i].width = int(width * w)
        rh = int(height / nrow)
        for r in range(nrow):
            table.rows[r].height = rh
        for c, h in enumerate(headers):
            cell = table.cell(0, c)
            cell.fill.solid(); cell.fill.fore_color.rgb = self._rgb("accent")
            self._fill_cell(cell, h, 15, color="bg", bold=True, cjk=True,
                            align=PP_ALIGN.CENTER)
        for r, it in enumerate(items, start=1):
            bg = "band" if r % 2 == 0 else "bg"
            c0 = table.cell(r, 0); c0.fill.solid(); c0.fill.fore_color.rgb = self._rgb(bg)
            self._fill_cell(c0, it.get("hz", ""), 23, color="ink", bold=True,
                            cjk=True, align=PP_ALIGN.CENTER)
            ci = 1
            if has_sw:
                sw = table.cell(r, 1); sw.fill.solid()
                sw.fill.fore_color.rgb = self._rgb(bg)
                hexc = it.get("color")
                if hexc:
                    # Chip bo góc CÓ VIỀN (để màu trắng/nhạt vẫn nổi trên nền).
                    col_x = left + int(width * widths[0])
                    col_w = int(width * widths[1])
                    chip_h = int(rh * 0.55)
                    chip_w = min(int(col_w * 0.64), int(chip_h * 1.9))
                    chip_x = col_x + (col_w - chip_w) // 2
                    chip_y = top + r * rh + (rh - chip_h) // 2
                    chip = slide.shapes.add_shape(
                        MSO_SHAPE.ROUNDED_RECTANGLE,
                        Emu(chip_x), Emu(chip_y), Emu(chip_w), Emu(chip_h))
                    chip.fill.solid()
                    chip.fill.fore_color.rgb = RGBColor.from_string(hexc)
                    chip.line.color.rgb = self._rgb("muted"); chip.line.width = Pt(1)
                    chip.shadow.inherit = False
                ci = 2
            cpy = table.cell(r, ci); cpy.fill.solid(); cpy.fill.fore_color.rgb = self._rgb(bg)
            self._fill_cell(cpy, it.get("py", ""), 15, color="accent", italic=True,
                            align=PP_ALIGN.LEFT)
            cvn = table.cell(r, ci + 1); cvn.fill.solid(); cvn.fill.fore_color.rgb = self._rgb(bg)
            self._fill_cell(cvn, it.get("vn", ""), 15, color="ink", align=PP_ALIGN.LEFT)

    def _slide_grammar(self, s):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", "Ngữ pháp"), s.get("kicker"))
        top = self._content_top()
        area_h = self._content_area_h()
        has_img = bool(s.get("image"))
        txt_left, txt_w, img_left, img_w = self._split_image_col(s, Inches(4.7))
        box, tf = self._textbox(slide, txt_left, top, txt_w, area_h,
                                anchor=MSO_ANCHOR.MIDDLE)
        first = True
        point = s.get("point")
        if point:
            for line in ([point] if isinstance(point, str) else point):
                p = tf.paragraphs[0] if first else tf.add_paragraph()
                if not first:
                    p.space_before = Pt(4)
                self._set_run(p.add_run(), line, 20, color="ink", bold=True,
                              cjk=True)
                first = False
        for ex in s.get("examples", []):
            # Pinyin nằm CÙNG DÒNG với Hán tự (theo ý user), nghĩa xuống dòng;
            # giãn RỘNG giữa các ví dụ để tách cụm cho dễ đọc.
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.space_before = Pt(20)
            self._set_run(p.add_run(), ex.get("hz", ""), 26, color="ink", bold=True,
                          cjk=True)
            if ex.get("py"):
                self._set_run(p.add_run(), "  " + ex["py"], 15, color="accent",
                              italic=True)
            if ex.get("vn"):
                p2 = tf.add_paragraph(); p2.space_before = Pt(3)
                self._set_run(p2.add_run(), ex["vn"], 15, color="muted")
        if s.get("note"):
            p = tf.add_paragraph(); p.space_before = Pt(15)
            self._set_run(p.add_run(), "• " + s["note"], 15, color="ink", cjk=True)
        if s.get("tip"):
            self._tip_paragraph(tf, first, s["tip"]); first = False
        if s.get("source"):
            p = tf.add_paragraph(); p.space_before = Pt(12)
            self._set_run(p.add_run(), "📖 " + s["source"], 12, color="muted",
                          italic=True)
        if has_img:
            self._place_image(slide, s["image"], img_left, top, img_w, area_h)

    def _slide_table(self, s):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", "So sánh"), s.get("kicker"))
        headers = s.get("headers", [])
        data = s.get("rows", [])
        ncol = len(headers); nrow = len(data) + 1
        top = self._content_top(); area_h = self._content_area_h()
        width = SLIDE_W - 2 * MARGIN
        rh = min(Inches(0.82), int(area_h / nrow))
        table_h = rh * nrow
        # canh giữa theo chiều dọc để không thừa khoảng trống phía dưới
        ttop = top + max(0, int((area_h - table_h) / 2))
        gfx = slide.shapes.add_table(nrow, ncol, MARGIN, ttop, width, table_h)
        table = gfx.table
        for r in range(nrow):
            table.rows[r].height = int(rh)
        cjk_cols = s.get("cjk_cols")
        for c, htext in enumerate(headers):
            cell = table.cell(0, c)
            cell.fill.solid(); cell.fill.fore_color.rgb = self._rgb("accent")
            self._fill_cell(cell, htext, 15, color="bg", bold=True, cjk=True,
                            align=PP_ALIGN.CENTER)
        for r, row in enumerate(data, start=1):
            for c in range(ncol):
                cell = table.cell(r, c)
                cell.fill.solid()
                cell.fill.fore_color.rgb = self._rgb("band" if r % 2 == 0 else "bg")
                text = row[c] if c < len(row) else ""
                is_cjk = (c in cjk_cols) if cjk_cols is not None else (c > 0)
                self._fill_cell(cell, text, 15, color="ink", bold=(c == 0),
                                cjk=is_cjk, align=PP_ALIGN.LEFT)

    def _slide_dialogue(self, s):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", "Hội thoại mẫu"), s.get("kicker"))
        turns = s.get("turns", [])
        top = self._content_top()
        if not turns:
            return
        n = len(turns)
        avail_h = int(SLIDE_H - top - Inches(0.30))

        def nlines(t):
            return 1 + (1 if t.get("py") else 0) + (1 if t.get("vn") else 0)

        # Kích thước "tự nhiên"; nếu tổng cao hơn khung thì co lại theo hệ số
        # scale (cả chiều cao lẫn cỡ chữ) để KHÔNG tràn khung dù nhiều lượt.
        gap0 = int(Inches(0.16)); line0 = int(Inches(0.40)); pad0 = int(Inches(0.30))
        natural = sum(line0 * nlines(t) + pad0 for t in turns) + gap0 * (n - 1)
        scale = min(1.0, avail_h / natural) if natural else 1.0
        line_h = int(line0 * scale); pad = int(pad0 * scale); gap = int(gap0 * scale)
        hz_sz = max(15, int(22 * scale)); py_sz = max(11, int(14 * scale))
        vn_sz = max(10, int(13 * scale)); spk_sz = max(11, int(13 * scale))
        bubble_w = Inches(7.6)
        first_speaker = turns[0].get("speaker")
        y = int(top)
        for t in turns:
            is_left = t.get("speaker") == first_speaker
            bubble_h = line_h * nlines(t) + pad
            left = MARGIN if is_left else int(SLIDE_W - MARGIN - bubble_w)
            bubble = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                            Emu(left), Emu(y), bubble_w, Emu(bubble_h))
            bubble.fill.solid()
            bubble.fill.fore_color.rgb = self._rgb("band" if is_left else "accent_soft")
            bubble.line.color.rgb = self._rgb("muted" if is_left else "accent")
            bubble.line.width = Pt(0.5); bubble.shadow.inherit = False
            tf = bubble.text_frame; tf.word_wrap = True
            tf.margin_left = Pt(12); tf.margin_top = Pt(5); tf.margin_bottom = Pt(5)
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
            spk = t.get("speaker", "")
            if spk:
                self._set_run(p.add_run(), spk + ": ", spk_sz, color="accent", bold=True)
            self._set_run(p.add_run(), t.get("hz", ""), hz_sz, color="ink", bold=True,
                          cjk=True)
            if t.get("py"):
                p = tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT
                self._set_run(p.add_run(), t["py"], py_sz, color="accent", italic=True)
            if t.get("vn"):
                p = tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT
                self._set_run(p.add_run(), t["vn"], vn_sz, color="muted")
            y = y + bubble_h + gap

    def _slide_reading(self, s):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", "Đọc thêm"), s.get("kicker", "阅读"))
        top = self._content_top(); area_h = self._content_area_h()
        box, tf = self._textbox(slide, MARGIN, top, SLIDE_W - 2 * MARGIN, area_h,
                                anchor=MSO_ANCHOR.MIDDLE)
        first = True
        for grp in s.get("groups", []):
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.space_before = Pt(12)
            self._set_run(p.add_run(), grp.get("label", ""), 17, color="accent",
                          bold=True)
            for it in grp.get("items", []):
                p = tf.add_paragraph(); p.space_before = Pt(4)
                self._set_run(p.add_run(), "•  ", 15, color="accent", bold=True)
                self._set_run(p.add_run(), str(it), 15, color="ink", cjk=True)

    def _slide_blank(self, s):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", ""), s.get("kicker"))
        if s.get("placeholder"):
            top = self._content_top(); area_h = self._content_area_h()
            box, tf = self._textbox(slide, MARGIN, top, SLIDE_W - 2 * MARGIN, area_h,
                                    anchor=MSO_ANCHOR.MIDDLE)
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            self._set_run(p.add_run(), s["placeholder"], 14, color="muted",
                          italic=True)

    def _slide_exercise(self, s):
        self._list_slide(s, "Luyện tập", numbered=True)

    def _slide_answers(self, s):
        self._list_slide(s, "Đáp án", numbered=True)

    def _slide_bullets(self, s):
        self._list_slide(s, "Nội dung", numbered=False)

    def _list_slide(self, s, default_title, numbered):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", default_title), s.get("kicker"))
        top = self._content_top(); area_h = self._content_area_h()
        has_img = bool(s.get("image"))
        txt_left, txt_w, img_left, img_w = self._split_image_col(s, Inches(4.6))
        box, tf = self._textbox(slide, txt_left, top, txt_w, area_h,
                                anchor=MSO_ANCHOR.MIDDLE)
        first = True
        if s.get("instructions"):
            p = tf.paragraphs[0]
            self._set_run(p.add_run(), s["instructions"], 16, color="accent",
                          italic=True)
            first = False
        items = s.get("items", s.get("bullets", []))
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.space_before = Pt(13)
            prefix = ("%d. " % (i + 1)) if numbered else "•  "
            self._set_run(p.add_run(), prefix, 20, color="accent", bold=True)
            self._set_run(p.add_run(), str(item), 20, color="ink", cjk=True)
        if s.get("tip"):
            self._tip_paragraph(tf, first, s["tip"])
        if has_img:
            self._place_image(slide, s["image"], img_left, top, img_w, area_h)


def main(argv):
    if len(argv) != 3:
        print("Usage: python build_deck.py <lesson.json> <output.pptx>",
              file=sys.stderr)
        return 2
    src = Path(argv[1]); out = Path(argv[2])
    spec = json.loads(src.read_text(encoding="utf-8"))
    spec.setdefault("_base", str(src.parent))
    prs = DeckBuilder(spec).render()
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))
    print("OK: %d slide -> %s" % (len(spec.get("slides", [])), out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
