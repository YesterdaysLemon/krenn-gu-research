# The complete P7 shallow deck has exact double-star fibres

## Status

**Exact characteristic-zero singular-locus theorem and target-specific
non-recovery family.**  On nine named vertices, collect every principal
hafnian of orders four, six, and eight.  This is exactly the nonlinear
cofactor tower left by the five-root/two-residual `P_7` deletion grades.

Adding the order-six and order-eight levels does not repair global edge
identifiability.  Fix two named vertices `p,q`, make the other seven vertices
an independent set, and allow arbitrary weights only on the two stars and on
the center edge `pq`.  Then:

- all order-six and order-eight principal hafnians vanish;
- the only possibly nonzero order-four values are

  ```text
  H_{pqij}=x_i y_j+x_j y_i;
  ```

- the center edge `a_pq` is absent from the entire combined deck;
- reciprocal scaling `(x,y)->(t x,t^(-1)y)` is also invisible;
- on a dense open part of this double-star stratum, the restricted fibre has
  dimension exactly two;
- at an explicit point the **ambient** combined-deck Jacobian has rank
  `36-2=34`, and its two-dimensional kernel is precisely the tangent to the
  displayed affine-line times torus family.

Thus the positive-dimensional singular fibre persists even when many
four-hafnians are nonzero.  Choosing `p,q` to be the desired blocker pair
makes that particular edge vary freely while the whole shallow tower remains
fixed.  This is stronger than the earlier one-edge zero-deck line.

There is also a sharp boundary statement for the zero four-deck.  If `n>=6`
and every edge weight is nonzero, the four-hafnians cannot all vanish.
Consequently the zero fibre lies entirely on the union of the coordinate
hyperplanes.  Stars and triangles give its matching-number-one coordinate
strata, but cancellation components on the coordinate boundary are not
classified here.

These families are legal weighted symmetric graphs, but they are not shown
to satisfy the GHZ target equations.  The theorem proves that no universal
recovery of the blocker pair from the complete `P_7` shallow deck is possible;
it does **not** prove that a GHZ witness can occupy this stratum.  The `P_7`
case and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## 1. Matching number filters every principal-hafnian tower

Let `A=(a_ij)` be a symmetric zero-diagonal weighted graph on a named vertex
set `V` over a characteristic-zero field `K`.  Write `G_A` for its support
graph and

```text
H_I(A)=haf A[I]                                       (1)
```

for every even set `I`.

### Lemma 1 (matching-number filtration)

If the matching number of `G_A` is less than `k`, then

```text
H_I(A)=0                 for every |I|=2k.            (2)
```

The same conclusion holds at every larger order.

### Proof

Every monomial in `H_I` is indexed by a perfect matching of `I`, hence by a
`k`-edge matching in `G_A`.  If no such support matching exists, every
monomial has a zero factor.  The argument uses support only as a sufficient
certificate; cancellations can produce further zeros.

When the matching number is at most one, the nonzero support edges form an
intersecting family of two-sets.  Such a family is contained in a star or in
a triangle.  Indeed, take two distinct edges `ab,ac`.  If not every edge
contains `a`, an edge meeting both must be `bc`; any edge meeting all three
triangle edges is itself a triangle edge.  Thus the zero combined deck
contains star spaces of dimension `n-1` and triangle spaces of dimension
three.

More importantly here, matching number at most two kills orders six and
eight while permitting nonzero order-four data.

## 2. The double-star response is an off-diagonal hyperbolic Gram map

Fix

```text
V={p,q} disjoint union W,             |W|=m,
c=a_pq,
x_i=a_pi,   y_i=a_qi                 (i in W),         (3)
```

and set every edge inside `W` to zero.  This is the weighted double-star
stratum `D_{p,q}`.  Its support has vertex cover `{p,q}`, hence matching
number at most two.

For a four-set, a direct matching expansion gives

```text
H_I(A)=x_i y_j+x_j y_i   if I={p,q,i,j},
H_I(A)=0                 otherwise.                   (4)
```

The term containing `c` would require the complementary edge `ij`, which is
zero.  Lemma 1 gives

```text
H_I(A)=0                 for every even |I|>=6.       (5)
```

In particular, the whole combined deck is independent of `c`; appending any
still higher principal hafnians would not help.  Global sign illustrates why
the sixth-order level helps generically but fails here:

```text
H_{2k}(-A)=(-1)^k H_{2k}(A).
```

Thus a nonzero sixth-order coordinate distinguishes `A` from `-A`, whereas
every sixth-order coordinate on the double-star stratum is zero.

Put

```text
z_i=(x_i,y_i)^T,                 J=[0 1; 1 0].        (6)
```

Then the nonzero part of (4) is the off-diagonal hyperbolic Gram map

```text
phi_m:(z_i)_i |-> (z_i^T J z_j)_{i<j}.                (7)
```

The group

```text
O(J)={g:g^T J g=J}=G_m semidirect C_2               (8)
```

acts on every `z_i` and preserves (7).  Its identity component is

```text
(x_i,y_i) |-> (t x_i,t^(-1)y_i).                     (9)
```

The other component swaps the two coordinates, followed by such a scaling.
Equation (8) follows directly by writing a two-by-two matrix `g`: in
characteristic different from two, `g^T J g=J` forces `g` to be diagonal or
anti-diagonal.

This is the same gauge principle that appears in low-rank Gram completion
and rigidity matrices.  The relevant literature uses a completion Jacobian
to distinguish local from global uniqueness; see Singer and Cucuringu,
[*Uniqueness of Low-Rank Matrix Completion by Rigidity
Theory*](https://arxiv.org/abs/0902.3846).  The hyperbolic, missing-diagonal
calculation below is self-contained.

## 3. Exact generic fibre dimension

### Theorem 2 (off-diagonal hyperbolic Gram rank)

For `m>=5`, the map `phi_m` in (7) has generic differential rank

```text
2m-1.                                                   (10)
```

Its generic fibres therefore have dimension one.  On the open set where the
`O(J)` action has finite stabilizer, each generic fibre component is the
closure of a one-dimensional `O(J)` orbit.  Thus the continuous ambiguity is
exactly (9), up to finitely many components and lower-dimensional boundary
points; no claim of one global branch is needed.

### Proof

Invariance under (9) gives the tangent kernel

```text
(delta x_i,delta y_i)=(lambda x_i,-lambda y_i),        (11)
```

so the rank is at most `2m-1`.

For the reverse inequality, take

```text
x_i=1,       y_i=s+i,              i=0,...,m-1,       (12)
```

with any fixed scalar `s`.  Write a tangent vector as `(u_i,v_i)` and put
`w_i=v_i+s u_i`.  The kernel equations are

```text
j u_i+w_i+i u_j+w_j=0                  (i<j).          (13)
```

The equations with `i=0` give

```text
w_j=-j u_0-w_0.                                      (14)
```

Put `d_i=u_i-u_0`.  For `i,j>=1`, equations (13)--(14) become

```text
j d_i+i d_j=2w_0.                                    (15)
```

Use the five pairs

```text
(1,2),(1,3),(1,4),(2,3),(2,4).                       (16)
```

The first three express `d_2,d_3,d_4` through `d_1,w_0`; the last two force
`w_0=0` and then `d_1=d_2=d_3=d_4=0`.  For every later `j`, equations with
`0` and `1` give `d_j=0`.  Hence

```text
u_i=u_0,        v_i=-(s+i)u_0,                       (17)
```

which is exactly (11).  The rank at (12) is `2m-1`, so that is the generic
rank.  Fibre dimension and the orbit statement follow from the fibre
dimension theorem and the fact that an algebraic fibre has finitely many
irreducible components.

### Corollary 3 (restricted combined-deck fibre)

On `D_{p,q}` with `m>=5`, the generic fibre of the principal
`4/6/8`-hafnian deck has dimension exactly two.  It contains

```text
c -> tau,                 tau in A^1,
(x,y) -> (t x,t^(-1)y),  t in G_m.                   (18)
```

Indeed, the deck is the product of `phi_m` with a constant map and is
independent of `c`.  Generically it is a finite union of
`A^1 times O(J)` orbit closures.

## 4. The ambient nine-vertex rank drop is exactly two

The restricted dimension count could in principle hide additional ambient
directions.  At a simple exact point it does not.

Take `m>=5` and the double-star point

```text
c=1,       x_i=1,       y_i=1+i,       i=0,...,m-1.  (19)
```

Let `z_ij` be a tangent variation of an edge inside `W`.  The differential
of the four-hafnian on `{p,i,j,k}` is

```text
z_ij+z_ik+z_jk.                                      (20)
```

If every expression (20) vanishes, fix leaf `0` and put `r_i=z_0i`.  The
triangle containing `0,i,j` gives

```text
z_ij=-r_i-r_j.                                       (21)
```

A triangle among three leaves different from `0` then gives

```text
r_i+r_j+r_k=0.                                       (22)
```

There are at least four such leaves.  Comparing triple sums makes all `r_i`
equal, and then `3r_i=0`; hence every `z_ij=0`.

The remaining differential equations, on `{p,q,i,j}`, are exactly the
off-diagonal Gram equations of Theorem 2.  The variation of `c` is free.
Therefore the kernel of the ambient four-deck Jacobian at (19) is precisely

```text
delta c arbitrary,
delta x_i=lambda x_i,
delta y_i=-lambda y_i,
delta a_ij=0 for i,j in W.                            (23)
```

Both directions integrate to the actual combined-deck family (18).  Adding
the order-six and order-eight rows cannot remove them, while the four-deck
rows already leave only those two directions.  Thus for nine vertices

```text
rank d(H_4,H_6,H_8)=36-2=34                          (24)
```

at (19).  The ambient fibre is smooth of local dimension exactly two there.
All 21 values `H_{pqij}=2+i+j` are nonzero, so this is not the zero-deck
fibre.

There is also a toric explanation.  Under diagonal vertex scaling

```text
a_ij -> d_i d_j a_ij,
H_I  -> (product_{i in I} d_i) H_I.                  (25)
```

For the nonzero labels `{p,q,i,j}`, the deck-stabilizer equations are

```text
d_p d_q d_i d_j=1                 for all i<j.        (26)
```

Their identity-component exponent kernel has dimension two: every leaf
exponent is one scalar `beta`, and

```text
alpha_p+alpha_q+2 beta=0.                             (27)
```

At a generic nonzero double star this torus acts with only a finite graph
stabilizer.  It produces precisely the two local directions in (23), with
one parameter changing the center edge and the other reciprocally scaling
the two shores.  This support-incidence torus is a useful general diagnostic
for other principal-deck rank drops.

## 5. The zero four-deck cannot meet the edge torus

### Theorem 4 (zero-deck coordinate-boundary theorem)

Let `n>=6`.  If

```text
H_I(A)=0 for every four-set I,                         (28)
```

then at least one edge weight `a_ij` is zero.  Equivalently, the zero fibre
of `H_4` has no point in the full edge torus `(K^*)^{binom(n,2)}`.

### Proof

Assume every edge is nonzero and fix vertices `1,2`.  For distinct
`i,j` outside them, `H_{12ij}=0` gives

```text
a_ij=-(a_1i a_2j+a_1j a_2i)/a_12.                   (29)
```

Put `r_i=a_2i/a_1i`.  Substitute (29) into `H_{1ijk}=0`.  After factoring
nonzero terms, one obtains

```text
0=-(2/a_12)a_1i a_1j a_1k(r_i+r_j+r_k).              (30)
```

Thus every triple sum of the `n-2>=4` ratios is zero.  Comparing two triples
that differ in one entry makes all ratios equal, and a triple then gives
`3r_i=0`.  Characteristic zero forces `r_i=0`, contradicting `a_2i!=0`.

The theorem places every zero-deck component on the coordinate boundary;
it does not say that every such component comes from low matching number.
The star and triangle spaces from Lemma 1 are explicit linear strata; no
claim that they are maximal irreducible components is made, and cancellation
strata remain possible.

## 6. Exact `P_7` consequence and boundary

In the five-root/two-residual `P_7` cell, the allowable mixed-root deletion
depths are five, three, and one.  On the nine nonroots these leave principal
hafnians of orders four, six, and eight, respectively.  Even granting legal
labels for every one of those cofactors, the double-star family proves:

```text
universal recovery from H_4 alone:             FALSE;
universal recovery from (H_4,H_6,H_8):         FALSE;
positive-dimensional fibre with H_4 nonzero:  PROVED;
desired center pair invisible on that fibre:  PROVED;
zero H_4 deck away from coordinate boundary:  IMPOSSIBLE;
GHZ forced away from every two-cover stratum:  UNKNOWN;
GHZ forced into the generic H_4 chart:         UNKNOWN;
P_7 obstruction:                              UNKNOWN;
global Krenn--Gu:                              UNRESOLVED.  (31)
```

This is exactly a determinant-drop boundary for the pinned-star inverse in
`PINNED_HAFNIAN_STAR_SYSTEM_AND_RATIONAL_EDGE_TOMOGRAPHY_THEOREM.md`.
For the center edge `p--q`, the corresponding pinned column consists of
four-hafnians on leaf-only four-sets and is therefore identically zero on
the double star.  Thus the generic rational theorem and this two-dimensional
fibre are compatible pieces of one stratified observation map.

The next nonlinear route cannot merely append deeper shallow-deck levels.
It must use a target equation that excludes the matching-number-two/two-cover
boundary, or combine the deck with root-label multiplication data that is not
contained in the principal hafnians themselves.

## Replay

```powershell
uv run --with sympy python verify_p7_combined_shallow_deck_double_star_gauge.py
python audit_p7_combined_shallow_deck_double_star_gauge.py
python -m py_compile verify_p7_combined_shallow_deck_double_star_gauge.py audit_p7_combined_shallow_deck_double_star_gauge.py
uv run --with ruff ruff check verify_p7_combined_shallow_deck_double_star_gauge.py audit_p7_combined_shallow_deck_double_star_gauge.py
```

The primary replay checks representative hafnian identities symbolically,
the rank-`2m-1` hyperbolic completion Jacobian, the rank-34 ambient tangent
certificate, the two-dimensional support-incidence torus, and the zero-deck
ratio identity.  The independent standard-library audit repeats the ranks by
rational elimination and the hafnian identities by its own recursive
arithmetic.  These are fixed audits of the symbolic proof, not searches over
graphs, supports, words, or parameter families.
