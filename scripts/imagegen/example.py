import sys; sys.stdout.reconfigure(encoding="utf-8")
"""Ví dụ chạy được: sinh 1 ảnh minh hoạ từ vựng (苹果) -> scripts/imagegen/example_out/pingguo.png

Chạy:  python scripts/imagegen/example.py
"""
import subprocess, sys
from pathlib import Path

here = Path(__file__).parent
out = here / "example_out" / "pingguo.png"
out.parent.mkdir(exist_ok=True)

prompt = ("Flat, child-friendly illustration of a single red apple on a plain white "
          "background, no text, simple shapes, bright colors")
subprocess.run([sys.executable, str(here / "gen_image.py"), prompt, "-o", str(out)], check=True)
print("Mở ảnh:", out)
