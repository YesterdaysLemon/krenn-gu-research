# Hostile review: maximum-root surplus-two zero-anchor rank-one pure-probe orientation and hafnian splicing boundary

## Verdict

**Accepted as an exact characteristic-zero `r=3` continuation of `GLS57`,
an exact exclusion of two natural six-label splices, and a required receiver-
interface correction.**  The package does not close the all-rank-one branch,
the zero-anchor branch, the strategic node, or the global conjecture.

Reviewed artifacts:

- [`GLS60` theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_ONE_PURE_PROBE_ORIENTATION_AND_HAFNIAN_SPLICING_BOUNDARY_THEOREM.md);
- [focused exact verifier](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_one_pure_probe_orientation_and_hafnian_splicing_boundary.py); and
- [independent no-import audit](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_one_pure_probe_orientation_and_hafnian_splicing_boundary.py).

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Source and quantifier audit

The theorem starts only after the exact `GLS57` hypotheses have been met:

```text
r=3;
zero old-probe anchor;
six auxiliary labels;
all six joint probe maps torus-rigid and rank one;
the GLS57 2+2+2 partition and complete same-graph target equation. (1)
```

It does not infer all-rank-one from all-rigid, does not cover the `GLS58`
higher-rank branch, and does not promote the `r=3` six-label count to higher
root order.  Its pure-shore and splice conclusions are pointwise and require
no response evaluation, nuisance-rank minor, or residual denominator.  The
fully supported probe vectors used for the splice no-gos exist because the
ground field is infinite; no single such vector is declared to be a legal
selector or response point.

## Pure-shore proof audit

For `P_c={s,t}`, the load-bearing source equation is

```text
h_c(x_s tensor y_t+x_t tensor y_s)=e_c tensor e_c,
h_c!=0.                                                   (2)
```

Writing `X=[x_s x_t]`, `Y=[y_s y_t]`, and
`J=[[0,1],[1,0]]`, the companion is `X J Y^T`.  If both `X` and `Y` had
column rank two, then `Y^T` would be onto, `J` invertible, and `X` injective;
the product would have rank two.  Thus one shore has rank at most one.  Since
the product is the nonzero coordinate square, that shore is exactly the
corresponding coordinate line.  This proves the alternative without choosing
a minor.

On the first pure shore, write `x_s=a e_c`, `x_t=b e_c`.  Substitution gives

```text
a y_t+b y_s=h_c^(-1)e_c.                                (3)
```

Modulo the coordinate line, `(bar y_s,bar y_t)` is `(a r,-b r)`.  The cases
`a=0` and `b=0` were checked explicitly rather than divided away.  They also
prove the labelwise nonzero-pure conclusion: a vanished pure-shore edge
forces the corresponding opposite-shore edge to be nonzero pure.  The
transposed case is identical.  The pigeonhole conclusion chooses one valid
shore for each of three pairs and therefore gives only two colour-pair shores
on one probe, not a three-colour star.

Hostile review rejects these stronger readings:

- both shores must be pure;
- both edges on the selected pure shore must be nonzero;
- one old probe must be pure on all three colour pairs;
- the pure side is canonical when both alternatives hold; or
- raw probe purity is already a legal target-pure anchor.

The exact controls include first-shore-only, second-shore-only, both-shore,
and zero-edge boundary points.

## First-variation and direct-companion audit

After contracting both probe roots, each companion is supported only at
`(kappa(s),kappa(t))`.  Direct expansion of the original eight-vertex
matching tensor gives

```text
F(Theta,W)=sum_D Theta_D tensor H_(Bhat-D)(W)
           =[u]H_Bhat(W+uTheta).                         (4)
```

The contracted target has weights `z_(0,c)z_(1,c)`, all nonzero at a fully
supported probe point.  This is a hafnian derivative, not automatically the
hafnian of a new graph.

If `Theta` itself is used as the new edge array, every perfect matching uses
the same fixed local word `kappa`.  Hence `H(Theta)` is zero or one
decomposable tensor on the nonconstant `2+2+2` word.  It has flattening rank
at most one under every invertible local change of basis, whereas the
contracted three-colour target has rank three.  The direct-companion splice
is therefore excluded, including local re-normalizations.  The rational
control with coefficient `18` shows that this conclusion is not merely a
forced-zero statement; it is explicitly not a full witness.

The review does not generalize this no-go to arrays constructed from both
`W` and `Theta`, nonlinear transformations, contractions retaining other
physical labels, or a separately proved permanent extraction.

## Vertex-gauge audit

Under

```text
Theta_(s,t)=(a_s+a_t)W_(s,t),                            (5)
```

each perfect matching contributes its `W` monomial multiplied by
`tau=sum_t a_t`.  Thus `F=tau H(W)` exactly.

- If `tau=0`, the first variation vanishes, contradicting its three nonzero
  target coefficients.
- If `tau!=0`, the existing internal array `W` is an honest six-vertex graph
  whose matching tensor is a weighted ternary diagonal.  One local diagonal
  normalization removes the three nonzero weights.  The accepted six-vertex
  theorem excludes it.

For a general characteristic-zero field, only finitely many coefficients
occur.  Their finitely generated field embeds into `C`, preserving all
equalities and nonzero target weights.  The complex certificate therefore
applies.  This excludes vertex-rescaling tangents and, in particular, common
scalar proportionality.  It does not classify the full first-variation
fibre or prove that every possible splice is a gauge.

## Receiver-type correction

The earlier `GLS57` theorem and review correctly said that the contracted
tensor is not automatically a six-vertex matching tensor, but then stated
that a weighted `P_6` restriction would be accepted by the committed
six-vertex theorem.  Those are different source tensors:

```text
six-vertex graph:  hafnian matching tensor, 15 matchings, edge degree 3;
repository P_6:    six-factor permanent, 720 permutations, factor degree 6.
                                                               (6)
```

The counts are a type audit, not a proof that no separately constructed
bridge can exist.  The logical correction is nevertheless mandatory: the
accepted `n=6` theorem excludes the first object, while an exact
`P_6 -> Delta_3` restriction enters the still-open permanent subtree
`PR/PR6/PRT`.  `GLS60` and the corrected `GLS57` owner/frontier preserve this
distinction and do not claim permanent nonrestriction.

## Verifier independence

The primary uses SymPy to verify all nine Cauchy--Binet minor factorizations,
symbolic normal forms, exact coefficient arrays, polynomial deformation,
and flattening ranks.  It checks all `729` local words twice and checks
`1458` gauge coefficients.

The audit imports neither the primary nor project code.  It uses a complete
`F_3` census of `816` admissible companion quadruples, with
`384/384/48` first-only/second-only/both orientation counts and `424`
zero-edge boundary points.  Its matching engine uses bit masks and compares
the direct eight-vertex expansion to the six-label marked-edge expansion on
all `729` words.  Its gauge derivation marks edges inside each perfect
matching instead of differentiating a polynomial.  This is genuinely
independent in derivation, representation, and implementation route.

The scripts audit the exact algebra and finite controls.  The written rank
argument, matching bijection, and accepted six-vertex dependency carry the
characteristic-zero theorem.

## Required replay

From repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_one_pure_probe_orientation_and_hafnian_splicing_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_one_pure_probe_orientation_and_hafnian_splicing_boundary.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_all_rank_one_rigid_colour_pairing_and_promoted_response_supply.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_all_rank_one_rigid_colour_pairing_and_promoted_response_supply.py
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_residual_excess_hafnian_first_variation_and_active_vertex_gauge_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_residual_excess_hafnian_first_variation_and_active_vertex_gauge_boundary.py
python claims/finite/n06/verify_six_vertex_final.py \
  --base <historical-certificate-bundle-root> \
  --output <outside-repository>/gls60-six-vertex-dependency-audit.json
```

The final repository gate is the index-complete candidate-tree validation
from `AGENTS.md`, followed by exact-head hosted CI.

### Authenticated six-vertex dependency replay

The current-main checker was run read-only against the historical certificate
bundle in the protected authority checkout and wrote its result outside every
repository.  A preliminary run against the fresh worktree failed closed, as
expected, because its ignored `tmp/` directory does not contain the 86 MB
DRAT bundle.  The authenticated replay then returned:

```text
certificate-bundle checkout HEAD: a16315f145324b503c3ec0ccd017ee7562f9626d
six-vertex theorem SHA-256:       63d41774e2a8c45ded67cb949b920c34d0cabb499ba6c215423dc274686066c4
final CNF SHA-256:                154b1a64a70b10eef5bd7cb3ddb929033d408b65f26ff2704eacc610030154c7
final DRAT SHA-256:               9273c872b3aa071e67b3ff176d84c50d104e212bcab38980be38de69f9ffb1d1
replay output SHA-256:            2e539db1802048560e7e18c8bc69c5e1274ffd7883863e33dbe1551070de67b7
verified:                         true
```

The authority checkout remained clean and was not updated or edited.

## Exact remaining obligation

```text
GLS57 pure pair equations:                         USED;
pure old-probe shore alternative:                  PROVED;
direct companion graph splice:                     EXCLUDED;
vertex-gauge splice:                               EXCLUDED;
P6/six-vertex interface:                           CORRECTED;

non-gauge W/Theta reconstruction:                  OPEN;
promoted complete-nuisance survival:               OPEN;
legal selector normalization and response point:   OPEN;
joint response synchronization and activity:       OPEN;
named receiver with every anchor/gate:              OPEN;
higher-rank rigid and arbitrary-root branches:      OPEN;
strategic-node closure:                             OPEN;
global conjecture:                                  UNRESOLVED.        (7)
```

The smallest positive successor is no longer “produce a weighted `P_6` and
apply the six-vertex theorem.”  It is either:

1. construct an honest six-vertex edge array from `W`, `Theta`, and the
   remaining complete mixed/deck equations by a demonstrably non-gauge
   transformation; or
2. transport the new raw pure-probe data into one named promoted target
   quotient and prove response, selector, synchronization, nuisance-survival,
   activity, and anchor gates pointwise.

Neither route is supplied by this package.
