# Arbitrary permanent active-support-at-least-six equality exclusion

## Status

This note gives an exact characteristic-zero classification of the
equality-five case on its full active coordinate support.  Let `K` be a
field of characteristic zero, let `n>=6`, and put

```text
Z_n=K[x_0,...,x_(n-1)]/(x_0^2,...,x_(n-1)^2).
```

Suppose that `U,V subset (Z_n)_1` are three-planes whose union uses all
`n` coordinates and

```text
dim(UV)=5.                                                   (1)
```

Then necessarily

```text
U=V=K x_i direct-sum W                                      (2)
```

for one coordinate axis, where `W` is a two-plane supported on the other
`n-1` coordinates and

```text
dim(W^2)=3.                                                  (3)
```

Conversely, (2)--(3) give an equality-five pair, active on all `n`
coordinates exactly when `W` uses all coordinates other than `i`.

No pair in (2) is Delta-admissible at the pair level.  Therefore an actual
weighted diagonal restriction cannot have an equality-five omitted pair
whose active coordinate support has size at least six.  In particular, the
active-support-six equality-five branch in `Z_6` is excluded.

This is a pair-level necessary-condition theorem.  It does not classify
active-support-four pairs, does not replace the separately owned
active-support-five argument, and does not prove that every omitted pair in
a putative `P_6 -> Delta_3` restriction has dimension five.  Unrestricted
permanent nonrestriction and the global Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

## 1. The multiplication-dual criterion

Write `E=(Z_n)_1` and use the coordinate basis `x_0,...,x_(n-1)`.  The
active-support hypothesis is

```text
supp(U) union supp(V)={0,...,n-1}.                          (4)
```

Put `P=UV`.  The multiplication map and its dual are

```text
mu:U tensor V -> P,
L=mu^*(P^*) subset U^* tensor V^*.                          (5)
```

As in the active-support-four orbit classification, the pair is
Delta-admissible exactly when `L` contains three rank-one forms

```text
lambda_e tensor rho_e,                     e=0,1,2,         (6)
```

whose left factors form a basis of `U^*` and whose right factors form a
basis of `V^*`.  We will show that every pair satisfying (1) and (4) has a
common coordinate axis and that all rank-one members of `L` annihilate that
axis.

For completeness, if a Delta-admissible basis is given, pull back the three
functionals on `P` which kill the mixed product plane and are dual to the
three diagonal products; their pullbacks are the three rank-one tensors in
(6).  Conversely, bases dual to spanning factor triples in (6) make all six
off-diagonal products lie in their common two-dimensional kernel and make
the three diagonal products independent modulo it.  Thus this criterion has
exactly the required pair-level scope.

## 2. Symmetric annihilators and the forced diagonal rank

Let

```text
T=T(U,V)={Q in Sym^2(E^*): Q(U,V)=0}.                       (7)
```

Let `D_0 subset Sym^2(E^*)` be the space of coordinate-zero-diagonal
symmetric forms.  Pairing a square-free quadratic with its edge
coefficients identifies the annihilator of `UV` with

```text
T intersect D_0.                                           (8)
```

The harmless off-diagonal factor `2` is invertible in characteristic zero.
Since `dim D_0=binomial(n,2)`, equation (1) gives

```text
dim(T intersect D_0)=binomial(n,2)-5.                       (9)
```

Set

```text
r=dim(U intersect V),
H=U+V,                         dim H=6-r,
C=ann_E(H),                    dim C=k=n-6+r.               (10)
```

Let `T_0` be the forms vanishing on `H x H`, equivalently the kernel of
restriction from `Sym^2(E^*)` to `Sym^2(H^*)`.  Inside `H^*`, put

```text
A=ann_H(V),                   B=ann_H(U),
dim A=dim B=3-r.                                         (11)
```

### Lemma 1 (residual block decomposition)

Restriction to `H` induces

```text
T/T_0 = Sym^2(A) direct-sum Sym^2(B).                       (12)
```

In particular, the residual dimensions for `r=0,1,2,3` are respectively

```text
12, 6, 2, 0.                                                (13)
```

### Proof

Choose

```text
H=R direct-sum Y direct-sum Z,
R=U intersect V,
U=R direct-sum Y,             V=R direct-sum Z.             (14)
```

A symmetric form killing `U x V` has zero `R x R`, `R x Y`, `R x Z`, and
`Y x Z` blocks.  Its only possible blocks on `H` are the symmetric `Y x Y`
and `Z x Z` blocks.  Their covector spaces are exactly `A` and `B`, proving
(12).  Their total dimension is `(3-r)(4-r)`, which gives (13).

### Lemma 2 (the exact diagonal rank)

For `diag(Q)=(Q(x_i,x_i))_i`, equality (1) forces

```text
d:=rank(diag|T)=n-4+r(r-1)/2.                              (15)
```

### Proof

Restriction to `H` is onto on all symmetric forms, so

```text
dim T_0=n(n+1)/2-(6-r)(7-r)/2.                             (16)
```

Add the residual dimension `(3-r)(4-r)` from Lemma 1.  The kernel of
`diag|T` is (8), whose dimension is fixed by (9).  Rank-nullity gives

```text
d=dim T-[binomial(n,2)-5]
 =n-4+r(r-1)/2.                                            (17)
```

No genericity is used.

## 3. Coordinate support of the invisible block

Define

```text
J=supp(C)={i: c(x_i)!=0 for some c in C},
s=|J|,                         I={0,...,n-1}\J.             (18)
```

### Lemma 3 (diagonal image and outside evaluations)

The diagonal image of `T_0` is exactly the coordinate subspace `K^J`.
Hence `s<=d`.  Every `x_i` with `i in I` belongs to `H`, and, writing

```text
a_i=(alpha -> alpha(x_i)) in A^*,
b_i=(beta  -> beta(x_i))  in B^*,                           (19)
```

one has

```text
q:=d-s
 =dim span{a_i^2 direct-sum b_i^2 : i in I}.               (20)
```

Moreover `s>=k`, and if `k>0` then active support forces `s>=k+1`.

### Proof

The space `T_0` is spanned by symmetrized tensors `c tensor ell` with
`c in C` and `ell in E^*`.  Their diagonals have entries
`2c(x_i)ell(x_i)`.  They vanish outside `J`; for each `i in J`, choose
`c(x_i)!=0` and let `ell` be supported only at `i` to obtain the `i`th
coordinate vector.  Thus the image is exactly `K^J`.

If `i in I`, every member of `C` vanishes on `x_i`, so
`x_i in C^perp=H`.  Modulo the already free coordinates `J`, Lemma 1 says
that the diagonal evaluation at `x_i` is precisely the functional
`a_i^2 direct-sum b_i^2`.  This proves (20).

Because `C subset K^J`, one has `s>=dim C=k`.  If equality held with
`k>0`, then `C=K^J`, so `H=C^perp` would omit every coordinate in `J`.
Both `U` and `V` would omit those coordinates, contradicting (4).

We also use the elementary square-span fact

```text
dim span{z_i^2} >= dim span{z_i}                            (21)
```

for vectors `z_i` in any finite-dimensional space.  Indeed, choose a
linearly independent subfamily and make it part of a basis; its pure
squares are linearly independent.

## 4. Intersection dimensions zero, one, and two are impossible

Let

```text
X=span{x_i:i in I} subset H,              dim X=n-s.        (22)
```

The evaluation map `H -> A^*` has kernel `V`.  By (20)--(21),

```text
dim image(X -> A^*) <= q,
dim(X intersect V) >= n-s-q.                              (23)
```

### Case `r=0`

Here `d=n-4`, so `q=n-4-s`.  Equation (23) gives

```text
dim(X intersect V)>=n-s-(n-4-s)=4,                         (24)
```

contradicting `dim V=3`.  This case is impossible even without the active-
support hypothesis.

### Case `r=1`

Now `k=n-5>0`.  Lemma 3 and active support give

```text
n-4<=s<=d=n-4.                                             (25)
```

Thus `s=d`, `q=0`, and `dim X=4`.  Each vector in (20) is zero, so every
outside coordinate axis lies in both `U` and `V`.  Therefore

```text
X subset U intersect V,
4=dim X<=r=1,                                               (26)
```

a contradiction.

### Case `r=2`

Here `k=n-4>0`, and the same argument gives

```text
n-3<=s<=d=n-3.                                             (27)
```

Consequently `q=0` and `dim X=3`.  Again `X subset U intersect V`, now
contradicting `3<=r=2`.

We have proved

```text
r=3,                         hence U=V.                     (28)
```

## 5. Classification of the surviving equality pairs

When `r=3`, Lemma 1 has no residual block.  Equations (15) and Lemma 3 give

```text
s=d=n-1.                                                    (29)
```

There is a unique index `i` outside `J`, and `x_i in H=U`.  Take

```text
W=U intersect ker(x_i-coordinate).
```

Then `dim W=2`, `W` is supported away from `i`, and

```text
U=K x_i direct-sum W.                                      (30)
```

In the square-free algebra, `x_iW` is a two-space supported on monomials
containing `x_i`, while `W^2` is supported on monomials not containing
`x_i`.  Hence

```text
U^2=x_iW direct-sum W^2,
5=dim U^2=2+dim W^2.                                       (31)
```

This proves (3).  Conversely, (30) and `dim W^2=3` give (31), so the
classification is exact.  Because `U=V`, the original active-support
hypothesis says precisely that `W` uses all `n-1` remaining coordinates.

## 6. The survivor is not Delta-admissible

Choose a basis of `U=V` beginning with `x_i`.  The multiplication-dual
space `L` lies in `Sym^2(U^*)`.  Every ambient square-free edge functional
has zero coordinate diagonal, so every member of `L` vanishes on
`(x_i,x_i)`.  Therefore

```text
L subset {Q in Sym^2(U^*):Q(x_i,x_i)=0}.                   (32)
```

Both spaces in (32) have dimension five: the left side by (1), and the
right side because it is a hyperplane in the six-dimensional
`Sym^2(U^*)`.  Thus equality holds.

A nonzero rank-one tensor in a symmetric matrix space has proportional
left and right factors, say it is a nonzero scalar multiple of
`lambda tensor lambda`.  Membership in (32) forces

```text
lambda(x_i)^2=0,
```

so `lambda` annihilates `x_i`.  All left and right factors of rank-one
members of `L` therefore lie in the same two-plane of `U^*`.  They cannot
supply the two bases required in (6).  The pair is not Delta-admissible.

The exact boundary is therefore

```text
active support n>=6 plus dim(UV)=5 structure:             CLASSIFIED;
only possible unbased structure:                          U=V=Kx_i+W;
Delta-admissible active-support n>=6 equality frame:      NONE;
active-support-six equality-five branch in Z_6:           EXCLUDED;
active-support-four orbit classification:                 NOT CHANGED;
active-support-five package:                              SEPARATELY OWNED;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.   (33)
```

## Replay

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_active_support_at_least_six_equality_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_active_support_at_least_six_equality_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_active_support_at_least_six_equality_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_active_support_at_least_six_equality_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_active_support_at_least_six_equality_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_active_support_at_least_six_equality_exclusion.py
```

The primary verifier checks the annihilator dimensions, forced diagonal-
rank formula, every intersection case, and exact active equality examples
over `Q`.  The independent no-import audit uses a custom finite-field row
reducer, a separate construction of symmetric annihilator equations, and
exhaustive square-span and rank-one-locus checks over `F_5`.  Those scripts
audit conventions and finite linear algebra; the written argument proves
the arbitrary-`n` characteristic-zero theorem.
