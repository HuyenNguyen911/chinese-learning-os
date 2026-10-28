import React from "react";
import { AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import story from "./story.json";
import durations from "./durations.json";
import envelope from "./envelope.json";
import sizes from "./sizes.json";

/* Clip kể chuyện 9:16: mỗi cảnh = 1 câu thoại. Độ dài cảnh = độ dài file giọng (durations.json, giây),
   chưa có giọng thì dùng story.defaultSec. Mọi mốc thời gian `at` là TỈ LỆ (0-1) của cảnh. */
export const FPS = 30;
const W = 1080, H = 1920;

type Actor = { img: string; x: number; feet: number; h: number; flip?: boolean; from?: number; fromSec?: number; walk?: boolean; still?: boolean; chat?: boolean; mime?: boolean; neutral?: boolean; lean?: number; enter?: { x: number; feet: number; h: number; sec: number }; talk?: boolean; swap?: { img: string; at: number }; bob?: "voice" | "laugh" | "none"; z?: number };
type Scene = {
  id: string; voice?: string; silent?: boolean; sec?: number; door?: boolean; text: string; actors: Actor[];
  bubble?: { text: string; at: number; x: number; y: number };
  glow?: { x: number; y: number; at: number }[];
  cards?: { han: string; py: string; en: string; at: number }[];
};
const scenes = story.scenes as Scene[];
const dur = durations as Record<string, number>;
const env = envelope as Record<string, number[]>;
const sz = sizes as Record<string, number[]>;
/* Một câu thoại (voice) có thể chia thành nhiều cảnh/đoạn phụ đề: thời lượng chia theo số chữ Hán.
   Chưa có giọng thì mỗi chữ ~0.24s (mốc nhép miệng theo chữ). */
const SEC_PER_CHAR = 0.24;
const hanCount = (t: string) => (t.match(/[一-鿿]/g) ?? []).length;
const voiceOf = (s: Scene) => s.voice ?? s.id;
type Layout = { s: Scene; start: number; n: number; voice: string; offset: number; chars: number };
const layout: Layout[] = [];
let cursor = 0;
for (const s of scenes) {
  const voice = voiceOf(s);
  const group = scenes.filter((x) => voiceOf(x) === voice);
  const gChars = group.reduce((n, x) => n + hanCount(x.text), 0);
  const chars = hanCount(s.text);
  const idx = group.indexOf(s);
  let n: number, offset = 0;
  if (s.sec) {
    n = Math.round(s.sec * FPS);
  } else if (dur[voice]) {
    const total = Math.round((dur[voice] + 0.5) * FPS);
    const cut = (k: number) => Math.round((total * group.slice(0, k).reduce((m, x) => m + hanCount(x.text), 0)) / gChars);
    offset = cut(idx);
    n = (idx === group.length - 1 ? total : cut(idx + 1)) - offset;
  } else {
    n = Math.round(Math.max(1.5, chars * SEC_PER_CHAR + 0.5) * FPS);
  }
  layout.push({ s, start: cursor, n, voice, offset, chars });
  cursor += n;
}
export const TOTAL = cursor;

const ease = Easing.bezier(0.45, 0, 0.55, 1);
const FONT = '"Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif';

const Room: React.FC<{ door?: boolean }> = ({ door }) => (
  <AbsoluteFill>
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <defs>
        <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#FBF3E6" /><stop offset="1" stopColor="#F3E4CF" /></linearGradient>
        <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#E3C29B" /><stop offset="1" stopColor="#D2AB80" /></linearGradient>
      </defs>
      <rect width={W} height={1380} fill="url(#wall)" />
      <rect y={1380} width={W} height={H - 1380} fill="url(#floor)" />
      <rect y={1368} width={W} height={20} fill="#F8EEDD" />
      {/* cửa sổ */}
      <rect x={90} y={300} width={330} height={440} rx={14} fill="#CFE6F2" stroke="#fff" strokeWidth={14} />
      <line x1={255} y1={300} x2={255} y2={740} stroke="#fff" strokeWidth={10} />
      <line x1={90} y1={520} x2={420} y2={520} stroke="#fff" strokeWidth={10} />
      {/* khung tranh */}
      <rect x={700} y={360} width={250} height={190} rx={8} fill="#FFFFFF" stroke="#C9A77C" strokeWidth={12} />
      <circle cx={790} cy={440} r={34} fill="#F6C9A5" /><path d="M715 530 L800 470 L860 520 L925 460 L935 535 Z" fill="#9FCBB3" />
      {door && (<>
        <rect x={930} y={640} width={190} height={740} fill="#FFF6D8" />
        <rect x={930} y={640} width={190} height={740} fill="none" stroke="#B98F63" strokeWidth={18} />
      </>)}
      {/* thảm */}
      <ellipse cx={540} cy={1640} rx={470} ry={110} fill="#F2D9C4" opacity={0.85} />
    </svg>
  </AbsoluteFill>
);

/* Khuôn mặt sống: miệng nhép + chớp mắt. Vẽ lại đúng vùng đó của ảnh gốc (cắt elip, nền = màu da) rồi co/giãn theo
   chiều dọc. Toạ độ theo tỉ lệ ảnh (cx,cy = tâm; rx,ry = nửa trục elip). */
type Part = { cx: number; cy: number; rx: number; ry: number; skin?: string };
const FACE: Record<string, { skin: string; mouth?: Part; eyes?: Part[]; chat?: Part[] }> = {
  jx3_smile: {
    skin: "#FDD1BD",
    mouth: { cx: 180 / 364, cy: 284 / 845, rx: 33 / 364, ry: 19 / 845, skin: "#FED8C1" },
    eyes: [{ cx: 120 / 364, cy: 226 / 845, rx: 26 / 364, ry: 26 / 845 }, { cx: 244 / 364, cy: 226 / 845, rx: 26 / 364, ry: 26 / 845 }],
  },
  jx3_confused_b: {
    skin: "#F3C7B5",
    mouth: { cx: 221 / 447, cy: 330 / 853, rx: 17 / 447, ry: 15 / 853, skin: "#FED8C5" },
    eyes: [{ cx: 143 / 447, cy: 263 / 853, rx: 36 / 447, ry: 34 / 853 }, { cx: 295 / 447, cy: 263 / 853, rx: 36 / 447, ry: 34 / 853 }],
  },
};
FACE.parents_sofa_laugh_v2 = { // mẹ (trái), bố (phải): miệng nói/cười xen kẽ, ghế đứng yên. Màu da lấy mẫu từ ảnh gốc
  skin: "#FDD9C3",
  chat: [
    { cx: 296 / 904, cy: 271 / 699, rx: 34 / 904, ry: 20 / 699, skin: "#FDD9C3" },
    { cx: 634 / 904, cy: 253 / 699, rx: 38 / 904, ry: 24 / 699, skin: "#FBD3B0" },
  ],
};
const PAD = 1.3; // elip nền da phủ rộng hơn bộ phận gốc

const ActorView: React.FC<{ a: Actor; sceneId: string; f: number; n: number; e: number; mouth: number }> = ({ a, sceneId, f, n, e, mouth }) => {
  const p = f / n;
  const img = a.swap && p >= a.swap.at ? a.swap.img : a.img;
  const [iw, ih] = sz[img] ?? sz[a.img];
  const en = a.enter ? interpolate(f, [0, a.enter.sec * FPS], [0, 1], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) }) : 1;
  const lerp = (from: number, to: number) => from + (to - from) * en;
  const h = a.enter ? lerp(a.enter.h, a.h) : a.h, w = (h * iw) / ih;
  const feet = a.enter ? lerp(a.enter.feet, a.feet) : a.feet;
  let x = a.enter ? lerp(a.enter.x, a.x) : a.x;
  if (a.from !== undefined) x = interpolate(f, [0, (a.fromSec ?? 0.55) * FPS], [a.from, a.x], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const ph = a.x * 0.013; // lệch pha để các nhân vật không cử động đồng loạt
  let dy = 0, sy = 1, rot = 0;
  if (a.bob === "voice") { dy = -e * 16; sy = 1 + e * 0.035; }
  if (a.lean) rot += a.lean * Math.min(1, f / (0.5 * FPS)); // nghiêng người về phía người đối diện
  if (a.bob !== "laugh" && !a.still) { sy *= 1 + 0.011 * Math.sin(f / 12 + ph); rot += 0.8 * Math.sin(f / 27 + ph); } // thở + dồn trọng tâm
  if (a.walk && a.from !== undefined && f < (a.fromSec ?? 0.55) * FPS) { dy = -Math.abs(Math.sin(f / 4)) * 16; rot += Math.sin(f / 4) * 2; }
  if (a.bob === "laugh") { dy = -Math.abs(Math.sin(f / 3.2)) * 18; rot = Math.sin(f / 3.2) * 1.2; }
  const cross = a.swap ? interpolate(p, [a.swap.at - 0.05, a.swap.at + 0.05], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const base: React.CSSProperties = { position: "absolute", left: x - w / 2, top: feet - h, width: w, height: h, transformOrigin: "50% 100%", transform: `translateY(${dy}px) scaleY(${sy}) rotate(${rot}deg) ${a.flip ? "scaleX(-1)" : ""}` };
  const shadow = <div style={{ position: "absolute", left: x - w * 0.42, top: feet - 22, width: w * 0.84, height: 44, borderRadius: "50%", background: "rgba(90,60,30,0.18)", filter: "blur(6px)" }} />;

  const face = FACE[img];
  const t = (f + Math.round(ph * 40)) % 100;
  const blink = t < 6 ? 1 - Math.sin((Math.PI * t) / 6) * 0.88 : 1; // 1 = mở mắt, ~0.12 = nhắm
  const el = (q: Part, k: number) => `ellipse(${q.rx * k * 100}% ${q.ry * k * 100}% at ${q.cx * 100}% ${q.cy * 100}%)`;
  const patch = (q: Part, sx: number, sy2: number, key: string) => (
    <div key={key} style={{ ...base, clipPath: el(q, PAD), background: q.skin ?? face.skin }}>
      <div style={{ position: "absolute", inset: 0, clipPath: el(q, 1), transformOrigin: `${q.cx * 100}% ${q.cy * 100}%`, transform: `scale(${sx}, ${sy2})` }}>
        <Img src={staticFile(`img/${img}.png`)} style={{ width: "100%", height: "100%" }} />
      </div>
    </div>
  );
  const faceLayers = face && (
    <>
      {face.eyes && blink < 1 && face.eyes.map((q, i) => patch(q, 1, blink, `e${i}`))}
      {a.talk && face.mouth && patch(face.mouth, 1 + mouth * 0.08, 0.35 + mouth * 0.85, "m")}
      {a.mime && face.mouth && (() => { // nhép miệng không thoại: nói theo từng đợt
        const turn = Math.max(0, Math.sin((f / FPS) * 1.6 + 1.3 * Math.PI));
        const o = turn * Math.abs(Math.sin(f / 2.4 + 0.9));
        return patch(face.mouth, 1 + o * 0.08, 0.4 + o * 0.8, "mm");
      })()}
      {a.neutral && face.mouth && ( // chưa cười: che miệng cười, vẽ miệng khép
        <div style={{ ...base, clipPath: el(face.mouth, PAD), background: face.mouth.skin ?? face.skin }}>
          <svg viewBox={`0 0 ${iw} ${ih}`} style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}>
            <path d={`M ${face.mouth.cx * iw - 10} ${face.mouth.cy * ih + 1} Q ${face.mouth.cx * iw} ${face.mouth.cy * ih + 5} ${face.mouth.cx * iw + 10} ${face.mouth.cy * ih + 1}`} stroke="#A85A4A" strokeWidth={2.6} fill="none" strokeLinecap="round" />
          </svg>
        </div>
      )}
      {a.chat && face.chat?.map((q, i) => { // nói xen kẽ: mỗi người nói ~1s rồi nghỉ, miệng mở theo nhịp âm tiết
        const turn = Math.max(0, Math.sin((f / FPS) * 1.9 + i * Math.PI));
        const o = turn * Math.abs(Math.sin(f / 2.6 + i * 1.7));
        return patch(q, 1 + o * 0.08, 0.5 + o * 0.7, `c${i}`);
      })}
    </>
  );
  if (!a.swap) return <>{shadow}<Img src={staticFile(`img/${img}.png`)} style={base} />{faceLayers}</>;
  return (
    <>{shadow}
      <Img src={staticFile(`img/${a.img}.png`)} style={{ ...base, opacity: 1 - cross }} />
      <Img src={staticFile(`img/${a.swap.img}.png`)} style={{ ...base, opacity: cross, width: (h * sz[a.swap.img][0]) / sz[a.swap.img][1], left: x - (h * sz[a.swap.img][0]) / sz[a.swap.img][1] / 2 }} />
    </>
  );
};

const SceneView: React.FC<{ L: Layout }> = ({ L }) => {
  const { s, n, voice, offset, chars } = L;
  const f = useCurrentFrame();
  const e = env[voice]?.[offset + f] ?? 0;
  // có giọng -> miệng theo âm lượng; chưa có -> mở/ngậm theo từng chữ trên màn hình
  const syl = SEC_PER_CHAR * FPS;
  const mouth = dur[voice] ? Math.min(1, e * 1.3) : f < chars * syl ? Math.pow(Math.abs(Math.sin((Math.PI * f) / syl)), 0.7) : 0;
  const { fps } = useVideoConfig();
  const p = f / n;
  const fadeIn = interpolate(f, [0, 6], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: fadeIn }}>
      <Room door={s.door} />
      {s.glow?.map((g, i) => {
        const t = (p - g.at) / 0.22;
        if (t < 0 || t > 1) return null;
        const r = 60 + t * 190;
        return <div key={i} style={{ position: "absolute", left: g.x - r, top: g.y - r, width: r * 2, height: r * 2, borderRadius: "50%", border: "10px solid rgba(255,196,64,0.9)", opacity: 1 - t, boxShadow: "0 0 40px rgba(255,196,64,0.7)" }} />;
      })}
      {[...s.actors].sort((a, b) => (a.z ?? 0) - (b.z ?? 0)).map((a, i) => <ActorView key={i} a={a} sceneId={s.id} f={f} n={n} e={e} mouth={mouth} />)}
      {s.bubble && p >= s.bubble.at && (() => {
        const k = spring({ frame: f - s.bubble.at * n, fps, config: { damping: 12 } });
        return (
          <div style={{ position: "absolute", left: s.bubble.x - 70, top: s.bubble.y - 70, width: 140, height: 140, borderRadius: "50%", background: "#fff", border: "8px solid #23201c", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 96, fontWeight: 800, fontFamily: FONT, color: "#C4492D", transform: `scale(${k})` }}>{s.bubble.text}</div>
        );
      })()}
      {s.cards?.map((c, i) => {
        const k = interpolate(p, [c.at, c.at + 0.08], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
        return (
          <div key={i} style={{ position: "absolute", left: 90, right: 90, top: 360 + i * 280, opacity: k, transform: `translateY(${(1 - k) * 30}px)`, background: "rgba(255,255,255,0.94)", borderRadius: 36, padding: "26px 40px", textAlign: "center", boxShadow: "0 10px 30px rgba(60,40,20,0.18)", fontFamily: FONT }}>
            <div style={{ fontSize: 112, fontWeight: 800, color: "#C4492D", lineHeight: 1.1 }}>{c.han}</div>
            <div style={{ fontSize: 40, color: "#5b5248", marginTop: 4 }}>{c.py}</div>
            <div style={{ fontSize: 38, color: "#2F6F6A", marginTop: 4, fontFamily: '"Segoe UI",sans-serif' }}>{c.en}</div>
          </div>
        );
      })}
{s.text && (      <div style={{ position: "absolute", left: 70, right: 70, top: 200, textAlign: "center", fontFamily: FONT, fontWeight: 800, fontSize: s.text.length > 14 ? 50 : 66, lineHeight: 1.3, color: "#fff", WebkitTextStroke: "14px #3a2a1c", paintOrder: "stroke fill" as any }}>{s.text}</div>)}
    </AbsoluteFill>
  );
};

export const Story: React.FC = () => {
  const voices = [...new Set(layout.map((L) => L.voice))];
  return (
    <AbsoluteFill style={{ background: "#FBF3E6" }}>
      {layout.map((L) => (
        <Sequence key={L.s.id} from={L.start} durationInFrames={L.n}>
          <SceneView L={L} />
        </Sequence>
      ))}
      <Audio src={staticFile("audio/bed.wav")} />
      {voices.filter((v) => dur[v]).map((v) => {
        const g = layout.filter((L) => L.voice === v);
        return (
          <Sequence key={v} from={g[0].start} durationInFrames={g.reduce((m, L) => m + L.n, 0)}>
            <Audio src={staticFile(`audio/${v}.wav`)} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
