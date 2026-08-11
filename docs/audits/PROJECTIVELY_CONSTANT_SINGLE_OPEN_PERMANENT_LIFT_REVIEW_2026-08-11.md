# Adversarial review of the projectively constant single-open permanent lift

## Review status and provenance

This record reviews
[`PROJECTIVELY_CONSTANT_SINGLE_OPEN_CONSECUTIVE_PERMANENT_LIFT_AND_COMPANION_FRAME_THEOREM.md`](../../claims/arbitrary-order/PROJECTIVELY_CONSTANT_SINGLE_OPEN_CONSECUTIVE_PERMANENT_LIFT_AND_COMPANION_FRAME_THEOREM.md)
as a conditional characteristic-zero reduction.

The review was performed by Codex in a fresh proof pass after the proposed
identity had been formulated.  The no-import audit was separately derived at
the implementation level and does not import the primary verifier or project
code.  This record is not represented as an independent human mathematical
review.  Its purpose is to preserve the load-bearing reasoning, rejected
strengthenings, and exact acceptance boundary rather than leaving them only
in a task transcript.

Review verdict: **accept the theorem at its stated conditional scope**, subject
to the focused and repository-wide replay gates recorded below.  Do not change
the global Krenn--Gu status, which remains **UNRESOLVED**.

## 1. Reconstructed obligation

The upstream fixed-surplus theorem gives a single-open identity with two
matching sectors:

```text
L_j(g_j(y))+sum_(s!=j) ell_(j,s)(y) Lambda^+_(js)
 =D_j(y).                                             (1)
```

The claim under review assumes all of the following, and only under their
intersection asserts a permanent lift:

1. the roots are fully supported and pairwise zero at their fixed vectors;
2. the outside graph has the physical form
   `W_uv=a_u tensor b_v+b_u tensor a_v`;
3. the second outside row is aligned with root `j`, so `b_u=h_(j,u)`;
4. the complete open root shore is projectively constant,
   `g_(j,u)(y)=eta_j(y)b_u`, with `eta_j(x_j)=1`; and
5. the original graph tensor is the ternary diagonal tensor, so the weights
   in `D_j` are nonzero.

The theorem does not claim that any of conditions 2--4 is universal.  This
scope was checked against the fixed-surplus and two-open owners.

## 2. Matching and factorial audit

Let `m=r+2q`.  The original matching graph has exactly

```text
r+|B|=2r+2q
```

vertices.  Contracting the `r-1` local root slots other than `j` leaves
exactly

```text
1+|B|=M=r+2q+1
```

open tensor modes.  The proposed permanent has

```text
(r-1)+(q+1)+(q+1)=M
```

source rows, so there is no parity or row-count mismatch.

For an outside set of size `2t`, expanding

```text
W_uv=a_u b_v+b_u a_v
```

over its perfect matchings gives

```text
H_S=1/t! P_(2t)(a^t,b^t;S).                          (2)
```

The divisor is `t!`, not `(t!)^2`: after a `t|t` endpoint split, one factor
of `t!` counts the actual bipartite perfect matchings while the other is the
redundancy from labelling identical permanent rows.  Direct symbolic and
integer ledgers confirm (2) at both `t=q` and `t=q+1`.

In the new column `j`, the three possible source-row types give:

- one `hat h_s` row: `ell_(j,s) Lambda^+_(js)`;
- one of `q+1` identical `hat a` rows:
  `(q+1)/(q+1)!=1/q!` times the fixed permanent; and
- one of the `hat b` rows: zero.

These cases are disjoint and exhaust the permanent column expansion.  They
reconstruct exactly (1), with no determinant signs and no omitted
root--root sector.

## 3. Contraction and orientation audit

At the original root vector,

```text
ell_(j,s)(x_j)=W_js(x_j,x_s)=0,
eta_j(x_j)=1.                                         (3)
```

Thus contraction of the new column at `x_j` selects one of the `q+1`
`hat a` rows and produces exactly the normalized fixed `P_m` layer.  The
same calculation works at `q=0`; there are then one `a` row and one `b` row,
and `0! = 1`.

The covector `ell_(j,s)=W_js(-,x_s)` lives on the open `j` mode.  The outside
row `h_(s,u)=W_su(x_s,-)` lives on mode `u`.  Placing these in the `j` and
`u` columns of one row family is therefore orientation-correct.  No
identification of different local dual spaces is used beyond their common
ternary coordinate labels on the target diagonal.

## 4. Quotient-frame audit

Write

```text
D_j(y)=sum_c bar X_c y[c] e_c^(tensor B),
F=D_j(x_j).                                           (4)
```

All `bar X_c` are nonzero, so `D_j` is an isomorphism from the local root
space to the three-dimensional diagonal tensor space.  For
`y in ker eta_j`, equation (1) reduces to

```text
sum_(s!=j) ell_(j,s)(y) Lambda^+_(js)=D_j(y).         (5)
```

If all companion coefficients in (5) vanished for a nonzero `y`, the right
side would contradict injectivity of `D_j`.  Hence the coefficient map on
`ker eta_j` is injective and has rank two.  Since every `ell_(j,s)`
annihilates `x_j`, their span is exactly `Ann(x_j)`.

Because `eta_j(x_j)=1`, one has

```text
L_j=ker eta_j direct-sum <x_j>,
Diag_B=D_j(ker eta_j) direct-sum <F>.                 (6)
```

Equation (5) is therefore an isomorphism between the effective coefficient
plane and the diagonal quotient modulo `F`.  The theorem correctly avoids
the stronger and unjustified assertion that every individual
`Lambda^+_(js)` is diagonal.  Only the combinations arising from the
two-dimensional effective coefficient plane are forced into the diagonal
complement.

## 5. Imported permanent consequences

After multiplication by `(q+1)!`, the lifted identity has all three diagonal
weights nonzero.  It is therefore legal to import the arbitrary-permanent
Hall and strict-support theorems.

- The `q+1` repeated `b` rows vanish in the new mode and have a one-dimensional
  local span on every outside mode.  The Hall quota requires `q+1` modes per
  colour, giving `3(q+1)<=r+2q`, hence `r>=q+3`.  At `q=0`, the singleton
  tricolour theorem gives the same count.
- The exact row-cell ledger is

  ```text
  I_-j+c_j+(q+1)(p_a+1)+(q+1)p_b.                    (7)
  ```

  Repeated rows are distinct source coordinates and must remain repeated in
  this count.  Applying the strict support theorem gives `3M+3`.  This is not
  a physical-edge count.

These imports do not prove that the permanent restriction is impossible;
support `3M+3` and all larger supports remain live.

## 6. Deliberate falsification cases

The replay suite includes the following cases because each catches a
different possible overstatement or normalization error:

| Case | Failure mode tested |
|---|---|
| `r=2,q=0` | smallest row count and the logical consequence that a rank-two companion frame cannot actually exist with one old root |
| `r=3,q=0` | zero-surplus contraction and `0!` normalization |
| `r=2,q=1` | first nontrivial Wick factor and the `2!` lifted divisor |
| `r=3,q=1` | simultaneous multiple old-root companions and Wick sectors |
| `r=2,q=2` | a higher repeated-row factorial in the no-import audit |
| `r=4,q=1` | more than the minimum number of persistent root rows |

Zero individual `a_u`, `b_u`, or companion covectors are permitted by the
written theorem.  The proof uses only the family identities; the derived
local concision and Hall conditions then rule out any zero pattern that is
incompatible with a diagonal restriction.

## 7. Independence and evidence boundary

The primary verifier uses symbolic expressions, a perfect-matching recursion,
and a labelled permanent expansion.  It compares the full graph contraction,
the outside sector, each old-root companion sector, and the contracted fixed
layer.

The no-import audit uses only the Python standard library, independent exact
integer data, a separately written permutation ledger, a separate matching
recursion, and rational row reduction.  It imports neither repository code
nor the primary verifier and uses no computer-algebra package.  It is
independent at the implementation and bounded algebra-rederivation layers.
Both checks share the theorem's mathematical model, and neither replaces the
arbitrary-order written matching/Laplace proof or the imported Hall/support
theorems.

## 8. Scope decision and remaining obligation

Accepted:

- the conditional `P_(m+1)` lift;
- exact contraction to the aligned fixed `P_m` layer;
- rank two of the effective old-root companion plane;
- the diagonal quotient-frame isomorphism; and
- the transferred Hall and row-cell support ledgers.

Not accepted or claimed:

- universal common-two-row factorization or alignment;
- universal projective constancy;
- diagonal status of each individual companion cofactor;
- transport from `Lambda^+_(js)` to the different two-open
  row-replacement tensors `A_(i,j;s)`;
- exclusion of arbitrary permanent restrictions; or
- any proof or counterexample for the global conjecture.

The precise next positive obligation is a legal cross-depth map or selector
that transports the rank-two frame in (5) to the two-open row-replacement
cofactor map.  Failure of such transport would need its own exact boundary
theorem; it cannot be inferred from the present lift.

## Replay record

The focused commands and final repository validation results are recorded in
the pull request and commit that publish this review.  Before publication,
the required commands are:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_single_open_permanent_lift.py
python claims/arbitrary-order/audit_projectively_constant_single_open_permanent_lift.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_single_open_permanent_lift.py claims/arbitrary-order/audit_projectively_constant_single_open_permanent_lift.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_single_open_permanent_lift.py claims/arbitrary-order/audit_projectively_constant_single_open_permanent_lift.py
```
