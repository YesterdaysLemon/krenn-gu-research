"use client";

import dagre from "@dagrejs/dagre";
import Link from "next/link";
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
} from "@xyflow/react";
import { useMemo, useState } from "react";
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

function layoutGraph(
  sourceNodes: FrontierNode[],
  sourceEdges: FrontierEdge[],
  selectedId: string,
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

  const nodes: BonsaiFlowNode[] = sourceNodes.map((frontier) => {
    const point = graph.node(frontier.id) ?? { x: 0, y: 0 };
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
    return {
      ...edge,
      type: "smoothstep",
      label: edge.relation,
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: treatment.stroke,
        width: 13,
        height: 13,
      },
      style: {
        stroke: treatment.stroke,
        strokeWidth: 2.2,
        strokeDasharray: treatment.dash,
      },
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

  const nodesById = useMemo(
    () => new Map(data.nodes.map((node) => [node.id, node])),
    [data.nodes],
  );
  const selected = nodesById.get(selectedId) ?? data.nodes[0];

  const visibleNodes = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return data.nodes.filter((node) => {
      const toneMatch = tone === "all" || node.tone === tone;
      const queryMatch =
        !needle ||
        `${node.id} ${node.title} ${node.exactStatus}`
          .toLowerCase()
          .includes(needle);
      return toneMatch && queryMatch;
    });
  }, [data.nodes, query, tone]);

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
    () => layoutGraph(visibleNodes, visibleEdges, selectedId),
    [selectedId, visibleEdges, visibleNodes],
  );

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
          <Link className="field-notes-link" href="/field-notes">
            <span>Field notes</span>
            Public agent log →
          </Link>
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
        <section className="canvas-panel" aria-label="Interactive proof topology">
          <div className="canvas-toolbar">
            <label className="search-box">
              <span className="sr-only">Search proof nodes</span>
              <span aria-hidden="true">⌕</span>
              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Find a node, theorem, or obligation…"
              />
              {query && (
                <button type="button" onClick={() => setQuery("")} aria-label="Clear search">
                  ×
                </button>
              )}
            </label>
            <div className="view-count" aria-live="polite">
              Showing {visibleNodes.length} of {data.nodes.length}
              {(tone !== "all" || query) && (
                <button
                  type="button"
                  onClick={() => {
                    setTone("all");
                    setQuery("");
                  }}
                >
                  Reset
                </button>
              )}
            </div>
          </div>

          <div className="graph-stage">
            <ReactFlow
              nodes={flow.nodes}
              edges={flow.edges}
              nodeTypes={nodeTypes}
              onNodeClick={(_, node) => setSelectedId(node.id)}
              fitView
              fitViewOptions={{ padding: 0.12, maxZoom: 0.86 }}
              minZoom={0.12}
              maxZoom={1.8}
              nodesDraggable={false}
              nodesConnectable={false}
              elementsSelectable
              panOnScroll
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
              <strong>{maintenanceCount ? "Source maintenance visible" : "Source topology aligned"}</strong>
              {data.health.missingFromMermaid.length > 0 && (
                <> · {data.health.missingFromMermaid.join(", ")} absent from the Mermaid block</>
              )}
              {data.health.unlinkedNodeIds.length > 0 && (
                <> · {data.health.unlinkedNodeIds.join(", ")} has no typed edge</>
              )}
              {data.health.unknownEdgeNodeIds.length > 0 && (
                <> · unknown edge references: {data.health.unknownEdgeNodeIds.join(", ")}</>
              )}
              . The bonsai includes node-key entries and never invents missing relationships.
            </p>
          </div>
        </section>

        <aside className="inspector" aria-label="Selected proof node">
          <div className="inspector-heading">
            <span className={`botanical-mark botanical-mark--${selected.tone}`} aria-hidden="true" />
            <div>
              <p>{toneCopy[selected.tone].singular} · {selected.id}</p>
              <h2>{selected.title}</h2>
            </div>
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
            onSelect={setSelectedId}
          />
          <BranchList
            title="Branches toward"
            edges={outbound}
            nodesById={nodesById}
            onSelect={setSelectedId}
          />
        </aside>
      </div>
    </main>
  );
}
