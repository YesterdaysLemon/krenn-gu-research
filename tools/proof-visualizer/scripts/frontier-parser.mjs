import path from "node:path";

const STATUS_MARKERS = {
  pruned: /\b(refuted|withdrawn|superseded)\b/i,
  growing: /\b(unresolved|open|conditional|partial|pending)\b|boundary-limited/i,
  established: /\b(proved|excluded|detected)\b|necessary and sufficient/i,
};

function section(markdown, heading, nextHeading) {
  const start = markdown.indexOf(heading);
  if (start < 0) return "";
  const bodyStart = start + heading.length;
  const end = nextHeading ? markdown.indexOf(nextHeading, bodyStart) : -1;
  return markdown.slice(bodyStart, end < 0 ? undefined : end);
}

function splitTableRow(line) {
  const trimmed = line.trim();
  if (!trimmed.startsWith("|") || !trimmed.endsWith("|")) return [];

  const cells = [];
  let current = "";
  let inCode = false;
  for (const char of trimmed.slice(1, -1)) {
    if (char === "`") inCode = !inCode;
    if (char === "|" && !inCode) {
      cells.push(current.trim());
      current = "";
    } else {
      current += char;
    }
  }
  cells.push(current.trim());
  return cells;
}

function plain(markdown) {
  return markdown
    .replace(/<br\s*\/?>/gi, " · ")
    .replace(/\[([^\]]+)]\([^)]+\)/g, "$1")
    .replace(/[*_`]/g, "")
    .replace(/&ge;/g, "≥")
    .replace(/&le;/g, "≤")
    .replace(/\s+/g, " ")
    .trim();
}

function ownerLinks(markdown) {
  return [...markdown.matchAll(/\[([^\]]+)]\(([^)]+)\)/g)].map(
    ([, label, href]) => ({ label: plain(label), href }),
  );
}

function normalizeOwnerLink(link, repoUrl, sourceCommit) {
  if (/^https?:\/\//i.test(link.href)) {
    return { ...link, document: null, url: link.href };
  }

  const [relativePath, anchor] = link.href.split("#", 2);
  const document = path.posix.normalize(path.posix.join("docs", relativePath));
  const url = `${repoUrl}/blob/${sourceCommit}/${document}${anchor ? `#${anchor}` : ""}`;
  return { ...link, document, anchor: anchor || null, url };
}

function mermaidLabels(markdown) {
  const match = markdown.match(/```mermaid\s*([\s\S]*?)```/i);
  if (!match) return new Map();

  const labels = new Map();
  for (const line of match[1].split(/\r?\n/)) {
    const node = line.match(/^\s*([A-Z][A-Z0-9]*)\["(.+)"\]\s*$/);
    if (!node) continue;
    labels.set(node[1], plain(node[2]));
  }
  return labels;
}

export function classifyStatus(status) {
  if (STATUS_MARKERS.pruned.test(status)) return "pruned";
  if (STATUS_MARKERS.growing.test(status)) return "growing";
  if (STATUS_MARKERS.established.test(status)) return "established";
  return "growing";
}

function ledgerEvidence(links, ledgerByDocument) {
  const records = links
    .map((link) => (link.document ? ledgerByDocument.get(link.document) : null))
    .filter(Boolean);

  return {
    indexedDocuments: records.length,
    linkedDocuments: links.filter((link) => link.document).length,
    ledgerStatuses: [...new Set(records.map((entry) => entry.status))].sort(),
    primaryVerifierCount: records.filter((entry) => entry.primary_verifier).length,
    independentAuditCount: records.filter((entry) => entry.independent_audit).length,
  };
}

export function parseFrontier(
  markdown,
  ledger,
  { repoUrl, sourceCommit, sourceDate },
) {
  const labels = mermaidLabels(markdown);
  const ledgerEntries = Array.isArray(ledger?.entries) ? ledger.entries : [];
  const ledgerByDocument = new Map(
    ledgerEntries.map((entry) => [entry.document, entry]),
  );

  const nodeSection = section(
    markdown,
    "## Node key",
    "## Typed-edge table",
  );
  const nodes = [];
  for (const line of nodeSection.split(/\r?\n/)) {
    const cells = splitTableRow(line);
    if (cells.length !== 3) continue;
    const idMatch = cells[0].match(/^`([A-Z][A-Z0-9]*)`$/);
    if (!idMatch) continue;

    const id = idMatch[1];
    const links = ownerLinks(cells[2]).map((link) =>
      normalizeOwnerLink(link, repoUrl, sourceCommit),
    );
    const exactStatus = plain(cells[1]);
    const diagramLabel = labels.get(id) ?? null;
    const title = diagramLabel?.split(" · ")[0] ?? links[0]?.label ?? id;

    nodes.push({
      id,
      title,
      diagramLabel,
      exactStatus,
      tone: classifyStatus(`${diagramLabel ?? ""} ${exactStatus}`),
      owners: links,
      evidence: ledgerEvidence(links, ledgerByDocument),
    });
  }

  const nodeIds = new Set(nodes.map((node) => node.id));
  const edgeSection = section(
    markdown,
    "## Typed-edge table",
    "## Smallest positive next obligations",
  );
  const edges = [];
  const unknownEdgeNodeIds = new Set();
  let rowIndex = 0;
  for (const line of edgeSection.split(/\r?\n/)) {
    const cells = splitTableRow(line);
    if (cells.length !== 4) continue;
    const sources = [...cells[0].matchAll(/`([A-Z][A-Z0-9]*)`/g)].map(
      (match) => match[1],
    );
    const targets = [...cells[2].matchAll(/`([A-Z][A-Z0-9]*)`/g)].map(
      (match) => match[1],
    );
    if (!sources.length || !targets.length) continue;

    for (const id of [...sources, ...targets]) {
      if (!nodeIds.has(id)) unknownEdgeNodeIds.add(id);
    }
    for (const source of sources) {
      for (const target of targets) {
        if (!nodeIds.has(source) || !nodeIds.has(target)) continue;
        edges.push({
          id: `${source}-${target}-${rowIndex}`,
          source,
          target,
          relation: plain(cells[1]),
          note: plain(cells[3]),
        });
      }
    }
    rowIndex += 1;
  }

  const degree = new Map(nodes.map((node) => [node.id, 0]));
  for (const edge of edges) {
    degree.set(edge.source, (degree.get(edge.source) ?? 0) + 1);
    degree.set(edge.target, (degree.get(edge.target) ?? 0) + 1);
  }

  const counts = { established: 0, growing: 0, pruned: 0 };
  for (const node of nodes) counts[node.tone] += 1;

  const globalMatch = markdown.match(/global Krenn[^\n]*?\*\*([A-Z]+)\*\*/i);
  return {
    schemaVersion: 1,
    programme: "Krenn–Gu conjecture programme",
    globalStatus: globalMatch?.[1]?.toUpperCase() ?? "UNKNOWN",
    source: {
      repository: repoUrl,
      commit: sourceCommit,
      committedAt: sourceDate,
      frontierDocument: `${repoUrl}/blob/${sourceCommit}/docs/current-frontier.md`,
      ledgerDocument: `${repoUrl}/blob/${sourceCommit}/catalog/theorem-ledger.json`,
      ledgerRole: ledger?.ledger_role ?? "unknown",
      ledgerCompleteness: ledger?.completeness ?? "unknown",
    },
    counts: { total: nodes.length, edges: edges.length, ...counts },
    health: {
      missingFromMermaid: nodes
        .filter((node) => !labels.has(node.id))
        .map((node) => node.id),
      missingFromNodeKey: [...labels.keys()].filter((id) => !nodeIds.has(id)),
      unlinkedNodeIds: nodes
        .filter((node) => (degree.get(node.id) ?? 0) === 0)
        .map((node) => node.id),
      unknownEdgeNodeIds: [...unknownEdgeNodeIds].sort(),
    },
    nodes,
    edges,
  };
}
