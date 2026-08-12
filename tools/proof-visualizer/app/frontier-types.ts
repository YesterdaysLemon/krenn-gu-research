export type BonsaiTone = "established" | "growing" | "pruned";

export interface OwnerLink {
  label: string;
  href: string;
  document: string | null;
  anchor?: string | null;
  url: string;
}
export interface FrontierNode {
  id: string;
  title: string;
  diagramLabel: string | null;
  exactStatus: string;
  tone: BonsaiTone;
  owners: OwnerLink[];
  evidence: {
    indexedDocuments: number;
    linkedDocuments: number;
    ledgerStatuses: string[];
    primaryVerifierCount: number;
    independentAuditCount: number;
  };
}

export interface FrontierEdge {
  id: string;
  source: string;
  target: string;
  relation: string;
  note: string;
}

export interface FrontierData {
  schemaVersion: number;
  programme: string;
  globalStatus: string;
  source: {
    repository: string;
    commit: string;
    ledgerCommit: string;
    committedAt: string;
    frontierDocument: string;
    ledgerDocument: string;
    ledgerRole: string;
    ledgerCompleteness: string;
  };
  counts: Record<BonsaiTone, number> & { total: number; edges: number };
  health: {
    missingFromMermaid: string[];
    missingFromNodeKey: string[];
    unlinkedNodeIds: string[];
    unknownEdgeNodeIds: string[];
  };
  nodes: FrontierNode[];
  edges: FrontierEdge[];
}
