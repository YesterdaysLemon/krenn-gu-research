# Generic weighted `H22` obstruction on component twenty-four

## Status

**Exact characteristic-zero function-field theorem.**  The complete generic
weighted `H22` fibre of the split-center mixed-star component (component
twenty-four) is empty over `K=C(k,s,t)`.

The two contraction directions `D01` and `D23` are treated as distinct pair
orbits.  Each is checked in the finite homogeneous-weight chart
`[lambda:1]` and directly at `[1:0]`.  Exact projection gives one branch for
each `D01` chart, two branches for each `D23` chart, and the fixed one-marked
minor `N0[0137]` excludes every saturated binary extension on all six
branches.

This is only a theorem over the generic point of component twenty-four.
Special parameter divisors, projective component-boundary fibres, component
exhaustiveness, and the arbitrary-order local-to-global reduction remain
open.  The global Krenn--Gu conjecture remains **UNRESOLVED**.  No
finite-field computation is used as proof.

## Generic component basis

Put

```text
A=(1,1,0,0), C=(1,-1,0,0),
B=(0,0,1,1), D=(0,0,1,-1),
c=(t-ks)/(1-kst).
```

Over `K=C(k,s,t)`, use

```text
alpha=(A,
       A+kD,
       A+cC+kB-kD,
       D),

beta =(B,
       B+sC,
       C,
       tA+C-ktB).                                  (1)
```

Only the all-beta pure coefficient is nonzero:

```text
T_1111=4(kst-1).                                   (2)
```

Mark by `beta_i -> beta_i+h_i alpha_i`, and adjoin the common extension

```text
z=(x0,x1,x2,x3;y0,y1,y2,y3).                      (3)
```

For direction `D01`, the finite and infinite maps are

```text
(v,e) -> (lambda v0+v1,v2,v3,e),
(v,e) -> (v0,v2,v3,e),                             (4)
```

while for `D23` they are

```text
(v,e) -> (v0,v1,lambda v2+v3,e),
(v,e) -> (v0,v1,v2,e).                             (5)
```

For each case let `M` be the fourteen-row mixed matrix and `a,b` its
all-alpha and all-beta diagonal rows.  Genuine binary incidence is encoded
without ideal quotients by

```text
Mz=0,       az=1,       u(bz)=1.                   (6)
```

Direct row-module reduction shows that neither `a` nor `b` lies in the mixed
row module in any of the four direction/chart cases.  Thus no case is lost
to a premature row-module obstruction; exact saturated projection is
required.

## The `D01` pair orbit

In the finite chart, eliminating `z,u` from (6) gives exactly

```text
J_01^fin=<h3-kt,h2,h0>.                            (7)
```

Thus `h=(0,H,0,kt)`, with both `H` and `lambda` free.  After this substitution,
adjoining

```text
det N0[0,1,3,7]                                    (8)
```

to (6) gives the unit ideal over `K[H,lambda]`.

At weight infinity, projection gives the single prime

```text
J_01^inf=<h3-kt,h2,
           k(t-1)h1+2kst-t-1,h0>.                 (9)
```

This is the marked-`H31` deletion-1 branch

```text
h=(0,(t+1-2kst)/(k(t-1)),0,kt).                   (10)
```

A fresh contraction calculation, rather than inference from the finite
chart, again makes (6) plus (8) the unit ideal.  Hence the entire `D01` pair
orbit is excluded.

## The finite `D23` pair orbit

The finite projection has a seven-element standard basis.  Its radical has
exactly two prime components.  One is the linear branch

```text
P_lin=<h3-kt,h2,kh1+1,h0>,                        (11)
```

so `h=(0,-1/k,0,kt)` and `lambda` is free.

For the second branch define

```text
F = (k^3 s^3 t+k^2 s^2-kst-1) lambda^2
  + (-4k^3 s^3 t-2k^2 s^2 t^2-2) lambda
  + 3k^3 s^3 t+2k^2 s^2 t^2+3k^2 s^2+kst-1,

G3 = 2s(k^2s^2-1)h3
   + (k^4s^4t^2-k^2s^2t^2-k^2s^2+1)lambda
   - 3k^4s^4t^2-2k^3s^3t^3+4k^3s^3t
   + k^2s^2t^2+k^2s^2-2kst+1,

G2 = k(t^2-1)(kst+1)h2+(kst-1)h3+kt(1-kst),

G1 = (1-k^2s^2)h3 lambda+2k^3s(t^2-1)h1
   + (k^2s^2+2kst+1)h3
   + k(k^2s^2t-t)lambda+k(-k^2s^2t-2ks-t).        (12)
```

Then the second prime is

```text
P_quad=<F,G3,G2,G1,h0>.                            (13)
```

`F` is irreducible over the generic component field, so this is a genuine
quadratic-weight branch rather than two silently adjoined square-root
branches.  Exact bidirectional reductions identify the projected radical
with `P_lin intersect P_quad`.

On `P_lin`, (6) plus (8) is the unit ideal.  On `P_quad`, adjoining all five
generators (13) and the same fixed minor (8) also gives the unit ideal over
`K`.  The latter is the decisive quadratic-branch calculation; rational
roots used during minor reconnaissance are not used in the proof.

## `D23` at weight infinity

Direct infinity projection gives the two primes

```text
P_3a=<h3-kt,h2,kh1+1,h0>,

P_3b=<h3-kt,
       2t(k^2s^2-1)h2+k^2s^2t^2-1,
       h1-st,h0>.                                  (14)
```

They are exactly the two deletion-3 marking branches from the verified
generic marked-`H31` theorem, but the verifier reconstructs the infinity
contraction directly.  Substituting

```text
h_3a=(0,-1/k,0,kt),

h_3b=(0,st,-(k^2s^2t^2-1)/(2t(k^2s^2-1)),kt)      (15)
```

makes (6) plus (8) the unit ideal on each branch.

## Theorem and boundary

Every genuine binary candidate in either weighted pair orbit and either
homogeneous weight chart makes `N0[0137]` nonzero.  Its mode-zero one-marked
ternary map therefore has rank four, so it cannot lift to weighted `H22`.
Consequently the generic weighted-`H22` fibre of component twenty-four is
empty.

The proof is over `C(k,s,t)`.  Factors such as `k`, `t`, `t^2-1`,
`k^2s^2-1`, and `kst-1` are units only at the generic point.  Their special
fibres are not claimed here.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/split-center-mixed-star/verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py
uv run --with sympy python claims/p5/h22/split-center-mixed-star/audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py
python -m ruff check claims/p5/h22/split-center-mixed-star/verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py claims/p5/h22/split-center-mixed-star/audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py
python -m py_compile claims/p5/h22/split-center-mixed-star/verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py claims/p5/h22/split-center-mixed-star/audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py
```

The primary verifier works over the exact function field, reconstructs all
four projections and six branch unit ideals, and separately records the four
row-module tests.  The independent no-import audit uses subset-DP permanents
and exact rational specializations to corroborate both roots of the
quadratic branch; those specializations audit but do not replace the generic
proof.
