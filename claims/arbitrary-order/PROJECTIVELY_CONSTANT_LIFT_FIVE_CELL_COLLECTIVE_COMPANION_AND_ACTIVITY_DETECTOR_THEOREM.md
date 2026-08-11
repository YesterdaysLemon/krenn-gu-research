# Projectively constant lift: five-cell collective companion and activity detector

## Status

**Exact conditional characteristic-zero reduction and detector theorem.**
Work on the aligned common-two-row, projectively constant branch of the
single-open consecutive permanent lift in the next tight cell

```text
q=0,                  r=5,                  |B|=5.    (1)
```

There are four non-aligned roots and four companion covectors at the aligned
root `j`.  Their span has dimension two.  The complete two-open tensors at
the four possible second roots form one exact collective linear system on
the six pair-replacement cofactors.

That companion system is injective unless either

1. one companion covector is zero; or
2. the four nonzero companions admit a partition into two proportional
   pairs.

On the injective companion stratum, assume one further exact activity
condition: after deleting any outside mode, at least three of the four
one-persistent-row tensors `P_4(h_p,a,a,b)` are nonzero.  Then at least one
of the four affine absorption directions is detected by the complete
two-open graph tensor.

In particular, the activity condition holds if `a_u,b_u` are linearly
independent at all five outside modes.  Thus the locally transverse
`q=0,r=5` cell has a collective detector whenever its companion configuration
is not one of the two explicitly classified exceptional types.

This is the first exact transport into the five-root cell.  It does not
exclude the exceptional companion configurations, force deletion activity
in every hypothetical witness, detect every individual root, prove
fixed-root injectivity, exclude a witness, treat positive surplus, or address
an unfactorized outside graph.  The full aligned `q=0,r=5` cell remains open.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Imported five-cell restriction

Let

```text
R={j} disjoint-union P,       P={1,2,3,4},
|B|=5.                                                   (2)
```

Use the aligned factorization and projective-shore hypotheses from
[`PROJECTIVELY_CONSTANT_SINGLE_OPEN_CONSECUTIVE_PERMANENT_LIFT_AND_COMPANION_FRAME_THEOREM.md`](PROJECTIVELY_CONSTANT_SINGLE_OPEN_CONSECUTIVE_PERMANENT_LIFT_AND_COMPANION_FRAME_THEOREM.md):

```text
W_uv=a_u tensor b_v+b_u tensor a_v,
b_u=h_(j,u),
W_ju(y,-)=eta_j(y)b_u,
eta_j(x_j)=1.                                           (3)
```

The complete single-open restriction is

```text
P_6((hat h_p)_(p in P),hat a,hat b)
 =sum_(c=0)^2 bar X_c e_c^(tensor (B disjoint-union {j})),
bar X_0 bar X_1 bar X_2!=0.                            (4)
```

At mode `j`,

```text
hat h_p|_j=ell_p:=ell_(j,p),
hat a|_j=eta_j,               hat b|_j=0.             (5)
```

The companion frame gives

```text
span{ell_1,ell_2,ell_3,ell_4}=Ann(x_j),
dim Ann(x_j)=2.                                         (6)
```

Contracting (4) at `x_j` gives the fixed tight layer

```text
P_5(h_1,h_2,h_3,h_4,b)
 =sum_(c=0)^2 X_c e_c^(tensor B),
X_0 X_1 X_2!=0.                                        (7)
```

The arbitrary-surplus full-span theorem therefore gives

```text
span{h_(p,u):u in B}=(K^3)^*       for every p in P.  (8)
```

All spaces and covectors are over a characteristic-zero field `K`.

## 2. Pair cofactors and the collective companion matrix

For an unordered pair `{p,q} subset P`, define

```text
B_pq=P_5(h_p,h_q,a,a,b).                              (9)
```

Every row family in (9) is restricted to the five modes of `B`.  For
distinct `i,v in P`, the two-open replacement tensor is

```text
A_(i,j;v)=B_pq,
{p,q}=P-{i,v}.                                        (10)
```

Thus the projective two-open coefficient at root `i` is

```text
C_i=sum_(v in P-{i}) ell_v tensor B_(P-{i,v}).        (11)
```

Here `B_(P-{i,v})` denotes the pair tensor whose two indices form that
complement.

Package the six pair tensors into a symmetric zero-diagonal `4 x 4` matrix
`X` by

```text
X_iv=B_(P-{i,v})              for i!=v,
X_ii=0.                                               (12)
```

Let `L` be the `4 x 2` companion matrix whose `v`-th row is `ell_v` in any
basis of `Ann(x_j)`.  Then all four equations (11) are exactly

```text
X L=0.                                                (13)
```

For tensor-valued entries, (13) is read after applying any linear functional
to the pair-tensor space.

## 3. Exact companion-system classification

Call the companion frame **balanced exceptional** if all four companions are
nonzero and there is a partition

```text
P=A disjoint-union D,       |A|=|D|=2,                (14)
```

such that the two companions in `A` are proportional and the two in `D`
are proportional.  The two projective directions are distinct because
`rank L=2`.

### Theorem 1 (collective companion injectivity)

The linear map from the six symmetric zero-diagonal entries of `X` to `XL`
is injective if and only if

```text
every ell_p is nonzero
and the frame is not balanced exceptional.            (15)
```

If (15) holds and all four `C_i` vanish, then

```text
B_pq=0                 for every pair {p,q}.          (16)
```

### Proof

First suppose some `ell_k=0`.  The other three companions have a nontrivial
linear relation

```text
sum_(v!=k) alpha_v ell_v=0.                           (17)
```

Put `X_kv=X_vk=alpha_v` and all other entries zero.  Then `X!=0` and
`XL=0`.  If two companions vanish, one may instead take the single entry
joining their indices.

If the frame is balanced exceptional, choose nonzero two-term relations
within the two pairs in (14).  Their outer product gives a nonzero symmetric
matrix supported on the cross edges between `A` and `D`; it has zero diagonal
and annihilates `L`.  Thus either exceptional type destroys injectivity.

Conversely, suppose all companions are nonzero and `0!=X=X^T` has zero
diagonal and satisfies `XL=0`.  Since `rank L=2`, the kernel of `X` contains
a two-dimensional subspace, so `rank X<=2`.  A symmetric rank-one matrix
with zero diagonal is zero in characteristic zero.  Hence `rank X=2`.

Choose a nonzero off-diagonal entry of `X`.  Its `2 x 2` principal minor is
nondegenerate, so the rank-two symmetric form is hyperbolic.  There are
vectors `u,v in K^4` such that

```text
X=u v^T+v u^T.                                        (18)
```

The zero diagonal gives `2u_p v_p=0` for every `p`.  Therefore every active
index belongs to one of two groups: `u_p!=0,v_p=0` or
`u_p=0,v_p!=0`.  Equation `XL=0` gives a nontrivial weighted relation among
the companions in each group.  Because every companion is nonzero, each
group contains at least two indices.  There are only four indices, so the
groups have size two and no inactive index remains.  A nonzero two-term
relation means the two companions in each group are proportional.  This is
exactly (14), proving the converse.

The tensor-valued conclusion follows by applying linear functionals to a
nonzero entry.  This proves Theorem 1.

### Exact exceptional kernels

The proof is constructive.  A zero companion produces a star relation
centered at its index.  A balanced `2+2` projective split produces a
rank-one cross-block relation.  These are coefficient-system kernels, not
graph witnesses and not proof that the physical pair tensors realize a
nonzero kernel element.

## 4. Quotienting pair-replacement tensors

At an outside mode `u`, put

```text
S_u=span{a_u,b_u},       pi_u:L_u^* -> L_u^*/S_u.     (19)
```

For `p in P`, define the four-mode deletion tensor

```text
R_(p,u)=P_4(h_p,a,a,b; B-{u}).                        (20)
```

### Lemma 2 (pair-collision quotient)

For distinct `p,q`,

```text
(pi_u tensor id_(B-{u})) B_pq
 =pi_u(h_(p,u)) tensor R_(q,u)
  +pi_u(h_(q,u)) tensor R_(p,u).                      (21)
```

### Proof

Expand `P_5(h_p,h_q,a,a,b)` by the source row assigned to mode `u`.
Terms assigning `a` or `b` there die modulo `S_u`.  Assigning `h_p` leaves
the first tensor product in (21); assigning `h_q` leaves the second.  The
two labelled `a` rows and their factor two occur identically inside each
`P_4`, so no additional multiplicity is present.

### Lemma 3 (three active deletions force local trapping)

Fix `u`.  Suppose all six `B_pq` vanish and at least three of the four
tensors `R_(p,u)` are nonzero.  Then

```text
h_(p,u) in S_u                 for every p in P.       (22)
```

### Proof

Write

```text
v_p=pi_u(h_(p,u)),       r_p=R_(p,u).                 (23)
```

Equation (21) becomes

```text
v_p tensor r_q+v_q tensor r_p=0       for p!=q.       (24)
```

Assume some `v_k!=0`.  If `r_k=0`, equation (24) forces every other `r_q`
to vanish, contradicting three active deletions.  If `r_k!=0`, then for any
other nonzero `r_q`, equality of the two nonzero rank-one tensors in (24)
gives a scalar `lambda_q!=0` with

```text
v_q=lambda_q v_k,        r_q=-lambda_q r_k.           (25)
```

There are at least two such distinct indices `q,r`.  Their equation (24)
becomes

```text
-2 lambda_q lambda_r v_k tensor r_k=0,                (26)
```

impossible in characteristic zero.  Hence every `v_p=0`, which is (22).

## 5. The five-cell activity detector

Call an outside mode `u` **three-active** if at least three of the four
deletion tensors in (20) are nonzero.

### Theorem 4 (collective `q=0,r=5` detector)

Assume:

1. the companion frame satisfies (15); and
2. every outside mode is three-active.

Then at least one coefficient tensor `C_i` in (11) is nonzero.  Consequently
every nonzero affine absorption direction at at least one non-aligned root is
detected by the complete two-open tensor.

### Proof

Assume all four `C_i` vanish.  Theorem 1 gives all six equations (16).
At each outside mode, Lemma 3 gives

```text
h_(p,u) in S_u           for every p.                 (27)
```

The five source rows of the fixed layer (7) are `h_1,h_2,h_3,h_4,b`.
At every mode, (27) places all of them in `S_u`, whose dimension is at most
two.  Thus the local flattening rank of the left side of (7) is at most two.
The weighted ternary diagonal has local flattening rank three because every
`X_c` is nonzero.  This contradiction proves that some `C_i!=0`.

On the projectively constant branch, the complete variation at that root is

```text
delta T_ij=tau kappa_i tensor C_i.                    (28)
```

It is nonzero for every nonzero absorption covector `kappa_i`.

### Corollary 5 (locally transverse five-cell detector)

Suppose `a_u,b_u` are linearly independent at every outside mode.  Then
every outside mode is four-active, hence three-active.  Therefore condition
(15) alone guarantees a collective detector.

### Proof

Fix `u,p`.  On the four retained modes `B-{u}`, local transversality makes

```text
h |-> P_4(h,a,a,b)                                    (29)
```

injective by the transverse four-mode collision theorem.  The row family
`h_p|_(B-{u})` is nonzero: otherwise (8) would give `h_p` support at only the
single mode `u`, contradicting its full span.  Hence `R_(p,u)!=0` for every
`p,u`.

## 6. Exact residual boundary

The new content is:

```text
four-companion collective coefficient system:         EXACT XL FORM;
collective companion map with a zero companion:        NONINJECTIVE;
collective companion map on balanced 2+2 split:        NONINJECTIVE;
all other rank-two four-companion configurations:      INJECTIVE;
pair-collision quotient at each outside mode:          EXACT;
three active deletions plus six zero pair tensors:      ROOT ROWS TRAPPED;
good companions plus three-activity at every mode:     SOME ROOT DETECTED;
locally transverse good-companion q=0,r=5 cell:        SOME ROOT DETECTED;
zero/2+2 companion branches:                           OPEN;
failure of three-activity at some mode:                OPEN;
full aligned q=0,r=5 cell:                             OPEN;
fixed-root detector injectivity:                       UNKNOWN;
q=0,r>=6, q>=1, and unfactorized cells:               UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.          (30)
```

The single-open lift, companion rank, fixed layer, complete two-open formula,
and root-row full-span theorem are imported at their existing scopes.  The
collective companion classification, pair quotient, activity lemma, and
five-cell detector are proved here.  The transverse corollary imports
[`PROJECTIVELY_CONSTANT_LIFT_TRANSVERSE_FOUR_CELL_TWO_OPEN_DETECTOR_THEOREM.md`](PROJECTIVELY_CONSTANT_LIFT_TRANSVERSE_FOUR_CELL_TWO_OPEN_DETECTOR_THEOREM.md).
The root-row span used in the corollary is imported from
[`ARBITRARY_SURPLUS_COMMON_ROW_FULL_SPAN_OBSTRUCTION.md`](ARBITRARY_SURPLUS_COMMON_ROW_FULL_SPAN_OBSTRUCTION.md).
The theorem has not been formalized in Lean.  Its preserved line-by-line
scope and adversarial reconstruction are in the
[`2026-08-11 review record`](../../docs/audits/PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_COLLECTIVE_DETECTOR_REVIEW_2026-08-11.md).

## Replay

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_five_cell_collective_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_five_cell_collective_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_five_cell_collective_detector.py claims/arbitrary-order/audit_projectively_constant_lift_five_cell_collective_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_five_cell_collective_detector.py claims/arbitrary-order/audit_projectively_constant_lift_five_cell_collective_detector.py
```

The primary verifier checks the `8 x 6` companion matrix on a bounded exact
frame census, explicit exceptional kernels, all `5 x 81` pair-quotient
slices, a bounded scalar model of the three-activity equations, and local
concision.  The
independent no-import audit instead uses rational row reduction, a symmetric
matrix ledger, a recursive permanent, and an exhaustive small scalar activity
census.  These are bounded convention and falsification checks.  The
characteristic-zero proof for arbitrary field-valued tensors is the written
symmetric-form, rank-one tensor, quotient, and concision argument above.
