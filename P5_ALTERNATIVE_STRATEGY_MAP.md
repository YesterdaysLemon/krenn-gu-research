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

A monomial-hypergraph refinement separates those 55 supports into 32
classes.  Only the original support is identical to the proved core
under a plain variable relabelling.  Thus a reusable theorem needs
genuine Laurent/gauge transformations or several different sparse
identities; the term-count rectangle is not itself the lemma.

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
certificates.  The exact-three runs completed with:

```text
C4+C6:  5,993 support-semantic survivor orbits
C10:   11,751 support-semantic survivor orbits
total: 17,744 support-semantic survivor orbits.
```

These catalogues are still exploratory until independently regenerated
and packaged with their algebraic obstruction artifacts.

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

The full covariant search has an exact low-degree floor.  The
multiplicity-free decomposition of
`Sym^2((C^3) tensor power 5)` has sixteen irreducible
`GL(3)^5` modules, indexed by even subsets of exterior-square factors.
An isolated pair of source permutations proves that the restriction
pullback is nonzero, hence injective, on every module.  Therefore the
`P_5` restriction image has no nonzero quadratic equations at all.
The proof map is `P5_NO_QUADRATIC_RESTRICTION_EQUATIONS.md`.

Degree three has nontrivial multiplicity spaces, but it is now closed
as well.  Exact Schur--Weyl character arithmetic reduces all 147
ordered cubic module tuples to thirteen type-count representatives.
Deterministic matrix-unit contractions of three copies of `P_5` have
full multiplicity rank in every representative; nonzero minors modulo
five certify the ranks over characteristic zero.  Therefore the full
cubic pullback is injective and the restriction image has no cubic
equations.  See `P5_NO_CUBIC_RESTRICTION_EQUATIONS.md`.

The obvious degree-three determinant contraction cannot work.  It uses
one alternating epsilon tensor in each of five modes; swapping two of
the three tensor copies changes its sign by `(-1)^5`, while a
degree-three polynomial is symmetric in those copies.  The contraction
is therefore identically zero.  Degree six, using two epsilon tensors
per mode, is the first natural invariant search space.

A naive 30-index degree-six contraction is computationally unsuitable,
but the symmetry-reduced search space is small.  Exact Young
seminormal-form character arithmetic verifies that the `S_6`
representation of shape `(2,2,2)` has dimension five and that

```text
dimension (([2,2,2]) tensor power 5)^(S_6) = 11.
```

Thus there are only eleven degree-six scalar invariants to test.
`analyze_p5_degree_six_invariant_space.py` checks the Coxeter relations,
the complete `S_6` character table, character orthogonality, and the
11-dimensional multiplicity.

That remaining test is now exact and negative.  Eleven explicit
epsilon-pair contractions have a generic evaluation minor with
determinant `1 mod 5`, so they form a basis.  Their pullbacks along
explicit local restrictions of `P_5` have an evaluation minor with
determinant `2 mod 5`.  The pullback is therefore injective: no nonzero
degree-six `SL(3)^5` scalar invariant vanishes on every `P_5`
restriction.  This closes the simple degree-six separator route, though
it does not exclude higher-degree invariant relations or non-invariant
equations.  The exact proof map is
`P5_DEGREE_SIX_INVARIANT_PULLBACK.md`.

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
3. use Route C if the survivor supports fall into few Grassmannian
   matroid strata;
4. keep Route E as a source of identities, but require a
   postselection-only elimination before investing in it.

Route D's homogeneous degree-six scalar separator has been ruled out
exactly.  The full covariant ideal is empty through degree three, so
the next representation search begins in degree four.  Revisit this
route only with a degree-four-or-higher non-invariant module or a
specific higher-degree invariant construction.
