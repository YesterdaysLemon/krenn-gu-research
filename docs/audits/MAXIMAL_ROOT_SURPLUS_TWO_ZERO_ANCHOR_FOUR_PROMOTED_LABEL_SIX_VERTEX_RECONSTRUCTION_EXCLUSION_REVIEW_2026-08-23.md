# Hostile review: zero-anchor four-promoted-label six-vertex reconstruction exclusion

## Verdict

**ACCEPT after exact source-interface reconstruction, two independent hostile
mathematical reviews, focused symbolic verification, a genuinely independent
no-import audit, and authenticated replay of the accepted six-vertex
dependency.**

`GLS53` excludes the zero-residual support in which exactly four effective
auxiliary labels are promoted ports.  Fixed-residual and inactive-port
contraction turns the six surviving raw pair terms into the exact hafnian of
one reconstructed legal six-vertex ternary graph.  The accepted six-vertex theorem then
gives a contradiction after a legal one-vertex diagonal normalization.

This does not treat a four-label support containing either residual label,
any five-plus-label support, source-to-full-swallow coverage, raw escape,
nonzero anchors, or a legal response/selector/attachment package.  The
strategic node and global Krenn--Gu conjecture remain **UNRESOLVED**.

## Reviewed artifacts and interfaces

- [`GLS53 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FOUR_PROMOTED_LABEL_SIX_VERTEX_RECONSTRUCTION_EXCLUSION_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_four_promoted_label_six_vertex_reconstruction_exclusion.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_four_promoted_label_six_vertex_reconstruction_exclusion.py)
- owning source interfaces `GLS21`, `GLS36`, and `GLS39`
- frontier context `GLS52`
- the accepted
  [`six-vertex theorem`](../../claims/finite/n06/SIX_VERTEX_CERTIFICATE.md)
- the current-frontier, node-DAG, and arbitrary-order README updates.

The first hostile review reconstructed the complete `GLS21` raw-label
equation directly and checked every complement.  The second independently
audited the effective edge typing, transposes, matching multiplicities,
target normalization, field transfer, and historical dependency provenance.
Both reported a mathematical pass.  Formatting and integration findings
from the second review were corrected before candidate-tree validation.

## Complete raw-label audit

The fixed-residual `GLS21` equation is

```text
sum_(D in binom(Bhat,2)) G_D^A tensor H_(Bhat-D)
 +omega tensor H_Bhat
 =fixed-residual GHZ target.                         (1)
```

Let the effective support be

```text
Act=P={u_0,u_1,u_2,u_3} subset Uhat,
I=Uhat-P.                                            (2)
```

An inactive promoted endpoint has both maps `X=Y=0`, so every pair
companion incident with `I` vanishes.  Ineffectiveness of either residual
auxiliary label means both of its evaluated shore vectors vanish.  Thus
every residual--port companion and the residual pair `q` vanish.  The top
term vanishes because `omega=0`.  Exactly the six labels in `binom(P,2)`
remain; no deck nonvanishing or rank assumption is used.

For a root pair `{u,v}` and complementary active pair `{k,l}=P-{u,v}`, one
has

```text
Bhat-{u,v}=Q union I union {k,l}.                    (3)
```

After evaluating `Q` at the fixed residual vectors and `I` at all ones, the
physical deck in (3) is a bilinear tensor

```text
D_kl in V_k^* tensor V_l^*.                         (4)
```

It is therefore a legal edge block between `k` and `l` in an ordinary
six-vertex graph.  Reversing the vertex order uses the natural transpose of
the same bilinear tensor; it does not introduce a second physical object.

## Matching and multiplicity audit

A complete graph on six labelled vertices has fifteen perfect matchings.
Exactly three pair the two probes `a_0,a_1`; the reconstructed root edge is
zero, so these terms vanish.  Each remaining matching chooses two distinct
ports `{u,v}` hit by the probes.  The two root orientations contribute

```text
X_u tensor Y_v+X_v tensor Y_u=mu_uv,                (5)
```

and the two complementary ports are forced onto the single edge `D_kl`.
Thus the other twelve matchings group, with coefficient one and no missing
transpose, into the six terms

```text
sum_({u,v} subset P) mu_uv tensor D_(P-{u,v}).       (6)
```

This is exactly the contracted source, not a formal deck model or an
incidence-only control.

## Target, field, and exceptional-fibre audit

All three fixed-residual target coefficients `alpha_c` are nonzero by the
fully supported target hypothesis.  All-ones evaluation of an inactive port
sends every coordinate covector `e_c^*` to one, so no target colour is lost.
The reconstructed graph therefore has target

```text
sum_c alpha_c e_c^(tensor 6).                        (7)
```

Multiplying the `a_0` local covector factor of every incident edge by
`diag(alpha_0^(-1),alpha_1^(-1),alpha_2^(-1))` is a legal local graph
transformation.  Every matching uses one edge incident with `a_0`; hence (7)
becomes normalized ternary GHZ, while zero and mixed coefficients remain
zero.  No root, port, deck, response, selector, or minor value is divided
out.

At `r=3`, `Uhat` has four vertices and `I` is empty.  Formula (4) is still
the residual-evaluated physical deck on the two complementary active ports,
so the reconstruction does not require an inactive vertex.  At larger `r`,
all inactive contractions are evaluations, not generic specializations.
Every rank-drop, deck-zero, divisor, response-zero, and cancellation fibre is
therefore retained.

For a point over an arbitrary characteristic-zero field, its finitely many
coefficients and the inverses of the three target weights generate a
finitely generated extension of `Q`.  Such a field embeds injectively into
`C`.  The embedding preserves the complete polynomial equation and the
three nonzero weights, so the accepted complex theorem applies.

## Authenticated six-vertex dependency replay

The accepted theorem's large certificate bundle is historical data under
`tmp/` in the protected authority checkout, not tracked data in a fresh
worktree.  It was replayed read-only with the current-main verifier and its
output redirected outside every repository:

```text
python claims/finite/n06/verify_six_vertex_final.py \
  --base C:\Users\Yeste\OneDrive\Documents\open-graph-theory-with-prize \
  --output C:\w\kg-gls53-six-vertex-dependency-audit-20260823.json
```

Replay provenance:

```text
GLS53 base HEAD:              62f97c1657a68e7b24c9d9f3bd81b07cc0b157be
authority checkout HEAD:      a16315f145324b503c3ec0ccd017ee7562f9626d
six-vertex theorem SHA-256:   63d41774e2a8c45ded67cb949b920c34d0cabb499ba6c215423dc274686066c4
top verifier SHA-256:         e383454d167b8d0cc7c35d6c56fb69fe7d302c2ca15d5d234047016c783a889e
replay output SHA-256:        2e539db1802048560e7e18c8bc69c5e1274ffd7883863e33dbe1551070de67b7
verified:                     true
CNF SHA-256:                  154b1a64a70b10eef5bd7cb3ddb929033d408b65f26ff2704eacc610030154c7
DRAT proof SHA-256:           9273c872b3aa071e67b3ff176d84c50d104e212bcab38980be38de69f9ffb1d1
```

The theorem document and top verifier hashes agree between current main and
the protected authority bundle.  No file in the authority checkout was
modified.

## Computational independence

The primary verifier uses SymPy and a direct recursive enumeration of all
fifteen matchings.  It groups the symbolic result into the six raw pair
labels, audits complements for several root orders including `r=3`, and
checks exact rational target normalization.

The independent audit imports no project code or algebra package.  It uses
its own bit-mask hafnian and sparse monomial dictionaries, then separately
evaluates random-looking deterministic exact samples over `F_101` using
direct matrix entries.  It also derives the live auxiliary-label census from
scratch.  The two checkers therefore differ in representation, algorithm,
and arithmetic route.  The written proof carries arbitrary root order and
characteristic zero.

## Required replay

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_four_promoted_label_six_vertex_reconstruction_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_four_promoted_label_six_vertex_reconstruction_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_effective_label_uncontracted_complementary_deck_two_colour_separation_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_effective_label_uncontracted_complementary_deck_two_colour_separation_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
```

The package must still pass full candidate-tree validation, exact-head hosted
CI, safe merge, and fresh merged-main replay before publication is complete.

## Unresolved boundary and no-go warnings

The six-vertex reconstruction relies on having four promoted labels and no
residual label.  If one or both residual labels are active, residual--port
terms remain and the same contraction does not become an ordinary graph on
the two probes plus four ports.  In particular, an exact rank-seven
one-residual/three-port incidence control shows that activity, full swallow,
and low incidence rank do not by themselves force a pair with two private
target colours.  That control fails the full target and is not a witness,
but it blocks an incidence-only extension of the GLS52 private-deck route.

The two-residual/two-port `q=0` quotient admits coordinate exceptional cells,
and every `q!=0` fibre remains open; neither is silently covered here.
Residual-containing four-label supports require new full-target physical-deck
coupling.  Five-plus labels and all source/response/selector/synchronization/
nuisance-survival/anchor gates also remain open.  No global-resolution claim
follows.
