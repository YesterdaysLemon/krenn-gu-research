# The unconstrained three-port boundary jet is dominant

## Status

**Exact characteristic-zero algebraic-independence no-go.**  For three core
mode terminals, three core source terminals, and a `3 x 3` exterior, the 20
balanced boundary responses

```text
1 + 9 + 9 + 1                                      (1)
```

are algebraically independent as polynomial functions of the 27 entries of
`Y,Z,W`.  Equivalently, the boundary-response map has Zariski-dense image in
the full 20-dimensional balanced signature space.

Therefore there is no nonzero universal polynomial identity among the
unconstrained degrees `0,1,2,3` of the zeon boundary jet.  A cross-degree
obstruction for Krenn--Gu must use additional hypotheses such as colour
incidence, local span, pure-backbone extension, coefficient alignment, or a
restricted support class.

This is a no-go for a method, not a construction of a graph restriction and
not a statement that every response vector is attained exactly.

## The response morphism

Take `d=n=3` in
`ARBITRARY_PERMANENT_THREE_EXCESS_ZEON_BOUNDARY_JET_THEOREM.md`.  For
`I,J subseteq {0,1,2}` with `|I|=|J|`, put

```text
R_(I,J)=sum_(|S|=|T|=|I|)
          per(Y_(I,T)) per(Z_(S,J))
          per(W_(complement S,complement T)).       (2)
```

Order the coordinates by degree and then lexicographically:

```text
k=0:  R_(empty,empty),
k=1:  R_(i,j),                         9 entries,
k=2:  R_(I,J), I,J in {01,02,12},      9 entries,
k=3:  R_(012,012).                                  (3)
```

These define a polynomial morphism over any characteristic-zero field:

```text
Phi: A^27 -> A^20,        (Y,Z,W) -> (R_(I,J)).     (4)
```

The zeon coefficients are `k! R_(I,J)`.  Multiplication by the nonzero
scalars `0!,1!,2!,3!` does not change dominance.

## An exact Jacobian certificate

Evaluate at the integer matrices

```text
Y_* = [1 2 0]       Z_* = [1 0 2]       W_* = [2 1 0]
      [0 1 3]             [3 1 0]             [1 3 2]
      [2 0 1],            [0 2 1],            [0 1 4]. (5)
```

Order the 27 parameters row-major as

```text
y_00,...,y_22, z_00,...,z_22, w_00,...,w_22.       (6)
```

Select the following 20 Jacobian columns:

```text
y_00,...,y_22,                 all 9 Y entries,
z_00,...,z_21,                 first 8 Z entries,
w_00,w_01,w_02.                first W row          (7)
```

For the coordinate order (3), the determinant of this `20 x 20` minor is

```text
10622643353619573315207168
 = 2^31 3^5 7^2 11^4 13^2 379 443 != 0.            (8)
```

Everything in (8) is an exact integer.  There is no floating-point rank
test, random specialization, finite-field lift, or family census.

## Dominance theorem

The differential `d Phi` has rank 20 at (5), by (8).  The affine domain is
smooth, so the Zariski closure of the image of `Phi` has dimension at least
20.  Its target has dimension 20.  Hence

```text
closure(im Phi)=A^20.                              (9)
```

Equivalently, the pullback

```text
K[t_(I,J)] -> K[Y,Z,W],       t_(I,J) |-> R_(I,J)  (10)
```

has zero kernel.  Thus the 20 response polynomials are algebraically
independent, proving the claimed no-go over every characteristic-zero field.

## What this rules out

There is no nonzero polynomial `F`, independent of `Y,Z,W`, such that

```text
F((R_(I,J))_(|I|=|J|))=0                          (11)
```

for every `3 x 3` exterior.  In particular, the following unconstrained
program cannot work:

```text
construct the all-sector jet;
derive a universal cross-degree equation from its abstract form alone;
contradict the diagonal target.                    (12)
```

Any size-independent identity in these balanced response coordinates would
specialize to size three, so (9) rules out an unconstrained uniform identity
of that kind.  It does not rule out an `n`-dependent equation whose
specialization at `n=3` becomes the zero polynomial, or an equation involving
additional size-specific data.  It also does not rule out an identity asserted
only for exterior sizes `n>=4`.

The theorem does **not** rule out equations after imposing any of:

- three-colour cell-component structure;
- a mandatory pure-backbone cover;
- local rank-three and degree-excess ledgers;
- coefficient-induced theta alignment;
- sparsity or planarity of the boundary graph;
- bounded ranks of the permanental compounds `P_k(Y),P_k(Z)`; or
- relations coupling several coefficient words.

Those conditions cut out a proper parameter locus before `Phi` is applied.
The next useful ideal must be the image ideal of such a constrained locus,
not the zero ideal of the ambient response map.

## Relation to other no-go results

The result is the all-sector analogue of the repository's hidden-overlay
surjectivity warnings: once an unconstrained exterior is allowed to absorb
the boundary data, scalar or low-order identities can disappear.  The zeon
jet still matters because it gives exact coordinates for imposing the
missing constraints.  Dominance tells us precisely where not to look for
the next theorem.

In algebraic-geometric language, the problem has moved from finding an
equation of the ambient boundary-signature variety--there is none--to
finding equations of the image of the coloured/aligned incidence variety.

## Holant and matchgate translation

In Holant language, (4) is a realization map for a charge-balanced
six-terminal signature.  Dominance says that arbitrary nonplanar bipartite
permanent gadgets fill the ambient balanced signature space densely; hence
they satisfy no ambient matchgate-style polynomial law.

This does not conflict with matchgate theory.  Matchgate identities
characterize the much smaller planar/Pfaffian signature locus, and
holographic reductions may impose an additional basis orbit.  Cai and
Gorenstein give a self-contained matchgate-identity characterization in
[*Matchgates Revisited*](https://arxiv.org/abs/1303.6729).  The present
theorem says precisely that such Grassmann--Pluecker identities cannot be
imported to an arbitrary permanent boundary gadget before planarity,
Pfaffian realizability, or a holographic basis restriction is proved.

## Scope wall

```text
proved:     the unconstrained d=n=3 response morphism is dominant;
proved:     its 20 balanced coordinates are algebraically independent;
proved:     no polynomial identity exists for the unconstrained n=3 jet;
proved:     no size-independent uniform identity survives n=3 specialization;
not proved: exact surjectivity onto every point of A^20;
not covered: coloured, aligned, sparse, or local-span constrained images;
not covered: planar matchgates or holographic basis-restricted signatures;
not proved: any legal full P_m -> Delta_3 construction;
not used:   large enumeration, finite fields, floating point, numerics;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_permanent_three_excess_boundary_jet_dominance_nogo.py
python claims/arbitrary-order/audit_arbitrary_permanent_three_excess_boundary_jet_dominance_nogo.py
```

The primary verifier differentiates the 20 exact response polynomials and
checks (8).  The independent no-import audit reconstructs the differential
with integer dual numbers and computes the same determinant by fraction-free
Bareiss elimination.  The determinant is a fixed symbolic certificate, not
experimental evidence.
