import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadFieldNotes, projectFieldNotes } from "./field-notes.mjs";

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outputPath = path.join(siteRoot, "app", "data", "field-notes.generated.json");
const data = projectFieldNotes(await loadFieldNotes());
const rendered = `${JSON.stringify(data, null, 2)}\n`;

if (process.argv.includes("--check")) {
  const existing = await readFile(outputPath, "utf8").catch(() => "");
  if (existing !== rendered) {
    console.error("field-notes.generated.json is stale; run npm run data:sync");
    process.exitCode = 1;
  }
} else {
  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, rendered, "utf8");
  console.log(`Synced ${data.entries.length} immutable public field notes.`);
}
