import { createHash } from "node:crypto";
import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const repoRoot = path.resolve(siteRoot, "..", "..");
export const entriesDirectory = path.join(
  repoRoot,
  "catalog",
  "public-field-notes",
  "entries",
);

export const activityKinds = new Set([
  "started",
  "exact-check",
  "independent-audit",
  "negative-result",
  "scoped-package",
  "correction",
  "withdrawal",
  "handoff",
]);

export const typedStatuses = new Set([
  "exploratory",
  "scoped-repository-evidence",
  "negative-result",
]);

const allowedKeys = new Set([
  "activity_kind",
  "agent",
  "artifacts",
  "corrects_entry",
  "entry_id",
  "global_status",
  "lane",
  "nonclaim",
  "recorded_at",
  "schema_version",
  "scope",
  "summary",
  "tags",
  "typed_status",
]);

const immutableArtifact =
  /^https:\/\/github\.com\/YesterdaysLemon\/krenn-gu-research\/(?:commit\/[0-9a-f]{40}|blob\/[0-9a-f]{40}\/[A-Za-z0-9._~!$&'()*+,;=:@%/-]+)(?:#[A-Za-z0-9._~!$&'()*+,;=:@%/-]+)?$/;
const pullRequestArtifact =
  /^https:\/\/github\.com\/YesterdaysLemon\/krenn-gu-research\/pull\/[1-9][0-9]*$/;

function sortedValue(value) {
  if (Array.isArray(value)) return value.map(sortedValue);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, sortedValue(value[key])]),
    );
  }
  return value;
}

export function canonicalJson(value) {
  return JSON.stringify(sortedValue(value));
}

export function renderEntry(entry) {
  return `${JSON.stringify(sortedValue(entry), null, 2)}\n`;
}

export function entryIdFor(entry) {
  const payload = { ...entry };
  delete payload.entry_id;
  return createHash("sha256").update(canonicalJson(payload), "utf8").digest("hex");
}

export function prepareEntry(draft, now = new Date()) {
  const recordedAt =
    draft.recorded_at ?? now.toISOString().replace(/\.\d{3}Z$/, "Z");
  const entry = sortedValue({ ...draft, recorded_at: recordedAt });
  delete entry.entry_id;
  entry.entry_id = entryIdFor(entry);
  return sortedValue(entry);
}

function publicText(value, name, { min = 1, max = 600 } = {}) {
  if (typeof value !== "string") return `${name} must be a string`;
  const length = value.trim().length;
  if (length < min || length > max) {
    return `${name} must contain ${min}-${max} non-whitespace characters`;
  }
  return null;
}

function validateArtifact(artifact, index) {
  const problems = [];
  if (!artifact || typeof artifact !== "object" || Array.isArray(artifact)) {
    return [`artifacts[${index}] must be an object`];
  }
  const keys = Object.keys(artifact).sort().join(",");
  if (keys !== "kind,label,url") {
    problems.push(`artifacts[${index}] must contain exactly kind, label, and url`);
  }
  const labelProblem = publicText(artifact.label, `artifacts[${index}].label`, {
    max: 100,
  });
  if (labelProblem) problems.push(labelProblem);
  if (!new Set(["commit", "blob", "pull-request"]).has(artifact.kind)) {
    problems.push(`artifacts[${index}].kind is not allowed`);
  }
  if (typeof artifact.url !== "string") {
    problems.push(`artifacts[${index}].url must be a string`);
  } else if (artifact.kind === "pull-request") {
    if (!pullRequestArtifact.test(artifact.url)) {
      problems.push(`artifacts[${index}] is not a repository pull-request URL`);
    }
  } else if (!immutableArtifact.test(artifact.url)) {
    problems.push(`artifacts[${index}] must pin a commit or blob at a commit`);
  }
  return problems;
}

export function validateEntry(entry, knownEntries = new Map()) {
  const problems = [];
  if (!entry || typeof entry !== "object" || Array.isArray(entry)) {
    return ["entry must be an object"];
  }

  const unexpectedKeys = Object.keys(entry).filter((key) => !allowedKeys.has(key));
  if (unexpectedKeys.length) {
    problems.push(`unexpected fields: ${unexpectedKeys.sort().join(", ")}`);
  }
  for (const key of allowedKeys) {
    if (!(key in entry)) problems.push(`missing field: ${key}`);
  }

  if (entry.schema_version !== 1) problems.push("schema_version must equal 1");
  if (entry.global_status !== "UNRESOLVED") {
    problems.push("global_status must equal UNRESOLVED");
  }
  if (!activityKinds.has(entry.activity_kind)) {
    problems.push(`activity_kind ${JSON.stringify(entry.activity_kind)} is not allowed`);
  }
  if (!typedStatuses.has(entry.typed_status)) {
    problems.push(`typed_status ${JSON.stringify(entry.typed_status)} is not allowed`);
  }
  const negativeKind = entry.activity_kind === "negative-result";
  const negativeStatus = entry.typed_status === "negative-result";
  if (negativeKind !== negativeStatus) {
    problems.push(
      "activity_kind and typed_status must both be negative-result or both be non-negative",
    );
  }
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(entry.recorded_at ?? "")) {
    problems.push("recorded_at must be an ISO-8601 UTC timestamp at second precision");
  } else if (Number.isNaN(Date.parse(entry.recorded_at))) {
    problems.push("recorded_at is not a real timestamp");
  }

  if (!entry.agent || typeof entry.agent !== "object" || Array.isArray(entry.agent)) {
    problems.push("agent must be an object");
  } else {
    if (Object.keys(entry.agent).sort().join(",") !== "name,role") {
      problems.push("agent must contain exactly name and role");
    }
    for (const key of ["name", "role"]) {
      const problem = publicText(entry.agent[key], `agent.${key}`, { max: 100 });
      if (problem) problems.push(problem);
    }
  }

  for (const [name, max] of [
    ["lane", 140],
    ["summary", 280],
    ["scope", 600],
    ["nonclaim", 600],
  ]) {
    const problem = publicText(entry[name], name, { max });
    if (problem) problems.push(problem);
  }
  if (
    negativeStatus &&
    /\b(?:failed|failure|timed[ -]?out|timeout|inconclusive)\b/i.test(
      `${entry.summary ?? ""} ${entry.scope ?? ""}`,
    )
  ) {
    problems.push(
      "negative-result is for a committed scoped exact no-go, not a failed, timed-out, or inconclusive run",
    );
  }

  if (!Array.isArray(entry.tags) || entry.tags.length > 8) {
    problems.push("tags must be an array with at most 8 entries");
  } else {
    for (const tag of entry.tags) {
      if (typeof tag !== "string" || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(tag)) {
        problems.push(`invalid public tag: ${JSON.stringify(tag)}`);
      }
    }
    if (new Set(entry.tags).size !== entry.tags.length) {
      problems.push("tags must be unique");
    }
  }

  if (!Array.isArray(entry.artifacts) || entry.artifacts.length > 4) {
    problems.push("artifacts must be an array with at most 4 entries");
  } else {
    entry.artifacts.forEach((artifact, index) => {
      problems.push(...validateArtifact(artifact, index));
    });
    const immutableCount = entry.artifacts.filter((artifact) =>
      new Set(["commit", "blob"]).has(artifact?.kind),
    ).length;
    const hasPullRequest = entry.artifacts.some(
      (artifact) => artifact?.kind === "pull-request",
    );
    if (hasPullRequest && immutableCount === 0) {
      problems.push("a pull-request link is supplemental and needs an immutable artifact");
    }
    if (
      new Set(["scoped-repository-evidence", "negative-result"]).has(entry.typed_status) &&
      immutableCount === 0
    ) {
      problems.push(`${entry.typed_status} requires an immutable committed artifact`);
    }
  }

  const isCorrection = new Set(["correction", "withdrawal"]).has(entry.activity_kind);
  if (isCorrection && !/^[0-9a-f]{64}$/.test(entry.corrects_entry ?? "")) {
    problems.push(`${entry.activity_kind} must name a valid corrects_entry`);
  }
  if (!isCorrection && entry.corrects_entry !== null) {
    problems.push("only correction or withdrawal entries may set corrects_entry");
  }
  if (entry.corrects_entry === entry.entry_id) {
    problems.push("an entry cannot correct itself");
  }
  if (entry.corrects_entry && knownEntries.size) {
    const corrected = knownEntries.get(entry.corrects_entry);
    if (!corrected) {
      problems.push(`corrects_entry ${entry.corrects_entry} does not exist`);
    } else if (Date.parse(corrected.recorded_at) >= Date.parse(entry.recorded_at)) {
      problems.push("a correction or withdrawal must be recorded after its target");
    }
  }

  if (!/^[0-9a-f]{64}$/.test(entry.entry_id ?? "")) {
    problems.push("entry_id must be a lowercase SHA-256 digest");
  } else if (entry.entry_id !== entryIdFor(entry)) {
    problems.push("entry_id does not match the canonical entry payload");
  }

  const serialized = JSON.stringify(entry);
  const sensitivePatterns = [
    [/[A-Za-z]:\\/, "local Windows path"],
    [/\\\\[^\\]/, "UNC path"],
    [/\b(?:PID|process id)\s*[:#]?\s*\d+/i, "process identifier"],
    [/\b(?:task|thread)[ _-]?id\b/i, "internal task identifier label"],
    [/\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/i, "internal UUID"],
  ];
  for (const [pattern, label] of sensitivePatterns) {
    if (pattern.test(serialized)) problems.push(`entry contains a ${label}`);
  }
  return problems;
}

export async function loadFieldNotes(directory = entriesDirectory) {
  const names = (await readdir(directory).catch((error) => {
    if (error.code === "ENOENT") return [];
    throw error;
  }))
    .filter((name) => name.endsWith(".json"))
    .sort();
  const parsed = [];
  for (const name of names) {
    const raw = await readFile(path.join(directory, name), "utf8");
    let entry;
    try {
      entry = JSON.parse(raw);
    } catch (error) {
      throw new Error(`${name}: invalid JSON: ${error.message}`);
    }
    const problems = validateEntry(entry);
    if (name !== `${entry.entry_id}.json`) {
      problems.push("filename must equal <entry_id>.json");
    }
    if (raw !== renderEntry(entry)) {
      problems.push("file must use canonical sorted pretty JSON plus one trailing newline");
    }
    if (problems.length) throw new Error(`${name}: ${problems.join("; ")}`);
    parsed.push(entry);
  }

  const byId = new Map(parsed.map((entry) => [entry.entry_id, entry]));
  if (byId.size !== parsed.length) throw new Error("duplicate field-note entry_id");
  for (const entry of parsed) {
    const problems = validateEntry(entry, byId);
    if (problems.length) throw new Error(`${entry.entry_id}: ${problems.join("; ")}`);
  }
  return parsed.sort(
    (left, right) =>
      right.recorded_at.localeCompare(left.recorded_at) ||
      right.entry_id.localeCompare(left.entry_id),
  );
}

export function projectFieldNotes(entries) {
  return {
    schemaVersion: 1,
    globalStatus: "UNRESOLVED",
    entries,
  };
}
