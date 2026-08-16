# Arbitrary permanent co-two `r=4` based-frame orbit classification

## Status

This note classifies the **based** pair-level `Delta_3` frames inside each
of the three admissible unbased equality-five pair orbits

```text
(3,1),                         (4,1),                         (4,2).
```

The classification is exact over every field of characteristic zero.  Up
to colour permutation and nonzero colour scalings, the raw numbers of
admissible frames are respectively

```text
2,                              14,                            12.
```

After the ordered pair stabilizer in the ambient coordinate monomial group
is also divided out, these become

```text
1,                               4,                             3.       (1)
```

If exchange of the two omitted modes is allowed, the counts become

```text
1,                               2,                             3.       (2)
```

There are no continuous based-frame moduli: all rank-one points from which
an admissible frame can be built are rational and form finite sets of sizes
`4,6,6`.

Consequently every admissible `(3,1)` frame transports to the displayed
representative of the unbased classification.  This is false for `(4,1)`
and `(4,2)`.  The displayed `(4,1)` frame is one of the mixed types and
misses a second, pure-triangle type even after the omitted modes are
exchanged.  The displayed fixed `(4,2)` frame is only one of three based
frame types.

This theorem is pair-level only.  It does not transport any full-extension
exclusion to the alternate frames, does not construct an extension, and
does not exclude the remaining unbased or based types.  Unrestricted
`P_6 -> Delta_3`, arbitrary-order permanent nonrestriction, and the global
Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. Rank-one reformulation of a based frame

Let

```text
Z_4=K[x_0,x_1,x_2,x_3]/(x_0^2,x_1^2,x_2^2,x_3^2)
```

over a characteristic-zero field.  Fix an equality-five pair of
three-planes `U,V subset (Z_4)_1`, put `B=UV`, and let

```text
mu:U tensor V -> B,
L=mu^*(B^*) subset U^* tensor V^*.                           (3)
```

For ordered bases `(u_0,u_1,u_2)` and `(v_0,v_1,v_2)`, let
`lambda_i` and `rho_i` be their dual covectors.  The rank-one criterion in
the unbased orbit theorem says that the two bases form a pair-level
`Delta_3` frame exactly when

```text
[lambda_i tensor rho_i] in P(L),                i=0,1,2,     (4)
```

and the three left factors and three right factors are projective bases.

Thus put

```text
R(L)=(P(U^*) x P(V^*)) intersect P(L).                       (5)
```

Nonzero rescaling of a colour vector only changes representatives of the
two projective factors in (5), and common colour permutation only reorders
the three paired points.  Hence based frames modulo colour scaling and
permutation are precisely the unordered three-subsets of `R(L)` whose two
projections both span.

## 2. Canonical pairs and their exact rank-one loci

Use the canonical ordered bases from the unbased classification:

```text
(3,1):
 U: (x_1-x_2, x_3, -x_0+x_2),
 V: (-x_1+x_2, x_0+x_1, x_3).

(4,1):
 U: (-x_0+x_2, x_0-x_3, x_1-x_2),
 V: (x_0+x_1-x_2+x_3, x_0+x_1, -x_1+x_2).

(4,2):
 U: (x_0-x_3, x_1-x_3, x_2-x_3),
 V: (x_1+x_2, x_0+x_2, x_2-x_3).                           (6)
```

Write a point of `P(U^*) x P(V^*)` as

```text
([a_0:a_1:a_2],[b_0:b_1:b_2]).
```

Exact multiplication in the square-free algebra and row reduction of (3)
give the following four membership equations for `R(L)`:

```text
(3,1):
 a_0 b_2+a_1 b_0=0,       a_1 b_2=0,
-a_0 b_1+a_2 b_0=0,       b_1(a_0+a_2)=0.                  (7)

(4,1):
 a_0(b_1+b_2)=0,          a_1(b_0+b_2)=0,
 2a_0b_1+(a_1+a_2)b_0=0, b_1(a_0+a_2)=0.                  (8)

(4,2):
 a_0(b_1-b_2)=0,          a_1(b_0-b_2)=0,
 b_0(a_1-a_2)=0,          b_1(a_0-a_2)=0.                  (9)
```

In coordinates relative to (6), the complete projective solution sets are
as follows.  Each ordered pair in the table is `(a;b)`.

```text
(3,1):
 P0=( (0,0,1); (0,0,1) )
 P1=( (0,1,0); (0,1,0) )
 P2=( (1,0,0); (1,0,0) )
 P3=( (1,0,-1);(1,-1,0) )

(4,1):
 P0=( (0,0,1);   (0,0,1) )
 P1=( (0,1,0);   (0,1,0) )
 P2=( (0,1,-1);  (1,0,-1) )
 P3=( (1,0,0);   (1,0,0) )
 P4=( (1,0,-1);  (2,1,-1) )
 P5=( (1,-1,-1); (1,1,-1) )

(4,2):
 P0=( (0,0,1); (0,0,1) )
 P1=( (0,1,0); (0,1,0) )
 P2=( (0,1,1); (1,0,1) )
 P3=( (1,0,0); (1,0,0) )
 P4=( (1,0,1); (0,1,1) )
 P5=( (1,1,1); (1,1,1) ).                                (10)
```

### Completeness of the catalogs

The nine pivot charts obtained by declaring the first nonzero coordinate
of `a` and of `b` to be one form a disjoint cover of the product of
projective planes.  Substitution in (7)--(9) gives the following complete
list of nonempty charts; all omitted charts contain the equation `1=0`.

```text
type       pivot(a),pivot(b)          normalized solutions

(3,1)          (0,0)                 P2,P3
               (1,1)                 P1
               (2,2)                 P0

(4,1)          (0,0)                 P3,P4,P5
               (1,0)                 P2
               (1,1)                 P1
               (2,2)                 P0

(4,2)          (0,0)                 P3,P5
               (0,1)                 P4
               (1,0)                 P2
               (1,1)                 P1
               (2,2)                 P0.                    (11)
```

For example the `(4,1)` point `P4` appears in the `(0,0)` chart as
`((1,0,-1);(1,1/2,-1/2))`.  Characteristic zero permits the displayed
division.  On each chart, the two factored equations in (7), (8), or (9)
split into zero/nonzero branches and the remaining equations are linear;
the results are exactly (11).  This proves (10) set-theoretically over an
arbitrary characteristic-zero field, not merely over an algebraic closure
or a sampled finite field.

## 3. All admissible colour triples

For compactness write `ijk` for `{P_i,P_j,P_k}`.  Exact `3 x 3`
determinants of the left and right coordinates in (10) give all and only
the following spanning triples:

```text
(3,1):
 012, 013.

(4,1):
 013, 014, 015, 024, 025, 035, 045,
 123, 124, 134, 135, 234, 235, 245.

(4,2):
 013, 015, 024, 025, 035, 045,
 123, 124, 134, 135, 234, 245.                              (12)
```

This proves the raw counts `2,14,12`.  By Section 1, (12) is already a
complete classification modulo common colour permutation and all nonzero
colour scalings.

## 4. Ordered pair stabilizers

The ambient automorphisms relevant here are coordinate permutations and
nonzero coordinate scalings.  For a full-support normal, a diagonal map
preserving its hyperplane is projectively scalar.  For `(3,1)`, the three
active coordinates must have one common scale, while the inactive
coordinate may have another; this connected torus fixes every point of the
finite set (10).  Thus no unlisted torus parameter acts on (12).

The residual ordered pair stabilizers and their actions on point labels are
generated by

```text
(3,1):  (P2 P3).

(4,1):  (P0 P4)(P2 P5),
         (P1 P4)(P2 P3).

(4,2):  (P1 P3)(P2 P4),
         (P0 P5)(P2 P4),
         (P0 P3)(P1 P5).                                  (13)
```

These are induced respectively by permutations inside the sign blocks;
the groups are `S_2`, `S_3`, and `(S_2 x S_2) semidirect S_2` of orders
`2,6,8`.  Their orbits on (12) are

```text
type     representative     orbit size      invariant

(3,1)       012                 2            unique

(4,1)       014                 1            k=3
            013                 6            k=2  (displayed)
            025                 6            k=1
            235                 1            k=0

(4,2)       013                 4            e=0  (displayed)
            025                 4            e=1
            024                 4            e=2.                           (14)
```

For `(4,1)`, the point set has two stabilizer orbits

```text
T_+={P0,P1,P4},                 T_-={P2,P3,P5},             (15)
```

and `k` is the number of selected points in `T_+`.  For `(4,2)`, the point
orbits have sizes four and two,

```text
Q={P0,P1,P3,P5},                E={P2,P4},                  (16)
```

and `e` is the number selected from `E`.  These invariants immediately
separate the rows of (14).

This proves the ordered-pair count (1).

## 5. Optional exchange of the omitted modes

The two omitted graph modes may be regarded as labeled or may be exchanged
by a graph-mode permutation.  The two conventions must not be mixed.

In the canonical normal forms, coordinate sign changes taking the first
normal to the second and conversely induce the following factor-swapping
actions on (10):

```text
(3,1): (P0 P1)(P2 P3),

(4,1): (P0 P5)(P1 P3)(P2 P4),

(4,2): (P0 P5)(P1 P3)(P2 P4).                             (17)
```

For `(4,1)`, (17) exchanges `T_+` and `T_-`, so it identifies `k` with
`3-k`.  The two remaining types are the pure triangles (`k=0 or 3`) and
the mixed triples (`k=1 or 2`).  For `(4,2)`, (17) preserves the value of
`e`, so none of its three orbits merge.  The `(3,1)` orbit was already
unique.  This proves (2).

## 6. Integral representative frames

The following frames give one exact representative for every row of (14).
Each triple is ordered only for display; common colour permutation and
nonzero scaling are already quotiented out.  Direct multiplication gives
mixed-product rank two and total product rank five in every case.

### `(3,1)`, the unique orbit `012`

```text
U: ( x_1-x_2,          x_3,             -x_0+x_2 )
V: (-x_1+x_2,          x_0+x_1,          x_3 )              (18)
```

### `(4,1)`, `k=3`, representative `014`

```text
U: ( x_0-x_1,          x_0-x_3,          x_0-x_2 )
V: ( x_0-x_1+x_2+x_3,  x_0+x_1+x_2-x_3, x_0+x_1-x_2+x_3 ) (19)
```

### `(4,1)`, `k=2`, representative `013` (the displayed orbit)

```text
U: (-x_0+x_2,          x_0-x_3,          x_1-x_2 )
V: ( x_0+x_1-x_2+x_3,  x_0+x_1,         -x_1+x_2 )         (20)
```

### `(4,1)`, `k=1`, representative `025`

```text
U: ( x_0-x_1-x_2+x_3,  x_2-x_3,          x_0-x_2 )
V: ( x_0+x_3,          x_2-x_3,          x_0+x_1 )         (21)
```

### `(4,1)`, `k=0`, representative `235`

```text
U: ( x_0-x_1+x_2-x_3,  x_0-x_1-x_2+x_3, x_0+x_1-x_2-x_3 )
V: ( x_0+x_2,          x_0+x_3,          x_0+x_1 )         (22)
```

### `(4,2)`, `e=0`, representative `013` (the displayed fixed orbit)

```text
U: ( x_0-x_3,          x_1-x_3,          x_2-x_3 )
V: ( x_1+x_2,          x_0+x_2,          x_2-x_3 )         (23)
```

### `(4,2)`, `e=1`, representative `025`

```text
U: ( x_1-x_2,          x_0-x_1,          x_0-x_3 )
V: ( x_1+x_3,          x_0-x_1,          x_0+x_2 )         (24)
```

### `(4,2)`, `e=2`, representative `024`

```text
U: ( x_0+x_1-x_2-x_3,  x_1-x_3,          x_0-x_3 )
V: ( x_0+x_1+x_2+x_3,  x_1+x_2,          x_0+x_2 )         (25)
```

The normals of (19)--(22) are `(1,1,1,1)` and
`(1,-1,-1,-1)`.  The normals of (23)--(25) are `(1,1,1,1)` and
`(1,1,-1,-1)`.  Hence the alternate frames stay inside the asserted
unbased pair rather than changing orbit.

## 7. Exact transport boundary

```text
finite rank-one loci of sizes 4,6,6:                    PROVED;
all admissible colour triples:                          CLASSIFIED;
ordered-pair based-frame orbit counts:                  1,4,3;
counts after optional omitted-mode exchange:            1,2,3;

every (3,1) frame transports to its displayed frame:    YES;
every (4,1) frame transports to its displayed frame:    NO;
every (4,2) frame transports to its displayed frame:    NO;

transport of fixed-frame extension exclusions to
  alternate (4,1) or (4,2) based frames:                NOT PROVED;
existence of a full P_6 -> Delta_3 restriction:          NOT IMPLIED;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.     (26)
```

In particular, the fixed `(4,2)` full-extension exclusion remains exact
for its displayed `e=0` based-frame orbit.  This classification exposes two
additional discrete `(4,2)` transport obligations rather than silently
promoting that fixed theorem to the entire unbased orbit.

## Replay

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_based_frame_orbit_classification.py
python claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_based_frame_orbit_classification.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_based_frame_orbit_classification.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_based_frame_orbit_classification.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_based_frame_orbit_classification.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_based_frame_orbit_classification.py
```

The primary verifier derives all three multiplication-dual equation spaces
with exact SymPy linear algebra, solves every projective pivot chart,
enumerates all spanning triples and stabilizer orbits, and checks all eight
integral frames.  The independent audit imports neither the primary
verifier nor SymPy.  It uses a standalone rational row reducer, reconstructs
the product tables and orbit actions, and separately enumerates the
rank-one loci over two finite fields.  Those finite fields audit the
catalog conventions only; the characteristic-zero completeness proof is
the pivot-chart argument (11).
