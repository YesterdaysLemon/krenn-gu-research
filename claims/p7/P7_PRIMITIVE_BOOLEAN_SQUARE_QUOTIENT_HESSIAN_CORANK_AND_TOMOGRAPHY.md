# Primitive P7 squares force an eight-dimensional Hessian kernel

## Status

**Exact characteristic-zero quotient-Hessian theorem and sharp ambient
control.**  Let

```text
A=K[z_0,...,z_7]/(z_0^2,...,z_7^2),
ell=z_0+...+z_7,
Q_B=sum_(i<j) b_ij z_i z_j,
```

and assume the surviving primitive P7 equation

```text
ell Q_B^2=0.                                           (1)
```

Write `H_U=haf B[U]` for four-sets, let `h=haf B`, and put

```text
c_e=haf B[V minus e],
D_(e,f)=haf B[V minus (e union f)]  if e and f are disjoint,
        0                            otherwise.         (2)
```

Thus `c` is the six-hafnian cofactor vector and `D` is the full
edge-indexed Hessian of the eight-vertex hafnian.

This note proves that (1) forces much more than one singular direction:

```text
im W_(1,2)(8) subset ker D,
dim im W_(1,2)(8)=8,
rank D<=20.                                            (3)
```

Equivalently, every additive edge vector `(u_i+u_j)_(ij)` is killed by `D`.
The cofactor vector is primitive as well:

```text
sum_(j!=i)c_ij=0                    for every i.        (4)
```

Hence `D` descends to a symmetric operator on the 20-dimensional
zero-row-sum edge space.  On the open where this quotient operator is
invertible, the `H_4/H_6` deck reconstructs the primitive component of the
graph exactly and leaves only the eight-dimensional additive gauge.  The
top hafnian obeys a quotient scalar stress.

The bound in (3) is sharp for the ambient 14-dimensional primitive
four-set space: the sum of the 14 standard `(4,4)` polytabloids has a
catalecticant of rank exactly 20.  A named principal `20 x 20` minor is

```text
1551182856192 = 2^18 * 3^6 * 8117 !=0.                (5)
```

This fixed control is not asserted to be a square `Q_B^2` or a physical
hafnian deck.  It proves that no representation-theoretic argument from
four-set primitivity alone can increase the forced Hessian corank beyond
eight.

The theorem does **not** show that the quotient-open chart meets the
primitive-square edge torus, and it does not exclude the quotient-singular
branch.  Primitive-square torus nonemptiness, P7, and global Krenn--Gu remain
**UNKNOWN/UNRESOLVED**.

## 1. Primitive four-set data

Let `E=binom(V,2)` and let `R:K^8 -> K^E` be the unsigned vertex-edge
incidence map

```text
(R u)_ij=u_i+u_j.                                     (6)
```

Its transpose takes edge data to vertex row sums.  Directly,

```text
R^T R=6I_8+J_8,                                      (7)
```

whose eigenvalues are `14` once and `6` seven times.  Thus `R` has rank
eight in characteristic zero.  Put

```text
C=im R,
P=ker R^T.
```

Then

```text
K^E=C direct-sum P,        dim C=8,        dim P=20.  (8)
```

The preceding dual-triangle theorem proves that (1) is equivalent to the
four-set vector `H=(H_U)` being Boolean primitive:

```text
sum_(l notin T) H_(T union {l})=0       for every |T|=3, (9)
```

and that four-set complementation fixes `H`:

```text
H_U=H_(V minus U).                                    (10)
```

## 2. The entire incidence space lies in the Hessian kernel

For a vertex `k`, let `s^(k)=R e_k`; thus `s^(k)_f=1` exactly when the edge
`f` contains `k`.

### Theorem 1 (incidence-kernel propagation)

Every primitive square (1) satisfies

```text
D s^(k)=0                         for k=0,...,7.       (11)
```

Consequently `C subset ker D`, `im D subset P`, and `rank D<=20`.

### Proof

Fix an edge `e`.  If `k in e`, no edge disjoint from `e` contains `k`, so
the `e` coordinate of `D s^(k)` is zero.  If `k notin e`, then (2) and
complementation (10) give

```text
(D s^(k))_e
 =sum_(l notin e union {k}) H_(V minus (e union {k,l}))
 =sum_(l notin e union {k}) H_(e union {k,l}).        (12)
```

The final expression is the down equation (9) on the triple `e union {k}`,
so it is zero.  This proves (11).  The rank and image statements follow
from (7), symmetry of `D`, and (8).

This proof uses both exact halves of the Boolean middle-degree theorem:
primitivity supplies (9), while the even `(4,4)` complement action supplies
(10).  Neither a generic singular-Hessian argument nor one pinned kernel
direction gives the eight vectors (11).

## 3. The six-hafnian cofactor is a primitive edge vector

Homogeneous Euler for the degree-four hafnian is

```text
D b=3c.                                               (13)
```

### Corollary 2 (cofactor row-sum law)

Every solution of (1) satisfies (4), equivalently `c in P`.

### Proof

For each vertex-incidence vector, symmetry, (11), and (13) give

```text
(s^(k))^T c=(1/3)(s^(k))^T D b=0.                    (14)
```

The left side is exactly `sum_(j!=k)c_kj`.

There is also a direct square-free explanation.  Multiplying (1) by `Q_B`
gives `ell Q_B^3=0`; after complementing six-sets to edges, its eight
seven-set equations are exactly (4).  Equation (14) shows that this cubic
propagation is already encoded by the quotient Hessian.

## 4. Quotient-Hessian tomography

Let

```text
Pi=I-R(R^T R)^(-1)R^T                                (15)
```

be the projection onto `P`, and write

```text
p=Pi b,                  b=p+R u.                    (16)
```

Because `D R=0`, equation (13) is

```text
(D|_P) p=3c.                                          (17)
```

### Theorem 3 (primitive quotient reconstruction)

Assume the induced operator `D|_P:P->P` is invertible.  Then

```text
p=3(D|_P)^(-1)c.                                      (18)
```

Thus `(H_4,H_6)` determines the primitive edge component uniquely.  The
complete fibre of (13) is

```text
b=p+R u,                         u in K^8.             (19)
```

The scalar hafnian obeys

```text
4h=p^T c=3c^T(D|_P)^(-1)c.                            (20)
```

### Proof

Equations (11), (13), and the direct sum (8) give (17).  Invertibility gives
(18), while `ker D=C` on this chart gives exactly (19).  Euler also gives
`4h=b^T c`.  Since `c in P` is orthogonal to `R u`, substitution of (16) and
(18) proves (20).

For an inverse-free coordinate form, choose any `28 x 20` full-column-rank
matrix `X` with `im X=P`, and put

```text
K_H=X^T D X,                  z=X^T c.                (21)
```

On `det K_H!=0`, if `p=X xi`, then

```text
K_H xi=3z,
xi=3 K_H^(-1)z,
4 det(K_H) h=3 z^T adj(K_H) z.                       (22)
```

Changing the basis `X` only multiplies the determinant-cleared equation by
the expected nonzero square, so its vanishing content is intrinsic.

The additive gauge in (19) is real information, not a defect of coordinates.
Writing `r=R^T b`, its representative is

```text
u=(6I+J)^(-1)r.                                      (23)
```

The primitive equation must still determine or obstruct these eight row-sum
coordinates.  The star-closure pencil is exactly that remaining nonlinear
problem.  Its complementary radial reduction, corank-one degree-67 equations,
and retained deeper singular branch are proved separately in
`P7_PRIMITIVE_BOOLEAN_SQUARE_COMPLEMENT_RADIAL_AND_EXCEPTIONAL_CLIQUE_THEOREM.md`.
The additive fibre is also no longer an actual multiplicity on the primitive
edge torus: `P7_PRIMITIVE_ADDITIVE_GAUGE_RIGIDITY_AND_COORDINATE_BOUNDARY_THEOREM.md`
proves that it contains at most one primitive full-edge point and gives the
exact quadratic Lefschetz system that tests its existence.

## 5. Sharp rank-20 primitive control

Let `T` range over the 14 standard Young tableaux of shape `(4,4)`.  If its
columns are `(a_1,b_1),...,(a_4,b_4)`, let

```text
e_T=product_(j=1)^4 (z_(a_j)-z_(b_j)),
H_*=sum_T e_T.                                        (24)
```

Every `e_T` is a `(4,4)` polytabloid, hence satisfies (9) and (10).  Form
`D_*` from `H_*` by (2), using (10) to identify its four-set entries.

Take the principal rows and columns indexed by

```text
01,02,03,04,05,06,
12,13,14,15,16,
23,24,25,26,
34,35,36,
45,46.                                                (25)
```

Direct exact determinant evaluation gives (5).  Therefore `rank D_*>=20`.
Theorem 1 applies to every primitive four-set vector, so `rank D_*<=20`.
Thus

```text
rank D_*=20,                  ker D_*=C.              (26)
```

This proves sharpness of the universal corank-eight theorem inside the
ambient primitive space.  It does not prove that `H_*` has a square root in
the Boolean edge algebra, much less a full-edge-torus graph root.

## 6. Exact frontier

```text
primitive P7 square makes H_4 Boolean primitive:          PROVED;
full hafnian Hessian kills vertex-incidence space:        PROVED;
forced full-Hessian corank:                               AT LEAST EIGHT;
six-hafnian cofactor vertex row sums:                     ALL ZERO;
quotient edge space dimension:                            TWENTY;
primitive component recovery on quotient determinant:    UNIQUE;
remaining graph fibre there:                              ADDITIVE 8-GAUGE;
quotient scalar stress (20)/(22):                         EXACT;
ambient primitive corank-eight bound:                     SHARP;
sharp control is a physical primitive square:             NOT CLAIMED;
primitive-square locus meets quotient-Hessian open:       UNKNOWN;
quotient-singular primitive-square edge torus:            UNKNOWN;
primitive-square locus meets any full edge torus:         UNKNOWN;
P7 nonrestriction and global Krenn--Gu:                   UNRESOLVED. (27)
```

No graph family, support family, parameter tuple, numerical approximation,
or finite field is searched.

## Replay

```powershell
uv run --with sympy python verify_p7_primitive_boolean_square_quotient_hessian_corank_and_tomography.py
python audit_p7_primitive_boolean_square_quotient_hessian_corank_and_tomography.py
python -m py_compile verify_p7_primitive_boolean_square_quotient_hessian_corank_and_tomography.py audit_p7_primitive_boolean_square_quotient_hessian_corank_and_tomography.py
uv run --with ruff ruff check verify_p7_primitive_boolean_square_quotient_hessian_corank_and_tomography.py audit_p7_primitive_boolean_square_quotient_hessian_corank_and_tomography.py
```

The primary verifier checks (11) on a basis of the complete 14-dimensional
primitive four-set space, the exact incidence decomposition, the rank-20
minor, and the quotient identities.  The independent standard-library audit
rebuilds the polytabloids, catalecticant, Bareiss determinant, kernel, and a
fixed quotient-gauge control without importing the primary or project code.
