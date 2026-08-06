# Merge audit report: `72780ac` (former `main` into the canonical line)

Stabilization pass, 2026-08-05.  This report records, for every file
that conflicted in merge commit `72780ac`, what each parent contained,
how the conflict was resolved, and whether the resolution is coherent
with the rest of the merged tree.  No claim here is taken on faith;
every statement below was re-derived from the git objects on this
checkout.

## Merge shape

- Merge commit: `72780ac`, parents
  `b6f24b5` (canonical line, former `codex/local-to-global-bottleneck`)
  and `21f77b3` (former `origin/main`, tip of PR #26).
- Fork point: `9ef09cc` (2026-07-30).  At merge time the canonical
  line was 380 commits ahead of the fork point and former `main` was
  46 commits ahead (PRs #3–#26: components 9–16, obligation ledger,
  divisor atlas, meta-theorem).
- Conflict count: 9 files.  All nine are in the disjoint mixed-star
  (eighth-component) track, which **both** lines developed
  independently in parallel.

## Resolution provenance

Every conflict was resolved to the **canonical-line parent's version**
(merge "ours").  Verified by hash comparison of the merge result
against both parents:

| File | Resolution |
|---|---|
| `P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md` | canonical |
| `P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | canonical |
| `P5_H22_DISJOINT_MIXED_STAR_WORKING_NOTE.md` | canonical |
| `P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | canonical |
| `P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md` | canonical |
| `README.md` | canonical |
| `RESEARCH_NOTES.md` | canonical |
| `audit_p5_h22_disjoint_mixed_star_component_generic_obstruction.py` | canonical |
| `verify_p5_h22_disjoint_mixed_star_component_generic_obstruction.py` | canonical |

Rationale at the time: the canonical line is a strict continuation —
its eighth-component documents include everything the former-main
versions claim **plus** the boundary programme (equal/opposite-weight
slopes, parameter pivots, coupled slope divisor, coefficient-quadratic
branch, linear slopes, torus quotient).  Per-file verification:

- **H31 doc**: branch-side adds ninth-component cross-links and the
  nine-component census note; former-main's eight-orbit claim is
  subsumed.  No dropped claim.
- **P4 component doc**: branch-side adds the affine/projective
  classification, components 9–10 cross-links, and five boundary
  theorem links.  Former-main's two targets are both addressed.  No
  dropped claim.
- **Working note**: branch-side keeps the supersession statement and
  the boundary-theorem chain; former-main's shorter supersession
  paragraph is subsumed.  No dropped claim.
- **Frontier doc**: branch-side carries the deeper continuation text;
  the former-main text it replaces was an interim state ("closed for
  `H31`, not yet for weighted `H22`") already superseded by both
  lines' later `H22` theorems.  No dropped claim.
- **Verifier/audit scripts**: the two lines contain **different
  proofs** of the same theorem (see below).  The canonical pair was
  kept as primary; the former-main pair is now restored as the
  alternate package.

## The one real collision: two proofs of the same theorem

Both lines independently proved the same statement — *the generic
weighted `H22` incidence of the eighth (disjoint mixed-star) component
is empty over `C`* — by materially different computations:

| | canonical line (kept as primary) | former `main` (recovered as alternate) |
|---|---|---|
| Marking locus, `D_01^r` | determinantal marking chart: seven selected `8 x 8` minors give a degree-five scheme; a `7 x 7` pivot is invertible on it; cover `t_2=0`, `t_1=t_3=0`, `t_1=L_3=L_2=0` | `t`-free linear elimination of the four marked extensions (`14 x 8` mixed system → exact `10 x 4` system `G(t)x=0`); one factored `4 x 4` minor `det G = u · t_1 t_2 (mod Phi)` with two sheet refinements giving four strata |
| Marking locus, `D_23^r` | seven selected minors force `t_1=t_2=t_3=0` | three unit-ideal chart certificates (`t_i != 0`) on all `4 x 4` minors of `G` |
| Ternary lift | one/two-minor ternary Fitting ideals unit on three charts | five two-minor Fitting strata unit on the four `01` strata and the `23` line |
| Shared inputs | component field `K=C(a,b,f)[phi]/(Phi)`, the two weighted pencils `D_01^r,D_23^r`, the "rank-four one-marked contraction" necessity from the `H22` reduction | same |
| Files | `P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`, `verify_..._obstruction.py`, `audit_..._obstruction.py` | `P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION_ALTERNATE.md`, `verify_..._obstruction_alternate.py`, `audit_..._obstruction_alternate.py` |

Overlap (identical claims): the component field and `Phi`, the weighted
pencil definitions, the two marking loci `t_1 t_2 = 0` (`01` pencil)
and `t_1 = t_2 = t_3 = 0` (`23` pencil), the rank-four one-marked
contraction obstruction, the dense-open conclusion, and the honest
frontier (special parameter/slope divisors, projective boundary, and
exhaustiveness all open).

Independence: no code or algebraic certificate is shared between the
two packages.  The canonical verifier imports
`p5_high_coordinate_tree_chart_cegar` and
`verify_p4_disjoint_mixed_star_pure_component`; the alternate verifier
is fully self-contained (imports only stdlib + sympy) and rebuilds the
family from its own `ALPHA`/`BETA` bases.  The two audits are likewise
independent (the canonical audit imports the `H31` audit module; the
alternate audit is self-contained).  Their modular corroboration uses
different component points.  Neither proof depends on the other's
Singular transcripts.

## Replay evidence (this machine, stabilization pass)

- **Alternate verifier**: `verified: true`, every Singular unit-ideal
  certificate replayed, wall time 1327 s.  Singular 4.3.2 invoked via
  WSL (`wsl.exe` on this Windows checkout).
- **Alternate audit**: `audited: true`, `independent_of_primary_imports:
  true`, finite-field censuses at moduli 11 and 13, wall time 167 s.
- **Canonical verifier**: **not** replayed in this pass (it requires
  its import chain plus Singular; see the candid audit section of
  `CURRENT_FRONTIER.md`).  Its status is unchanged by this merge
  audit; it was the primary on the canonical line before the merge.
- **Canonical audit**: not replayed in this pass.

## Known consequences of the branch-side resolution

Two documentation consequences, both repaired in this pass:

1. **README certificate index lost 15 former-main links.**  The
   branch-side README never contained the components 9–16 narrative or
   the ledger/atlas/meta-theorem links, and the branch-side resolution
   carried that forward.  Repaired: the former-main narrative is
   restored as an appendix section ("Former `main` line contributions
   carried through the merge") and all 15 documents are linked.
2. **`RESEARCH_NOTES.md` lost the former-main eighth-component
   weighted-`H22` section** (the `t`-free elimination narrative).
   Repaired: restored verbatim as a section explicitly labeled the
   alternate proof, pointing at the `*_ALTERNATE` package.

## What this audit does not claim

- It does not adjudicate which proof is better; both are exact.
- It does not replay every certificate in the merged tree — only the
  alternate package, because its survival was the merge's only
  contested content.
- It does not change any theorem statement.  The global conjecture
  remains **UNRESOLVED**.
