# Maximum-root surplus-two zero-anchor rank-four complete-pair structural-degree, cut, and triangle localization

## Status and scope

**Exact characteristic-zero arbitrary-root pointwise structural reduction.**
The two silent rank-four cores left by `GLS45` admit one common complete-label
form.  Let `K` have characteristic zero, let `T` be a finite label set, let
`V_t` be finite-dimensional over `K`, and let

```text
X_t,Y_t:V_t -> K^3.
```

For distinct labels put

```text
mu_(s,t)(v,w)
 =X_s(v) tensor Y_t(w)+X_t(w) tensor Y_s(v).          (1)
```

Write

```text
Delta=span{r_0,r_1,r_2},       r_i=e_i tensor e_i,
B=Delta direct-sum K f,                              (2)
```

where `f` is nonzero and has zero diagonal.  If

```text
im mu_(s,t) subset B              for every s!=t,
sum_(s<t) im mu_(s,t)=B,                              (3)
```

then all of the following hold.

1. Each of the six global coordinate families is supported on at most two
   labels.
2. After deleting zero labels and quotienting joint kernels, at most twelve
   labels remain and their total effective domain dimension is at most
   twelve.
3. For every label bipartition, the diagonal projection of all crossing pair
   images has dimension at most two.
4. Three independent diagonal outputs are supported on the three edges of
   one label triangle.  Each triangle edge has a one-dimensional diagonal
   image, and every other edge has zero diagonal image.
5. Consequently the missing fourth direction can occur only through a
   two-dimensional full image on one triangle edge or through a nonzero
   pure-`f` image on an edge outside the triangle.

The reduction is pointwise, uses no selected port value, and covers arbitrary
label-domain dimensions, support patterns, rank drops, divisor fibres, and
both `GLS45` survivors.  It is a uniform structural-degree theorem, not a
finite support atlas.  For the residual-free survivor, take `T` to be the
promoted-port labels.  For the sparse survivor, adjoin one label `q_0` with

```text
V_(q_0)=K,       X_(q_0)(1)=a,       Y_(q_0)(1)=t b.
```

Its cross map with a port `u` is exactly

```text
a tensor Y_u+t X_u tensor b.
```

The other residual label is zero and is deleted.  The port--port maps are
unchanged, no self-pair of `q_0` is introduced, and `q=0`; hence the sum of
all distinct-label images is exactly `im sigma_Q=B`.  Thus (2)--(3) hold for
both `GLS45` survivors rather than only for the promoted-port subfamily.

The theorem does **not** exclude either survivor.  An exact rational triangle
below shows that the tempting stronger global diagonal-rank-two statement is
false.  The theorem does not classify all triangle normal forms, exclude both
fourth-direction mechanisms, treat ranks five through nine or raw escape, or
supply response, activity, synchronization, nuisance survival, an anchor, a
receiver, or source coverage.  The strategic node and the global Krenn--Gu
conjecture remain **UNRESOLVED**.

This is `GLS46`.

## Dependencies and provenance

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for the promoted chart and legal-attachment boundary;
- [`GLS36`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  for the complete zero-anchor incidence family;
- [`GLS39`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_COMPLETE_PAIRWISE_DIAGONAL_FAMILY_RANK_BOUND_AND_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md)
  for the auxiliary-label interface and the zero-excess predecessor; and
- [`GLS45`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_SILENT_FULL_SWALLOW_RESIDUAL_SHORE_PROFILE_REDUCTION_THEOREM.md)
  for the exhaustive residual-free and sparse same-label rank-four boundary.

`GLS40` identifies the unique rank-four excess line, but its transverse
cylinder and the `GLS41` receiver require `p!=0`; the present fibre has
`q=p=0`.  No external literature claim is used.  The new content is the
coordinate structural-degree bound, arbitrary-dimensional two-block theorem,
all-cut consequence, triangle localization, and exact locked sharpness
triangle.

## 1. Coordinate support localization

Write the coordinate forms of `X_t,Y_t` as

```text
x_(t,i)=e_i^* X_t,              y_(t,j)=e_j^* Y_t,
x_i=(x_(t,i))_(t in T),         y_j=(y_(t,j))_(t in T). (4)
```

The global families in (4) are elements of the dual of the direct sum of
the label domains.

### Lemma 1 (labelled zero-product bound)

Let `K` have characteristic different from two.  Suppose nonzero labelled
families `alpha=(alpha_t)` and `beta=(beta_t)` satisfy

```text
alpha_s tensor beta_t+beta_s tensor alpha_t=0        (5)
```

for every `s!=t`.  Then

```text
supp alpha=supp beta,             |supp alpha|<=2.    (6)
```

#### Proof

If `s` lies in `supp alpha` but not `supp beta`, pairing it with any label in
`supp beta` makes (5) one nonzero simple tensor, a contradiction.  The
transposed argument gives equality of the supports.

For two distinct supported labels `s,t`, equality of the two nonzero simple
tensors gives nonzero scalars `rho_s,rho_t` with

```text
alpha_s=rho_s beta_s,       alpha_t=rho_t beta_t,
rho_s+rho_t=0.                                      (7)
```

Three supported labels would force both `rho_t=-rho_s` and
`rho_t=rho_s`, hence `2rho_s=0`, a contradiction. `square`

### Lemma 2 (coordinate-family localization)

Under (2)--(3), the three `x_i` are linearly independent and the three `y_j`
are linearly independent.  Moreover,

```text
|supp x_i|<=2,                  |supp y_j|<=2         (8)
```

for every colour.

#### Proof

If `sum_i u_i x_i=0`, then the row `u^T` kills every `X_t` and hence every
matrix in the combined image in (3).  It therefore kills `B`.  Since `B`
contains all three `r_i`, this forces `u=0`.  Transposition proves the
independence of the `y_j`.

Fix `i`.  Choose a nonzero vector `v^(i)` such that

```text
v_i^(i)=0,              sum_(j!=i) f_(i,j)v_j^(i)=0. (9)
```

This is one homogeneous equation on the two-dimensional coordinate
complement of `e_i`.  Put

```text
beta^(i)=sum_(j!=i) v_j^(i)y_j.                     (10)
```

The independence just proved makes `beta^(i)` nonzero.  The matrix
functional

```text
M |-> e_i^T M v^(i)                                 (11)
```

kills `Delta` by `v_i^(i)=0` and kills `f` by (9).  Applying (11) to every
pair map gives

```text
x_(s,i) tensor beta_t^(i)+beta_s^(i) tensor x_(t,i)=0.
```

Lemma 1 proves the first bound in (8).  The column-null transposed argument
proves the second. `square`

### Corollary 2.1 (uniform effective dimension twelve)

Let

```text
V_t^eff=V_t/(ker X_t intersect ker Y_t).             (12)
```

After deleting zero effective labels,

```text
# {t:V_t^eff!=0}<=12,          sum_t dim V_t^eff<=12. (13)
```

#### Proof

There are at most six left-active and six right-active labels by (8).  Also

```text
dim V_t^eff
 =dim span{x_(t,0),x_(t,1),x_(t,2),
           y_(t,0),y_(t,1),y_(t,2)}.                (14)
```

Summing (14) is bounded by the total number of nonzero local coordinate
forms.  The two shores contribute at most `3*2` each.  Joint-kernel vectors
and zero labels contribute no pair image, so their removal changes neither
(3) nor any later conclusion. `square`

The two-label bound in Lemma 1 is sharp: scalar families
`beta=(1,1)`, `alpha=(1,-1)` attain it.  Singleton support imposes no internal
proportionality.  In characteristic two, three equal scalar labels show why
the stated characteristic gate is necessary.

## 2. Arbitrary-dimensional two-block theorem

Let `U,V` be finite-dimensional and let

```text
X_U,Y_U:U->K^3,             X_V,Y_V:V->K^3.
```

Set

```text
M(u,v)=X_U(u)Y_V(v)^T+X_V(v)Y_U(u)^T.               (15)
```

### Theorem 3 (two-block diagonal span)

If the off-diagonal part of every matrix in (15) lies in one fixed line
`Kf`, then its three diagonal coordinate bilinear forms span a space of
dimension at most two.

The statement also holds for `f=0` and covers arbitrary block dimensions and
rank drops.

#### Proof: determinant equation

If `f=0`, every `M` is diagonal and has rank at most two, so
`D_0D_1D_2=0` in the polynomial domain `K[U,V]`; one `D_i` vanishes.
Assume `f!=0`.  A fixed nonzero entry of `f` defines a unique bilinear form
`L` with

```text
M=diag(D_0,D_1,D_2)+L f.                            (16)
```

This divides only by a fixed nonzero field element, not a parameter.  Extend
scalars to an algebraic closure; all relevant dimensions and identities are
preserved.  Put

```text
alpha=f_12 f_21,       beta=f_02 f_20,
gamma=f_01 f_10,
tau=f_01 f_12 f_20+f_02 f_10 f_21.                  (17)
```

Because (15) is a sum of two rank-one matrices, its determinant vanishes.
Thus

```text
P_f(D_0,D_1,D_2,L)=0,                               (18)

P_f(x,y,z,l)
 =xyz-l^2(alpha x+beta y+gamma z)+tau l^3.          (19)
```

#### Proof: projective bilinear-image lemma

For a bilinear map `Phi:U times V->R`, let `Z` be the projective closure of
its nonzero pure values.  If its values span a vector space of dimension at
least three, then

```text
dim Z>=2.                                            (20)
```

Indeed, assume `dim Z<=1`.  A fixed-`u` image of rank at least three supplies
a plane in `Z`.  A rank-two fixed image supplies a line; irreducibility of
the pure-image closure then makes the curve `Z` that line, contradicting a
span of dimension at least three.  Hence every fixed-`u` map has rank at
most one.

A linear space of rank-at-most-one tensors has either a common target factor
or a common source factor.  To see this, compare a fixed nonzero
`a tensor p` with every `b tensor q`; rank at most one of their sum forces
`a,b` or `p,q` to be proportional.  One nonproportional first factor then
forces every second factor onto the same line, and otherwise all first
factors share a line.  The first alternative makes `Z` a point.  The second
writes `Phi(u,v)=ell(v)psi(u)`, making `Z` projective linear; under the
assumed dimension bound it is a point or line.  Both alternatives contradict
the span hypothesis, proving (20).

#### Proof: reducible determinant cubic

The cubic (19) is reducible exactly when, after permuting colours,

```text
beta=gamma=tau=0,
P_f=x(yz-alpha l^2).                                 (21)
```

Any cubic factorization has a linear factor.  At `l=0` that factor divides
`xyz`, so after permutation and scaling it is `x+c l`.  Substituting
`x=-c l` in (19) gives

```text
-c l y z-beta l^2 y-gamma l^2 z+(c alpha+tau)l^3.
```

It vanishes identically exactly when `c=beta=gamma=tau=0`, proving (21) and
its cyclic mates.

On the irreducible parameter domain `K[U,V]`, equation (18) and (21) give
either `D_0=0` or

```text
D_1D_2=alpha L^2.                                   (22)
```

If `alpha=0`, one of `D_1,D_2` vanishes.  Assume `alpha!=0`.  If `L=0`,
then (22) again gives `D_1D_2=0`, so one diagonal form vanishes.  It remains
only to consider `L,D_1,D_2` all nonzero.  Unique factorization, with the
bidegree in the `U` and `V` variables, then writes

```text
D_1=c g a^2,       D_2=d g b^2,       L=e g a b,
cd=alpha e^2.                                        (23)
```

All three left sides have bidegree `(1,1)`.  Hence
`deg g+2deg a=deg g+2deg b=(1,1)`.  Nonnegative integral bidegrees force
`a,b` to be constants.  Thus `D_1,D_2,L` are proportional, and the three
diagonal forms lie in `span{D_0,g}`.

#### Proof: irreducible determinant cubic

Suppose now that `P_f` is irreducible.  Its projective cubic surface contains
only finitely many lines.  Here is a direct proof.

In `l=0`, the surface is `xyz=0`, so its only contained lines are the three
coordinate lines.  A line not contained in `l=0` can be written

```text
[x:y:z:l]
 =[a s+x_0 t:b s+y_0 t:c s+z_0 t:t].                (24)
```

Substitution in (19) gives

```text
abc=0,
ab z_0+ac y_0+bc x_0=0,
a y_0z_0+b x_0z_0+c x_0y_0
  -(alpha a+beta b+gamma c)=0,
x_0y_0z_0-(alpha x_0+beta y_0+gamma z_0)+tau=0.     (25)
```

If exactly two direction coordinates are nonzero, say `a,b!=0,c=0`, then
`z_0=0` and

```text
alpha a+beta b=0,        alpha x_0+beta y_0=tau.    (26)
```

When `(alpha,beta)!=0`, (26) gives at most one projective direction and one
line modulo translation along it.  When `alpha=beta=0`, it gives no line if
`tau!=0`, while `tau=0` makes `P_f=z(xy-gamma l^2)`, reducible.  The other
two support choices are cyclic.

If exactly one direction coordinate is nonzero, say `a!=0`, equations (25)
reduce, modulo translation in `x_0`, to

```text
y_0z_0=alpha,             beta y_0+gamma z_0=tau.   (27)
```

For `alpha!=0`, elimination gives

```text
beta y_0^2-tau y_0+gamma alpha=0.                   (28)
```

It has finitely many roots unless `beta=gamma=tau=0`, the reducible
`x(yz-alpha l^2)` case.  For `alpha=0`, the branches `y_0=0` and `z_0=0`
are finite unless respectively `gamma=tau=0` or `beta=tau=0`; those are the
cyclic reducible cases.  Thus an irreducible `P_f` has finitely many lines.

Assume the three `D_i` independent and define

```text
Phi=(D_0,D_1,D_2,L),          R=span im Phi.         (29)
```

Then `dim R` is three or four, and (20) makes its projective image closure a
surface.  If `dim R=3`, the closure is the whole projective plane `P(R)`, so
the cubic contains a plane and is reducible.  If `dim R=4`, the closure is
the cubic surface.  No fixed-`u` image can have rank three because the cubic
contains no plane.  If every fixed image has rank at most one, the rank-one
space classification either reduces `dim R` or makes the pure image all of
`P^3`, both impossible.  Hence a dense open set of `u` supplies lines on the
cubic.

There are only finitely many such lines.  For each, the condition that a
fixed-`u` image lie in its vector two-space is Zariski closed.  A finite union
of these closed sets contains the dense rank-two locus, hence its closure is
all of `P(U)`.  Irreducibility of `P(U)` forces one member of the finite union
to be all of `P(U)`, so one line contains every fixed image, contradicting
`dim R=4`.  Here the pure-image closure is irreducible because it is the
closure of the image of the nonzero-value open subset of
`P(U) times P(V)`.  This completes the irreducible case and Theorem 3.
`square`

## 3. All-cut and triangle consequences

For each pair let `D_(s,t)` be the diagonal projection of
`im mu_(s,t)` along the fixed excess line.

### Corollary 3.1 (every cut has diagonal rank at most two)

For every bipartition `A disjoint-union C=T`, one has

```text
dim sum_(s in A,t in C) D_(s,t)<=2.                 (30)
```

#### Proof

On `U=direct-sum_(s in A)V_s` and `V=direct-sum_(t in C)V_t`, sum the maps
on each shore.  The resulting two-block map is exactly

```text
sum_(s in A,t in C) mu_(s,t)(u_s,v_t).              (31)
```

Its diagonal image is exactly the sum in (30): isolate any component pair
for the reverse inclusion.  Theorem 3 applies. `square`

### Theorem 4 (triangle localization and external diagonal silence)

Under (2)--(3), there are three distinct labels, renamed `0,1,2`, such that

```text
D_(0,1), D_(0,2), D_(1,2)                           (32)
```

are independent lines whose direct sum is `Delta`.  Every other edge has
zero diagonal image.

#### Proof

Choose three actual pair outputs with independent diagonal projections and
form the graph of their three supporting label edges.  If this graph were
bipartite, one label cut would cross all three edges, contradicting (30).
A loopless graph with three edges is nonbipartite only when those edges form
a triangle.

The three vertex cuts show that the sum of each two triangle edge-spaces has
dimension at most two.  If one edge-space had dimension two, the other two
chosen basis vectors would both lie in it, contradicting independence.
Thus the three spaces in (32) are independent lines.

Let `x` be outside the triangle.  The cuts `{0}`, `{0,1}`, and `{0,2}` put
`D_(0,x)` respectively in

```text
span(D_(0,1),D_(0,2)),
span(D_(0,2),D_(1,2)),
span(D_(0,1),D_(1,2)).                              (33)
```

The intersection of the three planes in (33) is zero, so `D_(0,x)=0`.
The same argument handles edges from `x` to vertices `1,2`.

For two outside labels `x,y`, the cuts `{0,x}`, `{1,x}`, and `{2,x}` put
`D_(x,y)` in the three coordinate planes spanned by pairs of the independent
lines in (32).  Their intersection is zero.  Hence every nontriangle edge
has zero diagonal image. `square`

### Corollary 4.1 (exhaustive fourth-direction fork)

At least one of the following holds:

1. one triangle pair image has dimension two inside
   `D_(i,j) direct-sum Kf`; or
2. one nontriangle pair has a nonzero image contained in `Kf`.

#### Proof

If every triangle image were one-dimensional and every nontriangle image
zero, all pair images would span only the direct sum of the three independent
diagonal edge lines, of dimension three.  This contradicts (3).  Theorem 4
gives the asserted locations of every possible extra direction. `square`

## 4. Exact sharpness and no-go boundary

Put

```text
p_0=(0,1,1),       p_1=(1,0,1),       p_2=(1,1,0),
z_i=(p_i,p_i),
```

and let `f` have all six off-diagonal entries equal to one.  Direct
multiplication gives

```text
mu_(0,1)=f+2r_2,
mu_(0,2)=f+2r_1,
mu_(1,2)=f+2r_0.                                   (34)
```

Thus the global diagonal image can have dimension three.  The three matrices
in (34) span only a three-space: their diagonal projections are independent,
so no nontrivial combination cancels the diagonal and isolates `f`.  This is
not a rank-four full-swallow family or a witness.

The displayed triangle is tangent-locked.  A scalar pair `z=(x,y)` compatible
with the two triangle labels other than `i` satisfies an eight-variable
homogeneous system whose solution is exactly `K(z_i,1,1)`, including the two
off-diagonal proportionality scalars.  For example, at `i=0` it reduces to

```text
x_0=y_0=0,
x_1=x_2=y_1=y_2=lambda_1=lambda_2.                  (35)
```

Compatibility with all three triangle labels is a nine-variable full-rank
system and has only the zero solution.  Hence this exact normal form admits
neither a larger label block nor a fourth compatible scalar label.

Equations (34)--(35) refute the stronger global diagonal-rank-two route but
do not classify every characteristic-zero triangle or eliminate the two
forks of Corollary 4.1.

## 5. Frontier and unresolved remainder

```text
arbitrary-r silent rank-4 complete-pair effective dimension: <=12;
every label-cut diagonal rank:                             <=2;
three-diagonal supply:                 one triangle, other edges silent;
triangle-edge two-dimensional excess:                     OPEN;
external pure-f feeder:                                   OPEN;
all triangle normal forms / tangent locking:               OPEN;
rank-4 silent full-swallow fibre:                           OPEN;
ranks five through rank nine:                              OPEN;
raw escape / nonzero anchor:                               OPEN;
response / synchronization / nuisance / receiver:         OPEN;
arbitrary-r source cover / strategic-node closure:         OPEN;
global Krenn--Gu conjecture:                               UNRESOLVED.
```

The smallest next incidence obligation is now finite-dimensional but not
finite: classify the at-most-twelve-dimensional triangle-edge and pure-`f`
feeder forks without assuming the symmetric sharpness normal form.  Even a
complete rank-four incidence exclusion would leave the wider branches and
all original attachment gates listed above.

## Verification boundary

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_complete_pair_family_structural_degree_cut_and_triangle_localization.py
```

Run the genuinely independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_complete_pair_family_structural_degree_cut_and_triangle_localization.py
```

The primary uses exact symbolic matrices and polynomial identities to replay
the annihilator, determinant expansion, reducibility substitution and degree
constraints, line-parameter coefficients, triangle combinatorics, and
tangent-lock leaves.  The written proof carries the arbitrary-dimensional
reducibility and finite-line conclusions.  The audit imports no project
module or third-party package; it uses separate exact rational polynomial
arithmetic, exhaustive
finite graph/cut checks, and finite-field falsification of the support and
two-block boundaries.  The arbitrary-dimensional theorem is the written
proof, not either finite computation.
