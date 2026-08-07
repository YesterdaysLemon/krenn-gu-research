# A thirteenth pure `P_4` component: the single-word quadrilateral fivefold

## Status

This is an exact algebraic-geometric component theorem over `C`.

The locus of four rank-two maps whose restriction of the order-four
permanent is a nonzero pure tensor has a thirteenth certified
irreducible component orbit: a five-dimensional rational family, the
**single-word quadrilateral fivefold** (branch `Za2` of the
coincident-support chart in the discovery snapshot).  Its
restriction is the **single permanent word**

```text
T = -4bek * e_0110
```

for all parameter values, and its four generic rank-one exceptional
relations all carry the same fixed conjugacy `u3.ybar=0` on the
four-cycle of edges `{01},{02},{13},{23}` — a relation
quadrilateral, the pattern complementary to the ninth component's
all-rank-one triangle.  Together with the companion split-pair
fivefold
([`P4_SPLIT_PAIR_PURE_COMPONENT.md`](claims/p4/components/split-pair/P4_SPLIT_PAIR_PURE_COMPONENT.md),
found in the same sweep), the certified census lower bound is
thirteen component orbits: ten fivefolds and three sixfolds.

As for its companion, two features are new.  The generic pair-rank
profile is `(3,3,4,3,3,3)` with **sum 19**, and the bound
`sum <= 19` holds on the entire closure because all `4 x 4` minors
of the five rank-three pair matrices vanish identically on the
family: the component lives strictly inside the degenerate profile
range invisible to the earlier profile-based sweeps, and the
closure-wide bound separates it from every certified rank-sum-`21`
fivefold.  And the certificate point is a **singular point of the
universal Segre incidence** (tangent dimension six, transverse
direction second-order obstructed), so componenthood is certified
by the exact characteristic-zero **local slice standard basis**
pattern of the eleventh component: five fixed rational hyperplanes
cut the ratio-eliminated purity variety to local dimension zero,
and the Krull height bound pins the local dimension to exactly
five.

The component was located in the case-Z rank-two branch sweep of
[`research_snapshots/2026-08-04-p4-exhaustiveness-sweep-census-thirteen/`](research_snapshots/2026-08-04-p4-exhaustiveness-sweep-census-thirteen/README.md)
(scripts `s03`, `s04`, `s08`, `s07`).  The calibrated `24 x 24`
semicontinuity sieve against the eleven previously certified
components leaves only the tenth (coincident-support sixfold) as a
candidate container, and the tenth's closed triple-span invariant
(`dim(U_I+U_J+U_L)<=3` for some mode triple, identically on its
closure) refutes it: every mode triple of this family's sample
spans `C^4`.  This document is the standalone theorem: the forced-
kernel rational normal form with the single-tie purity mechanism,
the slice certificate stated precisely, the separating invariants —
including the closed split-plane invariant that separates it from
its companion — and the **corrected** mirror identification: the
mirror branch `Za3` is the image of this family under the
`(01)`-source swap at the same parameters (an earlier draft's claim
that `diag(1,1,1,-1)` realizes the mirror was wrong — that
reflection is a self-symmetry of each branch).

This is not a classification.  The generic `H31` and weighted `H22`
obstruction theorems proved for components one through ten are
**open** for this component.  Its boundary walls, the remaining
open strata of the coincident-support chart, component
exhaustiveness, and the global prize problem all remain open.

## The family

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).      (1)
```

Write `Pi=span(X_2,X_3)`, `P01=span(X_0,X_1)`,

```text
ybar=(1,-1,0,0),          u3=(1,1,0,0),
B(u,w)=u_2w_3+u_3w_2,     B01(u,w)=u_0w_1+u_1w_0,    (2)
```

with `B01(u3,ybar)=0`.  Let `b,e,k,W,w_2,w_3` be parameters and
take the coincident-support rows with proportional `Pi`-heads
(the `Z-a` gauge):

```text
p=(0,1,b,-bk),    q=(0,1,e,-ek),    w=(0,W,w_2,w_3),
U_1=span(ybar,p),   U_2=span(ybar,q),   U_3=span(u3,w). (3)
```

Modulo `P01` the moving heads of `U_1,U_2` are `b`- and
`e`-multiples of the single line `(0,0,1,-k)`.  Contracting the
permanent with the three covector triples
`(ybar,ybar,w),(ybar,q,w),(p,ybar,w)` in modes `1,2,3` gives the
`3 x 4` matrix `M_Z` of the coincident-support case Z; on the gauge
(3) it has rank at most two **identically**, with kernel plane

```text
ker M_Z = span(u3, zeta_W),
zeta_W=(-W(kw_2+w_3), 0, -w_2(kw_2-w_3), w_3(kw_2-w_3)), (4)
```

and a pure nonzero restriction forces `U_0=ker M_Z`.  Note the
`Pi`-part of `zeta_W` lies on `(0,0,-w_2,w_3)`, the `B`-conjugate
of the `Pi`-head `(0,0,w_2,w_3)` of `w`: the mode-`0` and mode-`3`
`Pi`-shadows are conjugate lines, the shadow analogue of the
split-pair geometry of the companion component.

**Identical purity.**  With `U_0=span(u3,zeta_W)` and `W` still
free, direct permanent expansion gives exactly four nonzero words —
the mode-`{1,2}` double-moving slice — and they share the single
branch tie `g=2Wbek+(b+e)(kw_2-w_3)` as follows:

```text
T_0110=-4bek,               T_0111=-g,
T_1110=(kw_2+w_3)*g,        T_1111=W(kw_2+w_3)*g,    (5)
```

all twelve other coefficients vanishing **identically** in
`(b,e,k,W,w_2,w_3)`.  Purity of (5) is the vanishing of the single
surviving flattening minor, the `2 x 2` determinant of the slice,
which factors as

```text
(kw_2+w_3) * g * ((b+e)(kw_2-w_3)-2Wbek) = 0:        (6)
```

three branches.  The branch `kw_2+w_3=0` (`Za1`) is a wall of the
tenth component (snapshot `s05`); the branch `g=0` is this family;
the third branch (`Za3`) is its mirror (below).  On `g=0` all three
non-anchor words of (5) die **at once**, leaving the single word

```text
T_0110=-4bek=2B(p,q),                                (7)
```

nonzero on the whole chart (`b,e,k` are chart units).  Solving
`g=0`,

```text
W=-(b+e)(kw_2-w_3)/(2bek),                           (8)
```

and rescaling `zeta_W` by `2bek/(kw_2-w_3)` gives the family `F13`:

```text
U_0=span(u3, zeta),
zeta=((b+e)(kw_2+w_3), 0, -2bekw_2, 2bekw_3),
U_1,U_2 as in (3),   U_3=span(u3,(0,W,w_2,w_3)),     (9)
```

five parameters `(b,e,k,w_2,w_3)` with `(w_2:w_3)` projective.  The
single-word restriction is pure for **every** parameter value, with
mode kernels the four "unused" rows

```text
K_0=zeta,   K_1=K_2=ybar,   K_3=(0,W,w_2,w_3).       (10)
```

The projective diagonal source torus `diag(t_0,t_1,t_2,1)`
multiplies the coefficient by `t_0t_1t_2`; its subtorus `t_0=t_1`
preserves the normal form by reparametrization, and the transverse
direction `t_0 != t_1` supplies a fifth tangent direction beyond
the four effective chart parameters.  The closure `closure(F13)`
of the image of the parametrization (defined on `bek(kw_2-w_3)!=0`)
times `(C^*)^3` is irreducible and torus-stable.

## Exact component certificate

Use the Grassmann charts with pivots

```text
(02),(01),(01),(02)                                  (11)
```

and the generic rational sample

```text
(b,e,k,w_2,w_3)=(2,3,5,1,7),
W=1/6,     zeta=(60,0,-60,420),                      (12)
```

whose sixteen chart coordinates are

```text
(1,0,1,-7, 2,-10,2,-10, 3,-15,3,-15, 1,0,1/6,7)      (13)
```

and whose restriction is the single word `T_0110=-120`.

**Family tangent.**  Differentiating the chart coordinates in the
eight parameter directions (five chart parameters plus the full
projective torus) gives a `16 x 8` matrix of rank exactly **five**
at (12); the five chart parameters alone give rank four (the
`(w_2:w_3)`-scaling redundancy).  Rows

```text
(0,2,3,4,5) x columns (b,e,k,w_2,t_0)                (14)
```

have determinant `28/15`.  Hence `dim closure(F13)>=5`.

**A singular incidence point.**  Adjoin the projective Segre point
of the pure coefficient tensor in the charts (11): tensor anchor
`0000` (chart bases), anchor value `-120`, adjacent ratios

```text
(1,1,1,0).                                           (15)
```

The fifteen universal Segre-incidence equations in the twenty
plane/target variables have Jacobian rank **fourteen** at the
sample — tangent dimension six, not five.  Deleting the `0110`-row,
the remaining fourteen rows on columns

```text
(Z_0..Z_10,Z_13,R_1,R_3)                             (16)
```

have determinant `189665280000=2^15*3^3*5^4*7^3`.  The tangent
direction transverse to the rank-five family tangent is
**second-order obstructed**: along it every incidence equation
vanishes to first order, while the vector `c_2` of second-order
coefficients satisfies

```text
rank [J | c_2] = 15.                                 (17)
```

The sample is a singular point of the pure incidence locus of its
expected dimension, so the smooth-point certificates that proved
components one through ten cannot apply at it; componenthood is
certified by the slice instead.

**The slice certificate.**  Work in the sixteen chart variables
`Z_0..Z_15` and eliminate the target ratios: for each of the eleven
words `w` differing from the anchor `a=0000` in `k>=2` bits, the
multi-flip polynomial

```text
G_w = T_w*T_a^(k-1)
      - prod_{m: w_m!=a_m} T_(a flipped at m)        (18)
```

vanishes on every decomposable chart tensor (for
`T=u_0 ox u_1 ox u_2 ox u_3` both sides are the same monomial in
the factor entries — no anchor-nonvanishing hypothesis is needed).
Let `V` be the variety of the eleven `G_w` near (13); then `V`
contains the pure locus in the chart, and all eleven `G_w` vanish
at (13).  Shift (13) to the origin, clear denominators, and
intersect with the five fixed integer linear forms

```text
( 1, 2,-1, 3, 1,-2, 1, 1,-3, 2, 1,-1, 2, 1,-2, 3)
( 2,-1, 1, 1,-2, 3, 1,-1, 1, 1,-2, 1, 3,-1, 1,-2)
( 1, 1, 2,-3, 1, 1,-1, 2, 1,-2, 3, 1,-1, 1, 1, 2)
( 3,-2, 1, 1, 1,-1, 2, 1,-2, 1, 1, 3, 1,-1, 2, 1)
( 1, 3,-2, 1, 2, 1, 1,-1, 1, 2,-1, 1, 1, 2,-3, 1)   (19)
```

in `Z_0..Z_15`.  A Singular `ds` (local) standard basis of the
sixteen polynomials over `Q` — exact, characteristic zero — has

```text
local dimension 0 at the origin.                     (20)
```

By the Krull height bound each hyperplane through the point cuts
the local dimension by at most one, so (20) is valid as an upper
bound for **any** five forms — no genericity or transversality is
invoked:

```text
dim_0(V) <= 0+5 = 5.                                 (21)
```

The pure locus therefore has local dimension at most five at (12);
the family tangent (14) gives at least five; so the local dimension
is **exactly five**, and the irreducible five-dimensional
`closure(F13)` — contained in the pure locus, passing through
(12) — is contained in an irreducible component of dimension at
most five, hence equals it.  `closure(F13)` **is** an irreducible
component of the pure locus, and since its restriction is nowhere
zero on the chart, of the closure of the nonzero-pure locus.  A
nonzero pure tensor has a unique Segre point, so the statement
descends from the incidence picture to the plane locus.

## Distinctness from the twelve other orbits

At (12), and hence generically, the lexicographic pair-image
profile is

```text
(r_01,r_02,r_03,r_12,r_13,r_23)=(3,3,4,3,3,3),       (22)
```

with rank sum `19`.  Moreover at the five rank-three edges
`{01},{02},{12},{13},{23}` **all** `4 x 4` minors of the `4 x 6`
pair-product matrices vanish identically in the family parameters,
so every point of `closure(F13)` has pair profile at most
`(3,3,4,3,3,3)` entrywise:

```text
rank sum <= 19 on all of closure(F13).               (23)
```

- **The three sixfolds** (seventh, tenth, eleventh): excluded by
  dimension.  `closure(F13)` is irreducible of dimension five by
  the certificate; an irreducible sixfold cannot equal it.  (For
  the tenth this repairs nothing — the sieve already excluded it by
  the triple-span invariant: `dim(U_1+U_2+U_3)<=3` holds
  identically on the tenth's closure while every mode triple at
  (12) spans `C^4`, and both facts are re-verified.)
- **The eight certified rank-sum-21 fivefolds** (first,
  diagonal-quadric, the three `1+3` branches, sixth, eighth,
  ninth): if `closure(F13)=g(closure(X))` for a census symmetry
  `g`, then `g` maps the documented certificate sample of `X` into
  `closure(F13)`.  Census symmetries permute the six pair ranks
  and preserve their sum, so the image point has pair-rank sum
  `21` — contradicting (23).  All eight sample rank sums are
  re-verified exactly.
- **The twelfth (split-pair) fivefold**: the dimensions, profile
  multisets `{3,3,3,3,3,4}`, and rank sums all agree, so profiles
  cannot separate.  Instead let `S` be the closed set of plane
  4-tuples in which some plane meets two **complementary**
  coordinate 2-planes (both intersections nonzero).  `S` is stable
  under every census symmetry.  Every split-pair point has
  `U_0 cap P01 = span(u3)` and `U_0 cap Pi = span((0,0,1,-k))` —
  verified identically on that family — so the twelfth's closure
  is contained in `S`; at (12) **no** plane of `F13` meets two
  complementary coordinate planes (each of the four planes meets
  `P01` alone).  Hence `closure(F13)!=g(closure(F12))` for every
  census symmetry `g`.

All three separators — dimension (with the triple-span refinement
for the tenth), pair-rank sums under census alignment, and
membership in the closed set `S` — are invariant under the allowed
equivalences, so the single-word quadrilateral fivefold is
inequivalent to all twelve other orbits: a **thirteenth component
orbit**.

## Generic geometry

At (12), and generically, the four rank-one exceptional relations
sit on the four-cycle of edges between the `u3`-pair `{0,3}` and
the `ybar`-pair `{1,2}`, and every one of them is the same fixed
conjugacy:

```text
{01},{02}:  u3.ybar=0     (supports {0,1},{0,1}),
{13},{23}:  ybar.u3=0     (supports {0,1},{0,1}).    (24)
```

Against the kernels (10): the `ybar` factors are the mode-`1,2`
kernels and neither `u3` factor is a kernel (`K_0=zeta`,
`K_3=(0,W,w_2,w_3)`), so drawing arrows into kernel endpoints
orients the quadrilateral as

```text
0 -> 1,  0 -> 2,  3 -> 1,  3 -> 2,                   (25)
```

with pure-kernel indegrees `(0,2,2,0)`: modes `0,3` are sources,
modes `1,2` sinks, and no kernel-kernel relation occurs.  The
`{12}` edge is rank three with an **irreducible** exceptional
relation (coefficient matrix of rank two, so no rank-one relation
there — verified at (12), hence generic), and the `{03}` edge — the
`u3`-pencil pair — is the unique rank-four edge.  Compare the
companion split-pair component, where the same quadrilateral
carries the same four conjugacies but the diagonal `{03}` carries a
fifth, `B`-conjugate relation and `{12}` is the rank-four edge.

**Self-symmetries and the corrected mirror.**  The family is
invariant under the mode-`(12)` swap composed with `b <-> e`, and
under the source reflection `diag(1,1,1,-1)` composed with
`(k,w_3) -> (-k,-w_3)` — both exact identities of plane tuples.
The reflection **preserves** the branch invariant
`Q=2Wbek/[(b+e)(kw_2-w_3)]` (`Q=-1` on this family, `Q=+1` on the
mirror branch `Za3`), which is why the first-draft claim that
`diag(1,1,1,-1)` realizes the mirror was wrong.  The correct
identification: the `(01)`-**source** swap `X_0 <-> X_1` fixes the
lines `ybar,u3` and the planes `U_1,U_2`, sends the `U_3`-row
`(0,W,w_2,w_3)` to `(0,-W,w_2,w_3)` modulo `u3` (flipping `Q` to
`-Q`), and carries `F13(b,e,k,w_2,w_3)` onto the `Za3` branch at
the **same** parameters: modes `1,2,3` match by exact span
equalities, and the image mode-`0` plane is the `Za3`
configuration's forced kernel plane (its `M_Z` kills both `u3` and
the image of `zeta`, and has rank two at the sample).  The two
branches form **one** census orbit, absorbed by this component
orbit.

**Boundary walls (open).**  `b+e=0` sends `W` to `0` and `zeta`
into `Pi`; `kw_2-w_3=0` sends `W` to `0` with `zeta ~ u3`-collinear
`P01`-part; `kw_2+w_3=0` is the junction with the `Za1` wall of
the tenth; `b=e` degenerates the `{12}` edge further.  None of
these walls is classified.

## Verification

Run:

```text
python verify_p4_single_word_quadrilateral_pure_component.py

python audit_p4_single_word_quadrilateral_pure_component.py
```

The primary verifier proves the forced-kernel facts (4) (rank of
`M_Z`, kernel membership of `u3` and `zeta_W`, the `B`-conjugate
shadows), the free-`W` four-word structure (5) with the shared-tie
factorizations, and the identical single-word purity (7)--(9)
symbolically (all flattening minors vanish; torus scaling
`t_0t_1t_2`; kernels (10)), replays the rank-five family tangent
(14) and the rank-fourteen incidence Jacobian (15)--(16) with the
second-order obstruction (17), reruns the characteristic-zero slice
certificate (18)--(20) in Singular (`ds` standard basis,
fail-closed subprocess), replays the distinctness certificates (the
identical vanishing of all rank-three-edge `4 x 4` minors behind
(23), the eight fivefold sample rank sums, the tenth's triple-span
invariant on its symbolic family, the split-plane invariant with
the twelfth's family verified identically), verifies the generic
relation geometry (24)--(25), both self-symmetries, and the
corrected `Za3` mirror identification, and checks this document's
headline claims against its text.

The independent audit imports nothing from the primary verifier.
It recomputes all sixteen coefficients with a subset-dynamic-
programming permanent, replays purity, profile, and the
no-split-plane facts modulo the two primes `10007` and `10009`
(randomized parameter trials), replays the family tangent and
incidence Jacobian ranks and minors modulo both primes by
dual-number differentiation, reruns the **slice** modulo both
primes in Singular (`ds`, local dimension zero — a consistency
check; the characteristic-zero run in the verifier is the
certificate, with the shift performed by a ring map inside Singular
as an independent construction path), and re-grounds the eight
fivefold rank sums, the tenth's triple-span facts, and the
twelfth-family split facts in exact rational arithmetic.

## Honest frontier

1. The generic marked `H31` fibre and the generic weighted `H22`
   incidence of this component are **open** — as they are for the
   eleventh and twelfth components.  The single-word structure (7)
   matches the ninth component's, whose `H31` obstruction ran
   through the ubiquitous single-word reconstruction kernel; the
   companion exploration
   `explore_p5_h31_single_word_quadrilateral.py` transports that
   mechanism (frames `q=0,1` identity-dead, all four projected
   marking ideals the unit ideal, an interior survivor divisor
   `b(kw_2+w_3)+e(kw_2-w_3)=0` located) but is exploration data, not
   a theorem: the survivor-divisor closure and the standalone
   `H31`/`H22` documents remain to be written.
2. The component's boundary classification is open: the walls
   `b+e=0`, `kw_2-w_3=0`, the `Za1` junction `kw_2+w_3=0`, and the
   `b=e` degeneration.
3. The remaining open strata of the coincident-support chart (the
   `Zc` wall's ambient component, the case-Y survivor walls, the
   `p`-in-`Pi` walls) are exactly the open items of the discovery
   snapshot and could still hide further components.
4. Component exhaustiveness is open — thirteen is a certified lower
   bound, not a census — and both new components sit at singular
   incidence points, confirming that smooth-point sweeps alone
   cannot close the census.
5. The global prize conjecture remains unresolved.
