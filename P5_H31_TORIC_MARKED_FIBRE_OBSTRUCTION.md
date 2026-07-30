# Complete marked-fibre obstruction on the genuine toric base boundary

## Status

This is an exact characteristic-zero obstruction.

The projective toric base of the known pure rank-two compression
component has five genuine divisor orbits and four edge orbits whose
slice images meet the `2 x 2 x 2` Segre variety.  At plane level these
give exactly

```text
13 divisor/orientation pairs + 8 edge/orientation pairs = 21.       (1)
```

Every marked row basis over every one of those 21 toric plane cases is
now excluded from an `H31` lift.  The calculation covers:

1. both pure directions on every secant slice;
2. the double pure direction on the tangent slice;
3. both projective charts of the first-plane fibre;
4. every kernel-row shift in all four planes; and
5. every binary `Delta_2` extension direction, not merely one displayed
   extension.

Equivalently, the 21 base-orbit/orientation cases refine to 17
pure-direction types and 39 pure-direction/orientation types, and all
39 are obstructed.

The internal `E=0` divisor and projective first-plane boundary over the
base interior have since been closed separately.  This does **not**
exclude the second diagonal-quadric component or any further
pure-compression component, so it is not a global nonexistence theorem
for `H31` or for the prize problem.

## Toric and Segre input

Use the three monomial plane maps and common normal fan from
[`P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md`](P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md).
For a toric orbit representative, contraction through its last three
planes gives

```text
Phi : (C^4)^* -> (C^2) tensor (C^2) tensor (C^2).                  (2)
```

The exact Segre calculation in
[`P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md`](P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md)
leaves the following genuine base orbits:

| orbit type | toric normal(s) | pure slice | all-rank `q` |
| --- | --- | --- | --- |
| divisor | `(-1,1,0)` | secant | `0,2` |
| divisor | `(0,-1,1)` | tangent | `0,1,3` |
| divisor | `(0,0,-1)` | secant | `2,3` |
| divisor | `(0,1,0)` | secant | `0,1,2` |
| divisor | `(1,0,-1)` | secant | `1,2,3` |
| edge | `(-1,0,0),(-1,1,0)` | secant | `0,2` |
| edge | `(-1,0,0),(0,0,-1)` | secant | `2,3` |
| edge | `(-1,1,0),(0,1,0)` | secant | `0,2` |
| edge | `(0,0,-1),(1,0,-1)` | secant | `2,3` |

Changing the representative inside a toric orbit acts by invertible
diagonal source transformations and row-basis transformations.  It
preserves the binary incidence, marked-map ranks, and transverse pure
coordinate.  Unit-coefficient representatives therefore lose no
cases.

## The complete marked fibre

Fix one of the 17 pure directions.  Let `K=ker(Phi)`, so `dim K=2`,
choose a basis `k_0,k_1`, and let `w` be the reconstructed pure lift.
The first kernel row ranges over `P(K)`.  Two charts cover it:

```text
finite:    alpha_0=k_0+r k_1,
           beta_0 =w+s k_1+t_0 alpha_0;

infinity:  alpha_0=k_1,
           beta_0 =w+s k_0+t_0 alpha_0.              (3)
```

For the other three planes, the pure tensor fixes a kernel line
`C alpha_i` and a complementary pure-colour row `U_i`.  Every marking
over the same plane is

```text
beta_i=U_i+t_i alpha_i,             i=1,2,3.         (4)
```

Thus `(r,s,t_0,t_1,t_2,t_3)` in the finite chart and
`(s,t_0,t_1,t_2,t_3)` in the infinity chart parameterize the complete
marked fibre, not a preferred section.

## Binary projection ledger

For distinguished source coordinate `q`, let `M_q z=0` be the fourteen
mixed binary equations and let `d_0(z),d_1(z)` be the two diagonal
coefficients.  Saturate by `d_0d_1` and eliminate the eight extension
coordinates.  The table below records a reference all-rank orientation
for each pure-direction type.

Write `F` and `I` for the finite and infinity charts.  The exact
absolute elimination ledger is:

| case | orbit/pure direction | `F` marking ideal | `I` marking ideal |
| ---: | --- | --- | --- |
| 0 | `(-1,1,0)`, `(-1,-1)` | `t1,t2,t3` | `t1,t2,s t3,t0 t3` |
| 1 | `(-1,1,0)`, `(1,-1)` | `t3,s t2,(t1+r)t2,t0 t2,t0(t1+1)` | `t3,t2,t1+1` |
| 2 | `(0,-1,1)`, tangent | `1` | `1` |
| 3 | `(0,0,-1)`, `(-1,-1)` | `t3,s t1,t0 t1,(r t2-1)t1,(t2-1)(r t0+s)` | `t3,t2,t0,s t1` |
| 4 | `(0,0,-1)`, `(1,-1)` | `t2+1,t1,s t3,r t3,t0 t3` | `1` |
| 5 | `(0,1,0)`, `(-1,-1)` | `t2,t1+r,t0,s t3` | `1` |
| 6 | `(0,1,0)`, `(1,-1)` | `t3,t1+r,t0,s t2` | `1` |
| 7 | `(1,0,-1)`, `(-1,-1)` | `t3,t2(s+1)+t0,t1(s+1),r t2-1,r t0+s+1,t0 t1` | `t3,t2,t0+1,s t1` |
| 8 | `(1,0,-1)`, `(1,-1)` | `t1,t3(s-1),t2(s-1)+t0,r t2-1,r t0+s-1,t0 t3` | `t2,t1,t0-1,s t3` |
| 9 | first edge, `(-1,-1)` | `t1,t2,t3` | `t1,t2,s t3,t0 t3` |
| 10 | first edge, `(1,-1)` | `t3,t1,s t2,r t2,t0 t2` | `t1,t2,t3` |
| 11 | second edge, `(-1,-1)` | `t1,t2,t3` | `t3,t2,s t1,t0 t1` |
| 12 | second edge, `(1,-1)` | `t2,t1,s t3,r t3,t0 t3` | `t1,t2,t3` |
| 13 | third edge, `(-1,-1)` | `t2,t1+r,t0,s t3` | `1` |
| 14 | third edge, `(1,-1)` | `t3,t1+r,t0,s t2` | `1` |
| 15 | fourth edge, `(-1,-1)` | `t3,s t2+t0,s t1,r t2-1,r t0+s,t0 t1` | `t3,t2,t0,s t1` |
| 16 | fourth edge, `(1,-1)` | `t1,s t3,s t2+t0,r t2-1,r t0+s,t0 t3` | `t2,t1,t0,s t3` |

Four finite-chart types change signs in the other all-rank
orientations:

```text
cases 5,6 at q=1:       t1+r -> t1-r;
case 7 at q=2,3:        t2(s+1)+t0 -> t2(s+1)-t0,
                        r t2-1 -> r t2+1;
case 8 at q=2,3:        t2(s-1)+t0 -> t2(s-1)-t0,
                        r t2-1 -> r t2+1.
```

All other displayed generators are unchanged.  The primary verifier
checks the full 78-entry `(direction,q,chart)` ledger, rather than
reusing the reference orientation.

The tangent case is already binary-empty.  Every other ideal is a
union of at most three elementary linear/coordinate strata.  No search
over local maps or Grassmannians is involved.

## Ternary obstruction

For a binary extension `z`, append its entries as the fifth source
column.  For mode `i`, let

```text
N_i(z) : C^4 -> C^8                                      (5)
```

be the one-marked map on the neighbouring hyperplane, and let
`p_i` be the distinguished column of the corresponding pure-hyperplane
map.

A third target colour would require, in every mode,

```text
p_i=0  or  rank N_i(z)<4.                                (6)
```

For each of the 34 direction/chart pairs, at most four selected
`4 x 4` minors suffice.  The primary verifier forms the exact ideal

```text
M_q z,
d_0(z)-1,
u d_1(z)-1,
(entry of p_i) * (selected 4-minor of N_i(z)).            (7)
```

The last products encode the necessary condition (6) without choosing
a nonzero entry of `p_i` or dividing by a parameter.  For all 39
orientations and both charts, the reduced ideal in (7) is the unit
ideal.  This simultaneously proves:

```text
d_0(z)d_1(z)!=0
    ==> some selected mode has p_i!=0 and rank N_i(z)=4.  (8)
```

Because (7) is checked before any rational-function branch
normalization, special values such as `r=0`, `r=1`, `s=0`, and the
coordinate-axis intersections are included automatically.  The
factor-level explanation is uniform: after restricting to a projection
stratum, a selected minor is

```text
d_0(z) d_1(z) * ell(z),                                (9)
```

and the residual linear forms `ell` either equal a nonzero scalar
multiple of `d_0` or form a two- or three-element cover with no common
zero on `d_0d_1!=0`.

Equation (8) is exactly the transverse-kernel obstruction: the third
target row would have to vanish on both adjacent source hyperplanes and
hence vanish globally, contradicting target rank three.

## Verification

Run:

```text
python verify_p5_h31_toric_marked_fibre_obstruction.py
python audit_p5_h31_toric_marked_fibre_obstruction.py
```

The primary verifier reconstructs the toric face/Segre data, reruns the
absolute saturated projection eliminations in Singular, and checks all
selected binary-plus-ternary ideals over characteristic zero.  The
independent audit evaluates every point of the projection strata over
`F_5` and `F_7`, computes each mixed kernel by modular row reduction,
enumerates every projective binary extension direction, and tests the
selected marked minors directly.  Its orientation-aware totals are
13,064 projection points, 272,624 binary extensions, 291,176 minor
tests, and 520 projection-closure artifacts.

The finite-field audit is a regression check for exceptional strata;
the characteristic-zero unit-ideal certificates are the proof.
