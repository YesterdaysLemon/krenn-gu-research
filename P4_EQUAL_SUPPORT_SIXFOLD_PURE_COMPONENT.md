# An eleventh pure `P_4` component: the equal-support sixfold

## Status

This is an exact algebraic-geometric component theorem over `C`.

The locus of four rank-two maps whose restriction of the order-four
permanent is a nonzero pure tensor has an eleventh certified
irreducible component orbit: a six-dimensional rational family, the
**equal-support sixfold** (working name `C10` in the discovery
snapshot), whose three generic rank-one exceptional relations all
live in the **same** coordinate two-plane `span(X_2,X_3)`.  The
certified census lower bound is therefore eleven component orbits:
eight fivefolds and three sixfolds.

Two features are new.  First, the restriction is pure for **all**
parameter values — like the ninth component the family is free, with
no defining hypersurface — but here purity has a two-line apolarity
mechanism rather than a coefficient cancellation.  Second, and
unlike every previous component, this component admits **no smooth
incidence certificate anywhere**: the universal Segre-incidence
tangent has dimension at least seven at every point of the closure,
and exactly seven on a dense open subset — one more than the
component dimension.  This is the first component certified at a singular
incidence point.  The certificate is instead an exact
characteristic-zero **local slice standard basis**: six fixed
rational hyperplanes through a generic sample cut the
ratio-eliminated purity variety to local dimension zero, so by the
Krull height bound its local dimension is at most six, which the
rank-six family tangent then meets exactly.

The component was located in the equal-support in-out chart of
[`research_snapshots/2026-08-04-p4-equal-support-rank-two-strata/`](research_snapshots/2026-08-04-p4-equal-support-rank-two-strata/README.md)
(steps 22--29; the snapshot's Task A conclusion plus its integration
addendum).  This document is its standalone theorem: the free
rational normal form with the apolar purity mechanism, the slice
certificate stated precisely, and the separating invariants —
including the closed coordinate-plane invariant that refutes the
expected identification with the tenth (coincident-support)
component, whose generic pair-rank profile multiset it shares.

This is not a classification.  The generic `H31` and weighted `H22`
obstruction theorems proved for earlier components are **open** for
this one — here not even exploratory modular data exists.  The
component's boundaries, the deep strata of its chart, component
exhaustiveness, and the global prize problem remain open.

## The family

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).      (1)
```

Write `Pi=span(X_2,X_3)` for the fixed coordinate plane and

```text
w_c=(0,0,1,-c),
B(u,w)=u_2 w_3+u_3 w_2,
B01(u,w)=u_0 w_1+u_1 w_0:                            (2)
```

`B` is the nondegenerate binary form on `Pi` whose conjugacy is the
zero-product condition for two `Pi`-vectors, with isotropic
directions `X_2,X_3`; `B01` is its twin on `span(X_0,X_1)`.

Let `c_0,c_1,c_2,t,v=(v_0,v_1,v_2,v_3),x_2,x_3` be ten free
parameters, put `x=(t v_0,t v_1,x_2,x_3)`, and take the row planes

```text
U_0=span((v_0,-v_1,0,0), w_{c_0}),
U_1=span(w_{c_1}, v),
U_2=span(w_{c_2}, x),
U_3=Pi=span(X_2,X_3).                                (3)
```

Each `U_i` meets `Pi` in a marked line (`w_{c_0}`, `w_{c_1}`,
`w_{c_2}`, all of `Pi`); the two moving rows `v,x` share the
`{0,1}`-head `(v_0,v_1)` up to the factor `t`; and the off-`Pi` row
of `U_0` is the `B01`-conjugate `(v_0,-v_1)` of that common head.

**Identical purity.**  In the bases (3) (mode-3 basis
`(0,0,1,1),(0,0,1,-1)`), direct permanent expansion gives

```text
T_1110=-2t v_0 v_1 (c_0-1),
T_1111=-2t v_0 v_1 (c_0+1),                          (4)
```

and all fourteen other coefficients vanish **identically** in the
ten parameters.  A tensor supported on two words differing in one
bit is decomposable, so the family restricts `P_4` to a pure tensor
for **every** parameter value, and to a nonzero one exactly when
`t v_0 v_1 != 0`.

The vanishing has a two-step apolar interpretation.  A permanent
word taking three or more rows inside the two-column plane `Pi`
(the mode-3 row, plus `w_{c_0}` if the `U_0`-bit is `1`, plus
`w_{c_1}`/`w_{c_2}` if the mode-1/2 bits are `0`) is killed by
support counting.  In every surviving word with `U_0`-bit `0` the
columns `{0,1}` must be covered by the row `(v_0,-v_1,0,0)`
together with one moving row, so the word factors through the binary
permanent

```text
B01((v_0,-v_1),(v_0,v_1))=v_0v_1-v_1v_0=0:           (5)
```

the `U_0`-row is `B01`-apolar to the common head of `v` and `x`, and
the whole `U_0`-bit-`0` slice dies.  The only words left are
`(1,1,1,*)`, where `v,x` must cover `{0,1}` and `w_{c_0},p_3` must
cover `{2,3}`, so the permanent factors exactly:

```text
T_(1,1,1,*)=perm2_{01}(v,x)*B(w_{c_0},p_3)
           =2t v_0 v_1*B(w_{c_0},p_3).               (6)
```

The restriction is the single linear functional `B(w_{c_0},.)` on
`U_3=Pi` planted on the word `(1,1,1,*)` — manifestly pure, with
mode kernels

```text
K_0=(v_0,-v_1,0,0),   K_1=w_{c_1},
K_2=w_{c_2},          K_3=(0,0,1,c_0)                (7)
```

(`K_3` is the `B`-conjugate of `U_0`'s `Pi`-line, and (4) is (6)
evaluated on the two mode-3 basis vectors).

The projective diagonal source torus `diag(t_0,t_1,t_2,1)`
multiplies every coefficient by the single monomial `t_0t_1t_2` and
maps the family into itself (each `w_c` rescales to `w_{c/t_2}`, the
`v`- and `x`-rows stay in shape with the same `t`): the family is
**torus-saturated**.  Its parameter count is six after gauges —
`c_0,c_1,c_2`, the class of `v` modulo `w_{c_1}` and scale (two),
and the class of `(t,x_2,x_3)` modulo `w_{c_2}` and scale (one).
The closure of the image of `A^10 x (C^*)^3` under the (rational,
totally defined where `t v_0 != 0`) parametrization is irreducible.

## Exact component certificate

Use the Grassmann charts with pivots

```text
(02),(02),(02),(23)                                  (8)
```

and the generic rational sample

```text
(c_0,c_1,c_2,t,v,x_2,x_3)
   =(3,-2,5,2,(3,-7,2,5),-1,4),                      (9)
```

whose sixteen chart coordinates are

```text
(7/3,0,0,-3, -7/3,1/3,0,2, -7/3,-1/6,0,-5, 0,0,0,0). (10)
```

**Family tangent.**  Differentiating the chart coordinates in the
thirteen parameter directions (ten family parameters plus the full
projective torus) gives a `16 x 13` matrix of rank exactly **six**
at (9).  Rows

```text
(0,3,5,7,9,11) x columns (c_0,c_1,c_2,t,v_0,v_1)     (11)
```

have determinant `1/324`.  Hence `dim closure(C10)>=6`, and the
torus directions add nothing beyond the family's own.

**Why no smooth certificate exists.**  Adjoin the projective Segre
point of the pure coefficient tensor in the charts (8): tensor
anchor `1000` (chart bases), anchor value `14`, adjacent ratios

```text
(0,0,0,-1/3).                                        (12)
```

The fifteen universal Segre-incidence equations in the twenty
plane/target variables have Jacobian rank **thirteen** at (9) —
tangent dimension seven, not six.  Rows `0..12` and columns

```text
(0,1,2,3,4,6,10,12,13,14,15,16,17)                   (13)
```

give determinant

```text
16866160640/6561 = 2^12*5*7^7/3^8.                   (14)
```

The excess direction is explicit: deforming `U_3` off `Pi` inside
the hyperplane `span((v_0,v_1,0,0),X_2,X_3)` by

```text
U_3(eps)=span(e_2+eps a_3(v_0,v_1,0,0),
              e_3+eps b_3(v_0,v_1,0,0))
```

with ratio `a_3:b_3=-c_0:1` makes every purity minor vanish to first
order in `eps` **identically in all parameters**, while at (9) eight
second-order coefficients such as

```text
-4c_0^2 t v_0^2 v_1^2 (c_0+c_1)(c_0+c_2)             (15)
```

are nonzero: the direction is tangent but second-order obstructed.
Since it exists at every family point with `(c_0+c_1)(c_0+c_2)!=0`,
the incidence tangent dimension is at least seven on a dense open
subset of the family, hence — tangent dimension can only jump up on
closed sets — at least seven **everywhere on** `closure(C10)`.  No
point of this component is a smooth point of the pure incidence
locus of its expected dimension: the smooth-point certificates that
proved components one through ten cannot exist here at any sample.

**The slice certificate.**  Work in the sixteen chart variables
`Z_0..Z_15` and eliminate the target ratios: for each of the eleven
words `w` differing from the anchor `a=1000` in `k>=2` bits, the
multi-flip polynomial

```text
G_w = T_w*T_a^(k-1)
      - prod_{m: w_m!=a_m} T_(a flipped at m)        (16)
```

vanishes on every decomposable chart tensor (for
`T=u_0 ox u_1 ox u_2 ox u_3` both sides are the same monomial in
the factor entries — no anchor-nonvanishing hypothesis is needed).
Let `V` be the variety of the eleven `G_w` near (10); then `V`
contains the pure locus in the chart.  All eleven `G_w` vanish at
(10).  Shift (10) to the origin, clear denominators, and intersect
with the six fixed integer linear forms

```text
( 1, 2,-1, 3, 1,-2, 1, 1,-3, 2, 1,-1, 2, 1,-2, 3)
( 2,-1, 1, 1,-2, 3, 1,-1, 1, 1,-2, 1, 3,-1, 1,-2)
( 1, 1, 2,-3, 1, 1,-1, 2, 1,-2, 3, 1,-1, 1, 1, 2)
( 3,-2, 1, 1, 1,-1, 2, 1,-2, 1, 1, 3, 1,-1, 2, 1)
( 1, 3,-2, 1, 2, 1, 1,-1, 1, 2,-1, 1, 1, 2,-3, 1)
( 2, 1, 1,-1, 3,-2, 1, 1, 2,-1, 1, 1,-2, 3, 1, 1)   (17)
```

in `Z_0..Z_15`.  A Singular `ds` (local) standard basis of the
seventeen polynomials over `Q` — exact, characteristic zero — has

```text
local dimension 0 at the origin.                     (18)
```

By the Krull height bound each hyperplane through the point cuts the
local dimension by at most one, so (18) is valid as an upper bound
for **any** six forms — no genericity or transversality is invoked:

```text
dim_0(V) <= 0+6 = 6.                                 (19)
```

The pure locus therefore has local dimension at most six at (9); the
family tangent (11) gives at least six; so the local dimension is
**exactly six**, and the irreducible six-dimensional
`closure(C10)` — contained in the pure locus, passing through (9) —
is contained in an irreducible component of dimension at most six,
hence equals it.  `closure(C10)` **is** an irreducible component of
the pure locus, and since its generic restriction is nonzero, of
the closure of the nonzero-pure locus.  A nonzero pure tensor has a
unique Segre point, so the statement descends from the incidence
picture to the plane locus.

(The full sixteen-variable local standard basis without slicing is
heavy — a char-31991 attempt hit its 480-second cap and is recorded
as null; the slice is the certificate precisely because cutting to
local dimension zero is cheap.)

## Distinctness from the ten earlier orbits

At (9), and hence generically, the lexicographic pair-image profile
is

```text
(r_01,r_02,r_03,r_12,r_13,r_23)=(4,4,3,4,3,3),       (20)
```

with rank sum `21`.  The three certified six-dimensional orbits are
separated as follows.

- **Seventh** (generic profile `(4,3,2,4,4,3)`, rank sum `20`): if
  `closure(C10)` lay in a mode-aligned image of the seventh's
  closure, every pair rank at the generic `C10` point would be
  bounded by the corresponding generic rank of the seventh;
  rank-sum monotonicity `21>20` excludes every alignment.
- **Tenth** (coincident-support component, certificate point
  `(b,e,k,m,r)=(2,3,5,7,11)`, generic profile `(3,3,4,3,4,4)`):
  the profile **multisets agree** (`{4,4,4,3,3,3}` both, rank sum
  `21` both), so profiles cannot separate.  Instead let `S` be the
  closed set of plane 4-tuples having at least one coordinate
  2-plane `span(e_a,e_b)` among their planes.  `S` is stable under
  every census symmetry (mode permutations, source-coordinate
  permutations, the diagonal source torus, in-plane basis changes).
  Every `C10` point has `U_3=span(e_2,e_3)`, so `closure(C10)` is
  contained in `S`; at the tenth's certificate point — re-grounded
  as the certified nonzero pure tuple — **none** of the four planes
  is a coordinate plane, so the tenth's closure is not contained in
  `S`.  If `closure(C10)=g(tenth)` for a census symmetry `g`, the
  tenth would lie in `g^{-1}(S)=S` at every point — contradiction.
  Hence `closure(C10)!=g(tenth)` for every `g`.
- **The eight fivefolds** (first, diagonal-quadric, the three `1+3`
  branches, sixth, eighth, ninth): separated by dimension, six
  against five.

All three separators — dimension, pair-rank sums under mode
alignment, and membership in the closed set `S` — are invariant
under the allowed equivalences, so the equal-support sixfold is
inequivalent to all ten earlier orbits: an **eleventh component
orbit**.

## Generic geometry

The name records the relation structure.  At (9), and generically,
the three rank-three edges are `{03},{13},{23}` — the star at mode
`3` — and each carries a rank-one exceptional relation whose two
factor supports **all equal** `{2,3}`: the relations are exactly the
`B`-conjugacies inside `Pi`

```text
{03}:  w_{c_0}.(0,0,1,c_0)=0,
{13}:  w_{c_1}.(0,0,1,c_1)=0,
{23}:  w_{c_2}.(0,0,1,c_2)=0.                        (21)
```

Against the kernels (7): on edge `{03}` the `U_3`-side factor
`(0,0,1,c_0)` is the kernel `K_3`, on `{13}`/`{23}` the `U_1`/`U_2`
factors are the kernels `K_1`/`K_2`.  Drawing arrows into kernel
endpoints orients the star as

```text
0 -> 3,   3 -> 1,   3 -> 2,                          (22)
```

with pure-kernel indegrees `(1,1,1,0)` and **no** kernel-kernel
relation generically.  (By contrast the ninth component's three
relations have pairwise distinct supports; here all three coincide
— the two extremes of the support geometry.)

**The `W`-wall.**  On the hyperplane `c_0=c_1` the relation vector
`(0,0,1,c_1)` of edge `{13}` collides with `K_3` and that relation
becomes kernel-kernel.  This five-dimensional wall is precisely the
`W`-branch of the equal-support rank-two stratum in which the
component was discovered (snapshot steps 1--7): the wall points are
the chart's own pure points, and freeing the `Pi`-directions of
`U_0,U_1,U_2` off the wall exposed the component.

**Swap symmetry.**  The family is invariant under the mode-`(12)`
swap composed with the reparametrization

```text
(v,x,t,c_1,c_2) -> (x,v,1/t,c_2,c_1),                (23)
```

an exact identity of plane tuples (Pluecker-proportionality in all
four modes, for all parameters with `t!=0`).  The swap exchanges the
walls `c_0=c_1` and `c_0=c_2`, so the kernel-kernel wall is unique
up to the family's own symmetry.

**Boundary walls (open).**  `c_0=1` and `c_0=-1` kill one of the
two coefficients (4) (single-word boundary); `t v_0 v_1=0` kills the
restriction; on `c_1=-c_0` and `c_2=-c_0` the second-order
obstruction (15) degenerates and the `U_3`-deformation integrates
into six-dimensional crossing sheets (snapshot steps 24--25).  None
of these is classified.

## Verification

Run:

```text
python verify_p4_equal_support_sixfold_pure_component.py

python audit_p4_equal_support_sixfold_pure_component.py
```

The primary verifier proves the identical-purity statement (4)--(6)
symbolically (all flattening minors of the symbolic family vanish;
torus scaling `t_0t_1t_2`; kernels (7)), replays the rank-six
family tangent (11) and the rank-thirteen incidence Jacobian
(12)--(14) with the first/second-order facts about the excess
direction (15), reruns the characteristic-zero slice certificate
(16)--(18) in Singular (`ds` standard basis, fail-closed subprocess),
replays the distinctness certificates (coordinate-plane invariant
with the tenth's certificate point re-grounded, profile and
rank-sum facts against the seventh's and tenth's generic samples),
verifies the `W`-wall kernel-kernel flip and the swap identity
(23), and checks this document's headline claims against its text.

The independent audit imports nothing from the primary verifier.
It recomputes all sixteen coefficients with a subset-dynamic-
programming permanent, replays purity, profile, and the
coordinate-plane facts modulo the two primes `10007` and `10009`
(randomized parameter trials), replays the family tangent and
incidence Jacobian ranks and minors modulo both primes by
dual-number differentiation, reruns the **slice** modulo both
primes in Singular (`ds`, local dimension zero — a consistency
check; the characteristic-zero run in the verifier is the
certificate), and re-grounds the tenth-point coordinate-plane
distinctness in exact integer arithmetic.

## Honest frontier

1. The generic marked `H31` fibre and the generic weighted `H22`
   incidence of this component are **open** — for the eleventh
   component there is not even exploratory modular data yet.
2. The deep strata of the equal-support chart remain to sweep:
   `s=0` with `(v_2+v_3)(v_1x_0-v_0x_1)=0`, support-degenerate `x`,
   and `v_0=v_1=0` (`U_1` inside `Pi`) — Grassmannian-moduli
   treatments, any of which could still hide further components.
3. The component's boundary classification is open: the single-word
   walls `c_0=+-1`, the zero-restriction locus `t v_0 v_1=0`, the
   kernel-kernel `W`-wall, and the crossing sheets at
   `c_1=-c_0`/`c_2=-c_0` where the obstructed normal direction
   integrates.
4. Component exhaustiveness is open — eleven is a certified lower
   bound, not a census — and the singular-incidence phenomenon
   found here warns that smooth-point sweeps alone cannot close the
   census.
5. The global prize conjecture remains unresolved.
