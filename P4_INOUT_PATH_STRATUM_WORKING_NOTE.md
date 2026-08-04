# The in-out path stratum of the pure `P_4` locus: working note

## Status

This is an exact exploratory checkpoint, not a complete component
theorem.  It opens the mixed-orientation stratum left unclassified by
[`P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md`](P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md):
two rank-one exceptional relations in directed **path** position.
The chart identities below are exact and replayed.  The `F_4` branch
is now settled: it is contained in the six-dimensional seventh
component, so it produces no ninth component orbit.  The `F_1`/`F_2`
orbit identifications and the deeper strata remain open.

## The stratum

Let `U_0,...,U_3` be planes on which `P_4` restricts to a nonzero
decomposable tensor, with kernel lines `K_i=span(y_i)`.  The first
certified component has pair profile `(4,4,4,3,3,3)` and exactly two
rank-one exceptional relations, in the orientation-path shape

```text
u_1 y_3 = 0,        y_2 u_3 = 0,
```

with `u_1 in U_1`, `u_3 in U_3` free directions: the arrows
`1 -> 3 -> 2` share mode `3` with opposite kernel roles.  This
in-out path is precisely the "mixed orientation" alternative that the
radical-star classification (both arrows out) and the mixed-star
charts (two arrows in, one out, at a common centre) do not cover.

By the zero-product support lemma, each relation lives in a
coordinate two-plane.  This note treats the **overlap-one** support
case, normalized by the diagonal source torus to

```text
u_1=(0,0,1,-1),   y_3=(0,0,1,1),
u_3=(1,0,d,0),    y_2=(1,0,-d,0),
U_1=span(u_1,v),  U_2=span(y_2,x),  U_3=span(y_3,u_3).
```

## Exact chart reduction

Associativity through `u_1 y_3=0` makes the perpendicularity
conditions `<z u_1, U_2 y_3>=0` vanish identically, so the pure
vanishing conditions on `U_0` reduce to the two covectors

```text
<z v, y_2 y_3> = 0,        <z v, x y_3> = 0.
```

On the chart where the Cramer pivot of columns `(0,1)`,

```text
pivot = -(v_2+v_3) F_3,
```

is nonzero, `U_0` is the forced kernel plane, and the active
`2 x 2` determinant factors exactly as

```text
det B = c (v_2+v_3) F_1 F_2 F_3 F_4,
```

with

```text
F_1 = -d v_1 x_0 + d v_0 x_1 - (v_2+v_3) x_1 - v_1 x_2 + v_1 x_3,
F_2 = -d v_1 x_0 - d v_0 x_1 + (v_2+v_3) x_1 - v_1 x_2 + v_1 x_3,
F_3 =  d v_1 x_0 - d v_0 x_1 + (v_2+v_3) x_1 + v_1 x_2 + v_1 x_3,
F_4 =  d v_1 x_0 + d v_0 x_1 + (v_2+v_3) x_1 + v_1 x_2 + v_1 x_3.
```

Because the pivot contributes `((v_2+v_3)F_3)^2` to the cleared
determinant, the open-chart pure locus is exactly

```text
F_1 F_2 F_4 = 0        (pivot != 0).
```

## The three open-chart branches

Exact rational sample points on each branch, avoiding the pivot
locus and the other branches, give nonzero pure restrictions with
all three flattenings of rank one and invariants:

| branch | pair profile | rank-3 relations | remark |
|---|---|---|---|
| `F_1` | `(4,4,3,4,3,3)` | rank-one star at mode `3` | sixth/eighth signature class; supports overlap |
| `F_2` | `(4,4,3,4,3,3)` | rank-one star at mode `3` | same class as `F_1` |
| `F_4` | `(4,3,2,4,3,3)` | three rank-one relations, one rank-two pair edge | contained in the seventh component (below) |

## The `F_4` branch is a slice of the six-dimensional component

At the `F_4` sample point the family tangent through the diagonal
torus has rank five, but the universal Segre-incidence Jacobian has
rank **fourteen**, so the local incidence dimension is six: `F_4` is
not a new five-dimensional component.  Its identity is exact.  The
`F_4` point tensor is supported on precisely the words
`1010, 1110` in the Grassmann charts with pivots
`(02),(02),(01),(02)` — the apolar support of
[`P4_SIX_DIMENSIONAL_PURE_COMPONENT.md`](P4_SIX_DIMENSIONAL_PURE_COMPONENT.md).
Writing `m_0,...,m_15` for the `F_4` chart coordinates, the sixfold
family matches with

```text
t_0=-1/m_1,     t_2=1/m_3,      t_1 free,
D=-m_11 t_1,    A+C=-m_10 t_1/t_2,
B=m_4 t_0/t_1,  E=m_6 t_2/t_1,
```

and the two nontrivial residual chart equations reduce, with
`h/t_1 = m_11 - m_10/t_2`, to

```text
1 - m_4 t_0 (h/t_1) - m_5 t_0 = 0,
1 - m_6 t_2 (h/t_1) - m_7 t_2 = 0,
```

both of which hold **identically** on the `F_4` branch; the
structural zero shapes of the remaining chart coordinates also hold
identically.  Hence every generic `F_4` point is a diagonal-torus
translate of a sixfold family point:

```text
the F_4 branch is contained in the seventh component.
```

No ninth component arises from this branch.

## The complementary sheets

On the sheet `v_2+v_3=0` with sub-pivot `v_1 G_4 != 0`
(`G_4=F_4|sheet`), the pure locus is exactly the restriction of
`F_1 F_2 = 0`: no new branch appears.

The `F_3` sheet is closed by two one-line identities:

```text
F_1 + F_3 = 2 v_1 x_3,
F_2 + F_3 = 2 (-d v_0 x_1 + (v_2+v_3) x_1 + v_1 x_3),
```

so the two apparent branches of its active determinant are exactly
the intersections of the `F_1` and `F_2` closures with the sheet.
The remaining sub-pivot factors are chart-normalization boundaries
(`d`, `v_0`, `v_1`, `x_1`), which belong to the other support cases.

On the deep stratum

```text
v_2+v_3=0,        G_4=0,
```

the covector matrix drops to rank one with covector
`(-d v_1, -d v_0, v_1, v_1)`, so `U_0` ranges over the Grassmannian
of planes in its three-dimensional kernel.  The active determinant
there is **independent of the `U_0` moduli** and factors as

```text
det = 4 d^2 v_1^2 x_3 (d v_0 x_1 + v_1 x_3):
```

the deep pure locus is the union of the two branches `x_3=0` and
`d v_0 x_1 + v_1 x_3 = 0`, each fibred by the full `U_0`
Grassmannian.  The first component's five-parameter family embeds in
the second branch: with the gauge

```text
d=i,   v=(l,1,-il,il),   x=(0,1,0,-il),
```

all three stratum equations hold identically.  A rank-monotonicity
comparison of pair profiles shows the first component is **not** in
the closure of the `F_1` branch even though `F_1` vanishes on it;
the rank-drop stratum carries it separately.  An exact sample on the
`x_3=0` branch is a genuine pure restriction with pair profile
`(4,4,4,3,3,3)` and rank-one relations on the full triangle
`{12},{13},{23}` — first-component-like profile but a different
generic relation-rank pattern; its identification is open.

The `F_1` and `F_2` branches are both the **sixth component**.  Its
canonical family, torus-aligned by `diag(t_0,t_1,t_2,-t_2)` with
`d=t_2/t_0`, lands exactly in this chart, and

```text
F_1 = 0   identically on the aligned family,
F_2 = -2 t_1 t_2 (P+Q) != 0 generically.
```

The sixth component has two in-arrows, and re-embedding with its
mode `0` plane in the chart's mode-`1` slot (its `{03}`-relation
free vector is proportional to `u_1` and kills `y_3`) gives

```text
F_2 = 0   identically,
F_1 = 2 t_1 t_2 (D+Q)(P+Q) != 0 generically.
```

Both branch equations are irreducible and the embedded images have
the full branch dimension, so `F_1` and `F_2` are two chart
translates of the sixth component's orbit.  With `F_4` a slice of
the seventh component, **no branch of this chart's open stratum is a
new component**.

## A ninth component through the deep `x_3=0` wall

At the exact rational sample of the deep `x_3=0` branch, the
universal Segre-incidence Jacobian has rank **fifteen**: the
pure-compression locus is smooth and five-dimensional there, so a
unique five-dimensional component passes through the point.  The
branch's own family tangent, including both Grassmannian moduli and
the in-chart torus, has rank only **four**: the branch is a
four-dimensional wall inside that component.

The ambient component is none of the eight certified orbits:

1. components with a generic pair rank `r_ij=3` or `2` at an edge
   where the sample has rank `4` are excluded by rank monotonicity
   on closures.  This eliminates the diagonal-quadric component, the
   three `1+3` components, the sixth, and the eighth (all with
   generic profile `(4,4,3,4,3,3)`), and the seventh is excluded by
   its dimension six against the smooth local dimension five;
2. the first component matches the sample's profile
   `(4,4,4,3,3,3)`, but every chart-normalized image of its dense
   five-parameter family lies in the other deep branch
   `d v_0 x_1 + v_1 x_3 = 0`, which is closed in the chart and does
   not contain the sample (the value there is nonzero).  Since the
   relation alignment forcing that confinement is rigid up to the
   enumerated torus and sign choices, and chart normalization is
   continuous near the sample, the sample is not in the first
   component's closure.

Hence a **ninth five-dimensional pure-compression component**
exists, and its certificate is complete.  The four-dimensional wall
tangent was an artifact of the slice: restoring the full projective
diagonal torus `diag(t_0,t_1,t_2,1)`, the family
`x_3`-branch `x` torus has tangent rank **five** at the exact
rational sample, matching the smooth incidence dimension five, so
its closure is the unique local component.  The same restoration
shows the other deep branch has full-torus tangent rank five as
well; since the first component is contained in its ambient local
fivefold and both are five-dimensional and irreducible, that branch
is exactly the first component, resolving its identification too.

The ninth component's generic point is the torus orbit of the
branch: profile `(4,4,4,3,3,3)` with an **all-rank-one relation
triangle** `{12},{13},{23}` — precisely the configuration slot the
directed classifications had left open (the first component realizes
the triangle with one rank-two relation; the ninth realizes it with
none).  Of the eliminations, the first-component confinement is the
one step using a continuity argument rather than a pure ideal
calculation; a standalone component theorem document with an
independent audit, its `H31`/`H22` generic obstructions, and its
separating invariants are the immediate continuation.

## The disjoint-support chart

In the disjoint support case the torus normalizes completely:

```text
u_1=(0,0,1,-1),  y_3=(0,0,1,1),  u_3=(1,1,0,0),  y_2=(1,-1,0,0),
```

with no residual modulus.  The `u_1`-side conditions again vanish
identically, the Cramer pivot factors as
`-(v_2+v_3)((v_2+v_3)(x_0+x_1)+(v_0+v_1)(x_2+x_3))`, and the active
determinant is the pivot's two factors times a **single irreducible
sextic**: the open stratum has exactly one branch.  The eighth
component embeds exactly: mapping its family through the coordinate
swap `(02)(13)` with mode map `(0,1,2,3) <- (2,1,0,3)` and torus
`t_3=-t_2`, `t_1=t_0` satisfies every chart normalization, the
active determinant reduces to zero modulo the component equation
`Phi`, and the pivot stays generically nonzero.  With matching
dimensions (three in-slice plus two transverse torus directions),
the open stratum of the disjoint chart **is the eighth component**;
no new component appears there.

The disjoint chart's sheets are computed as well.  On the sheet
`v_2+v_3=0` the active determinant's odd-exponent factors are `v_1`
and `v_0+v_1`; on the sheet `S=0` they are `x_2` and
`(v_2+v_3)(x_0+x_1)+(v_0+v_1)x_2`.  On the double-deep stratum
`v_3=-v_2`, `x_3=-x_2`, the covector matrix has rank one with
covector direction `(0,0,1,1)`, the extension kernel is
`z_2+z_3=0`, and with `U_0=span(k_1+alpha k_3, k_2+beta k_3)` for
its coordinate kernel basis the active determinant is exactly

```text
4 (beta-alpha)(v_0+v_1) x_2^2.
```

Unlike the overlap-one deep stratum, the determinant involves the
`U_0` moduli: the branch `alpha=beta` consists precisely of the
planes `U_0` containing the direction `(1,-1,0,0)=y_2`, and the
branch `v_0+v_1=0` of those where `U_1` contains that direction.

Exact samples show both deep branches carry genuine pure
restrictions with previously unrecorded profiles: `(4,3,3,4,3,3)`
with relation ranks `(2,1,1,1)` on `alpha=beta`, and
`(4,4,4,3,2,3)` — a rank-two pair edge — on `v_0+v_1=0`.  At both
branch samples the universal incidence Jacobian has rank thirteen
(tangent dimension seven) against branch tangents of five: the
branches are singular walls, and closure equations decide their
ambient components.

## A tenth component through the singular walls

Three closure computations identify the ambient geometry exactly.
First, eliminating the eighth component's gauge-saturated embedding
parameters gives the principal ideal generated by the chart's
irreducible sextic, so the whole deep stratum passes the
`(v,x)`-level membership test — but `M(v,x) u_1 = 0` holds
identically, so on every rank-two stratum the forced `U_0` contains
`u_1`, and the Pluecker coordinate `p_01(U_0)` vanishes on the
eighth's entire closure.  The deep branches have `p_01(U_0)=1`:
**neither branch lies in the eighth's closure**.  Second, a complete
semicontinuity sieve over all `24 x 24` mode-map/source-permutation
alignments, using rank monotonicity and the forced limits of
rank-one relations, and calibrated on the two proven containments
of this note, **excludes all nine certified components** from both
branches.  Third, the coincident-support configuration left open by
the radical-star classification supplies the ambient family: with
`ybar=(1,-1,0,0)`, `u_3=(1,1,0,0)`,

```text
U_I=span(ybar,(0,1,b,-bk)),   U_J=span(ybar,(0,1,e,-ek)),
U_K=span(u_3,(0,0,1,k)),      U_L=span((1,m,0,0),(0,r,1,-k)),
```

the restriction of `P_4` is **identically pure**,

```text
T = -2k ( be(m+1) e_1100 + (ber+b+e) e_1101 ),
```

and at `(b,e,k,m,r)=(2,3,5,7,11)` the family tangent has rank
**six** while the universal Segre-incidence Jacobian has rank
**fourteen**: a smooth incidence point of dimension six equal to the
family dimension.  Hence the closure is a **six-dimensional
irreducible pure-compression component**, distinct from the eight
fivefolds by dimension and from the seventh by its generic profile
`(3,3,4,3,4,4)` of maximal rank-sum `21` with no rank-two pair
edge: a **tenth component orbit**.  Exact identities place branch
`alpha=beta` inside the family on the nose and branch `v_0+v_1=0`
in its closure as a `b -> infinity` limit.  The certified component
lower bound is now **ten** (since raised to **eleven** by the
equal-support sixfold of continuation item 2).

Honest open items: the tangent gap (seven versus six) at the branch
points leaves room for further components through the same walls;
the remaining case branches of the coincident-support chart, the
third deep sub-branch `x_2=0`, and the tenth component's
independent audit, boundary classification, and `H31`/`H22`
obstructions are open.  The replay scripts are
`eighth_closure_j8_and_u0_obstruction.py`,
`branch_invariants_and_sieve.py`, and
`branch_ambient_certificates.py`.

## Open continuation

1. the standalone ninth-component theorem is now written, with a
   free rational two-parameter normal form, separating invariants,
   the exact `(5,15)` certificate, and a two-prime independent
   audit:
   [`P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md`](P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md);
   its exact `H31`/`H22` obstructions remain open, with an
   exploratory modular `H31` census showing line-shaped marking loci
   and branch-dependent rank-four minors;
2. the equal-support case and the rank-two-dominated strata are now
   analyzed in
   [`research_snapshots/2026-08-04-p4-equal-support-rank-two-strata/`](research_snapshots/2026-08-04-p4-equal-support-rank-two-strata/README.md):
   the equal-support rank-two stratum has a single genuinely pure
   branch `W` whose points are singular walls, and freeing the
   `Pi`-directions exposes an always-pure six-parameter family
   `C10` of family-tangent rank six with profile multiset equal to
   the tenth component's.  The expected alignment `C10 = tenth` is
   **refuted** and `C10` is certified as an **ELEVENTH component
   orbit** (snapshot addendum, steps 28/29): an exact char-0
   six-hyperplane slice standard basis pins the local dimension of
   the pure locus at a generic `C10` sample to exactly six — the
   first component certified at a singular incidence point
   (tangent seven, second-order obstructed normal) — while the
   closed symmetry-stable invariant "some mode's plane is a
   coordinate 2-plane" holds on all of `closure(C10)` (`U_3 = Pi`)
   and fails at the tenth's certificate point, so
   `closure(C10) != g(tenth)` for every census symmetry `g`; the
   `W`-branch is the wall `c0=c1` inside it.  The
   rank-two-dominated **star** stratum is generically **empty**
   (purity forces the zero restriction on the forced pencil), and
   the rank-two-dominated **triangle** reduces to a proper chord
   condition leaving at most four-dimensional walls and **no
   component**; boundary leaves of both remain, as do `C10`'s
   independent audit and `H31`/`H22` obstructions;
3. continue toward component exhaustiveness — eleven is a certified
   lower bound, not a census — plus the remaining `H31`/`H22`
   boundary work and the global prize conjecture, all open.

## Verification

Run:

```text
python verify_p4_inout_path_stratum_working_note.py
```

The script replays, over exact rationals: the identically vanishing
`u_1`-side conditions, the Cramer kernel identity and the factored
active determinant, the sheet and deep-stratum computations, the
first-component embedding, and the three branch sample points with
their flattening ranks, pair profiles, and relation ranks.  For the
`F_4` branch it additionally replays the rank-five family tangent,
the rank-fourteen universal Segre-incidence Jacobian, and the exact
sixfold containment identities.
