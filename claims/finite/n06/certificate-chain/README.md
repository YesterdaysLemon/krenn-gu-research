# Order-six certificate chain

This directory holds the finite order-six certificate, orbit, separator,
prism, replay-CNF, and exact checking machinery that formerly formed one
connected executable/provenance graph at repository root.  The shared
cross-family helper closure lives separately in `src/krenn_gu`; operator-only
entry points live in `tools/explore`.

The historical theorem-ledger evidence model remains a certificate chain,
not a newly manufactured primary/audit pair.  Modular, SAT, Laurent, and
Singular artifacts retain their stated scopes and do not establish a global
case cover.  The global conjecture remains **UNRESOLVED**.

## Lifecycle and replay boundary

The authoritative status source is
[`../SIX_VERTEX_CERTIFICATE.md`](../SIX_VERTEX_CERTIFICATE.md). Its accepted
top-level audit is the repaired, fail-closed fallback-free chain: all 18
pattern replays, both gauge partitions, all 48 `K3,3` DRAT proofs, and the
final CNF/proof hash audit. The older four-Singular global-pattern manifest
remains a valid independent cross-check, but the fallback-free linear-monomial
manifest supersedes it in the top-level audit. Two still-earlier checkpoints
remain **superseded**: the exact-fallback driver that stopped after its first
torus chart, and the prism normalization with reversed singleton orientation.
Preserving their carriers here records provenance; it does not restore either
checkpoint or turn the cross-check into the accepted primary chain.
