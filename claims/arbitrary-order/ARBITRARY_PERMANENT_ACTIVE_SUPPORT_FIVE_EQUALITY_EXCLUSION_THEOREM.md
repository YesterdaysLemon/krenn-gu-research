# Arbitrary permanent active-support-five equality exclusion theorem

## Status

This note classifies the active-coordinate-support-five equality case for
three-plane products in the square-free algebra.  Let `K` be a field with
`char K != 2`, let

```text
Z_5=K[x_0,...,x_4]/(x_0^2,...,x_4^2),
```

and let `U,V subset (Z_5)_1` be three-planes whose union uses all five
coordinates.  If

```text
dim(UV)=5,
```

then necessarily

```text
U=V=K x_i direct-sum W                               (1)
```

for one coordinate axis `K x_i` and a two-plane `W` on the other four
coordinates satisfying `dim(W^2)=3`.  Conversely, every pair of the form
(1) with `dim(W^2)=3` has product dimension five; it has active support five
exactly when `W` uses all four remaining coordinates.

No such equality pair is Delta-admissible at the pair level.  In a basis
beginning with `x_i`, its multiplication-dual five-space is the space of
symmetric `3 x 3` matrices whose `(0,0)` entry is zero.  Every rank-one
member has both factor lines in the fixed two-plane annihilating `x_i`, so
three members cannot have independently spanning left and right factors.

The result closes active support five only.  It does not classify
active-support-six equality pairs in `Z_6`, does not by itself exclude the
already classified active-support-four Delta-admissible frames, and does not
prove unrestricted `P_6 -> Delta_3` nonrestriction.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. Support and the rank-one criterion

For a subspace `A subset K^5`, write

```text
supp(A)={j : x_j|A is not identically zero}.
```

The pair `(U,V)` has active support five when

```text
supp(U) union supp(V)={0,1,2,3,4}.                       (2)
```

This definition is invariant under coordinate permutation and nonzero
coordinate scaling.  It does not initially require either individual plane
to use all five coordinates; that stronger fact will follow from `U=V`.

Put `B=UV`.  The multiplication map and its dual are

```text
mu:U tensor V -> B,
L=mu^*(B^*) subset U^* tensor V^*.                       (3)
```

The pair is Delta-admissible at the pair level exactly when `L` contains
three rank-one forms

```text
lambda_e tensor rho_e,             e=0,1,2,              (4)
```

whose left factors form a basis of `U^*` and whose right factors form a
basis of `V^*`.  This is the invariant rank-one criterion from the
active-support-four orbit classification.

## 2. The zero-diagonal annihilator

Let `E=K^5` with coordinate basis `e_0,...,e_4`.  Identify the dual of
`(Z_5)_2` with the ten-dimensional space of symmetric zero-diagonal
bilinear forms on `E`.  The nonzero factor `2` in this identification is why
`char K=2` is excluded.

Define

```text
S(U,V)={Q in Sym^2(E^*) : Q(U,V)=0},                     (5)
```

and let

```text
diag:S(U,V)->K^5,
diag(Q)=(Q(e_0,e_0),...,Q(e_4,e_4)).                     (6)
```

The annihilator of `UV` in `(Z_5)_2^*` is exactly

```text
S(U,V) intersect ker(diag).                              (7)
```

Consequently, the equality hypothesis `dim(UV)=5` is equivalent to

```text
dim ker(diag|S(U,V))=5.                                  (8)
```

Let

```text
r=dim(U intersect V).
```

Since both planes have dimension three in a five-space, `r` is `1`, `2`,
or `3`.  The next two sections exclude `r=1,2`.

## 3. Transverse intersection `r=1` is impossible

Put `R=U intersect V`.  When `r=1`, choose a direct sum

```text
E=R direct-sum A direct-sum C,
U=R direct-sum A,
V=R direct-sum C,
dim A=dim C=2.                                           (9)
```

If `Q(U,V)=0`, symmetry first makes `R` radical and kills the `A x C`
block.  Hence

```text
S(U,V)=Sym^2(A^*) direct-sum Sym^2(C^*),
dim S(U,V)=6.                                            (10)
```

Write the coordinate basis vector `e_j` as

```text
e_j=r_j+a_j+c_j
```

under (9).  The transpose of the diagonal map is spanned by the five
evaluation vectors

```text
(a_j^2,c_j^2) in Sym^2(A) direct-sum Sym^2(C).           (11)
```

Equation (8) and (10) would give `rank(diag)=1`.  But the coordinate vectors
span `E`, so their `A`-projections span the two-space `A`.  Two
nonproportional vectors in `A` have linearly independent symmetric squares.
The projection of the span in (11) to `Sym^2(A)` therefore has dimension at
least two, a contradiction.

Thus

```text
dim(U intersect V) != 1.                                 (12)
```

## 4. Two-dimensional intersection `r=2` is incompatible with active support

Now suppose `r=2`.  Then `H=U+V` is a hyperplane.  Choose a nonzero covector
`c` with

```text
H=ker(c),
```

and choose covectors `alpha,beta` such that

```text
U intersect V=ker(c) intersect ker(alpha) intersect ker(beta),

alpha|V=0,        beta|U=0.                              (13)
```

A block calculation gives

```text
S(U,V)=(c symmetric-tensor E^*)
       direct-sum K alpha^2 direct-sum K beta^2,
dim S(U,V)=7.                                            (14)
```

Here `c symmetric-tensor E^*` is the five-space of forms
`c tensor ell+ell tensor c`.  On coordinate diagonals it maps by

```text
c symmetric-tensor ell
  |-> (2c(e_0)ell(e_0),...,2c(e_4)ell(e_4)).             (15)
```

Because the coordinate evaluations of `ell` are arbitrary and `2!=0`, the
rank of (15) is exactly

```text
|supp(c)|.                                               (16)
```

Equations (8) and (14) give `rank(diag)=2`, so (16) forces
`|supp(c)|<=2`.  If `|supp(c)|=1`, then `H` is one coordinate hyperplane and
both `U,V` omit that coordinate, contrary to active support five.  Hence an
active pair would require

```text
|supp(c)|=2.                                             (17)
```

The image of the first summand in (14) then already equals the full
two-dimensional image of `diag`, supported on those two coordinates.
Therefore the diagonal vectors of `alpha^2` and `beta^2` vanish on each of
the other three coordinate axes.  Over a field this says

```text
alpha(e_j)=beta(e_j)=0
```

for all three indices `j` outside `supp(c)`.  Since also `c(e_j)=0`, all
three independent coordinate vectors lie in the two-space in (13), an
impossibility.

Thus an active-support-five equality pair cannot have `r=2`.  Together with
(12), this proves

```text
U=V.                                                      (18)
```

In particular, (2) now implies that the common plane individually uses all
five coordinates.

## 5. The unique symmetric multiplication relation has rank one

Write the common plane as `U`.  Since multiplication is symmetric and
`char K!=2`, it factors through

```text
mu_sym:Sym^2(U)->(Z_5)_2.                                 (19)
```

The domain has dimension six and the image `U^2` has dimension five, so

```text
ker(mu_sym)=K Q                                           (20)
```

for one nonzero symmetric tensor `Q` on `U^*`.

For each ambient coordinate put

```text
ell_j=x_j|U in U^*.                                      (21)
```

Active support makes all five `ell_j` nonzero, and the embedding
`U subset K^5` makes them span `U^*`.  The coefficient of `x_i x_j` in
`mu_sym(Q)` is a nonzero common scalar times `Q(ell_i,ell_j)`.  Hence (20)
gives the pairwise orthogonality relations

```text
Q(ell_i,ell_j)=0,                       i!=j.             (22)
```

The rank of `Q` cannot be three.  Choose three of the `ell_j` which form a
basis.  They are pairwise orthogonal; nondegeneracy makes their three
diagonal values nonzero.  Any fourth nonzero `ell_j` orthogonal to the basis
would lie in the zero radical, a contradiction.

The rank also cannot be two.  Let `R_Q` be its radical line.  In the
nondegenerate two-dimensional quotient, choose two coordinate forms with
independent images.  Every other `ell_j` is orthogonal to both and therefore
lies in `R_Q`.  There are at least three such remaining coordinate forms.
In a basis consisting of the first two forms and a generator of `R_Q`, both
bilinear forms

```text
diag(1,0,0),                     diag(0,1,0)              (23)
```

satisfy every off-diagonal condition (22): the remaining three coordinate
forms are multiples of the radical generator.  Thus the kernel in (20)
would have dimension at least two, a contradiction.

It follows that

```text
rank(Q)=1.                                                 (24)
```

The kernel line is therefore generated by `w^2` for some nonzero `w in U`.
Writing `w=sum_j w_j x_j`, its square-free square is

```text
w^2=2 sum_(i<j) w_i w_j x_i x_j.                         (25)
```

Equations (20), (25), and `2!=0` imply `w_iw_j=0` for every `i!=j`.
Thus `w` is a nonzero multiple of one coordinate vector.  After permutation
and rescaling,

```text
x_0 in U.                                                 (26)
```

Subtracting `x_0` components from two further basis vectors gives

```text
U=K x_0 direct-sum W,
W subset span{x_1,x_2,x_3,x_4},             dim W=2.      (27)
```

The product splits by edge support:

```text
U^2=(x_0W) direct-sum W^2,
dim(x_0W)=2.                                              (28)
```

Therefore `dim(U^2)=5` is equivalent to

```text
dim(W^2)=3,                                               (29)
```

or equivalently to injectivity of `Sym^2(W)->(Z_4)_2`.  This proves the
classification and its converse.  Active support five is exactly the
additional statement that `W` uses all four remaining coordinates.

## 6. Rank-one exclusion

Use a basis `(x_0,w_1,w_2)` of `U`.  The kernel of

```text
mu:U tensor U->U^2
```

is the direct sum of the three-dimensional alternating space and the line
`K(x_0 tensor x_0)`.  Consequently its dual image `L` from (3) is

```text
L={ A in Sym_3(K) : A_00=0 }.                             (30)
```

Every nonzero rank-one matrix in the symmetric space is a nonzero scalar
multiple of `lambda lambda^T`.  Membership in (30) gives

```text
lambda(x_0)^2=0,
```

so `lambda(x_0)=0`.  Thus the left and right factors of every rank-one
member of `L` lie in the fixed two-space

```text
{lambda in U^*:lambda(x_0)=0}.                            (31)
```

No three such factor lines can form bases of `U^*` on either side.  The
rank-one criterion (4) proves that no active-support-five equality pair is
Delta-admissible at pair level.

## 7. Exact example and scope boundary

The classified locus is nonempty.  Over `Q`, take

```text
U=V=span{x_0-x_4, x_1+x_2+x_4, x_3}.                    (32)
```

Here the coordinate axis is `x_3`, the other two generators use all four
remaining coordinates, and their three symmetric products are independent.
Thus `dim(U^2)=5` and the pair has active support five.  Its unique symmetric
kernel relation is `x_3^2=0`, and (30)--(31) exclude admissibility.

The exact boundary is

```text
active-support-five equality pairs:                   CLASSIFIED;
such pairs with U!=V:                                 NONE;
normal form U=V=Kx_i direct-sum W, dim W^2=3:         PROVED;
active-support-five Delta-admissible equality pairs:  NONE;

active-support-four admissible types:                 EXIST;
active-support-six equality-five classification:      OPEN;
unrestricted P_6 -> Delta_3:                          UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.       (33)
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_active_support_five_equality_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_active_support_five_equality_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_active_support_five_equality_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_active_support_five_equality_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_active_support_five_equality_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_active_support_five_equality_exclusion.py
```

The primary verifier checks the block-annihilator dimensions, the diagonal
rank mechanisms in the `r=1,2` exclusions, the exact example, its unique
rank-one symmetric relation, and the dual rank-one factor obstruction.  The
independent no-import audit exhausts all `1,210^2` ordered pairs of
three-planes in `F_3^5`: among full-union-support pairs it finds exactly 340
equality-five pairs, all diagonal `U=V`, and independently verifies the
coordinate-axis classification and rank-one exclusion.  This finite census
is audit evidence only; Sections 2--6 are the characteristic-not-two proof.
