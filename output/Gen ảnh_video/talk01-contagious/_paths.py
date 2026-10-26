"""Tìm thư mục skill genimagevideo từ bất kỳ project nào trong repo (project nằm ở output/Gen ảnh_video/<slug>/)."""
from pathlib import Path


def _skill_dir():
    for p in Path(__file__).resolve().parents:
        d = p / ".claude" / "skills" / "genimagevideo"
        if d.is_dir():
            return d
    raise SystemExit("Không tìm thấy .claude/skills/genimagevideo")


SKILL = _skill_dir()
IMAGEGEN = SKILL / "scripts" / "imagegen" / "gen_image.py"
VOICEGEN = SKILL / "scripts" / "voicegen"
