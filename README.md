# Krenn–Gu prize conjecture research

## Status

The global Krenn–Gu conjecture is **UNRESOLVED**. The repository contains
proved reductions, exact finite results, conditional exclusions, route
refutations, experiments, and open obligations. None currently forms a
complete characteristic-zero proof or an exact counterexample to the original
global statement.

**Start here:** [`docs/current-frontier.md`](docs/current-frontier.md) is the
maintained map of the live proof topology, open leaves, and refuted routes.
Owning theorem documents remain authoritative for mathematical statements.

For an interactive projection of that map, run
[`tools/proof-visualizer`](tools/proof-visualizer/README.md). Its bonsai colours
are navigation aids; the exact node text and owning claims remain authoritative.

## The conjecture

Let `n >= 6` be even and `d >= 3`. Assign a complex `d x d` matrix `W_ij` to
each unordered pair of vertices. For a word `a=(a_1,...,a_n)`, define

```text
T_W(a) = sum over perfect matchings M of
         product over {i,j} in M of W_ij[a_i,a_j].
```

The conjecture says that no such weighted graph realizes the diagonal GHZ
tensor

```text
T_W = sum_(c=0)^(d-1) e_c tensor ... tensor e_c.
```

The live symbolic programme is concentrated on the ternary case and on exact
reductions that any hypothetical witness must satisfy. Scope and field
qualifications are recorded in the owning claims and in the current frontier.

## Claim-family navigation

- [Arbitrary-order reductions and boundaries](claims/arbitrary-order/README.md)
- [Finite-order claims and certificates](claims/finite/README.md)
- [P3 restrictions](claims/p3/restrictions/README.md)
- [P4 component programme](claims/p4/README.md)
- [P5 obstruction programme](claims/p5/README.md)
- [P6 claim packages](claims/p6/README.md)
- [P7 claim packages](claims/p7/README.md)

The [`catalog/theorem-ledger.json`](catalog/theorem-ledger.json) is a partial
claim/evidence index. Its empty `dependencies` arrays mean “not recorded,” not
“no dependencies”; it is not the proof DAG.

## Evidence and proof contracts

- [Agent and contributor operating contract](AGENTS.md)
- [Evidence semantics](docs/evidence-semantics-contract.md)
- [Proof-obligation architecture](docs/proof-obligation-architecture.md)
- [Formalization interface](docs/formalization-interface.md)
- [Layout-migration runbook](docs/architecture/layout-migration-runbook.md)

These contracts require exact scope, separate evidence axes, honest
generic-versus-pointwise boundaries, and a proved bridge from any computation
to the mathematical obligation it is claimed to discharge.

## Basic verification

From repository root:

```text
python check_hygiene.py
python -m unittest -v tests.test_migration_tools
python -m unittest -v tests.test_fourteen_vertex_cycle_cover_lattice
```

Run a claim's focused verifier and independent audit from the commands in its
own theorem document. A passing bounded script supports only the scope stated
there; it does not automatically prove an arbitrary-order or global claim.

## Contributing

1. Work in the owning claim package and state the exact obligation, field,
   quantifiers, assumptions, and excluded boundaries.
2. Keep written proof, primary verifier, independent audit, and formalization
   status distinct.
3. Preserve failed and refuted routes when they constrain future work.
4. If a PR changes the live mathematical frontier, update
   [`docs/current-frontier.md`](docs/current-frontier.md). If mathematical
   claims change without altering the live frontier, explicitly state why no
   frontier update is needed.
5. Stage the complete candidate tree before the final hygiene and link checks.

## History and programme audits

- [Repository README chronicle through 2026-08-10](docs/history/repository-readme-chronicle-through-2026-08-10.md)
- [Frontier stabilization snapshot from 2026-08-05](docs/history/current-frontier-stabilization-snapshot-2026-08-05.md)
- [Dated 2026-08-10 symbolic handoff](docs/history/handoffs/SYMBOLIC_PROGRAM_HANDOFF_2026-08-10.md)
- [PR #72–#82 proof-topology audit](docs/audits/PROGRAMME_PROOF_TOPOLOGY_AUDIT_2026-08-10.md)

Historical documents preserve chronology and prior wording. They are not
current authority when they conflict with the maintained frontier or an owning
theorem document.
