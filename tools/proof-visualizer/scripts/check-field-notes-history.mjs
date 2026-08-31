import { execFileSync } from "node:child_process";
import { repoRoot } from "./field-notes.mjs";

const notesPath = "catalog/public-field-notes/entries";

function git(...args) {
  return execFileSync("git", ["-C", repoRoot, ...args], {
    encoding: "utf8",
  }).trim();
}

function option(flag) {
  const index = process.argv.indexOf(flag);
  if (index < 0) return null;
  const value = process.argv[index + 1];
  if (!value || value.startsWith("--")) throw new Error(`${flag} needs a value`);
  return value;
}

const base = option("--base");
const lines = [];
if (base) {
  lines.push(...git("diff", "--name-status", `${base}...HEAD`, "--", notesPath).split(/\r?\n/));
}
lines.push(...git("diff", "--name-status", "HEAD", "--", notesPath).split(/\r?\n/));
lines.push(...git("diff", "--cached", "--name-status", "HEAD", "--", notesPath).split(/\r?\n/));
for (const untracked of git("ls-files", "--others", "--exclude-standard", "--", notesPath).split(/\r?\n/)) {
  if (untracked) lines.push(`A\t${untracked}`);
}

const changes = [...new Set(lines.filter(Boolean))];
const violations = changes.filter((line) => !line.startsWith("A\t"));
if (violations.length) {
  console.error("Public field-note history is append-only; only added entry files are allowed:");
  for (const line of violations) console.error(`  ${line}`);
  process.exitCode = 1;
} else {
  console.log(
    `${changes.length} public field-note change${changes.length === 1 ? "" : "s"}; all are additions.`,
  );
}
