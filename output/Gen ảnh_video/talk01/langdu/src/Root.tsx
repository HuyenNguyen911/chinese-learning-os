import React from "react";
import { Composition } from "remotion";
import { Read, TOTAL, FPS } from "./Read";

export const Root: React.FC = () => (
  <>
    <Composition id="Read" component={Read} durationInFrames={TOTAL} fps={FPS} width={1080} height={1920} defaultProps={{ lang: "en" as const }} />
    <Composition id="ReadVI" component={Read} durationInFrames={TOTAL} fps={FPS} width={1080} height={1920} defaultProps={{ lang: "vi" as const }} />
  </>
);
