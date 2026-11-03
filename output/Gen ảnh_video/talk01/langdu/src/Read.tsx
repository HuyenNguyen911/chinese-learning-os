import React from "react";
import { AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, staticFile, useCurrentFrame } from "remotion";
import data from "./data.json";
import timing from "./timing.json";
import outro from "./outro.json";
import { Outro, outroSec } from "./Outro";
import sizes from "./sizes.json";

/* Video 朗读 9:16: bố cục cố định suốt video. Bài đọc xếp từng chữ vào ô lưới (vị trí tính sẵn) để
   gạch chân tiến độ + tô đỏ từ khoá chính xác theo giọng. timing.json = giây bắt đầu của từng chữ
   (chưa có giọng thì mỗi chữ SEC_PER_CHAR giây). Thẻ từ góc phải đổi nghĩa theo prop lang (en | vi). */
export const FPS = 30;
const W = 1080;
const FS = 44, CPL = 21, LH = 70, X0 = 78, Y0 = 180;     // cỡ chữ, chữ/dòng, cao dòng, lề trái, dòng đầu
const LEAD = 1.0, SEC_PER_CHAR = 0.24;                      // giây trước khi đọc, giây/chữ tạm (chưa có giọng)
const FONT = '"Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif';
const C = { ink: "#26231f", red: "#D2382B", green: "#3E8E5E", line: "#DCD5C6", bg: "#FFFBF2" };

type Word = { han: string; py: string; en: string; vi: string };
const words = data.words as Word[];
// Ngoặc kép thẳng -> ngoặc kép Trung (cùng dấu, chỉ đổi kiểu chữ cho vừa ô)
let q = 0;
const text = [...data.text].map((c) => (c === '"' ? (q++ % 2 ? "”" : "“") : c));
const NO_START = "，。、：；？！”）》—";

// Xếp chữ vào lưới: dấu câu không được đứng đầu dòng -> đẩy lên cuối dòng trước (tràn 1 ô)
const pos: { x: number; y: number; line: number }[] = [];
let line = 0, col = 0;
text.forEach((c) => {
  if (col >= CPL && !NO_START.includes(c)) { line++; col = 0; }
  pos.push({ x: X0 + col * FS, y: Y0 + line * LH, line });
  col++;
});
const LINES = line + 1;

// Từ khoá: chỉ số chữ bắt đầu/kết thúc (lần xuất hiện đầu)
const plain = text.join("");
const marks = words.map((w) => { const s = plain.indexOf(w.han); return { ...w, s, e: s + w.han.length }; }).filter((m) => m.s >= 0);
const red = new Set(marks.flatMap((m) => Array.from({ length: m.e - m.s }, (_, i) => m.s + i)));

const T: number[] = (timing as { chars?: number[] }).chars?.length === text.length
  ? (timing as { chars: number[] }).chars.map((t) => t + LEAD)
  : text.map((_, i) => LEAD + i * SEC_PER_CHAR);
const END = (timing as { end?: number }).end ? (timing as { end: number }).end + LEAD : T[T.length - 1] + SEC_PER_CHAR;
const HAS_VOICE = !!(timing as { end?: number }).end;
const OUTRO_START = END + 1.2;                                     // đọc xong nghỉ 1.2s rồi vào đoạn kết
export const TOTAL = Math.round((OUTRO_START + outroSec(outro.sec)) * FPS);

const WM_SPOTS: [number, number][] = [[470, 1850], [780, 1850], [620, 1820]];
const ease = Easing.bezier(0.45, 0, 0.55, 1);
const sz = sizes as Record<string, number[]>;

export const Read: React.FC<{ lang: "en" | "vi" }> = ({ lang }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  // số chữ đã đọc (có phần lẻ để gạch chân chạy mượt)
  let k = 0;
  while (k < T.length && T[k] <= t) k++;
  const frac = k > 0 && k < T.length ? Math.min(1, (t - T[k - 1]) / (T[k] - T[k - 1])) : 0;
  const read = k === 0 ? 0 : k - 1 + frac;
  const cur = marks.filter((m) => T[m.s] <= t).pop();                // thẻ: từ khoá gần nhất đã đọc tới
  const cardIn = cur ? interpolate(t - T[cur.s], [0, 0.25], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease }) : 0;
  const [cw, ch] = sz[data.character] ?? [425, 887];
  const charH = 670, charW = (cw / ch) * charH;
  const bob = Math.sin(t * 2.2) * 4;
  const textEnd = Y0 + LINES * LH;                                    // đáy bài đọc -> chữ ký nằm ngay dưới
  const wm = WM_SPOTS[Math.floor(t / 6) % WM_SPOTS.length];            // dấu chìm nhỏ đổi chỗ mỗi 6s (khó cắt bỏ)

  return (
    <AbsoluteFill style={{ background: C.bg, fontFamily: FONT }}>
      {/* nhạc nền vui nhẹ, rất nhỏ (Mixkit "A Happy Child"), vào/ra từ từ */}
      <Audio src={staticFile("audio/bg.mp3")} loop volume={(fr) => 0.09 * Math.min(1, fr / (FPS * 1.5), (TOTAL - fr) / (FPS * 2.5))} />
      {HAS_VOICE && <Sequence from={Math.round(LEAD * FPS)}><Audio src={staticFile("audio/read.wav")} /></Sequence>}
      {/* A. 1 dòng: 朗读 | tên chủ đề */}
      <div style={{ position: "absolute", top: 58, left: 0, right: 0, display: "flex", justifyContent: "center", alignItems: "baseline", gap: 22 }}>
        <div style={{ position: "relative", fontSize: 58, fontWeight: 800, color: C.ink, letterSpacing: 10, isolation: "isolate" }}>
          <div style={{ position: "absolute", left: -14, right: -4, bottom: 4, height: 26, borderRadius: 13, background: "#BFE3CC", zIndex: -1 }} />
          {data.title}
        </div>
        <div style={{ fontSize: 40, color: C.line, fontWeight: 300 }}>|</div>
        <div style={{ fontSize: 50, fontWeight: 700, color: C.green }}>{data.topic}</div>
      </div>
      <div style={{ position: "absolute", top: 70, right: 46, fontSize: 24, fontWeight: 700, color: C.red, background: "#fff", border: `3px solid ${C.red}`, borderRadius: 10, padding: "3px 10px" }}>禁止搬运</div>

      {/* B. bài đọc: dòng kẻ + gạch chân tiến độ + chữ */}
      {Array.from({ length: LINES }, (_, li) => {
        const ids = pos.map((p, i) => (p.line === li ? i : -1)).filter((i) => i >= 0);
        const x1 = pos[ids[0]].x, x2 = pos[ids[ids.length - 1]].x + FS;
        const done = Math.max(0, Math.min(ids.length, read - ids[0]));
        const xp = x1 + done * FS;
        const y = Y0 + li * LH + FS + 12;
        return (
          <React.Fragment key={li}>
            {done > 0 && <div style={{ position: "absolute", left: x1, width: Math.min(xp, x2) - x1, top: y - 1, height: 3, borderRadius: 2, background: C.green, opacity: 0.85 }} />}
          </React.Fragment>
        );
      })}
      {text.map((c, i) => (
        <div key={i} style={{ position: "absolute", left: pos[i].x, top: pos[i].y, width: FS, height: FS, lineHeight: `${FS}px`, textAlign: "center", fontSize: FS, color: red.has(i) ? C.red : C.ink, fontWeight: red.has(i) ? 700 : 400 }}>{c}</div>
      ))}
      {/* chữ ký dưới chân bài đọc */}
      <div style={{ position: "absolute", top: textEnd + 4, right: 70, fontSize: 30, fontWeight: 700, color: C.green, fontStyle: "italic" }}>—— {data.channel}</div>

      {/* nhân vật góc trái dưới */}
      <div style={{ position: "absolute", left: 36, top: 1910 - charH, width: charW, height: charH }}>
        <div style={{ position: "absolute", left: charW * 0.12, right: charW * 0.12, bottom: -8, height: 30, borderRadius: "50%", background: "rgba(80,70,50,0.12)" }} />
        <Img src={staticFile(`img/${data.character}.png`)} style={{ width: "100%", height: "100%", transform: `translateY(${bob}px)` }} />
      </div>

      {/* thẻ từ góc phải */}
      <div style={{ position: "absolute", left: 400, right: 46, top: textEnd + 90, height: 340, borderRadius: 32, background: "#fff", border: `4px solid ${C.red}`, boxShadow: "0 10px 28px rgba(60,40,20,0.12)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "20px 26px", textAlign: "center" }}>
        <div style={{ position: "absolute", top: -24, left: 30, background: C.green, color: "#fff", fontSize: 26, fontWeight: 700, borderRadius: 12, padding: "4px 16px" }}>重点词</div>
        {cur && (
          <div style={{ opacity: cardIn, transform: `translateY(${(1 - cardIn) * 20}px)` }}>
            <div style={{ fontSize: cur.han.length > 5 ? 62 : 88, fontWeight: 800, color: C.red, lineHeight: 1.15 }}>{cur.han}</div>
            <div style={{ fontSize: 40, color: "#5b5248", marginTop: 10 }}>{cur.py}</div>
            <div style={{ fontSize: 36, color: C.green, marginTop: 8, fontFamily: '"Segoe UI",sans-serif', lineHeight: 1.25 }}>{lang === "vi" ? cur.vi : cur.en}</div>
          </div>
        )}
      </div>

      <Sequence from={Math.round(OUTRO_START * FPS)}><Outro text="谢谢大家的收听～喜欢的话，记得点赞、关注我哦！" /></Sequence>
      {/* dấu chìm nhỏ, đổi chỗ định kỳ */}
      <div style={{ position: "absolute", left: wm[0], top: wm[1], fontSize: 26, fontWeight: 700, color: C.ink, opacity: 0.16 }}>瑾玄在练嘴</div>
    </AbsoluteFill>
  );
};
