# Hostile review of star--triangle exceptional companion propagation

## Verdict and exact scope

**PASS, for the stated displayed-frame, characteristic-zero incidence
theorem.**  The support-one/support-two quotient argument, active-colour
step, distinct-mode contraction legality, exact companion tables, reverse
cycles, residual-covector matroids, full second-contraction formula, and
scalarization countermodel all survived independent hostile review.

The result is deliberately a propagation theorem, not an exclusion.  It
shows that every exceptional low kernel occurrence in either displayed
frame forces a companion occurrence in another local mode, with disjoint
local colour support and zero value under all five double-contracted
sensors.  Those incidences close into allowed mutual cycles.  It does not
prove that a cycle extends to the full target, exclude a star or triangle
extension, normalize an arbitrary member of either unbased orbit, prove
unrestricted `P_6 -> Delta_3` nonrestriction, or resolve the prize problem.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed frozen package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_THEOREM.md
  verify_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py
  audit_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py
```

Load-bearing committed predecessors replayed in this review:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_STAR_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  ARBITRARY_PERMANENT_TRIANGLE_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
```

## 1. All-support quotient propagation

Let

```text
Q_p=span{B_zp:z=m_1,m_2,d_0,d_1,d_2},
H_p=ann_R(Q_p),
d=dim Q_p>=2.
```

Suppose, contrary to the propagation claim, that each of the other three
local planes misses `H_p`.  Quotienting by `H_p` embeds each of their
independent triples into

```text
W=D direct-sum A,       D=R/H_p,       dim W=d+2.
```

For fixed vectors of different colours in two modes, the map from `W` to
`D` obtained from

```text
C(y,z,w)=r(y)J(a(z),a(w))+r(z)J(a(y),a(w))
                         +r(w)J(a(y),a(z))
```

kills the embedded three-space from the third mode.  Its rank is therefore
at most

```text
(d+2)-3=d-1.
```

On the `D` summand it is scalar multiplication by the corresponding
`J`-pairing.  A nonzero scalar would have rank `d`, so every cross-colour
pairing between distinct modes is zero.  This is the only dimension gate;
it is valid for both residual ranks occurring in the tables, `d=2` and
`d=3`.

If `supp(p)` is a singleton, a nonzero surviving diagonal contains a
nonzero same-colour pairing after permuting the three remaining modes.
For each of the two off-colour vectors in the third mode, cross-colour
orthogonality and the zero tensor value force the `D` part to vanish.  Both
vectors then lie in the same one-dimensional `J`-orthogonal line in `A`,
contradicting independence of that local triple.

If `supp(p)` has size two, both supported colours are active.  The exact
two-dimensional active-colour lemma makes every `A`-column at the third
colour zero in all three remaining modes.  In the original, uncontracted
pure target at that third colour, only the removed mode can then supply an
`A` factor.  Polarization of `x_4x_5g` requires `x_4` and `x_5` to come from
two distinct tensor slots, so the target coefficient would be zero.  This
contradicts its nonzero `lambda_c`.

The active-colour lemma itself was rederived in both branches.  If every
mode's `A`-columns span at most a line, two differently coloured active
edges in the three-mode graph share an endpoint and contradict
cross-colour orthogonality.  Otherwise one mode contains independent
columns at two colours.  Every outside column at the third colour is
orthogonal to both and vanishes.  If both first colours are active, the two
resulting outside orthogonal lines are distinct, so the third-colour column
in the original mode vanishes as well.  This uses only that `A` is
two-dimensional and `J` is nondegenerate.

Thus some distinct local mode contains a nonzero

```text
q in L_s intersect H_p.
```

No nonzero complementary Gram or pairing matrix is assumed anywhere in
this proof.

## 2. Support disjointness and the single-contraction filter

By definition of `H_p`,

```text
B_zp(q)=0
```

for all five channels.  Since `p` and `q` lie in distinct local modes, the
double contraction is legal.  On the exact target its colour-`c` value is

```text
lambda_c alpha_c beta_c e_c^* tensor e_c^*.
```

The tensor is nonzero and `lambda_c!=0`, so

```text
alpha_c beta_c=0
```

for every colour.  This proves support disjointness directly from the pure
targets; it does not use a scalar `M` entry or assume that such an entry is
nonzero.

Likewise, an exact covector relation

```text
sum_z rho_z B_zq=0
```

gives, after one legal contraction in the mode containing `q`,

```text
sum_c rho_(d_c) lambda_c beta_c e_c^* tensor 3=0.
```

The three coordinate cubes have disjoint support, hence
`rho_(d_c)beta_c=0` separately.  This justifies every support filter used in
the two tables.

## 3. Exact star and triangle tables

Independent contraction and rational row reduction reproduced the star
table:

```text
p                         dim Q_p  H_p                         forced q/support

N=x_1+x_2                    2     span{x_2-x_1,x_1+x_3}      x_2+x_3 / {2}
B_0=x_0+x_2                  3     K(x_2-x_0)                 x_2-x_0 / {0}
C_0=x_0-x_1                  3     K(x_0+x_1)                 x_0+x_1 / {1}
B_1=x_0+x_3                  3     K(x_3-x_0)                 x_3-x_0 / {1}
C_1=x_0+x_1+x_2+x_3          3     K(-x_0+x_1+x_2+x_3)       that line / {0}
```

For the common star plane, writing

```text
q=(0,u,v,u+v)
```

the relation `2B_(m_1)q-B_(d_0)q+B_(d_1)q=0` kills local
colours `0,1`.  The surviving colour-`2` coefficient is nonzero, and

```text
uB_(d_2)q=(u+v)(B_(m_1)q+B_(m_2)q)
```

then forces `u=0`.  No division by an unproved parameter occurs.

The triangle table is:

```text
p                         dim Q_p  H_p                         forced q/support

N=x_1+x_2                    2     span{x_2-x_1,x_3}          x_3 / {0}
B_0=x_0+x_2                  3     K(x_2-x_0)                 x_2-x_0 / {2}
C_0=x_0-x_1                  3     K(x_0+x_1)                 x_0+x_1 / {1}
X=x_3                        2     span{x_1+x_2,x_3}          x_1+x_2 / nonempty subset {1,2}
```

Thus the triangle frame has four distinct starting exceptional directions
`N,B_0,C_0,X`, organized into three undirected mutual cycles.  For `N`, the
relation `B_(d_1)q+B_(d_2)q=0` first leaves only colour `0`, and
`bB_(m_2)q=aB_(d_0)q` forces `a=0`.  Conversely, support disjointness from
`X` kills colour `0`; if the `x_3` parameter were nonzero, the relation

```text
-aB_(d_0)q+b(B_(d_1)q+B_(d_2)q)=0
```

would kill the remaining two coefficients as well.  Hence the reverse
vector lies on `KN`.

## 4. Reverse cycles and covector matroids

The Hessians of all five quadratic cores are symmetric, so

```text
B_zp(q)=B_zq(p)=0.
```

Direct row reduction reproduces the four one-dimensional reverse star
kernels and the two one-dimensional reverse triangle kernels.  The common
reverse kernels are exactly

```text
star:     span{N,x_1+x_3},
triangle: span{N,X}.
```

In the star common plane, disjointness from the colour-`2` companion gives
`beta_2=0`.  Writing the vector as `(0,a+b,a,b)`, the displayed parameter
relation forces `b=0`, leaving `KN`.  The analogous triangle relation also
removes the `X` parameter.  Every reverse use therefore involves two
distinct modes and selects the claimed original direction; no contraction
uses two vectors from one local slot.

The common-cycle residual covectors were also recomputed from the quadratic
cores.  In the star case they have rank three and satisfy

```text
2x_0=h_0-h_1,
```

while in the triangle case they have rank three and satisfy

```text
2x_0=h_1+h_2.
```

In each case the remaining zero-slice residual is a coloop.  This proves
the stated equality of the contracted covector-matroid pattern after the
allowed relabelling and rescaling.  It does not identify the full star and
triangle pair orbits.

## 5. Full second contraction and exact countermodel

For a residual covector `h`, direct expansion of the trilinear form gives,
after inserting `y_b=(r_b,a_b)`, the bilinear tensor on modes `c,d`:

```text
h(r_b) A_c^T J A_d
+ h_c tensor (a_b^T J A_d)
+ (a_b^T J A_c) tensor h_d.
```

This is formula (28), with `M_(cd)=A_c^T J A_d`.  The last two summands
depend on the second contracted vector's `A`-part and do not disappear just
because the earlier vector producing `h` lay in `R`.

The rational scalarization countermodel is exact:

```text
r_b=0, a_b=x_4;       h(r_c)=1, a_c=0;
r_d=0, a_d=x_5.
```

Then the full value is `J(x_4,x_5)=1`, whereas the scalar-only term is
`h(r_b)J(a_c,a_d)=0`.  This refutes only the proposed algebraic shortcut;
it is not presented as a full target extension or a counterexample to the
conjecture.

## 6. Field, independence, and computational replay

The written propagation proof is field-linear in characteristic zero.  It
uses finite-dimensional rank, nondegeneracy of `J`, the exact nonzero target
scalars, and `2!=0` in the displayed matroid identities.  It does not use
order, positivity, algebraic closure, numerical approximation, or any
finite-field-to-characteristic-zero inference.

The final current-byte replay passed at base commit
`985f1a4cd49508da067ba1b4d788b2e576368448`:

```text
star--triangle companion primary verifier:             PASS;
star--triangle companion independent no-import audit:  PASS;
star kernel-boundary primary and audit:                 PASS;
triangle kernel-boundary primary and audit:             PASS;
py_compile on the two reviewed Python files:            PASS;
Ruff on the two reviewed Python files:                  PASS.
```

The primary verifier uses SymPy to reconstruct the quadratic cores,
Hessians, ranks, kernels, parameter identities, cycles, matroids, and
countermodel.  The independent audit imports neither SymPy nor the primary
verifier.  It separately enters the edge Hessians, uses `Fraction` row
reduction, and checks the identities and tables directly.  Its exhaustive
projective scans over `F_3,F_5,F_7` are finite stress checks of the displayed
case tables only; the written quotient argument is the characteristic-zero
proof.

## 7. Accepted boundary

```text
support-one exceptional low propagation:                 PROVED;
support-two exceptional low propagation:                 PROVED;
distinct companion mode:                                 PROVED;
companion ambient line/plane and local support:           CLASSIFIED;
all displayed arrows mutually sensor-orthogonal:          PROVED;
reverse line selection and mutual cycles:                 PROVED;
shared common-cycle covector matroid:                     PROVED LOCALLY;
scalar-only second-contraction replacement:               REFUTED EXACTLY;
same-mode or distinct-mode cycle exclusion:               OPEN HERE;
full star or triangle extension exclusion:                NOT PROVED HERE;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

## Final reviewed hashes

```text
companion-propagation theorem:
9C70842573B3DD02BE5AC9CC65B08047AF0C6877892EA816A5D89B2024ED36A3

primary verifier:
97177FE5D7A44821428AAED34707FAD30490D50D80163609A28FB3AE7BE663F0

independent audit:
9DB62582D752C85F2E7AE8343EC806B95786C5693466ECFB3666C5F838A35289

star kernel-boundary theorem:
2B44641806EEE9B14D2F9DCC692C2E8E1CB9917832A9C2FD9E658243ACFE51F5

triangle kernel-boundary theorem:
60858DFE1C1C9E11C74662B815E1A4173616C3277E28A25520EDAD97148EBA82
```
