// Chromium Remotion tự tải về hay lỗi EFTYPE trên Windows -> dùng Chrome/Edge có sẵn của máy nếu tìm thấy.
import { Config } from "@remotion/cli/config";
import { existsSync } from "fs";

const candidates = [
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
];
const browser = candidates.find((p) => existsSync(p));
if (browser) Config.setBrowserExecutable(browser);
