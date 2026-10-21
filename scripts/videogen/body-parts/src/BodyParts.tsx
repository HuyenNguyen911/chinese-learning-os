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
const PANEL = layout.panel;

// thời lượng mỗi từ = độ dài giọng đọc + ~1.1s để highlight/mũi tên, tối thiểu 54 khung
const LEN = words.map((w) => Math.max(54, Math.ceil(((durations as Record<string, number>)[w.id] + 1.1) * FPS)));
const START = LEN.map((_, i) => LEN.slice(0, i).reduce((a, b) => a + b, 0));
export const SEQ_LEN = LEN.reduce((a, b) => a + b, 0);
const SEQ_END = INTRO + SEQ_LEN;

const HAN = "'Microsoft YaHei','Noto Sans SC','PingFang SC',sans-serif";
const HEAD = "'Segoe UI Black','Arial Rounded MT Bold','Segoe UI',sans-serif";
const RED = "#E5392B";
const SMOOTH = Easing.bezier(0.45, 0, 0.55, 1);

const mix = (a: string, b: string, t: number) => {
  const p = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const [A, B] = [p(a), p(b)];
  return `rgb(${A.map((v, i) => Math.round(v + (B[i] - v) * t)).join(",")})`;
};

// đường bao 0→1→0 cho từ đang đọc
const envelope = (local: number, len: number) =>
  interpolate(local, [0, 14, len - 14, len], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: SMOOTH });

const charPt = (t: number[]) => {
  const k = CHAR.w / CHAR.srcW;
  return { x: CHAR.x + t[0] * k, y: CHAR.y + t[1] * k };
};

const Title = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const st = { fontFamily: HEAD, fontSize: 92, lineHeight: 1.05, textAlign: "center" as const, margin: 0, WebkitTextStroke: "3px #fff", paintOrder: "stroke fill" as const };
  const line = (delay: number, color: string, text: string) => {
    const p = spring({ frame: f - delay, fps, config: { damping: 18, stiffness: 90 } });
    return <h1 style={{ ...st, color, opacity: p, transform: `translateY(${(1 - p) * -36}px)` }}>{text}</h1>;
  };
  return (
    <div style={{ position: "absolute", top: 60, width: "100%" }}>
      {line(0, "#F08A4B", "BỘ PHẬN CƠ THỂ")}
      {line(6, "#5AA9E6", "TRONG TIẾNG HOA")}
    </div>
  );
};

// ảnh cắt từ chân dung: (cx,cy) tâm, cw bề ngang (tỉ lệ ảnh gốc), khung dw×dh
const Crop = ({ crop, dw, dh, border = 5 }: { crop: number[]; dw: number; dh: number; border?: number }) => {
  const [cx, cy, cw] = crop;
  const ch = (cw * dh) / dw;
  const imgW = dw / cw;
  return (
    <Img src={staticFile("img/portrait.png")} style={{ position: "absolute", width: imgW, height: imgW, left: -(cx - cw / 2) * imgW - border, top: -(cy - ch / 2) * imgW - border, maxWidth: "none" }} />
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
  const dim = 1 - 0.4 * seq * (1 - k);
  const cellW = Math.max(s.iw, 200);
  const visual = s.crop ? (
    <div style={{ position: "relative", width: s.iw, height: s.ih, borderRadius: 24, overflow: "hidden", border: "5px solid #fff", boxSizing: "border-box", background: "#fff", boxShadow: `0 5px 14px rgba(0,0,0,0.16), 0 0 ${22 * k}px ${5 * k}px rgba(229,57,43,${0.7 * k})` }}>
      <Crop crop={s.crop} dw={s.iw} dh={s.ih} />
    </div>
  ) : (
    <Img src={staticFile(`img/${w.id}.png`)} style={{ maxWidth: s.iw, maxHeight: s.ih, objectFit: "contain", filter: k > 0.02 ? `drop-shadow(0 0 ${18 * k}px rgba(229,57,43,${0.85 * k}))` : undefined }} />
  );
  return (
    <div style={{ position: "absolute", left: s.x - cellW / 2, top: s.y, width: cellW, textAlign: "center", opacity: enter * dim, transform: `scale(${enter * (1 + 0.1 * k)})`, transformOrigin: "50% 35%", zIndex: active ? 5 : 1 }}>
      <div style={{ height: s.ih, display: "flex", alignItems: "center", justifyContent: "center" }}>{visual}</div>
      <div style={{ fontFamily: HAN, fontSize: 48, fontWeight: 700, lineHeight: 1.15, marginTop: 6, color: mix("#3E7CB1", RED, k) }}>{w.han}</div>
      <div style={{ fontFamily: HAN, fontSize: 25, lineHeight: 1.2, color: mix("#7A6A55", RED, k) }}>{w.pinyin}</div>
      <div style={{ fontFamily: HAN, fontSize: 22, lineHeight: 1.25, color: mix("#9A8A76", "#B8301F", k) }}>{w.vi}</div>
    </div>
  );
};

// khung phóng to ở giữa: hình lớn của bộ phận đang đọc
const Panel = () => {
  const f = useCurrentFrame();
  const t = f - INTRO;
  if (t < 0 || f >= SEQ_END) return null;
  const idx = Math.max(0, START.filter((st) => t >= st).length - 1);
  const w = words[idx];
  const s = SLOTS[w.id];
  const local = t - START[idx];
  const k = envelope(local, LEN[idx]);
  const scale = 0.94 + 0.06 * k;
  const inner = (() => {
    if (!s.crop) {
      return <Img src={staticFile(`img/${w.id}.png`)} style={{ width: "100%", height: "100%", objectFit: "contain", padding: 28, boxSizing: "border-box" }} />;
    }
    // lấy vùng rộng hơn để thấy ngữ cảnh, rồi khoanh đúng vùng bộ phận bằng vòng đỏ
    const ctx = Math.max(s.crop[2] * 1.7, 0.34);
    const ratio = (s.crop[2] * 0.7) / ctx;
    const ow = PANEL.w * ratio, oh = (ow * s.ih) / s.iw;
    // giữ khung cắt trong phạm vi cái đầu (không lộ nền trắng); vòng đỏ dời theo
    const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));
    const ccx = clamp(s.crop[0], 0.12 + ctx / 2, 0.88 - ctx / 2);
    const ccy = clamp(s.crop[1], ctx / 2, 1 - ctx / 2);
    const ox = ((s.crop[0] - ccx) / ctx) * PANEL.w, oy = ((s.crop[1] - ccy) / ctx) * PANEL.h;
    return (
      <>
        <Crop crop={[ccx, ccy, ctx]} dw={PANEL.w} dh={PANEL.h} border={0} />
        <div style={{ position: "absolute", left: (PANEL.w - ow) / 2 + ox, top: (PANEL.h - oh) / 2 + oy, width: ow, height: oh, border: `7px solid ${RED}`, borderRadius: 28, boxSizing: "border-box" }} />
      </>
    );
  })();
  return (
    <div style={{ position: "absolute", left: PANEL.x, top: PANEL.y, width: PANEL.w, height: PANEL.h, opacity: k, transform: `scale(${scale})`, zIndex: 8 }}>
      <div style={{ position: "relative", width: "100%", height: "100%", borderRadius: 36, overflow: "hidden", background: "#fff", border: "8px solid #fff", boxSizing: "border-box", boxShadow: "0 10px 30px rgba(0,0,0,0.22)" }}>{inner}</div>
    </div>
  );
};

// mũi tên từ đáy khung phóng to xuống đúng chỗ trên nhân vật
const Pointer = ({ w, i }: { w: (typeof words)[number]; i: number }) => {
  const f = useCurrentFrame();
  const local = f - INTRO - START[i];
  if (local < 0 || local >= LEN[i]) return null;
  const s = SLOTS[w.id];
  const a = { x: PANEL.x + PANEL.w / 2, y: PANEL.y + PANEL.h + 4 };
  const b = charPt(s.t);
  const dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy);
  const tip = { x: b.x - (dx / len) * 22, y: b.y - (dy / len) * 22 };
  const draw = interpolate(local, [10, 28], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.22, 1, 0.36, 1) });
  const fade = interpolate(local, [LEN[i] - 14, LEN[i]], [1, 0], { extrapolateLeft: "clamp" });
  const ang = (Math.atan2(dy, dx) * 180) / Math.PI;
  const head = interpolate(draw, [0.85, 1], [0, 1], { extrapolateLeft: "clamp" });
  const cur = { x: a.x + (tip.x - a.x) * draw, y: a.y + (tip.y - a.y) * draw };
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: fade, zIndex: 10 }}>
      <line x1={a.x} y1={a.y} x2={cur.x} y2={cur.y} stroke={RED} strokeWidth={8} strokeLinecap="round" />
      <g transform={`translate(${tip.x},${tip.y}) rotate(${ang}) scale(${head})`} opacity={head}>
        <polygon points="14,0 -22,-18 -22,18" fill={RED} />
      </g>
      <circle cx={b.x} cy={b.y} r={26} fill="none" stroke={RED} strokeWidth={6} opacity={head} />
    </svg>
  );
};

export const BodyParts = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const charIn = spring({ frame: f - 5, fps, config: { damping: 14, stiffness: 80 } });
  const h = (CHAR.w * CHAR.srcH) / CHAR.srcW;
  return (
    <AbsoluteFill style={{ background: "#FFF3DC" }}>
      <Title />
      <Img src={staticFile("img/character.png")} style={{ position: "absolute", left: CHAR.x, top: CHAR.y, width: CHAR.w, height: h, transform: `scale(${charIn})`, transformOrigin: "50% 90%" }} />
      {words.map((w, i) => (
        <Card key={w.id} w={w} i={i} />
      ))}
      <Panel />
      {words.map((w, i) => (
        <Sequence key={`a-${w.id}`} from={INTRO + START[i] + 8}>
          <Audio src={staticFile(`audio/${w.id}.wav`)} />
        </Sequence>
      ))}
      {words.map((w, i) => (
        <Pointer key={w.id} w={w} i={i} />
      ))}
    </AbsoluteFill>
  );
};
