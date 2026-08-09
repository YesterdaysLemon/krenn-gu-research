# Primitive P7 additive gauge is rigid on the edge torus

## Status

**Exact characteristic-zero gauge-rigidity and quadratic reconstruction
theorem.**  Work first in the eight-variable Boolean algebra

```text
A=K[z_0,...,z_7]/(z_0^2,...,z_7^2),
ell=z_0+...+z_7,
Q_B=sum_(i<j) b_ij z_i z_j.
```

The quotient-Hessian theorem leaves the apparent additive fibre

```text
b -> b+R u,                 (R u)_ij=u_i+u_j.        (1)
```

This note proves that the fibre is rigid on the primitive-square edge
torus.  Put `U=sum_i u_i z_i`.  Then

```text
Q_(B+R u)=Q_B+ell U.                                  (2)
```

If both endpoints satisfy the primitive P7 equation, their exact transition
law is the quadratic degree-three obstruction

```text
U(Q_B+Q_(B+R u))=0.                                  (3)
```

Every nonzero solution of (3) between primitive squares has

```text
|supp u|<=4,
b_jk=0 for every j,k outside supp u.                 (4)
```

Thus the complement of the gauge support is an independent set of size at
least four.  In particular, if every `b_ij` is nonzero, then `u=0`.
This chord-rigidity statement in fact holds on every `n`-vertex Boolean
algebra with `n>=8`.

For P7, multiplication by `ell^2` is explicitly invertible.  Therefore any
fixed quotient representative `p` has a canonical defect

```text
Theta(Q_p)=(ell^2)^(-1)(ell Q_p^2) in A_3,            (5)
```

and its complete primitive additive fibre is the eight-variable quadratic
system

```text
Theta(Q_p)+2Q_p U+ell U^2=0.                         (6)
```

If this system has a full-edge-torus solution, chord rigidity makes it the
only solution in that additive fibre.  No existence or rational-solvability
claim is made.

Consequently, on the quotient-Hessian-open chart, identical `H_4/H_6` decks
determine a primitive full-edge-torus graph uniquely: the eight-dimensional
linear fibre found by quotient tomography contains no second physical
primitive square.

The coordinate boundary in (4) is essential.  Star-supported square-zero
quadrics give exact nontrivial gauge families there.  This theorem does not
prove that the primitive-square edge-torus locus is nonempty, does not treat
the quotient-Hessian-singular branch, and does not settle P7 or Krenn--Gu.
Those questions remain **UNKNOWN/UNRESOLVED**.

## 1. Exact Boolean gauge law

Let `E=binom({0,...,7},2)` and let `R:K^8->K^E` be the unsigned incidence
map in (1).  Boolean multiplication gives

```text
ell U=sum_(i<j)(u_i+u_j)z_i z_j,
```

which proves (2).

Suppose

```text
ell Q_B^2=0,
ell Q_(B+R u)^2=0.                                   (7)
```

Subtracting the two equations and using (2) gives

```text
0=ell((Q_B+ell U)^2-Q_B^2)
 =ell^2(2U Q_B+ell U^2)
 =ell^2 U(2Q_B+ell U).                               (8)
```

Multiplication by `ell^2` is an isomorphism

```text
ell^2:A_3 -> A_5.                                    (9)
```

Indeed, after complementing the five-set rows, its matrix is twice the
disjointness matrix on three-subsets of an eight-set.  Its spectrum is

```text
20^(1), (-12)^(7), 6^(20), (-2)^(28),
det=-2^64*3^27*5.                                   (10)
```

Explicitly, the disjointness eigenvalue in Boolean rank `r=0,1,2,3` is
`2(-1)^r binom(5-r,3-r)`, with multiplicity
`binom(8,r)-binom(8,r-1)`; this gives (10) and the displayed determinant.
Thus every eigenvalue is nonzero in characteristic zero.  Equivalently,
(9) is the middle Boolean Lefschetz isomorphism.  Cancelling `ell^2` in
(8) proves (3), since

```text
2Q_B+ell U=Q_B+Q_(B+R u).                            (11)
```

In coordinates, (3) is the fixed family of 56 quadratic equations

```text
u_i b_jk+u_j b_ik+u_k b_ij
 +u_i u_j+u_i u_k+u_j u_k=0             (i<j<k).    (12)
```

Thus quotient tomography does not leave an arbitrary affine eight-space:
physical primitive endpoints must also lie on the explicit quadratic gauge
incidence (12).

For `n>=8`, the same calculation takes place in the `n`-variable Boolean
algebra.  The Boolean Lefschetz map `ell^2:A_3->A_5` is then injective
(although it is square only at `n=8`): its matrix is `2W_(3,5)(n)`, which
has full column rank for `3+5<=n`.  Hence (3) and (12) remain valid with
`binom(n,3)` coordinates.

## 2. Large gauge support is impossible in every order `n>=8`

For a nonzero `U`, write

```text
S=supp u,                    T=V minus S,
s=|S|.
```

### Lemma 1 (large-support injectivity)

If `s>=5`, multiplication by `U` is injective from `A_2` to `A_3`.

### Proof

Rescaling the variables in `S` conjugates multiplication by `U` to
multiplication by `ell_S=sum_(i in S)z_i`.  Decompose source and target by
their degree `q` in the variables of `T`.  For `q=0,1,2`, the source blocks
are respectively

```text
A_2(S), A_1(S) tensor A_1(T), A_0(S) tensor A_2(T),
```

and multiplication acts on the `S` factor by the unsigned inclusion maps

```text
W_(2,3)(s),                  W_(1,2)(s),
W_(0,1)(s).                                          (13)
```

In characteristic zero these have full column rank for `s>=5` (the first
is square and invertible at `s=5`, and remains injective above the middle
rank; the other two are already injective for `s>=3` and `s>=1`).  Every
block is therefore injective.

### Theorem 2 (support bound)

In an `n`-variable Boolean algebra with `n>=8`, if (7) holds and `u!=0`,
then `|supp u|<=4`.

### Proof

Assume instead that `s>=5`.  Lemma 1 and (3) force

```text
Q_B+Q_(B+R u)=0,
2Q_B+ell U=0.                                        (14)
```

Primitivity of `Q_B=-ell U/2` then yields

```text
0=ell Q_B^2=(1/4)ell^3 U^2.                          (15)
```

The Boolean Lefschetz map

```text
ell^3:A_2 -> A_5                                    (16)
```

is injective in characteristic zero: its matrix is `6W_(2,5)(n)`, which
has full column rank for `2+5<=n`.  Hence `U^2=0`.  But

```text
U^2=2 sum_(i<j)u_i u_j z_i z_j,                      (17)
```

so at most one coordinate of `u` is nonzero.  This contradicts `s>=5`.

## 3. Small gauge support forces a coordinate boundary

### Theorem 3 (independent-complement obstruction)

In an `n`-variable Boolean algebra with `n>=8`, if (7) holds and `u!=0`,
then every edge internal to `T=V minus supp u` vanishes in `B`.

### Proof

Theorem 2 gives `1<=s<=4`.  Put

```text
C=Q_B+Q_(B+R u)=2Q_B+ell U.
```

Equation (3) is `UC=0`.  Fix `i in S` and distinct `j,k in T`.  In the
coefficient of `z_i z_j z_k`, the only surviving contribution is the
internal-`T` edge of `C`, because `u_j=u_k=0`:

```text
[z_i z_j z_k](UC)=u_i [z_j z_k]C=2u_i b_jk.         (18)
```

Choose `i` with `u_i!=0`.  Characteristic zero and (18) give `b_jk=0`.
This holds for every pair in `T`.  Since `|T|=n-s>=4`, a full-edge-torus
`B` cannot admit a nonzero gauge.  Together with Theorem 2 this proves the
following dimension-free form.

### Corollary 4 (primitive chord rigidity)

For every `n>=8`, an affine additive chord

```text
Q, Q+ell U
```

cannot contain two primitive endpoints if one endpoint has every edge
coefficient nonzero, unless `U=0`.

The conclusion is sharp as a boundary statement.  For any scalars
`a_1,...,a_7,lambda`, put

```text
Q=z_0 sum_(j=1)^7 a_j z_j,
U=lambda z_0,
Q'=Q+ell U=z_0 sum_(j=1)^7(a_j+lambda)z_j.           (19)
```

Both `Q^2` and `(Q')^2` vanish, so both are primitive squares, and they
differ by the nonzero one-vertex additive gauge when `lambda!=0`.  The
seven vertices outside its support form the forced independent set.

## 4. The quadratic Lefschetz gauge system

Return to `n=8` and write

```text
L_2:A_3->A_5,                 L_2(F)=ell^2 F.
```

Equation (10) makes `L_2` invertible.  For any fixed edge representative
`p`, define `Theta(Q_p)` by (5).  If `b=p+R u`, then

```text
ell Q_b^2
 =ell Q_p^2+ell^2(2Q_p U+ell U^2)
 =ell^2(Theta(Q_p)+2Q_p U+ell U^2).                  (20)
```

This proves (6).  It is a completely explicit quadratic obstruction in the
eight gauge coordinates.  After complementing five-set rows, let `K` be
the matrix `2 KG(8,3)`.  Its inverse is the fixed cubic polynomial

```text
K^(-1)=(-K^3+12K^2+220K-1056I)/2880,                (21)
```

because

```text
K^4-12K^3-220K^2+1056K+2880I=0.                     (22)
```

Thus `Theta` requires no search or unspecified inverse: complement
`ell Q_p^2`, apply (21), and read the result in the three-set basis of
`A_3`.

If two gauge values solve (6), their corresponding quadrics are primitive
and differ by `ell` times a linear form.  Corollary 4 shows that the
presence of one full-edge-torus solution makes it the sole solution of the
entire quadratic gauge system.  It does not show that any solution exists.

## 5. Quotient-deck rigidity

Let `D` be the full edge Hessian built from the four-hafnian deck and let
`c` be the six-hafnian cofactor vector, as in
`P7_PRIMITIVE_BOOLEAN_SQUARE_QUOTIENT_HESSIAN_CORANK_AND_TOMOGRAPHY.md`.
On the quotient-open chart that note proves

```text
ker D=im R,
D b=3c.                                              (23)
```

### Corollary 5 (physical tomography is unique)

Let `B` be a primitive-square full-edge-torus graph on the quotient-open
chart.  If another graph `B'` is primitive and has the same labeled
`H_4/H_6` deck, then `B'=B`.

### Proof

The common deck gives the same `D,c`.  Euler applied to both graphs gives
`D(b'-b)=0`.  Equation (23) therefore writes `b'-b=R u`.  Theorems 2 and 3
exclude every nonzero `u` because `B` has no zero edge.

More constructively, the common deck first recovers

```text
p=3(D|_P)^(-1)c,
```

then (5)--(6) give the exact quadratic gauge test.  If a torus realization
exists it is unique.  Neither the quotient formula nor chord rigidity
proves existence or that the unique solution is rational over a chosen
ground field.

This removes the additive ambiguity only after a physical second primitive
endpoint is imposed.  It does not claim that arbitrary vectors in the
linear Euler fibre are graph roots of the fixed deck.

## 6. Exact wall

```text
Boolean additive gauge law Q_(B+Ru)=Q_B+ell U:       PROVED;
primitive-to-primitive gauge obstruction (3)/(12):   PROVED, QUADRATIC;
primitive chord rigidity for every n>=8:              PROVED;
nonzero primitive gauge support:                      AT MOST FOUR;
complement of nonzero gauge support in B:             INDEPENDENT SET;
nontrivial gauges on coordinate boundary:             EXIST, EXACT FAMILY;
nontrivial gauge from a primitive full-edge graph:     IMPOSSIBLE;
fixed-representative P7 gauge equation (6):            EXACT, QUADRATIC;
full-torus solution of (6), if present:                UNIQUE;
H4/H6 tomography on quotient-open edge torus:         UNIQUE;
primitive-square edge-torus nonemptiness:              UNKNOWN;
quotient-Hessian-singular primitive-square branch:     UNKNOWN;
degree-67 radial incidence nonemptiness:               UNKNOWN;
P7 pinned matrix full rank on the edge torus:          UNKNOWN;
global Krenn--Gu:                                      UNRESOLVED. (24)
```

No graph family is enumerated, and no numerical, finite-field, support
search, or parameter sweep enters the proof.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_primitive_additive_gauge_rigidity_and_coordinate_boundary.py
python claims/p7/audit_p7_primitive_additive_gauge_rigidity_and_coordinate_boundary.py
python -m py_compile verify_p7_primitive_additive_gauge_rigidity_and_coordinate_boundary.py audit_p7_primitive_additive_gauge_rigidity_and_coordinate_boundary.py
uv run --with ruff ruff check verify_p7_primitive_additive_gauge_rigidity_and_coordinate_boundary.py audit_p7_primitive_additive_gauge_rigidity_and_coordinate_boundary.py
```

The primary verifier checks the two Lefschetz ranks, the spectrum and fixed
cubic inverse of the complemented map, every support block, the formal
Boolean transition and arbitrary-representative defect laws, all 56
coordinate equations, the independent-complement coefficient, and the
sharp star boundary family.  The independent standard-library audit
rebuilds the Boolean multiplication, integer matrix polynomial, inverse,
and exact rational ranks without importing the primary or project code.
