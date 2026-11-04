"""Vẽ cặp nhân vật (瑾玄 + 越黄) trên nền mint trơn -> assets/raw/<id>.png, rồi chạy cutout_mint.py <id>.
  python gen_pairs.py ask p2 p3      # các tư thế trong POSES"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from _paths import IMAGEGEN
sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open("src/scenes.json", encoding="utf8"))
BASE = "Flat pastel chibi cartoon illustration, thin clean outlines, soft flat colors, big heads, cute and warm. No text, no letters, no numbers, no logos anywhere. Every face is kind and gentle."
CH = " ".join([d["jx"], d["jx_out"], d["yh"], d["yh_out"], d["yh_play"]])
MINT = "Plain flat solid MINT GREEN background (#BFE3CC) filling the whole picture, no ground, no shadow, no scenery, nothing else; both characters full body, feet fully visible, nothing cut off, a small gap between them. JX on the left, YH on the right, same height, they face each other in a three-quarter view (except the front pose)."
POSES = {
  "front": "JX and YH stand side by side facing the viewer straight on and looking DIRECTLY into the camera, front view; JX smiles curiously, YH has a warm friendly open smile.",
  "ask": "ONLY TWO characters in the picture (exactly one JX and one YH). They have just stopped walking. YH turns towards JX and asks her something with a warm friendly smile, one hand casually in his pocket, eyebrows raised; JX looks at him, listening, mouth closed, curious.",
  "p2": "JX tilts her head to one side with a puzzled 'huh?' face, one finger touching her chin, mouth slightly open; YH watches her with a warm amused smile, mouth closed.",
  "p3": "JX proudly points her thumb at her own chest, chin up, bright confident smile, mouth open as if saying 'I go there all the time!'; YH smiles warmly, mouth closed, eyes sparkling.",
  "p4": "JX happily counts on her fingers with both hands raised in front of her chest, very proud, mouth open talking; YH covers his mouth with one hand holding back a laugh, eyes sparkling playfully.",
  "p5": "YH waves one hand side to side in a teasing 'no, no, no' gesture, laughing happily with a big open friendly laugh, mouth open; JX blinks at him innocently, mouth closed.",
  "p6": "YH points a finger at JX playfully, teasing her with a bright friendly laugh, mouth open talking; JX puts her hands on her hips with a little pout, mouth closed.",
  "p7": "JX spreads both palms upward with a blank, innocent, completely puzzled face, a small simple question mark shape floating above her head, mouth open asking; YH smiles warmly, mouth closed.",
}
ids = sys.argv[1:] or list(POSES)
def gen(k):
    p = " ".join([BASE, CH, MINT, POSES[k]])
    r = subprocess.run([sys.executable, str(IMAGEGEN), p, "-o", f"assets/raw/{k}.png", "--size", "1536x1024"], capture_output=True, text=True, encoding="utf-8")
    return f"{k}: {'OK' if r.returncode == 0 else 'LỖI ' + (r.stderr or r.stdout)[-200:]}"
with ThreadPoolExecutor(2) as ex:
    for m in ex.map(gen, ids): print(m, flush=True)
