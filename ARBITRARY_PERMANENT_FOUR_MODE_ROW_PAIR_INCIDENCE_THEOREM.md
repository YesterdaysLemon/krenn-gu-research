# Every permanent row pair needs four coordinate-incidence modes

## Status

**Exact arbitrary-order characteristic-zero incidence theorem.**  In every
hypothetical multilinear restriction

```text
P_m -> Delta_3,                    m>=3,              (1)
```

fix any two source rows.  Their two local covectors span a target coordinate
covector in at least **four** modes.

The later
[`ARBITRARY_PERMANENT_FIVE_MODE_ROW_PAIR_INCIDENCE_THEOREM.md`](ARBITRARY_PERMANENT_FIVE_MODE_ROW_PAIR_INCIDENCE_THEOREM.md)
classifies equality at four and excludes all six symbolic types, strengthening
the final lower bound to five modes.  The proof below remains the first polar
rank step in that argument.

The earlier kernel-deletion hierarchy gives two incidences of each target
colour and hence the coarse lower bound three modes.  The new step proves
that equality at three is impossible: equality would force the three local
row planes to be the coordinate planes `01,02,12`, but a polarized permanent
slice through any two of them is a nonzero rank-one diagonal.  The common
two-row factorization cannot produce that diagonal without losing local rank.

For the factorized `P_7` branch this strengthens the residual-null theorem
from at least three to at least four blockers.  It is a necessary structural
condition, not an exclusion of `P_7` or a proof of Krenn--Gu.  No support,
word, or graph-family enumeration is used.

## 1. Setup

Let

```text
phi_w:C^3 -> C^m,                 w=0,...,m-1,
r_(w,p)=e_p^* composed with phi_w,
```

and suppose

```text
P_m(phi_0(x_0),...,phi_(m-1)(x_(m-1)))
 =sum_(c=0)^2 lambda_c product_w x_w[c],
lambda_0 lambda_1 lambda_2 !=0.                        (2)
```

Fix distinct source rows `p,q`.  At mode `w`, put

```text
A_w=span{r_(w,p),r_(w,q)} subset (C^3)^*,
K_w=ker r_(w,p) intersection ker r_(w,q).             (3)
```

Call `w` a **coordinate-incidence mode** when

```text
e_c^* in A_w                                           (4)
```

for at least one target colour `c`.  Annihilator duality says this is
equivalent to `K_w` being contained in a coordinate hyperplane.  Over an
infinite field, it is also equivalent to `K_w` having no point in the target
coordinate torus.

## 2. Every colour occurs at least twice

### Lemma 1 (two-per-colour quota)

For every target colour `c`, condition (4) holds in at least two modes.

Proof.  Suppose it held in at most one mode.  In at least `m-1` modes,
`e_c^*` is not in `A_w`, so its restriction to `K_w` is nonzero.  Choose

```text
kappa_w in K_w,             kappa_w[c]!=0             (5)
```

in those `m-1` modes, and put `x_w=e_c` in the remaining mode.  The target
value in (2) is the nonzero scalar

```text
lambda_c product kappa_w[c].                           (6)
```

On the permanent side, the `m-1` vectors `phi_w(kappa_w)` all vanish in
source rows `p,q`.  They would have to be assigned injectively to the other
`m-2` source rows, which is impossible.  Hence the permanent is zero,
contradicting (6).

This is the `|S|=2` case of the committed arbitrary permanent
kernel-deletion hierarchy, included here to expose the equality case used
below.

### Corollary 2 (coarse three-mode bound)

There are at least six colour incidences in total.  Since `dim A_w<=2`, one
mode contains at most two independent coordinate covectors.  Hence at least
three modes are coordinate-incidence modes.

## 3. Equality at three has a unique local normal form

Assume for contradiction that exactly three modes are coordinate-incidence
modes.  Lemma 1 gives at least six incidences, while those three planes can
hold at most six.  Equality holds throughout.  Thus:

1. every one of the three modes has `dim A_w=2`;
2. each `A_w` contains exactly two coordinate covectors; and
3. every target colour occurs exactly twice.

The three planes are therefore, in some order,

```text
A_(w_0)=<e_1^*,e_2^*>,       K_(w_0)=<e_0>,
A_(w_1)=<e_0^*,e_2^*>,       K_(w_1)=<e_1>,
A_(w_2)=<e_0^*,e_1^*>,       K_(w_2)=<e_2>.           (7)
```

Every other `K_w` meets the coordinate torus; choose a torus vector
`kappa_w` in it.

## 4. The rank-one polar slice contradicts the common two-row frame

Expand the permanent in (2) along source rows `p,q`.  For two modes `u,v`
define the corrected two-row block

```text
D_uv=r_(u,p) tensor r_(v,q)+r_(u,q) tensor r_(v,p),   (8)
```

and let `F_uv` be the permanent tensor of the other `m-2` rows and modes.
Then

```text
sum_(u<v) D_uv tensor F_uv
 =sum_(c=0)^2 lambda_c e_c^(tensor m).                (9)
```

Select `{u,v}={w_1,w_2}`.  Contract `w_0` with `e_0` and every other mode
with its chosen torus vector in `K_w`.  Every pair term in (9) except
`{w_1,w_2}` meets a contracted common-null leg and dies termwise.  Therefore

```text
s D_(w_1 w_2)=mu e_0 tensor e_0,       mu!=0,         (10)
```

where `s` is the complementary permanent.  The right side is nonzero, so
`s!=0`; hence `D_(w_1 w_2)` itself is supported only at entry `(0,0)`.

At `w_1`, collect the two selected source-row evaluations into columns

```text
R_1(c)=(r_(w_1,p)[c],r_(w_1,q)[c])^T.                (11)
```

Equation (7) says `R_1(1)=0` and `{R_1(0),R_1(2)}` is a basis of `C^2`.
Likewise `R_2(2)=0` and `{R_2(0),R_2(1)}` is a basis.  With

```text
J=[[0,1],[1,0]],
D_(w_1 w_2)^(cd)=R_1(c)^T J R_2(d).                  (12)
```

Both matrices `R_1,R_2:C^3->C^2` have rank two.  Hence `R_2` is surjective,
`J` is invertible, and `R_1^T:C^2->C^3` is injective.  Their composition

```text
D_(w_1 w_2)=R_1^T J R_2                              (13)
```

has rank exactly two.  This contradicts the nonzero rank-one matrix in
(10).  Equivalently, its zero entries `(2,0)` and `(2,1)` make the nonzero
column `R_1(2)` orthogonal under `J` to the basis
`{R_2(0),R_2(1)}`, forcing that column to vanish.

This contradiction proves the main result.

### Theorem 3 (four-mode row-pair incidence)

For every selected source-row pair `{p,q}` in every restriction (2), at
least four local modes satisfy

```text
e_c^* in span{r_(w,p),r_(w,q)}
```

for some target colour `c`.

The theorem also rules out (2) at `m=3`, because four distinct incidence
modes cannot then exist.

## 5. P7 consequence and exact boundary

In the factorized seven-mode branch, take `p,q` to be the two residual port
rows `a,b`.  Then at least four blockers satisfy

```text
e_c^* in span{a_w,b_w}                               (14)
```

for some `c`.  Equivalently, at most three common null spaces
`ker a_w intersection ker b_w` meet the coordinate torus.

This strictly strengthens the determinant-only count `3/4` to `4/3`.  It
also explains why a model with three clustered incidences of one colour can
satisfy the canonical profile and all pure coefficients while failing the
full factorized identity: it violates Lemma 1 before mixed-word equations
are even considered.

Not proved here:

- a fifth coordinate-incidence blocker;
- a forced placement or colour pattern for the four blockers;
- incompatibility with the canonical `012,01,01,02,02,12,12` profile;
- nonexistence of `P_7 -> Delta_3`;
- the global Krenn--Gu conjecture.

All remain **UNKNOWN/UNRESOLVED**.

## Replay

```powershell
uv run --with sympy python verify_arbitrary_permanent_four_mode_row_pair_incidence_theorem.py
python audit_arbitrary_permanent_four_mode_row_pair_incidence_theorem.py
uv run --with sympy --with ruff python -m ruff check verify_arbitrary_permanent_four_mode_row_pair_incidence_theorem.py audit_arbitrary_permanent_four_mode_row_pair_incidence_theorem.py
python -m py_compile verify_arbitrary_permanent_four_mode_row_pair_incidence_theorem.py audit_arbitrary_permanent_four_mode_row_pair_incidence_theorem.py
```

The primary verifier checks the equality normal form, the partially polarized
rank-one target, and the symbolic nondegenerate-pairing contradiction.  The
independent no-import audit reconstructs the same contradiction with a
separate sparse-polynomial calculation.  The displayed Hall and polar proofs
establish the arbitrary-order theorem; neither replay performs a search.
