"""Vẽ NGUYÊN CẢNH khung tĩnh (nhân vật + nền tối giản) bằng model ảnh -> out/gen/<id>.png (3:2, ~1264x848).

  python gen_scenes.py K1 K5        # chỉ các cảnh này
  python gen_scenes.py              # mọi cảnh trong src/scenes.json chưa có out/gen/<id>.png

Prompt = style + các khối mô tả theo TAG của cảnh (nhân vật: jx/yh/son…, trang phục: jx_home/yh_out…) + mô tả cảnh (src/scenes.json).
Chỉ cảnh có tag nhân vật mới nhận mô tả nhân vật đó (cảnh không có 越黄 thì không nhét mô tả yh -> tránh vẽ thừa).
Model không nhận ảnh mẫu -> mặt nhân vật dựa hoàn toàn vào mô tả; soát từng ảnh trước khi chép sang assets/keyframes/.
"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from _paths import IMAGEGEN

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).parent
cfg = json.loads((here / "src" / "scenes.json").read_text(encoding="utf-8"))
out = here / "out" / "gen"; out.mkdir(parents=True, exist_ok=True)
ids = sys.argv[1:] or [i for i in cfg["scenes"] if not (out / f"{i}.png").exists()]


def gen(sid):
    *tags, desc = cfg["scenes"][sid]
    prompt = " ".join([cfg["style"], *(cfg[t] for t in tags), desc])
    r = subprocess.run([sys.executable, str(IMAGEGEN), prompt, "-o", str(out / f"{sid}.png"), "--size", cfg.get("size", "1536x1024")],
                       capture_output=True, text=True, encoding="utf-8")
    return f"{sid}: {'OK' if r.returncode == 0 else 'LỖI ' + (r.stderr or r.stdout)[-300:]}"


with ThreadPoolExecutor(2) as ex:
    for msg in ex.map(gen, ids):
        print(msg, flush=True)
