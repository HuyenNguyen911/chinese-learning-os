import { Composition } from "remotion";
import words from "../words.json";
import { BodyParts, FPS, INTRO, PER_WORD, OUTRO } from "./BodyParts";

export const Root = () => (
  <Composition
    id="BodyParts"
    component={BodyParts}
    width={1080}
    height={1920}
    fps={FPS}
    durationInFrames={INTRO + words.length * PER_WORD + OUTRO}
  />
);
