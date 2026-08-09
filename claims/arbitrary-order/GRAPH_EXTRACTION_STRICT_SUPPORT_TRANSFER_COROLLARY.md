# Graph-extraction strict-support transfer corollary

## Status

The arbitrary permanent bound

```text
support(P_m -> Delta_3)>=3m+3                        (1)
```

has exact graph-side consequences whenever one of the repository's
root--blocker extraction theorems applies.  It excludes the former equality
shell in every extracted permanent cell; it does not force such an
extraction in every hypothetical graph witness.

The strongest transfers proved here, including the 3 August two-residual
addendum, are:

```text
five roots + five tight blockers:       I>=18;
r roots + r+1 blockers + one port:      I+p>=3r+6;
r roots + r+2 blockers + exactly two residuals:
  beta coordinate monomial, or I+p_0+p_1>=3r+9.     (2)
```

The second line gives `I+p>=18` for four roots/five blockers and
`I+p>=21` for five roots/six blockers.  In the third line the exact
two-residual torus dichotomy makes the synchronized factorization automatic
on the non-coordinate branch.  The coordinate-monomial branch remains open,
and four or more residual vertices do not admit this one-channel conclusion.

These are active contraction-support inequalities, not bounds on the total
edge count of the original graph.

The exact inputs are
[`FIVE_ROOT_TIGHT_BLOCKER_P5_EXTRACTION.md`](FIVE_ROOT_TIGHT_BLOCKER_P5_EXTRACTION.md),
[`ODD_RESIDUAL_PORT_PERMANENT_EXTRACTION.md`](ODD_RESIDUAL_PORT_PERMANENT_EXTRACTION.md),
[`TWO_PORT_SEVEN_BLOCKER_REDUCTION.md`](TWO_PORT_SEVEN_BLOCKER_REDUCTION.md),
and the support theorem
[`ARBITRARY_PERMANENT_THREE_M_PLUS_TWO_SUPPORT_BOUND.md`](ARBITRARY_PERMANENT_THREE_M_PLUS_TWO_SUPPORT_BOUND.md).
The two-residual addendum is proved and replayed separately in
[`ARBITRARY_ORDER_TWO_RESIDUAL_STRICT_SUPPORT_STAIRCASE_AND_COORDINATE_FORCING.md`](ARBITRARY_ORDER_TWO_RESIDUAL_STRICT_SUPPORT_STAIRCASE_AND_COORDINATE_FORCING.md).

## Active root--blocker support

Let `R` be a set of fully supported pairwise zero-coupled root vectors
`x_i`, and let `B` be the relevant blocker union.  For every root--blocker
pair define

```text
a_(i,u)(z)=B_iu(x_i,z),       i in R, u in B,
I(R,B)=#{(i,u):a_(i,u) is not the zero form}.         (3)
```

The count `I` can be smaller than the number of nonzero graph edge blocks:
a nonzero block may vanish after contraction by `x_i`.

## Five tight blockers

The tight five-root extraction theorem gives maps

```text
L_u: C^3 -> C^5,
(L_u z)_i=a_(i,u)(z),                                (4)
```

and a concise restriction `P_5 -> Delta_3`.  Its physical row-cell support
is exactly `I(R,B)`.  Applying (1) at `m=5` gives

```text
I(R,B)>=18.                                          (5)
```

Thus a five-root/five-blocker cell with at most seventeen active contracted
root--blocker forms is impossible.  This is valid at arbitrary ambient even
order under the exact extraction hypotheses.

## First blocker surplus and one residual port

For `r` roots and `r+1` blockers, the odd-residual extraction theorem adds
one linear port form at each blocker:

```text
g_u(z)=H_({u} union Q)(z,z_Q),
p=#{u in B:g_u is not the zero form}.                (6)
```

The extracted maps have rows `a_(i,u)`, `i in R`, and `g_u`.  Their support
is exactly `I+p`, and they give `P_(r+1) -> Delta_3`.  Equation (1) with
`m=r+1` yields

```text
I(R,B)+p>=3(r+1)+3=3r+6.                             (7)
```

Consequently the complete `3r+5` equality shell of the earlier lower bound
is excluded in every one-port extraction.  In particular,

```text
r=4, five blockers:  I+p>=18;
r=5, six blockers:   I+p>=21.                        (8)
```

## A graph-only sufficient contradiction

Write `e_G(R,B)` for the number of nonzero original edge blocks between the
roots and blockers, and `e_G(B,Q)` for those between blockers and the odd
residual set.  Then

```text
I(R,B)<=e_G(R,B).                                    (9)
```

Moreover `g_u!=0` requires at least one nonzero blocker--residual edge
incident with `u`, by the exact partner expansion defining `g_u`.  Choosing
one such edge for each nonzero port gives

```text
p<=e_G(B,Q).                                        (10)
```

Hence the purely graph-side condition

```text
e_G(R,B)+e_G(B,Q)<=3r+5                              (11)
```

contradicts (7).  The active-covector inequality (7) is sharper than (11),
because nonzero graph blocks can contract to zero.

At minimum ambient order `2r+2`, the residual set is one vertex and the
extraction is a contracted active `(r+1) x (r+1)` bipartite cut.  Original
root--root or blocker--blocker blocks may still exist, but do not occur after
the extraction substitutions.  Thus (11) excludes:

```text
ten vertices:    an extracted 5 x 5 cut with <=17 edges;
twelve vertices: an extracted 6 x 6 cut with <=20 edges. (12)
```

The numbers in (12) concern the extracted cut, not the graph's total edge
count and not the older unrelated eight-vertex seventeen-edge statement.

## Exact two-residual transfer and the higher-residual boundary

For `r` roots and `r+2` blockers with exactly two residual nonblockers, let
`beta` be the residual edge restricted to their simultaneous-kernel spaces.
If `beta` is not a nonzero coordinate monomial, the torus-zero theorem
chooses coordinatewise-nonzero kernel vectors with residual value zero and
gives a synchronized factorization with common port rows
`g_(0u),g_(1u)`.  Define

```text
p_j=#{u:g_(ju) is not the zero form}.                (13)
```

The factorization extracts `P_(r+2) -> Delta_3` with support
`I+p_0+p_1`.  Equation (1) gives

```text
I+p_0+p_1>=3(r+2)+3=3r+9.                           (14)
```

For five roots and seven blockers, this is `I+p_0+p_1>=24`, excluding the
old `23` shell on every non-coordinate two-residual branch.  Equivalently,
a displayed root--blocker--residual graph cut of size at most `3r+8` forces
`beta` to be a nonzero coordinate monomial.  This is the exact conclusion of
`ARBITRARY_ORDER_TWO_RESIDUAL_STRICT_SUPPORT_STAIRCASE_AND_COORDINATE_FORCING.md`.

This addendum does not make a general two-port cofactor one-channel.  For
every even residual order at least four there are torus-zero residual
matrices with full-rank cofactor form, as proved in
`RESIDUAL_HAFNIAN_COMMON_GRAM_AUDIT_AND_TORUS_ZERO_FULL_RANK_SHARPNESS.md`.

## Exact global target

To turn (1) into a global Krenn--Gu contradiction, it is enough to force in
every hypothetical witness one of the established extractions with support
at most `3m+2`.  Numerically the sharp targets are

```text
P_5 extraction: support <=17;
P_6 extraction: support <=20;
P_7 extraction: support <=23.                        (15)
```

An upper bound of `3m+3` is insufficient because that first surviving layer
remains unresolved.  The five-root route still has boundary-resultant and
blocker-surplus branches; the exactly-two-residual route still has the
coordinate-monomial boundary, while larger residual systems remain
multichannel.

## Verification

Run:

```text
python claims/arbitrary-order/verify_graph_extraction_strict_support_transfer_corollary.py
python claims/arbitrary-order/audit_graph_extraction_strict_support_transfer_corollary.py
```

The original primary verifier checks every affine support substitution and
the named `P_5,P_6,P_7` values.  The original independent no-import audit
reconstructs the inequality table from the permanent order.  The new
two-residual package separately checks the exact matching recursion, torus
dichotomy representatives, two-row permanent transport, cut arithmetic, and
an independent assignment audit.  The written extraction theorems and the
implications (9)--(10) are the symbolic proof; no graph or matching census is
performed.

## Boundary

```text
strict local support bound:              3m+3;
five-root/five-blocker active support:   AT LEAST 18;
r/(r+1) one-port active support:         AT LEAST 3r+6;
r/(r+2) exactly-two-residual support:     COORDINATE, OR AT LEAST 3r+9;
graph-only one-port sparse-cut shell:    EXCLUDED BY (11);
graph-only two-residual cut <=3r+8:       COORDINATE MONOMIAL FORCED;
forced sparse extraction in every graph: NOT PROVED;
global Krenn--Gu conjecture:              UNRESOLVED.
```
