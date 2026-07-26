# Double-star annihilation and bilinear blocker lemma

## Setup

Let `V = C^3`.  For distinct vertices `i,j`, write

```text
B_ij(x_i,x_j) = transpose(x_i) W_ij x_j
```

for the scalar obtained by contracting the two endpoint colours of the
edge block.  The contraction of the full perfect-matching tensor against
local vectors `x_v in V` is

```text
H_W((x_v)_v) =
  sum over perfect matchings M
    product over {i,j} in M of B_ij(x_i,x_j).
```

For a Krenn--Gu witness this must equal

```text
G((x_v)_v) = sum_(c=0)^2 product_v x_v[c].
```

The lemma below is an arbitrary-order necessary condition for this
identity.  It is not restricted to the equality-support architecture.

## Double-star annihilation lemma

Fix distinct vertices `p,r` and vectors `x,y in V` satisfying

```text
B_pr(x,y) = 0.
```

For every other vertex `u`, define two covectors on `V`:

```text
a_u(z) = B_pu(x,z),
b_u(z) = B_ru(y,z).
```

Fix a colour `c` for which `x[c] y[c] != 0`, and call `u` a
`(p,r,x,y,c)` blocker when

```text
e_c in span(a_u,b_u).
```

Equivalently,

```text
ker(a_u) intersect ker(b_u)
  subset {z in V : z[c] = 0}.
```

**Theorem.**  If `H_W = G`, then there are at least two distinct blockers
among the vertices outside `{p,r}`.

### Proof

Suppose there are at most one.  Choose a vertex `q` outside `{p,r}` that
contains the sole blocker if it exists.  For each

```text
u not in {p,q,r},
```

the space

```text
H_u = ker(a_u) intersect ker(b_u)
```

is not contained in `z[c]=0`.  Choose `x_u in H_u` with `x_u[c] != 0`,
and put

```text
x_p = x,  x_r = y,  x_q = e_c.
```

Every perfect matching now has zero contracted weight.  Indeed, if `p`
is not paired with `q`, its edge is killed by `a_u`; this includes the
edge `pr`, which is zero by hypothesis.  If `p` is paired with `q`, then
`r` is paired with some `u not in {p,q,r}`, and that edge is killed by
`b_u`.  Hence

```text
H_W((x_v)_v) = 0.
```

On the other hand, `x_q=e_c` removes the other two summands of `G`, while
the colour-`c` summand is

```text
x[c] y[c] product_(u not in {p,q,r}) x_u[c] != 0.
```

This contradicts `H_W=G`, proving the theorem.

The important gain over the one-star killer argument is multiplicity:
the freely chosen exceptional partner `q` means that one blocker is not
enough.

## Irreducible bilinear consequence

Fix `p,r,c` and suppose the matrix of `B_pr` has rank at least two.  Let

```text
Q(x,y) = B_pr(x,y).
```

For every `u not in {p,r}`, define

```text
D_(u,c)(x,y) = det[
  transpose(e_c)
  a_u
  b_u
].
```

Both `Q` and `D_(u,c)` are bilinear polynomials in `(x,y)`.

**Corollary.**  There are at least two distinct vertices
`u not in {p,r}` for which

```text
D_(u,c)(x,y) = lambda_(u,c) Q(x,y)
```

identically in `(x,y)`, for some complex scalar `lambda_(u,c)`.
Moreover, the two vertices can be chosen so that their actual blocker
condition, not merely the determinant equation, holds on a dense
constructible subset of `X`.

### Proof

Because `rank(B_pr) >= 2`, the bilinear polynomial `Q` is irreducible.
Consequently

```text
X = {(x,y) : Q(x,y)=0}
```

is irreducible.  The locus in `X` on which `x[c]y[c] != 0` is a nonempty
dense open subset.

At every point of this open subset the theorem supplies at least two
actual blockers.  Let `C_u` be the constructible locus in the open subset
on which `u` is an actual blocker.  Then

```text
X_open = union_(u != v) (C_u intersect C_v).
```

The closure of a finite union is the union of the closures.  Since
`X_open` is dense in the irreducible variety `X`, at least one pair
`C_u intersect C_v` is dense.  Those fixed, distinct `u,v` are actual
blockers generically on `X`, and in particular both of their determinant
polynomials vanish throughout `X`.

For each such vertex, irreducibility gives `Q | D_(u,c)`.  The two
polynomials have the same bidegree, so their quotient is a scalar.

## Matrix form

Orient the blocks so that

```text
a_u = transpose(x) P_u,
b_u = transpose(y) R_u,
```

where `P_u=W_pu` and `R_u=W_ru`.  If `{alpha,beta}` is the complement of
`{c}` in `{0,1,2}`, then

```text
D_(u,c)(x,y)
 = transpose(x) (
     P_u[:,alpha] transpose(R_u[:,beta])
     - P_u[:,beta] transpose(R_u[:,alpha])
   ) y
```

up to the fixed sign determined by the order of `alpha,beta`.  Hence the
corollary is the exact matrix identity

```text
P_u[:,alpha] transpose(R_u[:,beta])
- P_u[:,beta] transpose(R_u[:,alpha])
= lambda_(u,c) W_pr.
```

If `W_pr` has rank three, the left side has rank at most two.  Thus
`lambda_(u,c)=0`, and at least two vertices `u` obey the sharper wedge
identity

```text
P_u[:,alpha] transpose(R_u[:,beta])
= P_u[:,beta] transpose(R_u[:,alpha]).
```

This supplies six forced wedge degeneracies around every rank-three edge:
two blocker vertices for each of the three colours.

### Dense-blocker classification at a rank-three edge

The dense actual-blocker conclusion rules out interpreting all of the
wedge identities as accidental determinant degeneracies.  Continue to
assume that `W_pr` has rank three, fix a colour `c`, and put

```text
P_0 = [P_u[:,alpha] P_u[:,beta]],
R_0 = [R_u[:,alpha] R_u[:,beta]].
```

For each of the two fixed dense blockers supplied above, at least one of
the following holds:

1. `P_u` is a nonzero block supported only in column `c`;
2. `R_u` is a nonzero block supported only in column `c`;
3. there is a nonzero vector `z in span(e_alpha,e_beta)` such that

   ```text
   P_u z = R_u z = 0.
   ```

To prove this, first use the wedge identity.  If `rank(P_0)=2`, applying
linear functionals that separately select its two independent columns
forces `R_0=0`.  Since the actual blocker condition holds generically and
`W_pr` is invertible, `R_u[:,c]` cannot also vanish.  Thus case 2 holds.
The symmetric argument gives case 1 when `rank(R_0)=2`.

It remains to consider `rank(P_0),rank(R_0) <= 1`.  If one complement
pair vanishes, generic blocking either makes that whole block a nonzero
column-`c` block or forces the other complement pair to vanish as well.
Otherwise write the two nonzero rank-one pairs as

```text
P_0 = A transpose(s),  R_0 = C transpose(t)
```

for nonzero two-vectors `s,t`.  The wedge identity says
`s[alpha]t[beta]=s[beta]t[alpha]`, so `s` and `t` are proportional.
Their common one-dimensional kernel supplies the vector `z` in case 3.

In particular, every dense blocker at a rank-three root edge touches a
singular incident block.  If neither incident block is a one-column
killer, both share an exact off-`c` kernel.  This is substantially sharper
than the bare conclusion that one of two complement-column pairs has rank
at most one.

## Rank-zero and rank-one components

The same argument has a precise, slightly weaker form when `Q` is
reducible.

- If `W_pr=0`, then `Q=0` on the irreducible space `V x V`.  For every
  colour `c`, multiplicity-two covering forces at least two
  `D_(u,c)` to vanish identically.
- If `rank(W_pr)=1`, write

  ```text
  Q(x,y) = l(x) m(y).
  ```

  On each component `l(x)=0` or `m(y)=0` that contains points with
  `x[c]y[c] != 0`, at least two blocker determinants vanish identically
  on that component.  Equivalently, at least two corresponding bilinear
  matrices have `l` as a left factor on the first component, and at
  least two have `m` as a right factor on the second.

A component supplies no colour-`c` information only when it is itself the
coordinate hyperplane `x[c]=0` or `y[c]=0`.  Those coordinate-aligned
rank-one edges are exactly the kind already exposed by the generic killer
and diagonal-anchor theorems.

## Consequence for a non-coordinate killer

Suppose the root edge is a colour-`c` killer from `p`:

```text
W_pr = a transpose(e_c),  a != 0,
```

and `a` is not proportional to `e_c`.  On the component
`transpose(x)a=0`, the colour-`c` open set is nonempty.  Apply the
rank-one component statement with `{alpha,beta}` equal to the other two
colours.  For at least two distinct vertices `u`, there is a row vector
`s_u` such that

```text
P_u[:,alpha] transpose(R_u[:,beta])
- P_u[:,beta] transpose(R_u[:,alpha])
= a transpose(s_u).
```

After quotienting the column space at `p` by `span(a)`, this says

```text
bar(P_u[:,alpha]) transpose(R_u[:,beta])
= bar(P_u[:,beta]) transpose(R_u[:,alpha]).
```

Therefore each of those two vertices satisfies the exact dichotomy

```text
P_u[:,alpha], P_u[:,beta] both lie in span(a),
```

or

```text
R_u[:,alpha], R_u[:,beta] are linearly dependent.
```

Indeed, if the two displayed `R_u` columns are independent, linear
functionals that select them separately force both quotient columns of
`P_u` to vanish.  Thus every non-coordinate killer has two
double-star witnesses: each is either backup-shaped at the killer's tail
in both non-killer columns, or exposes a two-column rank defect at the
killer's head.  The earlier failure-hyperplane theorem additionally
forces at least one backup-shaped block whose colour-`c` column escapes
`span(a)`.

The dense actual-blocker conclusion sharpens the second branch.  Let
`S_u` be the image in the two non-`c` coordinates of

```text
x -> transpose(x) P_u,  transpose(x)a=0,
```

and let `T_u` be the non-`c` row space of `R_u`.  For each of two fixed
dense blocker vertices, either

```text
T_u=0 and R_u[:,c] != 0,
```

so `R_u` is a nonzero column-`c` killer at its `u` endpoint, or

```text
dim(span(S_u union T_u)) <= 1.
```

Indeed, modulo `span(e_c)`, the two blocker covectors must be linearly
dependent for generic `x,y`.  If the first projected covector ranges over
two dimensions, the second must vanish identically and its surviving
`c`-coordinate must supply the blocker.  Otherwise both projected images
lie in the same line.  The case `S_u=0` is precisely the tail-side
backup-shaped condition

```text
P_u[:,alpha],P_u[:,beta] in span(a);
```

when both projected images are nonzero, this gives an exact shared
quotient direction rather than an unspecified rank defect.

## Simultaneously disabled primary killers

The two generic colour-`c` killers at the roots normally supply the two
blockers in the theorem automatically.  They can be removed
simultaneously unless the root block has a special bridge form.

Choose distinct roots `p,r` and non-coordinate primary killers whose
neighbours `k,l` lie outside `{p,r}`:

```text
W_(p,k) = A transpose(e_c),
W_(r,l) = B transpose(e_c),
```

where `A,B` are nonzero and neither is proportional to `e_c`.  Put

```text
H_A = {x : transpose(x)A=0},
H_B = {y : transpose(y)B=0}
```

and restrict the root bilinear form to `H_A x H_B`.

**Disabled-killer dichotomy.**  Exactly one of the following alternatives
is forced.

1. The restricted root form is a nonzero pure coordinate product:

   ```text
   B_pr(x,y) = lambda x[c] y[c] on H_A x H_B
   ```

   for some `lambda != 0`.  Equivalently, for some vectors `s,t`,

   ```text
   W_pr =
     lambda e_c transpose(e_c)
     + A transpose(s)
     + t transpose(B).
   ```

2. The restricted zero locus has an irreducible component containing a
   dense set of pairs with `x[c]y[c] != 0`.  On that component, two fixed
   distinct vertices are actual double-star blockers on a dense
   constructible subset.

To prove the dichotomy, note first that `x[c]` and `y[c]` are nonzero
linear forms on `H_A` and `H_B`.  If the restricted bilinear form has no
zero with both coordinates nonzero, then for every generic `x` its
linear form in `y` has kernel exactly `y[c]=0`.  Hence it is
`L(x)y[c]`; applying the same argument in `x` gives
`L(x)=lambda x[c]`.  The matrix equivalence is the elementary fact that
a bilinear form vanishing on `H_A x H_B` belongs to

```text
A tensor V* + V* tensor B.
```

Otherwise choose an irreducible component meeting the coordinate-open
set.  The double-star theorem gives two blockers at every point of that
open set.  The same finite constructible-pair argument used above makes
one fixed pair dense on the component.

This removes the automatic primary blocker at `k`, because its
`p`-covector is zero throughout `H_A`.  It can still count only if its
block from `r` contracts to a nonzero multiple of `e_c` along the chosen
component.  The symmetric statement holds for `l`.  In particular, if
`k=l`, neither root covector survives there and both dense blockers are
different vertices.

There is a clean generic refinement.  If the restricted form has rank
two as a bilinear form on the two-dimensional spaces `H_A,H_B`, its zero
curve is irreducible and projects densely to both factors.  Then `k` can
remain a blocker only when

```text
W_(r,k)[:,j] in span(B) for j != c,
W_(r,k)[:,c] not in span(B),
```

so the first primary neighbour is a failure-hyperplane backup for the
second root.  Likewise, `l` can remain only as a cross-backup for `A`.
Absent those two cross-backups, the restricted double-star argument
forces two genuinely new blocker vertices.

### Global all-bridge boundary

The coordinate-product bridge alternative cannot hold everywhere without
one of two further degeneracies.  Suppose that for one fixed colour `c`
every vertex `i` has a chosen primary vector `A_i` not proportional to
`e_c`, put `H_i=A_i^perp`, and suppose every edge restricts as

```text
B_ij(x_i,x_j) = lambda_ij x_i[c] x_j[c]
  on H_i x H_j.
```

The scalars `lambda_ij` are allowed to vanish.  On the product of all
failure planes, the full matching tensor becomes

```text
haf(lambda) product_i x_i[c].
```

Comparing with the restricted GHZ tensor gives

```text
product_i x_i[alpha]
+ product_i x_i[beta]
+ (1-haf(lambda)) product_i x_i[c] = 0,              (*)
```

where `{alpha,beta}` is the complement of `{c}`.

For at least two vertices, the three decomposable tensors in `(*)` cannot
be linearly dependent when all three are nonzero: the elementary
three-term tensor argument forces all three local coordinate forms to be
proportional in all but at most one mode, while they span the
two-dimensional dual of every `H_i`.  The cases with a zero tensor are
equally rigid.  Consequently

```text
haf(lambda) = 1
```

and exactly one of the following exceptional patterns is necessary:

1. both non-`c` product tensors vanish, so some `A_i` is proportional to
   `e_alpha` and some `A_j` is proportional to `e_beta`; or
2. neither vanishes, every `A_i[c]=0`, the two restricted non-`c`
   coordinate forms are proportional at every vertex, and the product
   of their proportionality scalars is `-1`.

Indeed, if exactly one non-`c` product vanishes, then at the vertex whose
failure plane is that coordinate hyperplane the other non-`c` form and
the colour-`c` form are independent, so the remaining two product tensors
cannot be proportional.  If neither vanishes and the third coefficient
in `(*)` is zero, proportionality of the first two tensors gives pattern
2.  If both vanish, `(*)` forces the third coefficient to be zero and
gives pattern 1.

Thus, outside these two explicit boundaries, some pair of vertices must
fall into the deeper-blocker alternative rather than the bridge
alternative.  The two boundary patterns still have to be combined with
the other colours' killer flags and diagonal anchors.

### One-normal and many-normal slices of the bridge boundary

The second boundary pattern is in fact impossible, and the first collapses
to a balanced coordinate partition.

Assume first that pattern 2 holds.  Write the restricted coordinate forms
on `H_i` as

```text
alpha_i = rho_i beta_i,
```

where every `rho_i` is nonzero and

```text
product_i rho_i = -1.
```

Fix a vertex `k`, leave its vector unrestricted, and restrict every other
vertex to its failure plane.  For each `j != k`, the bridge identity implies

```text
B_kj(x_k,x_j)
 = lambda_kj x_k[c] x_j[c] + A_k(x_k) s_kj(x_j)
```

for some linear form `s_kj` on `H_j`.  Put

```text
h_kj = haf(lambda on V minus {k,j}).
```

Expanding the matching tensor at `k`, and using `haf(lambda)=1`, gives

```text
H_W =
  x_k[c] product_(i != k) x_i[c]
  + A_k(x_k) sum_(j != k) h_kj s_kj(x_j)
      product_(i not in {k,j}) x_i[c].                 (**)
```

On the GHZ side the two non-`c` terms combine to

```text
(x_k[alpha] product_(i != k) rho_i + x_k[beta])
  product_(i != k) beta_i.
```

The parenthesized form vanishes on `H_k`, so it is a nonzero scalar
multiple `gamma_k A_k(x_k)`.  Cancelling that common normal form in the
identity with `(**)` would force

```text
sum_(j != k) h_kj s_kj(x_j)
  product_(i not in {k,j}) x_i[c]
 = gamma_k product_(i != k) beta_i.                    (***)
```

Choose two distinct vertices outside `k`.  At each, choose a vector in its
failure plane with nonzero `beta_i` coordinate and zero `c` coordinate;
this is possible because the two non-`c` coordinate forms are nonzero and
proportional there.  Choose all remaining vectors with nonzero `beta_i`.
Every summand on the left of `(***)` still contains the `c` coordinate at
one of the two selected vertices, whereas the right side is nonzero.  This
is a contradiction for `n >= 4`.  Hence pattern 2 cannot occur.

Now suppose pattern 1 holds.  Define

```text
I_alpha = {i : A_i is proportional to e_alpha},
I_beta  = {i : A_i is proportional to e_beta},
r = |I_alpha|,  s = |I_beta|.
```

Both sets are nonempty and disjoint.  Leave the vertices in `I_alpha`
unrestricted and then set their vectors equal to `e_alpha`; restrict all
other vertices to their failure planes.  An edge between two restricted
vertices contributes only its coordinate-`c` bridge.  Thus every surviving
matching term, viewed as a tensor on the restricted vertices, differs from
the pure product of their `c` coordinate forms in at most `r` modes: each
of the `r` unrestricted vertices can be paired with at most one restricted
vertex.

The GHZ tensor on this slice is the pure product of the restricted
`alpha` coordinate forms.  It follows that at most `r` restricted vertices
can have linearly independent restricted `alpha` and `c` coordinate
forms.  Otherwise choose `r+1` such modes with `c=0` and `alpha != 0`.
Every matching term vanishes because it has at most `r` non-`c` modes,
while the target product remains nonzero.

Every vertex in `I_beta` is one of those independent modes, so `s <= r`.
The symmetric argument gives `r <= s`; hence `r=s`.  The `I_beta` modes
already exhaust the `r` possible independent modes.  Therefore any vertex
outside `I_alpha union I_beta` would have both

```text
alpha restricted to H_i proportional to c restricted to H_i,
beta  restricted to H_i proportional to c restricted to H_i.
```

The first condition is equivalent to
`A_i in span(e_alpha,e_c)` and the second to
`A_i in span(e_beta,e_c)`.  Their intersection is `span(e_c)`, contrary
to the standing assumption that no `A_i` is proportional to `e_c`.
Consequently there are no such vertices:

```text
V = I_alpha disjoint union I_beta,
|I_alpha| = |I_beta| = n/2.
```

Thus the extreme all-bridge case has only one remaining normal form.  Up
to rescaling the primary vectors, half the vertices use `A_i=e_alpha` and
half use `A_i=e_beta`.  On a cross edge, oriented from the first half to
the second, the bridge matrix has the zero pattern

```text
[ *  *  * ]
[ 0  *  0 ]
[ 0  *  * ],
```

where the last diagonal entry is the coordinate-`c` bridge weight.  Edges
inside either half have support only in the corresponding coordinate row
or column, together with the `(c,c)` entry.  Excluding this balanced
normal form, or forcing it into the deeper-blocker branch for another
colour, is the remaining all-bridge task.

The balanced form has an additional exact cofactor obstruction.  Write
`X=I_alpha`, `Y=I_beta`, and define the three scalar edge matrices

```text
P_xy = W_xy[alpha,alpha],
Q_xy = W_xy[beta,beta]       for x in X, y in Y,
L_ij = W_ij[c,c]             for all i != j.
```

The all-`alpha` amplitude can use only cross edges, because every
`alpha-alpha` entry inside `Y` vanishes; counting then also forbids an
internal edge in `X`.  The symmetric statement holds for `beta`.  Hence

```text
per(P) = per(Q) = 1,       haf(L) = 1.
```

In fact, all complementary minors obey an exact orthogonality system.
Choose subsets `S subset X`, `T subset Y` of the same size `k`, colour
the vertices in `S union T` by `alpha`, and colour every other vertex by
`c`.  Every `alpha` vertex of `Y` must pair with an `alpha` vertex of
`X`: its internal entries vanish and the cross entry with row colour `c`
and column colour `alpha` is zero.  Since the two selected sets have the
same size, all selected vertices pair across the partition and all
remaining vertices use coordinate-`c` entries.  The amplitude therefore
factors as

```text
per(P[S,T]) haf(L[V minus (S union T)]).
```

The analogous `beta/c` colouring factors through `Q`.  Consequently, for
every `S,T` with `|S|=|T|=k`,

```text
per(P[S,T]) haf(L[V minus (S union T)])
  = 1  if k=0 or k=n/2,
  = 0  otherwise,

per(Q[S,T]) haf(L[V minus (S union T)])
  = 1  if k=0 or k=n/2,
  = 0  otherwise.                                      (****)
```

Here the size-zero permanent and the empty hafnian are one.  The
`k=n/2-1` equations say, for every cross pair `(x,y)`,

```text
L_xy per(P without row x and column y) = 0,
L_xy per(Q without row x and column y) = 0.
```

The `k=1` equations give the converse cofactor orthogonality:

```text
P_xy haf(L without x and y) = 0,
Q_xy haf(L without x and y) = 0.
```

Thus cross entries of `L` can occur only at simultaneous zero permanent
cofactors of `P,Q`, while entries of either `P` or `Q` can occur only at
zero cross cofactors of the hafnian of `L`.  These are exact
complementary-minor orthogonality equations between the three
monochromatic matching polynomials, not just first-order cofactor
conditions.

These equations force degeneration in every intermediate layer, not only
at the cofactors.  The permanent Laplace identity gives

```text
sum_(|S|=|T|=k)
  per(P[S,T]) per(P[X-S,Y-T])
= binomial(n/2,k) per(P)
= binomial(n/2,k).
```

Hence, for every `1 <= k < n/2`, some pair `S,T` makes both displayed
subpermanents nonzero.  Applying `(****)` to that pair and to its
complement forces

```text
haf(L[S union T]) = 0,
haf(L[V minus (S union T)]) = 0.
```

Thus the coordinate-`c` matrix has, at every balanced intermediate size,
a cut for which both induced hafnians vanish even though `haf(L)=1`.
The same conclusion follows from `Q`, potentially with a different cut.
At `k=1`, any nonzero monomial of `per(P)=1` also shows that the zero
pattern of the cross hafnian-cofactor matrix contains a perfect matching;
the same is true using `Q`.

The balanced `alpha/beta` slice has a different exact form.  Define

```text
V_xx' = the alpha-beta entry on an edge inside X,
U_yy' = the alpha-beta entry on an edge inside Y.
```

Fix `S subset X`, `T subset Y` with `|S|=|T|`.  Colour `S,T` by
`alpha` and their complements by `beta`.  A count of matching types shows
that a surviving matching can use only:

```text
P edges from S to T,
Q edges from X-S to Y-T,
V edges from S to X-S,
U edges from T to Y-T.
```

Indeed, if `p,q,z,u,v,a,b` count, respectively, the two diagonal cross
types, the triangular `alpha-beta` cross type, the two internal mixed
types, and the internal `alpha-alpha` and `beta-beta` types, vertex
balance gives

```text
z + u + 2a = v,
z + v + 2b = u.
```

Nonnegativity forces `z=a=b=0` and `u=v`.  Thus the original matching is
equivalently a perfect matching in an artificial bipartite graph with row
set `S union (Y-T)` and column set `T union (X-S)`.  Its matrix is

```text
M_(S,T) = [
  P[S,T]          V[S,X-S]
  transpose(U[T,Y-T])  transpose(Q[X-S,Y-T])
].
```

Consequently

```text
per(M_(S,T))
  = 1  if S=T=empty or S=X,T=Y,
  = 0  otherwise.                                      (*****)
```

Unlike `(****)`, this is a block-permanent equation rather than a product
of complementary minors.  The paired `V` and `U` transitions are exactly
why the two pairwise systems do not multiply into a three-colour
factorization.

The first intermediate layer makes that obstruction explicit.  For every
cross pair `(x,y)`, expansion of `(*****)` gives

```text
P_xy per(Q without x,y)
+ sum_(b != x, d != y)
    V_xb U_yd per(Q without {x,b},{y,d})
= 0.                                                    (******)
```

The complementary layer gives the symmetric identity with `P,Q`
interchanged.  Thus any failure of entrywise complementary-cofactor
orthogonality between `P` and `Q` must be paid for by a paired internal
transition through both `V` and `U`.  In particular, if either internal
transition matrix vanishes, then for every `S,T`

```text
per(P[S,T]) per(Q[X-S,Y-T]) = 0
```

at all intermediate sizes.  This conditional third two-colour subsystem
is still not a global contradiction, but it cleanly separates the
transition-free degeneration from the genuinely coupled branch.

In particular, when `n = 2 mod 4`, the two permanental cofactor matrices
must have a common zero.  Indeed, `|X|=|Y|` is then odd, so every perfect
matching contributing nontrivially to `haf(L)=1` contains a cross edge.
At least one such matching has nonzero edge product, and each of its cross
edges has `L_xy != 0`; both corresponding cofactors vanish by `(****)`.
Thus a balanced bridge witness of order `4k+2` is confined to a proper
permanental-cofactor degeneration.  This does not yet exclude that
degeneration, but it is an exact next boundary rather than a genericity
assumption.

The cofactor conditions alone are consistent.  At order six, take
`P=Q=I_3` and let the cross support of `L` be a cyclic derangement, with
its three nonzero entries scaled to have product one and all internal
entries zero.  Then both permanents and the hafnian are one, while every
`L` entry lies at an off-diagonal zero cofactor of both identity matrices.
All intermediate complementary-minor equations `(****)` hold as well.
This toy assignment does not satisfy the remaining mixed-colour tensor
equations and is not a graph witness.  It shows exactly why the next step
must use those mixed-colour identities rather than the cofactor equations
in isolation.

The remaining unequal-count mixed-colour amplitudes additionally involve
the triangular cross entries and the internal same-colour entries that
the balance equations eliminate from `(*****)`.

## Boundary

The lemma does not yet prove that the forced wedge or componentwise
factor identities are incompatible with all local killer flags and
diagonal anchors.  Turning that interaction into either a global rank
collapse or a forbidden amplitude is the precise remaining step before
this mechanism could become a global proof.
