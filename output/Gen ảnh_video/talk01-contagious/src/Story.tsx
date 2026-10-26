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

type Actor = { img: string; x: number; feet: number; h: number; flip?: boolean; from?: number; swap?: { img: string; at: number }; bob?: "voice" | "laugh" | "none"; z?: number };
type Scene = {
  id: string; text: string; actors: Actor[];
  bubble?: { text: string; at: number; x: number; y: number };
  glow?: { x: number; y: number; at: number }[];
  cards?: { han: string; py: string; vi: string; at: number }[];
};
const scenes = story.scenes as Scene[];
const dur = durations as Record<string, number>;
const env = envelope as Record<string, number[]>;
const sz = sizes as Record<string, number[]>;
const sceneFrames = (s: Scene) => Math.round((dur[s.id] ? dur[s.id] + 0.5 : story.defaultSec) * FPS);
export const TOTAL = scenes.reduce((n, s) => n + sceneFrames(s), 0);

const ease = Easing.bezier(0.45, 0, 0.55, 1);
const FONT = '"Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif';

const Room: React.FC = () => (
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
      {/* thảm */}
      <ellipse cx={540} cy={1640} rx={470} ry={110} fill="#F2D9C4" opacity={0.85} />
    </svg>
  </AbsoluteFill>
);

const ActorView: React.FC<{ a: Actor; sceneId: string; f: number; n: number }> = ({ a, sceneId, f, n }) => {
  const p = f / n;
  const img = a.swap && p >= a.swap.at ? a.swap.img : a.img;
  const [iw, ih] = sz[img] ?? sz[a.img];
  const h = a.h, w = (h * iw) / ih;
  let x = a.x;
  if (a.from !== undefined) x = interpolate(f, [0, 0.55 * FPS], [a.from, a.x], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const e = env[sceneId]?.[f] ?? 0;
  let dy = 0, sy = 1, rot = 0;
  if (a.bob === "voice") { dy = -e * 16; sy = 1 + e * 0.035; }
  if (a.bob === "laugh") { dy = -Math.abs(Math.sin(f / 3.2)) * 18; rot = Math.sin(f / 3.2) * 1.2; }
  const cross = a.swap ? interpolate(p, [a.swap.at - 0.05, a.swap.at + 0.05], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const base: React.CSSProperties = { position: "absolute", left: x - w / 2, top: a.feet - h, width: w, height: h, transformOrigin: "50% 100%", transform: `translateY(${dy}px) scaleY(${sy}) rotate(${rot}deg) ${a.flip ? "scaleX(-1)" : ""}` };
  const shadow = <div style={{ position: "absolute", left: x - w * 0.42, top: a.feet - 22, width: w * 0.84, height: 44, borderRadius: "50%", background: "rgba(90,60,30,0.18)", filter: "blur(6px)" }} />;
  if (!a.swap) return <>{shadow}<Img src={staticFile(`img/${img}.png`)} style={base} /></>;
  return (
    <>{shadow}
      <Img src={staticFile(`img/${a.img}.png`)} style={{ ...base, opacity: 1 - cross }} />
      <Img src={staticFile(`img/${a.swap.img}.png`)} style={{ ...base, opacity: cross, width: (h * sz[a.swap.img][0]) / sz[a.swap.img][1], left: x - (h * sz[a.swap.img][0]) / sz[a.swap.img][1] / 2 }} />
    </>
  );
};

const SceneView: React.FC<{ s: Scene; n: number }> = ({ s, n }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = f / n;
  const fadeIn = interpolate(f, [0, 6], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: fadeIn }}>
      <Room />
      {s.glow?.map((g, i) => {
        const t = (p - g.at) / 0.22;
        if (t < 0 || t > 1) return null;
        const r = 60 + t * 190;
        return <div key={i} style={{ position: "absolute", left: g.x - r, top: g.y - r, width: r * 2, height: r * 2, borderRadius: "50%", border: "10px solid rgba(255,196,64,0.9)", opacity: 1 - t, boxShadow: "0 0 40px rgba(255,196,64,0.7)" }} />;
      })}
      {[...s.actors].sort((a, b) => (a.z ?? 0) - (b.z ?? 0)).map((a, i) => <ActorView key={i} a={a} sceneId={s.id} f={f} n={n} />)}
      {s.bubble && p >= s.bubble.at && (() => {
        const k = spring({ frame: f - s.bubble.at * n, fps, config: { damping: 12 } });
        return (
          <div style={{ position: "absolute", left: s.bubble.x - 70, top: s.bubble.y - 70, width: 140, height: 140, borderRadius: "50%", background: "#fff", border: "8px solid #23201c", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 96, fontWeight: 800, fontFamily: FONT, color: "#C4492D", transform: `scale(${k})` }}>{s.bubble.text}</div>
        );
      })()}
      {s.cards?.map((c, i) => {
        const k = interpolate(p, [c.at, c.at + 0.08], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
        return (
          <div key={i} style={{ position: "absolute", left: 90, right: 90, top: 150 + i * 280, opacity: k, transform: `translateY(${(1 - k) * 30}px)`, background: "rgba(255,255,255,0.94)", borderRadius: 36, padding: "26px 40px", textAlign: "center", boxShadow: "0 10px 30px rgba(60,40,20,0.18)", fontFamily: FONT }}>
            <div style={{ fontSize: 112, fontWeight: 800, color: "#C4492D", lineHeight: 1.1 }}>{c.han}</div>
            <div style={{ fontSize: 40, color: "#5b5248", marginTop: 4 }}>{c.py}</div>
            <div style={{ fontSize: 38, color: "#2F6F6A", marginTop: 4, fontFamily: '"Segoe UI",sans-serif' }}>{c.vi}</div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 70, right: 70, bottom: 130, textAlign: "center", fontFamily: FONT, fontWeight: 800, fontSize: s.text.length > 24 ? 54 : 66, lineHeight: 1.3, color: "#fff", WebkitTextStroke: "14px #3a2a1c", paintOrder: "stroke fill" as any }}>{s.text}</div>
    </AbsoluteFill>
  );
};

export const Story: React.FC = () => {
  let start = 0;
  return (
    <AbsoluteFill style={{ background: "#FBF3E6" }}>
      {scenes.map((s) => {
        const n = sceneFrames(s), from = start; start += n;
        return (
          <Sequence key={s.id} from={from} durationInFrames={n}>
            <SceneView s={s} n={n} />
            {dur[s.id] ? <Audio src={staticFile(`audio/${s.id}.wav`)} /> : null}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
