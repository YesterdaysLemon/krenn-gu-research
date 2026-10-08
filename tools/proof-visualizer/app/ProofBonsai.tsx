"use client";

import dagre from "@dagrejs/dagre";
import {
  applyNodeChanges,
  Background,
  BackgroundVariant,
  Controls,
  EdgeLabelRenderer,
  Handle,
  MarkerType,
  MiniMap,
  Position,
  ReactFlow,
  type Edge,
  type EdgeProps,
  type Node,
  type NodeChange,
  type NodeProps,
  type OnNodeDrag,
  type ReactFlowInstance,
} from "@xyflow/react";
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  useSyncExternalStore,
  type CSSProperties,
} from "react";
import type {
  BonsaiTone,
  FrontierData,
  FrontierEdge,
  FrontierNode,
} from "./frontier-types";

const NODE_WIDTH = 196;
const NODE_HEIGHT = 88;
const POT_WIDTH = 154;
const POT_HEIGHT = 82;
const POT_NODE_ID = "__proof_bonsai_pot__";
const REDUCED_MOTION_QUERY = "(prefers-reduced-motion: reduce)";
const PHYSICS_FRAME_MS = 1000 / 60;
const PHYSICS_PAINT_MS = 64;
const POSITION_EPSILON_SQUARED = 0.12 ** 2;

function subscribeToReducedMotion(onStoreChange: () => void) {
  if (typeof window === "undefined") return () => undefined;
  const media = window.matchMedia(REDUCED_MOTION_QUERY);
  media.addEventListener("change", onStoreChange);
  return () => media.removeEventListener("change", onStoreChange);
}

function getReducedMotionSnapshot() {
  return typeof window === "undefined" || window.matchMedia(REDUCED_MOTION_QUERY).matches;
}

function getReducedMotionServerSnapshot() {
  return true;
}

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
  depth: number;
  seed: number;
};

type BonsaiFlowNode = Node<BonsaiNodeData, "bonsai">;

type BonsaiPotData = {
  label: string;
};

type BonsaiPotFlowNode = Node<BonsaiPotData, "bonsaiPot">;
type BonsaiGraphNode = BonsaiFlowNode | BonsaiPotFlowNode;

type LivingBranchData = {
  relation: string;
  stroke: string;
  dash?: string;
  width: number;
  opacity: number;
  seed: number;
  primary: boolean;
  selected: boolean;
  sprout: boolean;
  showLabel: boolean;
  trunk: boolean;
};

type LivingBranchEdge = Edge<LivingBranchData, "livingBranch">;

type LivingBody = {
  id: string;
  x: number;
  y: number;
  restX: number;
  restY: number;
  velocityX: number;
  velocityY: number;
  forceX: number;
  forceY: number;
  width: number;
  height: number;
  depth: number;
  mass: number;
  fixed: boolean;
  dragging: boolean;
};

type LivingSpring = {
  source: LivingBody;
  target: LivingBody;
  length: number;
  stiffness: number;
};

type LivingPhysics = {
  bodies: Map<string, LivingBody>;
  springs: LivingSpring[];
  quietFrames: number;
  elapsed: number;
};

function stringSeed(value: string) {
  let hash = 2166136261;
  for (let index = 0; index < value.length; index += 1) {
    hash ^= value.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function seededUnit(seed: number, shift = 0) {
  return ((seed >>> shift) & 1023) / 1023;
}

function nodeDimensions(node: BonsaiGraphNode) {
  return node.id === POT_NODE_ID
    ? { width: POT_WIDTH, height: POT_HEIGHT }
    : { width: NODE_WIDTH, height: NODE_HEIGHT };
}

function createLivingPhysics(
  restNodes: BonsaiGraphNode[],
  currentNodes: BonsaiGraphNode[],
  edges: LivingBranchEdge[],
  impulseStrength: number,
): LivingPhysics {
  const currentById = new Map(currentNodes.map((node) => [node.id, node]));
  const bodies = new Map<string, LivingBody>();

  for (const restNode of restNodes) {
    const currentNode = currentById.get(restNode.id) ?? restNode;
    const { width, height } = nodeDimensions(restNode);
    const depth = restNode.type === "bonsai" ? restNode.data.depth : -1;
    const fixed = restNode.id === POT_NODE_ID;
    const seed = stringSeed(`living:${restNode.id}`);
    const canopyWeight = Math.min(1.75, 0.55 + Math.max(0, depth) * 0.09);
    const windPhase = seededUnit(seed, 7) * Math.PI * 2;
    const catchesBreeze =
      !fixed && seededUnit(seed, 5) > (depth >= 3 ? 0.8 : 0.9);
    const breezeStrength = catchesBreeze ? impulseStrength : 0;

    bodies.set(restNode.id, {
      id: restNode.id,
      x: currentNode.position.x + width / 2,
      y: currentNode.position.y + height / 2,
      restX: restNode.position.x + width / 2,
      restY: restNode.position.y + height / 2,
      velocityX: fixed
        ? 0
        : breezeStrength * canopyWeight * (3.2 + Math.sin(windPhase) * 1.35),
      velocityY: fixed
        ? 0
        : breezeStrength * canopyWeight * Math.cos(windPhase * 1.7) * 1.15,
      forceX: 0,
      forceY: 0,
      width,
      height,
      depth,
      mass: 1.02 + Math.max(0, 5 - depth) * 0.11,
      fixed,
      dragging: Boolean(currentNode.dragging),
    });
  }

  const springs = edges.flatMap((edge) => {
    if (!edge.data?.primary) return [];
    const source = bodies.get(edge.source);
    const target = bodies.get(edge.target);
    if (!source || !target) return [];
    return [
      {
        source,
        target,
        length: Math.max(1, Math.hypot(target.restX - source.restX, target.restY - source.restY)),
        stiffness: edge.data.trunk
          ? 0.048
          : Math.max(0.016, 0.028 - Math.max(0, source.depth) * 0.00075),
      },
    ];
  });

  return { bodies, springs, quietFrames: 0, elapsed: 0 };
}

function syncDraggedBodies(physics: LivingPhysics, nodes: BonsaiGraphNode[]) {
  let draggedBodies = 0;

  for (const node of nodes) {
    const body = physics.bodies.get(node.id);
    if (!body || body.fixed) continue;
    const nextX = node.position.x + body.width / 2;
    const nextY = node.position.y + body.height / 2;

    if (node.dragging) {
      const movementX = nextX - body.x;
      const movementY = nextY - body.y;
      body.velocityX = body.velocityX * 0.28 + movementX * 0.34;
      body.velocityY = body.velocityY * 0.28 + movementY * 0.34;
      body.x = nextX;
      body.y = nextY;
      body.dragging = true;
      draggedBodies += 1;
    } else if (body.dragging) {
      body.velocityX = body.velocityX * 0.56 + (nextX - body.x) * 0.32;
      body.velocityY = body.velocityY * 0.56 + (nextY - body.y) * 0.32;
      body.x = nextX;
      body.y = nextY;
      body.dragging = false;
    }
  }

  return draggedBodies;
}

function advanceLivingPhysics(
  physics: LivingPhysics,
  elapsedMilliseconds: number,
  draggedBodies: number,
) {
  const delta = Math.min(1.8, Math.max(0.35, elapsedMilliseconds / PHYSICS_FRAME_MS));

  for (const body of physics.bodies.values()) {
    const rootStrength = body.id === "G0" ? 0.022 : 0;
    const anchorStrength = rootStrength || 0.0036 / (1 + Math.max(0, body.depth) * 0.035);
    body.forceX = (body.restX - body.x) * anchorStrength;
    body.forceY = (body.restY - body.y) * anchorStrength * 1.08;
  }

  for (const spring of physics.springs) {
    const offsetX = spring.target.x - spring.source.x;
    const offsetY = spring.target.y - spring.source.y;
    const distance = Math.max(0.001, Math.hypot(offsetX, offsetY));
    const directionX = offsetX / distance;
    const directionY = offsetY / distance;
    const relativeVelocity =
      (spring.target.velocityX - spring.source.velocityX) * directionX +
      (spring.target.velocityY - spring.source.velocityY) * directionY;
    const force = (distance - spring.length) * spring.stiffness + relativeVelocity * 0.034;
    const forceX = force * directionX;
    const forceY = force * directionY;
    spring.source.forceX += forceX;
    spring.source.forceY += forceY;
    spring.target.forceX -= forceX;
    spring.target.forceY -= forceY;
  }

  let maximumSpeed = 0;
  let maximumDisplacement = 0;
  const damping = Math.pow(0.895, delta);

  for (const body of physics.bodies.values()) {
    if (body.fixed) {
      body.x = body.restX;
      body.y = body.restY;
      body.velocityX = 0;
      body.velocityY = 0;
      continue;
    }
    if (!body.dragging) {
      body.velocityX = (body.velocityX + (body.forceX / body.mass) * delta) * damping;
      body.velocityY = (body.velocityY + (body.forceY / body.mass) * delta) * damping;
      const speed = Math.hypot(body.velocityX, body.velocityY);
      if (speed > 18) {
        body.velocityX = (body.velocityX / speed) * 18;
        body.velocityY = (body.velocityY / speed) * 18;
      }
      body.x += body.velocityX * delta;
      body.y += body.velocityY * delta;

      const displacementX = body.x - body.restX;
      const displacementY = body.y - body.restY;
      const displacement = Math.hypot(displacementX, displacementY);
      const maximumReach = body.id === "G0" ? 58 : Math.min(210, 88 + body.depth * 8);
      if (displacement > maximumReach) {
        body.x = body.restX + (displacementX / displacement) * maximumReach;
        body.y = body.restY + (displacementY / displacement) * maximumReach;
        body.velocityX *= 0.48;
        body.velocityY *= 0.48;
      }
    }

    maximumSpeed = Math.max(maximumSpeed, Math.hypot(body.velocityX, body.velocityY));
    maximumDisplacement = Math.max(
      maximumDisplacement,
      Math.hypot(body.x - body.restX, body.y - body.restY),
    );
  }

  physics.elapsed += elapsedMilliseconds;
  if (draggedBodies === 0 && maximumSpeed < 0.035 && maximumDisplacement < 0.75) {
    physics.quietFrames += 1;
  } else {
    physics.quietFrames = 0;
  }

  return physics.quietFrames > 14 || (draggedBodies === 0 && physics.elapsed > 5200);
}

function applyLivingPositions(
  nodes: BonsaiGraphNode[],
  physics: LivingPhysics,
) {
  let nextNodes: BonsaiGraphNode[] | null = null;

  nodes.forEach((node, index) => {
    const body = physics.bodies.get(node.id);
    if (!body || node.dragging) return;
    const nextX = body.x - body.width / 2;
    const nextY = body.y - body.height / 2;
    const movementSquared =
      (nextX - node.position.x) ** 2 + (nextY - node.position.y) ** 2;
    if (movementSquared < POSITION_EPSILON_SQUARED) return;
    if (!nextNodes) nextNodes = [...nodes];
    nextNodes[index] = {
      ...node,
      position: {
        x: nextX,
        y: nextY,
      },
    };
  });

  return nextNodes ?? nodes;
}

function BonsaiNode({ data, selected }: NodeProps<BonsaiFlowNode>) {
  const { frontier, seed } = data;
  const growthStyle = {
    "--growth-turn": `${(seededUnit(seed, 4) - 0.5) * 24}deg`,
    "--growth-scale": `${0.9 + seededUnit(seed, 14) * 0.2}`,
  } as CSSProperties;
  return (
    <div
      className={`bonsai-node bonsai-node--${frontier.tone}${selected ? " is-selected" : ""}`}
      aria-label={`${frontier.id}: ${frontier.title}. ${toneCopy[frontier.tone].meaning}`}
      title={`Inspect ${frontier.id}: ${frontier.title}`}
    >
      <Handle type="source" position={Position.Top} className="branch-handle" />
      <span
        className={`botanical-mark botanical-mark--${frontier.tone}`}
        style={growthStyle}
        aria-hidden="true"
      />
      <span className="node-copy">
        <span className="node-id">{frontier.id}</span>
        <span className="node-title">{frontier.title}</span>
      </span>
      <Handle type="target" position={Position.Bottom} className="branch-handle" />
    </div>
  );
}

function BonsaiPotNode({ data }: NodeProps<BonsaiPotFlowNode>) {
  return (
    <div className="bonsai-pot-node" aria-label={data.label}>
      <Handle type="source" position={Position.Top} className="pot-handle" />
      <span className="bonsai-pot-node__soil" aria-hidden="true" />
      <span className="bonsai-pot-node__rim" aria-hidden="true" />
      <span className="bonsai-pot-node__body" aria-hidden="true">
        <span />
      </span>
      <span className="bonsai-pot-node__shadow" aria-hidden="true" />
    </div>
  );
}

type CubicPoint = { x: number; y: number };

function cubicPoint(
  start: CubicPoint,
  controlOne: CubicPoint,
  controlTwo: CubicPoint,
  end: CubicPoint,
  progress: number,
) {
  const inverse = 1 - progress;
  return {
    x:
      inverse ** 3 * start.x +
      3 * inverse ** 2 * progress * controlOne.x +
      3 * inverse * progress ** 2 * controlTwo.x +
      progress ** 3 * end.x,
    y:
      inverse ** 3 * start.y +
      3 * inverse ** 2 * progress * controlOne.y +
      3 * inverse * progress ** 2 * controlTwo.y +
      progress ** 3 * end.y,
  };
}

function cubicTangent(
  start: CubicPoint,
  controlOne: CubicPoint,
  controlTwo: CubicPoint,
  end: CubicPoint,
  progress: number,
) {
  const inverse = 1 - progress;
  return {
    x:
      3 * inverse ** 2 * (controlOne.x - start.x) +
      6 * inverse * progress * (controlTwo.x - controlOne.x) +
      3 * progress ** 2 * (end.x - controlTwo.x),
    y:
      3 * inverse ** 2 * (controlOne.y - start.y) +
      6 * inverse * progress * (controlTwo.y - controlOne.y) +
      3 * progress ** 2 * (end.y - controlTwo.y),
  };
}

function livingBranchGeometry(
  sourceX: number,
  sourceY: number,
  targetX: number,
  targetY: number,
  seed: number,
) {
  const start = { x: sourceX, y: sourceY };
  const end = { x: targetX, y: targetY };
  const dx = targetX - sourceX;
  const dy = targetY - sourceY;
  const distance = Math.hypot(dx, dy);
  const direction = seed % 2 === 0 ? 1 : -1;
  const bow =
    direction *
    Math.min(94, 12 + Math.abs(dx) * 0.08 + distance * (0.025 + seededUnit(seed, 10) * 0.035));
  const controlOne = {
    x: sourceX + dx * 0.26 + bow,
    y: sourceY + dy * 0.37,
  };
  const controlTwo = {
    x: sourceX + dx * 0.74 - bow * 0.52,
    y: sourceY + dy * 0.72,
  };
  return {
    start,
    end,
    controlOne,
    controlTwo,
    path: `M ${start.x} ${start.y} C ${controlOne.x} ${controlOne.y}, ${controlTwo.x} ${controlTwo.y}, ${end.x} ${end.y}`,
  };
}

function LivingBranch({
  sourceX,
  sourceY,
  targetX,
  targetY,
  markerEnd,
  data,
}: EdgeProps<LivingBranchEdge>) {
  if (!data) return null;
  const geometry = livingBranchGeometry(sourceX, sourceY, targetX, targetY, data.seed);
  const midpoint = cubicPoint(
    geometry.start,
    geometry.controlOne,
    geometry.controlTwo,
    geometry.end,
    0.5,
  );
  const sproutPoint = cubicPoint(
    geometry.start,
    geometry.controlOne,
    geometry.controlTwo,
    geometry.end,
    0.58,
  );
  const tangent = cubicTangent(
    geometry.start,
    geometry.controlOne,
    geometry.controlTwo,
    geometry.end,
    0.58,
  );
  const angle = (Math.atan2(tangent.y, tangent.x) * 180) / Math.PI;
  const leafDirection = data.seed % 2 === 0 ? 1 : -1;
  const leafScale = 0.72 + seededUnit(data.seed, 12) * 0.4;
  const sproutStyle = {
    "--sprout-duration": `${4.2 + seededUnit(data.seed, 6) * 3.4}s`,
    "--sprout-delay": `${-seededUnit(data.seed, 17) * 5.8}s`,
    "--sprout-turn": `${leafDirection * (2.5 + seededUnit(data.seed, 3) * 3.5)}deg`,
  } as CSSProperties;

  return (
    <>
      <g
        className={`living-branch${data.primary ? " is-primary" : ""}${
          data.selected ? " is-selected" : ""
        }${data.trunk ? " is-trunk" : ""}`}
        opacity={data.opacity}
      >
        {(data.primary || data.trunk) && (
          <path
            className="living-branch__shadow"
            d={geometry.path}
            strokeWidth={data.width + (data.trunk ? 5 : 2.5)}
            vectorEffect="non-scaling-stroke"
          />
        )}
        <path
          className="living-branch__bark"
          d={geometry.path}
          stroke={data.stroke}
          strokeDasharray={data.dash}
          strokeWidth={data.width}
          markerEnd={markerEnd}
          vectorEffect="non-scaling-stroke"
        />
        {(data.primary || data.trunk) && (
          <path
            className="living-branch__light"
            d={geometry.path}
            strokeWidth={Math.max(0.55, data.width * 0.24)}
            vectorEffect="non-scaling-stroke"
          />
        )}
        {data.sprout && (
          <g
            className="living-branch__sprout"
            transform={`translate(${sproutPoint.x} ${sproutPoint.y}) rotate(${angle}) scale(${leafScale})`}
          >
            <g className="living-branch__sprout-leaves" style={sproutStyle}>
              <path
                d="M 0 0 C 5 -12 17 -13 24 -4 C 17 5 7 7 0 0 Z"
                transform={`rotate(${leafDirection * 48})`}
              />
              <path
                d="M 0 0 C 5 -10 14 -11 20 -3 C 14 5 6 6 0 0 Z"
                transform={`rotate(${-leafDirection * 42}) scale(.82)`}
              />
            </g>
          </g>
        )}
      </g>
      {data.showLabel && data.relation && (
        <EdgeLabelRenderer>
          <div
            className="living-branch-label"
            style={{
              transform: `translate(-50%, -50%) translate(${midpoint.x}px, ${midpoint.y}px)`,
            }}
          >
            {data.relation}
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
}

const nodeTypes = { bonsai: BonsaiNode, bonsaiPot: BonsaiPotNode };
const edgeTypes = { livingBranch: LivingBranch };

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

type GrowthForest = {
  primaryBranches: Set<string>;
  parentById: Map<string, string>;
  childrenById: Map<string, string[]>;
  depthById: Map<string, number>;
  roots: string[];
};

function buildGrowthForest(
  sourceNodes: FrontierNode[],
  sourceEdges: FrontierEdge[],
): GrowthForest {
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
  const primaryBranches = new Set<string>();
  const parentById = new Map<string, string>();
  const childrenById = new Map(sourceNodes.map((node) => [node.id, [] as string[]]));
  const depthById = new Map<string, number>();
  const forestRoots: string[] = [];

  for (const start of starts) {
    if (visited.has(start)) continue;
    visited.add(start);
    forestRoots.push(start);
    depthById.set(start, 0);
    const queue = [start];
    for (let index = 0; index < queue.length; index += 1) {
      for (const edge of outgoing.get(queue[index]) ?? []) {
        if (visited.has(edge.target)) continue;
        visited.add(edge.target);
        primaryBranches.add(edge.id);
        parentById.set(edge.target, queue[index]);
        childrenById.get(queue[index])?.push(edge.target);
        depthById.set(edge.target, (depthById.get(queue[index]) ?? 0) + 1);
        queue.push(edge.target);
      }
    }
  }

  return {
    primaryBranches,
    parentById,
    childrenById,
    depthById,
    roots: forestRoots,
  };
}

function separateGrowthRow(
  ids: string[],
  idealById: Map<string, number>,
  rawPoints: Map<string, LayoutPoint>,
) {
  if (ids.length === 0) return new Map<string, number>();
  const gap = NODE_WIDTH + 52;
  const ordered = [...ids].sort((left, right) => {
    const idealDifference =
      (idealById.get(left) ?? 0) - (idealById.get(right) ?? 0);
    if (Math.abs(idealDifference) > 0.01) return idealDifference;
    const rawDifference =
      (rawPoints.get(left)?.x ?? 0) - (rawPoints.get(right)?.x ?? 0);
    return rawDifference || left.localeCompare(right);
  });
  const placed = new Map<string, number>();
  ordered.forEach((id, index) => {
    const ideal = idealById.get(id) ?? 0;
    const previous = index > 0 ? placed.get(ordered[index - 1]) ?? ideal : ideal - gap;
    placed.set(id, Math.max(ideal, previous + gap));
  });

  const idealCentre =
    ordered.reduce((sum, id) => sum + (idealById.get(id) ?? 0), 0) / ordered.length;
  const placedCentre =
    ordered.reduce((sum, id) => sum + (placed.get(id) ?? 0), 0) / ordered.length;
  const correction = idealCentre - placedCentre;
  for (const id of ordered) placed.set(id, (placed.get(id) ?? 0) + correction);
  return placed;
}

function shapeLivingCanopy(
  rawPoints: Map<string, LayoutPoint>,
  forest: GrowthForest,
) {
  const rows = new Map<number, string[]>();
  for (const id of rawPoints.keys()) {
    const depth = forest.depthById.get(id) ?? 0;
    const row = rows.get(depth) ?? [];
    row.push(id);
    rows.set(depth, row);
  }

  const horizontal = new Map<string, number>();
  const detachedRoots = forest.roots.filter((id) => id !== "G0");
  if (rawPoints.has("G0")) horizontal.set("G0", 0);
  detachedRoots.forEach((id, index) => {
    const direction = index % 2 === 0 ? -1 : 1;
    const ring = Math.floor(index / 2) + 1;
    horizontal.set(id, direction * ring * (NODE_WIDTH + 82));
  });

  const maximumDepth = Math.max(0, ...rows.keys());
  for (let depth = 1; depth <= maximumDepth; depth += 1) {
    const row = rows.get(depth) ?? [];
    const ideal = new Map<string, number>();
    for (const id of row) {
      const parentId = forest.parentById.get(id);
      const siblings = parentId ? forest.childrenById.get(parentId) ?? [id] : [id];
      const siblingIndex = Math.max(0, siblings.indexOf(id));
      const siblingOffset =
        (siblingIndex - (siblings.length - 1) / 2) *
        (NODE_WIDTH + 62) *
        (0.88 + Math.min(depth, 12) * 0.012);
      const seed = stringSeed(`${parentId ?? "root"}:${id}`);
      const soloLean =
        siblings.length === 1 ? (seededUnit(seed, 5) - 0.5) * 78 : 0;
      const depthLean = Math.sin(depth * 0.61) * Math.min(34, depth * 3.2);
      ideal.set(
        id,
        (parentId ? horizontal.get(parentId) ?? 0 : rawPoints.get(id)?.x ?? 0) +
          siblingOffset +
          soloLean +
          depthLean,
      );
    }
    const separated = separateGrowthRow(row, ideal, rawPoints);
    for (const [id, x] of separated) horizontal.set(id, x);
  }

  for (let pass = 0; pass < 2; pass += 1) {
    for (let depth = maximumDepth - 1; depth >= 0; depth -= 1) {
      for (const id of rows.get(depth) ?? []) {
        const children = (forest.childrenById.get(id) ?? []).filter((child) =>
          horizontal.has(child),
        );
        if (!children.length || id === "G0") continue;
        const childCentre =
          children.reduce((sum, child) => sum + (horizontal.get(child) ?? 0), 0) /
          children.length;
        horizontal.set(id, (horizontal.get(id) ?? 0) * 0.58 + childCentre * 0.42);
      }
      const row = rows.get(depth) ?? [];
      const separated = separateGrowthRow(row, horizontal, rawPoints);
      for (const [id, x] of separated) horizontal.set(id, x);
    }
  }

  const rootOffset = horizontal.get("G0") ?? 0;
  const shaped = new Map<string, LayoutPoint>();
  for (const [depth, row] of rows) {
    const rowSeed = stringSeed(row.slice().sort().join("|"));
    const rowSway =
      depth === 0
        ? 0
        : Math.sin(depth * 0.52) * 44 + (seededUnit(rowSeed, 7) - 0.5) * 32;
    for (const id of row) {
      const seed = stringSeed(id);
      shaped.set(id, {
        x:
          (horizontal.get(id) ?? rawPoints.get(id)?.x ?? 0) -
          rootOffset +
          rowSway +
          (seededUnit(seed, 9) - 0.5) * 18,
        y:
          -depth * (NODE_HEIGHT + 66) +
          (depth === 0 ? 0 : (seededUnit(seed, 18) - 0.5) * 14),
      });
    }
  }
  if (shaped.has("G0")) shaped.set("G0", { x: 0, y: 0 });
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
  const forest = buildGrowthForest(sourceNodes, sourceEdges);
  const layoutPoints =
    mapScope === "all" ? shapeLivingCanopy(rawPoints, forest) : rawPoints;

  const nodes: BonsaiGraphNode[] = sourceNodes.map((frontier) => {
    const point = layoutPoints.get(frontier.id) ?? { x: 0, y: 0 };
    return {
      id: frontier.id,
      type: "bonsai",
      position: {
        x: point.x - NODE_WIDTH / 2,
        y: point.y - NODE_HEIGHT / 2,
      },
      data: {
        frontier,
        depth: forest.depthById.get(frontier.id) ?? 0,
        seed: stringSeed(frontier.id),
      },
      draggable: mapScope === "all",
      selectable: true,
      selected: frontier.id === selectedId,
      sourcePosition: Position.Top,
      targetPosition: Position.Bottom,
      style: { width: NODE_WIDTH, height: NODE_HEIGHT },
      ariaLabel: `${frontier.id}: ${frontier.title}`,
    };
  });

  if (mapScope === "all" && layoutPoints.has("G0")) {
    const root = layoutPoints.get("G0") ?? { x: 0, y: 0 };
    nodes.push({
      id: POT_NODE_ID,
      type: "bonsaiPot",
      position: {
        x: root.x - POT_WIDTH / 2,
        y: root.y + NODE_HEIGHT / 2 + 118,
      },
      data: { label: "Proof Bonsai pot and living root anchor" },
      draggable: false,
      selectable: false,
      sourcePosition: Position.Top,
      style: { width: POT_WIDTH, height: POT_HEIGHT },
      ariaLabel: "Proof Bonsai pot and living root anchor",
    });
  }

  const edges: LivingBranchEdge[] = sourceEdges.map((edge) => {
    const treatment = edgeTreatment(edge.relation);
    const isPrimary = forest.primaryBranches.has(edge.id);
    const isSelectedBranch = edge.source === selectedId || edge.target === selectedId;
    const wholeMap = mapScope === "all";
    const depth = forest.depthById.get(edge.source) ?? 0;
    const seed = stringSeed(edge.id);
    const taperedWidth = Math.max(1.45, 5.4 - depth * 0.14);
    return {
      ...edge,
      type: "livingBranch",
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: treatment.stroke,
        width: wholeMap ? 9 : 13,
        height: wholeMap ? 9 : 13,
      },
      data: {
        relation: edge.relation,
        stroke: treatment.stroke,
        dash: treatment.dash,
        width: wholeMap
          ? isSelectedBranch
            ? Math.max(4.2, taperedWidth)
            : isPrimary
              ? taperedWidth
              : 0.72
          : isSelectedBranch
            ? 3
            : 2.2,
        opacity: wholeMap
          ? isSelectedBranch
            ? 1
            : isPrimary
              ? 0.74
              : 0.11
          : isSelectedBranch
            ? 1
            : 0.78,
        seed,
        primary: isPrimary,
        selected: isSelectedBranch,
        sprout: wholeMap && isPrimary && (isSelectedBranch || seed % 11 === 0),
        showLabel: !wholeMap,
        trunk: false,
      },
      zIndex: isSelectedBranch ? 3 : isPrimary ? 2 : 1,
    };
  });

  if (mapScope === "all" && layoutPoints.has("G0")) {
    edges.unshift({
      id: `${POT_NODE_ID}-trunk`,
      source: POT_NODE_ID,
      target: "G0",
      type: "livingBranch",
      selectable: false,
      zIndex: 0,
      data: {
        relation: "",
        stroke: "#6f5136",
        width: 10,
        opacity: 0.96,
        seed: stringSeed("proof-bonsai-trunk"),
        primary: true,
        selected: false,
        sprout: false,
        showLabel: false,
        trunk: true,
      },
    });
  }

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
  const [flowInstance, setFlowInstance] = useState<
    ReactFlowInstance<BonsaiGraphNode, LivingBranchEdge> | null
  >(null);
  const [layoutEpoch, setLayoutEpoch] = useState(0);
  const [graphState, setGraphState] = useState<{
    key: string;
    nodes: BonsaiGraphNode[];
  }>({ key: "", nodes: [] });
  const [motionPreference, setMotionPreference] = useState<boolean | null>(null);
  const [physicsEpoch, setPhysicsEpoch] = useState(0);
  const [copyState, setCopyState] = useState<"idle" | "copied" | "failed">("idle");
  const [hashReady, setHashReady] = useState(false);
  const prefersReducedMotion = useSyncExternalStore(
    subscribeToReducedMotion,
    getReducedMotionSnapshot,
    getReducedMotionServerSnapshot,
  );
  const motionEnabled = motionPreference ?? !prefersReducedMotion;
  const canvasRef = useRef<HTMLElement>(null);
  const inspectorRef = useRef<HTMLElement>(null);
  const previousView = useRef({ mapScope, tone, layoutEpoch });
  const pendingImpulse = useRef(0);

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
  const layoutKey = `${mapScope}:${tone}:${
    mapScope === "neighborhood" ? selectedId : "canopy"
  }:${layoutEpoch}`;
  const graphNodes = graphState.key === layoutKey ? graphState.nodes : flow.nodes;
  const latestFlow = useRef(flow);
  const latestGraphNodes = useRef(graphNodes);

  useEffect(() => {
    latestFlow.current = flow;
    latestGraphNodes.current = graphNodes;
  }, [flow, graphNodes]);

  const trackNodeGrowth = useCallback(
    (changes: NodeChange<BonsaiGraphNode>[]) => {
      setGraphState((current) => ({
        key: layoutKey,
        nodes: applyNodeChanges(
          changes,
          current.key === layoutKey ? current.nodes : flow.nodes,
        ),
      }));
    },
    [flow.nodes, layoutKey],
  );

  const wakeBonsai = useCallback((impulseStrength = 0) => {
    pendingImpulse.current = Math.max(pendingImpulse.current, impulseStrength);
    setPhysicsEpoch((value) => value + 1);
  }, []);

  const toggleBonsaiMotion = useCallback(() => {
    const nextMotion = !motionEnabled;
    setMotionPreference(nextMotion);
    if (nextMotion) {
      pendingImpulse.current = Math.max(pendingImpulse.current, 0.32);
      setPhysicsEpoch((value) => value + 1);
    }
  }, [motionEnabled]);

  const regrowBonsai = useCallback(() => {
    pendingImpulse.current = Math.max(pendingImpulse.current, motionEnabled ? 0.24 : 0);
    setLayoutEpoch((value) => value + 1);
  }, [motionEnabled]);

  const wakeOnNodeDrag = useCallback<OnNodeDrag<BonsaiGraphNode>>(() => {
    if (motionEnabled && mapScope === "all") wakeBonsai();
  }, [mapScope, motionEnabled, wakeBonsai]);

  useEffect(() => {
    if (mapScope !== "all" || !motionEnabled) return;
    const restFlow = latestFlow.current;
    if (restFlow.nodes.length === 0) return;

    const physics = createLivingPhysics(
      restFlow.nodes,
      latestGraphNodes.current,
      restFlow.edges,
      pendingImpulse.current,
    );
    pendingImpulse.current = 0;
    let animationFrame = 0;
    let previousTimestamp = performance.now();
    let previousPaint = previousTimestamp - PHYSICS_PAINT_MS;
    let cancelled = false;

    const tick = (timestamp: number) => {
      if (cancelled) return;
      const elapsed = Math.min(48, Math.max(1, timestamp - previousTimestamp));
      previousTimestamp = timestamp;
      const draggedBodies = syncDraggedBodies(physics, latestGraphNodes.current);
      const settled = advanceLivingPhysics(physics, elapsed, draggedBodies);

      if (timestamp - previousPaint >= PHYSICS_PAINT_MS || settled) {
        previousPaint = timestamp;
        setGraphState((current) => {
          const nodes = applyLivingPositions(
            current.key === layoutKey ? current.nodes : restFlow.nodes,
            physics,
          );
          if (current.key === layoutKey && nodes === current.nodes) return current;
          return { key: layoutKey, nodes };
        });
      }

      if (!settled) animationFrame = window.requestAnimationFrame(tick);
    };

    animationFrame = window.requestAnimationFrame(tick);
    return () => {
      cancelled = true;
      window.cancelAnimationFrame(animationFrame);
    };
  }, [layoutKey, mapScope, motionEnabled, physicsEpoch]);

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
      prior.tone !== tone ||
      prior.layoutEpoch !== layoutEpoch;
    previousView.current = { mapScope, tone, layoutEpoch };
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
  }, [flow.nodes, flowInstance, layoutEpoch, mapScope, selectedId, tone]);

  const focusSelected = useCallback(() => {
    if (!flowInstance) return;
    const selectedFlowNode = graphNodes.find((node) => node.id === selected.id);
    if (!selectedFlowNode) return;
    const potNode = graphNodes.find((node) => node.id === POT_NODE_ID);
    void flowInstance.fitView({
      nodes:
        selected.id === "G0" && potNode
          ? [selectedFlowNode, potNode]
          : [selectedFlowNode],
      padding: 1.5,
      maxZoom: 1.08,
      duration: 380,
    });
  }, [flowInstance, graphNodes, selected.id]);

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
              {mapScope === "all" && (
                <div className="motion-controls" role="group" aria-label="Bonsai motion">
                  <button
                    type="button"
                    className="motion-toggle"
                    aria-pressed={motionEnabled}
                    onClick={toggleBonsaiMotion}
                    title={
                      prefersReducedMotion && motionPreference === null
                        ? "Motion is resting because reduced motion is preferred"
                        : "Toggle the spring response and ambient leaf movement"
                    }
                  >
                    <span className="motion-signal" aria-hidden="true">
                      <i />
                      <i />
                      <i />
                    </span>
                    {motionEnabled ? "Living" : "Still"}
                  </button>
                  <button
                    type="button"
                    className="breeze-button"
                    onClick={() => wakeBonsai(1)}
                    disabled={!motionEnabled}
                  >
                    Breeze
                  </button>
                </div>
              )}
              <div className="view-count" aria-live="polite">
                Showing {visibleNodes.length} of {data.nodes.length}
                {mapScope === "all" && (
                  <button type="button" onClick={regrowBonsai}>
                    Regrow layout
                  </button>
                )}
                {tone !== "all" && (
                  <button type="button" onClick={() => setTone("all")}>
                    Reset status
                  </button>
                )}
              </div>
            </div>
          </div>

          <div className={`graph-stage${motionEnabled && mapScope === "all" ? " is-living" : ""}`}>
            <div className="map-instructions" aria-live="polite">
              <strong>
                {mapScope === "neighborhood"
                  ? `${selected.id} · one-edge neighborhood`
                  : `Bonsai canopy · ${visibleNodes.length} nodes · ${motionEnabled ? "springs awake" : "branches resting"}`}
              </strong>
              <span>
                {mapScope === "neighborhood"
                  ? "Wheel to zoom · drag the canvas to pan · select a connected node to walk the proof."
                  : motionEnabled
                    ? "Wheel to zoom · any-button drag pans · drag a node to bend its lineage · Breeze sends a ripple through primary branches."
                    : "Wheel to zoom · any-button drag pans · node positions stay where you place them until motion wakes or the layout regrows."}
              </span>
            </div>
            <ReactFlow<BonsaiGraphNode, LivingBranchEdge>
              nodes={graphNodes}
              edges={flow.edges}
              nodeTypes={nodeTypes}
              edgeTypes={edgeTypes}
              onInit={setFlowInstance}
              onNodesChange={trackNodeGrowth}
              onNodeDragStart={wakeOnNodeDrag}
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
              minZoom={0.018}
              maxZoom={2.4}
              nodesDraggable={mapScope === "all"}
              nodesConnectable={false}
              elementsSelectable
              panOnScroll={false}
              zoomOnScroll
              zoomOnPinch
              preventScrolling
              zoomOnDoubleClick
              panOnDrag={[0, 1, 2]}
              selectionOnDrag={false}
              onPaneContextMenu={(event) => event.preventDefault()}
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
                  if (node.id === POT_NODE_ID) return "#76583e";
                  const nodeTone = (node.data as BonsaiNodeData).frontier?.tone;
                  return nodeTone === "established"
                    ? "#628b59"
                    : nodeTone === "growing"
                      ? "#d4a84e"
                      : "#b65a49";
                }}
                maskColor="rgba(11, 14, 10, 0.72)"
              />
            </ReactFlow>
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
