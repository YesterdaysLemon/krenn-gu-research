# Projectively constant lift: five-cell pair collision and all-companion detector

## Status

**Exact conditional characteristic-zero detector theorem.**  Continue on the
aligned common-two-row, projectively constant branch in the tight cell

```text
q=0,                  r=5,                  |B|=5.    (1)
```

Assume the local outside pairs `a_u,b_u` are linearly independent.  A
persistent root row `h_p` is called doubly transverse if it escapes
`span(a_u,b_u)` at at least two outside modes.  If at most one of the four
persistent roots is not doubly transverse, then at least one non-aligned
root has a nonzero complete two-open detector, for **every** rank-two
companion configuration.

The proof has two independent pieces.

1. If one root row is doubly transverse and is nonzero at a third mode, then
   the five-mode pair-collision operator

   ```text
   g |-> P_5(h,g,a,a,b)                               (2)
   ```

   is injective.  The third nonzero mode is automatic for every persistent
   root by the imported full-span theorem.
2. If all four collective companion equations vanish for any rank-two
   companion frame, at least one of the six pair-collision tensors must be
   zero.

Thus the zero-companion and balanced-`2+2` coefficient exceptions from the
first five-cell theorem are no longer exceptions on this root-transverse
stratum.  Combined with that theorem, the locally transverse five-cell
residual now requires an exceptional companion frame **and** at least two
persistent roots that escape the local `a/b` planes at no more than one
mode.

This remains detection, not fixed-root injectivity or witness exclusion.  It
does not force local transversality, force double root transversality, close
the full `q=0,r=5` cell, treat larger or positive-surplus cells, or address an
unfactorized outside graph.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Imported five-cell system

Use the notation and hypotheses of
[`PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_COLLECTIVE_COMPANION_AND_ACTIVITY_DETECTOR_THEOREM.md`](PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_COLLECTIVE_COMPANION_AND_ACTIVITY_DETECTOR_THEOREM.md).
The four non-aligned roots are

```text
P={1,2,3,4}.                                          (3)
```

At the aligned mode `j`, their companion covectors satisfy

```text
span{ell_p:p in P}=Ann(x_j),       dim Ann(x_j)=2.    (4)
```

On the five outside modes, the fixed layer is

```text
P_5(h_1,h_2,h_3,h_4,b)
 =sum_(c=0)^2 X_c e_c^(tensor B),
X_0 X_1 X_2!=0.                                      (5)
```

The root-row full-span theorem gives

```text
span{h_(p,u):u in B}=(K^3)^*       for every p in P. (6)
```

In particular, every row family `h_p` is nonzero at at least three outside
modes.  This use of (6) depends only on the number of nonzero covectors,
which is invariant under independent local basis changes; no cross-mode span
is inferred after normalization.

For an unordered pair `{p,q}` put

```text
B_pq=P_5(h_p,h_q,a,a,b).                              (7)
```

The four complete projective two-open coefficients are

```text
C_i=sum_(v in P-{i}) ell_v tensor B_(P-{i,v}).        (8)
```

All spaces and covectors are over a characteristic-zero field `K`.

## 2. Five-mode pair-collision injectivity

For this section let `B` be any five-mode set and suppose

```text
dim span(a_u,b_u)=2                 for every u in B. (9)
```

Put

```text
S_u=span(a_u,b_u),
K_u=ker a_u intersection ker b_u.                    (10)
```

Then `K_u` is a line.  Choose `0!=k_u in K_u` and define

```text
alpha_u=h_u(k_u),             beta_u=g_u(k_u).       (11)
```

The condition `alpha_u!=0` is basis-independent and is equivalent to
`h_u notin S_u`.

### Lemma 1 (double-transverse pair-collision injectivity)

Suppose:

1. `alpha_p alpha_q!=0` at two distinct modes `p,q`; and
2. `h_r!=0` at a third mode `r notin {p,q}`.

Then

```text
P_5(h,g,a,a,b)=0                 implies g=0.         (12)
```

### Proof

Contract (12) at `k_u`.  Assignments of either `a` row or the `b` row to
mode `u` vanish.  The two persistent-row assignments give exactly

```text
P_4(alpha_u g+beta_u h,a,a,b;B-{u})=0.               (13)
```

There is no missing factor: the two labelled `a` assignments occur with the
same multiplicity inside both four-mode summands.

On the retained four modes, every local `a_v,b_v` pair is independent.
The transverse four-mode collision theorem therefore makes

```text
t |-> P_4(t,a,a,b)                                   (14)
```

injective.  Equation (13) gives the row-family identities

```text
alpha_u g_v+beta_u h_v=0          for every v!=u.    (15)
```

Apply (15) first with `u=p` and then with `u=q`.  At the third nonzero mode
`r`,

```text
g_r=lambda_p h_r=lambda_q h_r,
lambda_p=-beta_p/alpha_p,
lambda_q=-beta_q/alpha_q.                            (16)
```

Hence `lambda_p=lambda_q=:lambda`.  The `u=p,v=q` and `u=q,v=p`
equations, together with all remaining `u=p` equations, now give

```text
g=lambda h.                                           (17)
```

Evaluating (17) at `k_p` gives `beta_p=lambda alpha_p`, while the definition
in (16) gives `beta_p=-lambda alpha_p`.  Thus

```text
2 lambda alpha_p=0.                                  (18)
```

Characteristic zero and `alpha_p!=0` imply `lambda=0`, so `g=0`.

The double-transverse hypothesis is a real operator boundary.  In normalized
local bases take `a_u=e_0^*`, `b_u=e_1^*` and

```text
h=(b,b,b,a-b,a-b),
g=(0,0,0,-a,a).                                      (19)
```

Then `g!=0` but `P_5(h,g,a,a,b)=0`.  This ambient collision-kernel model is
not a lifted witness: `g` is supported at only two modes and violates the
root-row full-span condition.  It shows only that local `a/b` transversality
and nonzero support of `h` do not make (2) universally injective.

### Corollary 2 (root-pair nonvanishing)

Call a persistent root `p` **doubly transverse** when

```text
#{u in B:h_(p,u) notin S_u}>=2.                       (20)
```

If `p` is doubly transverse, then

```text
B_pq!=0                   for every q!=p.             (21)
```

Indeed, (6) supplies the third nonzero mode required by Lemma 1, and `h_q`
is nonzero by the same theorem.

## 3. A zero pair is unavoidable under collective invisibility

Package the six tensors (7) into a symmetric zero-diagonal `4 x 4` matrix

```text
X_iv=B_(P-{i,v})          for i!=v,
X_ii=0.                                               (22)
```

Let `L` be the `4 x 2` matrix of companion coordinates.  As in the first
five-cell theorem, all four tensors (8) vanish exactly when

```text
X L=0.                                                (23)
```

### Lemma 3 (rank-two companion zero-edge lemma)

Let the entries of `X` lie in any finite-dimensional `K`-vector space.  If

```text
rank L=2,       X=X^T,       diag X=0,       XL=0,    (24)
```

then at least one of the six off-diagonal entries of `X` is zero.

### Proof

Suppose all six entries were nonzero.  Since `K` has characteristic zero, it
is infinite.  Choose a linear functional `f` nonzero on all six entries and
apply it entrywise.  This produces a scalar symmetric matrix

```text
Y=f(X),            diag Y=0,            YL=0,        (25)
```

with every off-diagonal entry nonzero.

The two columns of `L` lie in `ker Y`, so `rank Y<=2`.  A nonzero symmetric
rank-one matrix cannot have zero diagonal in characteristic zero.  Hence
`rank Y=2`.  A nonzero off-diagonal `2 x 2` principal block is hyperbolic,
so there are `u,v in K^4` with

```text
Y=u v^T+v u^T.                                        (26)
```

The zero diagonal gives `u_i v_i=0` for every index.  Thus nonzero entries
of `Y` can occur only between the `u`-support and the disjoint `v`-support.
That support graph is bipartite, whereas six nonzero off-diagonal entries
would give the complete graph on four indices.  This is impossible.  Hence
some entry of `X` is zero.

### Corollary 4 (all-pair nonvanishing detects collectively)

If all six tensors `B_pq` are nonzero, then at least one `C_i` is nonzero for
every rank-two companion frame.

Indeed, (22) is a bijection between the six pair tensors and the six
off-diagonal entries.  If all `C_i` vanished, Lemma 3 would force a zero pair
tensor.

This argument includes good frames, zero companions, balanced `2+2` frames,
and their boundary intersections.  It neither constructs nor interprets a
coefficient-kernel vector as a graph witness.

## 4. The all-companion five-cell detector

### Theorem 5 (pair-collision detector for arbitrary companions)

Assume:

1. `a_u,b_u` are linearly independent at all five outside modes; and
2. at most one of the four persistent roots is not doubly transverse in the
   sense of (20).

Then at least one coefficient `C_i` in (8) is nonzero.  Consequently every
nonzero affine absorption direction at at least one non-aligned root is
detected by the complete two-open graph tensor.

### Proof

Every unordered root pair has a doubly transverse endpoint.  Corollary 2
therefore gives

```text
B_pq!=0                   for all six pairs.          (27)
```

Corollary 4 gives some `C_i!=0`.  On the projectively constant branch the
complete variation at that root is

```text
delta T_ij=tau kappa_i tensor C_i.                    (28)
```

It is nonzero for every nonzero absorption covector `kappa_i`.

## 5. Combined exact five-cell boundary

The previous five-cell theorem detects the good-companion, three-active
stratum; local `a/b` transversality makes every deletion active.  The new
theorem detects every companion frame when at most one root is not doubly
transverse.  Therefore an invisible locally transverse five-cell system must
satisfy both

```text
the companion frame is zero-companion or balanced 2+2;
at least two persistent roots have quotient support <=1.                 (29)
```

Here quotient support means the number of modes with
`h_(p,u) notin span(a_u,b_u)`.

The exact ledger is

```text
five-mode pair collision with two transverse and one support mode: INJECTIVE;
all-pair nonvanishing under rank-two companions:       SOME ROOT DETECTED;
locally transverse, at most one weak root:             SOME ROOT DETECTED;
good-companion locally transverse stratum:             SOME ROOT DETECTED;
exceptional companions plus at least two weak roots:   OPEN;
local a/b dependence and deletion-activity failure:    OPEN;
full aligned q=0,r=5 cell:                             OPEN;
fixed-root detector injectivity:                       UNKNOWN;
q=0,r>=6, q>=1, and unfactorized cells:               UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.          (30)
```

The single-open lift, fixed layer, companion rank, complete two-open formula,
and root-row full span are imported at their existing scopes.  Lemma 1
imports the exact collision injectivity from
[`PROJECTIVELY_CONSTANT_LIFT_TRANSVERSE_FOUR_CELL_TWO_OPEN_DETECTOR_THEOREM.md`](PROJECTIVELY_CONSTANT_LIFT_TRANSVERSE_FOUR_CELL_TWO_OPEN_DETECTOR_THEOREM.md).
The pair-collision injection, rank-two zero-edge lemma, and all-companion
detector are proved here.  The theorem has not been formalized in Lean.  Its
preserved line-by-line scope and adversarial reconstruction are in the
[`2026-08-11 review record`](../../docs/audits/PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_PAIR_COLLISION_REVIEW_2026-08-11.md).

## Replay

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_five_cell_pair_collision_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_five_cell_pair_collision_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_five_cell_pair_collision_detector.py claims/arbitrary-order/audit_projectively_constant_lift_five_cell_pair_collision_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_five_cell_pair_collision_detector.py claims/arbitrary-order/audit_projectively_constant_lift_five_cell_pair_collision_detector.py
```

The primary verifier checks every common-kernel contraction slice, exact
four-mode collision rank, a census of rank-two companion zero-edge kernels,
and representative five-mode injectivity charts.  The independent no-import
audit instead uses a recursive permanent, rational elimination, a larger
companion census, and separately assembled chart matrices.  These are
bounded convention and falsification checks.  The arbitrary-field result is
the written contraction/injectivity and symmetric-matrix proof above.
