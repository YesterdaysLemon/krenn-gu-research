# Odd-residual port extraction for the first blocker surplus

## Status

This is an exact arbitrary-order bridge lemma over `C`.  In a hypothetical
three-colour Krenn--Gu witness on any even number of vertices, let `r` fully
supported roots be pairwise zero-coupled.  If their total blocker union has
size `r+1`, then

```text
P_(r+1) -> Delta_3.                                    (1)
```

The earlier one-nonblocker theorem proved this only at order `2r+2`, where
there is a single vertex outside the roots and blockers.  The argument below
allows an arbitrary odd residual set.  Its whole matching contribution
becomes one additional linear row of the permanent.

For `r=4`, five blockers therefore extract `P_5 -> Delta_3` at every even
ambient order, not only at order ten.  For `r=5`, six blockers extract
`P_6 -> Delta_3`; this does not by itself produce a `P_5` restriction.

The later strict support theorem forces at least `3r+6` nonzero cells across
the contracted root rows and this residual port row.  Its graph-only sparse
cut consequence is recorded in
`GRAPH_EXTRACTION_STRICT_SUPPORT_TRANSFER_COROLLARY.md`.

## Setup

Let `V=C^3`, let the vertex set `Omega` have even size `n`, and let the
perfect-matching form of edge blocks `W_uv` satisfy

```text
H_W((z_v)_(v in Omega))
  = sum_(c=0)^2 product_(v in Omega) z_v[c].            (2)
```

Fix a root set `R` of size `r>=2` and vectors `x_i in V`, `i in R`, with

```text
x_i[c]!=0                         for every i and c,
B_ij(x_i,x_j)=0                   for distinct i,j in R. (3)
```

For every outside vertex `u`, define

```text
a_(i,u)(z)=B_iu(x_i,z),
A_u=span{a_(i,u):i in R} subset V*,
K_u=A_u^perp.                                           (4)
```

Let

```text
B_c={u outside R:e_c^* belongs to A_u},
B=B_0 union B_1 union B_2,                              (5)
```

and assume

```text
|B|=r+1.                                                (6)
```

Put

```text
Q=Omega minus (R union B).
```

Every vertex of `Q` is a nonblocker for all three colours.  Since

```text
|Q|=n-2r-1,
```

the set `Q` has positive odd size.

## Simultaneous-kernel torus contraction

For `q in Q`, the space `K_q` is nonzero.  Otherwise `A_q=V*` and `q`
would block every colour.  Moreover, for each `c`, containment

```text
K_q subset ker(e_c^*)
```

would imply `e_c^* in K_q^perp=A_q`, again contradicting that `q` is a
nonblocker.  A complex vector space is not the union of finitely many proper
linear subspaces, so choose independently

```text
z_q in K_q,
z_q[0]z_q[1]z_q[2]!=0,             q in Q.             (7)
```

These substitutions kill every root--`Q` edge while preserving all three
target-colour products.

## The residual port row

For each blocker `u in B`, let

```text
g_u(z)=H_(W restricted to {u} union Q)(z,(z_q)_(q in Q)). (8)
```

The set `{u} union Q` is even.  Expanding by the partner of `u` gives

```text
g_u(z)=sum_(q in Q) B_uq(z,z_q)
                     H_(W restricted to Q minus {q})((z_v)_v). (9)
```

with the empty matching polynomial equal to one.  Thus `g_u` is a linear
form in `z`.

Define, for each blocker mode, the local map

```text
M_u:V -> C^(r+1),
(M_u z)_i=a_(i,u)(z)       for i in R,
(M_u z)_star=g_u(z).                                  (10)
```

## Exact permanent factorisation

Restrict the root modes to `x_i`, the residual modes to (7), and keep every
blocker vector free.  In a nonzero perfect-matching monomial:

1. no two roots pair, by (3);
2. no root pairs with `Q`, by (4) and (7);
3. the `r` roots therefore pair injectively with `r` distinct blockers;
4. one blocker `u` remains, and the matching on `{u} union Q` contributes
   exactly `g_u(z_u)`.

Conversely every choice in steps 3--4 is a surviving matching.  Summing first
over the leftover blocker and then over the root--blocker bijection is the
row expansion of a permanent:

```text
H_W restricted to (x_R,V^B,z_Q)
  = per([a_(i,u)(z_u)]_(i in R,u in B);
        [g_u(z_u)]_(u in B))
  = (tensor_(u in B) M_u)^* P_(r+1).                  (11)
```

This is a monomial-by-monomial identity.  It does not assume that any
residual matching scalar is nonzero and does not select a preferred vertex
of `Q`.

## The target forces a concise diagonal

Under the same substitutions, the right side of (2) becomes

```text
sum_(c=0)^2 lambda_c product_(u in B) z_u[c],
lambda_c=(product_(i in R) x_i[c])
         (product_(q in Q) z_q[c]).                    (12)
```

All three `lambda_c` are nonzero by (3) and (7).  Equations (11)--(12) give
a local restriction of `P_(r+1)` to a three-term concise diagonal.  An
invertible diagonal rescaling in one blocker mode normalizes the three
coefficients to one, proving (1).  Conciseness also forces every map `M_u`
to have rank three; no rank assumption was inserted.

## Consequence for the local-to-global chain

For an arbitrary five-vertex set, the ten internal bilinear forms always
have a projective common zero.  This alone does not give a fully supported
root tuple.  Avoiding the fifteen boundary resultants does give such a tuple.
For five fully supported roots, the exact alternatives now begin

```text
five blockers  -> P_5 -> Delta_3,
six blockers   -> P_6 -> Delta_3,
at least seven blockers -> deeper surplus branch.      (13)
```

The second arrow is the case `r=5` of this theorem.  There is currently no
proved implication `P_6 -> Delta_3` implies `P_5 -> Delta_3`; contracting a
sixth permanent mode produces a general support-up-to-six contraction, not
automatically a coordinate `P_5` slice.

The case `r=4` sharpens the transverse-boundary route.  Whenever four fully
supported pairwise-zero roots have total blocker union five, they extract
`P_5 -> Delta_3` at arbitrary even order, even if there are many residual
nonblockers.

Thus an actual global proof still needs all of the following:

1. force a torus five-root tuple, or control the boundary-resultant locus;
2. exclude the permanent restrictions produced at the first surplus levels,
   beginning with `P_5 -> Delta_3` and now also `P_6 -> Delta_3`;
3. control blocker union at least seven, or extend the port construction to
   several leftover blockers; and
4. complete the special/boundary local-restriction analysis needed for a
   genuine nonrestriction theorem.

The lemma closes a contraction gap, not those remaining quantifier and
classification gaps, and it does not resolve the Krenn--Gu conjecture.

## Replay

```text
python verify_odd_residual_port_permanent_extraction.py
python audit_odd_residual_port_permanent_extraction.py
```

The primary verifier compares the surviving matching polynomial and the
port-row permanent monomial by monomial for several independent `(r,|Q|)`
sizes and checks the exact counting formula.  The independent audit uses a
separate hafnian recurrence with deterministic integer edge weights and
checks the diagonal rescaling.  These finite checks audit the formulas; the
proof above is the arbitrary-order argument over `C`.
