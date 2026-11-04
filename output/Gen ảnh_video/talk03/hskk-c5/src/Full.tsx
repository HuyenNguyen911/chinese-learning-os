import React from "react";
import { AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import data from "./data.json";
import timing from "./timing.json";
import intro from "./intro.json";
import outro from "./outro.json";
import lines from "./lines.json";
import frames from "./frames.json";
import { Outro, outroSec } from "./Outro";
import { C, FONT, SANS, SEC, PH, Title, Chrome, Peeker, Card, Tag, Branch, t as tr, Lang, Ph } from "./Frames";

/* VIDEO HOÀN CHỈNH HSKK 高级 · Chủ đề 3 (活人图书馆) · câu 5 · 回答问题 (9:16, 1080x1920).
   Cảnh: S1 câu hỏi -> S2 mindmap -> S3 cụm đáng học -> 现在开始 -> S4 clip minh hoạ + phụ đề kiểu phim (Hán trên, dịch dưới) -> kết follow.
   Nhạc nền chạy SUỐT video (nhỏ, tự hạ khi có giọng). Clip muse-video đã bỏ tiếng. */
export const FPS = 30;
const CH = (timing as { chars: number[] }).chars;
const ANS = (timing as { end: number }).end;                       // độ dài giọng đọc câu trả lời

// ---- phụ đề: 20 dòng, mốc theo giọng
type Ln = { zh: string; vi: string; en: string; t0: number; t1: number };
const TXT = data.text;
const LN: Ln[] = lines.idx.map((s, i) => {
  const e = i + 1 < lines.idx.length ? lines.idx[i + 1] : TXT.length;
  return { zh: TXT.slice(s, e), vi: lines.vi[i], en: lines.en[i], t0: CH[s], t1: i + 1 < lines.idx.length ? CH[lines.idx[i + 1]] : ANS };
});
// ---- clip minh hoạ theo dòng (số dòng 1-based)
// Bản 2 (user chốt 2026-11-03): bỏ K2 (tờ rơi), K4 (toàn cảnh phòng đọc), K12 (sách người khác) để dồn thời gian cho mạch chính;
// KHÔNG tua nhanh clip (tốc độ thật, chỉ cắt đoạn đầu). Bản 3: thang máy = K1a (chờ thang, chiếu lúc 现在开始, "dòng 0") + K1 (cửa mở, né không đi chung); cảnh kết KHÔNG lời sau khi đọc xong:
// K15a (đẩy xe hàng giúp bà cụ) + K15b (bưng giúp thùng hàng nặng). Dòng 21, 22 = "dòng ảo" sau câu cuối.
const VIRT = [0, 3.0, 7.5], HOLD = VIRT[2];   // mốc (giây sau khi đọc xong) của dòng ảo 21, 22, 23: K15a 3s, K15b 4,5s (đỡ thùng -> cảm ơn -> cùng đi vào tiệm)
const CLIPS = [[0, 0, "K1a"], [1, 2, "K1"], [3, 4, "K3"], [5, 6, "K5"], [7, 8, "K6"], [9, 10, "K7"], [11, 12, "K8"], [13, 13, "K9"], [14, 15, "K10"], [16, 17, "K11"], [18, 18, "K13"], [19, 20, "K14"], [21, 21, "K15a"], [22, 22, "K15b"]] as [number, number, string][];
const TAIL = new Set<string>();                                       // clip nào lấy phần CUỐI (không dùng ở video này)
const USE: Record<string, number> = { K11: 5.0 };  // chỉ dùng X giây đầu của clip (phải khớp USE trong make_frames.py); K11 clip trả ngắn hơn 10s
const lineT = (n: number) => (n === 0 ? -(intro.now + 0.7) : n <= LN.length ? LN[n - 1].t0 : ANS + VIRT[n - LN.length - 1]);   // mốc đầu dòng n (1-based); dòng 0 = lúc 现在开始, dòng ảo theo VIRT
const SEGS = CLIPS.map(([a, b, id]) => {
  const s = lineT(a), e = lineT(b + 1), dur = e - s;
  const rate = Math.min(1.0, Math.max(0.8, (USE[id] ?? 10) / dur));  // tốc độ thật (chỉ giãn nhẹ khi clip ngắn hơn đoạn đọc)
  const startSec = TAIL.has(id) ? Math.max(0, 10 - dur * rate - 0.2) : 0;
  return { id, s, e, dur, rate, startSec };
});
// hồi tưởng: K7-K10 phủ màu sepia + viền tối; loé trắng khi vào (đầu K7) và khi ra (đầu K11). K6 đẩy cận hình xăm trước khi vào hồi tưởng.
const FLASH = new Set(["K7", "K8", "K9", "K10"]);
const segOf = (id: string) => SEGS.find((g) => g.id === id)!;
// ---- dòng nào có cụm đáng học (số dòng 1-based)
const PHRASE_AT: Record<number, keyof typeof PH> = { 4: "jy", 6: "tiao", 12: "sq", 13: "zyys", 14: "zc", 20: "bq" };
const S3_LIST = ["jy", "tiao", "sq", "zyys", "zc", "bq"] as (keyof typeof PH)[];

// ---- lịch cảnh (giây, toàn video)
const Q0 = 0.7;
const S1_END = Q0 + intro.q + 1.0;
const S2_0 = S1_END, S2_END = S2_0 + 12.5;
const S3_0 = S2_END, S3_STEP = 3.0, S3_END = S3_0 + 1.0 + S3_LIST.length * S3_STEP + 0.8;
const S4_0 = S3_END, NOW0 = S4_0 + 0.3, A0 = NOW0 + intro.now + 0.7;
const ANS_END = A0 + ANS, OUT0 = ANS_END + HOLD;
export const TOTAL = Math.round((OUT0 + outroSec(outro.sec)) * FPS);

/* clip minh hoạ = chuỗi ảnh JPG đã cắt sẵn khớp lời đọc (make_frames.py) — không phát mp4 vì OffthreadVideo lỗi ngẫu nhiên trên máy này */
const FR = frames as Record<string, number>;
const SegFrames: React.FC<{ id: string; style: React.CSSProperties }> = ({ id, style }) => {
  const f = useCurrentFrame();
  const i = Math.max(0, Math.min(FR[id] - 1, f));
  return <Img src={staticFile(`frames/${id}/${String(i + 1).padStart(4, "0")}.jpg`)} style={style} />;
};
const ease = Easing.bezier(0.45, 0, 0.55, 1);
const WM = [[470, 1850], [780, 1850], [620, 1820], [300, 1850]];

const Sub: React.FC<{ ln: Ln; lang: Lang; dim?: boolean; hl?: string }> = ({ ln, lang, dim, hl }) => {
  const i = hl ? ln.zh.indexOf(hl) : -1;
  return (
    <div style={{ opacity: dim ? 0.4 : 1, textAlign: "center", whiteSpace: "nowrap" }}>
      <div style={{ fontSize: Math.min(dim ? 46 : 62, 980 / ln.zh.length), fontWeight: 700, color: C.ink, lineHeight: 1.3 }}>
        {i >= 0 ? <>{ln.zh.slice(0, i)}<span style={{ color: C.red, fontWeight: 800 }}>{hl}</span>{ln.zh.slice(i + hl!.length)}</> : ln.zh}
      </div>
      {/* dòng dịch tự thu chữ theo độ dài (≈0,52em/ký tự Latin) để luôn vừa 1 dòng trong khung 1000px — câu dài từng bị cắt mép */}
      <div style={{ fontSize: Math.min(dim ? 29 : 36, 1000 / (0.52 * (lang === "vi" ? ln.vi : ln.en).length)), color: C.green, marginTop: 8, fontFamily: SANS, lineHeight: 1.3 }}>{lang === "vi" ? ln.vi : ln.en}</div>
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
  const duck = Math.min(...voices.map(([s, e]) => interpolate(t, [s - 0.3, s, e, e + 0.5], [1, 0.3, 0.3, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));
  const bgVol = 0.22 * duck * Math.min(1, t / 1.5, (TOTAL / fps - t) / 2.0);

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
        <AbsoluteFill style={{ opacity: 1 - k(S1_END - 0.3, S1_END) }}>
          <Peeker x={820} y={600} w={210} />
          <Card style={{ left: 46, right: 46, top: 600, height: 640, display: "flex", flexDirection: "column", justifyContent: "center", padding: "0 56px" }}>
            <div style={{ fontSize: 64, fontWeight: 800, color: C.ink, lineHeight: 1.45, whiteSpace: "nowrap" }}>
              说说你对“<span style={{ color: C.red }}>活人图书馆</span>”<br />的看法。
            </div>
            <div style={{ fontSize: 38, color: C.green, marginTop: 34, fontFamily: SANS, lineHeight: 1.35 }}>
              {tr(lang, "What do you think of the \"Human Library\"?", "Bạn nghĩ gì về \"Thư viện người sống\"?")}
            </div>
          </Card>
        </AbsoluteFill>
      )}

      {/* S2: mindmap, các nhánh hiện lần lượt */}
      {inS2 && (
        <AbsoluteFill style={{ opacity: sceneFade(S2_0, S2_END) }}>
          <div style={{ position: "absolute", left: 170, width: 660, top: 200, height: 130, borderRadius: 26, background: "#E4ECFA", border: "5px solid #3A6EBE", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 58, fontWeight: 800, color: "#2B57A0" }}>活人图书馆？</div>
          <div style={{ position: "absolute", left: 100, top: 330, width: 0, height: 1330, borderLeft: `5px dashed ${C.line}` }} />
          {[
            { i: 0, y: 400, idea: "很有意义的活动", ex: "价值在于面对面交流" },
            { i: 1, y: 700, idea: "免费聊四十五分钟", ex: "“书”自愿分享经历和知识" },
            { i: 2, y: 1000, idea: "最有意思的一点", ex: "真诚对话，理解不一样的想法" },
            { i: 4, y: 1300, idea: "我很支持", ex: "不只凭标签评判一个人" },
          ].map((b, n) => {
            const a = S2_0 + 0.6 + n * 2.2;
            const sp = spring({ frame: f - Math.round(a * fps), fps, config: { damping: 14 } });
            return <div key={b.i} style={{ opacity: Math.min(1, sp), transform: `translateY(${(1 - Math.min(1, sp)) * 24}px)` }}><Branch i={b.i} y={b.y} idea={b.idea} ex={b.ex} /></div>;
          })}
          <div style={{ position: "absolute", right: 20, top: 1750 - 440, height: 440, width: (424 / 925) * 440, opacity: k(S2_0 + 0.3, S2_0 + 0.8) }}>
            <Img src={staticFile("img/yh_front.png")} style={{ width: "100%", height: "100%" }} />
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
            说说你对“活人图书馆”的看法。
          </div>
          <div style={{ position: "absolute", left: 46, right: 46, top: 430, height: 556, borderRadius: 36, overflow: "hidden", border: `4px solid ${C.green}`, background: "#E3F2E9" }}>
            {t < A0 && <Img src={staticFile("img/K1_key.png")} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover" }} />}
            {SEGS.map((sg, n) => {
              const from = A0 + sg.s - (n === 0 ? 0 : 0.3), to = n === SEGS.length - 1 ? OUT0 + 0.5 : A0 + sg.e + 0.3;
              if (t < from || t > to) return null;
              const op = n === 0 && t < A0 + sg.s + 0.3 ? 1 : interpolate(t, [from, from + 0.3, to - 0.3, to], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
              // K6: 1,4s cuối đẩy chậm vào hình xăm trên tay chàng trai (góc phải dưới) -> dẫn vào hồi tưởng
              const zoom = sg.id === "K6" ? interpolate(t, [A0 + sg.e - 1.4, A0 + sg.e], [1, 1.45], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease }) : 1;
              return (
                <Sequence key={sg.id} from={Math.round(from * fps)}>
                  <SegFrames id={sg.id} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", opacity: op,
                    filter: FLASH.has(sg.id) ? "sepia(0.55) saturate(0.85) contrast(0.95)" : undefined,
                    transform: zoom !== 1 ? `scale(${zoom})` : undefined, transformOrigin: "76% 70%" }} />
                </Sequence>
              );
            })}
            {/* hồi tưởng: viền tối mờ quanh khung + loé trắng lúc vào/ra */}
            {(() => {
              const f0 = A0 + segOf("K7").s, f1 = A0 + segOf("K11").s;
              const vig = interpolate(t, [f0 - 0.15, f0 + 0.2, f1 - 0.2, f1], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
              const flash = Math.max(...[f0, f1].map((x) => interpolate(t, [x - 0.18, x, x + 0.55], [0, 0.9, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));
              return (
                <>
                  {vig > 0 && <div style={{ position: "absolute", inset: 0, opacity: vig, background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(60,40,20,0.55) 100%)" }} />}
                  {flash > 0 && <div style={{ position: "absolute", inset: 0, background: "#fff", opacity: flash }} />}
                </>
              );
            })()}
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
      <div style={{ position: "absolute", left: 0, right: 0, top: 1790, textAlign: "center", fontSize: 30, color: C.sub, opacity: 0.8 }}>活人图书馆 · {tr(lang, "Human Library", "Thư viện người sống")}</div>
      <div style={{ position: "absolute", left: wm[0], top: wm[1], fontSize: 26, fontWeight: 700, color: C.ink, opacity: 0.16 }}>瑾玄在练嘴</div>

      <Sequence from={Math.round(OUT0 * fps)}><Outro text="谢谢大家的观看～喜欢的话，记得点赞、关注我哦！" /></Sequence>
    </AbsoluteFill>
  );
};
