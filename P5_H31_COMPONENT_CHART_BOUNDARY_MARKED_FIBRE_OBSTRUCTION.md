# Complete marked-fibre obstruction on the nonzero component-chart divisor

## Status

This is an exact characteristic-zero obstruction.

The preferred four-Grassmannian chart of the known pure rank-two
component has one nonzero divisor outside the finite five-parameter
family.  The earlier theorem
[`P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md`](P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md)
excluded one canonical marked row section of that divisor.

The complete marked-basis fibre is now excluded.  For every plane tuple
on the divisor, every kernel-row shift, every distinguished source
coordinate `q=0,1,2,3`, and every binary `Delta_2` extension direction,
a neighbouring one-marked map is injective in a mode with a transverse
pure coordinate.  Hence no point of the divisor lifts to `H31`.

This theorem concerns one divisor in one known component chart.  The
first-plane Schubert line at infinity and internal `E=0` toric divisor
have since been closed separately.  A second diagonal-quadric
pure-compression component now exists and lies outside this theorem.

## Normalization and full row-basis fibre

Start with the boundary normal form from the canonical theorem, with

```text
A H N !=0,   R arbitrary.
```

The diagonal source action

```text
diag(N,N,1,1/H)                                      (1)
```

followed by nonzero row rescalings sends

```text
(A,H,N,R) -> (A/N,1,1,R).                            (2)
```

It sends the four row-shift coordinates bijectively to

```text
(t_0,t_1,t_2,t_3)
    -> (t_0,N t_1,t_2/N,t_3/(HN)).                   (3)
```

Thus no marking is lost by writing `H=N=1` and retaining `A!=0`.
Use canonical pure-colour rows

```text
alpha_0=(1,0,A,A-1),
alpha_1=(0,0,1,1),
alpha_2=(0,1,0,R),
alpha_3=(1,0,1,0),                                   (4)
```

and kernel rows

```text
U_0=(0,1,0,-R),
U_1=(R,1,-R,-R),
U_2=(-1,0,1,0),
U_3=(0,0,-1,1).                                      (5)
```

The pure restriction has only

```text
coefficient(alpha alpha alpha alpha)=2A.             (6)
```

The pure tensor fixes the line `C beta_i` in each plane.  Up to row
rescaling, every marked basis over the same plane is therefore

```text
alpha_i=U_i+t_i beta_i,       t in C^4.              (7)
```

## Exact binary incidence

For distinguished coordinate `q`, append extension entries

```text
z=(x_0,x_1,x_2,x_3;y_0,y_1,y_2,y_3)
```

after deleting `q`.  Let `M_q(t)z=0` be the fourteen mixed binary
coefficients and let `d_0(z),d_1(z)` be the two diagonal coefficients.
Saturate by

```text
A d_0(z)d_1(z) !=0                                   (8)
```

and eliminate `z`.  Absolute elimination over `Q` gives:

```text
q=0:
  < t3, t2, t0*t1, R*(R*t1+A-1), R*t0*(A-1) >;

q=1:
  < t3, t2, t1, 2*R*t0-A+1, (A+1)*t0, A^2-1 >;

q=2:
  < t3, t2, t1, R*t0*(A-1) >;

q=3:
  < t2, t1, t3*(A-t3+1), t3*(R*t0+1),
    R*t0*(A+1)+t3 >.                                 (9)
```

These are complete Zariski projection closures.  Their components are
only coordinate axes and linear hypersurfaces; no ambient-map or
Grassmannian enumeration is involved.

## Selected-minor obstruction

For mode `i`, let `p_i` be the distinguished column of the pure
one-marked map and let `N_i(z)` be the neighbouring one-marked map.
A ternary lift necessarily satisfies

```text
(entry of p_i) * (every 4-minor of N_i(z))=0.         (10)
```

The following selected minors suffice, with rows numbered
`000,001,...,111` as `0,...,7`:

| `q` | selected `(mode; rows)` |
| ---: | --- |
| 0 | `(2;0237)`, `(2;0367)`, `(2;0267)`, `(0;0457)` |
| 1 | `(0;0357)`, `(0;0457)` |
| 2 | `(2;0237)`, `(2;0367)`, `(2;0267)` |
| 3 | `(2;0237)`, `(2;0367)`, `(0;0457)` |

The components of (9) split into fourteen elementary certificate
strata.  On each stratum, write an arbitrary extension in an exact
basis of `ker M_q`.  Every selected determinant factors as

```text
d_0(z)d_1(z) ell(z),                                 (11)
```

where `ell` is a nonzero parameter multiple of `d_0` or `d_1`.
The only rational-basis exceptional values are

```text
R t0=-1  for q=0,3,
R t0= 1  for q=2.                                    (12)
```

They are checked in separate denominator-free kernel bases and obey
the same residual identities.  The branch factors are among

```text
1, R, 1/R, -2R, -R^2 t0,                             (13)
```

and the stated branch conditions make the chosen factor nonzero.
Consequently

```text
A d_0(z)d_1(z)!=0
  ==> some selected mode has p_i!=0 and rank N_i(z)=4. (14)
```

Equivalently, adding the products
`(entry of p_i)*(selected minor)` to the saturated binary incidence
gives the unit ideal in each orientation.  The primary verifier uses
the smaller factor ledger rather than making Gröbner elimination
rediscover the elementary branch decomposition.

The third target row at the selected mode must vanish on the
neighbouring hyperplane because `N_i(z)` is injective, and must vanish
on the remaining pure coordinate because `p_i!=0`.  It therefore
vanishes globally, contradicting rank three.  This proves the theorem.

## Verification

Run:

```text
python verify_p5_h31_component_chart_boundary_marked_fibre.py
python audit_p5_h31_component_chart_boundary_marked_fibre.py
```

Regenerate the four saturated projection ideals with:

```text
python derive_p5_h31_chart_boundary_marked_fibre_elimination.py q --run
```

The primary verifier checks the normalization, reconstructs all
permanent matrices, reruns (9), and verifies every kernel and residual
factor in the fourteen-stratum ledger over characteristic zero.  The independent
audit exhausts (9) over `F_5` and `F_7`, computes every modular mixed
kernel, enumerates every projective binary extension direction, and
tests the selected minors directly.

The finite-field audit is exceptional-stratum QA; the unit ideals are
the characteristic-zero proof.
