# One-nonblocker surplus extracts the next permanent tensor

## Status

This is an exact arbitrary-`r` bridge lemma over `C`.  In a hypothetical
three-colour GHZ witness on `2r+2` vertices, let `r` fully supported roots
be pairwise zero-coupled.  If their total blocker union has size `r+1`, so
that exactly one outside vertex is a nonblocker for all three colours, then

```text
P_(r+1) -> Delta_3.                                    (1)
```

For `r=4`, this says that a ten-vertex four-root/five-blocker configuration
extracts the unresolved `P_5` restriction.  The theorem does not exclude
`P_(r+1) -> Delta_3`, and it says nothing when there are additional
nonblocker or residual vertices.

## Setup

Let `V=C^3`, and let `B_uv` be the bilinear edge blocks of a hypothetical
`n=2r+2` vertex witness whose perfect-matching form obeys

```text
H_B((z_v)_v)=sum_(c=0)^2 product_v z_v[c].             (2)
```

Fix a root set `R` of size `r>=2` and vectors `x_i in V` satisfying

```text
x_i[c]!=0                         for every i and c,
B_ij(x_i,x_j)=0                   for distinct i,j in R. (3)
```

For every outside vertex `u`, put

```text
a_(i,u)(z)=B_iu(x_i,z),
A_u=span{a_(i,u):i in R},
K_u=A_u^perp.                                           (4)
```

Here the notation fills the root slot of the edge block with `x_i` and
leaves the outside-vertex slot free, irrespective of the numerical order
of the vertex labels.

Let

```text
B_c={u outside R:e_c^* belongs to A_u}
```

be the colour-`c` blocker set and

```text
B=B_0 union B_1 union B_2.
```

Assume `|B|=r+1`.  Since there are `r+2` vertices outside `R`, there is a
unique remaining vertex

```text
q notin R union B.                                      (5)
```

## Theorem and proof

Because `q` blocks no colour, `K_q` is nonzero: otherwise `A_q=V*`.
Moreover, containment `K_q subset ker(e_c^*)` would imply
`e_c^* in K_q^perp=A_q`, making `q` a colour-`c` blocker.  Thus `K_q` is
not contained in any of the three coordinate hyperplanes.  Over the
infinite field `C`, a vector space cannot be the union of finitely many
proper linear subspaces.  Choose

```text
z_q in K_q,
z_q[0]z_q[1]z_q[2]!=0.                                  (6)
```

Keep the `r+1` blocker vectors `z_u`, `u in B`, free.  Define maps with
rows indexed by `R union {q}`:

```text
M_u:V -> C^(r+1),
(M_u z)_i = B_iu(x_i,z)        for i in R,
(M_u z)_q = B_qu(z_q,z).                              (7)
```

Under this restriction, every nonzero perfect matching has the following
form.  No two roots pair by (3), and no root pairs with `q` because
`z_q in K_q`.  Thus the `r` roots use `r` distinct blockers.  Exactly one
blocker remains, and it must pair with `q`.  A blocker--blocker edge would
leave too few blockers for the roots.  Hence the surviving matchings are
exactly the bijections

```text
R union {q} -> B.                                       (8)
```

Their sum is the pullback of the order-`r+1` permanent tensor:

```text
(tensor_(u in B) M_u)^* P_(r+1).                       (9)
```

The GHZ side of the same restriction is

```text
sum_(c=0)^2 lambda_c product_(u in B) z_u[c],
lambda_c=z_q[c] product_(i in R) x_i[c].              (10)
```

All three `lambda_c` are nonzero by (3) and (6).  An invertible diagonal
rescaling in one blocker mode changes (10) to `Delta_3`.  Equations
(9)--(10) prove (1).  Conciseness of the target also forces every `M_u` to
have rank three; no rank assumption was inserted.

## Consequences

At order ten, four fully supported pairwise-zero roots have six outside
vertices.  The multi-star theorem gives a total blocker union of size at
least four.  The size-four case is impossible because `P_4` has subrank
two.  The theorem above identifies the next case exactly:

```text
five blockers -> P_5 -> Delta_3,
six blockers  -> persistent-surplus branch.           (11)
```

Thus excluding `P_5 -> Delta_3` would force all six outside vertices into
the blocker union.  This is a sharp classification, not a contradiction.

At order twelve, five fully supported pairwise-zero roots with a six-vertex
blocker union analogously extract `P_6 -> Delta_3`; no nonrestriction theorem
for that tensor is asserted here.

## Replay

```text
python verify_one_nonblocker_surplus_permanent_extraction.py
python audit_one_nonblocker_surplus_permanent_extraction.py
```

The primary verifier enumerates the surviving matching class through
`r=6`, checks its bijection with permutations, and checks the three-term
rescaling.  The independent audit uses a separate hafnian dynamic program
and exhausts the simultaneous-kernel torus lemma over `F_5`.  The written
argument is over `C` and arbitrary `r`.
