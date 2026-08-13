# Balanced `m=3` full-sensor separated-singleton pole localization theorem

## Status

**Exact characteristic-zero localization of every possible pair pole on the
normalized `m=3` full-sensor branch.**  After the empty deck coefficient is
fixed to one, the three remaining balanced-sensor columns depend linearly on
three separate nonroot projective factors.  Let `U_x,U_y,U_r` be their three
linear image spaces.  If the unique rational pair deck has a divisorial pole,
then at least one of the following low-span degeneracies is forced:

```text
dim U_u=1 for some u;
dim(U_u+U_v)=2 for some pair {u,v};
dim(U_x+U_y+U_r)=3.                                  (1)
```

Equivalently, if every singleton image has dimension at least two, every pair
of images spans dimension at least three, and the total span has dimension at
least four, then all three rational pair components are global bilinear
sections.  No factorization of a Cramer minor and no sampling are used.

For one physical common shore, these image spaces are the spans of its three
singleton-complement companion columns.  Target consistency, empty
normalization, and globality of the three pair components would reconstruct a
six-vertex Krenn--Gu graph.  The exact six-vertex exclusion therefore implies
that every normalized target-consistent physical `m=3` full sensor, if viewed
before applying that exclusion, must lie in the union (1).

This is a structural localization, not a new proof of the already certified
six-vertex theorem.  It does **not** exclude any of the three exceptional
strata in (1), extend the argument to `m>=4`, control the higher Euler--hafnian
recurrences, exclude the all-balanced rank-drop branch, or resolve the global
conjecture.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The normalized three-column system

Work over a characteristic-zero field `K`, extending scalars to an algebraic
closure when discussing divisors.  Let

```text
X,Y,R be three-dimensional K-vector spaces,
A be a finite-dimensional K-vector space,                    (2)
```

and let

```text
g_x:X -> A,       g_y:Y -> A,       g_r:R -> A              (3)
```

be linear maps.  On

```text
P=P(X) x P(Y) x P(R)                                      (4)
```

they define the separated-column bundle map

```text
phi:
 O(0,1,1) direct-sum O(1,0,1) direct-sum O(1,1,0)
 -> A tensor O(1,1,1),                                    (5)

(c_x,c_y,c_r) |-> g_x(x)c_x+g_y(y)c_y+g_r(r)c_r.
```

The subscripts on `c_u` name the singleton column, not its complementary pair
deck label.  Thus `c_x` has the degree of the nonroot pair `yr`, and cyclically.

Put

```text
U_u=image(g_u),
r_u=dim U_u,
s_uv=dim(U_u+U_v),
s=dim(U_x+U_y+U_r).                                  (6)
```

Assume `phi` has function-field column rank three.  In particular,

```text
r_u>=1,             s_uv>=2,             s>=3.       (7)
```

Let `b` be a global section of `A tensor O(1,1,1)` that belongs to the
function-field image of `phi`.  There is then a unique rational coefficient
triple

```text
c=(c_x,c_y,c_r),            phi(c)=b.                (8)
```

The question is whether any component of (8) can have a prime-divisor pole.

## 2. Divisors in the separated rank-drop locus

Let

```text
Z={(x,y,r) in P : g_x(x),g_y(y),g_r(r) are dependent}. (9)
```

Every dependence has a minimal nonempty support of size one, two, or three.
This elementary stratification gives the whole codimension calculation.

### Lemma 1 (minimal-support codimensions)

Under the function-field rank-three hypothesis:

1. A one-column stratum `g_u(u)=0` has codimension `r_u` when nonempty.
2. The stratum on which exactly the two nonzero columns `g_u(u),g_v(v)` are
   dependent has codimension `s_uv-1` in `P` when nonempty.
3. The stratum on which all three columns have a minimal dependence has
   codimension `s-2` in `P` when nonempty.

Consequently `Z` has a prime-divisor component if and only if at least one
condition in (1) holds.

### Proof

For one column, the zero set is `P(ker g_u)` in its `P^2` factor.  A rank
`r_u` linear map cuts codimension `r_u`; for `r_u=3` the projective zero set
is empty.

For a pair `{u,v}`, consider the sum map

```text
X_u direct-sum X_v -> U_u+U_v.                       (10)
```

Its kernel has dimension `6-s_uv`, hence projective dimension `5-s_uv`.
On the open set where both images are nonzero, a dependent projective pair
has a unique scalar ratio.  Therefore projectivizing (10)'s kernel maps
injectively to the two relevant `P^2` factors.  The unused third factor adds
dimension two.  The resulting dimension is `7-s_uv` inside the
six-dimensional product `P`, so the codimension is `s_uv-1`.

For a minimal three-column dependence, use instead

```text
X direct-sum Y direct-sum R -> U_x+U_y+U_r.           (11)
```

Its kernel has dimension `9-s` and projective dimension `8-s`.  After the
one- and two-column strata are removed, the dependence relation is unique,
so the same projectivization map is injective.  The codimension in `P` is

```text
6-(8-s)=s-2.                                         (12)
```

Every point of `Z` has one of these three minimal supports.  A codimension-one
component can therefore occur only at `r_u=1`, `s_uv=2`, or `s=3`.

Conversely, `r_u=1` gives the divisor `P(ker g_u)`.  If no rank-one case is
already present and `s_uv=2`, both images have dimension at least two and
their nonzero dependence stratum has the calculated codimension one.  If no
earlier case is present and `s=3`, the three columns lie in a common
three-space and their nonzero determinant is a trilinear equation; it is not
identically zero by function-field rank three and hence cuts a divisor.
This proves the final assertion.  QED.

## 3. Pole localization and globality

### Theorem 2 (all pair poles lie on the low-span union)

If one rational coefficient in (8) has a prime-divisor pole, then one of the
three conditions in (1) holds.

If instead

```text
r_x,r_y,r_r >=2,
s_xy,s_xr,s_yr >=3,
s>=4,                                                (13)
```

then the unique rational coefficients are global sections of their three
line bundles in (5).

### Proof

Let `D` be a prime divisor not contained in `Z` and work in regular local
frames at its generic point.  Some three-row minor of the column matrix of
`phi` is a unit in the discrete valuation ring `O_(P,D)`.  Restricting (8)
to those rows and inverting this unit minor shows that every component of
`c` lies in `O_(P,D)`.  Hence a pole divisor of `c` must be a divisor inside
`Z`.

Lemma 1 gives the first assertion.  Under (13), `Z` has codimension at least
two, so `c` is regular at every prime divisor.  The product of projective
spaces `P` is smooth and therefore normal.  A rational line-bundle section
regular at every prime divisor extends globally, proving the second
assertion.  QED.

In particular,

```text
H^0(P,O(0,1,1))=Y^* tensor R^*,                     (14)
```

and cyclically.  Thus the three extended components are exactly constant
physical bilinear edge blocks, not merely pole-free chart functions.

## 4. Specialization to the physical balanced sensor

Take the physical `m=3` common-shore notation of the
[`singleton-slice and empty-permanent theorem`](BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md).
The three singleton companion columns are

```text
G_x(x)=D_B(H_x x),
G_y(y)=D_B(H_y y),
G_r(r)=D_B(H_r r),                                  (15)
```

where `D_B` is the common root--root shared-factor map and each `H_u`
collects the three colour slices of the root--nonroot blocks at `u`.  Thus
(15) has exactly the separated form (3), with

```text
U_u=span_K{the three singleton slices at u}.          (16)
```

The four even-deck columns are ordered `(xy,xr,yr,empty)`.  If empty
normalization holds, subtracting the physical empty companion gives

```text
b=J-G_N
 =G_r C_xy+G_y C_xr+G_x C_yr.                       (17)
```

A function-field rank-four full sensor makes the three singleton columns in
(17) function-field independent.  Theorem 2 therefore applies to its unique
rational pair deck.

### Corollary 3 (the regular `m=3` incidence stratum is empty)

Over `C`, suppose one physical common-shore `m=3` sensor has function-field rank four,
satisfies all GHZ target rows, and has `C_empty=1`.  If its singleton image
spaces satisfy (13), then its three rational pair components are physical
bilinear blocks.  Adjoining them to the same shore produces a six-vertex
ternary Krenn--Gu graph.

The exact six-vertex exclusion rules this out.  Consequently every such
normalized target-consistent physical incidence must satisfy at least one
low-span condition in (1).

### Proof

Theorem 2 and (14) make all pair components global physical blocks.  At
`m=3` there is no higher even subset and hence no Euler--hafnian recurrence
beyond the pair layer.  Equation (17), empty normalization, and the balanced
complete-deck identity therefore reconstruct one graph satisfying the
original six-vertex GHZ equality.  This contradicts
[`SIX_VERTEX_CERTIFICATE.md`](../finite/n06/SIX_VERTEX_CERTIFICATE.md).
QED.

The corollary uses the accepted computer-assisted six-vertex theorem as an
upstream premise.  The same conclusion holds over an arbitrary
characteristic-zero field: the finitely many coefficients of a putative
solution generate a finitely generated extension of `Q`, which embeds in
`C`.  The new content is the complete divisor classification and the
reduction of every possible nonphysical pair lift to (1).

### Location of the eight S2M controls

Every normalized full-row sharpness control from S2M lies on the first
exceptional stratum in (1).  For the chosen pair `xy`, its singleton column
is `G_r`.  In the two outside controls, `G_r` is `r_0` times one fixed root
tensor.  In each of the six endpoint controls, it is `r_a` times one fixed
root tensor.  Hence

```text
dim U_r=1                                             (18)
```

in all eight cases.  Theorem 2 therefore does not incorrectly regularize
those ambient poles.  S2P supplies the different, physical common-shore
obstruction proving that none of the eight rank-one controls is realizable.

## 5. Sharp separated-column controls

The three exceptional conditions cannot be removed from Theorem 2 at the
level of separated linear columns and an arbitrary global target section.
The following exact systems exhibit their rank-drop divisors.

Use coordinates `x_i,y_i,r_i` and standard vectors `e_i`.

1. **Rank-one column.**  Take `g_x(x)=x_0e_0` and put the other two images in
   disjoint coordinate spaces.  Every maximal minor is divisible by `x_0`.
   The global target `x_1y_0r_0e_0` has the unique coefficient
   `(x_1/x_0)y_0r_0`, with a pole on `x_0=0`.
2. **Pair span two.**  Take

   ```text
   g_x=(x_0,x_1,0,0,0),
   g_y=(y_0,y_1,0,0,0),
   g_r=(0,0,r_0,r_1,r_2).                            (19)
   ```

   The common maximal-minor factor is
   `delta=x_0y_1-x_1y_0`.  With `t=x_2y_2r_0`, the global target `t e_0`
   has coefficients `t y_1/delta` and `-t x_1/delta` on the first two
   columns.
3. **Total span three.**  Put all three full-rank columns in one common
   three-space.  Their only maximal minor is the trilinear determinant
   `det[x,y,r]`, and a generic global target of multidegree `(1,1,1)` has
   Cramer coefficients with that denominator.

For contrast, the coordinate arrangement

```text
U_x=span(e_0,e_1),
U_y=span(e_1,e_2),
U_r=span(e_2,e_3)                                   (20)
```

has dimensions `(2,2,2)`, pair-span dimensions `(3,4,3)`, and total span
four.  Its maximal minors have greatest common divisor one, exactly as
Theorem 2 predicts.

These controls are sharpness examples for the abstract separated-column
localization.  They are not claimed to be physical common-shore sensors,
GHZ target incidences, or graph counterexamples.

## 6. Proof-topology consequence

The `m=3` part of the full-sensor branch now has the exact stratification

```text
normalized target-consistent physical full sensor
  -> unique rational three-pair lift;
  -> any pole forces rank-one, pair-plane, or common-three-space
     singleton incidence;
  -> outside that low-span union, all pairs are physical;
  -> certified n=6 exclusion makes the outside stratum empty.       (21)
```

What remains is not an unstructured search over arbitrary Cramer
denominators.  At `m=3`, every possible pole is localized to the three named
subspace arrangements.  The theorem does not show that those arrangements
are populated by a normalized physical target incidence, nor does it derive
an arbitrary-order localization from them.

```text
separated-column divisor classification:             PROVED;
all m=3 pair poles localized to (1):                  PROVED;
regular physical target-incidence stratum:            EMPTY via n=6;
rank-one singleton exceptional stratum:               NOT EXCLUDED HERE;
pair-plane singleton exceptional stratum:             NOT EXCLUDED HERE;
common-three-space singleton exceptional stratum:     NOT EXCLUDED HERE;
arbitrary m full-sensor gate:                         OPEN;
all-balanced rank-drop branch:                        OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.          (22)
```

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_full_sensor_separated_singleton_pole_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_full_sensor_separated_singleton_pole_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_full_sensor_separated_singleton_pole_localization.py claims/arbitrary-order/audit_balanced_m3_full_sensor_separated_singleton_pole_localization.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_full_sensor_separated_singleton_pole_localization.py claims/arbitrary-order/audit_balanced_m3_full_sensor_separated_singleton_pole_localization.py
```

The primary replay uses symbolic maximal minors and exact Cramer identities
to check all three sharp divisor types, the regular four-space control, and
the line-bundle multidegrees of the displayed poles.  The independent
no-import audit uses a separate sparse-polynomial exterior-product
implementation and exact rational subspace ranks.  The arbitrary-subspace
exhaustion is the minimal-support dimension proof in Lemma 1; neither script
samples graphs or substitutes for that proof.

## Dependencies

- [`BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md`](BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md)
- [`BALANCED_FULL_SENSOR_CRAMER_EULER_PAIR_POLE_GATE_THEOREM.md`](BALANCED_FULL_SENSOR_CRAMER_EULER_PAIR_POLE_GATE_THEOREM.md)
- [`BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md`](BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md)
- [`SIX_VERTEX_CERTIFICATE.md`](../finite/n06/SIX_VERTEX_CERTIFICATE.md)
