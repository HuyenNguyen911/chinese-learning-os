import { AbsoluteFill, Img, staticFile } from "remotion";

// Ảnh bìa bài đăng 3:4 (1080×1440) — dùng chung mọi nền tảng.
// Tiêu đề + mặt nhân vật dồn vào vùng giữa vì HelloTalk/Facebook hay cắt ảnh xem trước gần vuông.
const FONT = '"Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif';
const EMOJI = '"Segoe UI Emoji","Apple Color Emoji",sans-serif';

const Spark = ({ x, y, s, r = 0 }: { x: number; y: number; s: number; r?: number }) => (
  <div style={{ position: "absolute", left: x, top: y, fontSize: s, transform: `rotate(${r}deg)`, fontFamily: EMOJI }}>✨</div>
);

const Shadow = ({ cx, y, w }: { cx: number; y: number; w: number }) => (
  <div style={{ position: "absolute", left: cx - w / 2, top: y - 20, width: w, height: 40, borderRadius: "50%", background: "rgba(90,60,30,0.16)", filter: "blur(6px)" }} />
);

export const Cover = () => (
  <AbsoluteFill style={{ background: "#FBF3E6", overflow: "hidden" }}>
    {/* quầng nắng ấm sau nhân vật */}
    <div style={{ position: "absolute", left: 540 - 760, top: 1000 - 760, width: 1520, height: 1520, borderRadius: "50%", background: "repeating-conic-gradient(rgba(255,196,110,0.20) 0deg 9deg, rgba(255,196,110,0) 9deg 20deg)", WebkitMaskImage: "radial-gradient(circle, #000 25%, transparent 68%)" }} />
    <div style={{ position: "absolute", left: 540 - 520, top: 1000 - 420, width: 1040, height: 840, borderRadius: "50%", background: "radial-gradient(closest-side, rgba(255,214,150,0.55), rgba(255,214,150,0))" }} />

    {/* nhãn series */}
    <div style={{ position: "absolute", top: 118, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
      <div style={{ background: "#2F6F6A", color: "#fff", fontFamily: FONT, fontWeight: 700, fontSize: 40, padding: "12px 36px", borderRadius: 40, letterSpacing: 2 }}>
        每周一个话题 · Vol. 01
      </div>
    </div>

    {/* tiêu đề */}
    <div style={{ position: "absolute", top: 250, left: 40, right: 40, textAlign: "center", fontFamily: FONT, fontWeight: 900, fontSize: 104, lineHeight: 1.22, color: "#2A231C" }}>
      <div>快乐真的会</div>
      <div>“<span style={{ color: "#E8573A" }}>传染</span>”吗？</div>
    </div>

    {/* nhân vật */}
    <Shadow cx={680} y={1312} w={700} />
    <Img src={staticFile("img/parents_sofa_laugh_v2.png")} style={{ position: "absolute", left: 300, top: 1312 - 588, width: 760 }} />
    <Shadow cx={212} y={1392} w={260} />
    <Img src={staticFile("img/jx3_laugh.png")} style={{ position: "absolute", left: 50, top: 1392 - 720, height: 720 }} />

    <Spark x={600} y={590} s={64} r={-12} />
    <Spark x={960} y={660} s={52} r={14} />
    <Spark x={40} y={600} s={56} r={10} />

    <div style={{ position: "absolute", right: 40, bottom: 22, fontFamily: FONT, fontWeight: 700, fontSize: 28, color: "#3a2a1c", opacity: 0.45 }}>@瑾玄在练嘴</div>
  </AbsoluteFill>
);
