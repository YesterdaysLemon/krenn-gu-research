# Adversarial review of the transverse four-cell detector

## Review status and provenance

This record reviews
[`PROJECTIVELY_CONSTANT_LIFT_TRANSVERSE_FOUR_CELL_TWO_OPEN_DETECTOR_THEOREM.md`](../../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_TRANSVERSE_FOUR_CELL_TWO_OPEN_DETECTOR_THEOREM.md)
as a conditional characteristic-zero theorem.

Codex performed a fresh line-by-line reconstruction after identifying the
four-mode collision operator as the first larger-cell cofactor with only one
persistent root row.  The standard-library audit was separately implemented
from labelled row assignments and an explicit rational left inverse.  It
imports neither the SymPy verifier nor repository code.  This is durable
adversarial reasoning, not an independent human review.

Review verdict: **accept collision injectivity and the conditional
`q=0,r=4` detector at exactly their stated locally transverse scope** after
the focused and repository-wide replay gates pass.  Do not infer local
transversality from the lifted diagonal equation, do not call the fixed-root
map injective, and do not change the global Krenn--Gu status.  It remains
**UNRESOLVED**.

## 1. Reconstructed obligation and imported surface

The prior single-open theorem gives, on the aligned common-two-row and
projectively constant branch, an exact consecutive restriction

```text
P_(r+1)(hat h_(v!=j),hat a,hat b) -> weighted Delta_3
```

at `q=0`.  Its companion covectors at `j` span the two-dimensional
annihilator of `x_j`.  The prior minimum-cell theorem transported this frame
through `P_3(a,a,b)` only at `r=3`.

The reviewed obligation is the next cell `r=4`.  For an opened root `i`, two
other roots `s,t` remain in the companion sum, and the exact cofactors are

```text
A_(i,j;s)=P_4(h_t,a,a,b),
A_(i,j;t)=P_4(h_s,a,a,b).                             (1)
```

The candidate lemma adds one explicit condition:

```text
rank(a_u,b_u)=2             at every outside mode u. (2)
```

The review found no upstream theorem forcing (2).  It is therefore retained
as an assumption, not described as generic on the hypothetical-witness locus,
and listed in the exact frontier.

The fixed `q=0,r=4` contraction is

```text
P_4(h_i,h_s,h_t,b) -> weighted Delta_3.               (3)
```

The arbitrary-surplus full-span theorem applies directly to (3), so each
persistent `h` family spans the target dual across the four blocker modes.
The reviewed proof needs only that `h_s,h_t` are nonzero, but importing the
stronger theorem at its proved scope is legitimate.

## 2. Collision convention and factor audit

At each mode, condition (2) allows completion to a local dual basis
`(a_u,b_u,c_u)`.  Write

```text
h_u=x_u a_u+y_u b_u+z_u c_u.                          (4)
```

The labelled-row permanent has two identical `a` rows.  Once the `h` row is
assigned to mode `u` and the `b` row to a distinct mode `v`, the two `a`
assignments can be exchanged.  Thus

```text
P_4(h,a,a,b)
 =2 sum_(u!=v) h_u tensor b_v tensor a_(other two).   (5)
```

The factor `2` is load-bearing only through its nonvanishing in
characteristic zero.  The primary verifier reconstructs (5) from all `4!`
labelled row assignments in an `81 x 12` coefficient matrix.  The independent
audit performs the same labelled enumeration without a permanent helper,
SymPy, or project imports.

The review checked that no forbidden cross-mode identification is used.
Each `(a_u,b_u,c_u)` is a separate basis in its own local dual space.  The
letters merely label product-basis selectors.

## 3. Injectivity reconstruction

Assume (5) vanishes.

1. Select `c` at mode `u`, `b` at a different mode `v`, and `a` elsewhere.
   Only the `z_u` term survives, with coefficient `2z_u`; hence every
   `z_u=0`.
2. Select `b` at exactly modes `u,v` and `a` elsewhere.  The coefficient is
   `2(y_u+y_v)`.  All pair sums vanish.  Three pair equations on any triple
   force `2y_u=0`, and all four `y` coordinates vanish.
3. Select `b` only at mode `v`.  The coefficient is
   `2 sum_(u!=v)x_u`.  With `S=sum_u x_u`, every equation says `x_v=S`.
   Summing gives `3S=0`, hence every `x_v=0`.

This proves the collision map injective.  The argument divides only by `2`
and `3`, so characteristic zero is more than sufficient.

As a certificate of convention, the primary selects four `z` equations,
four independent `y` pair equations, and all four `x` complement equations.
The resulting normalized `12 x 12` minor has absolute determinant `24576`.
The no-import audit instead constructs a left inverse:

- read each `z_u` directly;
- recover the four `y_u` from pair sums using one triangle and a fourth edge;
- recover `S` as one third of the sum of the four complement sums and then
  set `x_v=S-(S-x_v)`.

It recovers all twelve basis vectors and a dense signed integer test vector
exactly with `Fraction` arithmetic.  This is a different verification route
from symbolic rank and determinant computation.

## 4. Companion deletion and tensor noncancellation

There are three companion covectors at `j`, spanning a two-dimensional
space.  Therefore at least one pair, say `ell_(j,s),ell_(j,t)`, is
independent.  Choosing `i` as the complementary root leaves exactly that pair
in the two-open sum.  This is a selection by a nonzero `2 x 2` minor, not an
assumption that every companion is nonzero or every pair is independent.

By full span, `h_s,h_t` are nonzero.  Collision injectivity gives both
cofactors in (1) nonzero.  Since the companion covectors are independent,

```text
ell_(j,s) tensor A_(i,j;s)
 +ell_(j,t) tensor A_(i,j;t)                          (6)
```

cannot vanish: a dual selector can isolate either summand.  No independence
between the two `A` tensors is needed for this nonzero conclusion.

The review separately checked the tangent-plane restriction.  Every
companion annihilates `x_j`, while `eta_j(x_j)=1`.  Hence

```text
L_j=<x_j> direct-sum ker eta_j
```

and restriction maps `Ann(x_j)` isomorphically to `(ker eta_j)^*`.  The
independent pair therefore remains independent on the effective two-open
domain.  There is no possibility that (6) is nonzero on the full local space
but vanishes on every allowed tangent input.

## 5. Detection versus injectivity

On the projectively constant branch, the imported defect row is zero and the
complete affine variation is

```text
delta T_ij=tau kappa_i tensor (6).                    (7)
```

For every nonzero absorption covector `kappa_i`, equation (7) is nonzero.
Thus the gauge is detected at the complementary root selected above.

The two cofactor tensors in (1) might nevertheless be proportional.  In that
case the map from the two-dimensional companion plane has rank one.  The
review rejected the stronger wording that the fixed-root map is injective.
If all three companion pairs are independent, the same nonzero argument can
be repeated for all three choices of `i`; this still does not prove any one
of the three maps has rank two.

## 6. Falsified strengthenings and boundary checks

The review rejected four possible promotions.

First, local transversality is not derived from Hall quotas or from the
single-open quotient frame.  It remains an explicit condition on the two
physical row families.

Second, failure of transversality is not equivalent to collision
noninjectivity.  The primary checks an exact chart with one dependent local
pair where the full collision matrix still has rank twelve.  Thus the theorem
does not classify the boundary.

Third, dependent local pairs can genuinely create a collision kernel.  The
ambient exact family

```text
a=(e_0,e_0,e_0,e_0),
b=(e_0,e_0,e_1,e_1),
h=(-e_0,e_0,0,0)                                     (8)
```

has `P_4(h,a,a,b)=0` with `h!=0`.  Both implementations replay (8).  It is
not a diagonal restriction and not a graph witness, so it establishes only
that some replacement for (2) is needed in the collision lemma.

Fourth, one detected absorption root does not exclude a hypothetical graph
or prove the global conjecture.  Detection says the particular affine gauge
cannot preserve the complete tensor; it does not prove that every solution
is gauge-equivalent to a prohibited normal form.

## 7. Independence and evidence boundary

The primary uses SymPy matrices, a labelled permanent enumeration, a selected
minor, exact local coordinate changes, and bounded rank-two companion frames.
The audit uses only the Python standard library, directly enumerated row
assignments, sparse integer tensors, a hand-coded rational elimination, and
an explicit left inverse.  The implementations share the displayed tensor
model but differ in representation and checking method.

Neither bounded script proves that every field-valued transverse collision
map is injective or that full span follows from the global matching problem.
Those are the written local-basis proof and the imported arbitrary-surplus
theorem, respectively.

## 8. Exact acceptance boundary

Accepted:

- injectivity of `h -> P_4(h,a,a,b)` when every local `(a_u,b_u)` pair is
  independent;
- survival of a companion basis after deleting at least one of the three
  non-aligned roots;
- nonzero two-open detection at that root in the aligned projective
  `q=0,r=4` cell; and
- detection at every root when all three companion pairs are independent.

Still open:

- whether local transversality is forced anywhere on the witness locus;
- the local-dependence part of `q=0,r=4`;
- fixed-root rank-two injectivity;
- `q=0,r>=5`, every `q>=1` cell, and the unfactorized branch;
- existence or exclusion of a witness in the reviewed cell; and
- the global Krenn--Gu conjecture.

## Replay record

Before publication, run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_transverse_four_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_transverse_four_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_transverse_four_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_transverse_four_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_transverse_four_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_transverse_four_cell_detector.py
```
