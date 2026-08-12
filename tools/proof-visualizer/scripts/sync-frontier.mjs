import { execFileSync } from "node:child_process";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseFrontier } from "./frontier-parser.mjs";

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repoRoot = path.resolve(siteRoot, "..", "..");
const outputPath = path.join(siteRoot, "app", "data", "frontier.generated.json");

function git(...args) {
  return execFileSync("git", ["-C", repoRoot, ...args], {
    encoding: "utf8",
  }).trim();
}

function repositoryUrl() {
  const remote = git("remote", "get-url", "origin")
    .replace(/\.git$/, "")
    .replace(/^git@github\.com:/, "https://github.com/");
  return remote;
}

const [frontier, ledgerText] = await Promise.all([
  readFile(path.join(repoRoot, "docs", "current-frontier.md"), "utf8"),
  readFile(path.join(repoRoot, "catalog", "theorem-ledger.json"), "utf8"),
]);
const sourceCommit = git(
  "log",
  "-1",
  "--format=%H",
  "HEAD",
  "--",
  "docs/current-frontier.md",
  "catalog/theorem-ledger.json",
);
const data = parseFrontier(frontier, JSON.parse(ledgerText), {
  repoUrl: repositoryUrl(),
  sourceCommit,
  sourceDate: git("show", "-s", "--format=%cI", sourceCommit),
});
const rendered = `${JSON.stringify(data, null, 2)}\n`;

if (process.argv.includes("--check")) {
  const existing = await readFile(outputPath, "utf8").catch(() => "");
  if (existing !== rendered) {
    console.error("frontier.generated.json is stale; run npm run data:sync");
    process.exitCode = 1;
  }
} else {
  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, rendered, "utf8");
  console.log(
    `Synced ${data.counts.total} nodes and ${data.counts.edges} typed edges from ${sourceCommit.slice(0, 8)}.`,
  );
}
