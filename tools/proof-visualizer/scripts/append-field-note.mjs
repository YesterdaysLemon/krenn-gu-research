import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import {
  entriesDirectory,
  loadFieldNotes,
  prepareEntry,
  renderEntry,
  validateEntry,
} from "./field-notes.mjs";

function valueAfter(flag) {
  const index = process.argv.indexOf(flag);
  if (index < 0) return null;
  const value = process.argv[index + 1];
  if (!value || value.startsWith("--")) throw new Error(`${flag} needs a value`);
  return value;
}

const inputPath = valueAfter("--input");
const inlineJson = valueAfter("--json");
if (Boolean(inputPath) === Boolean(inlineJson)) {
  throw new Error("provide exactly one of --input <draft.json> or --json <object>");
}

const draftText = inputPath ? await readFile(inputPath, "utf8") : inlineJson;
const draft = JSON.parse(draftText);
const existing = await loadFieldNotes();
const byId = new Map(existing.map((entry) => [entry.entry_id, entry]));
const entry = prepareEntry(draft);
const problems = validateEntry(entry, byId);
if (problems.length) throw new Error(problems.join("; "));

const rendered = renderEntry(entry);
if (process.argv.includes("--dry-run")) {
  process.stdout.write(rendered);
} else {
  await mkdir(entriesDirectory, { recursive: true });
  const destination = path.join(entriesDirectory, `${entry.entry_id}.json`);
  await writeFile(destination, rendered, { encoding: "utf8", flag: "wx" });
  console.log(`Appended ${entry.entry_id}`);
}
