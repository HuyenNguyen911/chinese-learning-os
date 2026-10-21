"""Sinh ảnh nhân vật + từng thẻ (nền trắng) -> assets/raw/. Sau đó chạy cutout.py để tách nền.

  python gen_assets.py              # chỉ sinh ảnh CHƯA có
  python gen_assets.py lian etou    # sinh lại đúng các id này (ghi đè)

Prompt từng thẻ: words.json -> "prompt" (thẻ không có prompt thì bỏ qua).
Phong cách chung + nhân vật: layout.json -> "style", "characterPrompt".
BÀI HỌC: style chung KHÔNG được chứa đặc điểm nhân vật (vd "curly hair") — AI sẽ vẽ tóc lên cả mũi/tai/tay.
"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
sys.path.insert(0, str(here))
from _paths import IMAGEGEN as gen  # noqa: E402

raw = here / "assets" / "raw"
raw.mkdir(parents=True, exist_ok=True)
L = json.loads((here / "layout.json").read_text(encoding="utf-8"))
STYLE = L["style"]
words = json.loads((here / "words.json").read_text(encoding="utf-8"))
jobs = [("character", L["characterPrompt"])] + [(w["id"], w["prompt"]) for w in words if "prompt" in w]
only = set(sys.argv[1:])


def run(j):
    name, p = j
    out = raw / f"{name}.png"
    if (only and name not in only) or (not only and out.exists()):
        return
    subprocess.run([sys.executable, str(gen), f"{p}. {STYLE}", "-o", str(out)], check=True)


with ThreadPoolExecutor(5) as ex:
    list(ex.map(run, jobs))
print("Xong. Chạy tiếp: python cutout.py  (tách nền + contact sheet + chép vào public/img)")
