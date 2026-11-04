#!/bin/bash
# Render chia đoạn — chống lỗi "No frame found at position" khi render dài nhiều clip OffthreadVideo (xem reference/gotchas.md).
# Dùng: bash chunk_render.sh FullEN video/<slug>-en.mp4 [STEP=600]   (chạy ở thư mục project; đoạn đã xong được giữ, chạy lại = làm tiếp)
cd "$(dirname "$0")"
COMP=$1; OUT=$2; STEP=${3:-600}; D=out/ch-$COMP
[ -z "$COMP" ] || [ -z "$OUT" ] && { echo "usage: bash chunk_render.sh <Composition> <out.mp4> [step]"; exit 1; }
mkdir -p $D
# Soát trước: clip/audio hỏng (vd commit lúc đang mã hoá dở → "moov atom not found") chỉ lộ ra giữa lúc render
BAD=0; for m in public/motion/*.mp4 public/audio/*; do [ -f "$m" ] || continue
  ffprobe -v error -show_entries format=duration -of csv=p=0 "$m" > /dev/null 2>&1 || { echo "FILE HỎNG: $m"; BAD=1; }; done
[ $BAD = 1 ] && { echo "dừng — gen/mã hoá lại file hỏng rồi chạy lại"; exit 1; }
TOTAL=$(npx remotion compositions src/index.ts 2>/dev/null | sed 's/\x1b\[[0-9;]*m//g' | awk -v c="$COMP" '$1==c {print $4}')
[ -z "$TOTAL" ] && { echo "không đọc được số khung của $COMP"; exit 1; }
: > $D/list.txt; i=0
for ((s=0; s<TOTAL; s+=STEP)); do
  e=$((s+STEP-1)); ((e>TOTAL-1)) && e=$((TOTAL-1)); f=$D/c$i.mp4
  if [ ! -f $f ]; then
    for try in 1 2 3; do
      conc=$([ $try = 1 ] && echo 3 || echo 1)
      npx remotion render src/index.ts $COMP $f --frames=$s-$e --concurrency=$conc --muted > $D/c$i.try$try.log 2>&1 && break
      rm -f $f; echo "đoạn $i lỗi (lần $try, $conc luồng) — $(grep -m1 -iE 'error|No frame|moov' $D/c$i.try$try.log | sed 's/\x1b\[[0-9;]*m//g' | cut -c1-160)"
    done
    [ -f $f ] || { echo "đoạn $i FAILED — xem $D/c$i.try*.log"; exit 1; }
  fi
  echo "file 'c$i.mp4'" >> $D/list.txt; echo "đoạn $i xong ($s-$e)"; i=$((i+1))
done
npx remotion render src/index.ts $COMP $D/audio.wav --codec=wav --timeout=180000 > $D/audio.log 2>&1 || { echo "audio FAILED"; exit 1; }
ffmpeg -v error -y -f concat -safe 0 -i $D/list.txt -c copy $D/v.mp4 &&
ffmpeg -v error -y -i $D/v.mp4 -i $D/audio.wav -c:v copy -c:a aac -b:a 192k -shortest "$OUT" && echo "DONE → $OUT"
