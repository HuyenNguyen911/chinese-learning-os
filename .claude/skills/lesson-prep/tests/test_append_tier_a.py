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
