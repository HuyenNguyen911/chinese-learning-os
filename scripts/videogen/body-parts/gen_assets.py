"""Sinh ảnh nhân vật + từng bộ phận (nền trắng) -> assets/raw/, rồi tách nền -> assets/*.png"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

here = Path(__file__).parent
gen = here.parent.parent / "imagegen" / "gen_image.py"
raw = here / "assets" / "raw"
STYLE = ("Cute flat children's-book cartoon illustration, soft thick outlines, warm pastel colors, "
         "cream and tan skin tone. Isolated on a plain pure white background, "
         "no text, no letters, no shadow, centered, a single subject.")
CHAR = ("a cute smiling little boy sitting on the floor facing front with both legs stretched straight out in front toward the viewer (not cross-legged), arms wide open, mustard-yellow hoodie, "
        "olive shorts, bare feet, curly brown hair, full body visible with all limbs clearly shown")

jobs = [("character", CHAR + " Curly brown hair.")] + [(w["id"], w["prompt"]) for w in json.loads((here / "words.json").read_text(encoding="utf-8")) if "prompt" in w]
only = set(sys.argv[1:])

def run(j):
    name, p = j
    out = raw / f"{name}.png"
    if only and name not in only or (not only and out.exists()):
        return
    subprocess.run([sys.executable, str(gen), f"{p}. {STYLE}", "-o", str(out)], check=True)

with ThreadPoolExecutor(5) as ex:
    list(ex.map(run, jobs))
