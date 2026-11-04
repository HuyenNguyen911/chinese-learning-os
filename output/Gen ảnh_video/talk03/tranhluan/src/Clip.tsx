import React from "react";
import { AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import dur from "./durations.json";
import outro from "./outro.json";
import { Outro, outroSec } from "./Outro";

/* Clip tranh luận Talk series · tập 03 (活人图书馆) — 越黄 hỏi, 瑾玄 hiểu nhầm thành "thư viện hay đi".
   Chữ trên video: toàn tiếng Trung; từ khó hiện thẻ 汉字 + pinyin + nghĩa EN. Mỗi câu 1 đoạn muse-video riêng (chỉ người nói mở miệng); khung = nền công viên + cặp nhân vật tách nền ghép (compose_key.py), phủ kín 9:16. */
export const FPS = 30;
const FONT = '"Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif';
const C = { ink: "#26231f", red: "#D2382B", green: "#3E8E5E", bg: "#FFFBF2", sub: "#5b5248", jx: "#E58AA4", yh: "#D2382B" };
const D = dur as Record<string, number>;
const GAP = 0.3;

type Sc = { id: string; img: string; clip: string; who?: "jx" | "yh"; voice?: string; sec?: number; text: string; card?: boolean; q?: boolean };
const SC: Sc[] = [
  { id: "1a", img: "S1a", clip: "m_walk", sec: 2.4, text: "" },
  { id: "1b", img: "S1a", clip: "m_ask", who: "yh", voice: "l1b", text: "瑾玄，你知道“活人图书馆”是什么吗？", card: true },
  { id: "2", img: "S2", clip: "m_p2", who: "jx", voice: "l2", text: "图书馆？" },
  { id: "3", img: "S2", clip: "m_p3", who: "jx", voice: "l3", text: "我常去啊！" },
  { id: "4", img: "S2", clip: "m_p4", who: "jx", voice: "l4", text: "那儿的书，我都快借遍了。" },
  { id: "5", img: "S3", clip: "m_p5", who: "yh", voice: "l5", text: "不是，不是那种图书馆……" },
  { id: "6", img: "S3", clip: "m_p6", who: "yh", voice: "l6", text: "你说的是借书的地方。" },
  { id: "7", img: "S4", clip: "m_p7", who: "jx", voice: "l7", text: "那还能借什么？", q: true },
  { id: "8", img: "S8", clip: "m_look", sec: 1.6, text: "" },
  { id: "9", img: "S8", clip: "m_q", who: "yh", voice: "l9", text: "大家知道“活人图书馆”是什么吗？评论区见！", card: true },
];
const T0 = 0;   // khung 0 đã có nhân vật + tiêu đề (ảnh đại diện trên feed — user nhắc nhiều lần)
let acc = T0;
const TL = SC.map((s) => { const len = (s.voice ? D[s.voice] : s.sec!) + (s.voice ? GAP : 0); const o = { ...s, t0: acc, len }; acc += len; return o; });
const END = acc + 0.6;
const CL = [...new Set(TL.map((x) => x.clip))].map((id) => { const g = TL.filter((x) => x.clip === id); return { id, from: g[0].t0, to: g[g.length - 1].t0 + g[g.length - 1].len }; });
export const CLIP_SECS = Object.fromEntries(CL.map((c) => [c.id, c.to - c.from + 0.3]));
const NF = (id: string) => Math.ceil((CLIP_SECS[id]) * FPS) + 2;
export const TOTAL = Math.round((END + outroSec(outro.sec)) * FPS);

const ease = Easing.bezier(0.45, 0, 0.55, 1);
export const Clip: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const cur = TL.find((s) => t >= s.t0 && t < s.t0 + s.len) ?? TL[TL.length - 1];
  const prevImg = TL[TL.indexOf(cur) - 1]?.img;
  const local = t - cur.t0;
  const speaking = !!cur.voice && local < D[cur.voice!];
  const zoom = 1 + 0.05 * Math.min(1, local / cur.len);
  const bob = speaking ? Math.sin(local * 14) * 5 : 0;
  const swap = prevImg && prevImg !== cur.img ? interpolate(local, [0, 0.25], [0, 1], { extrapolateRight: "clamp" }) : 1;
  const wob = cur.q ? Math.sin(local * 5) * 1.2 : 0;
  const chip = cur.who === "yh" ? { n: "越黄", bg: "#FBD9B4" } : cur.who === "jx" ? { n: "瑾玄", bg: "#BFE3CC" } : null;
  const sp = spring({ frame: f - Math.round(cur.t0 * fps), fps, config: { damping: 14 } });
  const TOT = TOTAL / FPS;
  const bgVol = 0.13 * Math.min(1, t / 0.6 + 0.3, (TOT - t) / 1.5);   // nhạc nền chạy SUỐT, kể cả đoạn kết follow
  const fs = Math.min(80, 980 / Math.max(1, cur.text.length));
  return (
    <AbsoluteFill style={{ background: C.bg, fontFamily: FONT }}>
      <Audio src={staticFile("audio/bg.mp3")} loop volume={Math.max(0, bgVol)} />
      {TL.filter((s) => s.voice).map((s) => (
        <Sequence key={s.id} from={Math.round((s.t0 + 0.05) * fps)}><Audio src={staticFile(`audio/${s.voice}.mp3`)} /></Sequence>
      ))}
      {TL.filter((s) => s.q).map((s) => (
        <Sequence key={"p" + s.id} from={Math.round((s.t0 + 0.1) * fps)}><Audio src={staticFile("sfx/pop_bubble.mp3")} volume={0.45} /></Sequence>
      ))}

      {/* cảnh dọc 9:16 phủ kín khung (như talk02/tranhluan) */}
      <AbsoluteFill style={{ background: "#CFE8F0" }}>
        <div style={{ position: "absolute", inset: 0 }}>
        {CL.map((c) => {
          const lo = c.from - 0.25, hi = c.to + 0.25;
          if (t < lo || t > hi) return null;
          const op = interpolate(t, [lo, c.from, c.to, hi], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const i = Math.max(0, Math.min(NF(c.id) - 1, Math.round((t - c.from) * FPS)));
          return <Img key={c.id} src={staticFile(`frames/${c.id}/${String(i + 1).padStart(4, "0")}.jpg`)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", opacity: op }} />;
        })}
        </div>
      </AbsoluteFill>

      <div style={{ position: "absolute", top: 70, right: 46, fontSize: 24, fontWeight: 700, color: C.red, background: "#fff", border: `3px solid ${C.red}`, borderRadius: 10, padding: "3px 10px" }}>禁止搬运</div>

      {/* phụ đề: chữ trắng viền đậm ở đầu khung, không đóng khung */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 230, textAlign: "center", fontSize: fs, fontWeight: 800, color: "#fff", WebkitTextStroke: "11px #3a2a1c", paintOrder: "stroke fill", whiteSpace: "nowrap", opacity: cur.text && t < END ? Math.min(1, sp) : 0 }}>{cur.text}</div>
      {/* tiêu đề mở đầu (từ khung 0, tới khi 越黄 bắt đầu hỏi) */}
      {t < TL[1].t0 + 0.3 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 250, textAlign: "center", fontSize: 128, fontWeight: 900, color: "#fff", WebkitTextStroke: "16px #3a2a1c", paintOrder: "stroke fill", whiteSpace: "nowrap", opacity: interpolate(t, [TL[1].t0 - 0.05, TL[1].t0 + 0.3], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>活人图书馆？</div>
      )}
      <div style={{ position: "absolute", left: 0, right: 0, top: 1790, textAlign: "center", fontSize: 30, color: "#fff", opacity: 0.35, fontWeight: 700 }}>瑾玄在练嘴</div>
      <div style={{ position: "absolute", right: 46, top: 1830, fontSize: 32, fontWeight: 800, color: "#fff", WebkitTextStroke: "6px #3a2a1c", paintOrder: "stroke fill" }}>@瑾玄在练嘴</div>
      <Sequence from={Math.round(END * fps)}><Outro text="谢谢大家的观看～喜欢的话，记得点赞、关注我哦！" /></Sequence>
    </AbsoluteFill>
  );
};
