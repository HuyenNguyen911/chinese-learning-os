import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";

/* KHUNG TĨNH v2 (theme mùa đông ấm cúng) cho 9 đoạn video minh hoạ khung S4, tỉ lệ 16:9.
   Ghép từ nhân vật chibi mới (public/img). KHÔNG chữ (AI làm méo). Là ảnh đầu vào gen_motion. */
export const KW = 1280, KH = 720;

const Living: React.FC = () => (
  <AbsoluteFill>
    <div style={{ position: "absolute", inset: 0, background: "#F5DDBD" }} />
    <div style={{ position: "absolute", left: 0, right: 0, top: 330, height: 14, background: "#E7C79B" }} />
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 215, background: "#C99A66" }} />
    {[0, 1, 2, 3, 4, 5].map((i) => <div key={i} style={{ position: "absolute", left: 0, right: 0, bottom: 20 + i * 36, height: 2, background: "rgba(120,80,40,.25)" }} />)}
    <div style={{ position: "absolute", left: 330, bottom: 40, width: 620, height: 120, borderRadius: "50%", background: "#B4573F", opacity: 0.55 }} />
    <div style={{ position: "absolute", left: 90, top: 60, width: 170, height: 210, borderRadius: 10, background: "#F3C98B", border: "9px solid #A97C50" }} />
    <div style={{ position: "absolute", left: 1000, top: 70, width: 190, height: 200, borderRadius: 10, background: "#D8EAF4", border: "10px solid #fff", boxShadow: "0 0 0 4px #CDAE86" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: "48%", height: 5, background: "#fff" }} />
      <div style={{ position: "absolute", top: 0, bottom: 0, left: "48%", width: 5, background: "#fff" }} />
    </div>
    <div style={{ position: "absolute", left: 1130, top: 440, width: 90, height: 130, borderRadius: "40% 40% 10% 10%", background: "#6FAE6B" }} />
    <div style={{ position: "absolute", left: 1118, top: 560, width: 114, height: 70, borderRadius: 12, background: "#B77A4B" }} />
  </AbsoluteFill>
);
const Room: React.FC = () => (
  <AbsoluteFill>
    <Img src={staticFile("img/room2_a.png")} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 88%" }} />
  </AbsoluteFill>
);
const Study: React.FC = () => (
  <AbsoluteFill>
    <div style={{ position: "absolute", inset: 0, background: "#F4E3CC" }} />
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 180, background: "#C79C6B" }} />
    <div style={{ position: "absolute", left: 80, top: 60, width: 330, height: 330, borderRadius: 14, background: "linear-gradient(#FBD9A6,#BFE0F2)", border: "12px solid #fff", boxShadow: "0 0 0 5px #CDAE86" }}>
      <div style={{ position: "absolute", left: 120, top: 150, width: 90, height: 90, borderRadius: "50%", background: "#FFD25E", opacity: 0.9 }} />
    </div>
    <div style={{ position: "absolute", left: 960, top: 50, width: 260, height: 400, background: "#B98655", borderRadius: 8 }}>
      {[0, 1, 2, 3].map((r) => (
        <div key={r} style={{ position: "absolute", left: 14, right: 14, top: 20 + r * 94, height: 78, background: "#E9D3AC", borderRadius: 4, display: "flex", gap: 6, padding: 6 }}>
          {[0, 1, 2, 3, 4].map((b) => <div key={b} style={{ flex: 1, background: ["#E8503A", "#3A6EBE", "#2FA36B", "#F59A23", "#8A5CC9"][(b + r) % 5], borderRadius: 3 }} />)}
        </div>
      ))}
    </div>
  </AbsoluteFill>
);
const Cafe: React.FC = () => (
  <AbsoluteFill>
    <div style={{ position: "absolute", inset: 0, background: "#7A4B35" }} />
    {Array.from({ length: 14 }, (_, i) => <div key={i} style={{ position: "absolute", left: (i % 7) * 190 - 20, top: Math.floor(i / 7) * 90 + 150, width: 180, height: 80, borderRadius: 6, background: i % 2 ? "#8C5A41" : "#6E4230" }} />)}
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 200, background: "#4A2E22" }} />
    <div style={{ position: "absolute", left: 100, top: 40, width: 440, height: 170, borderRadius: 10, background: "#2E2A28", border: "6px solid #B98655" }}>
      {[0, 1, 2, 3].map((r) => <div key={r} style={{ position: "absolute", left: 24, width: 200 + (r % 2) * 120, top: 24 + r * 36, height: 12, borderRadius: 6, background: "rgba(255,240,210,.7)" }} />)}
    </div>
    {[200, 480, 760, 1040].map((x, i) => (
      <React.Fragment key={i}>
        <div style={{ position: "absolute", left: x + 25, top: 0, width: 4, height: 70 + (i % 2) * 20, background: "#2E2018" }} />
        <div style={{ position: "absolute", left: x, top: 70 + (i % 2) * 20, width: 54, height: 54, borderRadius: "50%", background: "#FFD98A", boxShadow: "0 0 50px 20px rgba(255,210,120,.5)" }} />
      </React.Fragment>
    ))}
  </AbsoluteFill>
);
const Street: React.FC = () => (
  <AbsoluteFill>
    <div style={{ position: "absolute", inset: 0, background: "linear-gradient(#CFE3F1,#EEF5FA)" }} />
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 230, background: "#F7FAFC" }} />
    <div style={{ position: "absolute", left: 120, bottom: 200, width: 24, height: 250, background: "#7C5A3E" }} />
    <div style={{ position: "absolute", left: 1040, bottom: 190, width: 28, height: 300, background: "#7C5A3E" }} />
    {[[40, 110], [210, 150], [320, 90], [1180, 70], [900, 130]].map(([x, y], i) => <div key={i} style={{ position: "absolute", left: x, top: y, width: 18, height: 18, borderRadius: "50%", background: "#fff", boxShadow: "0 0 8px #fff" }} />)}
    {[[80, 200], [1130, 160], [1000, 260], [260, 40]].map(([x, y], i) => <div key={i} style={{ position: "absolute", left: x, top: y, width: 140, height: 40, borderRadius: 20, background: "#fff", opacity: 0.8 }} />)}
  </AbsoluteFill>
);

const P: React.FC<{ img: string; x: number; feet: number; h: number; flip?: boolean }> = ({ img, x, feet, h, flip }) => (
  <Img src={staticFile(`img/${img}.png`)} style={{ position: "absolute", left: x, top: feet - h, height: h, transform: flip ? "scaleX(-1)" : undefined, filter: "drop-shadow(0 8px 6px rgba(80,60,30,0.18))" }} />
);
const Heart: React.FC<{ x: number; y: number; s?: number }> = ({ x, y, s = 52 }) => <div style={{ position: "absolute", left: x, top: y, fontSize: s, color: "#E8503A" }}>♥</div>;
const Bubble: React.FC<{ x: number; y: number; w: number }> = ({ x, y, w }) => (
  <div style={{ position: "absolute", left: x, top: y, width: w, height: 54, borderRadius: 27, background: "#fff", border: "4px solid #3A6EBE" }}>
    <div style={{ position: "absolute", left: 18, top: 20, width: w - 60, height: 10, borderRadius: 5, background: "#C6D6EE" }} />
  </div>
);


/* thư trúng tuyển (không chữ): giấy trắng viền vàng + dấu đỏ, 2 bàn tay nhỏ đè lên mép — vẽ đè lên nhân vật đã duyệt */
const Letter: React.FC<{ x: number; y: number; s?: number; rot?: number }> = ({ x, y, s = 1, rot = -8 }) => (
  <div style={{ position: "absolute", left: x - 55 * s, top: y - 70 * s, width: 110 * s, height: 140 * s, transform: `rotate(${rot}deg)` }}>
    <div style={{ position: "absolute", inset: 0, borderRadius: 8 * s, background: "#fff", border: `${4 * s}px solid #E5A63C`, boxShadow: "0 6px 12px rgba(80,60,30,.25)" }}>
      {[0, 1, 2].map((i) => <div key={i} style={{ position: "absolute", left: 16 * s, right: 16 * s, top: (22 + i * 16) * s, height: 6 * s, borderRadius: 3 * s, background: "#EFD7A8" }} />)}
      <div style={{ position: "absolute", left: 38 * s, top: 82 * s, width: 34 * s, height: 34 * s, borderRadius: "50%", background: "#D2382B" }} />
    </div>
    {[-1, 1].map((d) => <div key={d} style={{ position: "absolute", left: (d < 0 ? -12 : 90) * s, top: 96 * s, width: 32 * s, height: 26 * s, borderRadius: "50%", background: "#FFD9C7", border: `${3 * s}px solid #4a2a22` }} />)}
  </div>
);

export const K1: React.FC = () => (<AbsoluteFill><Room /><P img="fam4_sofa_b" x={360} feet={680} h={500} /><Letter x={665} y={480} s={0.9} rot={-6} /></AbsoluteFill>);
export const K2: React.FC = () => (<AbsoluteFill><Room /><P img="fam4_hugl_b" x={650} feet={690} h={520} /><P img="yh_w_puzzled_a" x={150} feet={690} h={450} /></AbsoluteFill>);
export const K3: React.FC = () => (<AbsoluteFill><Room /><P img="fam4_hugl_b" x={700} feet={690} h={520} /><P img="yh_w_stroll_b" x={330} feet={695} h={440} /><Heart x={640} y={110} s={44} /><Heart x={1010} y={140} s={40} /></AbsoluteFill>);
export const K4: React.FC = () => (<AbsoluteFill><AbsoluteFill><Img src={staticFile("img/bg_study.png")} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 88%" }} /></AbsoluteFill><P img="yh_w_desk_hb_b" x={330} feet={700} h={620} /></AbsoluteFill>);
export const K5: React.FC = () => (<AbsoluteFill><Room /><P img="fam4_read" x={690} feet={660} h={430} /><P img="yh_w_stroll_b" x={405} feet={705} h={430} /></AbsoluteFill>);
export const K6: React.FC = () => (<AbsoluteFill><Room /><P img="yh_w_phone_s_b" x={420} feet={700} h={580} /><Bubble x={850} y={190} w={240} /><Bubble x={900} y={280} w={190} /><Bubble x={160} y={230} w={210} /></AbsoluteFill>);
export const K7: React.FC = () => (<AbsoluteFill><AbsoluteFill><Img src={staticFile("img/bg_cafe.png")} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 88%" }} /></AbsoluteFill><P img="friends4_c" x={290} feet={700} h={480} /></AbsoluteFill>);
export const K8: React.FC = () => (<AbsoluteFill><Room /><P img="fam4_sofa_b" x={640} feet={660} h={440} /><P img="yh_w_wave" x={250} feet={705} h={450} /><Heart x={560} y={190} /><Heart x={470} y={320} s={40} /><Heart x={760} y={110} s={44} /></AbsoluteFill>);
export const K9: React.FC = () => (<AbsoluteFill><AbsoluteFill><Img src={staticFile("img/bg_street.png")} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 88%" }} /></AbsoluteFill><P img="friends4_c" x={290} feet={700} h={500} /><Heart x={200} y={170} s={44} /><Heart x={1020} y={150} s={50} /><Heart x={640} y={70} s={40} /></AbsoluteFill>);

const House: React.FC<{ x: number }> = ({ x }) => (
  <>
    <div style={{ position: "absolute", left: x, top: 250, width: 380, height: 240, background: "#F1D9B4", border: "6px solid #B98655", borderRadius: 8 }} />
    <div style={{ position: "absolute", left: x - 34, top: 170, width: 448, height: 110, background: "#fff", border: "6px solid #CBD9E6", borderRadius: "50% 50% 8px 8px / 100% 100% 8px 8px" }} />
    <div style={{ position: "absolute", left: x + 40, top: 320, width: 100, height: 100, background: "#FFE49A", border: "6px solid #fff", boxShadow: "0 0 30px 10px rgba(255,210,120,.5)" }} />
    <div style={{ position: "absolute", left: x + 225, top: 340, width: 90, height: 150, background: "#C0553B", border: "6px solid #8E3C28", borderRadius: "45px 45px 0 0" }} />
  </>
);
/* nền tuyết riêng: nhà đứng trên nền tuyết, lối đi nhỏ dẫn từ dưới-trái thẳng tới cửa (không dùng bg_street vì đường lớn) */
export const K10: React.FC = () => (
  <AbsoluteFill>
    <div style={{ position: "absolute", inset: 0, background: "linear-gradient(#CFE3F1,#EEF5FA)" }} />
    {[[80, 70, 150], [420, 40, 120], [1090, 90, 150]].map(([x, y, w], i) => <div key={i} style={{ position: "absolute", left: x, top: y, width: w, height: 40, borderRadius: 20, background: "#fff", opacity: 0.8 }} />)}
    {[[60, 160], [250, 110], [520, 190], [900, 130], [1200, 200], [700, 60]].map(([x, y], i) => <div key={i} style={{ position: "absolute", left: x, top: y, width: 16, height: 16, borderRadius: "50%", background: "#fff", boxShadow: "0 0 8px #fff" }} />)}
    <div style={{ position: "absolute", left: 0, top: 480, width: 1280, height: 240, background: "#FAFCFE" }} />
    <div style={{ position: "absolute", left: 0, top: 480, width: 1280, height: 240, background: "#D5E2EE", clipPath: "polygon(930px 10px, 1010px 10px, 1000px 240px, 150px 240px)" }} />
    <House x={780} />
    <P img="yh_w_stroll_b" x={470} feet={690} h={400} />
  </AbsoluteFill>
);
export const K11: React.FC = () => (<AbsoluteFill><Room /><P img="friends4_table" x={290} feet={700} h={500} /></AbsoluteFill>);
export const K12: React.FC = () => (<AbsoluteFill><Img src={staticFile("img/bg_study.png")} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 88%" }} /><P img="yh_papers" x={340} feet={700} h={610} /></AbsoluteFill>);
export const K13: React.FC = () => (<AbsoluteFill><Img src={staticFile("img/bg_street.png")} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 88%" }} /><P img="friends4_c" x={300} feet={700} h={520} /></AbsoluteFill>);
export const K14: React.FC = () => (<AbsoluteFill><Room /><P img="yh_thumb" x={370} feet={700} h={500} /><P img="jx3_smile" x={650} feet={700} h={520} /></AbsoluteFill>);
