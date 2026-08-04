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

The dense overlap-one chart's pure locus is now completely described
and almost completely identified: `F_1` and `F_2` are sixth-component
translates, `F_4` is a seventh-component slice, and the first
component embeds in one deep-stratum branch.  Only the deep
`x_3=0` branch and the exact extent of the first-component branch
remain unidentified.

## Open continuation

1. identify the deep-stratum `x_3=0` branch and decide whether the
   `d v_0 x_1 + v_1 x_3 = 0` branch equals the first component's
   chart part or exceeds it;
2. treat the disjoint and equal support cases of the in-out path;
3. combine with the star classifications toward component
   exhaustiveness, the remaining `H31`/`H22` boundary work, and the
   global prize conjecture, all of which remain open.

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
