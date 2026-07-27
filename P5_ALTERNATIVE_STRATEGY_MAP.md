# Alternative routes for the remaining P5 obstruction

## Status

The global Krenn--Gu conjecture remains unresolved.  This note records
routes that can replace or guide support-by-support Gröbner calculations
in the remaining attempt to prove that the order-five permanent tensor
does not restrict to `Delta_3`.

The current exact-three-coordinate branch has now excluded zero, one,
and two partial non-coordinate cells.  Its next finite layer has three
partial cells.
There are

```text
2 * 6^5 * binomial(10,3) * 3^3 = 50,388,480
```

labelled supports in that layer, so direct materialization is no longer
the preferred enumeration method.

## Route A: sparse-resultant cores

One exact-two `C4+C6` support has a five-equation Laurent contradiction:

```text
22001, 22002, 22200, 22201, 22202.
```

The full support system has 205 mixed equations, but these five reduce
to the two-branch identity in
`P5_FIVE_EQUATION_LAURENT_CORE.md`.  This is evidence that the large
Gröbner bases may be discovering much smaller sparse resultants.

A term-count screen found 55 exact-two supports with the same
`(9,8,9,8,9)` five-equation rectangle profile: 29 of shape `C4+C6` and
26 of shape `C10`.  A five-second probe certified six of the 29
`C4+C6` systems directly; 23 timed out.  A timeout here is not a
survivor, because deleting equations can make a Gröbner calculation
harder.  Term counts alone also do not prove that two cores are related
by a Laurent change of variables.

The next useful test is therefore structural, not another longer batch:

1. encode each five-polynomial system as a monomial-incidence
   hypergraph;
2. quotient by variable relabelling and torus gauge transformations;
3. recover a symbolic resultant identity for each resulting class;
4. translate each identity back into a support-local forbidden pattern.

If a small number of forbidden patterns covers the exact-three layer,
the computational theorem can become a human-scale lemma.

## Route B: symmetry-broken exact-k SAT

The support constraints, local projective-signature catalogue,
source-pair quotas, pure-permanent requirement, and
no-unique-mixed-permanent condition are Boolean before any coefficient
algebra is attempted.  They can therefore be enumerated directly in a
symmetry-broken SAT model.

`enumerate_p5_exact_k_partial_supports.py` implements this route.  It
adds an exact cardinality constraint to the existing local-signature
CNF and blocks only canonical fixed-shape supports.  This avoids
building a Python set containing all 50,388,480 labelled exact-three
supports.  Every run checkpoints and stops before host-available memory
falls below 20 percent.

This remains a finite search, but it is sustainable enough to produce a
small survivor catalogue on which Routes A and C can learn structural
certificates.  The `C4+C6` exact-three run completed with 5,993
support-semantic survivor orbits.

## Route C: Grassmannian and Pluecker elimination

A proposed restriction consists of five surjective maps

```text
A_i : C^5 -> C^3.
```

Before choosing target bases, each map determines a two-plane
`ker(A_i)` in `Gr(2,5)`.  The current row-support language is a chartwise
description of these five Grassmannian points.  Replacing matrix entries
by Pluecker coordinates has three potential advantages:

- the rank-three condition is built in;
- changes of target basis disappear;
- the five local coordinate-plane incidence conditions become
  Schubert-type conditions.

The concrete experiment is to rewrite the pair-cover and
source-subset Hall hierarchy as incidences among five points of
`Gr(2,5)`, then eliminate against the Pluecker quadrics.  A resulting
empty intersection would close all support charts at once.  Even a
nonempty intersection would stratify the remaining charts by matroid,
which is a more invariant classifier than raw zero patterns.

## Route D: tensor invariants

The desired statement is

```text
(A_1 tensor ... tensor A_5) P_5 != Delta_3.
```

Thus a polynomial on `3 x 3 x 3 x 3 x 3` tensors that vanishes on every
restriction of `P_5` but not on `Delta_3` would be a one-line global P5
obstruction.

The obvious degree-three determinant contraction cannot work.  It uses
one alternating epsilon tensor in each of five modes; swapping two of
the three tensor copies changes its sign by `(-1)^5`, while a
degree-three polynomial is symmetric in those copies.  The contraction
is therefore identically zero.  Degree six, using two epsilon tensors
per mode, is the first natural invariant search space.

A naive 30-index degree-six contraction is computationally unsuitable.
The viable version should work in the
`S_6` representation of shape `(2,2,2)`, whose local dimension is five,
and search the invariant part of its fifth tensor power.  This reduces
the problem from raw tensor-index contraction to a small
representation-theoretic linear algebra calculation over a finite
field.  Any candidate separator must then be checked exactly over the
integers or rationals.

## Route E: Fourier charge and Gaussian moments

Applying the three-point Fourier transform in every target mode sends
`Delta_3` to the charge-conservation tensor

```text
1[k_1 + ... + k_5 = 0 mod 3].
```

This turns three isolated diagonal coefficients into one affine
`Z_3` hyperplane and may expose a convolution or character-sum identity
for the permanent tensor.  It is worth testing whether the five local
maps can satisfy this charge law without support enumeration.

The original graph tensor is also the squarefree, one-photon-per-party
sector of an exponential quadratic form, so Wick/hafnian identities are
available.  The caution is that standard Gaussian recurrences couple
different photon-number sectors, while the conjecture constrains only
one postselected sector.  A useful identity must eliminate the
unobserved sectors; otherwise this language is only a reformulation.

## Priority

1. finish the exact-three SAT survivor catalogue with Route B;
2. learn and prove sparse forbidden patterns with Route A;
3. run the finite-field degree-six invariant test from Route D;
4. use Route C if the survivor supports fall into few Grassmannian
   matroid strata;
5. keep Route E as a source of identities, but require a
   postselection-only elimination before investing in it.
