"""Kiểm tra bố cục TRƯỚC khi render: thẻ không chồng nhau, không tràn khung, đủ khoảng cách.
Chạy: python lint_layout.py   (exit 1 nếu có lỗi)"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
from itertools import combinations
from pathlib import Path

L = json.loads((Path(__file__).parent / "layout.json").read_text(encoding="utf-8"))
W, H, M = L["canvas"]["w"], L["canvas"]["h"], L["canvas"]["margin"]
GAP = 20          # khoảng trống tối thiểu giữa 2 thẻ
MIN_CELL_W = 200  # bề ngang tối thiểu của vùng chữ

boxes = {}
for k, s in L["slots"].items():
    cw = max(s["iw"], MIN_CELL_W)
    boxes[k] = (s["x"] - cw / 2, s["y"], s["x"] + cw / 2, s["y"] + s["ih"] + L["textH"])
c = L["char"]
boxes["_character"] = (c["x"], c["y"], c["x"] + c["w"], c["y"] + c["w"] * c["srcH"] / c["srcW"])

errs = []
for k, (x0, y0, x1, y1) in boxes.items():
    if x0 < M or y0 < M or x1 > W - M or y1 > H - M:
        errs.append(f"{k}: tràn khung ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
for (a, A), (b, B) in combinations(boxes.items(), 2):
    dx = max(A[0] - B[2], B[0] - A[2])
    dy = max(A[1] - B[3], B[1] - A[3])
    if max(dx, dy) < GAP:
        errs.append(f"{a} <-> {b}: cách nhau {max(dx, dy):.0f}px (< {GAP})")
print("\n".join(errs) if errs else f"OK: {len(L['slots'])} thẻ, không chồng/tràn, gap >= {GAP}px")
sys.exit(1 if errs else 0)
