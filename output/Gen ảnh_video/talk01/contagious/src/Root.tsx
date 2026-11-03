import { Composition } from "remotion";
import { Story, FPS, TOTAL } from "./Story";
import { Cover } from "./Cover";

export const Root = () => (
  <>
    <Composition id="Story" component={Story} width={1080} height={1920} fps={FPS} durationInFrames={TOTAL} />
    <Composition id="Cover" component={Cover} width={1080} height={1440} fps={FPS} durationInFrames={1} />
  </>
);
