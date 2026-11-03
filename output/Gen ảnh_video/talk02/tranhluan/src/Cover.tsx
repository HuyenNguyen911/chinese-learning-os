import { AbsoluteFill, Img, staticFile } from "remotion";

// Ảnh bìa bài đăng 3:4 (1080×1440) — dùng chung mọi nền tảng.
// Tiêu đề + mặt nhân vật dồn vào vùng giữa vì HelloTalk/Facebook hay cắt ảnh xem trước gần vuông.
// Nhân vật = ảnh đã duyệt trong clip (không gen lại): 瑾玄 chống nạnh (phe 在学校) vs 越黄 khoanh tay (phe 在家).
const FONT = '"Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif';
const GREEN = "#2F8A5B", ORANGE = "#E07A2E";

const Shadow = ({ cx, y, w }: { cx: number; y: number; w: number }) => (
  <div style={{ position: "absolute", left: cx - w / 2, top: y - 20, width: w, height: 40, borderRadius: "50%", background: "rgba(90,60,30,0.16)", filter: "blur(6px)" }} />
);

export const Cover = () => (
  <AbsoluteFill style={{ background: "#FBF3E6", overflow: "hidden" }}>
    {/* 2 quầng màu phe sau nhân vật: trái xanh (trường), phải cam (nhà) */}
    <div style={{ position: "absolute", left: 300 - 420, top: 1000 - 420, width: 840, height: 840, borderRadius: "50%", background: "radial-gradient(closest-side, rgba(150,210,175,0.55), rgba(150,210,175,0))" }} />
    <div style={{ position: "absolute", left: 790 - 420, top: 1000 - 420, width: 840, height: 840, borderRadius: "50%", background: "radial-gradient(closest-side, rgba(250,200,150,0.6), rgba(250,200,150,0))" }} />

    {/* nhãn series */}
    <div style={{ position: "absolute", top: 118, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
      <div style={{ background: "#2F6F6A", color: "#fff", fontFamily: FONT, fontWeight: 700, fontSize: 40, padding: "12px 36px", borderRadius: 40, letterSpacing: 2 }}>
        每周一个话题 · Vol. 02
      </div>
    </div>

    {/* tiêu đề */}
    <div style={{ position: "absolute", top: 250, left: 40, right: 40, textAlign: "center", fontFamily: FONT, fontWeight: 900, fontSize: 104, lineHeight: 1.22, color: "#2A231C" }}>
      <div>上学，你选哪边？</div>
      <div><span style={{ color: GREEN }}>在学校</span>还是<span style={{ color: ORANGE }}>在家</span>？</div>
    </div>

    {/* nhân vật */}
    <Shadow cx={300} y={1340} w={300} />
    <Img src={staticFile("img/jx_hips.png")} style={{ position: "absolute", left: 300 - (760 * 474 / 1016) / 2, top: 1340 - 760, height: 760 }} />
    <Shadow cx={790} y={1340} w={320} />
    <Img src={staticFile("img/yh_proud.png")} style={{ position: "absolute", left: 790 - (760 * 557 / 1055) / 2, top: 1340 - 760, height: 760 }} />

    {/* VS giữa 2 người */}
    <div style={{ position: "absolute", left: 540 - 75, top: 880, width: 150, height: 100, borderRadius: 50, background: "#D2382B", border: "7px solid #3a2a1c", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: '"Segoe UI",sans-serif', fontSize: 58, fontWeight: 900, color: "#fff", fontStyle: "italic", transform: "rotate(-6deg)" }}>VS</div>


    <div style={{ position: "absolute", right: 40, bottom: 12, fontFamily: FONT, fontWeight: 700, fontSize: 26, color: "#3a2a1c", opacity: 0.45 }}>@瑾玄在练嘴</div>
  </AbsoluteFill>
);
