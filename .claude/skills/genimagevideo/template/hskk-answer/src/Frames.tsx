import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";

/* KHUNG HÌNH MẪU v3 (chưa có giọng/chuyển động) — video HSKK 高级 · Chủ đề 2 (在家上学) · câu hỏi 6.
   Nội dung lấy từ onluyen/bai-mau-cau5-6.md (Bài 2, Câu 6). Bản dịch EN/VI là bản nháp của Claude, cần user rà.
   Nhân vật = 越黄 (yh, giọng nam trẻ). */
export const W = 1080, H = 1920;
export const FONT = '"Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif';
export const SANS = '"Segoe UI",sans-serif';
export const C = { ink: "#26231f", red: "#D2382B", green: "#3E8E5E", mint: "#BFE3CC", line: "#DCD5C6", bg: "#FFFBF2", sub: "#5b5248" };
const YH = { src: "img/jx3_smile.png", w: 364, h: 845, vis: 0.30 };       // vis = tỉ lệ chiều cao ảnh từ đỉnh tóc tới dưới miệng

export type Lang = "en" | "vi";
export const t = (lang: Lang, en: string, vi: string) => (lang === "vi" ? vi : en);

export const TOPIC = (l: Lang) => `在家上学 · ${t(l, "Homeschooling", "Học ở nhà")}`;
export const Q = "如果你有了子女，你会为他/她选择哪种学习方式？";
export const QT = (l: Lang) => t(l, "If you had children, which way of learning would you choose for them?", "Nếu sau này có con, bạn sẽ chọn cách học nào cho con?");

// 4 phần của bài (màu theo mindmap tham khảo). Chỉ dùng ở mindmap, KHÔNG hiện ở phần đọc (user bỏ thẻ mở/thân/kết ở S4)
export const SEC = [
  { zh: "开头", c: "#E8503A", tint: "#FCE3DF" },
  { zh: "理由一", c: "#F59A23", tint: "#FDEBD0" },
  { zh: "理由二", c: "#3A6EBE", tint: "#DCE6F6" },
  { zh: "另外", c: "#8A5CC9", tint: "#EBE1F7" },
  { zh: "结尾", c: "#2FA36B", tint: "#D9F1E3" },
];

// Cụm đáng học: chỉ cụm KHÓ / vế ngắn (cụm dễ + câu dài bỏ). py = chỉ hiện khi khó đọc.
export type Ph = { han: string; py?: string; en: string; vi: string };
export const PH: Record<string, Ph> = {
  qxy: { han: "更倾向于", py: "gèng qīngxiàng yú", en: "lean more toward", vi: "nghiêng về…" },
  pk: { han: "偏科", py: "piānkē", en: "favor one subject", vi: "học lệch" },
  rjjw: { han: "人际交往", py: "rénjì jiāowǎng", en: "social interaction", vi: "giao tiếp với mọi người" },
  qz: { han: "亲自", py: "qīnzì", en: "in person, oneself", vi: "đích thân, tự mình" },
  csbl: { han: "承受不了", py: "chéngshòu bù liǎo", en: "can't afford / bear", vi: "kham không nổi" },
  cy: { han: "出于对…的考虑", py: "chūyú duì… de kǎolǜ", en: "out of concern for…", vi: "vì nghĩ cho…" },
};

/* ---------- phần dùng chung ---------- */
export const Title: React.FC<{ sub?: string }> = ({ sub }) => (
  <div style={{ position: "absolute", top: 58, left: 0, right: 0, display: "flex", justifyContent: "center", alignItems: "baseline", gap: 22 }}>
    <div style={{ position: "relative", fontSize: 58, fontWeight: 800, color: C.ink, letterSpacing: 4, isolation: "isolate" }}>
      <div style={{ position: "absolute", left: -14, right: -4, bottom: 4, height: 26, borderRadius: 13, background: C.mint, zIndex: -1 }} />
      HSKK 高级
    </div>
    {sub && <div style={{ fontSize: 40, color: C.line, fontWeight: 300 }}>|</div>}
    {sub && <div style={{ fontSize: 46, fontWeight: 700, color: C.green }}>{sub}</div>}
  </div>
);

export const Chrome: React.FC<{ n: number; lang: Lang }> = ({ n, lang }) => (
  <>
    <div style={{ position: "absolute", top: 70, right: 46, fontSize: 24, fontWeight: 700, color: C.red, background: "#fff", border: `3px solid ${C.red}`, borderRadius: 10, padding: "3px 10px" }}>禁止搬运</div>
    {/* tên chủ đề nhỏ dưới chân trang */}
    <div style={{ position: "absolute", left: 0, right: 0, top: 1790, textAlign: "center", fontSize: 30, color: C.sub, opacity: 0.8 }}>{TOPIC(lang)}</div>
    <div style={{ position: "absolute", left: [470, 780, 620, 300][n], top: 1850, fontSize: 26, fontWeight: 700, color: C.ink, opacity: 0.16 }}>瑾玄在练嘴</div>
  </>
);

/* nhân vật nhỏ bám mép trên 1 khung: ló đầu + 2 bàn tay. (x,y) = tâm ngang, mép khung. Vẽ TRƯỚC khung để khung che phần dưới. */
export const Peeker: React.FC<{ x: number; y: number; w?: number; tilt?: number }> = ({ x, y, w = 190, tilt = -4 }) => {
  const h = (YH.h / YH.w) * w, vis = YH.vis * h;
  const hand = (dx: number) => (
    <div style={{ position: "absolute", left: w / 2 + dx - 17, top: vis - 12, width: 34, height: 28, borderRadius: "50%", background: "#FFD9C7", border: "3px solid #4a2a22" }} />
  );
  return (
    <div style={{ position: "absolute", left: x - w / 2, top: y - vis + 8, width: w, height: vis + 20, transform: `rotate(${tilt}deg)`, transformOrigin: "50% 100%" }}>
      <div style={{ width: w, height: vis, overflow: "hidden" }}>
        <Img src={staticFile(YH.src)} style={{ width: w, height: h, display: "block" }} />
      </div>
      {hand(-w * 0.34)}
      {hand(w * 0.34)}
    </div>
  );
};
/* nhân vật đứng ở góc: toàn thân nhỏ, chân đặt trên mép dưới vùng nội dung */
const Standing: React.FC<{ right: number; feet: number; h: number }> = ({ right, feet, h }) => (
  <div style={{ position: "absolute", right, top: feet - h, height: h, width: (YH.w / YH.h) * h }}>
    <div style={{ position: "absolute", left: "8%", right: "8%", bottom: -6, height: 22, borderRadius: "50%", background: "rgba(80,70,50,0.12)" }} />
    <Img src={staticFile(YH.src)} style={{ width: "100%", height: "100%" }} />
  </div>
);

export const Card: React.FC<{ style: React.CSSProperties; children?: React.ReactNode }> = ({ style, children }) => (
  <div style={{ position: "absolute", borderRadius: 32, background: "#fff", border: `4px solid ${C.red}`, boxShadow: "0 10px 28px rgba(60,40,20,0.12)", ...style }}>{children}</div>
);
export const Tag: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <div style={{ position: "absolute", top: -24, left: 30, background: C.green, color: "#fff", fontSize: 26, fontWeight: 700, borderRadius: 12, padding: "4px 16px", ...style }}>{children}</div>
);

/* ---------- Cảnh 1: câu hỏi (hook) — giữa khung ---------- */
export const S1: React.FC<{ lang: Lang }> = ({ lang }) => (
  <AbsoluteFill style={{ background: C.bg, fontFamily: FONT }}>
    <Title />
    <Peeker x={820} y={600} w={210} />
    <Card style={{ left: 46, right: 46, top: 600, height: 640, display: "flex", flexDirection: "column", justifyContent: "center", padding: "0 56px" }}>
      <div style={{ fontSize: 64, fontWeight: 800, color: C.ink, lineHeight: 1.45, whiteSpace: "nowrap" }}>
        你同意<span style={{ color: C.red }}>“快乐也会传染”</span><br />这种说法吗？<br />请说说你的看法和理由。
      </div>
      <div style={{ fontSize: 38, color: C.green, marginTop: 34, fontFamily: SANS, lineHeight: 1.35 }}>{QT(lang)}</div>
    </Card>
    <Chrome n={0} lang={lang} />
  </AbsoluteFill>
);

/* ---------- Cảnh 2: mindmap — chỉ tiếng Trung (luận điểm + ví dụ), không dịch, không cụm từ ---------- */
export const Branch: React.FC<{ i: number; y: number; idea: string; ex?: string }> = ({ i, y, idea, ex }) => {
  const s = SEC[i];
  return (
    <>
      <div style={{ position: "absolute", left: 100, top: y + 28, width: 60, height: 0, borderTop: `5px dashed ${s.c}` }} />
      <div style={{ position: "absolute", left: 74, top: y + 2, width: 52, height: 52, borderRadius: "50%", background: s.c, color: "#fff", fontSize: 30, display: "flex", alignItems: "center", justifyContent: "center" }}>★</div>
      <div style={{ position: "absolute", left: 170, top: y, width: 660 }}>
        <div style={{ display: "inline-block", background: s.c, color: "#fff", fontSize: 36, fontWeight: 800, borderRadius: 12, padding: "4px 26px" }}>{s.zh}</div>
        <div style={{ marginTop: 12, background: s.tint, borderRadius: 18, padding: "16px 26px", color: s.c, fontSize: 44, fontWeight: 800, lineHeight: 1.3 }}>
          {idea}
          {ex && <div style={{ fontSize: 31, fontWeight: 500, color: C.ink, marginTop: 8, lineHeight: 1.4 }}>{ex}</div>}
        </div>
      </div>
    </>
  );
};
export const S2: React.FC<{ lang: Lang }> = ({ lang }) => (
  <AbsoluteFill style={{ background: C.bg, fontFamily: FONT }}>
    <Title />
    <div style={{ position: "absolute", left: 170, width: 680, top: 200, height: 130, borderRadius: 26, background: "#E4ECFA", border: "5px solid #3A6EBE", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 58, fontWeight: 800, color: "#2B57A0" }}>分享快乐的方式</div>
    <div style={{ position: "absolute", left: 100, top: 330, width: 0, height: 1330, borderLeft: `5px dashed ${C.line}` }} />
    <Branch i={0} y={370} idea="每个人都有自己的方式" ex="例：升职了" />
    <Branch i={1} y={620} idea="第一时间打电话给爸妈" ex="亲戚很快知道，爸妈为我骄傲" />
    <Branch i={2} y={870} idea="告诉最好的朋友" ex="一起出去庆祝" />
    <Branch i={3} y={1120} idea="发一篇帖子" ex="分享努力的过程，传递正能量" />
    <Branch i={4} y={1370} idea="幸福在于有人陪你开心" ex="快乐加倍，世界更温暖" />
    <Standing right={20} feet={1750} h={440} />
    <Chrome n={1} lang={lang} />
  </AbsoluteFill>
);

/* ---------- Cảnh 3: cụm đáng học — chỉ cụm khó & ngắn; pinyin chỉ khi khó đọc ---------- */
export const S3: React.FC<{ lang: Lang }> = ({ lang }) => {
  const list = [PH.cyd, PH.dll, PH.bzbj, PH.pbjd, PH.crj, PH.znl];
  return (
    <AbsoluteFill style={{ background: C.bg, fontFamily: FONT }}>
      <Title sub={t(lang, "Phrases to learn", "Cụm đáng học")} />
      {list.map((p, i) => (
        <Card key={p.han} style={{ left: 46, right: 46, top: 210 + i * 230, height: 200, display: "flex", alignItems: "center", gap: 30, padding: "0 40px", borderRadius: 28 }}>
          <div style={{ fontSize: p.han.length > 6 ? 54 : 70, fontWeight: 800, color: C.red, lineHeight: 1.15, width: 470, flexShrink: 0, whiteSpace: "nowrap" }}>{p.han}</div>
          <div style={{ display: "flex", flexDirection: "column", lineHeight: 1.25 }}>
            {p.py && <div style={{ fontSize: 28, color: C.sub }}>{p.py}</div>}
            <div style={{ fontSize: 34, color: C.green, fontFamily: SANS, marginTop: 4 }}>{lang === "vi" ? p.vi : p.en}</div>
          </div>
        </Card>
      ))}
      <Chrome n={2} lang={lang} />
    </AbsoluteFill>
  );
};

/* ---------- Cảnh 4: video + phụ đề kiểu phim (tối đa 2 câu, mỗi câu 1 dòng: Hán trên, dịch dưới) ---------- */
const Sub: React.FC<{ han: string; tr: string; dim?: boolean; hl?: string }> = ({ han, tr, dim, hl }) => {
  const i = hl ? han.indexOf(hl) : -1;
  return (
    <div style={{ opacity: dim ? 0.4 : 1, textAlign: "center", whiteSpace: "nowrap" }}>
      <div style={{ fontSize: dim ? 46 : 62, fontWeight: 700, color: C.ink, lineHeight: 1.3 }}>
        {i >= 0 ? <>{han.slice(0, i)}<span style={{ color: C.red, fontWeight: 800 }}>{hl}</span>{han.slice(i + hl!.length)}</> : han}
      </div>
      <div style={{ fontSize: dim ? 29 : 36, color: C.green, marginTop: 8, fontFamily: SANS, lineHeight: 1.3 }}>{tr}</div>
    </div>
  );
};
export const S4: React.FC<{ lang: Lang }> = ({ lang }) => {
  const p = PH.bzbj;
  return (
    <AbsoluteFill style={{ background: C.bg, fontFamily: FONT }}>
      <Title />
      {/* câu hỏi: to + đậm, ngắt 2 dòng theo ý */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 170, fontSize: 46, fontWeight: 800, color: C.ink, textAlign: "center", lineHeight: 1.35, whiteSpace: "nowrap" }}>
        你同意“快乐也会传染”这种说法吗？<br />请说说你的看法和理由。
      </div>
      {/* khung video minh hoạ */}
      <Peeker x={880} y={430} w={170} />
      <div style={{ position: "absolute", left: 46, right: 46, top: 430, height: 560, borderRadius: 36, background: "#E3F2E9", border: `4px dashed ${C.green}`, display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column", color: C.green, fontFamily: SANS, gap: 8, textAlign: "center", padding: "0 40px" }}>
        <div style={{ fontSize: 60 }}>🎬</div>
        <div style={{ fontSize: 32 }}>{t(lang, "Illustration video for this part (AI-generated or free stock)", "Video minh hoạ cho phần này (AI gen hoặc stock free)")}</div>
        <div style={{ fontSize: 26, opacity: 0.8 }}>{t(lang, "e.g. coming home, family laughing together", "VD: về nhà, cả nhà cười với nhau")}</div>
      </div>
      {/* phụ đề: câu trước (mờ) + câu đang đọc; ngắt theo dấu phẩy để vừa 1 dòng */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 1060, display: "flex", flexDirection: "column", gap: 44 }}>
        <Sub dim han="首先，身边多一个快乐的人，" tr={t(lang, "First, one more happy person around you,", "Trước hết, bên cạnh có thêm một người vui vẻ,")} />
        <Sub hl="不知不觉" han="你也会不知不觉地跟着笑起来，" tr={t(lang, "you'll smile along without realizing it,", "bạn cũng bất giác cười theo,")} />
      </div>
      {/* thẻ cụm đang đọc */}
      <Card style={{ left: 240, right: 240, top: 1470, height: 210, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", textAlign: "center", borderRadius: 26 }}>
        <Tag>重点词</Tag>
        <div style={{ fontSize: 62, fontWeight: 800, color: C.red, lineHeight: 1.15 }}>{p.han}</div>
        <div style={{ fontSize: 26, color: C.sub, marginTop: 2 }}>{p.py} · <span style={{ color: C.green, fontFamily: SANS }}>{lang === "vi" ? p.vi : p.en}</span></div>
      </Card>
      <Chrome n={3} lang={lang} />
    </AbsoluteFill>
  );
};
