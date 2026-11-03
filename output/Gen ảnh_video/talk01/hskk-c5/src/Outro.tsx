import React from "react";
import { AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

/* Đoạn kết dùng chung mọi video Talk series: hồ sơ kênh 瑾玄在练嘴 + nút Follow -> bàn tay chạm -> ✓ Followed
   (tiếng tick) -> tim bật lên (pop). Câu thoại cảm ơn + nhờ like/follow đọc bằng giọng 瑾玄 (public/audio/outro.wav).
   Đặt trong <Sequence from={...} durationInFrames={outroFrames(voiceSec)}>. Cần public/img/jx_avatar.png,
   public/sfx/{tap_click,tick_check,pop_bubble}.mp3. */
export const outroSec = (voiceSec: number) => Math.max(3.6, voiceSec + 1.0);
const FONT = '"Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif';
const TAP = 1.7, DONE = 1.85, HEART = 2.35;          // giây trong đoạn kết

export const Outro: React.FC<{ text: string; channel?: string; handle?: string }> = ({ text, channel = "瑾玄在练嘴", handle = "@瑾玄在练嘴" }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const ease = Easing.bezier(0.45, 0, 0.55, 1);
  const k = (a: number, b: number) => interpolate(t, [a, b], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const cardIn = spring({ frame: f, fps, config: { damping: 14 } });
  const done = t >= DONE;
  const press = t >= TAP && t < DONE + 0.1 ? 0.94 : 1;
  const handIn = k(1.0, TAP);
  const handOut = k(DONE + 0.2, DONE + 0.6);
  const heart = spring({ frame: f - Math.round(HEART * fps), fps, config: { damping: 9 } });
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: "rgba(255,251,242,0.94)", opacity: k(0, 0.3) }} />
      <Sequence from={Math.round(0.2 * fps)}><Audio src={staticFile("audio/outro.wav")} /></Sequence>
      <Sequence from={Math.round(TAP * fps)}><Audio src={staticFile("sfx/tap_click.mp3")} volume={0.6} /></Sequence>
      <Sequence from={Math.round(DONE * fps)}><Audio src={staticFile("sfx/tick_check.mp3")} volume={0.8} /></Sequence>
      <Sequence from={Math.round(HEART * fps)}><Audio src={staticFile("sfx/pop_bubble.mp3")} volume={0.5} /></Sequence>

      {/* câu thoại: rớt dòng theo ý (sau ～ / 。/ ！), mỗi dòng không tự gãy — tránh "cùng câu mà rớt 1 chữ" */}
      <div style={{ position: "absolute", left: 40, right: 40, top: 300, textAlign: "center", fontFamily: FONT, fontWeight: 800, fontSize: 46, lineHeight: 1.4, color: "#26231f", opacity: k(0.1, 0.4) }}>
        {text.split(/(?<=[～。！？])/).filter(Boolean).map((l, i) => <div key={i} style={{ whiteSpace: "nowrap" }}>{l}</div>)}
      </div>

      {/* thẻ hồ sơ */}
      <div style={{ position: "absolute", left: 110, right: 110, top: 760, height: 520, borderRadius: 48, background: "#fff", boxShadow: "0 16px 44px rgba(60,40,20,0.16)", transform: `scale(${0.85 + 0.15 * cardIn})`, opacity: cardIn, fontFamily: FONT }}>
        <div style={{ position: "absolute", left: 60, top: 60, width: 220, height: 220, borderRadius: "50%", overflow: "hidden", border: "6px solid #FE2C55" }}>
          <Img src={staticFile("img/jx_avatar.png")} style={{ position: "absolute", width: 480, height: 480, left: -130, top: -50 }} />
        </div>
        <div style={{ position: "absolute", left: 320, top: 92, fontSize: 62, fontWeight: 800, color: "#26231f" }}>{channel}</div>
        <div style={{ position: "absolute", left: 322, top: 182, fontSize: 34, color: "#8a8178" }}>{handle}</div>
        <div style={{ position: "absolute", left: 60, right: 60, top: 340, height: 120, borderRadius: 60, background: done ? "#E9E6E1" : "#FE2C55", color: done ? "#4a443d" : "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 54, fontWeight: 800, fontFamily: '"Segoe UI",sans-serif', transform: `scale(${press})` }}>
          {done ? "✓ Followed" : "Follow"}
        </div>
        {/* bàn tay chạm nút */}
        <div style={{ position: "absolute", left: 520, top: 400 + (1 - handIn) * 260 + handOut * 200, fontSize: 130, opacity: handIn * (1 - handOut), transform: `scale(${press})`, fontFamily: '"Segoe UI Emoji","Apple Color Emoji",sans-serif' }}>👆</div>
        {/* tim */}
        <div style={{ position: "absolute", right: 30, top: -70, fontSize: 140, transform: `scale(${heart}) rotate(${(1 - heart) * -30}deg)`, opacity: t >= HEART ? 1 : 0, fontFamily: '"Segoe UI Emoji","Apple Color Emoji",sans-serif' }}>❤️</div>
      </div>
    </AbsoluteFill>
  );
};
