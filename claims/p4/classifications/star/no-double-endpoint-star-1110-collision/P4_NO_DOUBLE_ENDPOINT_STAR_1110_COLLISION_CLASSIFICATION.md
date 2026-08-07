# Classification of the no-double endpoint star `(1,1,1)` cell

## Status

**Exact characteristic-zero classification.**  Let a nonzero pure `P_4`
compression have all six pair-image ranks at least three, and choose a
rank-one exceptional star with no kernel--kernel spoke and endpoint-indegree
signature `(1,1,1,0)`.  Every such point lies in an already certified
component closure.  Hence the no-double part of the last star `(1,1,1)` cell
creates no new component.

Together with the separately replayed one-, two-, and three-double-spoke
theorems, this closes the rank-one star `(1,1,1)` all-pair cell.  It does not
close the remaining special/projective `P_5` fibres, the arbitrary-order
local-to-global reduction, or the global Krenn--Gu conjecture, which remains
**UNRESOLVED**.

All calculations below are over `Q` and therefore over `C`.  No finite-field
calculation is used as proof.

## The two orientation orbits

Center the star at mode zero and write `U_i=<y_i,x_i>`, with `y_i` the pure
kernel.  Up to leaf permutation there are two no-double orientations.

```text
A (all outward):  w_i y_i=0,                    i=1,2,3,
B (one inward):   y_0 v_1=0,  w_2 y_2=0,  w_3 y_3=0,
```

where every `w_i` belongs to `U_0`, and no displayed center factor equals
`y_0`.  A nonzero degree-one zero product is either a repeated singleton or
the two polar lines on one genuine binary coordinate support.

## Orbit A: all three relations point to leaves

Let `m` be the number of distinct center-factor lines among `w_1,w_2,w_3`.

### One center-factor line

If its support is singleton, all three leaf kernels are that singleton and
every exterior leaf pair has rank at most three.  For genuine binary support,
normalize the common factor and its polar to

```text
A=X_0+X_1,       C=X_0-X_1.
```

After Borel shifts the saturated purity radical has two minimal primes.  One
makes the center plane degenerate.  On the other, all three exterior
four-by-four product minors vanish.  Thus every nondegenerate point has an
exterior rank-three edge and is placed by the completed rank-one triangle
classification.

### Two center-factor lines

Relabel so `w_1=w_2`.  A singleton repeated factor immediately gives
`r_12<=3`.  For a genuine binary repeated factor, the second factor has four
support positions:

```text
same binary line       -> active coefficient is in the purity ideal,
overlapping binary     -> r_13,r_23<=3,
disjoint binary        -> r_13,r_23<=3,
outside singleton      -> saturated nonzero purity ideal is the unit ideal.
```

The singleton endpoint inside the first binary line belongs to the first
row.  The overlapping and disjoint statements follow from one exact minimal
prime apiece; no affine complementary-row direction is omitted.

### Three center-factor lines

A projective line meeting the union of the six coordinate support lines in
three distinct points is either one coordinate line or a transversal of the
three edges of one coordinate triangle.  Indeed, if the three points are not
on one coordinate line, their unique linear dependence has three nonzero
coefficients.  A source coordinate occurring in only one point would then
force its coefficient to vanish.  Hence every used coordinate occurs in at
least two of the three supports.  The supports have total size at most six,
so they use exactly three coordinates, each exactly twice; their labels are
the three edges of that coordinate triangle.  In the first case put the factors
at `C,C+lambda A,C+mu A`; the three polar equations `q_12=q_13=q_23=0`
generate the active coefficient, including singleton and coincident
parameter values.

For the coordinate-triangle case put

```text
f_1=X_0+X_1,  g_1=X_0-X_1,
f_2=X_0+X_2,  g_2=X_0-X_2,
f_3=X_2-X_1,  g_3=X_2+X_1,

U_0=<f_2+t f_1,f_1>,
U_1=<g_1,a_1f_1+b_1X_2+d_1X_3>,
U_2=<g_2,a_2f_2+c_2X_1+d_2X_3>,
U_3=<g_3,a_3f_3+c_3X_0+d_3X_3>.                 (1)
```

No double spoke is exactly `t(t+1)!=0`.  Saturating the full purity ideal of
(1) by `t(t+1)T_1111` gives a radical with exactly one minimal prime, and
`d_1d_2d_3` is nonzero on that prime.  Thus its normalized chart `d_i=1` is
dense.  There the equations give

```text
b_1=-2(a_2+a_3),
c_2=-2a_1+2a_3,
c_3=-2(a_1+a_2),
t=a_2(-a_1+a_3)/(a_1(a_2+a_3)),                  (2)
T_1111=8a_1(a_2+a_3).
```

Apply the source permutation

```text
(old X_0,old X_1,old X_2,old X_3)
       -> (new X_1,new X_2,new X_3,new X_0)
```

and reorder modes as `(3,1,2,0)`.  After legal row shifts, the parameters of
the `1+3` normal form are

```text
S=2a_1,  D=-2(a_2+a_3),  G=-2a_1+2a_3,  T=2a_2.
```

They satisfy exactly

```text
T=-D-G-S,
```

the certified branch `L_3`.  Moreover, with `P=G-T,Q=D-S`, transformed mode
zero is

```text
<(2,2c_3,-4a_3,0),(0,0,1,1)>
 = <(2,P+Q,Q-P,0),(0,0,1,1)>,
```

so this is an equality of plane tuples, not only a parameter coincidence.
The unique saturated prime then places every `d_i=0` projective boundary in
the same `L_3` closure.

The missing term in (2) is essential.  The previously considered values
`a_1=a_2=a_3=1,b_1=-4,c_2=2,c_3=-4,t=6/5` are **not pure**:

```text
T_0011=2,  T_0110=22/5,  T_1110=2,  T_1111=10.
```

The replay fixes this failed route permanently by checking both those four
coefficients and the corrected identity `c_2=-2a_1+2a_3`.

## Orbit B: one relation points to the center

If `w_2,w_3` are independent, the center line contains the three distinct
zero-divisor factors `y_0,w_2,w_3`.  The same line-incidence lemma leaves:

```text
coordinate binary line, all factors genuine -> component 21,
coordinate binary line with singleton point -> component 21 parameter closure,
coordinate-triangle transversal              -> radical-star L_1,L_2,L_3.
```

There are four placements of one or two singleton endpoints on the binary
line.  Normalize its three factor ratios to `s,1,t`.  On the open
`s*t*(s-1)*(s-t)*(t-1)!=0`, the saturated radical has two primes: one
degenerates `U_1`, while the unique nondegenerate prime is independent of
`s,t`.  It is the genuine coincident-support component-21 chart.  Setting
`s=0` gives the singleton endpoint with every complementary row fixed, so
the singleton sheet is an explicit parameter limit in component 21.  A
coordinate swap and leaf permutation give the other three endpoint
placements.  These boundary points need not be lower-pair: the verifier
records the exact profile `(3,3,3,4,4,4)` for one of them.

Suppose instead `w_2,w_3` are dependent.  Write their common factor as `w`
and its polar as `z`:

```text
U_0=<u,w>,  U_1=<y,v>,  U_2=<z,x>,  U_3=<z,q>,
uv=wz=0.                                          (3)
```

The complete support ledger for the two zero products in (3) is:

```text
same genuine binary support     -> component 21 reverse theorem,
support of w singleton          -> r_23<=3,
support of u singleton, inside  -> degenerate or r_23<=3,
support of u singleton, outside -> degenerate,
distinct overlapping binaries   -> degenerate,
distinct disjoint binaries      -> four nondegenerate primes,
                                   each with an exterior rank-three edge.
```

The disjoint four primes respectively force

```text
(r_12,r_13) <= (3,3),
(r_12,r_13,r_23) <= (3,3,3),
(r_12,r_23) <= (3,3),
(r_13,r_23) <= (3,3).
```

Thus every support-one, coincident, dependent-center-factor, and
complementary-row projective collision is zero, lower/exterior-rank, or in
component `21` or `L_1,L_2,L_3`.  The lower/exterior-rank cases are already
exhausted by the lower-pair and completed triangle theorems.

## Replay

```text
uv run --with sympy python claims/p4/classifications/star/no-double-endpoint-star-1110-collision/verify_p4_no_double_endpoint_star_1110_collision_classification.py
uv run --with sympy python claims/p4/classifications/star/no-double-endpoint-star-1110-collision/audit_p4_no_double_endpoint_star_1110_collision_classification.py
```

The primary verifier reconstructs all permanent coefficients, exact
characteristic-zero saturated radicals, exterior pair-minor containments,
the full source-triangle projective prime, and the explicit transformation
to `L_3`.  The no-import audit uses a separate subset-DP permanent,
independently checks the failed and corrected samples, replays representative
rational points in every nonempty collision branch, and checks their exact
pair profiles.  Finite-field output is not used.
