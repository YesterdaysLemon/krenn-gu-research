# Methods review for the fixed-star survivor-response parent problem

Date: 2026-08-26

## Scope and search limits

This is a bounded methods and related-work review prompted by `GLD75`.  It
asks which external techniques best fit the exact survivor-response incidence

```text
b alpha=T(F),                    D_q0(alpha)L=R(F),
```

after the local survivor germ has been reduced to four parameters modulo
tensor scaling.  It does not assign mathematical status and does not import
an external theorem into a proof.

The search inspected arXiv result pages, publisher abstracts, the HAL author
index, and the Stacks Project for combinations of `Krenn-Gu`, parametric
polynomial systems, comprehensive Groebner systems, discriminant varieties,
Fitting ideals, flattening stratifications, numerical irreducible
decomposition, and polynomial-system certification.  No PDF was downloaded or
archived.  The search was quick rather than exhaustive: it did not perform a
complete citation-graph, MathSciNet, zbMATH, or every-publisher search.

The bounded search found the already recorded 2022 unweighted classification
and 2024 sparse-graph result, but no newer primary paper claiming the full
complex-weight Krenn--Gu conjecture.  This is a search result with incomplete
coverage, not a novelty theorem or proof that no such paper exists.

## 1. Highest-value imported method: module and Fitting stratification

The response condition should first be rewritten as a statement about a
finitely presented module.  Over the coordinate ring of a survivor chart and
the raw-kernel parameters, form

```text
M=coker D_q0(alpha).
```

The three columns of `R(F)` define three sections of `M`.  Their simultaneous
vanishing after specialization is exactly the desired image-containment
condition.  Equivalently, on every rank-`r` stratum of `D`, one asks for

```text
rank [D | R]=rank D=r.
```

This yields a finite constructible cover using determinantal/Fitting ideals
and automatically retains response-rank drops.  The Stacks Project records
that Fitting ideals are presentation minors, commute with base change, and
control fibre generator counts; it also identifies Fitting ideals as the
standard source of flattening strata for finitely presented modules.

This is more faithful to the parent proposition than introducing all `51`
entries of `L` immediately.  It should be combined with the fixed
thirteen-column quotient discovered by `GLD74`, then used to identify the
smallest augmented minors or module relations that can possibly carry the
three target sections.

Relevant sources:

- [Stacks Project, Fitting ideals, Tag 07Z6](https://stacks.math.columbia.edu/tag/07Z6), especially Lemma 15.8.4 and Lemma 15.8.7;
- [Stacks Project, flattening stratifications, Tag 052F](https://stacks.math.columbia.edu/tag/052F).

## 2. Comprehensive Gröbner covers after compression

Montes and Wibmer's Gröbner-cover algorithm partitions parameter space into
disjoint locally closed segments on which a specialized reduced Groebner
basis has fixed leading data.  Lazard and Rouillier's discriminant-variety
approach likewise isolates parameter loci where a projected parametric system
changes behaviour.  These frameworks match the required output: a proved
principal open containing `GLD72`, together with explicitly named exceptional
divisors or a finite locally closed cover.

The recommended use is not to feed the full uncompressed incidence to a
comprehensive-basis routine.  First eliminate the linear raw solve, quotient
the fixed response module, decompose by symmetry, and choose a small
rank/Fitting stratum.  Then treat the four survivor coordinates as parameters
and the remaining raw/response variables as unknowns.  The leading
coefficients produced by the parametric computation are candidates for the
required exceptional polynomial `delta`; every zero branch must remain in the
cover.

The installed WSL Singular already contains `grobcov.lib`, so a bounded pilot
can be run without adding a new system dependency.

Relevant sources:

- [Montes and Wibmer, *Gröbner bases for polynomial systems with parameters*](https://www.sciencedirect.com/science/article/pii/S0747717110000970), DOI `10.1016/j.jsc.2010.06.017`;
- [Lazard and Rouillier, *Solving parametric polynomial systems*](https://doi.org/10.1016/j.jsc.2007.01.007), DOI `10.1016/j.jsc.2007.01.007`.

## 3. Projective boundary and escape to infinity

An empty affine fibre at one parameter value does not by itself imply an open
family of empty fibres: the elementary family `1-sx=0` is empty at `s=0` but
has `x=1/s` for every `s!=0`.  This is the precise geometric hazard in lifting
`GLD74`: raw or response variables may diverge along a survivor deformation.

Before a large parametric elimination, homogenize the raw-kernel and response
chart variables with their natural multidegrees and inspect the boundary at
infinity over `GLD72`.  If the compactified incidence has no boundary point
above `GLD72`, proper projection turns the pointwise exclusion into a
neighbourhood exclusion.  If boundary points exist, their initial ideals or
valuation vectors give explicit escape modes and should become named residual
branches.  The installed Singular also contains `tropical.lib`, making a
small initial-ideal/valuation pilot practical.

This projective-boundary check should precede attempts to infer openness from
a specialized Nullstellensatz identity.  Formal multiplier lifting alone can
hide unbounded growth in the eliminated variables.

## 4. Use the leaf symmetry representation-theoretically

`GLD75` proves that the local survivor germ is equal-leaf in its frame gauge,
and the complete interface has an `S_3` leaf-permutation action.  The next
response calculation should decompose the raw kernel, response domain, and
mixed quotient into trivial, standard, and sign isotypic pieces.  The target
diagonal response lies in the invariant sector.  An equivariant block
decomposition may therefore replace large minors by smaller covariant blocks
and identify which nontrivial raw directions can actually feed the invariant
target.

This needs an exact covariance audit of `D_q0`, not just tensor membership.
The installed Singular contains `finvar.lib`; for `S_3`, however, explicit
Reynolds projectors and rational character idempotents are likely simpler and
more independently auditable than a general invariant-ring computation.

## 5. Numerical algebraic geometry only as reconnaissance

Witness sets, monodromy, and numerical irreducible decomposition are designed
to census positive-dimensional components and estimate their dimensions and
degrees.  They could rapidly test whether the compactified response incidence
has components at infinity and suggest a finite component cover.  Smale
alpha-theory can certify isolated approximate roots of square systems.

Neither method proves emptiness of a positive-dimensional complex incidence
by itself.  In this repository it should be a discovery layer only: every
candidate component, divisor, or point must be reconstructed exactly and
checked by a portable algebraic certificate.

Relevant sources:

- [Sommese, Verschelde, and Wampler, *Numerical decomposition of the solution sets of polynomial systems into irreducible components*](https://doi.org/10.1137/S0036142900372549);
- [Hauenstein and Sottile, *alphaCertified: certifying solutions to polynomial systems*](https://arxiv.org/abs/1011.1091).

## 6. Recommended bounded experiment

The highest-value next sprint is:

1. use the `GLD75` ten-generator equal-leaf ideal, fix tensor scale, and take
   the four remaining free coordinates as parameters while retaining the
   dependent frame entries as unknowns on the certified Jacobian open (or in
   its local/etale algebra); do not assume those entries are globally rational
   functions of the four parameters;
2. express the `35`-parameter raw solve and `q_0` response equivariantly under
   leaf `S_3`;
3. form `coker D` and its augmented module with the three columns of `R`;
4. compute the lowest relevant Fitting/rank strata and the compactified
   boundary over `GLD72`;
5. only then run `grobcov` or a discriminant-style parametric standard-basis
   calculation on the smallest surviving block;
6. replay every resulting open certificate and exceptional branch without
   importing the discovery implementation.

Stop the sprint if the compactified boundary produces an exact response lift
or a persistent escape component; that is a route correction requiring
independent validation.  If the boundary is empty and a nonzero leading
coefficient is obtained, package its product as the explicit principal-open
polynomial `delta` and leave `delta=0` as the next named obligation.

## Assessment

The survivor-response track remains the most valuable **local** continuation
of `GLD74`: `GLD75` has reduced it to four genuine parameters rather than
showing it to be an unstructured large orbit problem.  It is also the best
place to develop a reusable module-level response obstruction.

It is not yet the unique highest-value route to the global conjecture.  Even a
principal-open fixed-star exclusion leaves exceptional survivor divisors,
other survivor components, other interfaces, and the source-to-interface
bridge.  A bounded module/compactification sprint is justified; an indefinite
sequence of ever larger fixed-star eliminations is not.  If the sprint does
not produce either an open certificate or a sharp boundary countermodel, the
programme should shift effort toward the universal source/interface theorem.
