# Balanced full-row Cramer target consistency and normalization remain compatible with every projective pair control

## Status

**Exact characteristic-zero compatibility boundary for the open balanced
full-sensor gate.**  At `m=3`, retain all `27` ternary root-word rows, the
four complete even-deck columns, the exact GHZ target in every row, full
function-field column rank, and empty normalization.  For each of the eight
retained projective pair-jet coordinates from the projective-minimal theorem,
there is an exact degree-compatible Cramer system in which that coordinate is
the only nonzero retained coordinate of the chosen pair.

Thus every selected-system sharpness **pattern** has a new control on which
the omitted target rows and empty normalization are both imposed, without
making that chosen pair coordinate redundant.  These are not literal row
extensions of the old matrices: their unique Cramer solutions failed empty
normalization.  The replacement controls below satisfy the complete target
equation `Gamma f=J`, not merely its selected Cramer rows.

The matrices below are **balanced-format** full-row systems: their columns
have the exact deck-complement multidegrees and their target is the exact GHZ
section.  They are not proved to arise from the common-shore companion
matching-sum formula for a balanced sensor.  No matching-sum realization,
physical graph, Krenn--Gu witness, or counterexample is asserted.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. The full-row balanced format

Work over

```text
R=Q[x_0,x_1,x_2,y_0,y_1,y_2,r_0,r_1,r_2],
F=Frac(R).                                             (1)
```

The three ternary nonroot groups are `x,y,r`.  Rows are indexed by all root
words

```text
W={0,1,2}^3,                                          (2)
```

and the complete even deck is ordered as

```text
(xy,xr,yr,empty).                                     (3)
```

The target column `J in R^27` is the contracted ternary GHZ section

```text
J_(c,c,c)=x_c y_c r_c,       c=0,1,2,
J_w=0                         otherwise.             (4)
```

A **degree-compatible full-row Cramer system** is a matrix
`Gamma in Mat_(27 x 4)(R)` whose columns have group multidegrees

```text
deg Gamma_xy    =(0,0,1),
deg Gamma_xr    =(0,1,0),
deg Gamma_yr    =(1,0,0),
deg Gamma_empty =(1,1,1).                            (5)
```

These are exactly the complements of the deck labels.  The system is
target-consistent and normalized when a vector `f in F^4` satisfies

```text
Gamma f=J,             f_empty=1.                    (6)
```

Every nonzero candidate deck component also has its own rational label
multidegree:

```text
deg f_xy    =(1,1,0),
deg f_xr    =(1,0,1),
deg f_yr    =(0,1,1),
deg f_empty =(0,0,0).                               (6a)
```

Both numerator and denominator degrees are counted in (6a).

If four rows form a minor `A` with `beta=det(A)!=0`, and `j` is the target
restricted to those rows, then (6) gives the ordinary Cramer identities

```text
f=A^(-1)j=v/beta,       v=adj(A)j,
Gamma v=beta J,         v_empty=beta.                (7)
```

Definition (5) and equations (6)--(7) retain the full-row algebra of the
balanced gate.  They deliberately do not impose the further nonlinear fact
that every column is one companion matching sum `G_(N-I)` built from the
same shore blocks.

Fix the projective chart

```text
x_0 y_0 r_0 !=0                                        (8)
```

and the chosen pair `e=xy`.  Its reduced ternary jet family consists of

```text
partial_(r,1) f_xy, partial_(r,2) f_xy;

partial_(x,a)partial_(x,b) f_xy,
partial_(y,a)partial_(y,b) f_xy,
             1<=a<=b<=2.                             (9)
```

Multiplication by the nonzero Cramer powers `beta^2` and `beta^3` converts
these derivatives into the replacement-minor stresses of the owning
projective-minimal theorem without changing which coordinates vanish.

## 2. Compatibility theorem

### Theorem 1 (all eight normalized full-row controls)

For every coordinate in (9), there is a matrix `Gamma` satisfying (5), of
function-field column rank four, and a vector `f` satisfying (6), such that
the chosen coordinate is nonzero and the other seven coordinates in (9)
vanish.

Consequently none of the eight retained coordinates of one pair follows
from

```text
complete 27-row GHZ target consistency;
empty normalization;
full function-field column rank;
deck-complement column multidegrees;
the other seven retained coordinates of that pair.   (10)
```

This conclusion is at the degree-compatible full-row level.  It is not a
sharpness theorem inside the common-shore matching-sum sensor image.

## 3. Two outside controls

Start every construction with

```text
Gamma_(c,c,c),empty = x_c y_c r_c,       c=0,1,2,   (11)
```

and all other entries zero.  A displayed row below replaces the entire base
row from (11).

Fix `a in {1,2}`.  Replace the four rows shown here:

```text
row       Gamma_xy  Gamma_xr  Gamma_yr  Gamma_empty

(a,a,a)     r_0        0         0           0
(0,0,1)    -r_0        0         0       x_a y_a r_a
(0,1,0)      0        y_0        0           0
(1,0,0)      0         0        x_0          0.      (12)
```

The Cramer solution on these rows is

```text
f_xy=(r_a/r_0)x_a y_a,
f_xr=f_yr=0,
f_empty=1.                                           (13)
```

Indeed the first row gives the `a`-th diagonal GHZ target, the second row
cancels to zero, and the last two rows force the zero pair components.  All
unlisted rows satisfy (6) by (11).  The selected determinant is

```text
beta=r_0 r_a x_0 x_a y_0 y_a !=0                    (14)
```

up to the harmless sign determined by row ordering.  Hence `Gamma` has
column rank four.  Among (9), the only nonzero derivative is

```text
partial_(r,a) f_xy=x_a y_a/r_0.                     (15)
```

This gives both outside controls.

## 4. Three controls at each endpoint

Fix `1<=a<=b<=2`.

### The `x`-endpoint control

Replace the following rows of (11):

```text
row       Gamma_xy  Gamma_xr  Gamma_yr  Gamma_empty

(0,0,1)     r_a        0        -x_b          0
(a,a,a)      0         0         x_0          0
(0,0,0)      0         0          0       x_0 y_0 r_0
(0,1,0)      0        y_0         0           0.     (16)
```

Then

```text
f_xy=(x_a x_b/x_0)y_a,
f_xr=0,
f_yr=(x_a/x_0)y_a r_a,
f_empty=1.                                           (17)
```

The first row is the exact cancellation

```text
r_a f_xy-x_b f_yr=0,                                (18)
```

the second row gives `J_(a,a,a)`, and the third row supplies the normalized
`c=0` target.  The selected determinant is

```text
beta=r_0 r_a x_0^2 y_0^2 !=0                       (19)
```

up to sign.  Every retained derivative in (9) vanishes except

```text
partial_(x,a)^2 f_xy=2y_a/x_0       if a=b,

partial_(x,a)partial_(x,b) f_xy=y_a/x_0
                                      if a<b.        (20)
```

The auxiliary `yr` component in (17) carries the radial quotient that the
old selected-only control placed in the empty component.  This is what makes
empty normalization compatible with the endpoint Hessian control.

### The `y`-endpoint control

Use instead

```text
row       Gamma_xy  Gamma_xr  Gamma_yr  Gamma_empty

(0,0,1)     r_a       -y_b       0           0
(a,a,a)      0         y_0       0           0
(0,0,0)      0          0        0       x_0 y_0 r_0
(0,1,0)      0          0       x_0          0,      (21)
```

with

```text
f_xy=x_a(y_a y_b/y_0),
f_xr=x_a(y_a/y_0)r_a,
f_yr=0,
f_empty=1.                                           (22)
```

Now `r_a f_xy-y_b f_xr=0`, the determinant is
`-r_0 r_a x_0^2 y_0^2`, and the sole nonzero coordinate in (9) is

```text
partial_(y,a)^2 f_xy=2x_a/y_0       if a=b,

partial_(y,a)partial_(y,b) f_xy=x_a/y_0
                                      if a<b.        (23)
```

Equations (20) and (23) give all six endpoint controls.  Together with
(12)--(15), they prove Theorem 1.

## 5. Exact proof-topology consequence

The S2L selected controls omitted two layers: the unused target rows and
empty normalization.  Their exact matrices cannot simply be row-extended,
because their already unique Cramer solutions have empty component `0`,
`x_a/x_0`, or `y_a/y_0`.  Theorem 1 instead supplies new controls imposing
both layers simultaneously, preserves all `27` GHZ target rows, and retains
coordinatewise sharpness for the chosen pair.  Therefore neither layer, nor
their combination with rank and column degrees, can by itself supply the
missing target-specific pair-jet forcing.

The nearest remaining bridge is now explicit:

```text
degree-compatible full-row Cramer system             PROVED HERE;
common-shore companion matching-sum realization      OPEN;
universal failure on every realized target incidence OPEN.         (24)
```

No claim is made that the matrices (12), (16), or (21) satisfy all polynomial
relations among companion columns imposed by common physical shore blocks.
Conversely, no nonrealizability theorem for those matrices is proved.  The
construction also does not require the auxiliary pair in (17) or (22) to
pass its own pair-pole gate.  At `m=3` there is no higher even-subset
Euler--hafnian recurrence; this low-order fact does not globalize the
controls to arbitrary `m` or to the original conjecture.

The all-balanced rank-drop branch and every unrelated proof-DAG leaf retain
their previous status.  Global Krenn--Gu remains **UNRESOLVED**.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_full_sensor_cramer_pair_empty_normalization_control_compatibility.py
python claims/arbitrary-order/audit_balanced_full_sensor_cramer_pair_empty_normalization_control_compatibility.py
python -m py_compile claims/arbitrary-order/verify_balanced_full_sensor_cramer_pair_empty_normalization_control_compatibility.py claims/arbitrary-order/audit_balanced_full_sensor_cramer_pair_empty_normalization_control_compatibility.py
uv run --with ruff ruff check claims/arbitrary-order/verify_balanced_full_sensor_cramer_pair_empty_normalization_control_compatibility.py claims/arbitrary-order/audit_balanced_full_sensor_cramer_pair_empty_normalization_control_compatibility.py
```

The primary verifier uses SymPy to build every `27 x 4` matrix, check all
target rows, compute each selected Cramer determinant and solution, verify
column multidegrees, and differentiate the chosen pair component.  The
independent audit imports neither SymPy nor repository code; it rebuilds the
eight systems in a separately written exact Laurent-polynomial model and
checks the same theorem through direct row identities, Leibniz determinants,
and exact exponent differentiation.
