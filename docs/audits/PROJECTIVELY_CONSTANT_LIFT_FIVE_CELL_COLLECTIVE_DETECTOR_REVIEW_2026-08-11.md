# Adversarial review of the five-cell collective detector

## Review status and provenance

This record reviews
[`PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_COLLECTIVE_COMPANION_AND_ACTIVITY_DETECTOR_THEOREM.md`](../../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_COLLECTIVE_COMPANION_AND_ACTIVITY_DETECTOR_THEOREM.md)
as a conditional characteristic-zero theorem.

Codex reconstructed the companion coefficient system, its exceptional
rank-loss locus, the pair-collision quotient, and the activity-to-concision
contradiction independently of the primary script.  The standard-library
audit separately rebuilds the coefficient matrix with rational elimination
and the permanent tensors by deletion recursion.  This is durable
adversarial reasoning, not an independent human review.

Review verdict: **accept collective two-open detection in the stated
aligned projective `q=0,r=5` stratum**, conditional on both a good companion
configuration and three-active deletions at every outside mode, after the
focused and repository-wide replay gates pass.  The locally transverse
corollary discharges the activity hypothesis but not the companion
hypothesis.  No exceptional companion configuration or activity failure is
excluded, no witness is excluded, and the global Krenn--Gu conjecture
remains **UNRESOLVED**.

## 1. Reconstructed obligation

There are four non-aligned roots `P={1,2,3,4}`.  The lifted six-row
restriction has companions `ell_p` at the aligned mode `j`, and

```text
span{ell_p:p in P}=Ann(x_j),       dim Ann(x_j)=2.    (1)
```

For each unordered pair `{p,q}` define the five-mode replacement tensor

```text
B_pq=P_5(h_p,h_q,a,a,b).                             (2)
```

Opening a root `i` leaves three possible companion roots `v`.  The exact
two-open coefficient is

```text
C_i=sum_(v!=i) ell_v tensor B_(P-{i,v}).              (3)
```

The obligation is not to prove one fixed-root map injective.  It is to show
that all four tensors in (3) cannot vanish simultaneously on an explicitly
identified stratum.

## 2. Companion-matrix reconstruction

Put the six pair tensors into the off-diagonal entries of a symmetric
zero-diagonal matrix

```text
X_iv=B_(P-{i,v}),       X_ii=0,                       (4)
```

and put the four companions into the rows of a `4 x 2` matrix `L`.  The four
equations (3) are exactly

```text
X L=0.                                                (5)
```

The complement indexing in (4) was checked explicitly: row `i`, column `v`
contains precisely the persistent pair left after deleting `i` and `v`.
Symmetry follows because the complement is unchanged on interchanging
`i,v`; no sign occurs in a permanent.

For scalar entries, a nonzero kernel is immediate in either of two cases.

- If `ell_k=0`, a relation among the other three companions gives a star
  matrix centered at `k`.  If two companions vanish, their joining edge is
  already a kernel vector.
- If the four nonzero companions split into two proportional pairs, the
  outer product of the two within-pair relations gives a symmetric
  cross-block kernel with zero diagonal.

The converse uses no finite census.  If `0!=X=X^T`, `diag X=0`, and `XL=0`,
then `rank X<=2` because the two columns of `L` lie in its kernel.  A
symmetric rank-one zero-diagonal matrix is zero in characteristic zero, so
`rank X=2`.  Any nonzero off-diagonal entry supplies a nondegenerate
hyperbolic `2 x 2` principal block.  Hence

```text
X=u v^T+v u^T.                                        (6)
```

The diagonal equations give `u_p v_p=0`.  Since `X!=0`, both the `u`-only
and `v`-only support groups are nonempty.  Equation (5), read on one index
from each group, separately gives

```text
u^T L=0,                 v^T L=0.                     (7)
```

With every companion nonzero, neither relation can have singleton support.
Two disjoint groups of size at least two among four indices must both have
size two and leave no inactive index.  Each two-term relation makes its pair
of companions proportional.  This is exactly the balanced `2+2` split.

Scalar injectivity extends to tensor-valued entries: if any tensor entry of
`X` were nonzero, a linear functional nonzero on that entry would produce a
nonzero scalar kernel.  The review therefore accepts the claimed if-and-only-if
classification over every characteristic-zero field.

## 3. Rejected false inference from the exceptional kernels

The zero-companion star and balanced `2+2` cross-block matrices are kernels
of the **coefficient map**.  They do not show that the six physical
permanents `B_pq` realize a nonzero kernel vector, do not construct a graph
witness, and do not refute the detector on either exceptional branch.  Those
branches remain open proof obligations.

## 4. Pair quotient and activity lemma

At an outside mode `u`, let

```text
S_u=span(a_u,b_u),
R_(p,u)=P_4(h_p,a,a,b;B-{u}).                         (8)
```

Laplace expansion of (2) at `u`, followed by quotienting the local output by
`S_u`, kills the assignments of either repeated `a` row and the `b` row.
The two persistent-root assignments survive and give exactly

```text
pi_u(B_pq)
 =pi_u(h_(p,u)) tensor R_(q,u)
  +pi_u(h_(q,u)) tensor R_(p,u).                      (9)
```

The factor two from the labelled `a` rows is already inside each `P_4`; no
extra factorial or multiplicity is missing.

Assume all six `B_pq` vanish.  Write `v_p=pi_u(h_(p,u))` and
`r_p=R_(p,u)`.  Then

```text
v_p tensor r_q+v_q tensor r_p=0       for p!=q.       (10)
```

If some `v_k!=0` and `r_k=0`, every other `r_q` is zero.  If instead both
are nonzero, each other active `r_q` forces

```text
v_q=lambda_q v_k,       r_q=-lambda_q r_k.            (11)
```

Two such additional active indices make their mutual equation equal to
`-2 lambda_q lambda_r v_k tensor r_k=0`, impossible in characteristic zero.
Thus three active `r_p` force every `v_p=0`, or equivalently all four local
root covectors lie in `S_u`.

This is an arbitrary-vector-space rank-one tensor argument.  The bounded
scalar activity censuses in the scripts only falsify signs and indexing;
they are not the proof of this implication.

## 5. Concision contradiction

On the injective companion stratum, all four `C_i=0` imply all six
`B_pq=0`.  If every outside mode is three-active, the activity lemma places
all four persistent root rows in `S_u` at each mode.  The fifth fixed-layer
row is `b_u`, already in `S_u`.  Therefore the local flattening rank of

```text
P_5(h_1,h_2,h_3,h_4,b)                               (12)
```

is at most two at every mode.  Its target is a weighted ternary diagonal
with all three weights nonzero, whose local flattening rank is three.  This
is a valid modewise contradiction and does not compare coordinates chosen
independently at different modes.

For the locally transverse corollary, deleting any outside mode leaves four
modes on which every local pair `(a,b)` is independent.  The prior
four-mode collision theorem makes `h -> P_4(h,a,a,b)` injective there.  The
restricted `h_p` is nonzero: otherwise the full-span root-row theorem would
leave `h_p` supported at only the deleted mode.  Hence all four deletion
tensors are active at every mode.

## 6. Independence and evidence boundary

The primary uses SymPy rank computations on 1,220 exact rank-two frames,
labelled permutation permanents on all `5 x 81` quotient slices, a bounded
scalar activity model, and the normalized four-mode collision rank.  The
audit uses only the Python standard library, rational row reduction on 2,310
frames, a recursive permanent, a separate scalar activity census, and a
dimension ledger.  It imports neither repository code nor computer algebra.

Neither bounded frame census proves the arbitrary companion classification,
and neither scalar activity census proves the arbitrary tensor lemma.  The
written rank-two symmetric-form proof and rank-one tensor proof above carry
those characteristic-zero implications.

## 7. Exact acceptance boundary

Accepted:

- the exact collective system `XL=0`;
- its zero-companion/balanced-`2+2` if-and-only-if rank-loss locus;
- the pair-collision quotient identity;
- local trapping from three active deletions and six zero pair tensors;
- collective detection under good companions and modewise three-activity;
  and
- the locally transverse corollary.

Still open:

- zero-companion configurations;
- balanced `2+2` companion configurations;
- failure of three-activity at any outside mode;
- fixed-root detector injectivity and witness exclusion;
- complete `q=0,r=5`, all `q=0,r>=6`, every `q>=1`, and the unfactorized
  branch;
- universal extraction/gluing; and
- the global Krenn--Gu conjecture.

## Replay record

Before publication, run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_five_cell_collective_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_five_cell_collective_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_five_cell_collective_detector.py claims/arbitrary-order/audit_projectively_constant_lift_five_cell_collective_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_five_cell_collective_detector.py claims/arbitrary-order/audit_projectively_constant_lift_five_cell_collective_detector.py
```
