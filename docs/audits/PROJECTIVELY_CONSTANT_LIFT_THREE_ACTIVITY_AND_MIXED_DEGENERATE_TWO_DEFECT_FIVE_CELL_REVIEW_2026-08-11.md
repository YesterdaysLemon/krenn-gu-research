# Adversarial review of the three-activity two-defect detector

## Review status and provenance

This record reviews
[`PROJECTIVELY_CONSTANT_LIFT_THREE_ACTIVITY_AND_MIXED_DEGENERATE_TWO_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md`](../../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_THREE_ACTIVITY_AND_MIXED_DEGENERATE_TWO_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md)
as a conditional characteristic-zero theorem and residual reduction.

Codex reconstructed the three-activity companion cases, the exact one-sided
collision kernels, the zero-mode transport, the mixed-kernel intersection,
and the same-type survivor ledger independently of the primary script.  The
standard-library audit separately uses rational elimination, direct labelled
permanents, and polarized rank-one-subspace checks.  This is durable
adversarial reasoning, not an independent human review.

Review verdict: **accept complete two-open detection for the `AB`, `AZ`,
`BZ`, and `ZZ` two-degenerate-defect cells**, after the focused and
repository-wide replay gates pass.  The `AA` and `BB` cells are reduced to
an overlapping double-kernel boundary but remain open.  Every cell with
three or more defects remains open.  No witness is excluded, and global
Krenn--Gu remains **UNRESOLVED**.

## 1. Reconstructed obligation

The preceding theorem closes one arbitrary defect and two defects when one
is a nonzero proportional `a/b` pair.  The remaining two-defect types are
built from

```text
A: a!=0,b=0;       B: a=0,b!=0;       Z: a=b=0.      (1)
```

The old four-active local lemma is not enough because each retained
collision operator now has a genuine kernel.  The reviewed proof must:

1. lower the universal activity threshold from four to three;
2. determine the exact `A/B/Z` collision kernels;
3. use two modes jointly rather than treating their inactive roots
   independently; and
4. preserve `AA` and `BB` if the resulting kernel crowding does not itself
   contradict the fixed layer.

## 2. Three-activity companion audit

At a dependent mode set

```text
v_p=pi(h_(p,u)),       r_p=R_(p,u),
F_pq=v_p tensor r_q+v_q tensor r_p.                  (2)
```

The review checked all companion degeneracies.

- On a good frame, all pair tensors vanish.  Centering at one active root
  makes every quotient vector zero or proportional to the center.
- With one zero companion, its incident star vanishes and the remaining
  triangle lies in one fixed tensor line.  If the zero-companion root is
  inactive, three-activity makes all other `r_p` nonzero.  The triangle
  tensor-line lemma then forces their quotient vectors into one line.
- With two zero companions, only the pair joining the two nonzero-companion
  roots may survive.  Three active roots include a zero-companion root, whose
  zero incident star gives the line directly.
- On a balanced frame, the two within-pair tensors vanish and the four cross
  tensors lie in one line.  With exactly three active roots, the inactive
  endpoint has zero quotient vector; one cross tensor vanishes, hence all do.
  Independent pair lines would then make the active cross tensor nonzero.
  With four active roots, the previously reviewed `A+E` versus `-A+E`
  argument applies.

The triangle sublemma was checked without assuming generic coefficient
support.  If two quotient vectors were independent, the corresponding
tensor-line coefficient cannot vanish.  Dual selectors put the third vector
in their span and produce two opposite formulas for its nonzero retained
tensor, forcing it to vanish in characteristic zero.  Thus three active
deletions always give quotient span at most one.

Since `dim span(a_u,b_u)<=1`, the five fixed-layer source rows then have
local span at most two, contradicting the weighted diagonal's rank-three
flattening.

## 3. Exact collision-kernel audit

On three transverse modes define `Q=P_3(a,a,b)`, which is nonzero by a
single one-`b` product-basis coefficient.  At the special fourth mode, direct
labelled expansion gives:

```text
K_A = K(-2a_0,a_1,a_2,a_3),                           (3)

K_B = {h_0=-gamma b_0,
       h_i=alpha_i a_i+gamma b_i,
       alpha_1+alpha_2+alpha_3=0},                    (4)

K_Z = {h:h_0=0}.                                      (5)
```

For `B`, the expansion is

```text
P_4(h,a,a,b)=h_0 tensor Q+b_0 tensor P_3(h,a,a).     (6)
```

Quotienting the special mode and comparing pure/one-`b` words gives (4).
For `Z`, only the assignment of `h` to the special mode survives, giving
`h_0 tensor Q`.  The `A` coordinate equations leave exactly (3).

The primary and audit independently recover ranks `11,9,3` and nullities
`1,3,9`, and check explicit bases rather than only the dimensions.

## 4. Zero-containing pairs

Let defect `u` be zero and `v` be the other defect.  The fixed `P_5` layer at
`u` has `b_u=0` but local rank three, so at least three root covectors
`h_(p,u)` are nonzero.  Deleting `v` leaves the zero mode `u`; every retained
collision tensor factors exactly as

```text
R_(p,v)=h_(p,u) tensor P_3(a,a,b; three transverse modes).   (7)
```

Hence `v` is three-active and the local lemma detects.  This proof treats
`AZ`, `BZ`, and `ZZ` uniformly and does not infer that a zero defect is
itself impossible.

## 5. Mixed `AB` kernel intersection

If a root is inactive after deleting the `B` defect, its retained `A` chart
has the pattern

```text
h_A=-2lambda a_A,       h_t=lambda a_t.              (8)
```

If it is also inactive after deleting the `A` defect, its retained `B` chart
has

```text
h_B=-gamma b_B,
h_t=alpha_t a_t+gamma b_t,
sum_t alpha_t=0.                                      (9)
```

Transverse independence gives `gamma=0` and every `alpha_t=lambda`; the sum
condition gives `3lambda=0`.  Thus the common kernel is zero.

Under collective invisibility, each defect has at least two inactive roots.
No full-span root can lie in the zero common kernel, so the inactive sets are
disjoint complementary pairs.  At every transverse mode, (8)--(9) put all
four roots and `b_t` in `span(a_t,b_t)`, contradicting local rank three.
This closes `AB`.

## 6. Same-type survivor audit

For `AA` or `BB`, each inactive set again has size at least two.  Every root
inactive at either defect lies in the local `a/b` plane at all three
transverse modes.  If the two inactive sets covered all four roots, the fixed
layer would have local rank at most two.  Therefore they must overlap and
their union must be proper.  In particular there is both a root inactive at
both defects and a root active at both.

Intersecting two copies of (3) or (4) gives the exact common kernels:

```text
AA: h=(-2lambda a_A,-2lambda a_A,lambda a_t,lambda a_t,lambda a_t),

BB: h_B=-gamma b_B at both defects,
    h_t=alpha_t a_t+gamma b_t,       sum_t alpha_t=0. (10)
```

These families have dimensions one and three.  Neither the written proof nor
the finite checks exclude them.  Recording them as the live boundary is
therefore necessary, not conservative wording around a hidden closure.

## 7. Independence and evidence boundary

The primary uses SymPy collision matrices, exact nullspaces, 150 activity
charts, all six common-kernel intersections, and a finite inactive-set
ledger.  The audit imports no repository code and no computer algebra; it
uses rational row reduction, 240 independently assembled activity charts,
explicit kernel bases, and a separate set census.

Neither finite chart family proves the arbitrary-field companion cases.  The
written tensor-line selectors, labelled collision expansions, kernel
intersection, and local flattening arguments carry that implication.

## 8. Exact acceptance boundary

Accepted:

- three active deletions detect at any dependent mode for every companion
  frame;
- exact `A/B/Z` retained collision kernels;
- complete detection of `AZ`, `BZ`, and `ZZ`;
- complete detection of mixed `AB`; and
- the overlapping double-kernel reduction for `AA` and `BB`.

Still open:

- exclusion or detection of the `AA` and `BB` double-kernel survivors;
- every cell with at least three local defects;
- fixed-root injectivity and existence or exclusion of a witness;
- `q=0,r>=6`, every `q>=1` cell, and the unfactorized branch;
- universal extraction/gluing; and
- the global Krenn--Gu conjecture.

## Replay record

Before publication, run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_three_activity_two_defect_five_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_three_activity_two_defect_five_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_three_activity_two_defect_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_three_activity_two_defect_five_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_three_activity_two_defect_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_three_activity_two_defect_five_cell_detector.py
```
