import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { classifyStatus, parseFrontier } from "../scripts/frontier-parser.mjs";

test("projects exact status text into conservative bonsai tones", () => {
  assert.equal(classifyStatus("PROVED reduction"), "established");
  assert.equal(classifyStatus("proved normal form; exclusion open"), "growing");
  assert.equal(classifyStatus("PARTIAL / boundary-limited"), "growing");
  assert.equal(classifyStatus("REFUTED ROUTE"), "pruned");
});
test("parses the canonical node key and typed-edge table", async () => {
  const repoRoot = new URL("../../../", import.meta.url);
  const [frontier, ledgerText] = await Promise.all([
    readFile(new URL("docs/current-frontier.md", repoRoot), "utf8"),
    readFile(new URL("catalog/theorem-ledger.json", repoRoot), "utf8"),
  ]);
  const data = parseFrontier(frontier, JSON.parse(ledgerText), {
    repoUrl: "https://github.com/example/research",
    sourceCommit: "0123456789abcdef",
    sourceDate: "2026-08-11T00:00:00Z",
  });

  assert.equal(data.globalStatus, "UNRESOLVED");
  assert.ok(data.nodes.length > 40);
  assert.ok(data.edges.length > 40);
  assert.equal(data.health.unknownEdgeNodeIds.length, 0);
  assert.equal(data.nodes.find((node) => node.id === "U5")?.tone, "pruned");
  assert.equal(data.nodes.find((node) => node.id === "U7")?.tone, "growing");
  assert.equal(data.nodes.find((node) => node.id === "S1")?.tone, "established");
  assert.ok(data.nodes.some((node) => node.id === "U7G"));
  for (const edge of data.edges) {
    assert.ok(data.nodes.some((node) => node.id === edge.source));
    assert.ok(data.nodes.some((node) => node.id === edge.target));
  }
});
