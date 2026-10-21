import { Composition } from "remotion";
import words from "../words.json";
import { BodyParts, FPS, INTRO, SEQ_LEN, OUTRO } from "./BodyParts";

export const Root = () => (
  <Composition
    id="BodyParts"
    component={BodyParts}
    width={1080}
    height={1920}
    fps={FPS}
    durationInFrames={INTRO + SEQ_LEN + OUTRO}
  />
);
