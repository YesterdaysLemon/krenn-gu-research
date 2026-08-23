# Hostile review: zero-anchor normal-product divisor kernel profile and same-graph sharpness

Date: 2026-08-22
Reviewed claim: `GLS30`
Global Krenn--Gu status: **UNRESOLVED**

## Verdict

**ACCEPT at its exact stated scope.**  The arbitrary-root complement-kernel
identity, the four-port one-/two-active profiles, the two exact scalar-normal
response-deck controls, and the one-active maximum-root pure-normalized
boundary graph are correct over characteristic zero.  The claim is not an
exclusion of the complete normal-product divisor and is not a pointwise cover
of the zero-anchor witness branch.

The sharp scope correction is load-bearing.  The displayed maximum-root graph
satisfies pure normalization, outside incidence defect four within the bound
six, six nonzero responses, and the complete scalar normal identity, but it
fails original mixed coefficients and does not have simultaneous full normal
absorption.  Conversely, the controls with every normal image full are not
maximum-root source controls.
It does not certify the complete `GLS26` top reconstruction or simultaneous
full-module selector failure.  Thus the certificate refutes only an argument
from the scalar normal identity plus six responses and full normal images, and
separately an upgrade from maximum-root/pure data plus the scalar identity to a
witness.  It does not refute a theorem coupling maximum-root incidence to
simultaneous scalar-normal absorption or using the complete zero-anchor witness
equations.

## Interfaces audited

The owning interfaces were read from:

- `GLS22`, for the full/transverse target quotient and legal-selector scope;
- `GLS23`, for the complete labelled nuisance rather than its normal image;
- `GLS26`, for top-diagonal reconstruction and the branch-P/shore-cover split;
- `GLS28`, for supplier envelopes and the distinction between useful-row
  failure and full absorption; and
- `GLS29`, for the rank-two-shore normal quotient, normal nuisance image,
  complete mixed-response identity, and active-colour occurrence.

`GLS30` does not silently identify its supplier `k_D` with the complementary
physical response, normal-image fullness with full nuisance absorption, or a
scalar normal contraction with the complete contracted GHZ tensor.

## Denominator-free identity audit

For a retained pair `D` and complement `C`, contract the `GLS29` complete
normal identity by arbitrary `z_u in K_u` at every `u in C`.  Every foreign
supplier pair contains some endpoint in `C`; its local factor lies in `Z_u`
and is killed.  The unique retained term is therefore

```text
D_beta(star_(u in C) z_u)=R_C((z_u)_(u in C)) k_D.
```

No response, coordinate, active product, or supplier minor is divided out.
The image of the active Hadamard-product space lies in the fixed line `K k_D`.
When the active diagonal is nonzero, its matrix rank is its active support
size, proving the asserted supplier rank.  When it is zero, the equation is
only a product-zero statement.  The theorem correctly retains that silent
branch.

The primary verifier replays supplier isolation on five ports and all ten
retained pairs.  The no-import audit independently performs all six four-port
contractions with `Fraction` arithmetic and a separately assembled response
family.  These finite checks audit the formula and implementation; the written
contraction argument proves the arbitrary-root statement.

## One-active profile audit

For one active colour `c`, the left side is nonzero exactly when both
complement kernel projections have nonzero `c` coordinate.  In that case the
complement response restriction and retained supplier are nonzero and the
supplier is pure rank one.  Otherwise only `0=R_C k_D` remains.

With `T={u:e_c^* in Z_u}`, `GLS29` supplies `|T|>=2`.

- If `|T|=2`, its complementary pair is kernel-visible and forces `k_T` pure
  nonzero with a nonzero complementary response restriction.  Both endpoint
  channels cannot have rank two, because their full-rank `3 x 2` channel
  matrices compose through the invertible exchange matrix to a rank-two
  supplier.  Rank-one endpoints containing `e_c^*` are exactly its coordinate
  line.
- If `|T|=3` or `4`, every two-port complement meets `T`, so all
  complement-kernel identities have zero left side.  No supplier factor is
  inferred.

This is an exact conditional profile, not a legal-row theorem.  In particular,
a disjoint supplier or overlap cylinder can still absorb the pure normal
column.

## Two-active profile audit

Projection to the two active coordinates commutes with coordinatewise
products.  Hence each pair of projected kernels has Hadamard-product dimension
at most one.  A pure-axis generator forces a pure rank-one complementary
supplier; an oblique generator forces a rank-two active diagonal supplier.

Two projected kernel planes would have a two-dimensional product.  If one is
a plane, any other nonzero line must be a coordinate axis.  The local rank-one
and rank-two channel interpretations follow directly from projecting the
annihilator of a line or the kernel line of a plane.  Zero projected spaces and
zero-star products are retained rather than discarded.

The independent audit checks the support-dimension rule using a different
line/plane representation.  It does not substitute this finite support replay
for the written linear-algebra proof.

## Scalar controls and same-graph integration

The one-active control has `x_u=y_u=e_0^*` at every port, so every supplier is
`2E_00`.  Its six nonzero response scalars sum to `1/2`, giving exactly
`e_0^tensor 4`.  The two-active control has two `e_0` ports and two `e_1`
ports.  The within-block terms give the two pure tensors and the four nonzero
cross responses cancel one common mixed word with scalars `(1,1,1,-3)`.

In both controls every target has a nonzero disjoint supplier, so its
**normal** nuisance image is the full nine-dimensional target space.  This is
not a statement about the full 72-row transverse nuisance.

The physical-deck realization is exact.  All evaluated `Q`--port covectors are
zero, `W_(q_0,q_1)=E_00`, and the promoted edges are the declared responses;
therefore the physical four-vertex response formula is literally `R_D=W_D`.
The displayed residual-shore bases have the asserted normals and give `p=2`
and `p=-2`.  Direct eight-vertex matching evaluation checks all 81 normal
coefficients and all 54 pair-response coefficients in each graph.  The
no-import audit reconstructs both graphs and repeats those checks through a
separate recursive matching implementation.

These graphs certify response-deck integrability of the scalar controls only.
They are not claimed to satisfy the full top reconstruction, maximum-root
source gates, or complete GHZ equations.

## Maximum-root boundary graph audit

For the separate one-active graph:

- the residual shores are both `span{e_1^*,e_2^*}`, with `q=E_11+E_22`,
  `p=2`, and active normal colour zero;
- the five outside incidence ranks are `(2,2,2,2,3)`, with defect sum four;
- the three nowhere-zero monomial cliques
  `{a_0,q_0,q_1}`, `{a_1,u_2,u_3}`, and `{k,u_1}` cover every vertex;
- the displayed three root evaluations kill all internal root edges, so the
  root is a torus root of size three, while the clique cover proves no larger
  torus root exists;
- all six physical responses are nonzero because they are the nonzero direct
  promoted edges multiplied by `h_Q=1`;
- direct matching enumeration gives pure coefficients `(1,1,1)` and normal
  tensor `e_0^tensor 4`; and
- the mixed words `01000000` and `10000000` both have coefficient `-1/2`.

The last item is a positive non-witness certificate.  No exact Krenn--Gu
counterexample appears.  A separate exact nuisance replay during hostile
development found that this graph does not satisfy the full top-diagonal
reconstruction and has a surviving nonzero-response pair row.  Those facts
are not needed for the theorem, but they confirm that the graph cannot be used
against a claim assuming the complete zero-anchor or simultaneous-failure
gates.

## Rejected overclaims

The following proposed readings are false and are explicitly excluded:

1. one or two active normal colours are impossible from the scalar normal
   identity;
2. all six nonzero responses force a useful row;
3. full normal nuisance image is full transverse nuisance absorption;
4. maximum-root incidence plus pure normalization upgrades a scalar control to
   the complete witness locus;
5. a silent zero-star contraction permits either response or supplier factor
   to be cancelled;
6. the four-port profiles cover the higher-root disjoint-supplier branch;
7. this tranche covers other shore ranks or `C12/C21/C22`; or
8. this tranche closes the supply-and-target node or resolves the conjecture.

## Verification and provenance

The focused verifier uses SymPy dense matrices, five-port direct contractions,
explicit tensor assembly, and perfect-matching evaluation.  The independent
audit imports neither that verifier nor SymPy nor repository helpers; it uses
standard-library `Fraction`, sparse tuples, a reverse-order recursive matching
enumerator, and independently rebuilt controls.  Both check exceptional
zero-star behavior rather than dividing it away.

The theorem was derived from the committed `GLS29` normal identity and exact
physical definitions.  The controls were found by coefficientwise rational
construction and retained only after direct same-graph replay.  No literature
claim or external unretained model output is used as proof evidence.

## Final scope ledger

```text
arbitrary-root complement-kernel identity:              ACCEPTED;
four-port one-active conditional profile:                ACCEPTED;
four-port two-active projected-kernel profile:           ACCEPTED;
one-/two-active scalar response-deck controls:           ACCEPTED;
one-active maximum-root pure-normalized boundary graph:  ACCEPTED;

normal identity + six responses + full normal images
  imply divisor exclusion:                               REFUTED;
maximum-root + simultaneous scalar-normal absorption:    OPEN;
complete zero-anchor divisor exclusion:                  OPEN;
full GLS26 top reconstruction on the controls:           NOT CLAIMED;
full GLS22 nuisance absorption/survival:                  OPEN;
simultaneous legal useful-row failure:                    OPEN;
higher-root disjoint supplier branch:                    OPEN;
other shore ranks and C12/C21/C22:                       OPEN;
maximum-root supply/attachment strategic node:           OPEN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```
