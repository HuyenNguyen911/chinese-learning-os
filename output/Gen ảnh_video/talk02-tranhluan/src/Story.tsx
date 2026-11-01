import React from "react";
import { AbsoluteFill, Audio, Easing, Img, OffthreadVideo, Sequence, getInputProps, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import story from "./story.json";
import durations from "./durations.json";
import envelope from "./envelope.json";
import sizes from "./sizes.json";
import outro from "./outro.json";
import { Outro, outroSec } from "./Outro";

/* Clip kể chuyện 9:16: mỗi cảnh = 1 câu thoại. Độ dài cảnh = độ dài file giọng (durations.json, giây),
   chưa có giọng thì dùng story.defaultSec. Mọi mốc thời gian `at` là TỈ LỆ (0-1) của cảnh. */
export const FPS = 30;
// --props='{"clean":true}': ẩn chữ/logo/đồng hồ/nhãn/nút/tia lửa -> khung tĩnh làm ảnh mẫu cho muse-video (chữ trong ảnh bị AI làm méo)
const CLEAN = !!(getInputProps() as { clean?: boolean }).clean;
const W = 1080, H = 1920;

type Actor = { img: string; x: number; feet: number; h: number; flip?: boolean; from?: number; fromSec?: number; walk?: boolean; still?: boolean; chat?: boolean; mime?: boolean; neutral?: boolean; lean?: number; enter?: { x: number; feet: number; h: number; sec: number }; talk?: boolean; swap?: { img: string; at: number }; bob?: "voice" | "laugh" | "none"; z?: number };
type Scene = {
  id: string; voice?: string; silent?: boolean; sec?: number; door?: boolean; text: string; actors: Actor[];
  video?: string; vstart?: number; // đoạn cử động thật public/motion/<video>.mp4 (muse-video) thay nền + nhân vật tĩnh
  bg?: "home" | "school" | "versus" | "road" | "floor" | "duo"; split?: boolean; clock?: string; labels?: string[]; spark?: boolean; vote?: boolean; who?: "jx" | "yh" | "both";
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
type Layout = { s: Scene; start: number; n: number; voice: string; offset: number; chars: number; vfrom: number; cont: boolean };
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
  // các cảnh liền nhau dùng chung 1 video: phát tiếp từ chỗ cảnh trước dừng (vstart = giây bắt đầu cắt của cảnh đầu)
  const prev = layout[layout.length - 1];
  const cont = !!s.video && prev?.s.video === s.video;
  const vfrom = !s.video ? 0 : cont ? prev.vfrom + prev.n : Math.round((s.vstart ?? 0) * FPS);
  layout.push({ s, start: cursor, n, voice, offset, chars, vfrom, cont });
  cursor += n;
}
/* Lớp video: các cảnh liền nhau cùng 1 video = 1 trình phát chạy liền (không tạo lại mỗi cảnh -> hết giật).
   Đoạn sau mờ dần lên TRÊN đoạn trước trong XF khung, đoạn trước vẫn phát tiếp bên dưới -> không lộ nền (hết "nháy"). */
const XF = 10;
type VG = { video: string; start: number; n: number; vfrom: number };
const vgroups: VG[] = [];
for (const L of layout) {
  if (!L.s.video) continue;
  const g = vgroups[vgroups.length - 1];
  if (L.cont && g) g.n += L.n; else vgroups.push({ video: L.s.video, start: L.start, n: L.n, vfrom: L.vfrom });
}
const OUTRO_START = cursor + Math.round(0.4 * FPS);                 // hết cảnh cuối nghỉ 0.4s rồi vào đoạn kết (Outro.tsx)
export const TOTAL = OUTRO_START + Math.round(outroSec(outro.sec) * FPS);
const WM_SPOTS: [number, number][] = [[60, 1855], [360, 1855], [640, 1770]];   // dấu chìm nhỏ đổi chỗ mỗi 6s

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

/* Nền lớp học: tường xanh nhạt + bảng đen trơn (không chữ) + sàn gỗ */
const School: React.FC = () => (
  <AbsoluteFill>
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <rect width={W} height={1380} fill="#E6F1EC" />
      <rect y={1380} width={W} height={H - 1380} fill="#D9B98F" />
      <rect y={1368} width={W} height={20} fill="#F4F8F5" />
      <rect x={120} y={560} width={840} height={420} rx={16} fill="#3F6B57" stroke="#B98F63" strokeWidth={20} />
      <rect x={300} y={985} width={480} height={18} rx={6} fill="#B98F63" />
      <rect x={340} y={975} width={60} height={14} rx={4} fill="#FFFFFF" />
    </svg>
  </AbsoluteFill>
);

/* Đường tới trường: trời xanh, cỏ, con đường, xa xa toà nhà trường (không chữ) */
const Road: React.FC = () => (
  <AbsoluteFill>
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#BFE3F5" /><stop offset="1" stopColor="#EAF6FB" /></linearGradient></defs>
      <rect width={W} height={1180} fill="url(#sky)" />
      <circle cx={180} cy={300} r={70} fill="#FFE7A3" />
      <ellipse cx={760} cy={260} rx={120} ry={46} fill="#fff" /><ellipse cx={840} cy={240} rx={80} ry={40} fill="#fff" />
      <rect x={560} y={760} width={420} height={420} rx={10} fill="#F6D9B8" stroke="#B98F63" strokeWidth={10} />
      <polygon points="540,770 770,620 1000,770" fill="#D27A5F" stroke="#9E5A43" strokeWidth={10} />
      {[0, 1, 2].map((c) => [0, 1].map((r) => <rect key={`${c}${r}`} x={600 + c * 125} y={830 + r * 130} width={80} height={80} rx={8} fill="#CFE6F2" stroke="#fff" strokeWidth={6} />))}
      <rect x={730} y={1060} width={80} height={120} rx={8} fill="#9E6B45" />
      <line x1={770} y1={620} x2={770} y2={520} stroke="#7a5a3c" strokeWidth={8} /><polygon points="770,520 850,545 770,570" fill="#D2382B" />
      <rect y={1180} width={W} height={H - 1180} fill="#BFE0B0" />
      <polygon points={`380,1180 700,1180 1080,${H} 0,${H}`} fill="#EBD9BC" />
    </svg>
  </AbsoluteFill>
);

/* Sàn phòng ngủ nhìn từ TRÊN xuống (cho ảnh giường top-down — đặt lên nền tường nhìn ngang trông như giường dựng đứng) */
const Floor: React.FC = () => (
  <AbsoluteFill>
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <rect width={W} height={H} fill="#E7C9A0" />
      {Array.from({ length: 9 }, (_, i) => <rect key={i} x={i * 130 - 20} y={0} width={6} height={H} fill="#D3AE80" />)}
      {Array.from({ length: 9 }, (_, i) => Array.from({ length: 6 }, (_, j) => <rect key={`${i}-${j}`} x={i * 130 - 20} y={j * 360 + (i % 2) * 180} width={130} height={5} fill="#D3AE80" />))}
      <rect x={150} y={1610} width={780} height={260} rx={60} fill="#F4D6D0" stroke="#E6B6AC" strokeWidth={10} />
      <ellipse cx={250} cy={1700} rx={50} ry={28} fill="#8FB9D9" /><ellipse cx={330} cy={1730} rx={50} ry={28} fill="#8FB9D9" />
      <rect x={830} y={560} width={170} height={170} rx={20} fill="#C99E6E" stroke="#A97E52" strokeWidth={8} />
      <circle cx={915} cy={645} r={42} fill="#FFE7A3" />
    </svg>
  </AbsoluteFill>
);

/* Nền chung 1 màu cho cảnh 2 người (thay Versus 2 màu: video AI xê dịch vạch chia -> chữ/tia sét trông lệch) */
const Duo: React.FC = () => (
  <AbsoluteFill>
    <div style={{ position: "absolute", inset: 0, background: "linear-gradient(#FFF6E6,#FBE9CF)" }} />
    <div style={{ position: "absolute", left: 0, right: 0, top: 1720, height: H - 1720, background: "rgba(150,110,70,0.16)" }} />
  </AbsoluteFill>
);

/* Nền đối đầu: nửa trái màu trường (xanh), nửa phải màu nhà (cam) — 🏫 vs 🏠 */
const Versus: React.FC = () => (
  <AbsoluteFill>
    <div style={{ position: "absolute", left: 0, top: 0, width: W / 2, height: H, background: "linear-gradient(#DCEFE6,#C6E3D6)" }} />
    <div style={{ position: "absolute", left: W / 2, top: 0, width: W / 2, height: H, background: "linear-gradient(#FBEBD8,#F5D9BA)" }} />
    <div style={{ position: "absolute", left: 0, right: 0, top: 1720, height: H - 1720, background: "rgba(150,110,70,0.18)" }} />
  </AbsoluteFill>
);

/* Nhãn phe theo nhân vật đang có mặt: 瑾玄 = 🏫 去学校 (xanh), 越黄 = 🏠 在家上学 (cam); cả hai -> 2 nhãn trên đầu từng người + VS */
const TAG = { jx: { t: "🏫 去学校", bg: "#BFE3CC" }, yh: { t: "🏠 在家上学", bg: "#FBD9B4" } };
const Tags: React.FC<{ who: "jx" | "yh" | "both" }> = ({ who }) => {
  const pill = (k: "jx" | "yh", left: number, width: number) => (
    <div key={k} style={{ position: "absolute", left, width, top: 330, height: 110, borderRadius: 55, background: TAG[k].bg, border: "6px solid #3a2a1c", boxShadow: "0 7px 0 #3a2a1c", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: FONT, fontSize: 50, fontWeight: 800, color: "#3a2a1c", whiteSpace: "nowrap" }}>{TAG[k].t}</div>
  );
  if (who !== "both") return pill(who, W / 2 - 240, 480);
  return (
    <>
      {/* 2 nhãn đối xứng qua tâm, khe giữa rộng 130px chứa VS — VS đè lên đầu nhãn thì nhìn lệch (chữ 2 bên dài khác nhau) */}
      {pill("jx", 40, W / 2 - 105)}{pill("yh", W / 2 + 65, W / 2 - 105)}
      <div style={{ position: "absolute", left: W / 2 - 58, top: 345, width: 116, height: 80, borderRadius: 40, background: "#D2382B", border: "6px solid #3a2a1c", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: '"Segoe UI",sans-serif', fontSize: 44, fontWeight: 900, color: "#fff", fontStyle: "italic" }}>VS</div>
    </>
  );
};

/* Nhãn chủ đề 2 phe ở khung đầu (ảnh xem trước): nhìn là biết clip bàn "đi học ở trường hay ở nhà" */
const Labels: React.FC<{ labels: string[] }> = ({ labels }) => (
  <>
    {labels.map((t, i) => (
      <div key={i} style={{ position: "absolute", left: i ? W / 2 + 30 : 30, width: W / 2 - 60, top: 330, height: 110, borderRadius: 55, background: i ? "#FBD9B4" : "#BFE3CC", border: "6px solid #3a2a1c", boxShadow: "0 7px 0 #3a2a1c", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: FONT, fontSize: 50, fontWeight: 800, color: "#3a2a1c", whiteSpace: "nowrap" }}>{t}</div>
    ))}
    {<div style={{ position: "absolute", left: W / 2 - 62, top: 345, width: 124, height: 80, borderRadius: 40, background: "#D2382B", border: "6px solid #3a2a1c", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: '"Segoe UI",sans-serif', fontSize: 44, fontWeight: 900, color: "#fff", fontStyle: "italic" }}>VS</div>}
  </>
);

/* Màn hình chia đôi (c1): trái = đường tới trường (trời sáng), phải = phòng ngủ 越黄; vạch trắng giữa + đồng hồ */
const Split: React.FC<{ clock?: string; labels?: string[]; f: number; overlay?: boolean }> = ({ clock, labels, f, overlay }) => {
  const shake = f < 24 ? Math.sin(f * 1.6) * 6 * (1 - f / 24) : 0; // đồng hồ rung lúc vào (chuông báo thức)
  return (
    <AbsoluteFill>
      {!overlay && (<>
        <div style={{ position: "absolute", left: 0, top: 0, width: W / 2, height: H, background: "linear-gradient(#CFE8F5,#E9F5FA 70%,#CDE3C3 70%)" }} />
        <div style={{ position: "absolute", left: W / 2, top: 0, width: W / 2, height: H, background: "linear-gradient(#EFE3F4,#F7EEDF)" }} />
        <div style={{ position: "absolute", left: W / 2 - 5, top: 0, width: 10, height: H, background: "#fff" }} />
      </>)}
      {/* nhãn chủ đề 2 phe — khung 0 làm ảnh xem trước, nhìn là biết clip bàn "đi học ở trường hay ở nhà" */}
      {!CLEAN && clock && (
        <div style={{ position: "absolute", left: W / 2 - 120, top: labels ? 500 : 420, width: 240, height: 240, borderRadius: "50%", background: "#fff", border: "10px solid #3a2a1c", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: FONT, fontSize: 66, fontWeight: 800, color: "#D2382B", transform: `rotate(${shake}deg)`, boxShadow: "0 8px 20px rgba(0,0,0,0.15)" }}>{clock}</div>
      )}
    </AbsoluteFill>
  );
};

/* Khuôn mặt sống: miệng nhép + chớp mắt. Vẽ lại đúng vùng đó của ảnh gốc (cắt elip, nền = màu da) rồi co/giãn theo
   chiều dọc. Toạ độ theo tỉ lệ ảnh (cx,cy = tâm; rx,ry = nửa trục elip). */
type Part = { cx: number; cy: number; rx: number; ry: number; skin?: string };
const FACE: Record<string, { skin: string; mouth?: Part; eyes?: Part[]; chat?: Part[]; draw?: boolean }> = {
  // <tên-ảnh-không-đuôi>: { skin: "#RRGGBB", mouth: { cx, cy, rx, ry, skin? }, eyes: [{...}, {...}], chat: [{...}] }
  // toạ độ theo TỈ LỆ ảnh (px / rộng, px / cao), dò từ pixel file ảnh — xem reference/gotchas.md
  // draw: ảnh miệng KHÉP (1 nét cười) -> vẽ đè miệng mở to/nhỏ theo giọng thay vì co giãn nét cười
  jx_talk: { skin: "#FFDBC5", mouth: { cx: 0.4989, cy: 0.3289, rx: 0.0873, ry: 0.0191 } },
  jx_wave: { skin: "#FFDCC7", mouth: { cx: 0.4165, cy: 0.3119, rx: 0.0746, ry: 0.0227 } },
  yh_wave: { skin: "#FEE1CF", mouth: { cx: 0.473, cy: 0.372, rx: 0.055, ry: 0.016 } },
  yh_proud: { skin: "#FEE1CF", draw: true, mouth: { cx: 0.499, cy: 0.385, rx: 0.084, ry: 0.012 } },
  yh_shrug: { skin: "#FEE1CF", draw: true, mouth: { cx: 0.489, cy: 0.396, rx: 0.066, ry: 0.012 } },
  yh_breakfast: { skin: "#FEE1CF", draw: true, mouth: { cx: 0.478, cy: 0.412, rx: 0.066, ry: 0.01 } },
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
  if (a.bob === "voice") { dy = -e * 4; sy = 1 + e * 0.008; } // nhún nhẹ — 16px bị chê "nhảy nhảy, nhức mắt"
  if (a.lean) rot += a.lean * Math.min(1, f / (0.5 * FPS)); // nghiêng người về phía người đối diện
  if (a.bob !== "laugh" && !a.still) { sy *= 1 + 0.011 * Math.sin(f / 12 + ph); rot += 0.8 * Math.sin(f / 27 + ph); } // thở + dồn trọng tâm
  if (a.walk && a.from !== undefined && f < (a.fromSec ?? 0.55) * FPS) { dy = -Math.abs(Math.sin(f / 4)) * 16; rot += Math.sin(f / 4) * 2; }
  if (a.bob === "laugh") { dy = -Math.abs(Math.sin(f / 5)) * 6; rot = Math.sin(f / 5) * 0.6; }
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
      {a.talk && face.mouth && !face.draw && patch(face.mouth, 1 + mouth * 0.08, 0.35 + mouth * 0.85, "m")}
      {a.talk && face.mouth && face.draw && mouth > 0.08 && (() => { // miệng mở vẽ đè lên nét cười khép
        const m = face.mouth, mx = m.cx * iw, my = m.cy * ih, mw = m.rx * iw * 0.62, mh = Math.max(3, mouth * m.rx * iw * 0.5);
        return (
          <svg viewBox={`0 0 ${iw} ${ih}`} style={{ ...base, overflow: "visible" }}>
            <ellipse cx={mx} cy={my} rx={m.rx * iw * 1.05} ry={m.ry * ih * 1.6 + mh * 0.6} fill={face.skin} />
            <ellipse cx={mx} cy={my + mh * 0.3} rx={mw} ry={mh} fill="#8E3B36" stroke="#4E2A20" strokeWidth={2.5} />
            <ellipse cx={mx} cy={my + mh * 0.85} rx={mw * 0.55} ry={mh * 0.4} fill="#E98A86" />
          </svg>
        );
      })()}
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
  const { s, n, voice, offset, chars, vfrom, cont } = L;
  const f = useCurrentFrame();
  const e = env[voice]?.[offset + f] ?? 0;
  // có giọng -> miệng theo âm lượng; chưa có -> mở/ngậm theo từng chữ trên màn hình
  const syl = SEC_PER_CHAR * FPS;
  const mouth = CLEAN ? 0 : dur[voice] ? Math.min(1, e * 1.3) : f < chars * syl ? Math.pow(Math.abs(Math.sin((Math.PI * f) / syl)), 0.7) : 0;
  const { fps } = useVideoConfig();
  const p = f / n;
  // cảnh đầu KHÔNG mờ dần: khung 0 là ảnh xem trước trên TikTok/RedNote — trắng trơn thì người ta lướt qua
  const fadeIn = L.start === 0 || cont || s.video ? 1 : interpolate(f, [0, 6], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: fadeIn }}>
      {s.video && s.split && <Split clock={s.clock} labels={s.labels} f={f + (cont ? vfrom : 0)} overlay />}
      {s.video ? null : s.split ? <Split clock={s.clock} labels={s.labels} f={f} /> : s.bg === "duo" ? <Duo /> : s.bg === "floor" ? <Floor /> : s.bg === "road" ? <Road /> : s.bg === "school" ? <School /> : s.bg === "versus" ? <Versus /> : <Room door={s.door} />}
      {!CLEAN && s.labels && <Labels labels={s.labels} />}
      {!CLEAN && s.who && <Tags who={s.who} />}
      {!CLEAN && s.spark && (() => { // tia lửa ⚡ giữa 2 người khi cãi nhau
        const k = spring({ frame: f, fps, config: { damping: 9 } });
        const flick = 1 + 0.08 * Math.sin(f / 2);
        // tia sét SVG (emoji ⚡ lệch tâm do lề chữ) — tâm đúng vạch chia 2 phe, ngang tầm mặt
        return (
          <svg width={200} height={280} viewBox="0 0 100 140" style={{ position: "absolute", left: W / 2 - 100, top: 900, transform: `scale(${k * flick})` }}>
            <polygon points="62,4 18,78 48,78 36,136 84,52 54,52" fill="#FFC93C" stroke="#E0611F" strokeWidth={5} strokeLinejoin="round" />
          </svg>
        );
      })()}
      {!CLEAN && s.vote && (() => { // 2 nút chọn phe
        const k = spring({ frame: f, fps, config: { damping: 12 } });
        const pill = (label: string, x: number, bgc: string) => (
          <div style={{ position: "absolute", left: x, top: 400, width: 380, height: 120, borderRadius: 60, background: bgc, border: "6px solid #3a2a1c", display: "flex", alignItems: "center", justifyContent: "center", gap: 14, fontFamily: FONT, fontSize: 52, fontWeight: 800, color: "#3a2a1c", transform: `scale(${k})`, boxShadow: "0 8px 0 #3a2a1c" }}>{label}</div>
        );
        return <>{pill("🏫 在学校", 70, "#BFE3CC")}{pill("🏠 在家", 630, "#FBD9B4")}</>;
      })()}
      {s.glow?.map((g, i) => {
        const t = (p - g.at) / 0.22;
        if (t < 0 || t > 1) return null;
        const r = 60 + t * 190;
        return <div key={i} style={{ position: "absolute", left: g.x - r, top: g.y - r, width: r * 2, height: r * 2, borderRadius: "50%", border: "10px solid rgba(255,196,64,0.9)", opacity: 1 - t, boxShadow: "0 0 40px rgba(255,196,64,0.7)" }} />;
      })}
      {!s.video && [...s.actors].sort((a, b) => (a.z ?? 0) - (b.z ?? 0)).map((a, i) => <ActorView key={i} a={a} sceneId={s.id} f={f} n={n} e={e} mouth={mouth} />)}
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
{!CLEAN && s.text && (      <div style={{ position: "absolute", left: 70, right: 70, top: 200, textAlign: "center", fontFamily: FONT, fontWeight: 800, fontSize: s.text.length > 14 ? 50 : 66, lineHeight: 1.3, color: "#fff", WebkitTextStroke: "14px #3a2a1c", paintOrder: "stroke fill" as any }}>{s.text}</div>)}
    </AbsoluteFill>
  );
};

const VideoLayer: React.FC<{ g: VG; first: boolean }> = ({ g, first }) => {
  const f = useCurrentFrame();
  const op = first ? 1 : interpolate(f, [0, XF], [0, 1], { extrapolateRight: "clamp", easing: ease });
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <OffthreadVideo src={staticFile(`motion/${g.video}.mp4`)} startFrom={g.vfrom} muted style={{ width: W, height: H, objectFit: "cover" }} />
    </AbsoluteFill>
  );
};

const Wm: React.FC = () => {
  const f = useCurrentFrame();
  const [x, y] = WM_SPOTS[Math.floor(f / FPS / 6) % WM_SPOTS.length];
  return <div style={{ position: "absolute", left: x, top: y, fontSize: 26, fontWeight: 700, color: "#3a2a1c", opacity: 0.22, fontFamily: FONT }}>瑾玄在练嘴</div>;
};

export const Story: React.FC = () => {
  const voices = [...new Set(layout.map((L) => L.voice))];
  return (
    <AbsoluteFill style={{ background: "#FBF3E6" }}>
      {vgroups.map((g, i) => {
        const last = i === vgroups.length - 1;
        const tail = last ? OUTRO_START - (g.start + g.n) + XF : XF;   // đoạn cuối phủ tới khi đoạn kết hiện
        return (
          <Sequence key={`v${i}`} from={g.start} durationInFrames={g.n + tail} premountFor={FPS}>
            <VideoLayer g={g} first={i === 0} />
          </Sequence>
        );
      })}
      {layout.map((L) => (
        <Sequence key={L.s.id} from={L.start} durationInFrames={L.n}>
          <SceneView L={L} />
        </Sequence>
      ))}
      <Audio src={staticFile("audio/bed.wav")} />   {/* nhạc nền + hiệu ứng: python make_bed.py */}
      {/* chống copy + tên kênh (design-rules §11) */}
      {!CLEAN && (<>
      <div style={{ position: "absolute", top: 60, right: 46, fontSize: 26, fontWeight: 700, color: "#D2382B", background: "#fff", border: "3px solid #D2382B", borderRadius: 10, padding: "3px 10px", fontFamily: FONT }}>禁止搬运</div>
      <div style={{ position: "absolute", bottom: 40, right: 50, fontSize: 32, fontWeight: 800, color: "#fff", WebkitTextStroke: "8px #3a2a1c", paintOrder: "stroke fill" as any, fontFamily: FONT }}>@瑾玄在练嘴</div>
      <Wm />
      </>)}
      <Sequence from={OUTRO_START}><Outro text="谢谢大家的观看～喜欢的话，记得点赞、关注我哦！" /></Sequence>
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
