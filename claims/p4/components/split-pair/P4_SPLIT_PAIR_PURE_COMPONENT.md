# A twelfth pure `P_4` component: the split-pair fivefold

## Status

This is an exact algebraic-geometric component theorem over `C`.

The locus of four rank-two maps whose restriction of the order-four
permanent is a nonzero pure tensor has a twelfth certified
irreducible component orbit: a five-dimensional rational family, the
**split-pair fivefold** (branch `Zb1` of the coincident-support
chart in the discovery snapshot), whose mode-`0` and mode-`3` planes
are both **split** across the coordinate splitting
`C^4=span(X_0,X_1)+span(X_2,X_3)` — each is the direct sum of a line
of `span(X_0,X_1)` and a line of `Pi=span(X_2,X_3)` — with the same
`span(X_0,X_1)`-line and `B`-conjugate `Pi`-lines.  Together with
the companion single-word quadrilateral fivefold
([`P4_SINGLE_WORD_QUADRILATERAL_PURE_COMPONENT.md`](../../../../P4_SINGLE_WORD_QUADRILATERAL_PURE_COMPONENT.md),
found in the same sweep), the certified census lower bound is
thirteen component orbits: ten fivefolds and three sixfolds.

Two features are new.  First, this component and its companion are
the first whose generic pair-rank profile has **sum below twenty**:
the profile is `(3,3,3,4,3,3)` with sum `19`, and the bound
`sum <= 19` holds on the **entire closure** because all `4 x 4`
minors of the five rank-three pair matrices vanish identically on
the family.  The component therefore lives strictly inside the
degenerate profile range that the earlier profile-based sweeps could
not see, and the closure-wide bound is itself the separating
invariant against every certified rank-sum-`21` fivefold.  Second,
like the eleventh component — and unlike components one through ten
— the certificate point is a **singular point of the universal
Segre incidence** (tangent dimension six, one more than the
component dimension, with the transverse direction second-order
obstructed), so the smooth-point machinery does not apply and
componenthood is certified by the exact characteristic-zero
**local slice standard basis** pattern: five fixed rational
hyperplanes cut the ratio-eliminated purity variety to local
dimension zero at the sample, so the Krull height bound pins the
local dimension to exactly five.

The component was located in the case-Z rank-two branch sweep of
[`research_snapshots/2026-08-04-p4-exhaustiveness-sweep-census-thirteen/`](../../../../research_snapshots/2026-08-04-p4-exhaustiveness-sweep-census-thirteen/README.md)
(scripts `s03`, `s04`, `s06`, `s07`).  The calibrated `24 x 24`
semicontinuity sieve against the eleven previously certified
components leaves only the diagonal-quadric fivefold as a candidate
container, and the closure-wide rank-sum bound refutes it.  This
document is the standalone theorem: the free rational normal form
with the three-conjugacy purity mechanism, the slice certificate
stated precisely, and the separating invariants — including the
closed split-plane invariant that separates this component from its
companion, whose profile multiset and rank sum it shares.

This is not a classification.  The generic `H31` and weighted `H22`
obstruction theorems proved for components one through ten are
**open** for this component.  Its boundary walls, the remaining open
strata of the coincident-support chart, component exhaustiveness,
and the global prize problem all remain open.

## The family

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).      (1)
```

Write `Pi=span(X_2,X_3)`, `P01=span(X_0,X_1)`, and

```text
ybar=(1,-1,0,0),          u3=(1,1,0,0),
w_c=(0,0,1,c),
B(u,w)=u_2w_3+u_3w_2,     B01(u,w)=u_0w_1+u_1w_0:    (2)
```

`B` is the nondegenerate binary form on `Pi` whose conjugacy is the
zero-product condition for two `Pi`-vectors, and `B01` is its twin
on `P01`.  The two fixed lines are `B01`-conjugate,
`B01(u3,ybar)=0`, and the two marked `Pi`-lines below are
`B`-conjugate, `B(w_{-k},w_k)=0`.

Let `p2,p3,q2,q3,k` be parameters, write `p=(0,1,p_2,p_3)`,
`q=(0,1,q_2,q_3)`, and take the row planes

```text
U_0=span(u3, w_{-k}),     U_1=span(ybar, p),
U_2=span(ybar, q),        U_3=span(u3, w_k),
with the single tie
k(p_2+q_2)+(p_3+q_3)=0.                              (3)
```

The end planes `U_0,U_3` are **split**: each is the direct sum of
the `P01`-line `u3` and a `Pi`-line, the two `Pi`-lines forming the
`B`-conjugate pair `w_{-k},w_k`; in particular
`U_0 cap U_3=span(u3)`.  The middle planes `U_1,U_2` share the
`B01`-conjugate line `ybar` and carry the moving `Pi`-heads
`(p_2,p_3),(q_2,q_3)`.  The tie says exactly that the **sum** of the
two moving `Pi`-heads is `B`-apolar to `U_3`'s `Pi`-line:
`B(w_k,p+q)=0`.

**Identical purity.**  Before imposing the tie, direct permanent
expansion in the bases (3) gives the three-word restriction

```text
T_0110=2(p_2q_3+p_3q_2)          =2B(p,q),
T_1110=(p_3+q_3)-k(p_2+q_2)      =B(w_{-k},p+q),
T_0111=(p_3+q_3)+k(p_2+q_2)      =B(w_k,p+q),        (4)
```

and the thirteen other coefficients vanish **identically** in
`(p_2,p_3,q_2,q_3,k)`.  Three elementary mechanisms cover them: a
word choosing three or more of the `P01`-rows `u3,ybar` dies by
column counting on the two-column space `P01`; a word choosing one
`u3`-row and one `ybar`-row (and at most one moving row) factors
through `B01(u3,ybar)=0`; and the double-`w` slice factors through
`B(w_{-k},w_k)=0` (the word `1111` already dies because no chosen
row meets column `0`).  Purity of (4) is the single binomial

```text
T_1110*T_0111=0                                      (5)
```

(the one flattening minor that does not vanish identically), whose
two branches are exchanged by the census symmetry
`(03)-mode swap composed with k -> -k`.  The split-pair family is
the branch `T_0111=0` — the tie in (3) — on which the restriction is
the two-word tensor

```text
T_0110=2B(p,q),   T_1110=-2k(p_2+q_2),               (6)
```

supported on two words differing in one bit: decomposable for
**every** parameter value, nonzero exactly when the two coefficients
(6) do not both vanish, with mode kernels

```text
K_0 ~ k(p_2+q_2)*u3+B(p,q)*w_{-k},   K_1=K_2=ybar,
K_3=w_k.                                             (7)
```

The projective diagonal source torus `diag(t_0,t_1,t_2,1)`
multiplies every coefficient by `t_0t_1t_2`.  Its subtorus
`t_0=t_1=t` preserves the normal form exactly, acting by the
reparametrization

```text
(p_2,p_3,q_2,q_3,k) ->
((t_2/t)p_2, p_3/t, (t_2/t)q_2, q_3/t, k/t_2),       (8)
```

which preserves the tie; the transverse direction `t_0 != t_1`
supplies a fifth tangent direction beyond the four chart parameters
`(p_2,p_3,q_2,k)`.  The closure `closure(F12)` of the image of
`A^4 x (C^*)^3` under the (rational, totally defined)
parametrization is irreducible and torus-stable.

## Exact component certificate

Use the Grassmann charts with pivots

```text
(02),(01),(01),(02)                                  (9)
```

and the generic rational sample

```text
(p_2,p_3,q_2,k)=(3,-1,5,2),      q_3=-15,            (10)
```

whose sixteen chart coordinates are the integers

```text
(1,0,0,-2, 3,-1,3,-1, 5,-15,5,-15, 1,0,0,2)          (11)
```

and whose restriction has `T_0110=-100`, `T_1110=-32`.

**Family tangent.**  Differentiating the chart coordinates in the
seven parameter directions (four chart parameters plus the full
projective torus) gives a `16 x 7` matrix of rank exactly **five**
at (10); the four chart parameters alone give rank four.  Rows

```text
(0,3,4,5,8) x columns (p_2,p_3,q_2,k,t_0)            (12)
```

have determinant `-1`.  Hence `dim closure(F12)>=5`.

**A singular incidence point.**  Adjoin the projective Segre point
of the pure coefficient tensor in the charts (9): tensor anchor
`0000` (chart bases), anchor value `-100`, adjacent ratios

```text
(8/25,1,1,0).                                        (13)
```

The fifteen universal Segre-incidence equations in the twenty
plane/target variables have Jacobian rank **fourteen** at the
sample — tangent dimension six, not five.  Deleting the `0110`-row,
the remaining fourteen rows on columns

```text
(Z_0..Z_9,Z_12,Z_13,Z_14,R_3)                        (14)
```

have determinant `28311552000=2^23*3^3*5^3`.  The tangent direction
transverse to the rank-five family tangent is **second-order
obstructed**: along it every incidence equation vanishes to first
order, while the vector `c_2` of second-order coefficients satisfies

```text
rank [J | c_2] = 15.                                 (15)
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
      - prod_{m: w_m!=a_m} T_(a flipped at m)        (16)
```

vanishes on every decomposable chart tensor (for
`T=u_0 ox u_1 ox u_2 ox u_3` both sides are the same monomial in
the factor entries — no anchor-nonvanishing hypothesis is needed).
Let `V` be the variety of the eleven `G_w` near (11); then `V`
contains the pure locus in the chart, and all eleven `G_w` vanish
at (11).  Shift (11) to the origin, clear denominators, and
intersect with the five fixed integer linear forms

```text
( 1, 2,-1, 3, 1,-2, 1, 1,-3, 2, 1,-1, 2, 1,-2, 3)
( 2,-1, 1, 1,-2, 3, 1,-1, 1, 1,-2, 1, 3,-1, 1,-2)
( 1, 1, 2,-3, 1, 1,-1, 2, 1,-2, 3, 1,-1, 1, 1, 2)
( 3,-2, 1, 1, 1,-1, 2, 1,-2, 1, 1, 3, 1,-1, 2, 1)
( 1, 3,-2, 1, 2, 1, 1,-1, 1, 2,-1, 1, 1, 2,-3, 1)   (17)
```

in `Z_0..Z_15`.  A Singular `ds` (local) standard basis of the
sixteen polynomials over `Q` — exact, characteristic zero — has

```text
local dimension 0 at the origin.                     (18)
```

By the Krull height bound each hyperplane through the point cuts the
local dimension by at most one, so (18) is valid as an upper bound
for **any** five forms — no genericity or transversality is
invoked:

```text
dim_0(V) <= 0+5 = 5.                                 (19)
```

The pure locus therefore has local dimension at most five at (10);
the family tangent (12) gives at least five; so the local dimension
is **exactly five**, and the irreducible five-dimensional
`closure(F12)` — contained in the pure locus, passing through
(10) — is contained in an irreducible component of dimension at
most five, hence equals it.  `closure(F12)` **is** an irreducible
component of the pure locus, and since its generic restriction is
nonzero, of the closure of the nonzero-pure locus.  A nonzero pure
tensor has a unique Segre point, so the statement descends from the
incidence picture to the plane locus.

## Distinctness from the twelve other orbits

At (10), and hence generically, the lexicographic pair-image
profile is

```text
(r_01,r_02,r_03,r_12,r_13,r_23)=(3,3,3,4,3,3),       (20)
```

with rank sum `19`.  Moreover at the five rank-three edges
`{01},{02},{03},{13},{23}` **all** `4 x 4` minors of the `4 x 6`
pair-product matrices vanish identically in the family parameters,
so every point of `closure(F12)` has pair profile at most
`(3,3,3,4,3,3)` entrywise:

```text
rank sum <= 19 on all of closure(F12).               (21)
```

- **The three sixfolds** (seventh, tenth, eleventh): excluded by
  dimension.  `closure(F12)` is irreducible of dimension five by
  the certificate; an irreducible sixfold cannot equal it.
- **The eight certified rank-sum-21 fivefolds** (first,
  diagonal-quadric, the three `1+3` branches, sixth, eighth,
  ninth): if `closure(F12)=g(closure(X))` for a census symmetry
  `g`, then `g` maps the documented certificate sample of `X` into
  `closure(F12)`.  Census symmetries (mode permutations,
  source-coordinate permutations, the diagonal torus, in-plane
  basis changes) permute the six pair ranks and preserve their
  sum, so the image point has pair-rank sum `21` — contradicting
  (21).  All eight sample rank sums are re-verified exactly.
- **The thirteenth (single-word quadrilateral) fivefold**: the
  dimensions, profile multisets `{3,3,3,3,3,4}`, and rank sums
  all agree, so profiles cannot separate.  Instead let `S` be the
  closed set of plane 4-tuples in which some plane meets two
  **complementary** coordinate 2-planes (both intersections
  nonzero).  `S` is stable under every census symmetry.  Every
  `F12` point has `U_0 cap P01=span(u3)` and
  `U_0 cap Pi=span(w_{-k})`, so `closure(F12)` is contained in
  `S`; at the thirteenth's certificate sample — re-grounded here
  as a nonzero pure tuple — **no** plane meets two complementary
  coordinate planes, so the thirteenth's closure is not contained
  in `S`.  Hence `closure(F12)!=g(closure(F13))` for every census
  symmetry `g`.

All three separators — dimension, pair-rank sums under census
alignment, and membership in the closed set `S` — are invariant
under the allowed equivalences, so the split-pair fivefold is
inequivalent to all twelve other orbits: a **twelfth component
orbit**.

## Generic geometry

At (10), and generically, the five rank-three edges each carry a
rank-one exceptional relation:

```text
{01},{02}:  u3.ybar=0     (supports {0,1},{0,1}),
{13},{23}:  ybar.u3=0     (supports {0,1},{0,1}),
{03}:       w_{-k}.w_k=0  (supports {2,3},{2,3}):   (22)
```

the four cross edges between the `u3`-pair `{0,3}` and the
`ybar`-pair `{1,2}` all carry the fixed `B01`-conjugacy, and the
diagonal `{03}` carries the `B`-conjugacy of the two split
`Pi`-lines.  Against the kernels (7): drawing arrows into kernel
endpoints orients the relation graph as

```text
0 -> 1,  0 -> 2,  3 -> 1,  3 -> 2,  0 -> 3,          (23)
```

with pure-kernel indegrees `(0,2,2,1)` and no kernel-kernel
relation.  The remaining edge `{12}` — the `ybar`-pencil pair — is
the unique rank-four edge.

**Swap symmetries.**  The family is invariant under the mode-`(12)`
swap composed with `(p_2,p_3) <-> (q_2,q_3)`, and under the source
reflection `diag(1,1,1,-1)` composed with
`(p_3,q_3,k) -> (-p_3,-q_3,-k)` — both exact identities of plane
tuples.  The mirror branch `Zb2` (`T_1110=0` in (5)) is the image
of `F12` under the `(03)`-mode swap composed with `k -> -k`: the
two branches form **one** census orbit, and this component orbit
absorbs both.

**Boundary walls (open).**  `B(p,q)=0` kills `T_0110` and
`p_2+q_2=0` kills `T_1110` (single-word boundaries); `k=0`
collapses the conjugate pair (`U_0=U_3`); `p,q` with proportional
`Pi`-heads meet the `Za`-branch locus of the same chart.  None of
these walls is classified.

## Verification

Run:

```text
python claims/p4/components/split-pair/verify_p4_split_pair_pure_component.py

python claims/p4/components/split-pair/audit_p4_split_pair_pure_component.py
```

The primary verifier proves the identical three-word structure (4)
and the two-word tie restriction (6) symbolically (all flattening
minors of the symbolic family vanish; the three purity mechanisms;
torus scaling `t_0t_1t_2`; the subtorus reparametrization (8);
kernels (7)), replays the rank-five family tangent (12) and the
rank-fourteen incidence Jacobian (13)--(14) with the second-order
obstruction (15), reruns the characteristic-zero slice certificate
(16)--(18) in Singular (`ds` standard basis, fail-closed
subprocess), replays the distinctness certificates (the identical
vanishing of all rank-three-edge `4 x 4` minors behind (21), the
eight fivefold sample rank sums, the split-plane invariant with the
thirteenth's sample re-grounded), verifies the generic relation
geometry (22)--(23) and the swap and `Zb2` identifications, and
checks this document's headline claims against its text.

The independent audit imports nothing from the primary verifier.
It recomputes all sixteen coefficients with a subset-dynamic-
programming permanent, replays purity, profile, and the split-plane
facts modulo the two primes `10007` and `10009` (randomized
parameter trials), replays the family tangent and incidence
Jacobian ranks and minors modulo both primes by dual-number
differentiation, reruns the **slice** modulo both primes in
Singular (`ds`, local dimension zero — a consistency check; the
characteristic-zero run in the verifier is the certificate, with
the shift performed by a ring map inside Singular as an independent
construction path), and re-grounds the eight fivefold rank sums and
the thirteenth-sample split facts in exact rational arithmetic.

## Honest frontier

1. The generic marked `H31` fibre and the generic weighted `H22`
   incidence of this component are **open** — as they are for the
   eleventh and thirteenth components.  The companion exploration
   `explore_p5_h31_split_pair.py` transports the tenth's
   concentration mechanism (frames `q=0,1` identity-dead; the
   frame-`2,3` marking ideals cut out the single rational survivor
   marking `t=(-1/(p_2+q_2),1/2,1/2,0)`), but the survivor's
   ternary closure and the standalone theorem documents remain to
   be written.
2. The component's boundary classification is open: the single-word
   walls `B(p,q)=0` and `p_2+q_2=0`, the collapse `k=0`, and the
   junction with the `Za`-branch locus.
3. The remaining open strata of the coincident-support chart (the
   `Zc` wall's ambient component, the case-Y survivor walls, the
   `p`-in-`Pi` walls) are exactly the open items of the discovery
   snapshot and could still hide further components.
4. Component exhaustiveness is open — thirteen is a certified lower
   bound, not a census — and both new components sit at singular
   incidence points, confirming that smooth-point sweeps alone
   cannot close the census.
5. The global prize conjecture remains unresolved.
