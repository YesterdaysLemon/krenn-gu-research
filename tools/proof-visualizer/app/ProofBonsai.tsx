"use client";

import dagre from "@dagrejs/dagre";
import {
  Background,
  BackgroundVariant,
  Controls,
  Handle,
  MarkerType,
  MiniMap,
  Position,
  ReactFlow,
  type Edge,
  type Node,
  type NodeProps,
  type ReactFlowInstance,
} from "@xyflow/react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type {
  BonsaiTone,
  FrontierData,
  FrontierEdge,
  FrontierNode,
} from "./frontier-types";

const NODE_WIDTH = 196;
const NODE_HEIGHT = 88;

const toneCopy: Record<
  BonsaiTone,
  { singular: string; plural: string; meaning: string }
> = {
  established: {
    singular: "Leaf",
    plural: "Leaves",
    meaning: "Established at the node’s stated scope",
  },
  growing: {
    singular: "Bud",
    plural: "Buds",
    meaning: "Contains an open, partial, conditional, or unresolved boundary",
  },
  pruned: {
    singular: "Scar",
    plural: "Scars",
    meaning: "A route or stronger argument has been refuted or retired",
  },
};

type BonsaiNodeData = {
  frontier: FrontierNode;
  selected: boolean;
};

type BonsaiFlowNode = Node<BonsaiNodeData, "bonsai">;

function BonsaiNode({ data }: NodeProps<BonsaiFlowNode>) {
  const { frontier, selected } = data;
  return (
    <div
      className={`bonsai-node bonsai-node--${frontier.tone}${selected ? " is-selected" : ""}`}
      aria-label={`${frontier.id}: ${frontier.title}. ${toneCopy[frontier.tone].meaning}`}
      title={`Inspect ${frontier.id}: ${frontier.title}`}
    >
      <Handle type="source" position={Position.Top} className="branch-handle" />
      <span className={`botanical-mark botanical-mark--${frontier.tone}`} aria-hidden="true" />
      <span className="node-copy">
        <span className="node-id">{frontier.id}</span>
        <span className="node-title">{frontier.title}</span>
      </span>
      <Handle type="target" position={Position.Bottom} className="branch-handle" />
    </div>
  );
}
const nodeTypes = { bonsai: BonsaiNode };

type MapScope = "neighborhood" | "all";

type LayoutPoint = { x: number; y: number };

function edgeTreatment(relation: string) {
  const lower = relation.toLowerCase();
  if (lower.includes("refutation") || lower.includes("insufficient")) {
    return { stroke: "#bb5a49", dash: "3 8" };
  }
  if (lower.includes("boundary") || lower.includes("open")) {
    return { stroke: "#c39548", dash: "8 8" };
  }
  if (lower.includes("special") || lower.includes("conditional")) {
    return { stroke: "#8c7453", dash: "4 5" };
  }
  return { stroke: "#6d5639", dash: undefined };
}

function primaryBranchIds(sourceNodes: FrontierNode[], sourceEdges: FrontierEdge[]) {
  const nodeIds = new Set(sourceNodes.map((node) => node.id));
  const indegree = new Map(sourceNodes.map((node) => [node.id, 0]));
  const outgoing = new Map(sourceNodes.map((node) => [node.id, [] as FrontierEdge[]]));

  for (const edge of sourceEdges) {
    if (!nodeIds.has(edge.source) || !nodeIds.has(edge.target)) continue;
    indegree.set(edge.target, (indegree.get(edge.target) ?? 0) + 1);
    outgoing.get(edge.source)?.push(edge);
  }
  for (const edges of outgoing.values()) {
    edges.sort(
      (left, right) =>
        left.target.localeCompare(right.target) || left.id.localeCompare(right.id),
    );
  }

  const roots = sourceNodes
    .filter((node) => (indegree.get(node.id) ?? 0) === 0)
    .map((node) => node.id)
    .sort((left, right) => {
      if (left === "G0") return -1;
      if (right === "G0") return 1;
      return left.localeCompare(right);
    });
  const starts = [...roots, ...sourceNodes.map((node) => node.id).sort()];
  const visited = new Set<string>();
  const primary = new Set<string>();

  for (const start of starts) {
    if (visited.has(start)) continue;
    visited.add(start);
    const queue = [start];
    for (let index = 0; index < queue.length; index += 1) {
      for (const edge of outgoing.get(queue[index]) ?? []) {
        if (visited.has(edge.target)) continue;
        visited.add(edge.target);
        primary.add(edge.id);
        queue.push(edge.target);
      }
    }
  }

  return primary;
}

function canopyProfile(progress: number) {
  if (progress <= 0.55) return 0.55 + (progress / 0.55) * 0.45;
  return 1 - ((progress - 0.55) / 0.45) * 0.44;
}

function shapeBonsaiCanopy(rawPoints: Map<string, LayoutPoint>) {
  const rows = new Map<number, Array<{ id: string; point: LayoutPoint }>>();
  for (const [id, point] of rawPoints) {
    const rank = Math.round(point.y);
    const row = rows.get(rank) ?? [];
    row.push({ id, point });
    rows.set(rank, row);
  }

  const orderedRows = [...rows.entries()].sort(([left], [right]) => right - left);
  const rootRowIndex = orderedRows.findIndex(([, row]) =>
    row.some(({ id }) => id === "G0"),
  );
  const canopyRows = orderedRows.flatMap(([rank, row], index) => {
    if (index !== rootRowIndex) return [[rank, row] as const];
    const rootCompanions = row.filter(({ id }) => id !== "G0");
    return rootCompanions.length ? [[rank, rootCompanions] as const] : [];
  });
  const largestRow = Math.max(1, ...canopyRows.map(([, row]) => row.length));
  const maximumCanopyWidth = (largestRow - 1) * (NODE_WIDTH + 38);
  const canopyBase = 1_080;
  const canopyHeight = Math.max(
    2_800,
    Math.max(0, canopyRows.length - 1) * (NODE_HEIGHT + 36),
  );
  const shaped = new Map<string, LayoutPoint>();

  canopyRows.forEach(([, unsortedRow], rowIndex) => {
    const row = [...unsortedRow].sort(
      (left, right) => left.point.x - right.point.x || left.id.localeCompare(right.id),
    );
    const progress = canopyRows.length <= 1 ? 0 : rowIndex / (canopyRows.length - 1);
    const minimumWidth = Math.max(0, row.length - 1) * (NODE_WIDTH + 34);
    const maximumWidth = Math.max(0, row.length - 1) * (NODE_WIDTH + 420);
    const profiledWidth = maximumCanopyWidth * canopyProfile(progress);
    const width =
      row.length <= 1
        ? 0
        : Math.min(maximumWidth, Math.max(minimumWidth, profiledWidth));
    const centreBend =
      Math.sin(progress * Math.PI * 1.35) * 620 -
      Math.sin(progress * Math.PI * 2.4) * 210;
    const rowY = -canopyBase - progress * canopyHeight;

    row.forEach(({ id }, nodeIndex) => {
      const normalized =
        row.length <= 1 ? 0 : nodeIndex / (row.length - 1) - 0.5;
      const horizontal = normalized * width;
      shaped.set(id, {
        x: centreBend + horizontal,
        y: rowY - Math.pow(Math.abs(normalized) * 2, 1.5) * 34,
      });
    });
  });

  shaped.set("G0", { x: 0, y: 0 });
  return shaped;
}

function layoutGraph(
  sourceNodes: FrontierNode[],
  sourceEdges: FrontierEdge[],
  selectedId: string,
  mapScope: MapScope,
) {
  const graph = new dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));
  graph.setGraph({
    rankdir: "BT",
    ranksep: 106,
    nodesep: 34,
    edgesep: 20,
    marginx: 42,
    marginy: 58,
  });
  for (const node of sourceNodes) {
    graph.setNode(node.id, { width: NODE_WIDTH, height: NODE_HEIGHT });
  }
  for (const edge of sourceEdges) graph.setEdge(edge.source, edge.target);
  dagre.layout(graph);

  const rawPoints = new Map<string, LayoutPoint>(
    sourceNodes.map((node) => {
      const point = graph.node(node.id) ?? { x: 0, y: 0 };
      return [node.id, { x: point.x, y: point.y }];
    }),
  );
  const layoutPoints =
    mapScope === "all" ? shapeBonsaiCanopy(rawPoints) : rawPoints;
  const primaryBranches = primaryBranchIds(sourceNodes, sourceEdges);

  const nodes: BonsaiFlowNode[] = sourceNodes.map((frontier) => {
    const point = layoutPoints.get(frontier.id) ?? { x: 0, y: 0 };
    return {
      id: frontier.id,
      type: "bonsai",
      position: {
        x: point.x - NODE_WIDTH / 2,
        y: point.y - NODE_HEIGHT / 2,
      },
      data: { frontier, selected: frontier.id === selectedId },
      draggable: false,
      selectable: true,
      sourcePosition: Position.Top,
      targetPosition: Position.Bottom,
      style: { width: NODE_WIDTH, height: NODE_HEIGHT },
      ariaLabel: `${frontier.id}: ${frontier.title}`,
    };
  });

  const edges: Edge[] = sourceEdges.map((edge) => {
    const treatment = edgeTreatment(edge.relation);
    const isPrimary = primaryBranches.has(edge.id);
    const isSelectedBranch = edge.source === selectedId || edge.target === selectedId;
    const wholeMap = mapScope === "all";
    const emphasized = !wholeMap || isPrimary || isSelectedBranch;
    return {
      ...edge,
      type: wholeMap ? "default" : "smoothstep",
      label: wholeMap ? undefined : edge.relation,
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: treatment.stroke,
        width: wholeMap ? 9 : 13,
        height: wholeMap ? 9 : 13,
      },
      style: {
        stroke: treatment.stroke,
        strokeWidth: wholeMap ? (isSelectedBranch ? 3.1 : isPrimary ? 1.65 : 0.55) : 2.2,
        strokeDasharray: treatment.dash,
        opacity: emphasized ? (isSelectedBranch ? 1 : 0.74) : 0.14,
        vectorEffect: wholeMap ? "non-scaling-stroke" : undefined,
      },
      zIndex: isSelectedBranch ? 3 : isPrimary ? 2 : 1,
      labelStyle: { fill: "#aa9c85", fontSize: 10, fontWeight: 650 },
      labelBgStyle: { fill: "#141812", fillOpacity: 0.9 },
      labelBgPadding: [5, 3],
      labelBgBorderRadius: 6,
    };
  });

  return { nodes, edges };
}

function BranchList({
  title,
  edges,
  nodesById,
  onSelect,
}: {
  title: string;
  edges: FrontierEdge[];
  nodesById: Map<string, FrontierNode>;
  onSelect: (id: string) => void;
}) {
  if (!edges.length) return null;
  return (
    <section className="inspector-section">
      <h3>{title}</h3>
      <ul className="branch-list">
        {edges.map((edge) => {
          const id = title === "Grows from" ? edge.source : edge.target;
          const node = nodesById.get(id);
          return (
            <li key={edge.id}>
              <button type="button" onClick={() => onSelect(id)}>
                <span>{id}</span>
                {node?.title ?? id}
              </button>
              <small>{edge.relation}</small>
            </li>
          );
        })}
      </ul>
    </section>
  );
}

export function ProofBonsai({ data }: { data: FrontierData }) {
  const [selectedId, setSelectedId] = useState("G0");
  const [tone, setTone] = useState<"all" | BonsaiTone>("all");
  const [query, setQuery] = useState("");
  const [mapScope, setMapScope] = useState<MapScope>("neighborhood");
  const [flowInstance, setFlowInstance] = useState<ReactFlowInstance | null>(null);
  const [copyState, setCopyState] = useState<"idle" | "copied" | "failed">("idle");
  const [hashReady, setHashReady] = useState(false);
  const canvasRef = useRef<HTMLElement>(null);
  const inspectorRef = useRef<HTMLElement>(null);
  const previousView = useRef({ mapScope, tone });

  const nodesById = useMemo(
    () => new Map(data.nodes.map((node) => [node.id, node])),
    [data.nodes],
  );
  const selected = nodesById.get(selectedId) ?? data.nodes[0];

  useEffect(() => {
    const selectFromHash = () => {
      const id = new URLSearchParams(window.location.hash.slice(1)).get("node");
      if (id && nodesById.has(id)) {
        setSelectedId(id);
        setCopyState("idle");
      }
    };
    const timer = window.setTimeout(() => {
      selectFromHash();
      setHashReady(true);
    }, 0);
    window.addEventListener("hashchange", selectFromHash);
    return () => {
      window.clearTimeout(timer);
      window.removeEventListener("hashchange", selectFromHash);
    };
  }, [nodesById]);

  useEffect(() => {
    if (!hashReady) return;
    const nextHash = `#node=${encodeURIComponent(selected.id)}`;
    if (window.location.hash !== nextHash) {
      window.history.replaceState(
        null,
        "",
        `${window.location.pathname}${window.location.search}${nextHash}`,
      );
    }
  }, [hashReady, selected.id]);

  const searchResults = useMemo(() => {
    const needle = query.trim().toLowerCase();
    if (!needle) return [];
    const score = (node: FrontierNode) => {
      const id = node.id.toLowerCase();
      const title = node.title.toLowerCase();
      if (id === needle) return 0;
      if (id.startsWith(needle)) return 1;
      if (title.startsWith(needle)) return 2;
      return 3;
    };
    return data.nodes
      .filter((node) =>
        `${node.id} ${node.title} ${node.exactStatus}`.toLowerCase().includes(needle),
      )
      .sort((left, right) => score(left) - score(right) || left.id.localeCompare(right.id))
      .slice(0, 8);
  }, [data.nodes, query]);

  const neighborhoodIds = useMemo(() => {
    const ids = new Set([selected.id]);
    for (const edge of data.edges) {
      if (edge.source === selected.id) ids.add(edge.target);
      if (edge.target === selected.id) ids.add(edge.source);
    }
    return ids;
  }, [data.edges, selected.id]);

  const visibleNodes = useMemo(() => {
    return data.nodes.filter((node) => {
      const scopeMatch = mapScope === "all" || neighborhoodIds.has(node.id);
      const toneMatch =
        tone === "all" ||
        node.tone === tone ||
        node.id === selected.id ||
        (mapScope === "all" && node.id === "G0");
      return scopeMatch && toneMatch;
    });
  }, [data.nodes, mapScope, neighborhoodIds, selected.id, tone]);

  const visibleIds = useMemo(
    () => new Set(visibleNodes.map((node) => node.id)),
    [visibleNodes],
  );
  const visibleEdges = useMemo(
    () =>
      data.edges.filter(
        (edge) => visibleIds.has(edge.source) && visibleIds.has(edge.target),
      ),
    [data.edges, visibleIds],
  );
  const flow = useMemo(
    () => layoutGraph(visibleNodes, visibleEdges, selectedId, mapScope),
    [mapScope, selectedId, visibleEdges, visibleNodes],
  );

  const selectNode = useCallback(
    (
      id: string,
      { keepMapScope = false, revealInspector = false } = {},
    ) => {
      if (!nodesById.has(id)) return;
      setSelectedId(id);
      setCopyState("idle");
      setQuery("");
      if (!keepMapScope) setMapScope("neighborhood");
      if (revealInspector && window.innerWidth <= 1080) {
        window.setTimeout(() => {
          inspectorRef.current?.scrollIntoView({
            behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
              ? "auto"
              : "smooth",
            block: "start",
          });
        }, 120);
      }
    },
    [nodesById],
  );

  useEffect(() => {
    if (!flowInstance || flow.nodes.length === 0) return;
    const prior = previousView.current;
    const shouldFit =
      mapScope === "neighborhood" ||
      prior.mapScope !== mapScope ||
      prior.tone !== tone;
    previousView.current = { mapScope, tone };
    if (!shouldFit) return;
    const timer = window.setTimeout(() => {
      void flowInstance.fitView({
        nodes: flow.nodes,
        padding: mapScope === "neighborhood" ? 0.24 : 0.06,
        maxZoom: mapScope === "neighborhood" ? 0.95 : 0.22,
        duration: 420,
      });
    }, 60);
    return () => window.clearTimeout(timer);
  }, [flow.nodes, flowInstance, mapScope, selectedId, tone]);

  const focusSelected = useCallback(() => {
    if (!flowInstance) return;
    const selectedFlowNode = flow.nodes.find((node) => node.id === selected.id);
    if (!selectedFlowNode) return;
    void flowInstance.fitView({
      nodes: [selectedFlowNode],
      padding: 1.5,
      maxZoom: 1.08,
      duration: 380,
    });
  }, [flow.nodes, flowInstance, selected.id]);

  const copyNodeLink = useCallback(async () => {
    const url = `${window.location.origin}${window.location.pathname}${window.location.search}#node=${encodeURIComponent(selected.id)}`;
    try {
      await navigator.clipboard.writeText(url);
      setCopyState("copied");
      window.setTimeout(() => setCopyState("idle"), 1800);
    } catch {
      setCopyState("failed");
    }
  }, [selected.id]);

  const inbound = data.edges.filter((edge) => edge.target === selected.id);
  const outbound = data.edges.filter((edge) => edge.source === selected.id);
  const maintenanceCount =
    data.health.missingFromMermaid.length +
    data.health.missingFromNodeKey.length +
    data.health.unlinkedNodeIds.length +
    data.health.unknownEdgeNodeIds.length;

  return (
    <main className="proof-app">
      <header className="app-header">
        <div>
          <p className="eyebrow">A living map of exact claims</p>
          <h1>Proof Bonsai</h1>
          <p className="subtitle">
            The Krenn–Gu programme, grown directly from its canonical frontier.
          </p>
        </div>
        <div className="header-actions">
          <a className="field-notes-link" href="/field-notes">
            <span>Field notes</span>
            Public agent log →
          </a>
          <div className="global-status" aria-label={`Global status ${data.globalStatus}`}>
            <span className="pulse" aria-hidden="true" />
            Global conjecture <strong>{data.globalStatus}</strong>
          </div>
        </div>
      </header>

      <section className="status-strip" aria-label="Bonsai status legend">
        {(Object.keys(toneCopy) as BonsaiTone[]).map((key) => (
          <button
            type="button"
            className={`status-chip status-chip--${key}${tone === key ? " is-active" : ""}`}
            onClick={() => setTone(tone === key ? "all" : key)}
            aria-pressed={tone === key}
            key={key}
          >
            <span className={`botanical-mark botanical-mark--${key}`} aria-hidden="true" />
            <span>
              <strong>{data.counts[key]}</strong> {toneCopy[key].plural}
            </span>
            <small>{toneCopy[key].meaning}</small>
          </button>
        ))}
        <div className="source-chip">
          <span>{data.counts.total} nodes</span>
          <span>{data.counts.edges} typed edges</span>
          <a href={data.source.frontierDocument} target="_blank" rel="noreferrer">
            source {data.source.commit.slice(0, 8)}
          </a>
        </div>
      </section>

      <div className="workspace">
        <section
          className="canvas-panel"
          aria-label="Interactive proof topology"
          ref={canvasRef}
        >
          <div className="canvas-toolbar">
            <div className="search-shell">
              <label className="search-box">
                <span className="sr-only">Search proof nodes</span>
                <span aria-hidden="true">⌕</span>
                <input
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Escape") setQuery("");
                    if (event.key === "Enter" && searchResults[0]) {
                      event.preventDefault();
                      selectNode(searchResults[0].id, { revealInspector: true });
                    }
                  }}
                  placeholder="Find a node, theorem, or obligation…"
                  role="combobox"
                  aria-autocomplete="list"
                  aria-expanded={Boolean(query.trim())}
                  aria-controls="proof-search-results"
                />
                {query && (
                  <button type="button" onClick={() => setQuery("")} aria-label="Clear search">
                    ×
                  </button>
                )}
              </label>
              {query.trim() && (
                <div
                  className="search-results"
                  id="proof-search-results"
                  aria-label="Matching proof nodes"
                >
                  {searchResults.length ? (
                    searchResults.map((node) => (
                      <button
                        type="button"
                        onClick={() => selectNode(node.id, { revealInspector: true })}
                        key={node.id}
                      >
                        <span
                          className={`botanical-mark botanical-mark--${node.tone}`}
                          aria-hidden="true"
                        />
                        <span className="search-result-copy">
                          <strong>{node.id}</strong>
                          <span>{node.title}</span>
                        </span>
                        <small>{toneCopy[node.tone].singular}</small>
                      </button>
                    ))
                  ) : (
                    <p>No matching node. Try an ID such as U7G or a theorem phrase.</p>
                  )}
                </div>
              )}
            </div>
            <div className="toolbar-cluster">
              <div className="map-mode" role="group" aria-label="Map scope">
                <button
                  type="button"
                  aria-pressed={mapScope === "neighborhood"}
                  onClick={() => setMapScope("neighborhood")}
                >
                  Nearby
                </button>
                <button
                  type="button"
                  aria-pressed={mapScope === "all"}
                  onClick={() => setMapScope("all")}
                >
                  Bonsai tree
                </button>
              </div>
              <div className="view-count" aria-live="polite">
                Showing {visibleNodes.length} of {data.nodes.length}
                {tone !== "all" && (
                  <button type="button" onClick={() => setTone("all")}>
                    Reset status
                  </button>
                )}
              </div>
            </div>
          </div>

          <div className="graph-stage">
            <div className="map-instructions" aria-live="polite">
              <strong>
                {mapScope === "neighborhood"
                  ? `${selected.id} · one-edge neighborhood`
                  : `Bonsai canopy · ${visibleNodes.length} nodes`}
              </strong>
              <span>
                {mapScope === "neighborhood"
                  ? "Select a connected node to walk the proof."
                  : "Thicker limbs are a navigation scaffold, not stronger evidence. Select a node, then explore nearby."}
              </span>
            </div>
            <ReactFlow
              nodes={flow.nodes}
              edges={flow.edges}
              nodeTypes={nodeTypes}
              onInit={setFlowInstance}
              onNodeClick={(_, node) =>
                selectNode(node.id, {
                  keepMapScope: mapScope === "all",
                  revealInspector: true,
                })
              }
              fitView
              fitViewOptions={{
                padding: mapScope === "neighborhood" ? 0.24 : 0.06,
                maxZoom: mapScope === "neighborhood" ? 0.95 : 0.22,
              }}
              minZoom={0.025}
              maxZoom={1.8}
              nodesDraggable={false}
              nodesConnectable={false}
              elementsSelectable
              panOnScroll={false}
              zoomOnScroll={false}
              preventScrolling={false}
              zoomOnDoubleClick={false}
              onlyRenderVisibleElements
            >
              <Background
                variant={BackgroundVariant.Dots}
                gap={28}
                size={1}
                color="rgba(171, 151, 112, 0.18)"
              />
              <Controls showInteractive={false} position="bottom-left" />
              <MiniMap
                position="bottom-right"
                pannable
                zoomable
                nodeColor={(node) => {
                  const nodeTone = (node.data as BonsaiNodeData).frontier.tone;
                  return nodeTone === "established"
                    ? "#628b59"
                    : nodeTone === "growing"
                      ? "#d4a84e"
                      : "#b65a49";
                }}
                maskColor="rgba(11, 14, 10, 0.72)"
              />
            </ReactFlow>
            <div className="bonsai-pot" aria-hidden="true">
              <span />
            </div>
          </div>

          <div className={`maintenance-note${maintenanceCount ? " has-findings" : ""}`}>
            <span aria-hidden="true">{maintenanceCount ? "△" : "✓"}</span>
            <p>
              {maintenanceCount ? (
                <>
                  <strong>Source maintenance visible</strong>
                  {data.health.missingFromMermaid.length > 0 && (
                    <> · {data.health.missingFromMermaid.join(", ")} absent from the Mermaid block</>
                  )}
                  {data.health.missingFromNodeKey.length > 0 && (
                    <> · {data.health.missingFromNodeKey.join(", ")} absent from the node key</>
                  )}
                  {data.health.unlinkedNodeIds.length > 0 && (
                    <> · {data.health.unlinkedNodeIds.join(", ")} has no typed edge</>
                  )}
                  {data.health.unknownEdgeNodeIds.length > 0 && (
                    <> · unknown edge references: {data.health.unknownEdgeNodeIds.join(", ")}</>
                  )}
                  . The bonsai never invents a missing relationship.
                </>
              ) : (
                <>
                  <strong>Source topology aligned</strong> · Mermaid labels, node key, and typed edges
                  agree. The map preserves each node’s exact scope.
                </>
              )}
            </p>
          </div>
        </section>

        <aside
          className="inspector"
          aria-label="Selected proof node"
          id="node-inspector"
          ref={inspectorRef}
        >
          <button
            type="button"
            className="back-to-map"
            onClick={() => canvasRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })}
          >
            ← Back to map
          </button>
          <div className="inspector-heading">
            <span className={`botanical-mark botanical-mark--${selected.tone}`} aria-hidden="true" />
            <div>
              <p>{toneCopy[selected.tone].singular} · {selected.id}</p>
              <h2>{selected.title}</h2>
            </div>
          </div>

          <div className="inspector-actions">
            {mapScope === "all" && (
              <button
                type="button"
                className="explore-nearby"
                onClick={() => setMapScope("neighborhood")}
              >
                Explore {selected.id} nearby
              </button>
            )}
            <button type="button" onClick={focusSelected}>
              Locate on map
            </button>
            <button type="button" onClick={copyNodeLink} aria-live="polite">
              {copyState === "copied"
                ? "Link copied"
                : copyState === "failed"
                  ? "Copy failed"
                  : "Copy node link"}
            </button>
          </div>

          <div className={`scope-banner scope-banner--${selected.tone}`}>
            {toneCopy[selected.tone].meaning}
          </div>

          <section className="inspector-section exact-status">
            <h3>Exact repository status</h3>
            <p>{selected.exactStatus}</p>
          </section>

          <section className="inspector-section">
            <h3>Owning sources</h3>
            <ul className="owner-list">
              {selected.owners.map((owner) => (
                <li key={`${owner.href}-${owner.label}`}>
                  <a href={owner.url} target="_blank" rel="noreferrer">
                    {owner.label}<span aria-hidden="true"> ↗</span>
                  </a>
                </li>
              ))}
            </ul>
          </section>

          <section className="inspector-section">
            <h3>Evidence axes</h3>
            <div className="evidence-grid">
              <div>
                <strong>{selected.evidence.indexedDocuments}/{selected.evidence.linkedDocuments}</strong>
                <span>linked docs indexed</span>
              </div>
              <div>
                <strong>{selected.evidence.primaryVerifierCount}</strong>
                <span>primary verifiers</span>
              </div>
              <div>
                <strong>{selected.evidence.independentAuditCount}</strong>
                <span>independent audits</span>
              </div>
            </div>
            {selected.evidence.ledgerStatuses.length > 0 && (
              <p className="ledger-status">
                Ledger records: {selected.evidence.ledgerStatuses.join(", ")}
              </p>
            )}
            <p className="evidence-caveat">
              These counts describe linked ledger records. They do not strengthen the exact status above.
            </p>
          </section>

          <BranchList
            title="Grows from"
            edges={inbound}
            nodesById={nodesById}
            onSelect={(id) => selectNode(id)}
          />
          <BranchList
            title="Branches toward"
            edges={outbound}
            nodesById={nodesById}
            onSelect={(id) => selectNode(id)}
          />
        </aside>
      </div>
    </main>
  );
}
