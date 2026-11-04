import { Composition } from "remotion";
import { Clip, FPS, TOTAL } from "./Clip";

export const Root = () => (
  <Composition id="Clip" component={Clip} width={1080} height={1920} fps={FPS} durationInFrames={TOTAL} />
);
