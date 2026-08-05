# Tight five-root blockers extract an order-five permanent restriction

## Status

**Exact arbitrary-order bridge lemma over `C`.**  In a hypothetical
three-colour Krenn--Gu witness, let five fully supported root vectors be
pairwise zero-coupled.  If the union of their blocker vertices over the
three colours has the minimum possible size five, then those five blockers
carry a concise local restriction

```text
P_5 -> Delta_3.
```

Consequently, once `P_5 -> Delta_3` is excluded, every such five-root tuple
must have at least six distinct blockers in total.

This is the missing exact extraction step between the arbitrary-order
multi-star theorem and the finite `P_5` programme.  It is **not** a global
proof: the five-root intersection may lie entirely on coordinate
hyperplanes, and a fully supported five-root tuple may have six or more
blockers.

Combined with the later strict support theorem, this extraction requires at
least 18 nonzero contracted root--blocker covectors.  See
`GRAPH_EXTRACTION_STRICT_SUPPORT_TRANSFER_COROLLARY.md`.

## Setup

Let `V=C^3`, let the vertex set have even size, and write

```text
B_ij(x_i,x_j)=transpose(x_i) W_ij x_j
```

for the bilinear edge block.  Assume the full matching tensor is the
three-colour diagonal tensor

```text
H_W((x_v)_v)=sum_(c=0)^2 product_v x_v[c].          (1)
```

Fix a five-element root set `R` and vectors `x_i in V`, `i in R`, such
that

```text
x_i[c] != 0                    for every i in R and c=0,1,2,
B_ij(x_i,x_j)=0                for distinct i,j in R.       (2)
```

For every outside vertex `u`, define

```text
a_(i,u)(z)=B_iu(x_i,z),
A_u=span{a_(i,u):i in R} subset V*,
K_u=intersection_(i in R) ker(a_(i,u))=A_u^perp.    (3)
```

Let

```text
B_c={u outside R:e_c^* belongs to A_u}              (4)
```

be the colour-`c` blocker set, and put

```text
B=B_0 union B_1 union B_2.                           (5)
```

The
[`MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md`](MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md)
gives

```text
|B_c| >= 5                    for c=0,1,2.           (6)
```

## Theorem

If `|B|=5`, then the five blocker modes support linear maps

```text
L_u:V -> C^5,       (L_u z)_i=a_(i,u)(z),           (7)
```

for which the pullback of the order-five permanent tensor is a concise
three-term diagonal:

```text
(tensor_(u in B) L_u)^* P_5
  = mu_0 (e_0^*)^(tensor 5)+mu_1 (e_1^*)^(tensor 5)
    +mu_2 (e_2^*)^(tensor 5),

mu_0 mu_1 mu_2 != 0.                                 (8)
```

After an invertible diagonal rescaling in one blocker mode, (8) is
`Delta_3`.  Thus `P_5` restricts to `Delta_3`.

## Proof

### The five blockers are common to all three colours

Equation (6) and `B_c subset B` imply, when `|B|=5`, that

```text
B_0=B_1=B_2=B.                                       (9)
```

Let

```text
Q={all vertices} minus (R union B).
```

Every `w in Q` is a nonblocker for all three colours.

### Every residual simultaneous kernel meets the coordinate torus

For `w in Q`, the space `K_w` is nonzero.  Otherwise `A_w=V*`, which
would contain every coordinate covector and make `w` a blocker.  Moreover,
for each colour `c`,

```text
K_w is not contained in ker(e_c^*).                  (10)
```

Indeed, containment in (10) would give

```text
e_c^* in K_w^perp=(A_w^perp)^perp=A_w,
```

again contradicting that `w` is a nonblocker.  A linear space over the
infinite field `C` cannot be the union of three proper linear subspaces.
Hence one can choose

```text
z_w in K_w with z_w[0]z_w[1]z_w[2] != 0             (11)
```

independently for every `w in Q`.  When `Q` is empty this choice is
vacuous.

### Exact matching factorisation

Keep the five blocker vectors `z_u`, `u in B`, arbitrary, and restrict
every residual vector to `K_w`.  In any nonzero perfect-matching monomial:

1. no two roots can be paired, by the second condition in (2);
2. no root can be paired to a residual vertex, by (3);
3. therefore every root must be paired to a distinct blocker;
4. because there are five roots and five blockers, these root--blocker
   edges form a bijection, and all residual vertices pair among themselves.

The surviving matchings are therefore exactly the Cartesian product of a
bijection `R -> B` and a perfect matching of `Q`.  Their weight sum factors
as

```text
H_W restricted to (x_R,V^B,K_Q) = F_B H_Q,           (12)

F_B((z_u)_(u in B))
 = per([a_(i,u)(z_u)]_(i in R,u in B)),              (13)
```

where `H_Q` is the matching polynomial of the edge blocks induced by `Q`.
Since the total vertex count and `|R union B|=10` are even, `|Q|` is even.
For `Q=empty`, use `H_Q=1`.

Equation (13) is precisely the pullback of `P_5` by the five maps (7).
Dually, their transposes are the local tensor maps in the usual
`P_5 -> Delta_3` convention.  No rank or conciseness assumption on those
maps has been inserted.

### The target forces all three diagonal coefficients

Under the same restriction, the right side of (1) is

```text
sum_(c=0)^2 X_c D_c R_c,                             (14)

X_c=product_(i in R) x_i[c],
D_c=product_(u in B) z_u[c],
R_c=product_(w in Q) z_w[c].                         (15)
```

Evaluate the residual modes at the torus points (11).  Put

```text
h=H_Q((z_w)_(w in Q)),
lambda_c=X_c R_c((z_w)_(w in Q)).                    (16)
```

All three `lambda_c` are nonzero by (2) and (11).  Equations (12)--(16)
give the blocker-tensor identity

```text
h F_B=sum_(c=0)^2 lambda_c D_c.                      (17)
```

The tensors `D_0,D_1,D_2` are linearly independent: evaluating every
blocker variable at `e_c` selects `D_c` and kills the other two.  Hence the
right side of (17) is nonzero, so `h!=0`.  Dividing by `h` gives (8) with

```text
mu_c=lambda_c/h != 0.                                (18)
```

In particular the resulting tensor is concise.  Equivalently, each `L_u`
must have rank three, since a rank-deficient local map would make the
corresponding one-mode flattening have rank at most two, while (8) has
flattening rank three.

Finally, precompose the multilinear form in one blocker argument with the
invertible diagonal map

```text
e_c -> mu_c^(-1) e_c.
```

It changes (8) to `Delta_3`, proving the theorem.

## Consequence for the current proof programme

The theorem gives the exact conditional chain

```text
fully supported pairwise-zero five roots
  + total blocker union of size five
  -> P_5 -> Delta_3.                                  (19)
```

Therefore a proof that `P_5` does not restrict to `Delta_3` would turn (19)
into the strict arbitrary-order alternative

```text
every fully supported pairwise-zero five-root tuple
has at least six distinct blocker vertices.           (20)
```

The five-root intersection theorem guarantees a projective common zero of
the ten root--root bilinear forms, counted by the top intersection number
`24`, but does not guarantee a fully supported point.  Even at a fully
supported point, (20) is consistent when at least six outside vertices are
available.  Ruling out persistent blocker surplus or the coordinate-boundary
intersection is the remaining local-to-global problem.

## Exact replay

```text
uv run --with sympy python verify_five_root_tight_blocker_p5_extraction.py
python audit_five_root_tight_blocker_p5_extraction.py
```

The primary verifier reconstructs the matching-factor Cartesian product
through several residual sizes, expands the order-five permanent pullback,
checks independence of the three diagonal monomials, and replays the exact
one-mode rescaling.  The independent audit uses a different hafnian dynamic
program over `F_101`, exhausts the nonblocker-kernel torus statement over
`F_5`, and checks the blocker-set and rescaling logic.  The finite-field
parts are corroboration; the proof above is over `C` and arbitrary order.
