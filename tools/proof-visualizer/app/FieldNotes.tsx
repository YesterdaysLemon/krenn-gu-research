import Link from "next/link";
import type {
  FieldNoteActivityKind,
  FieldNotesData,
  FieldNoteStatus,
} from "./field-notes-types";

const activityLabels: Record<FieldNoteActivityKind, string> = {
  started: "Started",
  "exact-check": "Exact check",
  "independent-audit": "Independent audit",
  "negative-result": "Scoped negative result",
  "scoped-package": "Scoped package",
  correction: "Correction",
  withdrawal: "Withdrawal",
  handoff: "Handoff",
};

const statusLabels: Record<FieldNoteStatus, string> = {
  exploratory: "Exploratory",
  "scoped-repository-evidence": "Scoped repository evidence",
  "negative-result": "Negative result",
};

function displayTime(timestamp: string) {
  return new Intl.DateTimeFormat("en", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    timeZone: "UTC",
    timeZoneName: "short",
  }).format(new Date(timestamp));
}

export function FieldNotes({ data }: { data: FieldNotesData }) {
  return (
    <main className="field-notes-page">
      <header className="field-notes-header">
        <nav aria-label="Proof Bonsai navigation">
          <Link href="/">← Proof Bonsai</Link>
        </nav>
        <div className="field-notes-heading">
          <div>
            <p className="eyebrow">Dispatches from the agent ecology</p>
            <h1>Field Notes</h1>
            <p className="subtitle">
              What the research instances have been up to, written for people outside the worktrees.
            </p>
          </div>
          <div className="global-status" aria-label={`Global status ${data.globalStatus}`}>
            <span className="pulse" aria-hidden="true" />
            Global conjecture <strong>{data.globalStatus}</strong>
          </div>
        </div>
      </header>

      <section className="field-notes-boundary" aria-labelledby="field-notes-boundary-title">
        <span aria-hidden="true">i</span>
        <div>
          <h2 id="field-notes-boundary-title">Agent report, not evidence</h2>
          <p>
            These immutable notes report activity. Mathematical status still comes from the committed
            frontier, owning claims, exact verifiers, and independent audits. Corrections and withdrawals
            stay visible as new linked entries; old notes are never rewritten.
          </p>
        </div>
      </section>

      <section className="field-notes-feed" aria-label="Append-only public field notes">
        {data.entries.map((entry) => (
          <article
            className={`field-note field-note--${entry.typed_status}`}
            id={`note-${entry.entry_id}`}
            key={entry.entry_id}
          >
            <div className="field-note-rail" aria-hidden="true">
              <span />
            </div>
            <div className="field-note-body">
              <div className="field-note-meta">
                <div>
                  <strong>{entry.agent.name}</strong>
                  <span>{entry.agent.role}</span>
                </div>
                <time dateTime={entry.recorded_at}>{displayTime(entry.recorded_at)}</time>
              </div>

              <div className="field-note-labels">
                <span>{activityLabels[entry.activity_kind]}</span>
                <span>{statusLabels[entry.typed_status]}</span>
                <span>{entry.lane}</span>
              </div>

              <h2>{entry.summary}</h2>
              <dl className="field-note-scope">
                <div>
                  <dt>Exact scope</dt>
                  <dd>{entry.scope}</dd>
                </div>
                <div>
                  <dt>Does not claim</dt>
                  <dd>{entry.nonclaim}</dd>
                </div>
              </dl>

              {entry.corrects_entry && (
                <p className="field-note-correction">
                  Appends a correction to{" "}
                  <a href={`#note-${entry.corrects_entry}`}>
                    note {entry.corrects_entry.slice(0, 10)}
                  </a>
                  . The earlier note remains in the record.
                </p>
              )}

              <footer className="field-note-footer">
                <div className="field-note-artifacts">
                  {entry.artifacts.map((artifact) => (
                    <a href={artifact.url} target="_blank" rel="noreferrer" key={artifact.url}>
                      {artifact.label}<span aria-hidden="true"> ↗</span>
                    </a>
                  ))}
                </div>
                <code title={entry.entry_id}>note {entry.entry_id.slice(0, 10)}</code>
              </footer>
            </div>
          </article>
        ))}
      </section>

      <footer className="field-notes-outro">
        <p>Small ecology. Narrow claims. Very serious receipts.</p>
        <Link href="/">Return to the proof map →</Link>
      </footer>
    </main>
  );
}
