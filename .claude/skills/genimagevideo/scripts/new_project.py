"""Tạo project video mới từ template -> output/Gen ảnh_video/<slug>/

  python .claude/skills/genimagevideo/scripts/new_project.py <slug> [--template poster-highlight] [--no-install]

slug: không dấu, nối gạch ngang (vd mau-sac, do-an). Project tự chứa: data (words/layout.json),
script sinh ảnh/giọng, code Remotion. Template copy kèm DATA MẪU (bộ phận cơ thể) để sửa đè.
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SKILL = Path(__file__).resolve().parent.parent
REPO = SKILL.parent.parent.parent
OUT_ROOT = REPO / "output" / "Gen ảnh_video"

ap = argparse.ArgumentParser()
ap.add_argument("slug")
ap.add_argument("--template", default="poster-highlight")
ap.add_argument("--no-install", action="store_true")
a = ap.parse_args()

src = SKILL / "template" / a.template
dest = OUT_ROOT / a.slug
if not src.is_dir():
    sys.exit(f"Không có template: {src}")
if dest.exists():
    sys.exit(f"Đã tồn tại: {dest} — chọn slug khác hoặc sửa trực tiếp project đó")

shutil.copytree(src, dest, ignore=shutil.ignore_patterns("node_modules", "out", "video", "assets", "public", "gen.log"))
pkg = dest / "package.json"
pkg.write_text(pkg.read_text(encoding="utf-8").replace("__SLUG__", a.slug), encoding="utf-8")
for d in ("assets/raw", "public/img", "public/audio", "video", "out"):
    (dest / d).mkdir(parents=True, exist_ok=True)
(dest / "src" / "durations.json").write_text("{}", encoding="utf-8")

if not a.no_install:
    npm = "npm.cmd" if sys.platform == "win32" else "npm"
    subprocess.run([npm, "ci", "--no-audit", "--no-fund"], cwd=dest, check=True)

print(f"""Đã tạo: {dest}
Tiếp theo (trong thư mục project):
  1. Sửa words.json (id, han, pinyin, vi, prompt) + layout.json (title, style, characterPrompt, slots, hl)
  2. python lint_layout.py
  3. python gen_assets.py && python cutout.py   -> xem assets/contact.jpg
  4. python gen_voice.py [--no-tts]             -> public/audio + src/durations.json
  5. npm run still  (ảnh tĩnh kiểm tra)  ->  npm run render  -> video/{a.slug}.mp4""")
