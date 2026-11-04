import React from "react";
import { AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import timing from "./timing.json";
import intro from "./intro.json";
import outro from "./outro.json";
import lines from "./lines.json";
import frames from "./frames.json";
import data from "./data.json";
import plan from "./plan.json";
import { Outro, outroSec } from "./Outro";
import { C, FONT, SANS, PH, Title, Peeker, Card, Tag, Branch, t as tr, Lang, Ph } from "./Frames";

/* VIDEO HOÀN CHỈNH HSKK 高级 · Chủ đề 3 (活人图书馆) · câu 6 · 回答问题 (9:16, 1080x1920). Nhân vật 瑾玄.
   Cảnh: S1 câu hỏi -> S2 mindmap -> S3 8 cụm đáng học (1 màn) -> 现在开始 -> S4 clip minh hoạ + phụ đề -> kết follow.
   Lịch clip đọc từ plan.json (CHUNG với make_frames.py). Khoảng lặng "gap" chèn trước dòng gapLine: giọng đọc ngắt ra,
   người đọc (chàng trai đeo kính) nhép miệng hỏi, rồi 瑾玄 kể tiếp. Cảnh hồi tưởng (plan.mem) phủ sepia nhẹ + viền tối, loé trắng lúc vào/ra. */
export const FPS = 30;
type Clip = [number | "gap", number | "gap", string];
const P = plan as { gapLine: number; gap: number; virt: number[]; clips: Clip[]; use: Record<string, number>; mem: string[] };
const CH = (timing as { chars: number[] }).chars;
const ANS0 = (timing as { end: number }).end;
const IDX = lines.idx as number[];
const GL = P.gapLine, GAP = P.gap;
const CUT = CH[IDX[GL - 1]];                                    // giây (trong read.wav) bắt đầu dòng gapLine
const chT = (i: number) => CH[i] + (i >= IDX[GL - 1] ? GAP : 0);
const ANS = ANS0 + GAP;

type Ln = { zh: string; vi: string; en: string; t0: number; t1: number };
const TXT = data.text;
const LN: Ln[] = IDX.map((s, i) => {
  const e = i + 1 < IDX.length ? IDX[i + 1] : TXT.length;
  const t1 = i + 1 >= IDX.length ? ANS : i + 1 === GL - 1 ? CUT : chT(IDX[i + 1]);
  return { zh: TXT.slice(s, e), vi: lines.vi[i], en: lines.en[i], t0: chT(s), t1 };
});
const N = LN.length;
const lineT = (n: number) => (n === 0 ? -(intro.now + 0.7) : n <= N ? LN[n - 1].t0 : ANS + P.virt[n - N - 1]);
const SEGS = P.clips.map(([a, b, id]) => {
  const s = a === "gap" ? CUT : lineT(a), e = a === "gap" ? CUT + GAP : (b as number) + 1 === GL ? CUT : lineT((b as number) + 1);
  return { id, s, e };
});
const HOLD = P.virt[P.virt.length - 1];
const MEM = new Set(P.mem);

// cụm đáng học theo dòng (1-based); 1 dòng có thể có 2 cụm (dòng 20: 追梦 + 一帆风顺)
const PHRASE_AT: Record<number, (keyof typeof PH)[]> = { 6: ["fc"], 10: ["bzs"], 14: ["zyc"], 17: ["np"], 20: ["zm", "yf"], 21: ["zyd"], 27: ["mm"] };
const S3_LIST = ["fc", "bzs", "zyc", "np", "yf", "mm", "zyd", "zm"] as (keyof typeof PH)[];
const hlOf = (p: Ph) => p.han.split("…")[0];

// ---- lịch cảnh (giây, toàn video)
const Q0 = 0.7;
const S1_END = Q0 + intro.q + 1.0;
const S2_0 = S1_END, S2_END = S2_0 + 12.5;
const S3_0 = S2_END, S3_STEP = 2.7, S3_END = S3_0 + 1.0 + S3_LIST.length * S3_STEP + 0.8;
const S4_0 = S3_END, NOW0 = S4_0 + 0.3, A0 = NOW0 + intro.now + 0.7;
const ANS_END = A0 + ANS, OUT0 = ANS_END + HOLD;
export const TOTAL = Math.round((OUT0 + outroSec(outro.sec)) * FPS);

const FR = frames as Record<string, number>;
const SegFrames: React.FC<{ id: string; style: React.CSSProperties }> = ({ id, style }) => {
  const f = useCurrentFrame();
  const i = Math.max(0, Math.min(FR[id] - 1, f));
  return <Img src={staticFile(`frames/${id}/${String(i + 1).padStart(4, "0")}.jpg`)} style={style} />;
};
const ease = Easing.bezier(0.45, 0, 0.55, 1);
const WM = [[470, 1850], [780, 1850], [620, 1820], [300, 1850]];

const Hl: React.FC<{ s: string; hl: string[] }> = ({ s, hl }) => {
  const out: React.ReactNode[] = []; let rest = s, k = 0;
  while (rest.length) {
    const hits = hl.map((h) => [rest.indexOf(h), h] as [number, string]).filter(([i]) => i >= 0).sort((a, b) => a[0] - b[0]);
    if (!hits.length) { out.push(rest); break; }
    const [i, h] = hits[0];
    if (i > 0) out.push(rest.slice(0, i));
    out.push(<span key={k++} style={{ color: C.red, fontWeight: 800 }}>{h}</span>);
    rest = rest.slice(i + h.length);
  }
  return <>{out}</>;
};
const Sub: React.FC<{ ln: Ln; lang: Lang; dim?: boolean; hl?: string[] }> = ({ ln, lang, dim, hl }) => {
  const tr2 = lang === "vi" ? ln.vi : ln.en;
  return (
    <div style={{ opacity: dim ? 0.4 : 1, textAlign: "center", whiteSpace: "nowrap" }}>
      <div style={{ fontSize: Math.min(dim ? 46 : 62, 980 / ln.zh.length), fontWeight: 700, color: C.ink, lineHeight: 1.3 }}>
        {hl && hl.length ? <Hl s={ln.zh} hl={hl} /> : ln.zh}
      </div>
      <div style={{ fontSize: Math.min(dim ? 29 : 36, 1000 / (0.52 * Math.max(1, tr2.length))), color: C.green, marginTop: 8, fontFamily: SANS, lineHeight: 1.3 }}>{tr2}</div>
    </div>
  );
};
const PhCard: React.FC<{ p: Ph; lang: Lang; style: React.CSSProperties }> = ({ p, lang, style }) => (
  <Card style={{ top: 1470, height: 210, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", textAlign: "center", borderRadius: 26, ...style }}>
    <Tag>重点词</Tag>
    <div style={{ fontSize: p.han.length > 6 ? 44 : 60, fontWeight: 800, color: C.red, lineHeight: 1.15, whiteSpace: "nowrap" }}>{p.han}</div>
    <div style={{ fontSize: 25, color: C.sub, marginTop: 2, whiteSpace: "nowrap" }}>{p.py ? p.py + " · " : ""}<span style={{ color: C.green, fontFamily: SANS }}>{lang === "vi" ? p.vi : p.en}</span></div>
  </Card>
);

export const Full: React.FC<{ lang: Lang }> = ({ lang }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const k = (a: number, b: number) => interpolate(t, [a, b], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const wm = WM[Math.floor(t / 6) % WM.length];
  const ta = t - A0;
  const curI = ta >= 0 ? LN.findIndex((l) => ta >= l.t0 && ta < l.t1) : -1;
  const cur = curI >= 0 ? LN[curI] : null;
  const prev = curI > 0 ? LN[curI - 1] : null;
  const phs = cur ? (PHRASE_AT[curI + 1] ?? []).map((x) => PH[x]) : [];

  const voices: [number, number][] = [[Q0, Q0 + intro.q], [NOW0, NOW0 + intro.now], [A0, ANS_END], [OUT0 + 0.2, OUT0 + 0.2 + outro.sec],
    ...S3_LIST.map((_, i) => [S3_0 + 1.0 + i * S3_STEP, S3_0 + 1.0 + i * S3_STEP + 2.0] as [number, number])];
  const duck = Math.min(...voices.map(([s, e]) => interpolate(t, [s - 0.3, s, e, e + 0.5], [1, 0.3, 0.3, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));
  const bgVol = 0.22 * duck * Math.min(1, t / 1.5, (TOTAL / fps - t) / 2.0);

  const inS1 = t < S2_0, inS2 = t >= S2_0 && t < S3_0, inS3 = t >= S3_0 && t < S4_0, inS4 = t >= S4_0 && t < OUT0;
  const sceneFade = (a: number, b: number) => Math.min(k(a, a + 0.35), 1 - k(b - 0.35, b));
  // hồi tưởng: độ phủ sepia theo cảnh hiện tại + loé trắng ở mỗi lần vào/ra
  const segNow = SEGS.find((g) => ta >= g.s && ta < g.e);
  const memEdges = SEGS.filter((g, i) => i > 0 && MEM.has(g.id) !== MEM.has(SEGS[i - 1].id)).map((g) => g.s);
  const memOn = Math.max(0, ...SEGS.filter((g) => MEM.has(g.id)).map((g) => interpolate(ta, [g.s - 0.15, g.s + 0.2, g.e - 0.2, g.e + 0.1], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));
  const flash = Math.max(0, ...memEdges.map((x) => interpolate(ta, [x - 0.18, x, x + 0.55], [0, 0.85, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));

  return (
    <AbsoluteFill style={{ background: C.bg, fontFamily: FONT }}>
      <Audio src={staticFile("audio/bg.mp3")} loop volume={bgVol} />
      <Sequence from={Math.round(Q0 * fps)}><Audio src={staticFile("audio/intro_q.wav")} /></Sequence>
      <Sequence from={Math.round(NOW0 * fps)}><Audio src={staticFile("audio/intro_now.wav")} /></Sequence>
      {/* giọng đọc tách 2 phần quanh khoảng lặng (người đọc nhép miệng hỏi) */}
      <Sequence from={Math.round(A0 * fps)} durationInFrames={Math.round(CUT * fps)}><Audio src={staticFile("audio/read.wav")} /></Sequence>
      <Sequence from={Math.round((A0 + CUT + GAP) * fps)}><Audio src={staticFile("audio/read.wav")} startFrom={Math.round(CUT * fps)} /></Sequence>
      {S3_LIST.map((_, i) => <Sequence key={i} from={Math.round((S3_0 + 1.0 + i * S3_STEP) * fps)}><Audio src={staticFile(`audio/intro_p${i}.wav`)} /></Sequence>)}

      <Title />

      {inS1 && (
        <AbsoluteFill style={{ opacity: 1 - k(S1_END - 0.3, S1_END) }}>
          <Peeker x={820} y={600} w={210} />
          <Card style={{ left: 46, right: 46, top: 600, height: 640, display: "flex", flexDirection: "column", justifyContent: "center", padding: "0 50px" }}>
            <div style={{ fontSize: 56, fontWeight: 800, color: C.ink, lineHeight: 1.5, whiteSpace: "nowrap" }}>
              如果你是活人图书馆的<br />一本“书”，你会是一本<br /><span style={{ color: C.red }}>什么样的“书”</span>？
            </div>
            <div style={{ fontSize: 36, color: C.green, marginTop: 30, fontFamily: SANS, lineHeight: 1.35 }}>
              {tr(lang, "If you were a \"book\" in a Human Library, what kind of \"book\" would you be?", "Nếu bạn là một \"cuốn sách\" trong thư viện người sống, bạn sẽ là cuốn sách thế nào?")}
            </div>
          </Card>
        </AbsoluteFill>
      )}

      {inS2 && (
        <AbsoluteFill style={{ opacity: sceneFade(S2_0, S2_END) }}>
          <div style={{ position: "absolute", left: 140, width: 720, top: 200, height: 130, borderRadius: 26, background: "#E4ECFA", border: "5px solid #3A6EBE", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 54, fontWeight: 800, color: "#2B57A0" }}>我是一本什么书？</div>
          <div style={{ position: "absolute", left: 100, top: 330, width: 0, height: 1330, borderLeft: `5px dashed ${C.line}` }} />
          {[
            { i: 0, y: 370, idea: "一本《寻找自己》的书", ex: "不是成功的人，是普通人" },
            { i: 1, y: 620, idea: "成长、犯错、重新选择", ex: "慢慢找到自己" },
            { i: 2, y: 870, idea: "学中文：敢开口", ex: "才看到自己的潜力" },
            { i: 3, y: 1120, idea: "人生也一样", ex: "遇到困难能坚持下去" },
            { i: 4, y: 1370, idea: "给人多一点勇气", ex: "这本书就值得被借阅" },
          ].map((b, n) => {
            const a = S2_0 + 0.6 + n * 2.2;
            const sp = spring({ frame: f - Math.round(a * fps), fps, config: { damping: 14 } });
            return <div key={b.i} style={{ opacity: Math.min(1, sp), transform: `translateY(${(1 - Math.min(1, sp)) * 24}px)` }}><Branch i={b.i} y={b.y} idea={b.idea} ex={b.ex} /></div>;
          })}
        </AbsoluteFill>
      )}

      {/* S3: 8 cụm trên CÙNG 1 màn (user yêu cầu không rớt sang khung sau) */}
      {inS3 && (
        <AbsoluteFill style={{ opacity: sceneFade(S3_0, S3_END) }}>
          <div style={{ position: "absolute", top: 150, left: 0, right: 0, textAlign: "center", fontSize: 40, fontWeight: 700, color: C.green }}>{tr(lang, "Phrases to learn", "Cụm đáng học")}</div>
          {S3_LIST.map((key, i) => {
            const p = PH[key];
            const a = S3_0 + 1.0 + i * S3_STEP;
            const sp = spring({ frame: f - Math.round(a * fps), fps, config: { damping: 14 } });
            const on = t >= a && t < a + 2.0;
            return (
              <div key={key} style={{ opacity: Math.min(1, sp), transform: `translateY(${(1 - Math.min(1, sp)) * 30}px) scale(${on ? 1.03 : 1})` }}>
                <Card style={{ left: 46, right: 46, top: 220 + i * 178, height: 158, display: "flex", alignItems: "center", gap: 26, padding: "0 34px", borderRadius: 26, borderColor: on ? C.red : "#E9B7B0" }}>
                  <div style={{ fontSize: p.han.length > 6 ? 42 : 58, fontWeight: 800, color: C.red, lineHeight: 1.15, width: 440, flexShrink: 0, whiteSpace: "nowrap" }}>{p.han}</div>
                  <div style={{ display: "flex", flexDirection: "column", lineHeight: 1.25 }}>
                    {p.py && <div style={{ fontSize: 26, color: C.sub, whiteSpace: "nowrap" }}>{p.py}</div>}
                    <div style={{ fontSize: 31, color: C.green, fontFamily: SANS, marginTop: 4 }}>{lang === "vi" ? p.vi : p.en}</div>
                  </div>
                </Card>
              </div>
            );
          })}
        </AbsoluteFill>
      )}

      {inS4 && (
        <AbsoluteFill style={{ opacity: k(S4_0, S4_0 + 0.4) }}>
          <div style={{ position: "absolute", left: 0, right: 0, top: 150, fontSize: 44, fontWeight: 800, color: C.ink, textAlign: "center", lineHeight: 1.35, whiteSpace: "nowrap" }}>
            如果你是活人图书馆的一本“书”，<br />你会是一本什么样的“书”？
          </div>
          <div style={{ position: "absolute", left: 46, right: 46, top: 430, height: 556, borderRadius: 36, overflow: "hidden", border: `4px solid ${C.green}`, background: "#E3F2E9" }}>
            {t < A0 + SEGS[0].s + 0.05 && <Img src={staticFile("img/K1_key.png")} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover" }} />}
            {SEGS.map((sg, n) => {
              const from = A0 + sg.s - (n === 0 ? 0 : 0.3), to = n === SEGS.length - 1 ? OUT0 + 0.5 : A0 + sg.e + 0.3;
              if (t < from || t > to) return null;
              const op = n === 0 && t < A0 + sg.s + 0.3 ? 1 : interpolate(t, [from, from + 0.3, to - 0.3, to], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
              return (
                <Sequence key={sg.id} from={Math.round(from * fps)}>
                  <SegFrames id={sg.id} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", opacity: op,
                    filter: memOn > 0 && MEM.has(sg.id) ? `sepia(${0.5 * memOn}) saturate(${1 - 0.15 * memOn}) contrast(0.96)` : undefined }} />
                </Sequence>
              );
            })}
            {memOn > 0 && <div style={{ position: "absolute", inset: 0, opacity: memOn, background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(60,40,20,0.5) 100%)" }} />}
            {flash > 0 && <div style={{ position: "absolute", inset: 0, background: "#fff", opacity: flash }} />}
            {t < A0 && (
              <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
                <div style={{ fontSize: 120, fontWeight: 800, color: "#fff", WebkitTextStroke: `10px ${C.green}`, paintOrder: "stroke fill", transform: `scale(${0.8 + 0.2 * k(NOW0, NOW0 + 0.3)})`, opacity: k(NOW0, NOW0 + 0.3) }}>现在开始！</div>
              </div>
            )}
          </div>
          {cur && (
            <div style={{ position: "absolute", left: 0, right: 0, top: 1060, display: "flex", flexDirection: "column", gap: 44 }}>
              {prev && <Sub ln={prev} lang={lang} dim />}
              <Sub ln={cur} lang={lang} hl={phs.map(hlOf)} />
            </div>
          )}
          {phs.length === 1 && <PhCard p={phs[0]} lang={lang} style={{ left: 200, right: 200 }} />}
          {phs.length === 2 && (<>
            <PhCard p={phs[0]} lang={lang} style={{ left: 46, width: 480 }} />
            <PhCard p={phs[1]} lang={lang} style={{ left: 554, width: 480 }} />
          </>)}
        </AbsoluteFill>
      )}

      <div style={{ position: "absolute", top: 70, right: 46, fontSize: 24, fontWeight: 700, color: C.red, background: "#fff", border: `3px solid ${C.red}`, borderRadius: 10, padding: "3px 10px" }}>禁止搬运</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1790, textAlign: "center", fontSize: 30, color: C.sub, opacity: 0.8 }}>活人图书馆 · {tr(lang, "Human Library", "Thư viện người sống")}</div>
      <div style={{ position: "absolute", left: wm[0], top: wm[1], fontSize: 26, fontWeight: 700, color: C.ink, opacity: 0.16 }}>瑾玄在练嘴</div>

      <Sequence from={Math.round(OUT0 * fps)}><Outro text="谢谢大家的观看～喜欢的话，记得点赞、关注我哦！" /></Sequence>
    </AbsoluteFill>
  );
};
