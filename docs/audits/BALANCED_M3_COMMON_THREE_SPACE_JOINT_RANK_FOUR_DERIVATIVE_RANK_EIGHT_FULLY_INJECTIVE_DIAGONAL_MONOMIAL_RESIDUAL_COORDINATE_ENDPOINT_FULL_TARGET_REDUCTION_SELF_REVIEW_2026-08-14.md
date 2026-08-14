# Self-review: diagonal-monomial coordinate-endpoint full-target reduction

Date: 2026-08-14

## Verdict

Accept the stated characteristic-zero result as an exact local reduction,
subject to the repository validation recorded below.  It applies only to the
two diagonal coordinate endpoints left by S2CD, normalized as

```text
C=lambda e_2 tensor e_2,       w=e_0,       lambda!=0.
```

It does not exclude either endpoint.  It replaces the incomplete
`w`-perpendicular slice by an exact gauge-free full-target system and proves
one incidence subcase empty.  Nonmonomial residuals and all wider branches
remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## Load-bearing chain checked

1. S2CC supplies the graph presentation
   `K=span((x,y,0))+span(k_0,k_1,k_2)` and the complete coefficientwise target
   identity.  S2CD, colour permutation, and shared-factor rescaling reduce
   each surviving diagonal endpoint to `C=lambda E_22,w=e_0` with `C` outside
   the derivative tangent plane and `x,y` not proportional to `e_2`.
2. For `k_c=(a_c,b_c,e_c)`, the derivative image is
   `(a_c tensor y-x tensor b_c) tensor e_0+C tensor e_c`.  Coefficient
   extraction therefore has tangent sign `+a_c tensor y-x tensor b_c`; no
   factor from the six-term permanent polarization enters this linear
   derivative formula.
3. The `(2,2)` entries of the `k=1,2` slices determine `S_1,S_2`.  The other
   sixteen root entries remain explicit zero/target equations; source
   recovery does not remove them.  Subtracting the recovered tangent
   contributions from the `k=0` slice leaves exactly
   `R=kappa tensor S_0`, where `kappa=C+a_0 tensor y-x tensor b_0`.
4. The graph-lift gauge
   `a_c -> a_c+t_c x, b_c -> b_c+t_c y` fixes every tangent tensor.  The
   reduction therefore depends only on the four-space `K`, not on a chosen
   set of graph lifts.
5. Rank eight proves `kappa!=0`: otherwise `C` belongs to
   `A_1 tensor y+x tensor A_2`.  Consequently all pairwise flattening minors
   are equivalent pointwise to the existence of `S_0`.  Solver descendants
   may split into nine nonzero-entry charts, but the theorem itself neither
   divides by a chart coordinate nor inserts a localization.
6. Contracting the retained complete identity by `alpha in x^perp` and
   `beta in y^perp` kills the tangent correction and puts both involved rows
   in `Q=span(q_0,q_1,q_2)`.  The resulting `2 x 2 x 3` cube has the residual
   correction only in its `(1,1)` cell.  This is a consequence, not a converse
   to the sixteen face equations.
7. The target-visibility census is derived from the two evaluation vectors,
   not from a genericity assumption.  It explicitly retains every one-target
   and zero-target coordinate wall.
8. The two-radical lemma is a denominator-free support classification for
   the six-term split-cubic polarization.  Applied only when the common
   exceptional row supplies both radical identities, it excludes the fully
   supported middle-plane orbit in that distinct-plane intersection subcase.
9. At `x=y=e_1`, perturbing only `P^(1)_11` by a nonzero source tensor leaves
   source recovery, every perpendicular contraction, and the `k=0`
   flattening unchanged while violating one retained face equation.  This
   exact negative control makes the logical loss under contraction explicit.
10. An exact quotient-only realization satisfies the corrected cube on a
   one-visible wall.  It is deliberately not extended to the outside graph
   row or the tangent-coset equation.  Its role is to prove that no argument
   using the quotient cube alone can close the physical endpoint.

## Two-radical lemma audit

The proof splits by the support of the common radical row.

- With three nonzero source components, the two other rows are componentwise
  scalings.  Their scaling triples lie in `s+t+u=0` and are isotropic and
  mutually orthogonal for `st+su+tu`.  The polar form is nondegenerate there
  in characteristic zero, contradicting independence of the three rows.
- With two source components, evaluation at the common row forces both other
  rows, hence all of `Q`, to miss the third source.
- With one source component, either all rows miss a common other source or a
  crossed missing-factor pattern forces one of the other rows to be pure.
  Every nonzero output then shares one factor line.

The hypothesis `Q=span(a,b,c)` with `dim Q=3` is load-bearing.  The theorem
does not generalize the lemma beyond that scope.

## Adversarial checks and rejected shortcuts

- A tempting active-intersection identity
  `alpha^o_k beta_k=alpha_k beta^o_k` was rejected during review.  Permanent
  symmetry only yields a formula for
  `per(c,a-b,q_k)`; equality requires the extra condition
  `a-b in Rad_Q(c)`, which plane incidence does not supply.  No statement or
  consequence depending on that false identity remains in the theorem.
- A same-third-row binary-table slice has exact abstract realizations.  Those
  models fail the unsliced target coefficient and therefore neither prove nor
  refute the physical endpoint.  They motivate, but do not replace, the
  tangent-coset equation.
- Numerical least-squares behavior and capped Singular runs supplied no
  certificate and are not cited as evidence.
- The quotient-only control is labeled exact but nonphysical.  It does not
  assert that the graph lifts, rank-eight derivative, or full target can be
  realized simultaneously.
- The source tensors are eliminated only after their exact defining slices
  and all sixteen other face entries are retained.  The first draft omitted
  those entries and was rejected before commit after an adversarial audit
  supplied the tangent-slot counter-control.  There is no saturation variable,
  modular lift, random specialization, or inferred generic point.

## Verifier independence

The primary SymPy replay symbolically reconstructs the coefficient identity,
the graph gauge, all sixteen retained face entries, source elimination,
flattening-minor pivot identities, contraction and the omission control, the
support census, support-pattern interfaces in the two-radical lemma, and the
sharp quotient control.

The independent audit imports neither the primary verifier nor SymPy.  It
uses standard-library `Fraction` arithmetic, reversed traversal and
permutation order, separate face and contraction loops, independent pivot and
rank/determinant checks, support-pattern controls, and its own split-form permanent
implementation.  It is an interface audit rather than a formal proof
assistant reconstruction.

## Validation

Validation at the candidate checkpoint completed as follows:

```text
primary SymPy replay:                         PASS
independent no-import Fraction audit:         PASS
Python byte compilation:                      PASS
Ruff:                                         PASS
candidate-tree hygiene:                       PASS
  1,994 Python / 1,137 Markdown / 218 ledger entries
migration-tool unit tests:                    191 PASS
fourteen-vertex cycle-cover lattice tests:     14 PASS
link rewrite:                                  zero changes
```

The bounded coordinate-endpoint search reported elsewhere reached its
120-second/8-GiB cap without a certificate.  That run is **inconclusive** and
is not part of this validation or proof.

## Remaining obligations

The exact successor obligation is an exhaustive incidence atlas for the two
contracted planes in `Q`, split by the target-visibility walls, retaining all
sixteen recovered face equations and coupled to the nine nonzero-entry charts
of `kappa` and the ordinary flattening minors.  No such exhaustive atlas or
endpoint exclusion is claimed here.  Every
nonmonomial S2BQ residual, lower-rank target cell, other component and pole
stratum, pair gate, and higher order also remains open.  The global resolution
gate is not triggered by this reduction.
