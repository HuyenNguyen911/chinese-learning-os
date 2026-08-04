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
        self._cur_cjk_cols = None

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

    def _place_footer_note(self, slide, text):
        """Dòng chú thích nhỏ ở đáy slide (vd đối chiếu giáo trình khác) — dùng
        chung cho MỌI loại slide qua render(), thay vì phải để riêng 1 slide
        '对照' đứng một mình."""
        box, tf = self._textbox(slide, MARGIN, SLIDE_H - Inches(0.42),
                                SLIDE_W - 2 * MARGIN, Inches(0.32),
                                anchor=MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]
        self._set_run(p.add_run(), "📖 " + text, 11, color="muted", italic=True,
                      cjk=True)

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
        (tùy chọn trong JSON) để đổi bên cho đa dạng. `image_w_in` (số inch)
        cho phép slide xin cột ẢNH HẸP HƠN mặc định — dùng khi ảnh chỉ là 1
        icon nhỏ (không cần cả cột lớn), để dành chỗ cho bảng/nội dung dày
        (vd bảng 生词 nhiều từ) mà vẫn có icon. Không có ảnh → chữ full."""
        if not s.get("image"):
            return MARGIN, SLIDE_W - 2 * MARGIN, None, img_w
        if s.get("image_w_in"):
            img_w = Inches(s["image_w_in"])
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

    def _footer_reserved_h(self, s):
        """Chiều cao dành riêng ở đáy slide cho "tip" (mẹo ghi nhớ) — TÁCH
        khỏi luồng nội dung chính thay vì chèn lẫn vào cuối bullet/grammar
        (review buổi 01: mẹo phải là footer, không phải nội dung chính).
        footer_note đã có sẵn 1 dải cố định trong _content_area_h; tip cần
        thêm 1 dải nữa ngay phía trên đó."""
        return Inches(0.38) if s.get("tip") else Inches(0)

    def _place_tip(self, slide, text, has_footer_note):
        top = SLIDE_H - Inches(0.42) - (Inches(0.36) if has_footer_note else Inches(0))
        box, tf = self._textbox(slide, MARGIN, top, SLIDE_W - 2 * MARGIN,
                                Inches(0.34), anchor=MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]
        self._set_run(p.add_run(), "🔑 Mẹo ghi nhớ: ", 13, color="accent", bold=True)
        self._set_run(p.add_run(), text, 13, color="ink", cjk=True)

    # -- auto-fit cho các slide dạng textbox (grammar/bullets/reading) -----
    # Trước đây các slide này neo MSO_ANCHOR.MIDDLE với chiều cao cố định:
    # ít nội dung thì chữ dồn giữa trang, nhiều nội dung thì tràn lên đè cả
    # header. Dùng lại đúng ý tưởng đã chứng minh hiệu quả ở _slide_dialogue
    # (ước lượng chiều cao "tự nhiên" rồi co font/spacing nếu vượt khung) +
    # neo TOP để nội dung luôn bắt đầu ngay dưới header, nhất quán dù ít/nhiều.
    def _line_h(self, pt):
        return int(Pt(pt) * 1.28)

    def _wrap_lines(self, text, width_emu, pt, cjk=False, bold=False):
        if not text:
            return 1
        avg_char_w = Pt(pt) * (1.0 if cjk else 0.52)
        if bold:
            # Chữ đậm rộng hơn chữ thường ~12% — không tính vào sẽ ước lượng
            # thiếu số dòng cần wrap, khiến chiều cao hàng bảng bị co quá tay
            # (review buổi 02: chữ Hán cột đậm bị rớt dòng dù đã tính wrap).
            avg_char_w = int(avg_char_w * 1.12)
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
            if s.get("tip") and stype in ("bullets", "exercise", "answers", "grammar"):
                self._place_tip(self.prs.slides[-1], s["tip"],
                                has_footer_note=bool(s.get("footer_note")))
            if s.get("footer_note"):
                self._place_footer_note(self.prs.slides[-1], s["footer_note"])
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
        # Nếu item có key "ex" (câu ví dụ dùng từ) -> thêm cột "Ví dụ" cuối bảng.
        has_sw = any(it.get("color") for it in items)
        has_ex = any(it.get("ex") for it in items)
        if has_sw and has_ex:
            widths = [0.13, 0.09, 0.15, 0.23, 0.40]
            headers = ["汉字", "Màu", "Pinyin", "Nghĩa", "Ví dụ"]
        elif has_sw:
            widths = [0.22, 0.12, 0.28, 0.38]
            headers = ["汉字", "Màu", "Pinyin", "Nghĩa"]
        elif has_ex:
            widths = [0.14, 0.18, 0.26, 0.42]
            headers = ["汉字", "Pinyin", "Nghĩa", "Ví dụ"]
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
        # Font co theo chiều cao hàng thực tế — nrow cố định 23/15pt tràn ô
        # khi 1 slide nhồi nhiều từ (vd 13 từ); scale xuống cho hàng thấp,
        # KHÔNG phóng to quá cỡ gốc khi hàng cao (nrow ít).
        ideal_rh = Inches(0.52)
        fscale = min(1.0, rh / ideal_rh) if ideal_rh else 1.0
        hz_sz = max(14, int(23 * fscale))
        py_sz = vn_sz = max(10, int(15 * fscale))
        hdr_sz = max(11, int(15 * fscale))
        for c, h in enumerate(headers):
            cell = table.cell(0, c)
            cell.fill.solid(); cell.fill.fore_color.rgb = self._rgb("accent")
            self._fill_cell(cell, h, hdr_sz, color="bg", bold=True, cjk=True,
                            align=PP_ALIGN.CENTER)
        for r, it in enumerate(items, start=1):
            bg = "band" if r % 2 == 0 else "bg"
            c0 = table.cell(r, 0); c0.fill.solid(); c0.fill.fore_color.rgb = self._rgb(bg)
            self._fill_cell(c0, it.get("hz", ""), hz_sz, color="ink", bold=True,
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
            self._fill_cell(cpy, it.get("py", ""), py_sz, color="accent", italic=True,
                            align=PP_ALIGN.LEFT)
            cvn = table.cell(r, ci + 1); cvn.fill.solid(); cvn.fill.fore_color.rgb = self._rgb(bg)
            self._fill_cell(cvn, it.get("vn", ""), vn_sz, color="ink", align=PP_ALIGN.LEFT)
            if has_ex:
                cex = table.cell(r, ci + 2); cex.fill.solid()
                cex.fill.fore_color.rgb = self._rgb(bg)
                self._fill_cell(cex, it.get("ex", ""), 13, color="muted", cjk=True,
                                align=PP_ALIGN.LEFT)

    # -- wordcard: 1 từ / 1 slide — 2 CỘT dùng hết chiều ngang: trái = ảnh +
    #    汉字/pinyin/nghĩa; phải = tối đa 3 câu ví dụ. Dùng khi cần đào sâu
    #    từng từ (thay cho bảng vocab dồn nhiều từ/slide).
    def _slide_wordcard(self, s):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", s.get("hz", "生词")), s.get("kicker"))
        top = self._content_top()
        area_h = self._content_area_h()
        content_w = SLIDE_W - 2 * MARGIN
        gap = Inches(0.5)
        left_w = int(content_w * 0.42)
        right_left = MARGIN + left_w + gap
        right_w = SLIDE_W - MARGIN - right_left

        # --- Cột trái: ảnh vuông trên, 汉字/pinyin/nghĩa/từ loại dưới -------
        has_img = bool(s.get("image"))
        if has_img:
            img_side = min(left_w, Inches(3.4))
            img_left = MARGIN + (left_w - img_side) // 2
            self._place_image(slide, s["image"], img_left, top, img_side, img_side)
            info_top = top + img_side + Inches(0.15)
        else:
            info_top = top
        info_h = top + area_h - info_top
        box, tf = self._textbox(slide, MARGIN, info_top, left_w, info_h,
                                anchor=MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        self._set_run(p.add_run(), s.get("hz", ""), 54, color="ink", bold=True, cjk=True)
        if s.get("pos"):
            self._set_run(p.add_run(), "  " + s["pos"], 16, color="muted", italic=True)
        if s.get("py"):
            p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER; p2.space_before = Pt(6)
            self._set_run(p2.add_run(), s["py"], 22, color="accent", italic=True)
        if s.get("vn"):
            p3 = tf.add_paragraph(); p3.alignment = PP_ALIGN.CENTER; p3.space_before = Pt(4)
            self._set_run(p3.add_run(), s["vn"], 18, color="ink")

        # --- Cột phải: tối đa 3 câu ví dụ, canh giữa theo chiều dọc --------
        ebox, etf = self._textbox(slide, right_left, top, right_w, area_h,
                                  anchor=MSO_ANCHOR.MIDDLE)
        p = etf.paragraphs[0]
        self._set_run(p.add_run(), "例句", 16, color="accent", bold=True, cjk=True)
        for ex in s.get("examples", [])[:3]:
            p = etf.add_paragraph(); p.space_before = Pt(22)
            self._set_run(p.add_run(), "•  ", 18, color="accent", bold=True)
            self._set_run(p.add_run(), ex.get("hz", ""), 20, color="ink", bold=True,
                          cjk=True)
            if ex.get("py"):
                p2 = etf.add_paragraph(); p2.space_before = Pt(2)
                self._set_run(p2.add_run(), "     " + ex["py"], 14, color="accent",
                              italic=True)
            if ex.get("vn"):
                p3 = etf.add_paragraph(); p3.space_before = Pt(1)
                self._set_run(p3.add_run(), "     " + ex["vn"], 14, color="muted")

    def _slide_grammar(self, s):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", "Ngữ pháp"), s.get("kicker"))
        top = self._content_top()
        area_h = self._content_area_h() - self._footer_reserved_h(s)
        has_img = bool(s.get("image"))
        txt_left, txt_w, img_left, img_w = self._split_image_col(s, Inches(4.7))

        point = s.get("point")
        point_lines = ([point] if isinstance(point, str) else point) if point else []
        examples = s.get("examples", [])
        note = s.get("note"); source = s.get("source")

        # Ước lượng chiều cao "tự nhiên" ở cỡ chữ gốc rồi co scale nếu vượt
        # khung (xem _fit_scale) — tránh vừa dồn giữa trang (ít nội dung) vừa
        # tràn đè header (nhiều nội dung, vd slide có 5 ví dụ + note + tip).
        natural = 0
        for i, line in enumerate(point_lines):
            natural += self._wrap_lines(line, txt_w, 20, cjk=True) * self._line_h(20)
            natural += 0 if i == 0 else Pt(4)
        for ex in examples:
            natural += Pt(20) + self._line_h(26)
            if ex.get("vn"):
                natural += Pt(3) + self._line_h(15)
        if note:
            natural += Pt(15) + self._wrap_lines(note, txt_w, 15, cjk=True) * self._line_h(15)
        if source:
            natural += Pt(12) + self._line_h(12)
        scale = self._fit_scale(natural, area_h)

        def sz(pt, floor):
            return max(floor, int(pt * scale))

        box, tf = self._textbox(slide, txt_left, top, txt_w, area_h,
                                anchor=MSO_ANCHOR.TOP)
        first = True
        for i, line in enumerate(point_lines):
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            if not first:
                p.space_before = Pt(4 * scale)
            self._set_run(p.add_run(), line, sz(20, 13), color="ink", bold=True,
                          cjk=True)
            first = False
        for ex in examples:
            # Pinyin nằm CÙNG DÒNG với Hán tự (theo ý user), nghĩa xuống dòng;
            # giãn RỘNG giữa các ví dụ để tách cụm cho dễ đọc.
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.space_before = Pt(20 * scale)
            self._set_run(p.add_run(), ex.get("hz", ""), sz(26, 16), color="ink",
                          bold=True, cjk=True)
            if ex.get("py"):
                self._set_run(p.add_run(), "  " + ex["py"], sz(15, 11), color="accent",
                              italic=True)
            if ex.get("vn"):
                p2 = tf.add_paragraph(); p2.space_before = Pt(3 * scale)
                self._set_run(p2.add_run(), ex["vn"], sz(15, 11), color="muted")
        if note:
            p = tf.add_paragraph(); p.space_before = Pt(15 * scale)
            self._set_run(p.add_run(), "• " + note, sz(15, 11), color="ink", cjk=True)
            first = False
        if source:
            p = tf.add_paragraph(); p.space_before = Pt(12 * scale)
            self._set_run(p.add_run(), "📖 " + source, sz(12, 10), color="muted",
                          italic=True)
        if has_img:
            self._place_image(slide, s["image"], img_left, top, img_w, area_h)

    def _col_weights(self, headers, data, cjk_cols):
        """Bề rộng cột tỉ lệ theo độ dài nội dung DÀI NHẤT mỗi cột (thay vì
        chia đều) — cột chữ ngắn (vd 声母 1 ký tự) co lại, cột chữ dài (vd
        "Đọc gần giống") có thêm chỗ để không bị rớt dòng. Cột CJK tính
        rộng hơn/ký tự (chữ Hán vuông) so với cột Latin."""
        ncol = len(headers)
        weights = []
        for c in range(ncol):
            is_cjk = (c in cjk_cols) if cjk_cols is not None else (c > 0)
            max_len = len(str(headers[c]))
            for row in data:
                text = str(row[c]) if c < len(row) else ""
                max_len = max(max_len, len(text))
            per_char = 1.7 if is_cjk else 1.0
            weights.append(max(2.2, max_len * per_char))
        total = sum(weights)
        return [w / total for w in weights]

    def _row_heights(self, headers, data, widths_frac, width_emu, min_rh, max_rh):
        """Chiều cao MỖI HÀNG ước theo số dòng wrap thực tế (kế thừa
        _wrap_lines dùng ở list/grammar) — hàng nội dung dài cao hơn, hàng
        ngắn giữ compact, tránh chữ bị rớt/dồn khi ép 1 chiều cao cố định."""
        heights = []
        for row in [headers] + data:
            nlines = 1
            for c, w in enumerate(widths_frac):
                text = str(row[c]) if c < len(row) else ""
                is_cjk = (c in (self._cur_cjk_cols or [])) if self._cur_cjk_cols is not None else (c > 0)
                # Cột 0 luôn render đậm (_fill_cell bold=(c==0)) — phải khớp
                # bold=True ở đây để ước lượng đúng số dòng wrap thực tế.
                nlines = max(nlines, self._wrap_lines(
                    text, int(width_emu * w) - Pt(16), 15, cjk=is_cjk, bold=(c == 0)))
            heights.append(min(max_rh, max(min_rh, int(min_rh * (0.62 + 0.38 * nlines)))))
        return heights

    def _slide_table(self, s):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", "So sánh"), s.get("kicker"))
        headers = s.get("headers", [])
        data = s.get("rows", [])
        ncol = len(headers); nrow = len(data) + 1
        top = self._content_top(); area_h = self._content_area_h()
        tleft, width, img_left, img_w = self._split_image_col(s, Inches(3.6))
        if s.get("image"):
            self._place_image(slide, s["image"], img_left, top, img_w, area_h)
        cjk_cols = s.get("cjk_cols")
        self._cur_cjk_cols = cjk_cols
        note = s.get("note")
        note_h = Inches(0.4) if note else Inches(0)
        table_avail_h = area_h - note_h
        widths_frac = self._col_weights(headers, data, cjk_cols)
        min_rh = int(min(Inches(0.82), table_avail_h / nrow))
        row_h = self._row_heights(headers, data, widths_frac, width, min_rh,
                                  int(Inches(1.55)))
        table_h = sum(row_h)
        font_scale = 1.0
        if table_h > table_avail_h:
            shrink = table_avail_h / table_h
            row_h = [int(h * shrink) for h in row_h]
            table_h = sum(row_h)
            # Nén chiều cao hàng mà giữ nguyên cỡ chữ sẽ tràn/rớt dòng — co cả
            # font theo cùng hệ số (sàn 11pt để còn đọc được).
            font_scale = shrink
        hdr_sz = max(11, int(15 * font_scale))
        cell_sz = max(11, int(15 * font_scale))
        # canh giữa theo chiều dọc để không thừa khoảng trống phía dưới
        ttop = top + max(0, int((table_avail_h - table_h) / 2))
        gfx = slide.shapes.add_table(nrow, ncol, tleft, ttop, width, table_h)
        table = gfx.table
        for c, wf in enumerate(widths_frac):
            table.columns[c].width = int(width * wf)
        for r in range(nrow):
            table.rows[r].height = row_h[r]
        for c, htext in enumerate(headers):
            cell = table.cell(0, c)
            cell.fill.solid(); cell.fill.fore_color.rgb = self._rgb("accent")
            self._fill_cell(cell, htext, hdr_sz, color="bg", bold=True, cjk=True,
                            align=PP_ALIGN.CENTER)
        for r, row in enumerate(data, start=1):
            for c in range(ncol):
                cell = table.cell(r, c)
                cell.fill.solid()
                cell.fill.fore_color.rgb = self._rgb("band" if r % 2 == 0 else "bg")
                text = row[c] if c < len(row) else ""
                is_cjk = (c in cjk_cols) if cjk_cols is not None else (c > 0)
                self._fill_cell(cell, text, cell_sz, color="ink", bold=(c == 0),
                                cjk=is_cjk, align=PP_ALIGN.LEFT)
        if note:
            note_top = ttop + table_h + Inches(0.1)
            box, tf = self._textbox(slide, tleft, note_top, width,
                                    (top + area_h) - note_top)
            p = tf.paragraphs[0]
            self._set_run(p.add_run(), "🔍 So sánh: ", 13, color="accent", bold=True)
            self._set_run(p.add_run(), note, 13, color="ink", cjk=True)

    def _slide_info_grid(self, s):
        """N thẻ (ảnh + label CJK + caption Việt) xếp lưới trong 1 slide —
        dùng cho hồ sơ văn hoá 1 quốc gia (cờ/biểu tượng/thủ đô/ngôn ngữ/tiền
        tệ...) khi cần NHIỀU ảnh trên cùng 1 slide, khác _slide_vocab/
        _slide_grammar (chỉ hỗ trợ 1 ảnh/slide)."""
        slide = self._new_slide()
        self._band_header(slide, s.get("title", "Hồ sơ"), s.get("kicker"))
        cards = s.get("cards", [])
        if not cards:
            return
        top = self._content_top(); area_h = self._content_area_h()
        n = len(cards)
        ncols = n if n <= 4 else 4
        nrows = -(-n // ncols)
        gap = Inches(0.18)
        card_w = int((SLIDE_W - 2 * MARGIN - gap * (ncols - 1)) / ncols)
        card_h = int((area_h - gap * (nrows - 1)) / nrows)
        img_h = int(card_h * 0.52)
        for i, card in enumerate(cards):
            r, c = divmod(i, ncols)
            cx = int(MARGIN + c * (card_w + gap))
            cy = int(top + r * (card_h + gap))
            if card.get("image"):
                self._place_image(slide, card["image"], cx, cy, card_w, img_h)
            else:
                ph = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                            cx, cy, card_w, img_h)
                ph.fill.solid(); ph.fill.fore_color.rgb = self._rgb("band")
                ph.line.color.rgb = self._rgb("muted"); ph.line.width = Pt(0.5)
                ph.shadow.inherit = False
                tf = ph.text_frame; p = tf.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                self._set_run(p.add_run(), "[hình]", 11, color="muted", italic=True)
            label_top = cy + img_h + Inches(0.02)
            box, tf = self._textbox(slide, cx, label_top, card_w, Inches(0.26),
                                    anchor=MSO_ANCHOR.MIDDLE)
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            self._set_run(p.add_run(), card.get("label", ""), 15, color="accent",
                          bold=True, cjk=True)
            py = card.get("py")
            py_top = label_top + Inches(0.24)
            if py:
                box_py, tf_py = self._textbox(slide, cx, py_top, card_w, Inches(0.2),
                                              anchor=MSO_ANCHOR.MIDDLE)
                p_py = tf_py.paragraphs[0]; p_py.alignment = PP_ALIGN.CENTER
                self._set_run(p_py.add_run(), py, 10, color="muted", italic=True)
            cap = card.get("caption")
            if cap:
                cap_top = py_top + (Inches(0.2) if py else Inches(0.02))
                box2, tf2 = self._textbox(slide, cx, cap_top, card_w, Inches(0.28),
                                          anchor=MSO_ANCHOR.TOP)
                p2 = tf2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
                self._set_run(p2.add_run(), cap, 11, color="muted", cjk=True)

    def _speaker_icon(self, name):
        # CHỈ dùng emoji 1 codepoint — chuỗi ghép ZWJ (vd 🧑‍🏫) PowerPoint
        # không ráp được, hiển thị vỡ thành 2 icon rời (đã gặp ở review buổi 02).
        if "老师" in name:
            return "\U0001F469"  # 👩 teacher
        if name in ("小语", "AI小语"):
            return "\U0001F916"  # 🤖 AI
        if "们" in name or "学生" in name:
            return "\U0001F393"  # 🎓 students
        return "\U0001F642"  # 🙂

    AVATAR_PALETTE = ["2980B9", "27AE60", "D35400", "8E44AD", "C0392B", "16A085"]

    def _avatar_color(self, speaker_colors, speaker):
        if speaker not in speaker_colors:
            speaker_colors[speaker] = self.AVATAR_PALETTE[
                len(speaker_colors) % len(self.AVATAR_PALETTE)]
        return speaker_colors[speaker]

    def _place_avatar(self, slide, speaker, color_hex, cx, cy, d):
        """Chấm tròn màu + chữ cái/ chữ Hán đầu tên nhân vật, đè lên góc bong
        bóng thoại — thay cho ảnh chụp thật, giúp phân biệt nhân vật xuyên
        suốt các 课文 mà không cần tải ảnh ngoài."""
        circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, Emu(int(cx)), Emu(int(cy)),
                                      Emu(int(d)), Emu(int(d)))
        circ.fill.solid(); circ.fill.fore_color.rgb = RGBColor.from_string(color_hex)
        circ.line.color.rgb = self._rgb("bg"); circ.line.width = Pt(1.5)
        circ.shadow.inherit = False
        tf = circ.text_frame; tf.word_wrap = False
        tf.margin_left = 0; tf.margin_right = 0
        tf.margin_top = 0; tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        letter = (speaker or "?")[:1]
        d_inches = d / 914400.0
        self._set_run(p.add_run(), letter, max(12, int(d_inches * 30)),
                      color="bg", bold=True, cjk=True)

    def _slide_dialogue(self, s):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", "Hội thoại mẫu"), s.get("kicker"))
        turns = s.get("turns", [])
        top = self._content_top()
        if not turns:
            return
        # Ảnh ngữ cảnh (vd cảnh đón taxi) đặt 1 bên, khung thoại co vào bên
        # còn lại — cùng bố cục split-column đã dùng ở vocab/grammar/passage,
        # giúp học viên hình dung bối cảnh thay vì chỉ thấy bong bóng chữ nổi
        # trên nền trắng (review buổi 02: "khó xem, không liên tưởng").
        has_img = bool(s.get("image"))
        if has_img:
            txt_left, txt_w, img_left, img_w = self._split_image_col(
                s, Inches(4.2), default_side="left")
            self._place_image(slide, s["image"], img_left, top, img_w,
                              self._content_area_h())
        else:
            txt_left, txt_w = MARGIN, SLIDE_W - 2 * MARGIN
        uniq_speakers = []
        for t in turns:
            spk = t.get("speaker")
            if spk and spk not in uniq_speakers:
                uniq_speakers.append(spk)
        # >2 người nói thật (vd 王老师/小语/学生们): ép vào 2 cột trái/phải làm
        # 2 người "phe phải" dồn chung 1 cột, không biết ai đang nói + để
        # nhiều khoảng trắng giữa 2 cột trông như 2 hội thoại tách rời, RẤT
        # khó đọc (review buổi 02, 2 lần). Chuyển sang danh sách 1 CỘT, đọc
        # tuần tự trên→dưới như kịch bản — luôn rõ ràng bất kể bao nhiêu người.
        if len(uniq_speakers) > 2:
            self._dialogue_script(slide, turns, top, uniq_speakers, txt_left, txt_w)
        else:
            self._dialogue_bubbles(slide, turns, top, txt_left, txt_w)

    def _dialogue_script(self, slide, turns, top, uniq_speakers, txt_left=None, txt_w=None):
        # Swimlane: MỖI người nói 1 CỘT riêng, cùng hàng ngang = cùng lượt
        # thoại — vừa thấy AI ai đang nói (cột) vừa thấy thứ tự trước/sau
        # (hàng trên→dưới) cùng lúc, không cần đoán qua trái/phải hay icon
        # nhỏ nữa (review buổi 02: 1-cột vẫn không rõ ai nói khi nào).
        if txt_left is None:
            txt_left, txt_w = MARGIN, SLIDE_W - 2 * MARGIN
        n_spk = len(uniq_speakers)
        col_gap = Inches(0.2)
        col_w = int((txt_w - col_gap * (n_spk - 1)) / n_spk)
        col_x = [int(txt_left + i * (col_w + col_gap)) for i in range(n_spk)]
        palette = ["F7E4E1", "E4EEF7", "FBF0D9", "E7F3E8"]
        spk_color = {sp: palette[i % len(palette)] for i, sp in enumerate(uniq_speakers)}
        spk_col = {sp: i for i, sp in enumerate(uniq_speakers)}

        header_h = int(Inches(0.4))
        for i, sp in enumerate(uniq_speakers):
            hdr = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                        col_x[i], int(top), col_w, header_h)
            hdr.fill.solid(); hdr.fill.fore_color.rgb = RGBColor.from_string(spk_color[sp])
            hdr.line.color.rgb = self._rgb("accent"); hdr.line.width = Pt(0.75)
            hdr.shadow.inherit = False
            tf = hdr.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            self._set_run(p.add_run(), self._speaker_icon(sp) + " " + sp, 14,
                          color="ink", bold=True, cjk=True)

        y0 = int(top) + header_h + int(Inches(0.12))
        avail_h = int(SLIDE_H - y0 - Inches(0.30))
        n = len(turns)

        def nlines(t):
            return 1 + (1 if t.get("py") else 0) + (1 if t.get("vn") else 0)

        gap0 = int(Inches(0.08)); pad0 = int(Inches(0.14)); line0 = int(Inches(0.30))
        natural = sum(line0 * nlines(t) + pad0 for t in turns) + gap0 * (n - 1)
        scale = min(1.0, avail_h / natural) if natural else 1.0
        line_h = int(line0 * scale); pad = int(pad0 * scale); gap = int(gap0 * scale)
        hz_sz = max(12, int(16 * scale)); py_sz = max(9, int(11 * scale))
        vn_sz = max(8, int(10 * scale))

        y = y0
        for t in turns:
            spk = t.get("speaker")
            ci = spk_col.get(spk, 0)
            row_h = line_h * nlines(t) + pad
            card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                        col_x[ci], Emu(y), col_w, Emu(row_h))
            card.fill.solid()
            card.fill.fore_color.rgb = RGBColor.from_string(spk_color.get(spk, "F4F5F7"))
            card.line.color.rgb = self._rgb("muted"); card.line.width = Pt(0.5)
            card.shadow.inherit = False
            tf = card.text_frame; tf.word_wrap = True
            tf.margin_left = Pt(8); tf.margin_right = Pt(6)
            tf.margin_top = Pt(3); tf.margin_bottom = Pt(3)
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
            self._set_run(p.add_run(), t.get("hz", ""), hz_sz, color="ink", bold=True,
                          cjk=True)
            if t.get("py"):
                p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.LEFT
                self._set_run(p2.add_run(), t["py"], py_sz, color="accent", italic=True)
            if t.get("vn"):
                p3 = tf.add_paragraph(); p3.alignment = PP_ALIGN.LEFT
                self._set_run(p3.add_run(), t["vn"], vn_sz, color="muted")
            y = y + row_h + gap

    def _dialogue_bubbles(self, slide, turns, top, txt_left=None, txt_w=None):
        if txt_left is None:
            txt_left, txt_w = MARGIN, SLIDE_W - 2 * MARGIN
        first_speaker = turns[0].get("speaker")
        n = len(turns)
        avail_h = int(SLIDE_H - top - Inches(0.30))
        speaker_colors = {}

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
        max_bubble_w = min(Inches(7.6), txt_w); min_bubble_w = min(Inches(1.9), txt_w)

        def _bubble_w(t):
            # Bề rộng RIÊNG mỗi bubble theo dòng dài nhất — câu ngắn (vd 你们好!)
            # không bị kéo giãn hết cỡ như câu dài (review buổi 02: "nội dung
            # ngắn mà khung dài").
            def w(text, pt, cjk):
                if not text:
                    return 0
                return len(text) * Pt(pt) * (1.0 if cjk else 0.55)
            needed = max(w(t.get("hz", ""), hz_sz, True),
                        w(t.get("py", ""), py_sz, False),
                        w(t.get("vn", ""), vn_sz, False))
            return int(min(max_bubble_w, max(min_bubble_w, needed + Inches(0.5))))

        y = int(top)
        for t in turns:
            is_left = t.get("speaker") == first_speaker
            bubble_h = line_h * nlines(t) + pad
            bubble_w = _bubble_w(t)
            left = int(txt_left) if is_left else int(txt_left + txt_w - bubble_w)
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
            avatar_d = int(min(Inches(0.46), bubble_h * 0.62))
            color_hex = self._avatar_color(speaker_colors, spk)
            acx = (left - avatar_d * 0.42) if is_left else (left + bubble_w - avatar_d * 0.58)
            acy = y - avatar_d * 0.28
            self._place_avatar(slide, spk, color_hex, acx, acy, avatar_d)
            y = y + bubble_h + gap

    #    mỗi câu 1 khối 汉字 + pinyin + nghĩa, không dùng bong bóng thoại.
    def _slide_passage(self, s):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", "课文"), s.get("kicker"))
        top = self._content_top(); area_h = self._content_area_h()
        has_img = bool(s.get("image"))
        txt_left, txt_w, img_left, img_w = self._split_image_col(s, Inches(4.2))
        box, tf = self._textbox(slide, txt_left, top, txt_w, area_h,
                                anchor=MSO_ANCHOR.MIDDLE)
        first = True
        for sent in s.get("sentences", []):
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.space_before = Pt(16)
            self._set_run(p.add_run(), sent.get("hz", ""), 22, color="ink", bold=True,
                          cjk=True)
            if sent.get("py"):
                p2 = tf.add_paragraph(); p2.space_before = Pt(1)
                self._set_run(p2.add_run(), sent["py"], 14, color="accent", italic=True)
            if sent.get("vn"):
                p3 = tf.add_paragraph(); p3.space_before = Pt(1)
                self._set_run(p3.add_run(), sent["vn"], 14, color="muted")
        if s.get("note"):
            p = tf.add_paragraph(); p.space_before = Pt(14)
            self._set_run(p.add_run(), "• " + s["note"], 14, color="ink", cjk=True)
        if has_img:
            self._place_image(slide, s["image"], img_left, top, img_w, area_h)

    def _slide_reading(self, s):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", "Đọc thêm"), s.get("kicker", "阅读"))
        top = self._content_top(); area_h = self._content_area_h()
        txt_w = SLIDE_W - 2 * MARGIN
        groups = s.get("groups", [])
        natural = 0
        for grp in groups:
            natural += Pt(12) + self._line_h(17)
            for it in grp.get("items", []):
                natural += Pt(4) + self._wrap_lines(str(it), txt_w - Inches(0.3), 15, cjk=True) * self._line_h(15)
        scale = self._fit_scale(natural, area_h)

        def sz(pt, floor):
            return max(floor, int(pt * scale))

        box, tf = self._textbox(slide, MARGIN, top, txt_w, area_h,
                                anchor=MSO_ANCHOR.TOP)
        first = True
        for grp in groups:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.space_before = Pt(12 * scale)
            self._set_run(p.add_run(), grp.get("label", ""), sz(17, 12), color="accent",
                          bold=True)
            for it in grp.get("items", []):
                p = tf.add_paragraph(); p.space_before = Pt(4 * scale)
                self._set_run(p.add_run(), "•  ", sz(15, 11), color="accent", bold=True)
                self._set_run(p.add_run(), str(it), sz(15, 11), color="ink", cjk=True)

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

    def _slide_image(self, s):
        """Header + 1 ảnh lớn canh giữa (+ chú thích ngắn tùy chọn bên dưới).
        Dùng cho sơ đồ tổng quan / biểu đồ tĩnh — không cần bảng hay bullet,
        tránh vẽ shape/connector phức tạp ngay trong renderer."""
        slide = self._new_slide()
        self._band_header(slide, s.get("title", ""), s.get("kicker"))
        top = self._content_top(); area_h = self._content_area_h()
        img_w = SLIDE_W - 2 * MARGIN
        captions = s.get("captions", [s["caption"]] if s.get("caption") else [])
        cap_h = Inches(0.34) * len(captions) if captions else Inches(0)
        gap = Inches(0.12) if captions else Inches(0)
        img_h = area_h - cap_h - gap
        self._place_image(slide, s.get("image", ""), MARGIN, top, img_w, img_h)
        if captions:
            box, tf = self._textbox(slide, MARGIN, top + img_h + gap, img_w, cap_h,
                                    anchor=MSO_ANCHOR.TOP)
            first = True
            for line in captions:
                p = tf.paragraphs[0] if first else tf.add_paragraph()
                first = False
                p.alignment = PP_ALIGN.CENTER
                self._set_run(p.add_run(), str(line), 15, color="muted",
                              italic=True, cjk=True)

    def _slide_word_groups(self, s):
        """N nhóm (vd mỗi 声母 1 nhóm) xếp CẠNH NHAU theo cột, mỗi nhóm = 1
        banner chữ to (label) + bảng con 汉字|Pinyin|Nghĩa liệt kê từng ví dụ
        1 dòng — thay cho kiểu "声母 | Ví dụ 1 | Ví dụ 2 | Ví dụ 3" nhồi nhiều
        ví dụ vào 1 ô (review buổi 01: muốn tách cột riêng, chữ to, đều cột)."""
        slide = self._new_slide()
        self._band_header(slide, s.get("title", ""), s.get("kicker"))
        top = self._content_top()
        area_h = self._content_area_h() - self._footer_reserved_h(s)
        groups = s.get("groups", [])
        n = max(1, len(groups))
        gap = Inches(0.28)
        row_gap = Inches(0.22)
        # Số cột/hàng CHỌN THEO n để lấp đầy khung thay vì luôn nhồi 1 hàng
        # ngang (cột hẹp, chữ rớt dòng) — vd 4 nhóm thì xếp 2x2 "4 góc" thay
        # vì 1x4, mỗi ô rộng gấp đôi. >4 nhóm mới cần nhiều cột/hàng hơn.
        if n <= 3:
            cols_per_row = n
        elif n == 4:
            cols_per_row = 2
        else:
            cols_per_row = min(4, -(-n // 2))
        n_grid_rows = -(-n // cols_per_row)
        col_w = (SLIDE_W - 2 * MARGIN - gap * (cols_per_row - 1)) / cols_per_row
        # Đủ cao cho 2 dòng: chữ cái to (label chính) + chú thích nhỏ (vd
        # "trong ei") — nếu chỉ ép 1 dòng, label dài sẽ tự xuống dòng và TRÀN
        # khỏi banner vì text_frame word_wrap không tự co cỡ chữ theo shape.
        banner_h = Inches(0.72)
        note = s.get("note")
        note_h = Inches(0.4) if note else Inches(0)
        avail_h = area_h - note_h

        # Bề rộng cột TÍNH CHUNG trên toàn bộ items của MỌI nhóm (không phải
        # riêng từng nhóm) — để các bảng con thẳng cột với nhau, nhìn "đều
        # đều" thay vì mỗi nhóm co giãn khác nhau theo nội dung riêng của nó.
        # KHÔNG dùng _col_weights (hệ số cjk 1.7 hiệu chỉnh cho bảng full-width
        # cùng 1 cỡ chữ) — 3 cột ở đây LUÔN khác cỡ chữ nhau (hz 20pt > py
        # 14pt > vn 13pt), phải tính theo pt-width thật mỗi cột mới không bị
        # hz (chữ Hán 2 nét, cỡ to nhất) rớt dòng dù text ngắn hơn cột khác.
        all_items = [it for grp in groups for it in grp.get("items", [])]

        def _needed_pt(texts, font_pt, is_cjk):
            max_len = max((len(t) for t in texts), default=1) or 1
            per_char = font_pt * (1.15 if is_cjk else 0.58)
            return max_len * per_char + 18  # +margin trái/phải cố định

        need_hz = _needed_pt([it.get("hz", "") for it in all_items], 20, True)
        need_py = _needed_pt([it.get("py", "") for it in all_items], 14, False)
        need_vn = _needed_pt([it.get("vn", "") for it in all_items], 13, False)
        total_need = need_hz + need_py + need_vn
        if all_items:
            widths_frac = [need_hz / total_need, need_py / total_need, need_vn / total_need]
            # Sàn tối thiểu 22%/cột — 1 cột nội dung dài bất thường (vd chú
            # thích nghĩa dài) không được "nuốt" hết chỗ của 2 cột kia (đã gặp
            # thật: 1 dòng nghĩa dài làm cột 汉字 hẹp đến mức 1 chữ cũng rớt
            # dòng dù bản thân chữ đó rất ngắn).
            floor = 0.22
            deficits = [max(0.0, floor - w) for w in widths_frac]
            if sum(deficits) > 0:
                surplus_pool = [max(0.0, w - floor) for w in widths_frac]
                total_surplus = sum(surplus_pool)
                total_deficit = sum(deficits)
                widths_frac = [
                    w + deficits[i] - (surplus_pool[i] / total_surplus * total_deficit
                                       if total_surplus else 0)
                    for i, w in enumerate(widths_frac)
                ]
        else:
            widths_frac = [0.34, 0.33, 0.33]
        max_nrow = max((len(g.get("items", [])) for g in groups), default=1) or 1

        # Chiều cao hàng: vừa đủ chữ ở mức lý tưởng, co lại nếu tổng chiều
        # cao lưới (nhiều hàng x nhiều item) vượt khung.
        ideal_row_h = Inches(0.56)
        block_h = banner_h + Inches(0.1) + ideal_row_h * max_nrow
        grid_h = block_h * n_grid_rows + row_gap * (n_grid_rows - 1)
        # Cho scale GIÃN NỞ (không chỉ co) khi lưới còn dư nhiều khoảng trống
        # dọc — tận dụng khung thay vì để trắng cả nửa dưới slide (feedback
        # buổi 01: "khoảng dưới còn rất nhiều chỗ"), chặn trần để chữ không
        # phóng to vô lý khi chỉ có 1 nhóm ít ví dụ.
        scale = (avail_h / grid_h) if grid_h else 1.0
        # Trần giãn nở thấp hơn trần lý thuyết — phóng chữ quá to (vd 1.7x)
        # trong khi bề RỘNG cột không đổi (chỉ phụ thuộc cols_per_row) dễ làm
        # chữ tràn ngang dù cao thì vừa; 1.35x đã đủ lấp khoảng trống rõ rệt.
        scale = max(0.55, min(1.35, scale))
        # QUAN TRỌNG: cỡ CHỮ không được vượt mốc gốc (font_scale trần 1.0) dù
        # scale > 1 — bề RỘNG cột cố định theo cols_per_row, không giãn theo
        # scale; phóng to chữ mà không phóng cột làm chữ Hán 2 nét (vd 咖啡,
        # 开心) rớt dòng trong ô hẹp. scale > 1 chỉ nên làm HÀNG cao hơn/rộng
        # rãi hơn (thêm khoảng trắng dễ nhìn), không phóng chữ.
        font_scale = min(1.0, scale)
        row_h = int(ideal_row_h * scale)
        banner_h_s = int(banner_h * scale)
        block_h_s = int((banner_h + Inches(0.1)) * scale) + row_h * max_nrow
        row_gap_s = int(row_gap * scale)

        for i, grp in enumerate(groups):
            gr, gc = divmod(i, cols_per_row)
            gx = int(MARGIN + gc * (col_w + gap))
            gy = int(top + gr * (block_h_s + row_gap_s))
            items = grp.get("items", [])
            banner = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                            gx, gy, int(col_w), banner_h_s)
            banner.fill.solid(); banner.fill.fore_color.rgb = self._rgb("accent")
            banner.line.fill.background(); banner.shadow.inherit = False
            tf = banner.text_frame; tf.word_wrap = True
            tf.margin_top = Pt(2); tf.margin_bottom = Pt(2)
            main_label, _, sub_label = grp.get("label", "").partition(" · ")
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            self._set_run(p.add_run(), main_label, max(16, int(30 * font_scale)),
                          color="bg", bold=True)
            if sub_label:
                p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
                self._set_run(p2.add_run(), sub_label, max(9, int(12 * font_scale)),
                              color="accent_soft")

            if not items:
                continue
            table_top = gy + banner_h_s + int(Inches(0.1) * scale)
            nrow = len(items)
            gfx = slide.shapes.add_table(nrow, 3, gx, table_top, int(col_w), row_h * nrow)
            table = gfx.table
            for c, wf in enumerate(widths_frac):
                table.columns[c].width = int(col_w * wf)
            for r in range(nrow):
                table.rows[r].height = row_h
            for r, it in enumerate(items):
                bg = "band" if r % 2 == 0 else "bg"
                c0 = table.cell(r, 0); c0.fill.solid(); c0.fill.fore_color.rgb = self._rgb(bg)
                self._fill_cell(c0, it.get("hz", ""), max(13, int(20 * font_scale)), bold=True,
                                cjk=True, align=PP_ALIGN.CENTER)
                c1 = table.cell(r, 1); c1.fill.solid(); c1.fill.fore_color.rgb = self._rgb(bg)
                self._fill_cell(c1, it.get("py", ""), max(10, int(14 * font_scale)), color="accent",
                                italic=True, align=PP_ALIGN.CENTER)
                c2 = table.cell(r, 2); c2.fill.solid(); c2.fill.fore_color.rgb = self._rgb(bg)
                self._fill_cell(c2, it.get("vn", ""), max(9, int(13 * font_scale)), align=PP_ALIGN.LEFT)

        if note:
            note_top = top + avail_h + Inches(0.08)
            box, tf = self._textbox(slide, MARGIN, note_top, SLIDE_W - 2 * MARGIN,
                                    (top + area_h) - note_top)
            p = tf.paragraphs[0]
            self._set_run(p.add_run(), "🔍 So sánh: ", 13, color="accent", bold=True)
            self._set_run(p.add_run(), note, 13, color="ink", cjk=True)

    def _slide_stroke_group(self, s):
        """N chữ Hán CÙNG minh hoạ 1 nguyên tắc viết nét (vd 一/二/三 đều là
        "nét ngang, trái→phải") xếp thành 1 hàng thẻ, thay vì mỗi chữ 1 slide
        riêng — tránh lặp nguyên tắc giống hệt nhau nhiều lần (review buổi 01)."""
        slide = self._new_slide()
        self._band_header(slide, s.get("title", "Nguyên tắc viết chữ"), s.get("kicker"))
        top = self._content_top()
        area_h = self._content_area_h() - self._footer_reserved_h(s)
        chars = s.get("chars", [])
        principle = s.get("principle")

        principle_h = Inches(0)
        if principle:
            lines = self._wrap_lines(principle, SLIDE_W - 2 * MARGIN, 17, cjk=False)
            principle_h = Inches(0.2) + Inches(lines * 0.32) + Inches(0.18)
            box, tf = self._textbox(slide, MARGIN, top, SLIDE_W - 2 * MARGIN,
                                    principle_h, anchor=MSO_ANCHOR.TOP)
            p = tf.paragraphs[0]
            self._set_run(p.add_run(), "📐 Nguyên tắc: ", 17, color="accent", bold=True)
            self._set_run(p.add_run(), principle, 17, color="ink", cjk=True)

        n = max(1, len(chars))
        gap = Inches(0.3)
        card_top = top + principle_h
        card_area_h = area_h - principle_h
        cap_h = Inches(0.75)
        card_w = (SLIDE_W - 2 * MARGIN - gap * (n - 1)) / n
        img_side = min(card_w, card_area_h - cap_h)
        for i, ch in enumerate(chars):
            cx = MARGIN + i * (card_w + gap)
            img_left = cx + (card_w - img_side) / 2
            self._place_image(slide, ch.get("image", ""), img_left, card_top,
                              img_side, img_side)
            cap_top = card_top + img_side + Inches(0.06)
            box, tf = self._textbox(slide, cx, cap_top, card_w, cap_h,
                                    anchor=MSO_ANCHOR.TOP)
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            self._set_run(p.add_run(), ch.get("hanzi", ""), 24, color="ink",
                          bold=True, cjk=True)
            self._set_run(p.add_run(), "  " + ch.get("pinyin", ""), 15,
                          color="accent", italic=True)
            if ch.get("meaning"):
                p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
                p2.space_before = Pt(2)
                self._set_run(p2.add_run(), ch["meaning"], 13, color="muted",
                              cjk=True)

    def _slide_exercise(self, s):
        self._list_slide(s, "Luyện tập", numbered=True)

    def _slide_answers(self, s):
        self._list_slide(s, "Đáp án", numbered=True)

    def _slide_bullets(self, s):
        self._list_slide(s, "Nội dung", numbered=False)

    def _list_slide(self, s, default_title, numbered):
        slide = self._new_slide()
        self._band_header(slide, s.get("title", default_title), s.get("kicker"))
        top = self._content_top()
        area_h = self._content_area_h() - self._footer_reserved_h(s)
        has_img = bool(s.get("image"))
        txt_left, txt_w, img_left, img_w = self._split_image_col(s, Inches(4.6))
        instructions = s.get("instructions")
        items = s.get("items", s.get("bullets", []))
        prefix_w = Inches(0.45)

        natural = 0
        if instructions:
            natural += self._wrap_lines(instructions, txt_w, 16, cjk=True) * self._line_h(16)
        for item in items:
            natural += Pt(13) + self._wrap_lines(str(item), txt_w - prefix_w, 20, cjk=True) * self._line_h(20)
        scale = self._fit_scale(natural, area_h)

        def sz(pt, floor):
            return max(floor, int(pt * scale))

        box, tf = self._textbox(slide, txt_left, top, txt_w, area_h,
                                anchor=MSO_ANCHOR.TOP)
        first = True
        if instructions:
            p = tf.paragraphs[0]
            self._set_run(p.add_run(), instructions, sz(16, 12), color="accent",
                          italic=True)
            first = False
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.space_before = Pt(13 * scale)
            prefix = ("%d. " % (i + 1)) if numbered else "•  "
            self._set_run(p.add_run(), prefix, sz(20, 14), color="accent", bold=True)
            self._set_run(p.add_run(), str(item), sz(20, 14), color="ink", cjk=True)
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
