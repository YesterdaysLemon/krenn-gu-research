# Adversarial review of the complete four-cell detector

## Review status and provenance

This record reviews
[`PROJECTIVELY_CONSTANT_LIFT_COMPLETE_FOUR_CELL_TWO_OPEN_DETECTOR_THEOREM.md`](../../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_FOUR_CELL_TWO_OPEN_DETECTOR_THEOREM.md)
as a conditional characteristic-zero theorem.

Codex performed a fresh line-by-line reconstruction after the locally
transverse four-cell theorem exposed the remaining collision-kernel boundary.
The standard-library audit was separately implemented with a recursive
permanent, integer quotient slices, and a bounded normalized zero-pattern
census.  It imports neither the SymPy verifier nor repository code.  This is
durable adversarial reasoning, not an independent human review.

Review verdict: **accept complete two-open detection in the aligned
projective `q=0,r=4` cell at exactly that conditional scope** after the
focused and repository-wide replay gates pass.  The word “complete” refers
only to affine-gauge detection in this cell.  It is not a witness exclusion,
does not force the aligned/projective hypotheses, and does not change the
global Krenn--Gu status.  The global conjecture remains **UNRESOLVED**.

## 1. Reconstructed obligation

The complete lifted restriction has five source rows and five modes:

```text
P_5(hat h_i,hat h_s,hat h_t,hat a,hat b)
 -> weighted Delta_3.                                 (1)
```

At the new mode `j`, the three persistent rows carry companion covectors,
`hat a_j=eta_j`, and `hat b_j=0`.  The companions span `Ann(x_j)`, of
dimension two.  Choosing an independent pair `ell_(j,s),ell_(j,t)` and
opening the complementary root `i` leaves the two exact replacement tensors

```text
A_s=P_4(h_t,a,a,b),
A_t=P_4(h_s,a,a,b).                                  (2)
```

If the detector vanished, companion independence would force both tensors
in (2) to vanish separately.  This selection remains valid on the effective
tangent plane because restriction maps `Ann(x_j)` isomorphically to
`(ker eta_j)^*`.

The prior transverse theorem proved nonvanishing when every local
`(a_u,b_u)` pair was independent.  The reviewed theorem must remove that
extra assumption without silently treating a normalized local basis as one
common cross-mode basis.  The review explicitly rejected any argument that
used “kernel rows span at most two in normalized coordinates” to contradict
the global root-row span theorem: independent local basis changes do not
preserve cross-mode row span.

## 2. Quotient identity audit

For each outside mode put

```text
S_u=span(a_u,b_u),
Q_u=P_3(a,a,b) on B-{u}.                              (3)
```

Quotient the output at mode `u` by `S_u`.  In the labelled expansion of
`P_4(h,a,a,b)`, every term assigning `h` elsewhere has either `a_u` or
`b_u` at mode `u` and dies.  The remaining terms assign `h` to `u` and are
exactly

```text
[h_u] tensor Q_u.                                    (4)
```

Thus a zero collision and `Q_u!=0` force `h_u in S_u`.  The review checked
the normalization and factorial: `P_4` contributes the factor two from the
two labelled `a` rows, and the same factor is already present in `Q_u`; no
extra scalar appears in (4).

The primary verifier normalizes only the selected local mode and checks all
`4*27` symbolic quotient slices against a labelled `4!` permanent.  The
audit instead uses fixed integer covectors and a recursive permanent.  Both
routes confirm that terms with another `h` assignment vanish in the quotient
and that no companion or graph-sector term has been inserted into this pure
row-replacement identity.

## 3. Four-row Hall capacity

Assume both tensors in (2) vanish and define

```text
Z={u:Q_u=0}.                                          (5)
```

At `u notin Z`, (4) puts both persistent rows `h_s,h_t` in `S_u`.  Apply the
all-subset Hall theorem to

```text
{hat h_s,hat h_t,hat a,hat b}.                        (6)
```

For each of three target colours, its coordinate axis must lie in the span
of (6) at four modes: at least twelve axis-mode incidences.

At mode `j`, the independent companion pair plus `eta_j` spans the whole
three-dimensional dual.  At a nonzero-cofactor mode the span in (6) is
`S_u`, of dimension at most two.  At a zero-cofactor mode it has dimension
at most three.  Hence

```text
12 <= 3 + sum_(u notin Z) dim S_u + 3|Z|.             (7)
```

The review checked each small zero-set case.

- `|Z|=0` gives capacity at most eleven.
- `|Z|=1` forces all three complementary local pairs to have rank two.
  In their product bases, the three possible locations of the `b` row in
  `P_3(a,a,b)` are distinct nonzero basis words, contradicting the one zero
  cofactor.
- `|Z|=2` forces the two nonzero-cofactor local ranks to sum to at least
  three.  At a rank-two mode, flattening either zero `Q` separates the
  coefficient `a_v tensor a_t` from
  `b_v tensor a_t+a_v tensor b_t`.  The two zero cofactors then force one of
  the supposedly nonzero cofactors to vanish, in both cases `a_t=0` and
  `a_t!=0`.

Therefore at least three deletion cofactors vanish.  The primary checks the
flattening coefficient identities symbolically.  The independent audit
enumerates 2,401 normalized rank/zero types as a bounded falsification pass;
the written tensor argument, not that census, proves the arbitrary-field
statement.

## 4. No-common-zero branch

Assume no outside mode has `a_u=b_u=0`.  If one local pair at mode `t` has
rank two, choose two zero cofactors whose deleted modes differ from `t`.
Flattening each at `t` shows that the other two `a` covectors vanish.  Across
the two choices, every `a_u` outside `t` vanishes.  This contradicts the
already proved lifted quota `p_a>=2`.

Thus every local `(a_u,b_u)` span has dimension at most one.  Apply the
all-subset Hall theorem to `{hat a,hat b}`.  It demands two occurrences of
each coordinate axis, hence six incidences.  There are only five modes, and
the selected pair spans at most a line at every outside mode and exactly the
line `eta_j` at `j`; capacity is at most five.  This contradiction forces a
common-zero mode.

The review checked that this argument uses the physical outside support
count `p_a`, not the five-mode support of `hat a`.  It also uses only
dimension capacities for coordinate axes, so it is invariant under the local
bases used in the quotient proof.

## 5. Common-zero branch

Let `a_w=b_w=0`.  Because `hat b_j=0` as well, singleton tricolour cover
forces the three remaining `b` covectors to be nonzero multiples of the
three distinct coordinate axes.

Suppose the surviving deletion cofactor

```text
Q_w=P_3(a,a,b) on B-{w}                              (8)
```

were zero.  Its three-term expansion first forces all three remaining `a`
covectors nonzero: one zero would force a second and contradict `p_a>=2`.
Modewise flattening then forces each `a` proportional to the corresponding
coordinate `b`.

On a constant outside colour `c`, the `b` row is now forced to its unique
mode `u_c`, and the `a` row is forced to the new mode `j`.  The pure
coefficient is

```text
eta_j(e_c) beta_c K_c!=0.                             (9)
```

Recolour only `j` to `d!=c`.  The row-type assignment is unchanged, while
the diagonal target coefficient is zero, forcing `eta_j(e_d)=0`.  The pure
coefficient for colour `d` forces the same value nonzero.  Hence (8) cannot
vanish.

The primary reconstructs all nine `(c,d)` coefficients with a symbolic
`5!` permanent.  The audit uses a recursive integer permanent and arbitrary
nonzero companion entries; those entries never contribute because `a` is
forced to `j`.  This independently checks that no persistent-row-at-`j`
assignment was overlooked.

With `Q_w!=0`, the quotient identity and the two vanished collisions force

```text
h_(s,w)=h_(t,w)=0.                                   (10)
```

At column `w` of the lifted `P_5` table, only `h_(i,w)` can remain nonzero.
The source-column span therefore has dimension at most one.  Every permanent
tensor lies locally in that span, whereas the weighted ternary diagonal has
flattening rank three.  This is the final contradiction.

## 6. Falsified strengthenings and exact scope

The review rejected the following stronger inferences:

- “complete four-cell” does not mean a witness is excluded;
- a nonzero fixed-root detector need not be injective on the two-dimensional
  companion plane;
- the aligned common-two-row factorization and projective shore are still
  hypotheses, not universal conclusions;
- the argument does not extend unchanged to `r>=5`, where a replacement
  tensor retains more than one persistent root row and the four-row Hall
  capacity changes;
- it says nothing universal about `q>=1`, with repeated-row factorials and
  additional persistent rows; and
- an unfactorized outside graph is not represented by the `a/b` quotient.

The exact result is nonzero affine-gauge detection at one complementary root
in the conditional `q=0,r=4` cell, or at every root when all companion pairs
are independent.  Global status remains **UNRESOLVED**.

## 7. Independence and evidence boundary

The primary uses SymPy, labelled permutations, symbolic quotient slices,
symbolic flattening coefficients, and symbolic common-zero recolouring.  The
audit uses only the Python standard library, a deletion-recursive permanent,
fixed integer tensors, direct three-location `P_3` arithmetic, dimension
ledgers, and a bounded normalized type census.  It imports no project module
and no computer algebra.

Neither bounded script proves the arbitrary-field Hall implications, the
zero-set classification, or the recolouring contradiction.  Those are the
written characteristic-zero arguments reviewed above.

## 8. Exact acceptance boundary

Accepted:

- the collision quotient identity;
- at least three zero deletion cofactors under detector invisibility;
- reduction of that extreme zero pattern to a common outside `a/b` zero;
- nonvanishing of the surviving cofactor at a common zero;
- the local-concision contradiction; and
- nonzero two-open detection in the full aligned projective `q=0,r=4` cell.

Still open:

- fixed-root injectivity;
- existence or exclusion of a witness in the cell;
- `q=0,r>=5`, every `q>=1` cell, and the unfactorized branch;
- universal extraction/gluing; and
- the global Krenn--Gu conjecture.

## Replay record

Before publication, run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_complete_four_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_complete_four_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_complete_four_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_four_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_complete_four_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_four_cell_detector.py
```
