# Review: Gaussian survivor full projective response-boundary classification

Date: 2026-08-26

## Verdict

Accept `GLD79` as an **exact exhaustive classification of the projective
boundary of the fixed-Gaussian `GLD74` necessary response incidence**.  The
boundary consists of precisely the three reduced `GLD77` sign points.  The
trivial and standard isotypic blocks are empty, mixed support cannot cancel
between output isotypes, and injectivity of `K_0` covers the other two
projective charts.  This is not yet a moving-survivor open theorem.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## Evidence checked

The primary verifier reconstructs from the physical torus-star data:

1. the rank-`44` nuisance map and its complete `35`-dimensional raw kernel;
2. the exact `GLD74` `65 x 3 x 35` homogeneous quotient response;
3. every actual leaf-permutation action on the raw space;
4. transformed-coordinate covariance of the `81 x 79` nuisance map and all
   `78 x 79` raw response maps, stability of the thirteen-dimensional
   quotient subspace, and the induced `65 x 35` intertwining identities for
   every `K_r`;
5. raw isotypic dimensions `8+3+24` and the twelve-dimensional standard
   multiplicity space;
6. nonzero `K_0` minors on all three blocks, hence `rank K_0=35`;
7. a finite exact trivial-block minor cover with no projective solution;
8. a finite exact standard-block determinantal cover with no projective
   solution;
9. the `GLD77` three-point reduced sign scheme.

The exact `K_0` determinant values are

```text
trivial:              -5328+5328i,
sign:                 (-1+i)/6,
standard multiplicity: 21275136-7091712i.
```

For the trivial first pencil, two maximal minors have gcd `a+1`.  The sole
kernel line at `a=-1` fails the second pencil because two displayed residual
rows have gcd one in `Q(i)[b]`.

For the standard multiplicity first pencil, three displayed maximal minors
have gcd `(a+1)^4`.  On the remaining line `a=-1`, the first pencil has a
four-dimensional kernel, and two displayed `4 x 4` minors of the second
pencil restricted to that kernel have gcd one.  This proves emptiness over
algebraic closure: it is not a finite slope sample or a modular inference.

The independent standard-library audit already reconstructs the quotient,
raw sign action, and the reduced three-point sign scheme in reverse fibre
order without importing repository modules.  It does not independently
replay the new standard-block determinant calculation.  That is an explicit
independent-evidence gap, not a mathematical gap in the exact primary
certificate.  Two separate Luna-max hostile calculations also reproduced
the trivial and standard exclusions through independently selected minors;
those ephemeral calculations informed this review but are not counted as a
portable repository audit.

## Exhaustiveness audited

The output quotient is an actual `S_3` representation and every `K_r` is an
intertwiner.  Characteristic zero makes the raw kernel the direct sum

```text
U_triv direct-sum U_sign direct-sum U_std.
```

For a fixed slope pair, the two proportionality equations preserve this
sum.  Their zero output has zero projection to each output isotype, so one
isotypic raw component cannot cancel another.  A mixed solution would
therefore produce a pure solution in every nonzero component.  Empty trivial
and standard kernels force the complete solution to be sign-isotypic.

The selected minors and Bezout/gcd identities are units over `Q(i)` and stay
units after every field extension.  Hence the emptiness statements are
geometric.  Near each of the three sign points, one full-rank trivial minor
and one full-rank standard minor eliminate those coordinates over the local
ring.  The residual sign ideal is reduced by `GLD77`, so the conclusion is
scheme-theoretic rather than only a classification of closed points.

The standard `+1` transposition eigenspace is one copy of the multiplicity
space because the irreducible standard representation has a one-dimensional
fixed line for a transposition.  Equivariant maps act as a multiplicity map
tensored with the standard identity, so injectivity/rank on this twelve-space
is equivalent to the complete twenty-four-space statement.

Finally, `K_0` is injective on every isotype.  A projective rank-one triple
with first column zero would therefore have zero raw direction.  Thus every
projective point is in the `K_0t!=0` slope chart and no second or third chart
branch is omitted.

## Load-bearing limits

1. `GLD79` is fixed at the exact `GLD72` Gaussian survivor.  It does not
   assert that the projective boundary remains three points over nearby
   survivor frames.
2. The classified object is the homogeneous boundary of the necessary
   `GLD74` quotient rank-one condition.  It is not itself the full legal lift
   incidence or a source graph.
3. The three sign directions lie at infinity; none is promoted to a finite
   raw preimage or counterexample.
4. A survivor-open theorem still needs the proper-image/curve-selection
   bridge from `GLD74`, `GLD78`, and this exhaustive fibre classification.
5. No explicit survivor-only exceptional polynomial has been calculated.
6. Other survivor components, frame gauges, source presentations, roots,
   non-star interfaces, maximum-root/no-fifth-root certification, and global
   graph coverage remain open.

## Recommended successor

Form the projective compactification of the affine necessary incidence over
the scale-fixed `GLD75` survivor chart.  Let `C` be the closure of its affine
part.  Properness of the projection and the `GLD79` boundary fibre reduce
possible specialization over `F_0` to the three sign points; `GLD78` excludes
formal/analytic affine branches through each.  If written with a precise
curve-selection argument, this gives an existential principal survivor-open
exclusion containing `F_0`.  Computing an explicit base polynomial remains a
separate elimination obligation.
