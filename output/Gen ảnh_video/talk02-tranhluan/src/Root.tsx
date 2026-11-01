import { Composition } from "remotion";
import { Story, FPS, TOTAL } from "./Story";

export const Root = () => (
  <Composition id="Story" component={Story} width={1080} height={1920} fps={FPS} durationInFrames={TOTAL} />
);
