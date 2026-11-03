import React from "react";
import { Composition } from "remotion";
import { S1, S2, S3, S4, W, H } from "./Frames";
import { Full, TOTAL, FPS } from "./Full";

const c = (id: string, comp: React.FC<{ lang: "en" | "vi" }>, lang: "en" | "vi") => (
  <Composition key={id} id={id} component={comp} durationInFrames={1} fps={30} width={W} height={H} defaultProps={{ lang }} />
);
export const Root: React.FC = () => (
  <>
    {c("S1", S1, "vi")}{c("S2", S2, "vi")}{c("S3", S3, "vi")}{c("S4", S4, "vi")}
    <Composition id="FullVI" component={Full} durationInFrames={TOTAL} fps={FPS} width={1080} height={1920} defaultProps={{ lang: "vi" as const }} />
    <Composition id="FullEN" component={Full} durationInFrames={TOTAL} fps={FPS} width={1080} height={1920} defaultProps={{ lang: "en" as const }} />
    {c("S1EN", S1, "en")}{c("S2EN", S2, "en")}{c("S3EN", S3, "en")}{c("S4EN", S4, "en")}
  </>
);
