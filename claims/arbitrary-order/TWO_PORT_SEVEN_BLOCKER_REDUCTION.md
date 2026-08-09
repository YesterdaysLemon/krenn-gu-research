# The seven-blocker surplus is an exact two-port tensor

## Status

**Exact arbitrary-order characteristic-zero reduction.**  Let `r` fully
supported roots of a hypothetical three-colour GHZ realization be pairwise
zero-coupled, and let their total blocker union have size `r+s`.  After
choosing simultaneous-kernel vectors at the residual nonblockers, every
surviving matching is classified by the `s` blockers not paired to roots.
The restricted identity is

```text
sum_(S subset B, |S|=s) per(A_(B\S)) H_(Q union S)
  = sum_(c=0)^2 lambda_c product_(u in B) z_u[c],    (1)
```

with every `lambda_c` nonzero.  The known tight and one-port lemmas are the
cases `s=0,1`.

For five roots and seven blockers, `s=2`: the residual cofactor is bilinear,
not another row of a permanent.  The minimally incident seven-blocker cell
has one triple blocker and two blockers of each double type.  It contains
three overlapping pure `P_5` restrictions.  Excluding that shared system is
the sharp next finite local-to-global problem.

This theorem does not exclude the two-port tensor and does not prove a
`P_6` or `P_7` nonrestriction.  The Krenn--Gu conjecture remains
**UNRESOLVED**.

If the synchronized representation below did hold, the later strict support
theorem would force at least 24 active cells in the resulting `P_7`
extraction.  That consequence remains conditional on synchronization; see
`GRAPH_EXTRACTION_STRICT_SUPPORT_TRANSFER_COROLLARY.md`.

## Matching factorization

Let `R` be the roots, `B` their blocker union, and `Q` the remaining outside
vertices.  Choose

```text
z_q in K_q=intersection_(i in R) ker B_iq(x_i,-),
z_q[0]z_q[1]z_q[2]!=0                              (2)
```

for every `q in Q`.  The usual finite-union argument over `C` supplies such
vectors whenever `q` blocks no colour.

No surviving matching contains a root--root or root--nonblocker edge.  The
`r` roots therefore use `r` distinct blockers.  If `S` is the set of unused
blockers, then `|S|=s`, the root--blocker contribution is

```text
F_S=per([B_iu(x_i,z_u)]_(i in R,u in B\S)),         (3)
```

and the remaining matching sum is the perfect-matching form

```text
H_(Q union S).                                     (4)
```

Conversely a root--blocker bijection and a perfect matching on `Q union S`
give one surviving matching.  This bijection proves (1), term by term.  The
GHZ coefficients are

```text
lambda_c=product_(i in R)x_i[c] product_(q in Q)z_q[c], (5)
```

and are nonzero by full support and (2).

## Five roots and seven blockers

At order twelve, take `r=5`, `|B|=7`, and `Q` empty.  Equation (1) becomes

```text
sum_(u<v) G_uv(z_u,z_v) F_uv(z_(B\{u,v}))
  = sum_c lambda_c product_(u in B)z_u[c],          (6)
```

where

```text
G_uv=H_{u,v}=B_uv,       F_uv=per(A_(B\{u,v})).    (7)
```

Thus (6) is a genuine two-port tensor.  A synchronized representation

```text
G_uv=g_(0u)g_(1v)+g_(1u)g_(0v)                    (8)
```

would add two common port rows and extract `P_7 -> Delta_3`, not `P_6`.
Equation (8) is not automatic: an edge block can have rank three, whereas
the right side has rank at most two.

## The canonical minimal incidence cell

Let

```text
I_u={c:u belongs to B_c}.                           (9)
```

Each colour has at least five blockers, hence

```text
sum_u |I_u| >=15.                                  (10)
```

Seven proper blocker spans contribute at most fourteen incidences, so some
blocker has `I_u={0,1,2}` and therefore `A_u=(C^3)^*`, `K_u=0`.  If `t_j`
counts vertices with `|I_u|=j`, then

```text
t_3-t_1>=1.                                        (11)
```

In the minimally incident case `|B_c|=5` for all colours, if there is exactly
one triple blocker then (10)--(11) force

```text
012, 01,01, 02,02, 12,12.                         (12)
```

A double-type blocker has a one-dimensional simultaneous kernel: type `12`
has kernel `C e_0`, and cyclically.  Fix the two type-`12` modes at `e_0`.
Every term of (6) vanishes except their common cofactor, while the GHZ side
is a nonzero colour-zero monomial.  Hence the other five modes restrict to a
nonzero pure `P_5`.  Cyclically, (12) contains the three systems

```text
012+01+01+02+02 -> e_0^(tensor 5),
012+01+01+12+12 -> e_1^(tensor 5),
012+02+02+12+12 -> e_2^(tensor 5).                 (13)
```

The three systems share one rank-three mode and four modes at a time.  Their
compatibility uses the full matching identity and cannot be decided by the
incidence count alone.

## Replay

```text
python claims/arbitrary-order/verify_two_port_seven_blocker_reduction.py
python claims/arbitrary-order/audit_two_port_seven_blocker_reduction.py
```

The primary replay enumerates the matching bijection and the canonical type
ledger, including surplus three and nonempty residual sets.  The independent
finite combinatorial audit checks the same higher-surplus counts.  Those
finite checks are explicitly diagnostic of the fixed combinatorics only; the
written theorem and primary identities are over characteristic zero.
