# Arbitrary permanent equality two-switch port-completion shore theorem

## Status

This is an exact arbitrary-order dichotomy inside the sole two-switch branch
of hypothetical `3m+2` equality.  It does not enumerate supports, words, or
matchings.

The direct mixed-backbone completion that forces the rectangle between the
two degree-four switch modes exists if and only if one switch-independent
residual graph has a perfect matching.  If that completion fails, a minimal
Hall-deficient residual set produces a connected shore of exact coloured cut
type

```text
(1,1,1) or (1,1,3).                                  (1)
```

An explicit six-mode symbolic support satisfies the equality degree ledger,
local rank three, exactly two pure switches, and every source-subset Hall
quota, but has a shore of type `(1,1,3)`.  It is not a full equality
restriction.  It proves that the ledger, localization, pure-cube structure,
local concision, and deletion quotas alone cannot force the desired port
completion.  Subsequent theorems exclude `(1,1,1)` by full-support tight-cut
flattening and `(1,1,3)` by a five-port Kempe exchange.  Consequently the
residual completion must exist in every hypothetical two-switch equality
survivor.

## Two-switch support normal form

Let `c,d` be the switchable colours and `e` the third colour.  Use the notation
of the excess-plane separation theorem:

- the two noncoordinate excess cells are at mode `a` and sources `p_1,p_2`;
- `b_c,b_d` are the degree-four mandatory switch modes;
- the unique coordinate cell at `a` has colour `e` and source
  `q notin {p_1,p_2}`.

Put

```text
A_0={a,b_c,b_d},       Q={q,p_1,p_2}.                (2)
```

Choose any one of the four pure backbones

```text
H=M_c union M_d union M_e                            (3)
```

and delete the modes and sources in (2):

```text
R=H-A_0-Q.                                           (4)
```

Every mode outside `A_0` has degree three, is coordinate-only, and has one
cell of each colour.  Every nonexceptional mandatory cell is forced in its
colour matching.  Hence (4) is also the full physical support induced on the
residual modes and sources, and it is independent of both switch bits.

## Port-completion equivalence

The following are equivalent.

1. `R` has a perfect matching.
2. An opposite-source backbone fibre has a mixed perfect matching containing

   ```text
   a --e--> q,
   b_c --c--> p_s,
   b_d --d--> p_(3-s)                                (5)
   ```

   for one `s in {1,2}`.

If `K` is a perfect matching of `R`, adjoining the three edges (5) covers all
modes and sources exactly once and gives the required mixed matching.
Conversely, deleting (5) from such a matching leaves a perfect matching of
`R`.

The exceptional-source rectangle theorem applies to the matching in (5).
Its unique cross partner transposes the two switch-mode edges at
`p_1,p_2`.  Equality therefore forces

```text
r_(b_c,p_1)[c] r_(b_d,p_2)[d]
+r_(b_c,p_2)[c] r_(b_d,p_1)[d]=0.                   (6)
```

Equivalently,

```text
g_(b_c,c)=-g_(b_d,d).                                (7)
```

Thus the direct backbone route to the third port rectangle is a residual Hall
question, not a matchgate deletion identity.  When `R` has no perfect
matching, equation (6) could still be an algebraic consequence of other
mixed coefficients; no claim to the contrary is made.

## Necessary conditions for failure

Let

```text
q_c=source of the coordinate c-cell at b_d,
q_d=source of the coordinate d-cell at b_c.          (8)
```

If `q_c=q`, then `M_c(A_0)=Q`, and the restriction of `M_c` to (4) is a
perfect matching of `R`.  Similarly, `q_d=q` lets `M_d` complete `R`.
Therefore failure of (6) through this route requires

```text
q_c!=q,       q_d!=q.                                (9)
```

Assume from now on that `R` has no perfect matching.  Choose an
inclusion-minimal Hall-deficient set `S` of residual modes and put

```text
T=N_R(S).                                            (10)
```

The only coloured backbone edges from residual modes into the deleted source
set `Q` are the four ports

```text
u_c=M_c^(-1)(q),
u_d=M_d^(-1)(q),
u_(e,1)=M_e^(-1)(p_1),
u_(e,2)=M_e^(-1)(p_2).                               (11)
```

There is one `c` port, one `d` port, and two `e` ports.  Since `M_h(S)` has
`|S|` distinct sources inside `T union Q`, each colour must use at least
`|S|-|T|` of its available ports.  Colour `c` has only one, while Hall
deficiency gives `|T|<|S|`.  Hence

```text
|T|=|S|-1,                                           (12)
u_c,u_d in S,
{u_(e,1),u_(e,2)} intersect S !=empty.               (13)
```

The modes `u_c,u_d` are distinct: otherwise the same coordinate-only
physical cell at source `q` would have to carry both coordinate colours.

The switch-colour restrictions are exact bijections

```text
M_c:S-{u_c} -> T,
M_d:S-{u_d} -> T.                                   (14)
```

Consequently the internal graph of `M_c union M_d` on `S union T` consists
of one alternating path from `u_c` to `u_d` plus disjoint alternating
cycles.

Minimality makes `R[S,T]` connected.  Otherwise each connected component
would correspond to a proper subset of `S`; minimality makes every such
subset Hall-sufficient, contradicting the total deficit one in (12).

## Exact shore cut types

Let

```text
k=|{u_(e,1),u_(e,2)} intersect S| in {1,2}.          (15)
```

If `k=1`, the restriction of `M_e` from `S` minus its one port mode is a
bijection onto `T`.  If `k=2`, the remaining `e`-edges from `S` miss exactly
one source of `T`, whose `e`-preimage lies outside `S`.

For the shore

```text
W=S union T,                                         (16)
```

count both matching edges leaving a mode in `S` and matching edges entering
a source in `T` from outside `S`.  Equations (14)--(15) give

```text
|delta_(M_c)(W)|=1,
|delta_(M_d)(W)|=1,
|delta_(M_e)(W)|=2k-1.                               (17)
```

Thus every failed completion contains exactly one of the connected shore
types in (1).  This is the sharp tight-cut/Dulmage--Mendelsohn normal form for
the residual obstruction.

## Exact structural countermodel

The following fixed support has `m=6`.  Its sources are
`p_1,p_2,q,t,r,s`, its modes are `a,b_c,b_d,x,y,z`, and coordinate entries
have weight one:

```text
a:    p_1:(1,1,0), p_2:(1,2,0) noncoordinate; q:e
b_c:  p_1:c, p_2:c, s:d, r:e
b_d:  p_1:d, p_2:d, r:c, s:e
x:    q:c, t:d, p_1:e
y:    t:c, q:d, p_2:e
z:    s:c, r:d, t:e.                                 (18)
```

It has `20=3m+2` physical cells, degree ledger `3,4,4,3,3,3`, and rank three
at every mode.  Representative pure matchings are

```text
M_c=(a,p_1),(b_c,p_2),(b_d,r),(x,q),(y,t),(z,s),
M_d=(a,p_1),(b_d,p_2),(b_c,s),(x,t),(y,q),(z,r),
M_e=(a,q),(b_c,r),(b_d,s),(x,p_1),(y,p_2),(z,t).     (19)
```

Colours `c,d` each have exactly the displayed exceptional-source switch;
colour `e` is unique.  After deleting (2),

```text
N_R({x,y})={t},                                      (20)
```

so `R` has no perfect matching.  Here `S={x,y}`, `T={t}`, and the shore has
cut type `(1,1,3)`.

The support also satisfies every source-subset Hall quota without a subset
search.  For colour `c`, the coordinate source-to-mode map is injective
except that `p_1,p_2` both map to `b_c`; when both are selected, the excess
rows at mode `a` span the `c,d` plane and restore the missing quota mode.
Colour `d` is identical with `b_d`.  The coordinate `e` cells occupy six
distinct modes.  Hence every source subset `S` has at least `|S|` modes whose
`S`-row span contains the required coordinate covector, exactly as demanded
by the kernel-deletion hierarchy.

This is not a solution of the mixed coefficient equations and is not an
equality construction.  It is a structural countermodel showing that the
current ledger, localization, pure-switch, local-rank, and Hall tools do not
imply port completion.

## Literature translation

Hall deficiency and the canonical decomposition of bipartite matching
structure are classical; see Dulmage and Mendelsohn,
[*Coverings of Bipartite Graphs*](https://doi.org/10.4153/CJM-1958-052-0).
What is problem-specific is the port count in (11): the equality support
ledger collapses every minimal failure to one alternating switch-colour path
and a three- or five-edge coloured shore.

This suggests a tight-cut induction rather than a support census.  Contract
the connected shore while retaining its three or five port values, then use
the mixed coefficient equations to constrain the boundary signature.  The
three-edge signature is excluded by the rank-two Laplace factorization in
`ARBITRARY_PERMANENT_EQUALITY_THREE_EDGE_SHORE_FLATTENING_EXCLUSION.md`.
The five-edge signature is excluded by the boundary-pairing argument in
`ARBITRARY_PERMANENT_EQUALITY_FIVE_EDGE_SHORE_KEMPE_EXCLUSION.md`.  The
explicit model (18) remains a guardrail: Hall quotas and local ranks alone do
not perform the latter step; mixed-coefficient localization is essential.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_equality_two_switch_port_completion_shore_theorem.py
python audit_arbitrary_permanent_equality_two_switch_port_completion_shore_theorem.py
```

The primary verifier checks the rectangle-to-gain equation and the complete
ledger, local ranks, pure matchings, Hall defect, and analytic quota pattern
of (18).  The independent no-import audit checks the shore cut counts from
(19) and the deficit-one port arithmetic.  They are fixed exact checks of
the stated construction and formulas, not a support or matching search.

## Boundary

```text
direct mixed-matching rectangle route:   IFF RESIDUAL R HAS PERFECT MATCHING;
no-completion Hall deficit:              EXACTLY ONE;
switch-colour shore cuts:                (1,1);
third-colour shore cut:                  1 OR 3;
no-completion shore types:               (1,1,1) OR (1,1,3);
(1,1,1) shore:                           EXCLUDED SUBSEQUENTLY;
(1,1,3) shore:                           EXCLUDED SUBSEQUENTLY;
residual R in equality:                  HAS A PERFECT MATCHING;
direct port-completion rectangle:        FORCED;
ledger/rank/Hall force completion:        NO;
two-switch equality stratum:             EXCLUDED SUBSEQUENTLY;
global Krenn--Gu conjecture:              UNRESOLVED.
```
