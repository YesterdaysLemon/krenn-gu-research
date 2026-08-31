export type FieldNoteActivityKind =
  | "started"
  | "exact-check"
  | "independent-audit"
  | "negative-result"
  | "scoped-package"
  | "correction"
  | "withdrawal"
  | "handoff";

export type FieldNoteStatus =
  | "exploratory"
  | "scoped-repository-evidence"
  | "negative-result";

export interface FieldNoteArtifact {
  kind: "commit" | "blob" | "pull-request";
  label: string;
  url: string;
}

export interface FieldNoteEntry {
  activity_kind: FieldNoteActivityKind;
  agent: { name: string; role: string };
  artifacts: FieldNoteArtifact[];
  corrects_entry: string | null;
  entry_id: string;
  global_status: "UNRESOLVED";
  lane: string;
  nonclaim: string;
  recorded_at: string;
  schema_version: 1;
  scope: string;
  summary: string;
  tags: string[];
  typed_status: FieldNoteStatus;
}

export interface FieldNotesData {
  schemaVersion: 1;
  globalStatus: "UNRESOLVED";
  entries: FieldNoteEntry[];
}
