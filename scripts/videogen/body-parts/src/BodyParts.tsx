import { AbsoluteFill, Audio, Sequence, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import words from "../words.json";
import layout from "../layout.json";
import durations from "./durations.json";

export const FPS = 30;
export const INTRO = 75;
export const OUTRO = 60;

type Slot = { x: number; y: number; iw: number; ih: number; side: string; t: number[]; crop?: number[] };
const SLOTS = layout.slots as Record<string, Slot>;
const CHAR = layout.char;
// thời lượng mỗi từ = độ dài giọng đọc + ~1.1s để highlight/mũi tên, tối thiểu 54 khung
const LEN = words.map((w) => Math.max(54, Math.ceil(((durations as Record<string, number>)[w.id] + 1.1) * FPS)));
const START = LEN.map((_, i) => LEN.slice(0, i).reduce((a, b) => a + b, 0));
export const SEQ_LEN = LEN.reduce((a, b) => a + b, 0);
const SEQ_END = INTRO + SEQ_LEN;

const HAN = "'Microsoft YaHei','Noto Sans SC','PingFang SC',sans-serif";
const HEAD = "'Segoe UI Black','Arial Rounded MT Bold','Segoe UI',sans-serif";
const RED = "#E5392B";
const SOFT = Easing.bezier(0.33, 1, 0.68, 1); // ease-out mềm
const SMOOTH = Easing.bezier(0.45, 0, 0.55, 1); // ease-in-out

const mix = (a: string, b: string, t: number) => {
  const p = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const [A, B] = [p(a), p(b)];
  return `rgb(${A.map((v, i) => Math.round(v + (B[i] - v) * t)).join(",")})`;
};

// đường bao 0→1→0 cho từ đang đọc (vào nhanh-mềm, ra chậm-mềm, không bật đột ngột)
const envelope = (local: number, len: number) =>
  interpolate(local, [0, 16, len - 16, len], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: SMOOTH,
  });

const charPt = (t: number[]) => {
  const k = CHAR.w / CHAR.srcW;
  return { x: CHAR.x + t[0] * k, y: CHAR.y + t[1] * k };
};
const startPt = (s: Slot) => {
  if (s.side === "R") return { x: s.x + s.iw / 2 + 10, y: s.y + s.ih / 2 };
  if (s.side === "L") return { x: s.x - s.iw / 2 - 10, y: s.y + s.ih / 2 };
  if (s.side === "B") return { x: s.x, y: s.y + s.ih + layout.textH - 6 };
  return { x: s.x, y: s.y - 10 };
};

const Title = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const st = { fontFamily: HEAD, fontSize: 92, lineHeight: 1.05, textAlign: "center" as const, margin: 0, WebkitTextStroke: "3px #fff", paintOrder: "stroke fill" as const };
  const line = (delay: number, color: string, text: string) => {
    const p = spring({ frame: f - delay, fps, config: { damping: 18, stiffness: 90 } });
    return (
      <h1 style={{ ...st, color, opacity: p, transform: `translateY(${(1 - p) * -36}px)` }}>{text}</h1>
    );
  };
  return (
    <div style={{ position: "absolute", top: 60, width: "100%" }}>
      {line(0, "#F08A4B", "BỘ PHẬN CƠ THỂ")}
      {line(6, "#5AA9E6", "TRONG TIẾNG HOA")}
    </div>
  );
};

const Card = ({ w, i }: { w: (typeof words)[number]; i: number }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = SLOTS[w.id];
  const enter = spring({ frame: f - 14 - i * 3, fps, config: { damping: 16, stiffness: 80 } });
  const local = f - INTRO - START[i];
  const active = local >= 0 && local < LEN[i];
  const k = active ? envelope(local, LEN[i]) : 0;
  const seq = interpolate(f, [INTRO - 12, INTRO + 8, SEQ_END - 8, SEQ_END + 12], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const dim = 1 - 0.45 * seq * (1 - k);
  const floatY = 4 * Math.sin((f + i * 11) / 17);
  const tilt = 1.1 * Math.sin((f + i * 7) / 23) + (active ? -1.5 * k : 0);
  const scale = enter * (1 + 0.15 * k);
  const cellW = Math.max(s.iw, 200);

  let visual;
  if (s.crop) {
    const [cx, cy, cw] = s.crop;
    const ch = (cw * s.ih) / s.iw;
    const imgW = s.iw / cw;
    visual = (
      <div style={{ position: "relative", width: s.iw, height: s.ih, borderRadius: 26, overflow: "hidden", border: "5px solid #fff", boxSizing: "border-box", background: "#fff", boxShadow: `0 6px 16px rgba(0,0,0,0.18), 0 0 ${26 * k}px ${6 * k}px rgba(229,57,43,${0.75 * k})` }}>
        <Img src={staticFile("img/portrait.png")} style={{ position: "absolute", width: imgW, height: imgW, left: -(cx - cw / 2) * imgW - 5, top: -(cy - ch / 2) * imgW - 5, maxWidth: "none" }} />
      </div>
    );
  } else {
    visual = (
      <Img src={staticFile(`img/${w.id}.png`)} style={{ maxWidth: s.iw, maxHeight: s.ih, objectFit: "contain", filter: k > 0.02 ? `drop-shadow(0 0 ${20 * k}px rgba(229,57,43,${0.85 * k}))` : undefined }} />
    );
  }

  return (
    <div style={{ position: "absolute", left: s.x - cellW / 2, top: s.y, width: cellW, textAlign: "center", opacity: enter * dim, transform: `translateY(${floatY}px) rotate(${tilt}deg) scale(${scale})`, transformOrigin: "50% 35%", zIndex: active ? 5 : 1 }}>
      <div style={{ height: s.ih, display: "flex", alignItems: "center", justifyContent: "center" }}>{visual}</div>
      <div style={{ fontFamily: HAN, fontSize: 48, fontWeight: 700, lineHeight: 1.15, marginTop: 6, color: mix("#3E7CB1", RED, k) }}>{w.han}</div>
      <div style={{ fontFamily: HAN, fontSize: 25, lineHeight: 1.2, color: mix("#7A6A55", RED, k) }}>{w.pinyin}</div>
      <div style={{ fontFamily: HAN, fontSize: 22, lineHeight: 1.25, color: mix("#9A8A76", "#B8301F", k) }}>{w.vi}</div>
    </div>
  );
};

const Pointer = ({ w, i }: { w: (typeof words)[number]; i: number }) => {
  const f = useCurrentFrame();
  const local = f - INTRO - START[i];
  if (local < 0 || local >= LEN[i]) return null;
  const s = SLOTS[w.id];
  const a = startPt(s), b = charPt(s.t);
  const dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy);
  const nx = -dy / len, ny = dx / len;
  const bend = 0.16 * len * (s.side === "R" || s.side === "T" ? 1 : -1);
  const c = { x: (a.x + b.x) / 2 + nx * bend, y: (a.y + b.y) / 2 + ny * bend };
  // điểm cuối lùi lại 20px theo tiếp tuyến để mũi tên không đè lên điểm chỉ
  const tx = b.x - c.x, ty = b.y - c.y, tl = Math.hypot(tx, ty);
  const tip = { x: b.x - (tx / tl) * 22, y: b.y - (ty / tl) * 22 };
  const draw = interpolate(local, [8, 30], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.22, 1, 0.36, 1) });
  const fade = interpolate(local, [LEN[i] - 14, LEN[i]], [1, 0], { extrapolateLeft: "clamp" });
  const ang = (Math.atan2(ty, tx) * 180) / Math.PI;
  const head = interpolate(draw, [0.85, 1], [0, 1], { extrapolateLeft: "clamp" });
  const ripple = (offset: number) => {
    const p = ((local - 24 - offset + 60) % 40) / 40;
    return local < 24 ? null : (
      <circle cx={b.x} cy={b.y} r={10 + 42 * p} fill="none" stroke={RED} strokeWidth={5} opacity={(1 - p) * 0.9} />
    );
  };
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: fade, zIndex: 10 }}>
      <path d={`M ${a.x} ${a.y} Q ${c.x} ${c.y} ${tip.x} ${tip.y}`} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} fill="none" stroke={RED} strokeWidth={8} strokeLinecap="round" />
      <g transform={`translate(${tip.x},${tip.y}) rotate(${ang}) scale(${head})`} opacity={head}>
        <polygon points="14,0 -22,-18 -22,18" fill={RED} />
      </g>
      <circle cx={b.x} cy={b.y} r={7} fill={RED} opacity={head} />
      {ripple(0)}
      {ripple(20)}
    </svg>
  );
};

export const BodyParts = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const charIn = spring({ frame: f - 5, fps, config: { damping: 14, stiffness: 80 } });
  const h = (CHAR.w * CHAR.srcH) / CHAR.srcW;
  const idx = Math.max(0, START.filter((st) => f - INTRO >= st).length - 1);
  const inSeq = f >= INTRO && f < SEQ_END;
  const cam = inSeq ? envelope(f - INTRO - START[idx], LEN[idx]) : 0;
  const tgt = charPt(SLOTS[words[idx].id].t);
  const sway = 1.2 * Math.sin(f / 38);
  const breathe = 1 + 0.012 * Math.sin(f / 21);
  return (
    <AbsoluteFill style={{ background: "#FFF3DC" }}>
      <AbsoluteFill style={{ transform: `scale(${1 + 0.025 * cam})`, transformOrigin: `${tgt.x}px ${tgt.y}px` }}>
        <Title />
        <Img src={staticFile("img/character.png")} style={{ position: "absolute", left: CHAR.x, top: CHAR.y, width: CHAR.w, height: h, transform: `scale(${charIn * breathe}) rotate(${sway}deg)`, transformOrigin: "50% 90%" }} />
        {words.map((w, i) => (
          <Card key={w.id} w={w} i={i} />
        ))}
        {words.map((w, i) => (
          <Sequence key={`a-${w.id}`} from={INTRO + START[i] + 8}>
            <Audio src={staticFile(`audio/${w.id}.wav`)} />
          </Sequence>
        ))}
        {words.map((w, i) => (
          <Pointer key={w.id} w={w} i={i} />
        ))}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
