# Generic marked `H31` obstruction on the disjoint mixed-star component

## Status

This is an exact characteristic-zero theorem on a dense open subset of
the eighth pure-`P_4` component proved in
[`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md).

The complete marked-basis fibre over the generic point of that
component has no `H31` lift.  Thus all eight pure-component orbits
certified at that checkpoint have empty generic marked `H31` fibre.
The later embedded-`P_3` ninth component is not covered.

This does not close special parameter or projective boundary points,
prove that the nine known components are exhaustive, or resolve the global
prize problem.  The generic weighted `H22` fibre has since been closed
in
[`P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).

## Component function field

Use the pure-factor bases `(alpha_i,beta_i)=(y_i,x_i)` from the
component theorem:

```text
alpha_0=(0,0,1,-1),       beta_0=(a+b,a-b,0,2),

alpha_1=(-af+1,-af-1,f+phi,f-phi),
 beta_1=(1,1,0,0),

alpha_2=(-aj+eta,-aj-eta,j+kappa,j-kappa),
 beta_2=(1,1,0,0),

alpha_3=(1,-1,0,0),       beta_3=(0,0,1,1),        (1)
```

where

```text
j=f+b phi^2,       kappa=phi(bf+1),       eta=-(bf+1)
```

and

```text
Phi=
 a^2 b f phi^2+a^2 f^2
 -b^2 f^2+b^2 phi^2-bf-1=0.                       (2)
```

The polynomial `Phi` is irreducible, so the generic component field is

```text
K=C(a,b,f)[phi]/(Phi).                              (3)
```

Every marked basis on the same four planes is represented, up to
irrelevant row scalings, by

```text
beta_i(t)=beta_i+t_i alpha_i.                       (4)
```

## Exact projection of genuine binary neighbours

For a distinguished source coordinate `q`, replace that coordinate by
the fifth source coordinate.  Let `z` be the eight extension entries,
let `M_q(t)z` be the fourteen mixed binary coefficients, and denote the
two diagonal coefficients by

```text
A_q(z), B_q(z).
```

A genuine neighbouring `Delta_2` direction satisfies

```text
M_q(t)z=0,             A_q(z)B_q(z) != 0.          (5)
```

Normalize `A_q(z)=1`, invert `B_q(z)`, and eliminate the nine
extension/inverse variables over `C(a,b,f)`, retaining (2).
For `q=0,1`, the projected ideal is the unit ideal.

For `q=2,3`, it is respectively

```text
(Phi,t_1,t_2,t_3,L_2),        (Phi,t_1,t_2,t_3,L_3),               (6)
```

where, with

```text
G=a^2 b f^2+2b^2 f+b,
```

one has

```text
L_2 =
 G phi+(1-a^2 f^2)t_0
 +3a^2 f^2-2b^2 f^2-2bf-3,

L_3 =
 G phi+(1-a^2 f^2)t_0
 -a^2 f^2+2b^2 f^2+2bf+1.                         (7)
```

The verifier proves equality of ideals in both directions, rather
than only containment of the displayed equations in the computed
projection.  Thus over `K`, and on `1-a^2f^2 != 0`, each of `q=2,3`
has exactly one surviving marked basis:

```text
t_1=t_2=t_3=0,          L_q=0.                     (8)
```

There are no hidden marking sheets.

## A uniform one-minor obstruction

On either marking (8), the mixed matrix has rank six over `K`; hence
its extension kernel has dimension two.  Let `P_q(z)` be the
mode-zero one-marked map on the neighbouring hyperplane, and take its
minor in rows `0,1,3,7`.  Exact reduction modulo

```text
(Phi,L_q,M_q(t)z)
```

gives the all-extension identities

```text
det P_2(z)[0,1,3,7] =  R A_2(z) B_2(z)^2,
det P_3(z)[0,1,3,7] = -R A_3(z) B_3(z)^2,          (9)
```

with

```text
R = f(bf+1)(1-a^2f^2)/(a^2f+b).                    (10)
```

On the dense open set where the factors in (10) are nonzero,
condition (5) makes the relevant determinant in (9) nonzero for every
genuine extension.  The neighbouring one-marked map then has rank
four.  A ternary lift would factor this map through a three-dimensional
target local space, so its rank would be at most three.  This is
impossible.

Combining the unit projections for `q=0,1`, the complete projections
(6)--(8), and the identities (9) proves:

```text
the generic marked H31 fibre of the disjoint mixed-star
component is empty.                                (11)
```

## Geometric interpretation

The calculation is a small determinantal-incidence argument over the
component function field.  Projection of (5) computes the relevant
open Fitting stratum of the extension bundle.  Equations (9) show
that the rank-at-most-three Fitting locus is disjoint from every
genuine binary direction on that stratum.  No ambient Grassmannian
or local-map tuple is enumerated.

## Honest frontier

All eight component orbits known at this theorem checkpoint are
generically closed for `H31`; the companion theorem closes their
generic weighted `H22` fibres as well.  A ninth, embedded-`P_3`
component has since been certified and its marked fibres are open.
What remains is:

1. the ninth component's generic marked fibres;
2. the special parameter/projective boundaries of the components not
   already closed in full;
3. component exhaustiveness, especially exceptional triangle,
   rank-two-relation, and lower pair-rank strata.

The global conjecture remains unresolved.

## Verification

Run:

```text
tmp/codex_verify_env/Scripts/python.exe \
  verify_p5_h31_disjoint_mixed_star_component_generic_obstruction.py

tmp/codex_verify_env/Scripts/python.exe \
  audit_p5_h31_disjoint_mixed_star_component_generic_obstruction.py
```

The primary verifier reconstructs (1)--(4), performs all four exact
function-field projections, proves the bidirectional ideal equalities
(6), and checks the characteristic-zero all-extension identities
(9)--(10).

The independent audit imports nothing from the primary verifier.  At
two generic finite-field component points it exhausts the affine
marked bases, independently recovers only the two markings (8), and
checks (9) on every genuine projective extension direction.  This
finite-field census is corroboration only; the function-field
eliminations and reductions prove the theorem over `C`.
