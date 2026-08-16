# Self-review: canonical-binomial residual exclusion

Date: 2026-08-14

## Verdict

Accept the stated characteristic-zero result as an exact exclusion of one
target-stabilizer orbit in the fully injective joint-rank-four,
derivative-rank-eight cell, subject to the repository validation recorded
below.  In normalized coordinates that orbit is

```text
x=y=w=e_2,
C=kappa_0 e_0 tensor e_0+kappa_1 e_1 tensor e_1,
kappa_0 kappa_1!=0.
```

The theorem does not put every nonmonomial residual in this form and proves
no target-preserving degeneration to it.  All other nonmonomial residuals and
the diagonal monomial coordinate endpoints remain open.  Global Krenn--Gu
remains **UNRESOLVED**.

## Load-bearing chain checked

1. The allowed normalization is an actual stabilizer of the six-factor GHZ
   target: one common colour permutation and diagonal maps whose six
   same-colour weights multiply to one.  Arbitrary diagonal scalings on the
   three root factors can be compensated on the nonroot factors.  Thus
   nonzero `x,y,w` on one coordinate line can all be normalized to `e_2`
   without changing the target equation.
2. S2BQ and S2BR give
   `K=image H=D^(-1)(U)`, `dim K=4`, `dim U=3`, and
   `N=ker D=span((e_2,e_2,0)) subset K`.  With `L=N^perp`, the quotient-dual
   identity `(K/N)^*=L/K^perp` gives
   `V=H^T(L)` of dimension three.  Every third-root covector belongs to `L`;
   injectivity of `theta` therefore gives `Q=image theta=V`.
3. The quotient maps `H_bar:W->K/N` and `D_bar:K/N->U` are respectively
   onto and invertible.  Direct expansion of the three separated singleton
   columns of `D_bar H_bar` is a nonzero basis determinant times `Alt(Q)`.
   Physical full-sensor rank therefore gives the load-bearing
   `Alt(Q)!=0`; this is not assumed for an arbitrary three-plane.
4. The canonical derivative coefficient at `(i,j,k)` has only the two
   tangent shores at root colour two and the two diagonal residual entries.
   Its annihilator gives, from the complete target rather than a contracted
   slice, the two mixed zero pairs
   `M_(r_0,p_1)|Q=M_(r_1,p_0)|Q=0` and a weighted difference of the two
   diagonal maps with rank two onto `span(T_0,T_1)`.
5. The mixed-zero-pair lemma is an exhaustive source-support split.  Pure
   support contradicts `Alt(Q)!=0`; support two gives the conjugate pair
   `x+y,x-y`; full support forces componentwise scalings satisfying two
   scalar equations and then a nonzero linear form that cannot vanish on all
   of `Q`.  No generic coordinate or divisor is inverted.
6. The lemma implies `dim Rad_Q(u)<=1`.  In the square-zero branch, support
   two would make `Q` miss a source, full support has a two-dimensional
   global square kernel, and pure support has no independent radical partner.
   This closes the `(1,2)` and `(2,1)` diagonal-plane profiles immediately.
7. Permanent symmetry puts the intersection of the two diagonal row planes
   in `span(q_2)`.  In the `(2,2)` profile it is exactly that line, and each
   diagonal map has the opposite plane as its kernel.  Their image lines are
   independent because the weighted target difference has rank two.
8. Relative to the common line, an ordered pair of distinct projective row
   lines has exactly the three types `R=(c,A)`, `P=(A,c)`, or
   `G=(A,A+c)`.  The resulting nine pairs are exhaustive, including every
   boundary flag.  In six charts the two cross-zero planes meet in a line
   that the zero-pair classification makes both pure and two-supported.  The
   `RP/PR` charts make both diagonal maps share one decomposable image line.
9. In `GG`, all four actual row scalars are retained.  The exact identity is
   `M_(A-B,A-B)=F_0/(a_0 b_0)+F_1/(a_1 b_1)`, not the unscaled projective
   shorthand.  Its square image has rank two and equals
   `span(T_0,T_1)`, contradicting S2AL tangent-line separation.  No target
   cross-ratio value is specialized.
10. In the `(1,1)` profile, proportional row lines kill both diagonal maps;
    independent row lines are a conjugate pair whose square maps are
    proportional.  Either fork contradicts the rank-two target difference.

## Adversarial checks and rejected overreach

- An earlier projective `GG` shorthand dropped the nonzero row scalars.  The
  theorem was not promoted until the scalar-correct identity was restored;
  kernels, image lines, and the rank-two contradiction are unchanged.
- The cross-ratio parameter is described as left unfixed.  The proof works
  for every value satisfying the determinant condition but does not claim
  that every projective value is physically realized.
- A target-stabilizer one-parameter subgroup can expose monomial terms of a
  general residual, but it need not preserve derivative rank eight,
  injectivity, full-sensor rank, or the complete target on the limit.  There
  is no degeneration bridge from the full nonmonomial atlas to this orbit.
- Exact abstract contracted-slice models elsewhere in the research do not
  satisfy the unsliced target.  They are neither counterexamples nor inputs
  to this theorem.
- No solver timeout, numerical least-squares observation, modular sample,
  finite-field flag census, or unrestricted ideal computation is used as
  mathematical evidence.

## Verifier independence

The primary SymPy replay symbolically reconstructs the rank-eight canonical
derivative and its annihilators, the complete target relation, the
full-sensor alternating determinant interface, every support branch of the
zero-pair lemma, the radical square-kernel dimension, all nine flag
intersections, the `RP/PR` common-image interface, the target cross-ratio
determinant, the scalar-correct `GG` identity, and the dependent profiles.

The independent audit imports neither the primary verifier nor SymPy.  It
uses standard-library `Fraction` arithmetic, its own reverse-order permanent,
rank, span, and plane-incidence routines, and separately reconstructs
the derivative, target annihilators, support identities, flag table,
scalar-correct `GG` relation, and dependent-profile interfaces.  The scripts
audit exact algebraic interfaces; the written support and projective
arguments own the theorem.

## Validation

Validation at the candidate checkpoint completed as follows:

```text
primary SymPy replay:                         PASS
independent no-import Fraction audit:         PASS
Python byte compilation:                      PASS
Ruff:                                         PASS
candidate-tree hygiene:                       PASS
  1,996 Python / 1,139 Markdown / 219 ledger entries
migration-tool unit tests:                    191 PASS
fourteen-vertex cycle-cover lattice tests:     14 PASS
link rewrite:                                  zero changes
```

No large or uncapped solver run forms part of this validation.

## Remaining obligations

The immediate nonmonomial obligation is a target-coupled atlas for residual
classes not in this exact orbit, or a separately proved invariant or flat
degeneration that preserves every physical rank and target hypothesis and
controls all boundary components.  The diagonal monomial coordinate
endpoints still require exhaustive coupling of the sixteen retained faces
with the tangent-coset flattening from S2CF.  Joint-rank-three/rank-eight,
derivative-rank-seven, pair, component, pole, higher-order, and all-rank-drop
branches also remain.  The dedicated global resolution gate is not
triggered.
