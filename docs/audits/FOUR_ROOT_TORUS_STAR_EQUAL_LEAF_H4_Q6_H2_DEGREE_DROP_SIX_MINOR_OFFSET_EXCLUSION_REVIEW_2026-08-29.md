# GLD99 H2 degree-drop six-minor offset exclusion review

## Verdict

Verdict: PASS for the exact `GLD99` scope.  The owner document may carry the
status **Proved exact scoped characteristic-zero theorem (`GLD99`).**  This
review validates a scoped proof leaf and its two exact replays; it does not
close any upstream or downstream obligation outside that leaf.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Exact claim audited

The audited statement is the normalized, scale-fixed equal-leaf `H4` chart
written in the GLD88/F88 offset coordinates

```text
b = b88(p,q,a) + B,
c = c88(p,q,a) + C.
```

It imposes the degree-drop component

```text
H2 = 2p^2 - 2p + 1 = 0,
Q6 = 0,
```

and works only on `D(Delta)`, where
`Delta=(p-q)(p+q-1)P L1 L2 e`.  The coefficient field is characteristic zero,
extended to `Q(i)` to split `H2`; `a`, `B`, and `C` remain polynomial
coordinates.  The `d0=p+q-1` component is excluded by `D(Delta)`, not
silently inverted in `Q(i)[q]/(Q6)`.  The assertion is that full GLD71
syndrome rank at most six makes the six selected seven-minors vanish, and
their exact polynomial memberships then force `B=C=0` on this chart.  GLD95
is a separate endpoint used only for the resulting F88 incidence.

This review makes no claim for arbitrary `p`, arbitrary `H4/Q6` points outside
the written F88 offset chart, `Delta=0`, `R31=0` by a new localization,
`E31=0`, `g0=0`, the GLD83 Fitting pullback, other charts or components,
source integrability, graph lifting, roots or orders.  In particular, no
`R31`, `E31`, or `g0` factor is used or inverted here.

## Authoritative replays

The primary replay is
[`verify_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py`](../../claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py).
Its final run is `gld99-h2-primary-final-2`, with script-reported elapsed time
`170.196` seconds and child exit code `0`.  It reconstructs the GLD71
`37 x 9` syndrome and GLD88 family, checks the factorization and all
denominator gates, recomputes both quadratic branches, and verifies the exact
Macaulay memberships.

The independent replay is
[`audit_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py`](../../claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py).
Its final recorded run directory is `gld98-h2-audit-final` (a historical
mislabel for this GLD99 audit); the reproduction command below uses the
semantic run ID `gld99-h2-audit`.  The recorded run has script-reported
elapsed time `476.513` seconds, runner wall time `480.331` seconds, and child
exit code `0`.  It uses copied immutable supports and formulas, direct sparse
determinants, local quotient arithmetic, and independent Gaussian-rational
RREF.  It imports neither the primary verifier nor GLD71, GLD88, GLD96, or
the GLD98 exploratory census.  The final line is
`H2 degree-drop six-minor membership audit: PASS`.

Both replays report the two branches independently.  The minus branch is
accumulated and RREF-checked rather than inferred from conjugation; the
coefficientwise conjugation relation is an additional cross-check.  The
primary canonical-builder probe checks `333` entries and the `37 x 9`
syndrome shape.  The audit separately confirms its copied input relations
against the canonical GLD71/GLD88/GLD96 builders in the evidence test below.

## Exact certificate surface

The common sparse support is rows
`(0,1,2,3,17,25,28,31,32,33)` with support digest
`c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0`.
The fixed pivot rows are `(0,1,2,17,25,31)` and the fixed pivot columns are
`(0,1,3,4,6,7)`.  The six selected minors are `T0,T1,T2,T3,D0,D2`.
Every one has total `BC` degree `3`; `D0` and `D2` have a genuine `C^2`
term, while `T0,T1,T2,T3` have `C` degree `1`.  The `a` degrees are `2,3,3,2`
for `T0,T1,T2,T3` and `2,2` for `D0,D2`.

For each branch, the exact coefficient system has `158` rows, `144` columns,
and rank `140`; adjoining either target column still has rank `140`, with an
exact zero residual for both `B` and `C`.  The multiplier ansatz has `a`
degree at most `3`, `BC` degree at most `1`, and uses the ordered quotient
basis `(1,q)`.  The branch-specific payload and certificate hashes are:

| branch | `p` | `T0` | `T1` | `T2` | `T3` | `D0` | `D2` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `+` | `(1+i)/2` | `c66046efa2e34a5cff341e5edb6deccc0fab008fd5fe4ff89f458abf5ebc2e4e` | `106ebfdaf5c6aea5f4f5d844ad170d3be4be45dcb10a73cedd57721c1754d83f` | `7e562e95ae2a740d76469338204cf942903d025c264c81987d5a7cc687c52adb` | `f5576f4d76055fe5cea933ca4bd2fa9b2a4279a0f92155b8b5143fd60938019f` | `463c8a46c7583204a8cbefa5fb0dae6c46af86105d45a5f2d27658e183ed9ace` | `e311a0588bc91f96530de1799ee05a829fce5999ed246a3cfc3cea926ee9e936` |
| `-` | `(1-i)/2` | `aab9bf74f768c5e8aabadf988e7a795556a432a2c7b3b808eb4c08c71f6d8aa7` | `8c3b58a67a46f3159c64fe42e2902a8eb973db07a869dc41a37136dbf5db935b` | `68c0a116dfc57bbb4ac72c5750f3d821977cbd78b168ce27de2a116d1f43c06d` | `0fd46d37b59d76b6a3224a1a15006a80fbc2e862e634ae6d8b7be29ea7229bbf` | `af0791f41ea378e8045902b90ced9167af1551633cfe94fe8e62f50bc5c3b3f3` | `856831444749d5b033247401445313384fc4789ab9184c97e19b13f130324445` |

The exact certificate hashes for the target memberships are:

| branch | target `B` | target `C` |
| --- | --- | --- |
| `+` | `da5154181e031400a933d6ecb2e4b82dbaf6c3d9b7c11dc557cf20740546b9e3` | `e52ba0af1cc4c2b65a9849bebe6c8414f75eb64dbb42ae4879464d3ee3213e35` |
| `-` | `837adda0446d760cc959890eef072b600fc93dc9ca3f2a837bbd256a8be82cf0` | `7143e9974307c5855ebe438433ffe0776cc187b05883f0453ae5672efd94774a` |

The H2/Q6 factorization payload is pinned by
`72c0f82d284e3fdbf977e20827a5a21ec811f1ddb4b8826d369b35bd149ac86b`.
The two quadratic `q` factors both have discriminant `-6`; the `d0` factor
is the component removed by `D(Delta)`.

## Adversarial repair record

The final PASS follows explicit repairs and controls:

1. A stale degree-four claim was corrected: all six minor payloads have total
   `BC` degree `3`, not `4`.  This correction retained the genuine `C^2`
   terms in `D0,D2` instead of weakening the shape claim.
2. The primary kernel counter and Matrix indexing preflight fixes were applied
   before the final run.  The canonical-builder probe now checks all `333`
   expected entries, and the exact branch certificates use the corrected
   coefficient indexing.
3. The first final-audit implementation exposed a tuple-add residual in the
   exact RREF check.  The tuple-add residual fix was applied; the final audit
   reports zero residual for both targets on both branches.
4. Generator payloads and target certificates are pinned branch by branch.
   This branch-specific certificate pinning is checked independently; plus
   and minus hashes are not substituted for one another merely because the
   payloads are conjugate.
5. There is no optional hash bypass.  The support, generator, and certificate
   hashes are fail-closed constants in both replay programs and are checked
   by the evidence test.
6. A T-only degree22 residual was explored as a diagnostic shortcut/control;
   it is not used in the theorem.  The final result uses all six generators
   and the uniform symbolic-`a` membership system, with no T-only shortcut.

Earlier failed or timed-out attempts remain run outcomes, not proof evidence:
the stale degree-four assertion, primary Matrix-indexing preflight, and the
early audit tuple-add residual were repaired; a path-recovery run and later
diagnostic probes also failed or timed out.  In particular, failed runs are
not evidence.  Only the named final primary and final independent audit runs
support this review.

## Retained obligations

The result is a scoped exact theorem/proof leaf for the normalized H2 degree
drop.  It does not provide an exhaustive cover of the global Krenn--Gu
problem.  The current frontier must retain the `E31/g0/Delta` residual after
GLD96, arbitrary H4/Q6 points outside F88, `Delta=0`, the GLD83 Fitting
pullback, other charts/components/source branches, and all global
integrability and extraction obligations.  GLD95 remains a separate endpoint;
its existence does not broaden GLD99's scope.

The owner status, this review, the live frontier, both claim READMEs, the
verified theorem-ledger entry, and the evidence-status test are the durable
integration surface.  The ledger pins the staged owner-document hash and
distinguishes the algebraic `D(Delta)` endpoint from the physical
`D(Omega Delta)` incidence exclusion.
