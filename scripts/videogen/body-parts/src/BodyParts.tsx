import { AbsoluteFill, Audio, Sequence, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import words from "../words.json";
import layout from "../layout.json";
import durations from "./durations.json";

// MỘT hiệu ứng duy nhất: thẻ đang đọc phóng to + đổi đỏ + sáng; các thẻ khác mờ đi. Không mũi tên, không khung phụ.

export const FPS = 30;
export const INTRO = 75;
export const OUTRO = 60;

type Slot = { x: number; y: number; iw: number; ih: number; crop?: number[] };
const SLOTS = layout.slots as Record<string, Slot>;
const CHAR = layout.char;
const FOCUS = layout.focusScale;

// thời lượng mỗi từ = độ dài giọng đọc + ~1.1s, tối thiểu 54 khung
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

const envelope = (local: number, len: number) =>
  interpolate(local, [0, 14, len - 14, len], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: SMOOTH });

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
const Crop = ({ crop, dw, dh }: { crop: number[]; dw: number; dh: number }) => {
  const [cx, cy, cw] = crop;
  const ch = (cw * dh) / dw;
  const imgW = dw / cw;
  return <Img src={staticFile("img/portrait.png")} style={{ position: "absolute", width: imgW, height: imgW, left: -(cx - cw / 2) * imgW, top: -(cy - ch / 2) * imgW, maxWidth: "none" }} />;
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
  const dim = 1 - 0.7 * seq * (1 - k);
  const cellW = Math.max(s.iw, 200);
  const round = s.iw === s.ih ? "50%" : 40;
  const visual = s.crop ? (
    <div style={{ position: "relative", width: s.iw, height: s.ih, borderRadius: round, overflow: "hidden", background: "#fff", boxShadow: `0 4px 12px rgba(0,0,0,0.12), 0 0 ${30 * k}px ${8 * k}px rgba(229,57,43,${0.65 * k})` }}>
      <Crop crop={s.crop} dw={s.iw} dh={s.ih} />
    </div>
  ) : (
    <Img src={staticFile(`img/${w.id}.png`)} style={{ maxWidth: s.iw, maxHeight: s.ih, objectFit: "contain", filter: k > 0.02 ? `drop-shadow(0 0 ${22 * k}px rgba(229,57,43,${0.8 * k}))` : undefined }} />
  );
  return (
    <div style={{ position: "absolute", left: s.x - cellW / 2, top: s.y, width: cellW, textAlign: "center", opacity: enter * dim, transform: `scale(${enter * (1 + (FOCUS - 1) * k)})`, transformOrigin: "50% 50%", zIndex: active ? 5 : 1 }}>
      <div style={{ height: s.ih, display: "flex", alignItems: "center", justifyContent: "center" }}>{visual}</div>
      <div style={{ fontFamily: HAN, fontSize: 54, fontWeight: 700, lineHeight: 1.15, marginTop: 8, color: mix("#3E7CB1", RED, k) }}>{w.han}</div>
      <div style={{ fontFamily: HAN, fontSize: 28, lineHeight: 1.2, color: mix("#7A6A55", RED, k) }}>{w.pinyin}</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: s.ih + 100, fontFamily: HAN, fontSize: 24, lineHeight: 1.2, color: RED, opacity: k }}>{w.vi}</div>
    </div>
  );
};

export const BodyParts = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const charIn = spring({ frame: f - 5, fps, config: { damping: 14, stiffness: 80 } });
  const h = (CHAR.w * CHAR.srcH) / CHAR.srcW;
  const seq = interpolate(f, [INTRO - 12, INTRO + 8, SEQ_END - 8, SEQ_END + 12], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ background: "#FFF3DC" }}>
      <Title />
      <Img src={staticFile("img/character.png")} style={{ position: "absolute", left: CHAR.x, top: CHAR.y, width: CHAR.w, height: h, opacity: 1 - 0.55 * seq, transform: `scale(${charIn})`, transformOrigin: "50% 90%" }} />
      {words.map((w, i) => (
        <Card key={w.id} w={w} i={i} />
      ))}
      {words.map((w, i) => (
        <Sequence key={`a-${w.id}`} from={INTRO + START[i] + 8}>
          <Audio src={staticFile(`audio/${w.id}.wav`)} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
