import React from "react";
import { AbsoluteFill, Audio, Easing, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import data from "./data.json";
import timing from "./timing.json";
import intro from "./intro.json";
import outro from "./outro.json";
import lines from "./lines.json";
import { Outro, outroSec } from "./Outro";
import { C, FONT, SANS, SEC, PH, Title, Chrome, Peeker, Card, Tag, Branch, t as tr, Lang, Ph } from "./Frames";

/* VIDEO HOÀN CHỈNH HSKK 高级 · Chủ đề 1 · 回答问题 (9:16, 1080x1920).
   Cảnh: S1 câu hỏi -> S2 mindmap -> S3 cụm đáng học -> 现在开始 -> S4 clip minh hoạ + phụ đề kiểu phim (Hán trên, dịch dưới) -> kết follow.
   Nhạc nền chạy SUỐT video (nhỏ, tự hạ khi có giọng). Clip muse-video đã bỏ tiếng. */
export const FPS = 30;
const CH = (timing as { chars: number[] }).chars;
const ANS = (timing as { end: number }).end;                       // độ dài giọng đọc câu trả lời

// ---- phụ đề: 32 dòng, mốc theo giọng
type Ln = { zh: string; vi: string; en: string; t0: number; t1: number };
const TXT = data.text;
const LN: Ln[] = lines.idx.map((s, i) => {
  const e = i + 1 < lines.idx.length ? lines.idx[i + 1] : TXT.length;
  return { zh: TXT.slice(s, e), vi: lines.vi[i], en: lines.en[i], t0: CH[s], t1: i + 1 < lines.idx.length ? CH[lines.idx[i + 1]] : ANS };
});
// ---- clip minh hoạ theo dòng (số dòng 1-based)
const CLIPS = [[1, 3, "K1"], [4, 6, "K10"], [7, 8, "K2"], [9, 11, "K3"], [12, 13, "K11"], [14, 14, "K12"], [15, 16, "K4"], [17, 19, "K5"], [20, 20, "K6"], [21, 22, "K13"], [23, 24, "K7"], [25, 26, "K8"], [27, 30, "K14"], [31, 32, "K9"]] as [number, number, string][];
const TAIL = new Set(["K4"]);                                         // clip lấy phần CUỐI (nắm đấm mừng) cho khớp đoạn đọc
const SEGS = CLIPS.map(([a, b, id]) => {
  // clip cuối còn chạy tiếp tới OUT0+0.5 (= ANS+1.7) -> tính tốc độ trên ANS+2.5 để không đòi khung vượt quá 10s clip
  const s = LN[a - 1].t0, e = b < LN.length ? LN[b].t0 : ANS + 2.5, dur = e - s;
  const rate = Math.min(1.6, Math.max(0.8, 10 / dur));              // clip gốc 10s: nén/giãn cho vừa đoạn đọc
  const startSec = TAIL.has(id) ? Math.max(0, 10 - dur * rate - 0.2) : 0;
  return { id, s, e, dur, rate, startSec };
});
// ---- dòng nào có cụm đáng học (số dòng 1-based)
const PHRASE_AT: Record<number, keyof typeof PH> = { 10: "bzbj", 12: "cyd", 13: "dll", 20: "pbjd", 25: "znl", 32: "crj" };
const S3_LIST = ["cyd", "dll", "bzbj", "pbjd", "crj", "znl"] as (keyof typeof PH)[];

// ---- lịch cảnh (giây, toàn video)
const Q0 = 0.7;
const S1_END = Q0 + intro.q + 1.0;
const S2_0 = S1_END, S2_END = S2_0 + 12.5;
const S3_0 = S2_END, S3_STEP = 2.4, S3_END = S3_0 + 1.0 + S3_LIST.length * S3_STEP + 0.8;
const S4_0 = S3_END, NOW0 = S4_0 + 0.3, A0 = NOW0 + intro.now + 0.7;
const ANS_END = A0 + ANS, OUT0 = ANS_END + 1.2;
export const TOTAL = Math.round((OUT0 + outroSec(outro.sec)) * FPS);

const ease = Easing.bezier(0.45, 0, 0.55, 1);
const WM = [[470, 1850], [780, 1850], [620, 1820], [300, 1850]];

const Sub: React.FC<{ ln: Ln; lang: Lang; dim?: boolean; hl?: string }> = ({ ln, lang, dim, hl }) => {
  const i = hl ? ln.zh.indexOf(hl) : -1;
  return (
    <div style={{ opacity: dim ? 0.4 : 1, textAlign: "center", whiteSpace: "nowrap" }}>
      <div style={{ fontSize: dim ? 46 : 62, fontWeight: 700, color: C.ink, lineHeight: 1.3 }}>
        {i >= 0 ? <>{ln.zh.slice(0, i)}<span style={{ color: C.red, fontWeight: 800 }}>{hl}</span>{ln.zh.slice(i + hl!.length)}</> : ln.zh}
      </div>
      <div style={{ fontSize: dim ? 29 : 36, color: C.green, marginTop: 8, fontFamily: SANS, lineHeight: 1.3 }}>{lang === "vi" ? ln.vi : ln.en}</div>
    </div>
  );
};

export const Full: React.FC<{ lang: Lang }> = ({ lang }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const k = (a: number, b: number) => interpolate(t, [a, b], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const wm = WM[Math.floor(t / 6) % WM.length];
  const ta = t - A0;                                                // giờ theo giọng đọc câu trả lời
  const curI = ta >= 0 ? LN.findIndex((l) => ta >= l.t0 && ta < l.t1) : -1;
  const cur = curI >= 0 ? LN[curI] : null;
  const prev = curI > 0 ? LN[curI - 1] : null;
  const phKey = cur ? PHRASE_AT[curI + 1] : undefined;
  const ph: Ph | undefined = phKey ? PH[phKey] : undefined;
  const hl = ph ? ph.han.replace(/…/g, "").replace(/ \/ .*/, "") : undefined;

  // nhạc nền: hạ khi có giọng
  const voices: [number, number][] = [[Q0, Q0 + intro.q], [NOW0, NOW0 + intro.now], [A0, ANS_END], [OUT0 + 0.2, OUT0 + 0.2 + outro.sec],
    ...S3_LIST.map((_, i) => [S3_0 + 1.0 + i * S3_STEP, S3_0 + 1.0 + i * S3_STEP + 2.0] as [number, number])];
  const duck = Math.min(...voices.map(([s, e]) => interpolate(t, [s - 0.3, s, e, e + 0.5], [1, 0.42, 0.42, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));
  const bgVol = 0.07 * duck * Math.min(1, t / 1.5, (TOTAL / fps - t) / 2.0);

  const inS1 = t < S2_0, inS2 = t >= S2_0 && t < S3_0, inS3 = t >= S3_0 && t < S4_0, inS4 = t >= S4_0 && t < OUT0;
  const sceneFade = (a: number, b: number) => Math.min(k(a, a + 0.35), 1 - k(b - 0.35, b));

  return (
    <AbsoluteFill style={{ background: C.bg, fontFamily: FONT }}>
      <Audio src={staticFile("audio/bg.mp3")} loop volume={bgVol} />
      <Sequence from={Math.round(Q0 * fps)}><Audio src={staticFile("audio/intro_q.wav")} /></Sequence>
      <Sequence from={Math.round(NOW0 * fps)}><Audio src={staticFile("audio/intro_now.wav")} /></Sequence>
      <Sequence from={Math.round(A0 * fps)}><Audio src={staticFile("audio/read.wav")} /></Sequence>
      {S3_LIST.map((_, i) => <Sequence key={i} from={Math.round((S3_0 + 1.0 + i * S3_STEP) * fps)}><Audio src={staticFile(`audio/intro_p${i}.wav`)} /></Sequence>)}

      <Title />

      {/* S1: câu hỏi giữa khung */}
      {inS1 && (
        <AbsoluteFill style={{ opacity: Math.min(1, k(0, 0.4)) * (1 - k(S1_END - 0.3, S1_END)) }}>
          <Peeker x={820} y={600} w={210} />
          <Card style={{ left: 46, right: 46, top: 600, height: 640, display: "flex", flexDirection: "column", justifyContent: "center", padding: "0 56px" }}>
            <div style={{ fontSize: 64, fontWeight: 800, color: C.ink, lineHeight: 1.45, whiteSpace: "nowrap" }}>
              你同意<span style={{ color: C.red }}>“快乐也会传染”</span><br />这种说法吗？<br />请说说你的看法和理由。
            </div>
            <div style={{ fontSize: 38, color: C.green, marginTop: 34, fontFamily: SANS, lineHeight: 1.35 }}>
              {tr(lang, "Do you agree that “happiness is contagious”? Share your view and reasons.", "Bạn có đồng ý rằng “niềm vui cũng lây lan” không? Hãy nói quan điểm và lý do của bạn.")}
            </div>
          </Card>
        </AbsoluteFill>
      )}

      {/* S2: mindmap, các nhánh hiện lần lượt */}
      {inS2 && (
        <AbsoluteFill style={{ opacity: sceneFade(S2_0, S2_END) }}>
          <div style={{ position: "absolute", left: 170, width: 660, top: 200, height: 130, borderRadius: 26, background: "#E4ECFA", border: "5px solid #3A6EBE", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 58, fontWeight: 800, color: "#2B57A0" }}>快乐会传染？</div>
          <div style={{ position: "absolute", left: 100, top: 330, width: 0, height: 1130, borderLeft: `5px dashed ${C.line}` }} />
          {[
            { i: 0, y: 400, idea: "快乐确实会传染", ex: "一家人团聚的情景" },
            { i: 1, y: 700, idea: "身边人快乐，你也快乐", ex: "例：回到家，看到家人笑，你也跟着笑" },
            { i: 2, y: 1040, idea: "独乐乐不如众乐乐", ex: "例：考过HSK六级，告诉家人朋友，一起庆祝" },
            { i: 3, y: 1380, idea: "快乐是正能量", ex: "做快乐的“传染源”" },
          ].map((b, n) => {
            const a = S2_0 + 0.6 + n * 2.6;
            const sp = spring({ frame: f - Math.round(a * fps), fps, config: { damping: 14 } });
            return <div key={b.i} style={{ opacity: Math.min(1, sp), transform: `translateY(${(1 - Math.min(1, sp)) * 24}px)` }}><Branch i={b.i} y={b.y} idea={b.idea} ex={b.ex} /></div>;
          })}
          <div style={{ position: "absolute", right: 20, top: 1750 - 440, height: 440, width: (520 / 917) * 440, opacity: k(S2_0 + 0.3, S2_0 + 0.8) }}>
            <Img src={staticFile("img/yh_w_wave.png")} style={{ width: "100%", height: "100%" }} />
          </div>
        </AbsoluteFill>
      )}

      {/* S3: cụm đáng học, từng thẻ + đọc */}
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
                <Card style={{ left: 46, right: 46, top: 230 + i * 230, height: 200, display: "flex", alignItems: "center", gap: 30, padding: "0 40px", borderRadius: 28, borderColor: on ? C.red : "#E9B7B0" }}>
                  <div style={{ fontSize: p.han.length > 6 ? 54 : 70, fontWeight: 800, color: C.red, lineHeight: 1.15, width: 470, flexShrink: 0, whiteSpace: "nowrap" }}>{p.han}</div>
                  <div style={{ display: "flex", flexDirection: "column", lineHeight: 1.25 }}>
                    {p.py && <div style={{ fontSize: 28, color: C.sub }}>{p.py}</div>}
                    <div style={{ fontSize: 34, color: C.green, fontFamily: SANS, marginTop: 4 }}>{lang === "vi" ? p.vi : p.en}</div>
                  </div>
                </Card>
              </div>
            );
          })}
        </AbsoluteFill>
      )}

      {/* S4: câu hỏi + khung video + phụ đề kiểu phim */}
      {inS4 && (
        <AbsoluteFill style={{ opacity: k(S4_0, S4_0 + 0.4) }}>
          <div style={{ position: "absolute", left: 0, right: 0, top: 170, fontSize: 46, fontWeight: 800, color: C.ink, textAlign: "center", lineHeight: 1.35, whiteSpace: "nowrap" }}>
            你同意“快乐也会传染”这种说法吗？<br />请说说你的看法和理由。
          </div>
          <Peeker x={880} y={430} w={170} />
          <div style={{ position: "absolute", left: 46, right: 46, top: 430, height: 556, borderRadius: 36, overflow: "hidden", border: `4px solid ${C.green}`, background: "#E3F2E9" }}>
            {t < A0 && <Img src={staticFile("img/K1_key.png")} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover" }} />}
            {SEGS.map((sg, n) => {
              const from = A0 + sg.s - (n === 0 ? 0 : 0.3), to = n === SEGS.length - 1 ? OUT0 + 0.5 : A0 + sg.e + 0.3;
              if (t < from || t > to) return null;
              const op = n === 0 && t < A0 + sg.s + 0.3 ? 1 : interpolate(t, [from, from + 0.3, to - 0.3, to], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
              return (
                <Sequence key={sg.id} from={Math.round(from * fps)}>
                  <OffthreadVideo src={staticFile(`motion/${sg.id}.mp4`)} muted playbackRate={sg.rate} startFrom={Math.round(sg.startSec * fps)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", opacity: n === SEGS.length - 1 ? op : op }} />
                </Sequence>
              );
            })}
            {t < A0 && (
              <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
                <div style={{ fontSize: 120, fontWeight: 800, color: "#fff", WebkitTextStroke: `10px ${C.green}`, paintOrder: "stroke fill", transform: `scale(${0.8 + 0.2 * k(NOW0, NOW0 + 0.3)})`, opacity: k(NOW0, NOW0 + 0.3) }}>现在开始！</div>
              </div>
            )}
          </div>
          {cur && (
            <div style={{ position: "absolute", left: 0, right: 0, top: 1060, display: "flex", flexDirection: "column", gap: 44 }}>
              {prev && <Sub ln={prev} lang={lang} dim />}
              <Sub ln={cur} lang={lang} hl={hl} />
            </div>
          )}
          {ph && cur && (
            <Card style={{ left: 240, right: 240, top: 1470, height: 210, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", textAlign: "center", borderRadius: 26 }}>
              <Tag>重点词</Tag>
              <div style={{ fontSize: ph.han.length > 6 ? 46 : 62, fontWeight: 800, color: C.red, lineHeight: 1.15, whiteSpace: "nowrap" }}>{ph.han}</div>
              <div style={{ fontSize: 26, color: C.sub, marginTop: 2 }}>{ph.py ? ph.py + " · " : ""}<span style={{ color: C.green, fontFamily: SANS }}>{lang === "vi" ? ph.vi : ph.en}</span></div>
            </Card>
          )}
        </AbsoluteFill>
      )}

      {/* chống copy + tên chủ đề */}
      <div style={{ position: "absolute", top: 70, right: 46, fontSize: 24, fontWeight: 700, color: C.red, background: "#fff", border: `3px solid ${C.red}`, borderRadius: 10, padding: "3px 10px" }}>禁止搬运</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1790, textAlign: "center", fontSize: 30, color: C.sub, opacity: 0.8 }}>快乐会传染 · {tr(lang, "Happiness is contagious", "Niềm vui lây lan")}</div>
      <div style={{ position: "absolute", left: wm[0], top: wm[1], fontSize: 26, fontWeight: 700, color: C.ink, opacity: 0.16 }}>瑾玄在练嘴</div>

      <Sequence from={Math.round(OUT0 * fps)}><Outro text="谢谢大家的观看～喜欢的话，记得点赞、关注我哦！" /></Sequence>
    </AbsoluteFill>
  );
};
