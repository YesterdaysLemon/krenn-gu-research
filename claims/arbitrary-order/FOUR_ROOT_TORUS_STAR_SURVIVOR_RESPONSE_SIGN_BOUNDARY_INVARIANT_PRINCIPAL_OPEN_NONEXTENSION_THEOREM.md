# Four-root torus-star survivor response: sign-boundary invariant principal-open nonextension

## Status

**Exact local principal-open exclusion in the three `GLD77` sign-boundary
charts (`GLD78`).**  Work over `Q(i)` and then extend scalars to `C`.  Retain
the complete canonical `GLD70` fully-supported, nonisotropic rank-two
torus-star interface, the scale-fixed equal-leaf `GLD75` survivor germ, the
complete `35`-dimensional raw fibre, and the legal `q_0` first response.

For each of the three reduced sign-boundary points of `GLD77`, this theorem
defines a regular determinant whose nonvanishing excludes the affine part of
that proportionality chart.  This is an all-order algebraic exclusion on a
named principal open, not merely a tangent calculation.  It closes the three
sign-plane strict-transform entrances near the Gaussian point.  It does
**not** classify boundary points with trivial or standard raw components,
exclude the full survivor neighbourhood, cover other survivor components or
source presentations, prove maximum-root or no-fifth-root statements, or
resolve Krenn--Gu.  The global conjecture remains **UNRESOLVED**.

## 1. Regular moving literal-Delta system

Let `X` be the scale-fixed four-dimensional equal-leaf survivor germ in the
certified `GLD75` frame chart, with Gaussian point `F_0`.  For each moving
frame, conjugate the target to literal `Delta_4` **and transport the complete
interface with it**.  Put

```text
U_F=tensor_(u=0)^3 F_u^(-1),        P'_u=P_u F_u^(-T).
```

Let `b_F` and `D'_F` be the nuisance and complete legal-response maps rebuilt
from the transformed ports.  The induced raw-coordinate map `S_F` acts by an
inverse frame on each residual label and by the corresponding Kronecker
product on each pair label.  Let `J_F` be the invertible response-domain
change induced on the thirteen constant and four root directions.
Multilinearity of the matching cofactors gives

```text
U_F b=b_F S_F,          U_F D_q0(alpha)=D'_F(S_F alpha)J_F,
U_F R(F)=Diag.                                           (1)
```

Equivalently, the constant-block images agree and every root-response
operator satisfies `U_F H_r=H'_(r,F)S_F`.

Thus this is covariance of the actual graph/source response semantics.  The
fixed-coordinate universal legal incidence remains the `68 x 4` system of
`GLD76`; the three-column system below is used only in the transported
literal-Delta presentation.

Define the exact frame open

```text
Omega(F)=delta_gauge(F) product_(u=0)^3 det F_u,
delta_gauge=product_(u=1)^3 product_(c=0)^2 (F_u)_(0,c).
```

The fully-supported and nonisotropic data belong to the fixed `GLD70`
interface and retain their already-declared nonzero hypotheses.  After also
inverting the selected rank-44 nuisance pivot, use pivot choices specializing
exactly to `GLD74`:

```text
beta(F,t)=beta_0(F)+K_F t,       t in A^35,             (2)
```

where `b_F beta=Delta_4`, `K_F` is a regular frame of `ker b_F`, and
`beta_0(F)` is regular.  Quotient the mixed legal response by the moving
`13`-column `Q`/eta-residual block.  The resulting columns are

```text
Z_r(F,t)=A_r(F)+K_(r,F)t,        r=0,1,2,3.             (3)
```

Partitioning matchings by the neighbor of `q_0` gives, for every solution of
`b_F beta=Delta_4`,

```text
Z_0+Z_1+Z_2-Z_3=0.                                    (4)
```

The `q_1` and port classes lie in the quotient block, the four root classes
have coefficients `xi=(1,1,1,-1)`, and the mixed part of `Delta_4` is zero.
Since the transported target is the three-dimensional diagonal space, the
same `17-(13+rank Z)` argument as `GLD74` proves that every legal lift
satisfies `rank[Z_0 Z_1 Z_2]<=1`.

All constructions in (1)--(4) are regular after the named localizations.  The
quotient uses mixed rows specializing at `F_0` to

```text
(0,1,2,3,4,5,7,8,9,11,17,27,53),
```

whose moving `13 x 13` determinant is the named function `gamma`, with

```text
gamma(F_0)=8(1+i)/27 != 0.
```

Thus no response-pivot divisor is omitted.  The original wording that used a
fixed mixed quotient in untransformed moving coordinates is superseded by
(1)--(4); it would discard the moving target's mixed coordinates and is not
used.

On the first proportional-column chart introduce slopes `(a,b)` and write

```text
Phi_(F,a,b)(t)=
  ((a K_(0,F)-K_(1,F))t, (b K_(0,F)-K_(2,F))t),

w_(F,a,b)=
  (a A_0(F)-A_1(F), b A_0(F)-A_2(F)).                  (5)
```

The homogenized necessary response equation is

```text
Phi_(F,a,b)(t)+s w_(F,a,b)=0.                          (6)
```

The affine raw fibre is `s!=0`; the boundary is `s=0`.  Equation (6) retains
all raw corrections and every rank drop and does not divide by a response
minor.

## 2. Leaf-invariant compression

Because the three leaf frames are equal, the actual leaf-`S_3` action
preserves the transported interface, nuisance map, all complete legal
response maps, kernel bundle, mixed quotient, and diagonal target response.
Hence (6) is `S_3`-equivariant.  Since the characteristic is zero, the
Reynolds projector is exact.

The `GLD76` raw-kernel decomposition is

```text
ker b_F = 8 trivial + 3 sign + 24 standard dimensions. (7)
```

Average the section `beta_0(F)` over `S_3`.  It remains a preimage of
`Delta_4` and makes `w_(F,a,b)` invariant.  Select the regular moving
invariant raw basis whose Gaussian specialization is obtained by
Reynolds-averaging kernel columns

```text
(0,7,8,9,10,12,13,16).                                (8)
```

Its determinant on fibre rows

```text
(0,1,8,9,10,12,13,16)                                 (9)
```

is the Gaussian value of the named moving basis minor `beta`, with

```text
beta=1008 i != 0.                                      (10)
```

This records explicitly the basis open used below.

Let `V_triv(F)` denote those eight regular invariant columns.  If (6) has a
solution, project it with the output Reynolds idempotent.  Every sign or
standard raw component disappears from this projected equation, while the
invariant raw component and `s w` remain.  Therefore a necessary condition is

```text
Phi_(F,a,b)(V_triv(F))u + s w_(F,a,b)=0, u in A^8.     (11)
```

This step does not assume that an arbitrary raw correction is invariant; it
uses the direct isotypic decomposition to retain and test its complete
invariant component.

## 3. Three explicit obstruction determinants

For the three `GLD77` points use the following slopes and quotient-row sets:

| point | `(a,b)` | selected rows in the `130`-row pair |
|---|---:|---|
| `v_-` | `(-1,1)` | `(2,3,6,14,15,16,18,19,67)` |
| `v_+` | `(1,-1)` | `(2,3,6,14,15,16,18,19,22)` |
| `v_x` | `(-1,-1)` | `(2,3,6,14,15,16,18,19,67)` |

For a row set `J_j`, define the regular polynomial

```text
delta_j(F,a,b)=det(
  [ Phi_(F,a,b)(V_triv(F)) | w_(F,a,b) ]_(J_j)
).                                                       (12)
```

The exact Gaussian values are

```text
delta_-(F_0,-1, 1) = 6574160/27 + (1735448/9)i,
delta_+(F_0, 1,-1) = 153664/9  + (44480/3)i,
delta_x(F_0,-1,-1) = -29451260/81 + (3419540/81)i.     (13)
```

All three are nonzero.

### Theorem 3.1 (sign-boundary principal-open nonextension)

For `j` equal to `-`, `+`, or `x`, equation (6) has no solution with `s!=0`
on

```text
D(Omega theta gamma beta delta_j)                      (14)
```

in the corresponding first proportional-column chart.  In particular, no
formal or analytic affine-response arc specializing to the `j`-th `GLD77`
sign point can remain in (14).

#### Proof

On `D(beta)` the eight columns in (8) are a basis of the invariant raw
kernel.  Suppose an actual `79`-coordinate coefficient vector solved (6).
Average that vector under the actual raw `S_3` action.  Equivariance of `b_F`,
the complete response, and `Delta_4` shows that the average is
still a raw preimage satisfying the same proportionality equations.  Its
kernel correction is invariant, so it has coordinates in the basis (8) and
gives (11).  This averages the coefficient vector itself, not a potentially
non-equivariant choice of free `t`-coordinates.

On `D(delta_j)` the selected `9 x 9` matrix in (12) is invertible.  Hence the
coefficients of its first eight columns and its final coefficient `s` must
all vanish, contradicting `s!=0`.  No division by `s` is needed.  The factors
`Omega`, `theta`, and `gamma` retain the declared frame, nuisance-pivot, and
quotient charts.  The
same column-independence argument holds over the localized coordinate ring,
so it also forces `s=0` for a formal arc even when `s` vanishes to positive
order.  This excludes arcs of every order, not only first-order
deformations.  `square`

## 4. Independent first-strict-jet check

A separate exact dual-number calculation differentiates the moving nuisance
map, raw pivot solve, `13`-column quotient, four scale-fixed survivor
directions, and both slope variables.  At each of the three points its
boundary operator `M`, complete first-jet coefficient matrix `S`, and affine
augmentation satisfy

```text
rank M=34,        rank S=36,        rank[S|r]=37.       (15)
```

Thus the normalized first-order affine system is inconsistent at all three
points.  Its homogeneous nullspace has dimension five and lies entirely in
`s=0`.  Equation (15) alone would not exclude higher-order arcs; Theorem 3.1
does so on the named opens by the invariant determinant argument.

## 5. Proof-topology consequence and residual obligation

`GLD77` made the sign-plane boundary an exhaustive three-point cover.
Theorem 3.1 now excludes every one of those three entrances on a nonempty
principal open containing its Gaussian boundary point.  The unresolved
projective boundary is therefore outside the pure sign plane: it may contain
trivial components, standard components, or mixtures of isotypic blocks.

**Successor update (`GLD79`, 2026-08-26).**  Exact `S_3` isotypic and
determinantal certificates subsequently prove that the complete Gaussian
projective boundary is exactly these three reduced sign points: the trivial
and standard blocks are empty, mixed blocks cannot cancel, and the other two
projective charts are empty.  Thus the missing boundary-fibre cover is now
exhaustive.  `GLD80` subsequently combines `GLD74`, `GLD78`, and `GLD79`
using the intrinsic `s`-saturated projective incidence and an algebraic
DVR-selection lemma; it proves that an existential principal survivor-open
containing `F_0` excludes every raw preimage.  Other survivor components, an
explicit survivor-only exceptional polynomial, and the source/interface
bridge remain separate.

## 6. Verification and hostile controls

Run:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_survivor_response_sign_boundary_first_strict_jet_obstruction.py
python claims/arbitrary-order/verify_four_root_torus_star_survivor_response_sign_boundary_invariant_open_obstruction.py
python claims/arbitrary-order/verify_four_root_torus_star_survivor_response_universal_module_reduction.py
python -I claims/arbitrary-order/audit_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py
```

The invariant verifier evaluates the literal-Delta quotient, invariant basis,
and three determinants at their Gaussian boundary points.  The universal
verifier checks the nuisance, complete-response, raw-coordinate, and target
intertwiners at that specialization.  Their regular moving continuations are
defined by (1)--(6) and determinant formula (12); the all-order
extension from a nonzero value to its principal open is the localized-ring
argument in Theorem 3.1, not a claim that the verifier expanded a universal
four-parameter polynomial.  The independent audit rebuilds the same base
data without importing repository modules.

The hostile controls are preserved:

- `GLD72` remains an exact concise GHZ survivor in the nuisance space;
- the `GLD70` epsilon generator is not used as a GHZ-membership test;
- the complete `GLD74` `65 x 3` quotient and affine-fibre exclusion replay;
- the actual nuisance and all complete `81`-coordinate response maps, not
  merely the abstract GHZ orbit, are checked for leaf covariance;
- frame ambiguity is handled in the certified `GLD75` gauge;
- `Omega`, `theta`, `gamma`, `beta`, and every `delta_j` are named, and no determinant,
  support coordinate, nonisotropic slope, or chart coordinate is discarded;
- arbitrary raw corrections are decomposed, not assumed invariant;
- the first-jet calculation retains all `35` raw, four survivor, and two
  slope directions;
- no sign-plane statement is promoted to a full boundary cover, source
  theorem, graph witness, counterexample, or global resolution.
