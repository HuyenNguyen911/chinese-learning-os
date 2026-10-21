import { Composition } from "remotion";
import { Poster, FPS, INTRO, SEQ_LEN, OUTRO } from "./Poster";

export const Root = () => (
  <Composition
    id="Poster"
    component={Poster}
    width={1080}
    height={1920}
    fps={FPS}
    durationInFrames={INTRO + SEQ_LEN + OUTRO}
  />
);
