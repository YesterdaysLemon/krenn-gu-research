import assert from "node:assert/strict";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  canonicalJson,
  loadFieldNotes,
  prepareEntry,
  renderEntry,
  validateEntry,
} from "../scripts/field-notes.mjs";

function draft(overrides = {}) {
  return {
    schema_version: 1,
    recorded_at: "2026-08-31T05:32:21Z",
    agent: { name: "Lark", role: "Krenn–Gu PR wing" },
    lane: "public field notes",
    activity_kind: "started",
    typed_status: "exploratory",
    summary: "Lark began a public activity journal for the agent ecology.",
    scope: "A presentation and provenance surface for public-safe agent updates.",
    nonclaim: "This does not change any theorem, frontier edge, or global status.",
    artifacts: [],
    corrects_entry: null,
    tags: ["ecology", "field-notes"],
    global_status: "UNRESOLVED",
    ...overrides,
  };
}

test("canonical JSON recursively sorts object keys while preserving arrays", () => {
  assert.equal(
    canonicalJson({ z: [{ b: 2, a: 1 }], a: "first" }),
    '{"a":"first","z":[{"a":1,"b":2}]}',
  );
});

test("prepares a content-addressed, canonically rendered entry", () => {
  const entry = prepareEntry(draft());
  assert.match(entry.entry_id, /^[0-9a-f]{64}$/);
  assert.deepEqual(validateEntry(entry), []);
  assert.equal(renderEntry(entry), `${JSON.stringify(entry, null, 2)}\n`);
});

test("rejects status inflation, local identifiers, and PR-only evidence", () => {
  const resolved = prepareEntry(draft({ global_status: "RESOLVED" }));
  assert.ok(validateEntry(resolved).some((problem) => problem.includes("UNRESOLVED")));

  const candidate = prepareEntry(draft({ typed_status: "candidate" }));
  assert.ok(validateEntry(candidate).some((problem) => problem.includes("typed_status")));

  const localPath = prepareEntry(draft({ summary: "Checked C:\\private\\result.json." }));
  assert.ok(validateEntry(localPath).some((problem) => problem.includes("local Windows path")));

  const prOnly = prepareEntry(
    draft({
      typed_status: "scoped-repository-evidence",
      artifacts: [
        {
          kind: "pull-request",
          label: "PR #322",
          url: "https://github.com/YesterdaysLemon/krenn-gu-research/pull/322",
        },
      ],
    }),
  );
  assert.ok(validateEntry(prOnly).some((problem) => problem.includes("immutable")));
});

test("negative results are exact scoped records, never run outcomes", () => {
  const immutableArtifact = [
    {
      kind: "commit",
      label: "Pinned exact result",
      url: "https://github.com/YesterdaysLemon/krenn-gu-research/commit/49bb3308913135b8a093c88b79ce45de2bd76913",
    },
  ];
  const mismatched = prepareEntry(
    draft({
      activity_kind: "exact-check",
      typed_status: "negative-result",
      artifacts: immutableArtifact,
    }),
  );
  assert.ok(validateEntry(mismatched).some((problem) => problem.includes("must both")));

  const timedOut = prepareEntry(
    draft({
      activity_kind: "negative-result",
      typed_status: "negative-result",
      summary: "A timed-out computation did not find a witness.",
      artifacts: immutableArtifact,
    }),
  );
  assert.ok(validateEntry(timedOut).some((problem) => problem.includes("timed-out")));
});

test("loads only canonical hash-named entries and preserves correction history", async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), "kg-field-notes-"));
  try {
    const first = prepareEntry(draft());
    const correction = prepareEntry(
      draft({
        recorded_at: "2026-08-31T05:33:21Z",
        activity_kind: "correction",
        summary: "Lark clarified the scope of the public journal.",
        corrects_entry: first.entry_id,
      }),
    );
    await writeFile(path.join(directory, `${first.entry_id}.json`), renderEntry(first));
    await writeFile(
      path.join(directory, `${correction.entry_id}.json`),
      renderEntry(correction),
    );
    const entries = await loadFieldNotes(directory);
    assert.equal(entries.length, 2);
    assert.equal(entries[0].corrects_entry, first.entry_id);
    assert.equal(entries[1].entry_id, first.entry_id);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});
