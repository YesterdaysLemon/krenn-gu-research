# Cancellation-to-physical sprint handoff — September 13, 2026

## Outcome

This sprint completed the finite `n=10` recursive zero-pattern (RZP) result as
an auditable theorem and connected guarded quotient and row-space algebra to a
small physical-source core. The global Krenn–Gu conjecture remains
**UNRESOLVED**.

The owning finite theorem is
[`TEN_VERTEX_ALL_DIAGONAL_RECURSIVE_HAFNIAN_EXCLUSION_THEOREM.md`](../../claims/finite/n10/TEN_VERTEX_ALL_DIAGONAL_RECURSIVE_HAFNIAN_EXCLUSION_THEOREM.md).
It proves only that no ternary complex all-diagonal witness exists at exactly
ten vertices. It does not prove AP' unsatisfiable at `n=10`, cover
bichromatic edge entries, or supply an arbitrary-order theorem.

## Evidence completed

- Thirteen CNF/binary-DRAT pairs cover the chosen perfect-matching normal
  forms exhaustively and replay `s VERIFIED` with the pinned checker. Each
  case also passes one positive and two false-proof controls.
- The independent standard-library audit reconstructs every CNF byte, all
  seven pair cycle types, and explicit transporters for all 945 perfect
  matchings. It imports neither the repository encoder nor a SAT library.
- The portable archive `n10-all-diagonal-rzp-20260913-v2.zip` is 282,243,424
  bytes with SHA-256
  `80c3a2cd5ec1d76e9b325fbc060b385198115b76d1ec78d2b4fd328b1d21fd04`.
  Its unpacked replay and audit receipts have SHA-256
  `41af58d23ec7f74f201af52a2e008c2a5f54ee8048ff39d13afad49f8640e807`
  and
  `7fdfaef892ecb0880a7891cc279a3ae3496c87d253c59e8b56b084f86fa0db59`.
  The archive remains outside ordinary Git; distribution is a separate owner
  action.

## Physical-support refinement completed

The typed source-algebra boundary now accepts exact recursive quotient,
binomial-kernel, and Laurent row-space certificates, reconstructs the
certificate-specific guarded clause, and permits only regenerated base
clauses, that one clause, and explicit physical-entry units in the final
solver-free RUP core.

The integration controls are recorded in
[`physical-support-refinement-sprint-2026-09-13.md`](physical-support-refinement-sprint-2026-09-13.md).
The material delta is:

- a 43-literal `n=6` physical projection of the stored row-space certificate;
- a 27-literal physical cut, with no killers or ratio clauses, excluding the
  prior 136-entry `n=8` support while leaving all proper cofactor supports
  free; and
- a cumulative four-cut parent-orbit test that is still SAT and returns a new
  134-entry Boolean physical support.

The last item is not a weighted witness. It shows only that the four checked
physical cuts and their allowed vertex/global-colour symmetries do not cover
the recursive parent necessary model.

## Next load-bearing question

Keep the all-order supplied-family problem as the parent target. For each
colour `c`, the nonempty family

```text
U_c = {U subset V : |U|=4 and haf(Z^c[V-U]) != 0}
```

must be combined across all three colours with recursive accessibility,
four-set coverage, and signed-ratio transport. A useful next result would be
either a proved incompatible cancellation system or an exact globally
constrained countermodel that identifies the missing hypothesis. Another
isolated finite support census is not, by itself, progress on this parent.

## Reproduction and process state

Focused source-core, quotient, row-space, and RZP tests pass. The independent
thirteen-case audit passes from the unpacked portable archive. Repository
hygiene and migration-floor commands should be rerun from the index-complete
candidate immediately before any later publication or PR.

No research process launched by this sprint is left running. No remote push,
PR, or publication was performed.
