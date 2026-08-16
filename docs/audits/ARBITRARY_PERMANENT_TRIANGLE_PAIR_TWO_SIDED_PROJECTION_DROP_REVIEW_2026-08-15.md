# Hostile review of the triangle-pair two-sided projection-drop theorem

## Verdict and exact scope

**PASS, for the displayed `(3,1)` triangle frame, pointwise,
characteristic-zero, full-`Delta_3` scope.**  No mathematical,
case-exhaustiveness, dependency, characteristic, or implementation blocker
survived hostile review.

For this explicit pair, every exact `P_6 -> Delta_3` extension has a
rank-at-most-two mode in each of the two mixed-factor projection families:

```text
min_t rank(Phi_1|L_t) <= 2,
min_t rank(Phi_2|L_t) <= 2.
```

The proof is genuinely asymmetric.  The `Phi_2`-full direction reduces to
a one-dimensional common kernel and the familiar low-mode split.  The
`Phi_1`-full direction has a two-dimensional ambient kernel, but injectivity
of `Phi_1` normalizes each low kernel line to `K(x_3+sN)` and exposes a fixed
noncoordinate high hyperplane.  The three-low case in that direction is a
new load-bearing branch and was reviewed separately below.

The theorem does not exclude the residual where both families already have
rank-drop modes.  It does not transport automatically to every based frame
inside the unbased `(3,1)` orbit, and it does not classify active-support-five
or active-support-six equality-five pairs.  It is not an unrestricted
permanent nonrestriction theorem.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_TRIANGLE_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md
  verify_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py
  audit_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py
```

The load-bearing predecessors replayed were the exact `r=4` equality-five
pair-orbit classification and the fixed-pair two-sided package supplying an
independent implementation of the hyperplane-plane and HHPP geometry.

## 1. Pair algebra and full target

Independent square-free multiplication reproduced the displayed product
table

```text
(u_i v_j)= [ d_0   m_1   m_2 ]
            [-m_2  d_1    0  ]
            [ m_1  -m_1  d_2 ].
```

The five elements `(m_1,m_2,d_0,d_1,d_2)` are independent.  All mixed
products lie in `M=span{m_1,m_2}`, and the three diagonal classes complement
`M`.  This matches the explicit Delta-admissible `(3,1)` frame in the
pair-orbit predecessor; no normalization from the inequivalent `(4,1)` or
`(4,2)` pairs is assumed.

Edge complementation gives exactly

```text
F_1=x_4x_5 x_3 ell_1,
F_2=x_4x_5 x_0 ell_2,

D_0=2x_4x_5 x_0x_3,
D_1= x_4x_5 x_2(x_0+x_1),
D_2= x_4x_5 x_1(x_0-x_2),

ell_1=x_2-x_1-x_0,
ell_2=x_2-x_1.
```

Thus `F_k` is the pullback of the four-variable permanent through

```text
Phi_1=(x_3,x_4,x_5,ell_1),
Phi_2=(x_0,x_4,x_5,ell_2).
```

The mixed target equations make both permanent tensors identically zero,
while the three pure sensors are nonzero diagonal fourth powers.  Every
profile argument is applied to the actual image subspaces, onto which the
restricted local maps are surjective.

## 2. Hyperplane/plane profile classification

The profile lemmas were re-derived over an arbitrary characteristic-zero
field.  For hyperplanes `H_alpha,H_beta` in a four-space, the annihilator of
their square-free quadratic product is represented by symmetric
zero-diagonal forms.

If the normals are independent and `H_0=H_alpha intersect H_beta`, any such
form kills `H_0` and descends to the two-dimensional quotient.  Vanishing
on the two distinct quotient lines removes the cross coefficient, so the
form is

```text
c alpha alpha^T+e beta beta^T.
```

The zero-diagonal subspace has dimension at most two; hence
`dim(H_alpha H_beta)>=4`.  If the normals are proportional to `alpha`, the
annihilator consists of `alpha z^T+z alpha^T`.  Its zero-diagonal equations
give

```text
dim(H_alpha H_alpha)=2+|supp(alpha)|.
```

Therefore the minimum three occurs exactly when both hyperplanes are the
same coordinate hyperplane `W_i`, whose product is `W_i^2`.

For a hyperplane `H=ker(alpha)` and plane `P`, the annihilator condition is

```text
C(P) subset K alpha.
```

The exact Pluecker-chart rank split gives `dim(HP)>=3`, with equality only
in the following cases:

```text
A. H=W_i and P subset W_i;

B. H=span{z_k,z_l,z_i+t z_j},
   P=span{z_k,z_l},
   t!=0.
```

The containment implication

```text
HP subset W_i^2  =>  H=W_i and P subset W_i
```

follows directly from the missing `z_i z_j` coefficients.  Pairing product
spaces under edge complementation then gives the exhaustive zero-permanent
profiles:

- four hyperplanes must be one coordinate hyperplane;
- three hyperplanes and one plane must share a coordinate hyperplane;
- two hyperplanes and two planes either share a coordinate hyperplane or
  form the unique opposite-parameter family `H(t),H(-t),P,P`.

In the last case, direct and crossed pairings are both required.  They make
the two planes equal to the unique complementary coordinate plane and force
the high parameters to be opposites.  Since `2t!=0`, the exceptional high
hyperplanes are distinct.

## 3. Common-factor sensor table

Exact full-monomial extraction gives the complete double common-factor
rank table

```text
                         g
                  x_0   x_4   x_5   ell_2
f       x_3        1     0     0      2
        x_4        0     0     0      0
        x_5        0     0     0      0
        ell_1      1     0     0      1.
```

Every cell has sensor rank at most two.  If all four local planes lie in
one such common kernel, the three constant-colour products nevertheless
induce three independent functionals on the five-dimensional pair-product
space.  This is a valid rank contradiction.  The proof uses the ambient
common-factor product space only as an upper bound on the actual local
sensor and does not silently reverse containment.

The single-factor observations are also exact: common omission of either
`x_3` or `x_0` kills `D_0`.

## 4. Excluding four full `Phi_2` ranks

Assume all four `Phi_2` restrictions have rank three.  The zero tensor
`F_2` forces a common omitted factor.  Missing `x_4` or `x_5` kills every
pure sensor, and missing `x_0` kills `D_0`; hence all four local planes lie
in `ker(ell_2)`.

On this hyperplane, the kernel of `Phi_1` is exactly

```text
K N,  N=x_1+x_2.
```

A secondary `Phi_1` image is therefore a hyperplane or plane, with the
plane case occurring exactly when the local mode contains `N`.  Calling
these modes low, all possible counts are exhausted as follows:

```text
low count   disposition
0           common coordinate cell, sensor-rank contradiction
1           common coordinate cell, sensor-rank contradiction
2           common cell or exceptional HHPP family
3           impossible by N contractions
4           impossible by N contractions
```

At a low mode write `N=sum_c alpha_c y_c`.  The single contraction
`i_N D_0=0` forces `alpha_0=0`.  At two distinct low modes,

```text
i_N i_N D_0=0,
i_N i_N D_1= 2J,
i_N i_N D_2=-2J,

J(y,z)=x_4(y)x_5(z)+x_5(y)x_4(z).
```

The last two ambient tensors are negatives, while their target supports are
the distinct colour entries `(1,1)` and `(2,2)`.  Both must vanish, giving

```text
alpha_(s,1)alpha_(t,1)=0,
alpha_(s,2)alpha_(t,2)=0.
```

With at least two lows, every nonzero support is a singleton in `{1,2}` and
any pair uses different labels.  Three or four lows are impossible.

With exactly two lows, normalize them at colours `1` and `2`.  The common
coordinate HHPP branch returns to the table.  In the exceptional branch,
contracting the full target in those two differently coloured slots gives

```text
J(H_+,H_-)=0.
```

The rank-two form `J` has radical equal to the plane spanned by the two
factor coordinates other than `x_4,x_5`.  Two mutually `J`-orthogonal
hyperplanes must both contain the radical.  Their exceptional intersection
is the common low plane, which therefore equals the radical.  The two low
original planes have `x_4=x_5=0`; the two high modes would need to supply
those common factors, but their two assignments sum to the already-zero
`J`.  Every pure sensor vanishes, a contradiction.

This closes every rank profile in the `Phi_2`-full direction.

## 5. Excluding four full `Phi_1` ranks

Assume all four `Phi_1` restrictions have rank three.  The zero tensor
`F_1` forces all local planes into `ker(ell_1)`: missing `x_4` or `x_5`
kills all pure sensors, while missing `x_3` kills `D_0`.

On `ker(ell_1)`, one has `x_2=x_0+x_1` and `ell_2=x_0`.  Because
`Phi_1|L_t` is full rank and its `ell_1` coordinate vanishes, the three
covectors `(x_3,x_4,x_5)` form a basis of `L_t^*`.  In particular `x_4,x_5`
are independent on every local plane, so every `Phi_2` image has dimension
at least two.

All `Phi_2` images lie in the fixed noncoordinate hyperplane

```text
bar H={z_3=z_0},
(z_0,z_1,z_2,z_3)=(x_0,x_4,x_5,ell_2).
```

A high image is exactly `bar H`; a low image is a plane.  The ambient kernel
on `ker(ell_1)` is

```text
ker(Phi_2)=span{N,x_3},  N=x_1+x_2.
```

The local kernel line cannot equal `KN`, because `Phi_1|L_t` is injective
and `Phi_1(N)=0`.  It therefore has a unique normalized generator

```text
K_t=x_3+s_tN.
```

For two low modes, exact double contraction gives

```text
i_(K_s)i_(K_t)D_0=0,
i_(K_s)i_(K_t)D_1= 2s_s s_t J,
i_(K_s)i_(K_t)D_2=-2s_s s_t J.
```

Writing `K_t=sum_c alpha_(t,c)y_(t,c)`, the zero `D_0` contraction handles
colour zero.  The last two ambient tensors are negatives with disjoint
target supports, so all three colours satisfy

```text
alpha_(s,c)alpha_(t,c)=0.
```

Distinct low-kernel supports are pairwise disjoint.  This immediately
excludes four low modes.  The remaining counts were attacked separately:

```text
low count   disposition
0           four copies of noncoordinate bar H, impossible
1           three copies of bar H plus a plane, impossible
2           common-coordinate or distinct-high HHPP branches, impossible
3           contraction/radical argument below
4           impossible by disjoint nonempty supports
```

For zero or one low, the profile corollary would make `bar H` coordinate.
For two lows, the common-coordinate branch does the same, while the
exceptional branch requires two distinct high hyperplanes and therefore
cannot have both highs equal to `bar H`.

With exactly three lows, their nonempty pairwise-disjoint supports are the
three singleton colours `0,1,2`.  If `s_t=0`, then `K_t=x_3`.  Since

```text
i_(x_3)D_1=i_(x_3)D_2=0,
```

the nonzero diagonal target prevents this kernel from having colour `1` or
`2`.  Thus the colour-`1` and colour-`2` kernel parameters are both nonzero.
Apply their double-contraction identity.  The selected colours differ, so
both diagonal target contractions vanish; division by the two nonzero
parameters yields

```text
J(P,bar H)=0,
```

where `P` is the remaining low image and the fourth image is the sole high
`bar H`.

For `J=z_1 tensor z_2+z_2 tensor z_1`, one has

```text
bar H^perp=rad(J)=span{z_0,z_3},
bar H intersect rad(J)=K(z_0+z_3).
```

Since every image, including `P`, lies in `bar H`, the equation
`J(P,bar H)=0` puts the two-plane `P` inside the displayed line.  This is
impossible.  The load-bearing three-low branch is therefore closed, and so
is the entire `Phi_1`-full direction.

## 6. Full-target and characteristic boundaries

The full exact `Delta_3` hypothesis is load-bearing.  Tensor-wide mixed
zeros are needed for the profile classifications.  Single contractions are
identities on all three remaining modes, double contractions compare full
bilinear slices, and both radical arguments use target support separation
outside a bounded Hamming shell.  The result does not establish a
radius-two version.

Characteristic zero is correctly stated.  The proof uses `2!=0`, opposite
exceptional parameters, nonzero `2J`, and division by the nonzero kernel
parameters in the three-low branch.  Odd-prime computations below audit
identities and case structure; the written characteristic-zero arguments
are the proof.

## 7. Computational replay and independence

The primary verifier uses exact SymPy algebra to reconstruct the full pair
table and all five quartics, both asymmetric restricted kernels, the fixed
high hyperplane, every common-factor sensor rank, every `N` and
`x_3+sN` contraction, the exceptional HHPP geometry, and both radical
calculations.

The independent audit imports neither the primary verifier nor SymPy.  It
uses a custom modular reducer, separate square-free multiplication, and
exact rational arithmetic.  Over `F_3` it independently found

```text
HP equality cases:
  coordinate/support-one: 52,
  support-two:             12;

ordered zero HHPP tuples:
  common coordinate:      676,
  opposite exceptional:    12.
```

It also found no zero permanent profile with the fixed noncoordinate high
hyperplane in the `HHHH`, `HHHP`, or `HHPP` cases.  It replayed the variable
kernel contractions over `F_3,F_5,F_7`, exhaustively checked the two- and
three-colour support combinatorics, computed all sixteen sensor ranks over
the rationals, and independently found no plane
`P subset bar H` satisfying `J(P,bar H)=0` over `F_3`.

Focused replay passed:

```text
new primary exact verifier:                      PASS;
new independent no-import audit:                 PASS;
pair-orbit classification primary/audit:         PASS/PASS;
fixed-pair two-sided predecessor primary/audit:  PASS/PASS;
py_compile:                                      PASS;
Ruff:                                            PASS;
git diff --check:                                PASS.
```

The new package was absent from `origin/main` commit
`4efbbd2c4dc364930809cfceb5486268fa3fd00f`.  This is a repository-level
novelty observation only, not an external priority claim.

## 8. Accepted boundary

```text
displayed triangle pair, four full Phi_1 ranks:         EXCLUDED;
displayed triangle pair, four full Phi_2 ranks:         EXCLUDED;
displayed triangle pair, a drop in each family:         PROVED NECESSARY;
Phi_2-full exceptional HHPP branch:                     EXCLUDED;
Phi_1-full three-low branch:                            EXCLUDED;
simultaneous projection-drop residual:                 OPEN;
other based-frame stabilizer orbits of type (3,1):      OPEN;
active-support-five/six equality-five pairs:            OPEN;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

Any integration that changes the live mathematical frontier must update
the canonical frontier and theorem-ledger artifacts under the repository
contract.  This review does not perform that integration.

## Final reviewed hashes

```text
new theorem:
C5E8F47B499318595481D84DB75425240BA6A01AD512A92BF923F5FAB56BF485

new primary verifier:
770F21C2D34A5B98CE5820D023405D0A95B3FE167539747E3EFB9EDE4A538153

new independent audit:
14AB3E48905246452B9B02D962D0D5902D543398EA74B0009ACAF12C720D136D

pair-orbit theorem:
4B7FCCCCF68B55E1DDEACB7328B7469A8A82F36AA2AB0303E9094519A95FC5BC

fixed-pair two-sided theorem:
A383731E094E0D0E45482AAB889FB8B202FC7A2CF452D8534D5035E737089F36
```
