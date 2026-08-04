# The in-out path stratum of the pure `P_4` locus: working note

## Status

This is an exact exploratory checkpoint, not a component theorem.
It opens the mixed-orientation stratum left unclassified by
[`P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md`](P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md):
two rank-one exceptional relations in directed **path** position.
The chart identities below are exact and replayed; the component
identifications they suggest are explicitly open.

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
| `F_4` | `(4,3,2,4,3,3)` | three rank-one relations, one rank-two pair edge | **matches no recorded component profile** |

The six-dimensional component's recorded profile is `(4,3,2,4,4,3)`,
so the `F_4` branch is either a new component orbit or a special
slice of a known one; deciding requires the tangent and
Segre-incidence certificates of the component toolkit.

## The complementary sheets

On the sheet `v_2+v_3=0` with sub-pivot `v_1 G_4 != 0`
(`G_4=F_4|sheet`), the pure locus is exactly the restriction of
`F_1 F_2 = 0`: no new branch appears.

On the deep stratum

```text
v_2+v_3=0,        G_4=0,
```

the covector matrix drops to rank one, so `U_0` is no longer forced
and gains Grassmannian moduli.  The first component's five-parameter
family embeds exactly there: with the gauge

```text
d=i,   v=(l,1,-il,il),   x=(0,1,0,-il),
```

both stratum equations hold identically.  A rank-monotonicity
comparison of pair profiles shows the first component is **not** in
the closure of the `F_1` branch even though `F_1` vanishes on it; the
rank-drop stratum carries it separately.

## Open continuation

1. classify the rank-one stratum of the deep locus (where the first
   component lives) and the `F_3` sheet;
2. run the tangent/Segre-incidence certificates on `F_1`, `F_2`,
   `F_4` and identify their orbits against the eight known
   components; a ninth orbit at `F_4` would extend the certified
   lower bound;
3. treat the disjoint and equal support cases of the in-out path;
4. combine with the star classifications toward component
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
their flattening ranks, pair profiles, and relation ranks.
