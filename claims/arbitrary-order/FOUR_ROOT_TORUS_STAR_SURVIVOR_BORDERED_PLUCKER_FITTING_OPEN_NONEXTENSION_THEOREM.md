# Four-root torus-star survivor bordered-Pluecker Fitting-open nonextension

## Status

**Exact denominator-free principal-open theorem and intrinsic Fitting-open
reduction (`GLD83`).** Work over `K=Q(i)` and then extend scalars to `C`.
Retain the fixed `GLD70` fully-supported, nonisotropic rank-two maximal-star
interface, the scale-fixed equal-leaf survivor chart of `GLD75`--`GLD82`, and
the complete legal `q_0` first response.

There is an explicit polynomial circuit

```text
Delta_83(F)=Omega(F) det M_Pl(F)                         (1)
```

which is nonzero at the `GLD72` Gaussian frame. On `D(Delta_83)`, every
concise GHZ tensor in the fixed rank-`44` nuisance image and every raw
coefficient preimage fails the legal first-response condition. By `GLD81`,
the same open excludes the named root-order-four, surplus-two,
fully-supported, rank-three, nonisotropic maximal-star source branch.

Unlike `GLD82`, (1) does not divide by or include the selected thirteen-row
quotient pivot `gamma_num`. Its forty-five columns are coefficient vectors of
bordered `15 x 15` Pluecker determinants. The principal open itself forces the
constant mixed block to have rank thirteen, including points where the old
selected pivot vanishes.

The full family of bordered determinants also defines an intrinsic finite
quadratic Fitting open `D(Omega I_Pl)`. It contains `D(Delta_83)` and is
excluded by the same argument. This is an exact finite-cover reduction, not a
claim that this Fitting open exhausts the survivor component or that quadratic
span is necessary for projective emptiness.

The intrinsic residual `V(I_Pl)`, the frame/gauge complement `V(Omega)`,
other survivor components and gauges, rank/support boundaries, triangles,
other root profiles, and the global Krenn--Gu conjecture remain
**UNRESOLVED**.

Owning dependencies are `GLD75`, `GLD80`, `GLD81`, and especially the
[`GLD82` fraction-free quadratic theorem](FOUR_ROOT_TORUS_STAR_SURVIVOR_INVARIANT_QUADRATIC_MACAULAY_PRINCIPAL_OPEN_NONEXTENSION_THEOREM.md).

## 1. Base ring and moving mixed response

Let

```text
X_sf=Spec K[x_0,...,x_14]/(g_0,...,g_9,x_8),
F=(A,G,G,G).
```

Put `B=X_sf`. This is the globally defined equal-leaf subincidence in the
displayed affine frame gauge, not an assertion that it is one irreducible
component or that it exhausts the fixed-star survivor locus. In particular,
unlike the smaller `GLD80` neighborhood, `B` does **not** invert the selected
mixed pivot `gamma_num`. All statements below are restricted to `B`, with
the frame/gauge condition imposed explicitly by `Omega`. Put

```text
d(F)=det(A)det(G)^3,
Omega(F)=delta_gauge(F)d(F).
```

The normalized chart has `delta_gauge=1`; `D(Omega)` retains the frame and
gauge open on which literal-Delta transport represents the original GHZ
frame.

Use the fixed rank-`44` nuisance solve and fixed rank-eight invariant raw
kernel of `GLD82`:

```text
alpha_bar(F;u,s)=s bar(alpha)_0(F)+V_0u,
y=(u_0,...,u_7,s) in P^8.                               (2)
```

Let

```text
U_num=adj(A) tensor adj(G) tensor adj(G) tensor adj(G)
```

and project its outputs to the 78 mixed tensor words. The transported
thirteen-column constant `Q`/eta-residual block and the first three root
columns are

```text
C_F = pi_mix U_num C                    in Mat_(78 x 13)(O_B),
w_r(F;y)=pi_mix U_num H_r(alpha_bar(F;u,s)) in O_B^78,
r=0,1,2.                                                   (3)
```

The inherited target normalization is

```text
U_num(F)R(F)=d(F) Diag,
```

up to the common invertible monomial change of the three displayed response
columns allowed in `GLD80`--`GLD82`.

Every entry in (3) is polynomial in the frame shifts and linear in `y` for
the response columns. No quotient row, response minor, nonzero response
column, or raw coefficient preimage has been selected.

The exact leaf-`S_3` covariance audit of `GLD82` preserves `im C_F` and each
root index separately. On every geometric point where `rank C_F=13`,
Reynolds averaging therefore maps every full affine necessary rank-one
quotient solution to an invariant one of the form (2). Zero columns and
response-rank drops are retained.

## 2. Bordered Pluecker response equations

For a pair `0<=c<d<=2` and any ordered fifteen-element row list `S`, define

```text
P_(S;c,d)(F;y)=det [C_F | w_c(F;y) | w_d(F;y)]_S.        (4)
```

It is a homogeneous quadratic in the nine coordinates `y`. A legal first
response makes the three quotient classes of the root columns proportional
whenever `rank C_F=13`; hence every polynomial (4) vanishes. More generally,
if `rank C_F<13`, every matrix in (4) has rank at most fourteen, so (4) still
vanishes identically. Thus (4) is a denominator-free necessary equation on
every constant-block rank fibre.

There is also a direct response-domain interpretation. The complete legal
domain has thirteen constant and four root coordinates, the four root
columns obey their matching-partition relation, and a legal lift supplies
three independent diagonal directions killed by `pi_mix`. Consequently the
mixed response matrix has rank at most fourteen, so all its bordered
`15 x 15` minors vanish. This agrees with (4) and does not divide by a
constant-block pivot.

## 3. The selected gamma-free principal open

Retain the `GLD82` row partition

```text
I=(0,1,2,3,4,5,7,8,9,11,17,27,53),
J=the ordered complement in {0,...,77}.                  (5)
```

For each of the forty-five `GLD82` descriptors `(p,q,c,d)`, use the ordered
row list

```text
S_(p,q)=(I[0],...,I[12],J[p],J[q])                       (6)
```

in (4). Order the forty-five degree-two monomials in `y` by pairs
`0<=i<=j<=8`, and let `M_Pl(F)` be the `45 x 45` coefficient matrix of these
forty-five bordered quadrics. Equations (2)--(6), together with the explicit
descriptor list in `GLD82`, are a finite polynomial arithmetic circuit for
every entry of `M_Pl` and hence for (1).

The order (6) is used for the exact sign in Section 3. Relative to the
increasing exterior-coordinate basis it may introduce a signed coordinate
functional. Those column signs are units and do not change the selected open
or its membership in the full Fitting ideal.

Let

```text
gamma_num(F)=det (C_F)_I.
```

The fraction-free quotient column of `GLD82` is

```text
Q_num(v)=gamma_num v_J-(C_F)_J adj((C_F)_I)v_I.          (7)
```

Bordered determinant expansion, with the row order (6), gives the polynomial
identity

```text
minor_(p,q)(Q_num(w_c),Q_num(w_d))
 =gamma_num P_(S_(p,q);c,d).                             (8)
```

Although it can be proved on `D(gamma_num)` by the Schur complement, (8) is
first an identity in the ambient frame polynomial ring and therefore holds
everywhere. Restricting it to `O(B)` and any further localization gives

```text
M_ff=gamma_num M_Pl,
det M_ff=gamma_num^45 det M_Pl.                          (9)
```

At `F_0`, `GLD82` proves

```text
d(F_0)=24-24i,
gamma_num(F_0)=-692533995824480256(1+i),
det M_0 !=0,                                             (10)
```

and

```text
M_ff(F_0)=(d(F_0)gamma_num(F_0))^2 M_0.
```

Combining this with (9) gives

```text
M_Pl(F_0)=d(F_0)^2 gamma_num(F_0) M_0,
det M_Pl(F_0)=d(F_0)^90 gamma_num(F_0)^45 det M_0 !=0.   (11)
```

Hence `Delta_83(F_0)!=0`. Moreover

```text
Delta_82=gamma_num^46 Delta_83,                          (12)
```

so `D(Delta_82)` is contained in the gamma-free `D(Delta_83)`. Strict
containment is possible but is not asserted without survivor-divisor
analysis.

### Theorem 3.1 (bordered-Pluecker principal-open nonextension)

The invariant projective response incidence is empty over every geometric
point of `D(Delta_83)` in the declared survivor chart. Consequently every raw
coefficient preimage there fails the complete legal first-response
condition.

#### Proof

If `rank C_F<13`, every selected bordered quadratic is zero, so `M_Pl(F)=0`.
Therefore `det M_Pl(F)!=0` forces `rank C_F=13` without selecting any
particular constant-block pivot.

On that rank-thirteen fibre, suppose a full raw preimage admitted a legal
first response. The intrinsic Reynolds argument gives an invariant affine
solution and hence a projective point `[u:1]`. Every bordered quadratic (4),
in particular the forty-five selected ones, vanishes there.

But `det M_Pl(F)!=0` says that the selected quadrics form a basis of the
forty-five-dimensional space of quadrics in `y_0,...,y_8`. Their ideal
contains every `y_j^2`, so they have no common projective zero. This is a
contradiction. The factor `Omega` makes the moving literal-Delta covariance
legal. `square`

### Corollary 3.2 (physical maximal-star source branch)

No complex Krenn--Gu witness on the `GLD81` root-order-four, surplus-two,
fully-supported, rank-three, nonisotropic maximal-star source branch can have
an induced normalized equal-leaf survivor frame
`F in B intersect D(Delta_83)`.

#### Proof

The forward source bridge in `GLD81`, Theorem 3.1, is the matching identity
before its old `D(delta)` consequence: on the declared invertible port-frame
gauge it sends every such source, its physical raw vector, and its legal lift
to the complete response incidence. It does not require `gamma_num`. `GLD83`
Theorem 3.1 excludes that incidence on the stated
`B intersect D(Delta_83)`.
`square`

## 4. Full intrinsic quadratic Fitting open

Let `E=O_B^78` and `Y=O_B^9`. The thirteen columns of `C_F` give

```text
c_F=C_1 wedge ... wedge C_13 in exterior^13 E.           (13)
```

For each response pair form the vector-valued quadratic

```text
calP_(c,d)(F;y)=c_F wedge w_c(F;y) wedge w_d(F;y)
                in exterior^15 E tensor Sym^2(Y^*).      (14)
```

Taking all coordinate functionals of `exterior^15 E` and all three response
pairs produces a coefficient map

```text
A_Pl(F): (exterior^15 E)^* tensor O_B^3 -> Sym^2(Y^*).   (15)
```

In coordinates it is a `45 x N` matrix, where

```text
N=3 binomial(78,15)=13103742929259840.                   (16)
```

Define the intrinsic quadratic-span ideal

```text
I_Pl=I_45(A_Pl)=Fitt_0(coker A_Pl).                       (17)
```

The coordinate description is enormous but finite and completely indexed;
no generated expansion is claimed as a durable certificate. The displayed
wedge representative and generators depend on ordered bases and may scale by
units. A change of mixed-word basis, constant-block basis, or homogeneous
`Y`-basis (including a recalibration of the invariant raw coordinates)
changes (15) by invertible source or target operations and leaves its
surjectivity and the Fitting-open/vanishing condition unchanged. This basis-
independent condition is the sense in which `I_Pl` is intrinsic.

The selected determinant `det M_Pl` is one maximal minor in (17). Therefore

```text
D(Delta_83) subset D(Omega I_Pl),
D(I_Pl)=union_B D(det A_Pl[:,B]),                         (18)
```

where `B` runs over the finite forty-five-column subsets.

### Theorem 4.1 (full bordered quadratic Fitting-open exclusion)

Over every geometric point of `D(Omega I_Pl)` in the declared survivor
chart, every raw coefficient preimage fails the complete legal first-response
condition. The remaining fixed-chart response obligation is contained in

```text
V(I_Pl) intersect D(Omega).                              (19)
```

#### Proof

At a point of `D(I_Pl)`, the scalar coordinates of the three vector-valued
quadrics (14) span every quadratic in `y`. They therefore have no common
projective zero. Surjectivity also forces `c_F!=0`, hence `rank C_F=13`, so
the Reynolds reduction used in Theorem 3.1 applies. A legal response would
give a common projective zero of all (14), contradiction. `square`

Theorem 4.1 is a sufficient quadratic-span obstruction. It does not say that
a point of `V(I_Pl)` admits a response, nor that every empty quadratic system
has coefficient rank forty-five. Treating (19) requires an exact Fitting
cover, a stronger projective ideal certificate, or an exact surviving lift.

## 5. Residual obligations and hostile controls

The corrected residual alternatives are:

1. the intrinsic bordered quadratic rank-drop locus `V(I_Pl)` in the
   frame/gauge open;
2. `Omega=0` or a different survivor gauge/component; or
3. a lower-rank port, smaller survivor family, maximal triangle, residual
   coordinate boundary, isotropic slope, other root/surplus profile, or
   non-leading source branch.

The old selected equation `gamma_num=0` and the old single determinant
`det M_ff=0` are not treated as intrinsic survivor components. They are
coordinate charts whose complements are absorbed into (14)--(19).

Hostile controls:

- `GLD72` remains an exact concise GHZ tensor in `N_star`; only legal first
  response is excluded.
- The `GLD70` `Q` generator and epsilon are not used as GHZ-membership tests.
- Every raw preimage is retained before the proved Reynolds compression.
- A rank drop of `C_F` makes every bordered equation zero and therefore lies
  outside the Fitting open; it is not divided away.
- Zero response columns and response-rank drops remain inside the bordered
  determinantal equations.
- The homogenizing coordinate `s` retains escape to infinity in `P^8`.
- Frame nonuniqueness is controlled only in the certified
  `GLD75`--`GLD80` gauge.
- The full Fitting open is an exact finite union, not a practical enumeration
  of its roughly `10^16` quadratic columns and not an exhaustive survivor
  theorem.
- The result is fixed-star and first-response only. It is not global
  Krenn--Gu resolution.

## 6. Verification

Run:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_survivor_bordered_plucker_fitting_open_nonextension.py
python -I claims/arbitrary-order/audit_four_root_torus_star_survivor_bordered_plucker_fitting_open_nonextension.py
```

At the exact `GLD72` frame, the primary verifier reconstructs the transported
`78 x 13` constant block and the three moving response maps directly from the
interface builder. It then computes all `2,025` coefficients of the forty-five
selected bordered quadrics through exact Schur complements and compares them
entry-for-entry with the pinned physical `GLD82` certificate and quotient
fingerprint. It also checks the indexing, the Gaussian scaling (9)--(12), and
the full exterior/Fitting dimensions. The standard-library no-import audit
independently recomputes the Gaussian determinant, the gamma-free scaling, the
combinatorial indexing, singular-pivot bordered controls, and the theorem's
scope fences.

The universal polynomial block-determinant identity and the geometric-point
Fitting argument are the written proof; a finite specialization is not
substituted for either. Neither audit materializes the roughly `10^16` columns
of the full map `A_Pl`, and the primary reconstructs the selected moving
circuit only at the exact Gaussian specialization rather than expanding it
symbolically over `B`. That evidence boundary is explicit rather than being
called an independent universal moving-circuit derivation.
