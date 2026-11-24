// news-image-20261124 entrypoint: copy the pre-rendered front page to the
// grader's output directory, verifying it is a real 1024x1024 PNG under 1 MiB
// and byte-identical to the repository copy. Node 22, standard library only.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL("./entry.png", import.meta.url);
const data = readFileSync(src);

// PNG magic: 89 50 4E 47 0D 0A 1A 0A
const magic = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
for (let i = 0; i < magic.length; i++) {
  if (data[i] !== magic[i]) throw new Error("entry.png is not a PNG file");
}
if (data.length > 1048576) {
  throw new Error(`entry.png is ${data.length} bytes, over the 1 MiB cap`);
}
// IHDR: width at bytes 16-19, height at 20-23, big-endian.
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}
// PNG ends with a 12-byte IEND chunk.
const tail = data.subarray(data.length - 12);
if (tail.toString("latin1") !== "\0\0\0\0IEND\xaeB`\x82") {
  throw new Error("entry.png is missing a valid trailing IEND chunk");
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);

// Prove the copy: re-read it and byte-compare against the repository file.
const back = readFileSync(dest);
if (!back.equals(data)) throw new Error("copied entry.png differs from the source");
console.log(
  `wrote ${dest} (${back.length} bytes, 1024x1024 PNG, verified identical)`,
);
